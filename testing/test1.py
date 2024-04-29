from simservices import DeltaNotchSimService, PlanarSheetSimService
from subcellular import MaBoSSDeltaNotch, RoadRunnerDeltaNotch
from multicellular import CenterPlanarSheet, PottsPlanarSheet, VertexPlanarSheet
from typing import List, Tuple

registry_subcellular = {
    'Boolean': {
        'MaBoSS': MaBoSSDeltaNotch
    },
    'ODE': {
        'RoadRunner': RoadRunnerDeltaNotch
    }
}
registry_multicellular = {
    'Center': {
        'Tissue Forge': CenterPlanarSheet
    },
    'Potts': {
        'CompuCell3D': PottsPlanarSheet
    },
    'Vertex': {
        'Tissue Forge': VertexPlanarSheet
    }
}


def create_subcellular(method: str, simulator: str, *args, **kwargs) -> DeltaNotchSimService:
    return registry_subcellular[method][simulator](*args, **kwargs)


def create_multicellular(method: str, simulator: str, *args, **kwargs) -> PlanarSheetSimService:
    return registry_multicellular[method][simulator](*args, **kwargs)


def query_subcellular(method: str, simulator: str):
    service = registry_subcellular[method][simulator]
    return service.init_arginfo(), service.init_kwarginfo()


def query_multicellular(method: str, simulator: str):
    service = registry_multicellular[method][simulator]
    return service.init_arginfo(), service.init_kwarginfo()


def launch_models(subcellular_method: str,
                  multicellular_method: str,
                  subcellular_simulator: str,
                  multicellular_simulator: str,
                  subcellular_args,
                  subcellular_kwargs,
                  multicellular_args,
                  multicellular_kwargs) -> Tuple[List[DeltaNotchSimService], PlanarSheetSimService]:
    try:
        num_cells_x = multicellular_kwargs['num_cells_x']
        num_cells_y = multicellular_kwargs['num_cells_y']
        cell_radius = multicellular_kwargs['cell_radius']
    except KeyError:
        print('Must specify num_cells_x, num_cells_y, and cell_radius')
        raise KeyError('Must specify num_cells_x, num_cells_y, and cell_radius in multicellular keyword arguments')

    subcellulular_services = [
        create_subcellular(subcellular_method, subcellular_simulator, *subcellular_args, **subcellular_kwargs) for _ in
        range(num_cells_x * num_cells_y)]
    multicellular_service = create_multicellular(multicellular_method, multicellular_simulator, *multicellular_args,
                                                 **multicellular_kwargs)
    return subcellulular_services, multicellular_service


def integrate_models(subcellulular_services: List[DeltaNotchSimService], multicellular_service: PlanarSheetSimService):
    # Update neighbor delta in each subcellular model

    for i, ss in enumerate(subcellulular_services):
        nbs_info = multicellular_service.neighbor_surface_areas(i)
        d_tot = 0
        nbs_tot = 0
        for j, nbs_area in nbs_info.items():
            d_tot += subcellulular_services[j].get_delta()
            nbs_tot += nbs_area
        ss.set_delta_neighbors(d_tot, nbs_tot)

    # Step each subcellular model

    [ss.step() for ss in subcellulular_services]

    # Note: if the multicellular model used the delta notch models to determine cell behaviors,
    #   then those routines would be implemented here

    # Step the multicellular model
    multicellular_service.step()


def test_query():
    for k, v in registry_subcellular.items():
        print('Method:', k)
        for name in v.keys():
            print('\tSimulator:', name)
            aa, ka = query_subcellular(k, name)
            print('\t\tPosition arguments:')
            [print('\t\t\t', aaa) for aaa in aa]
            print('\t\tKeyword arguments:')
            [print('\t\t\t', kaa) for kaa in ka]
    for k, v in registry_multicellular.items():
        print('Method:', k)
        for name in v.keys():
            print('\tSimulator:', name)
            aa, ka = query_multicellular(k, name)
            print('\t\tPosition arguments:')
            [print('\t\t\t', aaa) for aaa in aa]
            print('\t\tKeyword arguments:')
            [print('\t\t\t', kaa) for kaa in ka]


def main():
    return test_query()


if __name__ == '__main__':
    main()
