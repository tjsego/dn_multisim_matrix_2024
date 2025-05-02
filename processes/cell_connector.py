import random
from process_bigraph import Step


class CellConnector(Step):
    """
    Takes a map of cell neighborhoods from the multicell simulator,
    retrieves the shared surface area between each cell and its neighbor,
    gets the delta values, and multiply by the shared surface area,
    and sums these up to get total delta from neighbors.
    """
    config_schema = {
        'initial_deltas': {
            '_type': 'list',
            '_element': 'float',
            '_default': [0, 1]}}

    def __init__(self, config, core=None):
        super().__init__(config, core)

    def inputs(self):
        return {
            "connections": "neighborhood_surface_areas",
            "cells": "map[delta:float]"
        }

    def outputs(self):
        return {
            "cells": "map[delta_neighbors:float|delta:float]"
            # "cells": {  # "map[delta_neighbors_store:float]":
            #     "_type": "map",
            #     "_value": {
            #         # "delta store": "float",
            #         "delta_neighbors_store": "float"
            #     }
            # }
        }

    def calculate_delta_neighbors(self, cell_deltas, cell_id, connection):
        delta = 0
        for neighbor_id, surface_area in connection.items():
            delta += cell_deltas[neighbor_id] * surface_area
        return delta
        

    def update(self, inputs):
        connections = inputs["connections"]
        cells = inputs["cells"]

        cell_updates = {}

        existing_connections = set(connections.keys())
        existing_cells = set(cells.keys())

        new_cell_ids = existing_connections - existing_cells
        remove_cell_ids = existing_cells - existing_connections
        remaining_cells = existing_cells - remove_cell_ids

        cell_deltas = {
            cell_id: cells[cell_id]['delta']
            for cell_id in remaining_cells}

        for cell_id in new_cell_ids:
            cell_deltas[cell_id] = random.choice(
                self.config['initial_deltas'])

        cell_updates['_remove'] = list(remove_cell_ids)
        cell_updates['_add'] = {
            cell_id: {
                'delta': cell_deltas[cell_id],
                'delta_neighbors': self.calculate_delta_neighbors(
                    cell_deltas, cell_id, connections[cell_id])}
            for cell_id in new_cell_ids}

        for cell_id in remaining_cells:
            delta = self.calculate_delta_neighbors(
                cell_deltas, cell_id, connections[cell_id])
            cell_updates[cell_id] = {
                'delta_neighbors': delta}

        import ipdb; ipdb.set_trace()

        return {
            "cells": cell_updates
        }
