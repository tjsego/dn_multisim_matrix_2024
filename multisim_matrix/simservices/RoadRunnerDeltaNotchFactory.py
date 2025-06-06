from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory
from .RoadRunnerDeltaNotch import RoadRunnerDeltaNotch

SERVICE_NAME = 'RoadRunnerDeltaNotch'


class RoadRunnerDeltaNotchServiceWrap(TypeProcessWrap):
    _process_cls = RoadRunnerDeltaNotch


ServiceManagerLocal.register_service(SERVICE_NAME, RoadRunnerDeltaNotchServiceWrap)


def roadrunner_delta_notch_simservice(*args, **kwargs):
    return process_factory(SERVICE_NAME, *args, **kwargs)
