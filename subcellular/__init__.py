from .MaBoSSDeltaNotch import MaBoSSDeltaNotch
from .RoadRunnerDeltaNotch import RoadRunnerDeltaNotch

from simservice.managers import ServiceManagerLocal
from simservice.service_wraps import TypeProcessWrap
from simservice.service_factory import process_factory


class MaBoSSDeltaNotchWrap(TypeProcessWrap):
    _process_cls = MaBoSSDeltaNotch


class RoadRunnerDeltaNotchWrap(TypeProcessWrap):
    _process_cls = RoadRunnerDeltaNotch


ServiceManagerLocal.register_function("MaBoSSDeltaNotch", MaBoSSDeltaNotchWrap)
ServiceManagerLocal.register_function("RoadRunnerDeltaNotch", RoadRunnerDeltaNotchWrap)


def delta_notch_maboss(*args, **kwargs):
    return process_factory("MaBoSSDeltaNotch", *args, **kwargs)


def delta_notch_roadrunner(*args, **kwargs):
    return process_factory("RoadRunnerDeltaNotch", *args, **kwargs)
