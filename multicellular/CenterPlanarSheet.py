import numpy as np
from simservice.PySimService import PySimService
from simservices.PlanarSheetSimService import PlanarSheetSimService
import tissue_forge as tf
from typing import Dict, Optional

# Total area: pi * d
# Nominal neighborhood: 6 neighbors perfectly in contact
# Note that TF searches for neighbors from the surface of a particle of interest

neighbor_cutoff_cd = 1.5


def neighbor_area(cell_diameter: float, dist: float):
    mag = np.pi * cell_diameter / 6

    cutoff = neighbor_cutoff_cd * cell_diameter
    if dist < cell_diameter:
        return mag
    elif dist > cutoff:
        return 0.0

    cf = 1.0 - (dist - cell_diameter) / (cutoff - cell_diameter)
    return mag * cf * cf


DEF_STEP_SIZE = 1.0
DEF_DT = 0.01
DEF_SHOW = False


class CenterPlanarSheet(PlanarSheetSimService):

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
        self._cell_type: Optional[tf.ParticleType] = None

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

    def _neighbor_surface_areas(self, _cell_id: int) -> Dict[int, float]:
        if not self._cell_type or _cell_id >= len(self._cell_type):
            return {}
        ph = tf.ParticleHandle(_cell_id)
        cell_diameter = ph.radius * 2
        return {nh.id: neighbor_area(cell_diameter, ph.relativePosition(nh.position).length()) for nh in
                ph.neighbors(distance=neighbor_cutoff_cd * cell_diameter - ph.radius)}

    def neighbor_surface_areas(self) -> Dict[int, Dict[int, float]]:
        return {ph.id: self._neighbor_surface_areas(ph.id) for ph in self._cell_type}

    # PySimService interface

    def _run(self) -> None:
        pass

    def _init(self) -> bool:

        # Initialize the simulation

        min_dim = min(self.num_cells_x, self.num_cells_y) * np.sqrt(3) * self.cell_radius
        min_cells = 3
        len2cells = min_dim / min_cells

        dim = [self.num_cells_x * self.cell_radius, self.num_cells_y * np.sqrt(3) * self.cell_radius, len2cells]

        tf.init(windowless=not self._show,
                dim=dim,
                bc={'x': tf.BOUNDARY_FREESLIP, 'y': tf.BOUNDARY_FREESLIP, 'z': tf.BOUNDARY_FREESLIP},
                cells=[int(d / len2cells) + 1 for d in dim],
                dt=self._dt,
                cutoff=2 * self.cell_radius * 1.5)

        # Create a cell type

        self._cell_type = tf.ParticleType()
        self._cell_type.thisown = 0
        self._cell_type.radius = self.cell_radius
        self._cell_type.dynamics = tf.Overdamped
        self._cell_type.frozen_z = True

        # Add potentials

        pot_contact = tf.Potential.morse(d=1E-5,
                                         a=5,
                                         r0=2 * self._cell_type.radius,
                                         min=0,
                                         max=4 * self._cell_type.radius,
                                         shifted=False)
        pot_contact.thisown = 0
        # tf.bind.types(pot_contact, self._cell_type, self._cell_type)

        # Add some noise

        rforce = tf.Force.random(1E-3, 0.0)
        rforce.thisown = 0
        # tf.bind.force(rforce, self._cell_type)

        # Initialize the population

        uc = tf.lattice.hex2d(0.99, self._cell_type)
        n = [self.num_cells_x, self.num_cells_y, 1]
        cell_half_size = (uc.a1 + uc.a2 + uc.a3) / 2
        extents = n[0] * uc.a1 + n[1] * uc.a2 + n[2] * uc.a3
        offset = tf.FVector3(0.0, 0.0, 0.0)
        origin = tf.Universe.center + offset - extents / 2 + cell_half_size
        origin[1] -= np.sqrt(3) / 4 * self._cell_type.radius
        tf.lattice.create_lattice(uc, n, origin=origin)

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
    sim = CenterPlanarSheet(10, 10, 1.0, show=True)
    # sim = CenterPlanarSheet(4, 9, 1.0, show=True)
    # sim = CenterPlanarSheet(9, 4, 1.0, show=True)
    sim._init()
    tf.system.camera_view_top()
    tf.show()


if __name__ == '__main__':
    test()
