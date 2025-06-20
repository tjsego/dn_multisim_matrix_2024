from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory
from multisim_matrix.simservice.MaBoSSDeltaNotch import MaBoSSDeltaNotch

SERVICE_NAME = 'MaBoSSDeltaNotch'


class MaBoSSDeltaNotchServiceWrap(TypeProcessWrap):
    _process_cls = MaBoSSDeltaNotch


ServiceManagerLocal.register_service(SERVICE_NAME, MaBoSSDeltaNotchServiceWrap)


def maboss_delta_notch_simservice(*args, **kwargs):
    return process_factory(SERVICE_NAME, *args, **kwargs)
