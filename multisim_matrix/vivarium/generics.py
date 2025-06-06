from copy import deepcopy
import json
from process_bigraph import deep_merge
import os
from process_bigraph import Process
from simservices.DeltaNotchSimService import DeltaNotchSimService
from vivarium_simservice.processes.simservice_process import SimServiceProcess
from typing import Type

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

        outputs = {}
        for key, method in self.access_methods['outputs'].items():
            # skip disabled ports
            if key in self.process_config['disable_ports']['outputs']:
                continue

            # retrieve the get method and call it
            get_method = getattr(self.service, method)
            outputs[key] = get_method()

        return outputs

    def inputs(self):
        return deepcopy(input_schema_multicellular)

    def outputs(self):
        return deepcopy(output_schema_multicellular)


class DeltaNotchProcess(Process):

    config_schema = deepcopy(config_schema_subcellular)
    service_cls: Type[DeltaNotchSimService] = None

    def __init__(self, config=None, core=None):
        super().__init__(config, core)

        self.service = self.service_cls(**self.config)
        self.service.run()
        self.service.init()
        self.service.start()

    def inputs(self):
        return deepcopy(input_schema_subcellular)

    def outputs(self):
        return deepcopy(output_schema_subcellular)

    def update(self, state, interval):
        self.service.set_delta(state['delta'])
        self.service.set_notch(state['notch'])
        self.service.set_delta_neighbors(state['delta_neighbors'])

        self.service.step()

        # todo: this should implement a set operation but T.J. can't figure out where "_apply": "set" should go
        return {
            'delta': self.service.get_delta() - state['delta'],
            'notch': self.service.get_notch() - state['notch']
        }
