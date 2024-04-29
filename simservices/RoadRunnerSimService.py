from roadrunner import RoadRunner
from simservice.PySimService import PySimService
from typing import Optional


class RoadRunnerSimService(PySimService):

    def __init__(self,
                 model_str: str,
                 step_size=1.0,
                 num_steps=2,
                 stochastic=False,
                 seed: int = None):

        super().__init__()

        self._model_str = model_str
        self._step_size = step_size
        self._num_steps = num_steps
        self._stochastic = stochastic
        self._seed = seed

        self._time = 0.0
        self._sim: Optional[RoadRunner] = None

    def _run(self):
        pass

    def _init(self):
        self._sim = RoadRunner(self._model_str)
        if self._stochastic:
            self._sim.integrator.integrator = 'gillespie'
            if self._seed is not None:
                self._sim.integrator.seed = self._seed
        return True

    def _start(self):
        return True

    def _step(self):
        new_time = self._time + self._step_size
        self._sim.simulate(self._time, new_time, self._num_steps)
        self._time = new_time

    def _finish(self):
        pass

    def _stop(self, terminate_sim: bool = True):
        pass

    # Service interface

    def get_model_str(self):
        return self._model_str

    def get_step_size(self):
        return self._step_size

    def set_step_size(self, _val: float):
        if _val <= 0:
            raise ValueError
        self._step_size = _val

    def get_num_steps(self):
        return self._num_steps

    def set_num_steps(self, _val: int):
        if _val < 2:
            raise ValueError
        self._num_steps = _val

    # RoadRunner interface

    def _check_sim(self):
        if self._sim is None:
            raise RuntimeError('Simulation unavailable')

    def get_rr_val(self, _name: str):
        self._check_sim()
        return self._sim[_name]

    def set_rr_val(self, _name: str, _val):
        self._check_sim()
        self._sim[_name] = _val
