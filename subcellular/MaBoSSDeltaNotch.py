from simservices import DeltaNotchSimService, MaBoSSSimService

bnd_str = """
node delta 
{
    logic = NOT notch;
    rate_up = @logic ? $rate : 0.0;
    rate_down = @logic ? 0.0 : $rate;
}

node notch 
{
    rate_up = $delta_nbs;
    rate_down = $rate;
}
"""

cfg_str = """
$rate=1.0;
"""

DEF_TIME_STEP = 1.0
DEF_TIME_TICK = 1.0
DEF_DISCRETE_TIME = False
DEF_SEED = None


class MaBoSSDeltaNotch(DeltaNotchSimService, MaBoSSSimService):

    def __init__(self,
                 time_step: float = DEF_TIME_STEP,
                 time_tick: float = DEF_TIME_TICK,
                 discrete_time: bool = DEF_DISCRETE_TIME,
                 seed: int = DEF_SEED):
        super().__init__(bnd_str=bnd_str,
                         cfg_str=cfg_str,
                         time_step=time_step,
                         time_tick=time_tick,
                         discrete_time=discrete_time,
                         seed=seed)

    @classmethod
    def init_arginfo(cls):
        return []

    @classmethod
    def init_kwarginfo(cls):
        return [
            ('time_step', 'Period of a simulation time step', float.__name__, True, DEF_TIME_STEP),
            ('time_tick', 'Simulation time tick', float.__name__, True, DEF_TIME_TICK),
            ('discrete_time', 'Flag to use discrete time', bool.__name__, True, DEF_DISCRETE_TIME),
            ('seed', 'Random number generator seed', int.__name__, True, DEF_SEED)
        ]

    def get_delta(self):
        return float(self.get_node_state('delta'))

    def set_delta(self, _val):
        self.set_node_state('delta', bool(_val))

    def get_notch(self):
        return float(self.get_node_state('notch'))

    def set_notch(self, _val):
        self.set_node_state('notch', bool(_val))

    def set_delta_neighbors(self, _d_avg: float):
        self.set_symbol_table_val('delta_nbs', _d_avg)
