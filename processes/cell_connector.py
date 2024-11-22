from process_bigraph import Step


class CellConnector(Step):
    """
    Takes a map of cell neighborhoods from the multicell simulator,
    retrieves the shared surface area between each cell and its neighbor,
    gets the delta values, and multiplie by the shared surface area,
    and sums these up to get total delta from neighbors.
    """
    config_schema = {}

    def __init__(self, config, core=None):
        super().__init__(config, core)

    def inputs(self):
        return {
            "connections": "any",
            "cells": "any"
        }

    def outputs(self):
        return {
            "cells": "any"
        }

    def update(self, inputs):
        connections = inputs["connections"]
        cells = inputs["cells"]

        return {}
