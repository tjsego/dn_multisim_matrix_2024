import numpy as np
from simservices.PlanarSheetSimService import PlanarSheetSimService
from typing import Dict

from cc3d.core.simservice.CC3DSimService import CC3DSimService
from cc3d.core import PyCoreSpecs as pcs
from cc3d.core.iterators import CellNeighborListFlex


def core_specs(num_cells_x: int,
               num_cells_y: int,
               cell_radius: int):
    area = np.pi * cell_radius * cell_radius
    cell_len = int(np.sqrt(area))
    area = int(area)

    dim_x = num_cells_x * cell_len
    dim_y = num_cells_y * cell_len

    return [
        pcs.PottsCore(dim_x=dim_x,
                      dim_y=dim_y,
                      fluctuation_amplitude=10,
                      neighbor_order=2),
        pcs.CellTypePlugin('TypeA'),
        # pcs.ContactPlugin(4,
        #                   pcs.ContactEnergyParameter('Medium', 'TypeA', 5),
        #                   pcs.ContactEnergyParameter('TypeA', 'TypeA', 5)),
        # pcs.VolumePlugin(pcs.VolumeEnergyParameter('TypeA', area, 5)),
        pcs.UniformInitializer(pcs.UniformInitializerRegion((0, 0, 0),
                                                            (dim_x, dim_y, 1),
                                                            width=cell_len,
                                                            cell_types=['TypeA'])),
        pcs.NeighborTrackerPlugin()
    ]


DEF_OUTPUT_FREQUENCY = 0
DEF_SCREENSHOT_OUTPUT_FREQUENCY = 0
DEF_OUTPUT_DIR = None
DEF_OUTPUT_FILE_CORE_NAME = None


class PottsPlanarSheet(CC3DSimService, PlanarSheetSimService):

    def __init__(self,
                 num_cells_x: int,
                 num_cells_y: int,
                 cell_radius,
                 output_frequency=DEF_OUTPUT_FREQUENCY,
                 screenshot_output_frequency=DEF_SCREENSHOT_OUTPUT_FREQUENCY,
                 output_dir=DEF_OUTPUT_DIR,
                 output_file_core_name=DEF_OUTPUT_FILE_CORE_NAME):

        PlanarSheetSimService.__init__(self, num_cells_x, num_cells_y, cell_radius)
        CC3DSimService.__init__(self,
                                output_frequency=output_frequency,
                                screenshot_output_frequency=screenshot_output_frequency,
                                output_dir=output_dir,
                                output_file_core_name=output_file_core_name,
                                sim_name='PlanarSheet')

        self.register_specs(core_specs(num_cells_x, num_cells_y, cell_radius))

    @staticmethod
    def _get_simulator():
        from cc3d.CompuCellSetup import persistent_globals as pg
        if pg.simulator is None:
            return None
        return pg.simulator

    @staticmethod
    def _get_cell_inventory():
        sim = PottsPlanarSheet._get_simulator()
        if sim is None:
            return None
        potts = sim.getPotts()
        if potts is None:
            return None
        return potts.getCellInventory()

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
            ('output_frequency', 'Steps per data output', int.__name__, True, DEF_OUTPUT_FREQUENCY),
            ('screenshot_output_frequency', 'Steps per screenshot output', int.__name__, True,
             DEF_SCREENSHOT_OUTPUT_FREQUENCY),
            ('output_dir', 'Data output directory', str.__name__, True, DEF_OUTPUT_DIR),
            ('output_file_core_name', 'Data output file core name', str.__name__, True, DEF_OUTPUT_FILE_CORE_NAME)
        ])
        return result

    def neighbor_surface_areas(self, _cell_id: int) -> Dict[int, float]:
        sim = PottsPlanarSheet._get_simulator()
        cinv = PottsPlanarSheet._get_cell_inventory()
        result = {}
        if cinv is None:
            return result

        neighbor_tracker_plugin = sim.pluginManager.getNeighborTrackerPlugin()
        if neighbor_tracker_plugin is None:
            return result

        cell = cinv.attemptFetchingCellById(_cell_id)
        if cell is None:
            return result

        for nbs, csa in CellNeighborListFlex(neighbor_tracker_plugin, cell):
            if nbs:
                result[nbs.id] = csa
        return result


def test():
    sim = PottsPlanarSheet(10, 10, 3)
    sim.run()
    sim.init()
    sim.start()
    sim.visualize()
    input('Press any key to continue...')
    print('Done!')


if __name__ == '__main__':
    test()
