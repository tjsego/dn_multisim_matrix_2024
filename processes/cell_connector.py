from process_bigraph import Step


class CellConnector(Step):
    """
    Takes a map of cell neighborhoods from the multicell simulator,
    retrieves the shared surface area between each cell and its neighbor,
    gets the delta values, and multiply by the shared surface area,
    and sums these up to get total delta from neighbors.
    """
    config_schema = {}

    def __init__(self, config, core=None):
        super().__init__(config, core)

    def inputs(self):
        return {
            "connections": "neighborhood_surface_areas",
            "cells": "map[delta:float]"
        }

    def outputs(self):
        return {
            "cells": "map[delta_neighbors:float]"
            # "cells": {  # "map[delta_neighbors_store:float]":
            #     "_type": "map",
            #     "_value": {
            #         # "delta store": "float",
            #         "delta_neighbors_store": "float"
            #     }
            # }
        }

    def update(self, inputs):
        connections = inputs["connections"]
        cells = inputs["cells"]

        cell_updates = {}
        for cell_id, cell in cells.items():
            delta = 0
            if cell_id in connections:
                for neighbor_id, surface_area in connections[cell_id].items():
                    delta += cells[neighbor_id]["delta"] * surface_area
            cell_updates[cell_id] = {"delta_neighbors": delta}

        return {
            "cells": cell_updates
        }
