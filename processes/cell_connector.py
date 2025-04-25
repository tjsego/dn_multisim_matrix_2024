import numpy as np
from process_bigraph import Step


class CellConnector(Step):
    """
    Takes a map of cell neighborhoods from the multicell simulator,
    retrieves the shared surface area between each cell and its neighbor,
    gets the delta values, and multiply by the shared surface area,
    and sums these up to get total delta from neighbors.
    """

    config_schema = {
        'cells_count': 'integer',
        'read_molecules': 'list[string]'}


    def initial_state(self):
        cells = {
            str(cell_id): {
                'delta_neighbors': 0.0}
            for cell_id in range(self.config['cells_count'])}

        return cells


    def inputs(self):
        return {
            "connections": "neighborhood_surface_areas",
            "cells": "map[delta:float]"
        }


    def outputs(self):
        return {
            "cells": "map[delta_neighbors:float]"
        }


    def update(self, inputs):
        connections = inputs["connections"]
        input_cells = inputs["cells"]

        cell_updates = {}

        connection_ids = set(connections.keys())
        cell_ids = set(input_cells.keys())

        adding = connection_ids - cell_ids
        removing = cell_ids - connection_ids
        keeping = cell_ids - removing

        cell_updates = {
            cell_id: {'delta': np.random.random()}
            for cell_id in adding}
        for keep_id in keeping:
            cell_updates[keep_id] = input_cells[keep_id]

        cell_updates['_remove'] = list(removing)

        for cell_id in connections:
            delta = 0
            for neighbor_id, surface_area in connections[cell_id].items():
                delta += cell_updates[neighbor_id]["delta"] * surface_area
            cell_updates[cell_id]['delta_neighbors'] = delta

        import ipdb; ipdb.set_trace()

        return {
            "cells": cell_updates
        }
