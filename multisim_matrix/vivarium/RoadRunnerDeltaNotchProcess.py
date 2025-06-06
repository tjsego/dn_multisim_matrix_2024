from .generics import *
from subcellular.RoadRunnerDeltaNotch import RoadRunnerDeltaNotch

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_subcellular_roadrunner.json'), 'r') as f:
    config_data = json.load(f)

config_schema = deepcopy(config_schema_subcellular)
config_schema.update(config_data['config_schema'])


class RoadRunnerDeltaNotchProcess(DeltaNotchProcess):

    config_schema = deepcopy(config_schema)
    service_cls = RoadRunnerDeltaNotch
