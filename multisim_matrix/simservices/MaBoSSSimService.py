from cc3d import CompuCellSetup
from cc3d.core import MaBoSSCC3D
import numpy as np
from simservice.PySimService import PySimService
from typing import Optional


class MaBoSSSimService(PySimService):

    def __init__(self,
                 bnd_str: str,
                 cfg_str: str,
                 time_step: float = 1.0,
                 time_tick: float = 1.0,
                 discrete_time: bool = False,
                 seed: int = None):
        super().__init__()

        self._bnd_str = bnd_str
        self._cfg_str = cfg_str
        self._time_step = time_step
        self._time_tick = time_tick
        self._discrete_time = discrete_time
        self._seed = seed

        self._sim: Optional[MaBoSSCC3D.maboss_engine_type] = None

    def _run(self):
        pass

    def _init(self):
        seed = self._seed if (self._seed is not None and self._seed >= 0) else int(np.random.randint(0, int(1E6)))
        self._sim = MaBoSSCC3D.maboss_model(bnd_str=self._bnd_str,
                                            cfg_str=self._cfg_str,
                                            time_step=self._time_step,
                                            time_tick=self._time_tick,
                                            discrete_time=self._discrete_time,
                                            seed=seed)
        return self._sim is not None

    def _start(self):
        return True

    def _step(self):
        self._sim.step()

    def _finish(self):
        pass

    def _stop(self, terminate_sim: bool = True):
        pass

    def _check_sim(self):
        if self._sim is None:
            raise RuntimeError('Simulation unavailable')

    # Engine interface

    def get_time(self):
        self._check_sim()
        return self._sim.time

    # Config interface

    def _get_config_generic(self, _attr: str):
        self._check_sim()
        return getattr(self._sim.run_config, _attr)

    def _set_config_generic(self, _attr: str, _val):
        self._check_sim()
        setattr(self._sim.run_config, _attr, _val)

    def get_config_sample_count(self):
        return self._get_config_generic('sample_count')

    def set_config_sample_count(self, _val):
        self._set_config_generic('sample_count', _val)

    def get_config_seed(self):
        return self._get_config_generic('seed')

    def set_config_seed(self, _val):
        self._set_config_generic('seed', _val)

    def get_config_time_tick(self):
        return self._get_config_generic('time_tick')

    def set_config_time_tick(self, _val):
        self._set_config_generic('time_tick', _val)

    def get_config_discrete_time(self):
        return self._get_config_generic('discrete_time')

    def set_config_discrete_time(self, _val):
        self._set_config_generic('discrete_time', _val)

    # Node interface

    def _get_node_generic(self, _attr: str, _name: str):
        self._check_sim()
        return getattr(self._sim[_name], _attr)

    def _set_node_generic(self, _attr: str, _name: str, _val):
        self._check_sim()
        setattr(self._sim[_name], _attr, _val)

    def get_node_is_internal(self, _name: str):
        return self._get_node_generic('is_internal', _name)

    def set_node_is_internal(self, _name: str, _val):
        self._set_node_generic('is_internal', _name, _val)

    def get_node_is_reference(self, _name: str):
        return self._get_node_generic('is_reference', _name)

    def set_node_is_reference(self, _name: str, _val):
        self._set_node_generic('is_reference', _name, _val)

    def get_node_istate(self, _name: str):
        return self._get_node_generic('istate', _name)

    def set_node_istate(self, _name: str, _val):
        self._set_node_generic('istate', _name, _val)

    def get_node_logical_input_expr(self, _name: str):
        return self._get_node_generic('logical_input_expr', _name)

    def set_node_logical_input_expr(self, _name: str, _val):
        self._set_node_generic('logical_input_expr', _name, _val)

    def get_node_rate_down_expr(self, _name: str):
        return self._get_node_generic('rate_down_expr', _name)

    def set_node_rate_down_expr(self, _name: str, _val):
        self._set_node_generic('rate_down_expr', _name, _val)

    def get_node_rate_up_expr(self, _name: str):
        return self._get_node_generic('rate_up_expr', _name)

    def set_node_rate_up_expr(self, _name: str, _val):
        self._set_node_generic('rate_up_expr', _name, _val)

    def get_node_ref_state(self, _name: str):
        return self._get_node_generic('ref_state', _name)

    def set_node_ref_state(self, _name: str, _val):
        self._set_node_generic('ref_state', _name, _val)

    def get_node_state(self, _name: str) -> bool:
        return self._get_node_generic('state', _name)

    def set_node_state(self, _name: str, _val: bool):
        self._set_node_generic('state', _name, _val)

    def get_node_rate_up(self, _name: str):
        return self._get_node_generic('rate_up', _name)

    def get_node_rate_down(self, _name: str):
        return self._get_node_generic('rate_down', _name)

    # Symbol table interface

    def get_symbol_table_val(self, _name: str):
        self._check_sim()
        return self._sim.network.symbol_table[_name]

    def set_symbol_table_val(self, _name: str, _val):
        self._check_sim()
        self._sim.network.symbol_table[_name] = _val
