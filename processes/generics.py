from copy import deepcopy
import json
from process_bigraph import deep_merge
import os
from vivarium_simservice.processes.simservice_process import SimServiceProcess

_this_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_this_dir, 'config_planar.json'), 'r') as f:
    config_data_multicellular = json.load(f)
with open(os.path.join(_this_dir, 'config_subcellular.json'), 'r') as f:
    config_data_subcellular = json.load(f)

config_schema_multicellular = config_data_multicellular['config_schema']
access_methods_multicellular = config_data_multicellular['access_methods']
input_schema_multicellular = config_data_multicellular['input_schema']
output_schema_multicellular = config_data_multicellular['output_schema']

config_schema_subcellular = config_data_subcellular['config_schema']
access_methods_subcellular = config_data_subcellular['access_methods']
input_schema_subcellular = config_data_subcellular['input_schema']
output_schema_subcellular = config_data_subcellular['output_schema']


def config_schema_generator(_config_schema: dict):
    return deep_merge(
        dct=deepcopy(SimServiceProcess.config_schema),
        merge_dct=deepcopy(_config_schema)
    )


class MulticellularPlanarProcess(SimServiceProcess):

    config_schema = config_schema_generator(config_schema_multicellular)

    access_methods = deepcopy(access_methods_multicellular)

    def initial_state(self):
        # get the initial state from the service
        # feed that state through the ports
        return {}

    def inputs(self):
        return deepcopy(input_schema_multicellular)

    def outputs(self):
        return deepcopy(output_schema_multicellular)


class DeltaNotchProcess(SimServiceProcess):

    config_schema = config_schema_generator(config_schema_subcellular)

    access_methods = deepcopy(access_methods_subcellular)

    def inputs(self):
        return deepcopy(input_schema_subcellular)

    def outputs(self):
        return deepcopy(output_schema_subcellular)

