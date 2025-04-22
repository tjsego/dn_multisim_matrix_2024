import json
import os

# DO NOT REMOVE THESE SEEMINGLY UNUSED IMPORTS!
import multicellular.CenterPlanarSheetFactory
import multicellular.VertexPlanarSheetFactory
import multicellular.PottsPlanarSheetFactory
import subcellular.MaBoSSDeltaNotchFactory
import subcellular.RoadRunnerDeltaNotchFactory


from .CenterPlanarProcess import CenterPlanarProcess
from .MaBoSSDeltaNotchProcess import MaBoSSDeltaNotchProcess
from .PottsPlanarProcess import PottsPlanarProcess
from .RoadRunnerDeltaNotchProcess import RoadRunnerDeltaNotchProcess
from .VertexPlanarProcess import VertexPlanarProcess
from .cell_connector import CellConnector

__processes__ = [
    CenterPlanarProcess,
    MaBoSSDeltaNotchProcess,
    PottsPlanarProcess,
    RoadRunnerDeltaNotchProcess,
    VertexPlanarProcess,
    CellConnector,
]


def register_processes(core):
    [core.register_process(p.__name__, p) for p in __processes__]
    return core


def register_types(core):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'type_info.json'), 'r') as f:
        for d in json.load(f):
            core.register(*d)

    register_processes(core)
    return core