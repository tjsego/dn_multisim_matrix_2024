'''
Composites of Delta-Notch
'''
from process_bigraph import ProcessTypes, Composite
from processes import register_types



def run_composites(core, n_cells=10):
    subcellular_processes = core.query('subcellular')  # TODO -- how do we get the list of possible subcellular processes?
    multicellular_processes = core.query('multicellular')

    for multicell in multicellular_processes:
        for subcell in subcellular_processes:

            document = {
                'tissue': {
                    '_type': 'process',
                    'address': f'{multicell}',
                    'config': {},  # TODO -- get config
                    '_inputs': {},
                    '_outputs': {
                        'neighbor_surface_areas': 'any',
                    },
                    'inputs': {},
                    'outputs': {
                        'neighbor_surface_areas': ['neighbor surface areas'],
                        # this is a map from each cell to ids of its neighbors and their common surface area
                    }
                },
                'cells': {
                    f'{n}': {
                        'cell_process': {
                            '_type': 'process',
                            # 'address': f'{subcell}',
                            'config': {},
                            '_inputs': {
                                'delta_neighbors': 'any',
                            },
                            '_outputs': {
                                'delta': 'any',
                                'notch': 'any'
                            },
                            'inputs': {
                                'delta_neighbors': ['delta neighbors']
                                # this is a scalar value, sum of the delta values of the neighbors
                            },
                            'outputs': {
                                'delta': ['delta'],
                                'notch': ['notch']
                            }
                        }
                    } for n in range(n_cells)
                },
                'cell connecter': {
                    '_type': 'step',
                    'config': {
                        'read_molecules': ['delta'],  # TODO -- this will tell the connector what molecule id to read
                    },
                    '_inputs': {
                        'connections': 'any',
                        'cells': 'any'
                    },
                    '_outputs': {
                        'cell': 'any'
                    },
                    'inputs': {
                        'connections': ['neighbor surface areas'],  # this gives the connectivity
                        'cells': ['cells']  # it sees the cells so it can read the delta values
                    },
                    'outputs': {
                        'cell': ['cells']  # this updates the total delta values seen by each cell
                    }
                },
                'neighbor surface areas': {}
            }

            
            sim = Composite({'state': document})
            









if __name__ == '__main__':
    core = ProcessTypes()
    register_types(core)

    run_composites(core)
