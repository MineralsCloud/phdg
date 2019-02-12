from gibbs import GibbsFreeEnergyGrid
from reader import GibbsFreeEnergyGridTableReader
from typing import List, Tuple
import itertools
import numpy

class Substance:
    '''
    The class represent a certain structure. It holds the name and type and Gibbs free energy for the phase.
    '''
    substance_type: str
    substance_name: str
    gibbs_free_energy: GibbsFreeEnergyGrid
    gibbs_free_energy_num_formula_units: float

    def __init__(self, substance_name: str, substance_type: str, fname: str, num_formula_units: float):
        self.substance_type = substance_type
        self.substance_name = substance_name
        self.gibbs_free_energy = GibbsFreeEnergyGridTableReader().read_gibbs_free_energy(fname)
        self.gibbs_free_energy_num_formula_units = num_formula_units
    
    def __repr__(self):
        return "<Substance {} ({})>".format(
            self.substance_type,
            self.substance_name
        )

    def get_temperature_range(self) -> Tuple[float]:
        return (
            numpy.min(self.gibbs_free_energy.temperature_array),
            numpy.max(self.gibbs_free_energy.temperature_array)
        )

    def get_pressure_range(self) -> Tuple[float]:
        return (
            numpy.min(self.gibbs_free_energy.pressure_array),
            numpy.max(self.gibbs_free_energy.pressure_array)
        )
    
    def get_gibbs_free_energy(self, P, T):
        return self.gibbs_free_energy.g_pt(P, T) / self.gibbs_free_energy_num_formula_units

class Combination:
    '''
    A helper class that combines several substances.

    '''
    substances: List[Tuple[float, Substance]]

    def __init__(self, substances):
        self.substances = substances

    def get_temperature_range(self) -> Tuple[float]:
        return (
            numpy.max([
                substance[1].get_temperature_range()[0]
                for substance in self.substances
            ]),
            numpy.min([
                substance[1].get_temperature_range()[1]
                for substance in self.substances
            ]) 
        )

    def get_pressure_range(self) -> Tuple[float]:
        return (
            numpy.max([
                substance[1].get_pressure_range()[0]
                for substance in self.substances
            ]),
            numpy.min([
                substance[1].get_pressure_range()[1]
                for substance in self.substances
            ]) 
        )

    def is_valid_range(self):
        if numpy.subtract(*self.get_pressure_range()) > 0: return False
        elif numpy.subtract(*self.get_temperature_range()) > 0: return False
        else: return True
            
    def get_gibbs_free_energy(self, P, T):

        p_min, p_max = self.get_pressure_range()
        t_min, t_max = self.get_temperature_range()

        if P > p_min and P < p_max and T > t_min and T < t_max:
            return numpy.sum([
                substance[0] * substance[1].get_gibbs_free_energy(P, T) for substance in self.substances
            ])
        else:
            return numpy.inf

    def get_gibbs_free_energy_unsafe(self, P, T):
        return numpy.sum([
            substance[0] * substance[1].get_gibbs_free_energy(P, T) for substance in self.substances
        ], axis=0)

    def __repr__(self):
        return "Combination [{}]".format(
            ", ".join(str(substance) for substance in self.substances)
        )

class System:
    '''
    An Al-O system includes AlOOH or Al2O3 + H2O.

    A manifest of possible combination of substances:

        [
            [ (2, AlOOH) ],
            [ (1, Al2O3), (1, H2O) ]
        ]

    '''
    substances: List[Substance]
    substance_manifests: List[tuple]

    def __init__(self, config):

        self.substances = []
        
        for substance in config['system']['substances']:
            self.substances.append(
                Substance(substance['name'], substance['type'], substance['gibbs_dir'], substance['num_formula_units'])
            )

        self.substance_manifests = config['system']['manifests']

    def find_substances_by_type(self, substance_type: str) -> list:
        '''
        Find substance based on given criterion, criteria could be the combination of the following:

        1. substance type
        2. substance temperature / pressure range

        '''
        return [
            substance for substance in self.substances 
            if substance.substance_type == substance_type
        ]
    
    def find_combinations_by_manifest(self, manifest: List[Tuple[float, str]]):
        for combination in itertools.product(*(
            self.find_substances_by_type(substance_spec[1])
            for substance_spec in manifest
        )):
            combination = Combination(list(zip((s[0] for s in manifest), combination)))
            if combination.is_valid_range():
                yield combination

    def find_combinations(self) -> List[Combination]:
        '''
        Find combinations based on given combination manifest
        '''

        combinations = []

        for manifest in self.substance_manifests:
            combinations.extend(self.find_combinations_by_manifest(manifest))
        
        return combinations
