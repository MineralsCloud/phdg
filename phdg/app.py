from abstract import System, Substance

if __name__ == "__main__":

    # Al-O System

    s = System()
    s.substances = [
        Substance('HC', 'AlOOH'),
        Substance('Pbca', 'AlOOH'),
        Substance('Pyrite', 'AlOOH'),
        Substance('Ice X', 'H2O'),
        Substance('Ice VII', 'H2O'),
        Substance('Rh2O3', 'Al2O3'),
        Substance('Cor', 'Al2O3'),
        # Substance('PPv', 'Al2O3'),
    ]
    s.substance_manifests = [
        [(1, 'Al2O3'), (1, 'H2O')],
        [(2, 'AlOOH')]
    ]
    for c in s.find_combinations():
        print(c)