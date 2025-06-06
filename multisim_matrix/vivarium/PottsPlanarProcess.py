from .generics import *

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_planar_potts.json'), 'r') as f:
    config_data = json.load(f)

config_schema = deepcopy(config_schema_multicellular)
config_schema.update(config_data['config_schema'])


class PottsPlanarProcess(MulticellularPlanarProcess):

    config_schema = config_schema_generator(config_schema)
    service_name = config_data['service_name']

