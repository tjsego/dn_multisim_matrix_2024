import json
import os

from .CenterPlanarProcess import CenterPlanarProcess
from .MaBoSSDeltaNotchProcess import MaBoSSDeltaNotchProcess
from .PottsPlanarProcess import PottsPlanarProcess
from .RoadRunnerDeltaNotchProcess import RoadRunnerDeltaNotchProcess
from .VertexPlanarProcess import VertexPlanarProcess

__processes__ = [
    CenterPlanarProcess,
    MaBoSSDeltaNotchProcess,
    PottsPlanarProcess,
    RoadRunnerDeltaNotchProcess,
    VertexPlanarProcess
]


def register_processes(core):
    [core.register(p.__name__, p) for p in __processes__]
    return core


def register_types(core):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'type_info.json'), 'r') as f:
        for d in json.load(f):
            core.register(*d)
