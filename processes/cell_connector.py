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
            "cell_deltas": "map[float]",
            'cells': 'map[delta_notch_cell]'
        }

    def outputs(self):
        return {
            "cell_delta_neighbors": "map[float]",
            'cells': 'map[delta_notch_cell]'
            # "cells": {  # "map[delta_neighbors_store:float]":
            #     "_type": "map",
            #     "_value": {
            #         # "delta store": "float",
            #         "delta_neighbors_store": "float"
            #     }
            # }
        }

    def update(self, inputs):
        # TODO: compare connections input to the cells input and add
        #   and remove cells that are different and report to output cells

        connections = inputs["connections"]
        cell_deltas = inputs["cell_deltas"]

        cell_updates = {}
        for cell_id, cell_delta in cell_deltas.items():
            neighbor_delta = 0
            if cell_id in connections:
                for neighbor_id, surface_area in connections[cell_id].items():
                    neighbor_delta += cell_deltas[neighbor_id] * surface_area # ["delta"] * surface_area
            cell_updates[cell_id] = neighbor_delta # {"delta_neighbors": delta}

        return {
            "cell_delta_neighbors": cell_updates
        }
