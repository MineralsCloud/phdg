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

    def __init__(self, substance_name: str, substance_type: str, fname: str = ""):
        self.substance_type = substance_type
        self.substance_name = substance_name
        # self.gibbs_free_energy = GibbsFreeEnergyGridTableReader().read_gibbs_free_energy(fname)
    
    def __repr__(self):
        return "<Substance {} ({})>".format(
            self.substance_type,
            self.substance_name
        )

class Combination:
    '''
    A helper class that combines several substances.

    '''
    substances: List[Tuple[float, Substance]]

    def __init__(self, substances):
        self.substances = substances

    def get_temperature_range(self):
        return (
            numpy.min([
                substance[1].gibbs_free_energy.temperature_array
                for substance in self.substances
            ]),
            numpy.max([
                substance[1].gibbs_free_energy.temperature_array
                for substance in self.substances
            ]) 
        )

    def get_pressure_range(self):
        return (
            numpy.min([
                substance[1].gibbs_free_energy.pressure_array
                for substance in self.substances
            ]),
            numpy.max([
                substance[1].gibbs_free_energy.pressure_array
                for substance in self.substances
            ]) 
        )
    
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

    def find_substances_by_type(self, substance_type: str):
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
            yield Combination(list(zip((s[0] for s in manifest), combination)))

    def find_combinations(self):
        '''
        Find combinations based on given combination manifest
        '''

        combinations = []

        for manifest in self.substance_manifests:
            combinations.extend(self.find_combinations_by_manifest(manifest))
        
        return combinations
