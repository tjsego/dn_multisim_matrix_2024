import json
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import path as mpath
import numpy as np
import os
from typing import Any, Dict, List

from process_bigraph import Step

SUBDIR_CELL = 'cells'
SUBDIR_DELTA = 'delta'
SUBDIR_NOTCH = 'notch'
SUBDIR_DN = 'dn'
SUBDIRS_RENDER = [
    SUBDIR_CELL,
    SUBDIR_DELTA,
    SUBDIR_NOTCH,
    SUBDIR_DN
]

render_schema_fp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'simservices', 'schema_render.json')
with open(render_schema_fp, 'r') as f:
    render_schema = json.load(f)


def _check_render_specs(_specs: Dict[str, Any]):
    for k, v in render_schema['data'].items():
        if k not in _specs:
            raise KeyError(f'Missing schema data ({k}): {v["description"]}')


class _MCRenderer2D(Step):

    config_schema = {
        'render_specs': 'tree[any]',
        'output_dir': 'string'
    }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._step_count = -1

    def initialize(self, config):
        _check_render_specs(config['render_specs'])
        self.build_output_structure()

    def inputs(self):
        return {
            'cells': 'map[delta:float|notch:float]',
            'cell_spatial_data': 'any'
        }

    def outputs(self):
        return {}

    def update(self, inputs):
        self._step_count += 1

        if 'cell_spatial_data' not in inputs:
            return {}
        cell_spatial_data = inputs['cell_spatial_data']
        if not cell_spatial_data:
            return {}

        self.save_figure(self.render_cells(cell_spatial_data), SUBDIR_CELL)

        if 'cells' not in inputs:
            return {}
        cells = inputs['cells']
        if not cells:
            return {}

        states_delta = {}
        states_notch = {}
        for k, v in cells.items():
            states_delta[int(k)] = v['delta']
            states_notch[int(k)] = v['notch']

        self.save_figure(self.render_state(cell_spatial_data, states_delta), SUBDIR_DELTA)
        self.save_figure(self.render_state(cell_spatial_data, states_notch), SUBDIR_NOTCH)
        self.save_figure(self.render_2state(cell_spatial_data, states_delta, states_notch), SUBDIR_DN)

        return {}

    def build_output_structure(self):
        output_dir = self.config['output_dir']
        for subdir in SUBDIRS_RENDER:
            d = os.path.join(output_dir, subdir)
            if not os.path.isdir(d):
                os.makedirs(d)

    def save_figure(self, fig: plt.Figure, subdir: str):
        render_specs = self.config['render_specs']
        file_extensions: List[str] = render_specs['file_extensions']
        dpi: int = render_specs['dpi']

        subdir_abs = os.path.join(self.config['output_dir'], subdir)
        if not os.path.isdir(subdir_abs):
            raise NotADirectoryError(subdir_abs)

        for fext in file_extensions:
            _fext = fext if fext.startswith('.') else f'.{fext}'
            output_fp = os.path.join(subdir_abs, f'{self._step_count}{_fext}')
            fig.savefig(output_fp,
                        dpi=dpi)

        plt.close(fig)

    def render_cells(self, cell_data) -> plt.Figure:
        raise NotImplementedError

    def render_state(self, cell_data, states) -> plt.Figure:
        raise NotImplementedError

    def render_2state(self, cell_data, states1, states2) -> plt.Figure:
        raise NotImplementedError


class MCCenterRenderer2D(_MCRenderer2D):

    @staticmethod
    def _render_cells(pos_x, pos_y, dim_x, dim_y, radius, cell_c) -> plt.Figure:
        fig, ax = plt.subplots(1, 1, layout='compressed')
        ax.scatter(pos_x, pos_y, s=radius * 2 * 72, c=cell_c, edgecolors='black')
        ax.set_xlim(0, dim_x)
        ax.set_ylim(0, dim_y)
        return fig

    def render_cells(self, cell_data) -> plt.Figure:
        pos_x, pos_y, cell_ids, dim_x, dim_y, radius = cell_data
        return self._render_cells(pos_x, pos_y, dim_x, dim_y, radius, 'red')

    def render_state(self, cell_data, states) -> plt.Figure:
        max_state = max(states.values())
        if max_state <= 0:
            max_state = 1.0

        pos_x, pos_y, cell_ids, dim_x, dim_y, radius = cell_data
        cell_c = [[states[i] / max_state, 0.0, 0.0] for i in cell_ids]

        return self._render_cells(pos_x, pos_y, dim_x, dim_y, radius, cell_c)

    def render_2state(self, cell_data, states1, states2) -> plt.Figure:
        max_state1 = max(states1.values())
        max_state2 = max(states2.values())
        if max_state1 <= 0.0:
            max_state1 = 1.0
        if max_state2 <= 0.0:
            max_state2 = 1.0

        pos_x, pos_y, cell_ids, dim_x, dim_y, radius = cell_data
        cell_c = [[states1[i] / max_state1, states2[i] / max_state2, 0.0] for i in cell_ids]

        return self._render_cells(pos_x, pos_y, dim_x, dim_y, radius, cell_c)


class MCPottsRenderer2D(_MCRenderer2D):

    @staticmethod
    def _render_cells(x, dim_x, dim_y, rendered_x):
        res = 5
        x_res = np.repeat(np.repeat(x, res, axis=0), res, axis=1)
        rendered_x_res = np.repeat(np.repeat(rendered_x, res, axis=0), res, axis=1)

        mask = x_res[:-1, :] != x_res[1:, :]
        rendered_x_res[1:, :][mask] = rendered_x_res[:-1, :][mask] = [0.0, 0.0, 0.0]
        mask = x_res[:, :-1] != x_res[:, 1:]
        rendered_x_res[:, 1:][mask] = rendered_x_res[:, :-1][mask] = [0.0, 0.0, 0.0]

        fig, ax = plt.subplots(1, 1, layout='compressed')
        ax.imshow(rendered_x_res)
        ax.set_xlim(0, dim_x * res - 1)
        ax.set_ylim(0, dim_y * res - 1)
        return fig

    def render_cells(self, cell_data) -> plt.Figure:
        x, dim_x, dim_y = cell_data

        rendered_x = np.zeros((x.shape[0], x.shape[1], 3), dtype=float)
        rendered_x[x > 0] = [1.0, 0.0, 0.0]

        return self._render_cells(x, dim_x, dim_y, rendered_x)

    def render_state(self, cell_data, states) -> plt.Figure:
        max_state = max(states.values())
        if max_state <= 0:
            max_state = 1.0

        x, dim_x, dim_y = cell_data

        rendered_x = np.zeros((x.shape[0], x.shape[1], 3), dtype=float)

        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                cell_id = x[i, j]
                if cell_id > 0:
                    rendered_x[i, j, :] = [states[cell_id - 1] / max_state, 0.0, 0.0]

        return self._render_cells(x, dim_x, dim_y, rendered_x)

    def render_2state(self, cell_data, states1, states2) -> plt.Figure:
        max_state1 = max(states1.values())
        if max_state1 <= 0:
            max_state1 = 1.0
        max_state2 = max(states2.values())
        if max_state2 <= 0:
            max_state2 = 1.0

        x, dim_x, dim_y = cell_data

        rendered_x = np.zeros((x.shape[0], x.shape[1], 3), dtype=float)

        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                cell_id = x[i, j]
                if cell_id > 0:
                    rendered_x[i, j, :] = [states1[cell_id - 1] / max_state1, states2[cell_id - 1] / max_state2, 0.0]

        return self._render_cells(x, dim_x, dim_y, rendered_x)


class MCVertexRenderer2D(_MCRenderer2D):

    @staticmethod
    def _render_cells(points, dim_x, dim_y, colors):
        rendered_points = []
        patches = []
        for pts, clr in zip(points, colors):
            path_data = [(mpath.Path.MOVETO, pts[0])]
            for p in pts[1:]:
                path_data.append((mpath.Path.LINETO, p))
            path_data.append((mpath.Path.CLOSEPOLY, pts[0]))
            codes, verts = zip(*path_data)
            path = mpath.Path(verts, codes)
            rendered_points.append(zip(*path.vertices))
            patches.append(mpatches.PathPatch(path, facecolor=clr))

        fig, ax = plt.subplots(1, 1, layout='compressed')
        [ax.plot(*p, 'ko-') for p in rendered_points]
        [ax.add_patch(patch) for patch in patches]
        ax.set_xlim(0, dim_x)
        ax.set_ylim(0, dim_y)
        return fig

    def render_cells(self, cell_data) -> plt.Figure:
        points, dim_x, dim_y, cell_ids = cell_data
        face_colors = [[1.0, 0.0, 0.0]] * len(cell_ids)
        return self._render_cells(points, dim_x, dim_y, face_colors)

    def render_state(self, cell_data, states) -> plt.Figure:
        max_state = max(states.values())
        if max_state <= 0:
            max_state = 1.0

        points, dim_x, dim_y, cell_ids = cell_data
        face_colors = [[states[cid] / max_state, 0.0, 0.0] for cid in cell_ids]
        return self._render_cells(points, dim_x, dim_y, face_colors)

    def render_2state(self, cell_data, states1, states2) -> plt.Figure:
        max_state1 = max(states1.values())
        if max_state1 <= 0:
            max_state1 = 1.0
        max_state2 = max(states2.values())
        if max_state2 <= 0:
            max_state2 = 1.0

        points, dim_x, dim_y, cell_ids = cell_data
        face_colors = [[states1[cid] / max_state1, states2[cid] / max_state2, 0.0] for cid in cell_ids]
        return self._render_cells(points, dim_x, dim_y, face_colors)
