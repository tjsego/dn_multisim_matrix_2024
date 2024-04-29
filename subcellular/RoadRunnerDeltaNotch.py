from simservices import DeltaNotchSimService, RoadRunnerSimService

model_str = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by XMLPrettyPrinter on 4/28/2011 from  -->
<sbml xmlns = "http://www.sbml.org/sbml/level2" level = "2" version = "1">
   <model id = "cell">
      <listOfCompartments>
         <compartment id = "compartment" size = "1"/>
      </listOfCompartments>
      <listOfSpecies>
         <species id = "Davg" boundaryCondition = "true" initialConcentration = "0.4" compartment = "compartment"/>
         <species id = "X" boundaryCondition = "true" initialConcentration = "0" compartment = "compartment"/>
         <species id = "D" boundaryCondition = "false" initialConcentration = "0.5" compartment = "compartment"/>
         <species id = "N" boundaryCondition = "false" initialConcentration = "0.5" compartment = "compartment"/>
      </listOfSpecies>
      <listOfParameters>
         <parameter id = "k" value = "2"/>
         <parameter id = "a" value = "0.01"/>
         <parameter id = "v" value = "1"/>
         <parameter id = "b" value = "100"/>
         <parameter id = "h" value = "2"/>
      </listOfParameters>
      <listOfReactions>
         <reaction id = "_J1" reversible = "false">
            <listOfReactants>
               <speciesReference species = "X" stoichiometry = "1"/>
            </listOfReactants>
            <listOfProducts>
               <speciesReference species = "N" stoichiometry = "1"/>
            </listOfProducts>
            <kineticLaw>
               <math xmlns = "http://www.w3.org/1998/Math/MathML">
                  <apply>
                     <minus/>
                     <apply>
                        <divide/>
                        <apply>
                           <power/>
                           <ci>
                                 Davg
                           </ci>
                           <ci>
                                 k
                           </ci>
                        </apply>
                        <apply>
                           <plus/>
                           <ci>
                                 a
                           </ci>
                           <apply>
                              <power/>
                              <ci>
                                    Davg
                              </ci>
                              <ci>
                                    k
                              </ci>
                           </apply>
                        </apply>
                     </apply>
                     <ci>
                           N
                     </ci>
                  </apply>
               </math>
            </kineticLaw>
         </reaction>
         <reaction id = "_J2" reversible = "false">
            <listOfReactants>
               <speciesReference species = "X" stoichiometry = "1"/>
            </listOfReactants>
            <listOfProducts>
               <speciesReference species = "D" stoichiometry = "1"/>
            </listOfProducts>
            <kineticLaw>
               <math xmlns = "http://www.w3.org/1998/Math/MathML">
                  <apply>
                     <times/>
                     <ci>
                           v
                     </ci>
                     <apply>
                        <minus/>
                        <apply>
                           <divide/>
                           <cn type = "integer">
                                 1
                           </cn>
                           <apply>
                              <plus/>
                              <cn type = "integer">
                                    1
                              </cn>
                              <apply>
                                 <times/>
                                 <ci>
                                       b
                                 </ci>
                                 <apply>
                                    <power/>
                                    <ci>
                                          N
                                    </ci>
                                    <ci>
                                          h
                                    </ci>
                                 </apply>
                              </apply>
                           </apply>
                        </apply>
                        <ci>
                              D
                        </ci>
                     </apply>
                  </apply>
               </math>
            </kineticLaw>
         </reaction>
      </listOfReactions>
   </model>
</sbml>
"""

DEF_STEP_SIZE = 1.0
DEF_NUM_STEPS = 2
DEF_STOCHASTIC = False
DEF_SEED = None


class RoadRunnerDeltaNotch(DeltaNotchSimService, RoadRunnerSimService):

    def __init__(self,
                 step_size=DEF_STEP_SIZE,
                 num_steps=DEF_NUM_STEPS,
                 stochastic=DEF_STOCHASTIC,
                 seed: int = DEF_SEED):
        super().__init__(model_str=model_str,
                         step_size=step_size,
                         num_steps=num_steps,
                         stochastic=stochastic,
                         seed=seed)

    @classmethod
    def init_arginfo(cls):
        return []

    @classmethod
    def init_kwarginfo(cls):
        return {
            ('step_size', 'Period of a simulation step', float.__name__, True, DEF_STEP_SIZE),
            ('num_steps', 'Number of substeps per simulation step', int.__name__, True, DEF_NUM_STEPS),
            ('stochastic', 'Flag to use Gillespie SSA', bool.__name__, True, DEF_STOCHASTIC),
            ('seed', 'Random number generator seed', int.__name__, True, DEF_SEED)
        }

    def get_delta(self):
        return self.get_rr_val('D')

    def set_delta(self, _val):
        self.set_rr_val('D', _val)

    def get_notch(self):
        return self.get_rr_val('N')

    def set_delta(self, _val):
        self.set_rr_val('N', _val)

    def set_delta_neighbors(self, _d_tot: float, _num_nbs: int):
        self.set_rr_val('Davg', _d_tot / _num_nbs if _num_nbs > 0 else 0.0)
