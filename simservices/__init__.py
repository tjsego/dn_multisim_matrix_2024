import antimony
from .DeltaNotchSimService import DeltaNotchSimService
from .MaBoSSSimService import MaBoSSSimService
from .PlanarSheetSimService import PlanarSheetSimService
from .RoadRunnerSimService import RoadRunnerSimService


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
