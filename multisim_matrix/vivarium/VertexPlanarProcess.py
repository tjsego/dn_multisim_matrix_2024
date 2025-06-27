
from multisim_matrix.vivarium.generics import *

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas', 'config_planar_vertex.json'), 'r') as f:
    config_data = json.load(f)

config_schema = deepcopy(config_schema_multicellular)
config_schema.update(config_data['config_schema'])

access_methods = deepcopy(access_methods_multicellular)
access_methods['inputs'].update(config_data['access_methods']['inputs'])
access_methods['outputs'].update(config_data['access_methods']['outputs'])


class VertexPlanarProcess(MulticellularPlanarProcess):

    config_schema = config_schema_generator(config_schema)
    access_methods = access_methods
    service_name = config_data['service_name']

    def inputs(self):
        result = super().inputs()
        result.update(config_data['input_schema'])
        return result

    def outputs(self):
        result = super().outputs()
        result.update(config_data['output_schema'])
        return result
