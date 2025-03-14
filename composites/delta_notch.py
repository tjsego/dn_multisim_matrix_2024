"""
Composites of Delta-Notch

TODO -- need to pass in ids for the cells so that we can synchronize.
"""
from process_bigraph import ProcessTypes, Composite, default, gather_emitter_results
from bigraph_schema.registry import deep_merge_copy
from processes import register_types
import processes



def run_composites(core):

    # TODO -- maka this work:
    # subcellular_processes = core.query("subcellular")  # TODO -- how do we get the list of possible subcellular processes?
    # multicellular_processes = core.query("multicellular")
    # TODO -- consider making subcellular simulators typical processes; startup for potentially 100s of services will be expensive without adding much value
    num_cells_x = 2 #4
    num_cells_y = 2 #4
    cell_radius = 5
    n_initial_cells = num_cells_x * num_cells_y
    step_size = 1.0  # time of one step in process bigraph engine
    dt = 1.0         # the period of time step according to tissue forge
    interval = 10.   # the total time to run the simulation
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
                # "neighborhood_surface_areas_store": {
                #     f"{n}": {
                #         f"{m}": 0.0 for m in range(n_initial_cells) if m != n
                #     } for n in range(n_initial_cells)
                # },
                "tissue": {
                    "_type": "process",
                    "address": f"{multicell_address}",
                    "config": multicell_config_merged,
                    "inputs": {},
                    "outputs": {
                        "neighborhood_surface_areas": ["neighborhood_surface_areas"],
                        # this is a map from each cell to ids of its neighbors and their common surface area
                    }
                },
                "cells": {},
                "cell connector": {
                    "_type": "step",
                    "address": "local:CellConnector",
                    "config": {
                        "read_molecules": ["delta"],  # TODO -- this will tell the connector what molecule id to read
                    },
                    "inputs": {
                        "connections": ["neighborhood_surface_areas"],  # this gives the connectivity and surface area
                        "cells": ["cells"]  # it sees the cells so it can read their delta values
                    },
                    "outputs": {
                        "cells": ["cells"]  # this updates the total delta values seen by each cell
                    }
                },
                "neighbor_surface_areas": {},
                "emitter": {
                    "_type": "step",
                    "address": "local:ram-emitter",
                    "config": {
                        "emit": {
                            'cells': 'map[delta:float|notch:float]'
                            # "delta": "delta",
                            # "notch": "notch"
                        }
                    },
                    "inputs": {
                        'cells': ['cells']
                        # # TODO -- make this more general
                        # "delta": ["cells", "0", "delta"],
                        # "notch": ["cells", "0", "notch"]
                    },
                }
            }

            composition = {
                "cells": {
                    "_type": "map",
                    "_value": {
                        "cell_process": {
                            "_type": "process",
                            "address": default("string", f"{subcell_address}"),
                            "config": default("quote", subcellular_config_merged),
                            "inputs": default("tree[wires]", {
                                "delta_neighbors": ["delta_neighbors"]
                            }),
                            "outputs": default("tree[wires]", {
                                "outputs": {
                                    "delta": ["delta"],  # this has to be called delta store for the connector to read it
                                    "notch": ["notch"]
                            }})
                        }
                    },

                }
            }

            # TODO -- set initial state

            # make the composite
            print(f"Building composite with {multicell_address} and {subcell_address}")
            sim = Composite(
                config={"state": document,
                        "composition": composition},
                core=core
            )

            # import ipdb; ipdb.set_trace()

            # run the simulation
            print(f"Running composite with {multicell_address} and {subcell_address}")
            sim.run(interval=interval)

            # retrieve the results
            results = gather_emitter_results(sim)

            # print the results
            # TODO -- is the emitter not wired to the right location
            print(f"Results: {results[('emitter',)]}")


if __name__ == "__main__":
    core = ProcessTypes()
    register_types(core)

    run_composites(core)
