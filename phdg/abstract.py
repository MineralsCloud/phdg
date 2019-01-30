from gibbs import GibbsFreeEnergyGrid
from typing import List
import itertools

class Substance:
    substance_type: str
    gibbs_free_energy: GibbsFreeEnergyGrid

    def __init__(self, substance_type: str):
        self.substance_type = substance_type
    
    def __repr__(self):
        return "<Substance {}>".format(
            self.substance_type
        )

class System:
    '''
    An Al-O system includes AlOOH or Al2O3 + H2O

    A manifest of possible combination of substances:

        [
            [ (2, AlOOH) ],
            [ (1, Al2O3), (1, H2O) ]
        ]

    '''
    substances: List[Substance]
    substance_manifest: List[tuple]

    def find_substance(self, substance_type: str):
        '''
        Find substance based on given criterion, criteria could be the combination of the following:

        1. substance type
        2. substance temperature / pressure range

        '''
        return [
            substance for substance in self.substances 
            if substance.substance_type == substance_type
        ]
    
    def find_combinations(self):
        '''
        Find combinations based on given combination manifest
        '''

        combinations = []

        for manifest_item in self.substance_manifest:
            combinations.extend(itertools.product(*(
                self.find_substance(substance_spec[1])
                for substance_spec in manifest_item
            )))
        
        return combinations

if __name__ == '__main__':
    s = System()
    s.substances = [
        Substance('H2'),
        Substance('H2'),
        Substance('O2'),
        Substance('O2'),
        Substance('H2O'),
        Substance('H2O'),
    ]
    s.substance_manifest = [
        [(1, 'H2'), (1, 'O2')],
        [(2, 'H2O')]
    ]
    print(s.find_combinations())