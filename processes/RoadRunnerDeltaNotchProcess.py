from .generics import *

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_subcellular_maboss.json'), 'r') as f:
    config_data = json.load(f)

config_schema = deepcopy(config_schema_subcellular)
config_schema.update(config_data['config_schema'])


class RoadRunnerDeltaNotchProcess(DeltaNotchProcess):

    config_schema = config_schema_generator(config_schema)
    service_name = config_data['service_name']
