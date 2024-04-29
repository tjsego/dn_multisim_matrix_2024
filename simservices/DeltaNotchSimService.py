import abc
from simservice.PySimService import PySimService
from typing import Any, List, Tuple


class DeltaNotchSimService(PySimService, abc.ABC):

    @abc.abstractclassmethod
    def init_arginfo(cls) -> List[Tuple[str, str]]:
        """
        Returns information about implementation initialization positional arguments

        * description
        * type
        """
        raise NotImplemented

    @abc.abstractclassmethod
    def init_kwarginfo(cls) -> List[Tuple[str, str, str, bool, Any]]:
        """
        Returns information about implementation initialization keyword arguments

        * keyword
        * description
        * type
        * optional flag
        * default value if optional, otherwise None
        """
        raise NotImplemented

    @abc.abstractmethod
    def get_delta(self) -> float:
        raise NotImplemented

    @abc.abstractmethod
    def set_delta(self, _val: float):
        raise NotImplemented

    @abc.abstractmethod
    def get_notch(self) -> float:
        raise NotImplemented

    @abc.abstractmethod
    def set_notch(self, _val: float):
        raise NotImplemented

    @abc.abstractmethod
    def set_delta_neighbors(self, _d_tot: float, _num_nbs: int):
        raise NotImplemented
