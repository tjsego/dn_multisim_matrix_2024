import numpy as np
from simservice.PySimService import PySimService
from simservices.PlanarSheetSimService import PlanarSheetSimService
import tissue_forge as tf
from tissue_forge.models.vertex import solver as tfvs
from typing import Dict, Optional

DEF_STEP_SIZE = 1.0
DEF_DT = 0.01
DEF_SHOW = False


class VertexPlanarSheet(PlanarSheetSimService):

    def __init__(self,
                 num_cells_x: int,
                 num_cells_y: int,
                 cell_radius,
                 step_size=DEF_STEP_SIZE,
                 dt=DEF_DT,
                 show=DEF_SHOW):

        PySimService.__init__(self,
                              sim_name='PlanarSheet')
        PlanarSheetSimService.__init__(self,
                                       num_cells_x,
                                       num_cells_y,
                                       cell_radius)

        self._step_size = step_size
        self._dt = dt
        self._show = show
        self._cell_type: Optional[tfvs.SurfaceType] = None

    # PlanarSheetSimService interface

    @classmethod
    def init_arginfo(cls):
        return []

    @classmethod
    def init_kwarginfo(cls):
        """
        Returns information about implementation initialization keyword arguments

        * keyword
        * description
        * type
        * optional flag
        * default value if optional, otherwise None
        """
        result = cls.default_init_kwarginfo()
        result.extend([
            ('step_size', 'Simulation time per service step', float.__name__, True, DEF_STEP_SIZE),
            ('dt', 'Simulation time per simulation step', float.__name__, True, DEF_DT),
            ('show', 'Flag to show simulation in real-time', bool.__name__, True, DEF_SHOW)
        ])
        return result

    def neighbor_surface_areas(self, _cell_id: int) -> Dict[int, float]:
        if not self._cell_type or _cell_id >= len(self._cell_type):
            return {}
        sh = tfvs.SurfaceHandle(_cell_id)
        result = {}
        vertices = [v for v in sh.vertices]
        vertices.append(vertices[0])
        for i in range(len(vertices) - 1):
            va: tfvs.VertexHandle = vertices[i]
            vb = vertices[i + 1]
            dist = va.position.relativePosition(vb.position).length()
            for s in va.shared_surfaces(vb):
                if s == sh:
                    continue
                try:
                    result[s.id] += dist
                except KeyError:
                    result[s.id] = dist
        return result

    # PySimService interface

    def _run(self) -> None:
        pass

    def _init(self) -> bool:

        # Initialize the simulation

        min_dim = min(self.num_cells_x * 2, self.num_cells_y * np.sqrt(3)) * self.cell_radius
        min_cells = 3
        len2cells = min_dim / min_cells

        dim = [(self.num_cells_x + 1) * 2 * self.cell_radius, (self.num_cells_y + 1) * np.sqrt(3) * self.cell_radius,
               len2cells]

        tf.init(windowless=not self._show,
                dim=dim,
                bc={'x': tf.BOUNDARY_FREESLIP, 'y': tf.BOUNDARY_FREESLIP, 'z': tf.BOUNDARY_FREESLIP},
                cells=[int(d / len2cells) + 1 for d in dim],
                dt=self._dt,
                cutoff=self.cell_radius)

        # Create a cell type

        self._cell_type = tfvs.SurfaceType()
        area_constraint = tfvs.SurfaceAreaConstraint(1.0, 1.5 * np.sqrt(3) * self.cell_radius * self.cell_radius)
        area_constraint.thisown = 0
        tfvs.bind.surface(area_constraint, self._cell_type)

        # Initialize the population

        start_pos_x = (self.num_cells_x + 1) / 2
        # Not sure why I need this factor of 1.5, but it seems to work
        # start_pos_y = (self.num_cells_y + 3) * np.cos(np.pi / 3) * np.cos(np.pi / 6)
        start_pos_y = (self.num_cells_y) * np.sqrt(3) / 2
        start_pos = tf.Universe.center - tf.FVector3(start_pos_x, start_pos_y, 0) * self.cell_radius
        tfvs.create_hex2d_mesh(self._cell_type, start_pos, self.num_cells_x, self.num_cells_y, self.cell_radius)

        if tf.err_occurred():
            print(tf.err_get_all())

        return True

    def _start(self) -> bool:
        return True

    def _step(self) -> bool:
        return tf.step(self._step_size) == 0

    def _finish(self) -> None:
        pass


def test():
    sim = VertexPlanarSheet(10, 10, 1.0, show=True)
    # sim = VertexPlanarSheet(4, 9, 1.0, show=True)
    # sim = VertexPlanarSheet(9, 4, 1.0, show=True)
    sim._init()
    tf.system.camera_view_top()
    tf.show()


if __name__ == '__main__':
    test()
