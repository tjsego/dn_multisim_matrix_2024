"""
Composites of Delta-Notch
"""
# from bigraph_viz.dict_utils import deep_merge
from process_bigraph import ProcessTypes, Composite
from bigraph_schema.registry import deep_merge_copy
from processes import register_types
# from bigraph_viz import plot_bigraph, replace_regex_recursive
import processes



def run_composites(core):

    # TODO -- maka this work:
    # subcellular_processes = core.query("subcellular")  # TODO -- how do we get the list of possible subcellular processes?
    # multicellular_processes = core.query("multicellular")
    # TODO -- consider making subcellular simulators typical processes; startup for potentially 100s of services will be expensive without adding much value
    num_cells_x = 10
    num_cells_y = 10
    cell_radius = 5
    n_initial_cells = num_cells_x * num_cells_y
    step_size = 1.0  # time of one step in process bigraph engine
    dt = 1.0         # the period of time step according to tissue forge
    assert step_size >= dt, "The time step of the process bigraph engine must be greater than or equal to the time step of tissue forge"

    multicellular_startup_settings = {
        "local:CenterPlanarProcess": {
            "step_size": step_size,
            "dt": dt,
        },
        "local:PottsPlanarProcess": {},
        "local:VertexPlanarProcess": {
            "step_size": step_size,
            "dt": dt
        },
    }
    subcellular_startup_settings = {
        "local:MaBoSSDeltaNotchProcess": {
            "time_step": dt,
            "time_tick": step_size,
            "discrete_time": True,
            "seed": 0
        },
        "local:RoadRunnerDeltaNotchProcess": {
            "step_size": dt,
            "num_steps": int(step_size/dt),
            "stochastic": False,
            "seed": 0
        }
    }

    # general config settings
    multicell_config = {
        "num_cells_x": num_cells_x,
        "num_cells_y": num_cells_y,
        "cell_radius": cell_radius
    }
    subcellular_config = {}

    # go through all the combinations of multicellular and subcellular processes
    for multicell_address, multicell_settings in multicellular_startup_settings.items():
        for subcell_address, subcell_settings in subcellular_startup_settings.items():

            # merge specific simulator settings with the general settings
            multicell_config_merged = deep_merge_copy(
                {"simservice_config": multicell_config}, multicell_settings)
            subcellular_config_merged = deep_merge_copy(
                {"simservice_config": subcellular_config}, subcell_settings)
            
            # make the document
            document = {
                "tissue": {
                    "_type": "process",
                    "address": f"{multicell_address}",
                    "config": multicell_config_merged,
                    "_inputs": {},
                    "_outputs": {
                        "neighborhood_surface_areas": "neighborhood_surface_areas",
                    },
                    "inputs": {},
                    "outputs": {
                        "neighborhood_surface_areas": ["neighborhood surface areas store"],
                        # this is a map from each cell to ids of its neighbors and their common surface area
                    }
                },
                "cells": {
                    f"{n}": {
                        "cell_process": {
                            "_type": "process",
                            "address": f"{subcell_address}",
                            "config": subcellular_config_merged,
                            "_inputs": {
                                "delta_neighbors": "delta",
                            },
                            "_outputs": {
                                "delta": "delta",
                                "notch": "notch"
                            },
                            "inputs": {
                                "delta_neighbors": ["delta neighbors store"]
                                # this is a scalar value, sum of the delta values of the neighbors
                            },
                            "outputs": {
                                "delta": ["delta store"],
                                "notch": ["notch store"]
                            }
                        }
                    } for n in range(n_initial_cells)
                },
                "cell connector": {
                    "_type": "step",
                    "address": "local:CellConnector",
                    "config": {
                        "read_molecules": ["delta"],  # TODO -- this will tell the connector what molecule id to read
                    },
                    "_inputs": {
                        "connections": "any",
                        "cells": "any"
                    },
                    "_outputs": {
                        "cells": "any"
                    },
                    "inputs": {
                        "connections": ["neighbor surface areas"],  # this gives the connectivity
                        "cells": ["cells"]  # it sees the cells so it can read the delta values
                    },
                    "outputs": {
                        "cells": ["cells"]  # this updates the total delta values seen by each cell
                    }
                },
                "neighbor surface areas": {},
            }

            # # plot the composite
            # plot_bigraph(document,
            #              core=core,
            #              remove_process_place_edges=True,
            #              out_dir="out",
            #              filename=f'delta_notch_{multicell_address}_{subcell_address}.png')

            # make the composite
            sim = Composite(
                config={"state": document},
                core=core
            )
            





if __name__ == "__main__":
    core = ProcessTypes()
    register_types(core)

    run_composites(core)
