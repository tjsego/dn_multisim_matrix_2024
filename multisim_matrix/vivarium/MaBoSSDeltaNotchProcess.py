from .generics import *
from subcellular.MaBoSSDeltaNotch import MaBoSSDeltaNotch

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_subcellular_maboss.json'), 'r') as f:
    config_data = json.load(f)

config_schema = deepcopy(config_schema_subcellular)
config_schema.update(config_data['config_schema'])


class MaBoSSDeltaNotchProcess(DeltaNotchProcess):

    config_schema = deepcopy(config_schema)
    service_cls = MaBoSSDeltaNotch
