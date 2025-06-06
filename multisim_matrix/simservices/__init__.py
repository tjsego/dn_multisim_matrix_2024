import antimony
from .DeltaNotchSimService import DeltaNotchSimService
from .MaBoSSSimService import MaBoSSSimService
from .PlanarSheetSimService import PlanarSheetSimService
from .RoadRunnerSimService import RoadRunnerSimService
from .CenterPlanarSheet import CenterPlanarSheet
from .PottsPlanarSheet import PottsPlanarSheet
from .VertexPlanarSheet import VertexPlanarSheet

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


def antimony_to_sbml(model_str: str):
    antimony.clearPreviousLoads()
    if antimony.loadString(model_str) == -1:
        raise RuntimeError(antimony.getLastError())
    module_name = antimony.getMainModuleName()
    if not module_name:
        raise RuntimeError(antimony.getLastError())
    sbml_model_str = antimony.getSBMLString()
    if not sbml_model_str:
        raise RuntimeError(antimony.getLastError())
    return sbml_model_str
