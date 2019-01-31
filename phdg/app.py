from abstract import System, Substance

import matplotlib
from matplotlib import pyplot as plt
import numpy

import yaml

if __name__ == "__main__":


    import os
    
    os.chdir('example/AlOOH')
    
    with open('input.yml') as fp:
        config = yaml.load(fp)
    
    system = System(config)

    def draw_rectangle(x, y, text=""):
        x_min, x_max = x
        y_min, y_max = y
        line, = plt.plot((x_min, x_max, x_max, x_min, x_min), (y_min, y_min, y_max, y_max, y_min))
        plt.text(x_max, y_max, text, ha='right', va='top', color=line.get_color())

    # FIG 01

    plt.figure()

    print('We are working on the following phases:')

    for substance in system.substances:

        print(' - {} with P in {} and T in {}'.format(substance, substance.get_pressure_range(), substance.get_temperature_range()))

        p_range = substance.get_pressure_range()
        t_range = substance.get_temperature_range()

        draw_rectangle(p_range, t_range, '{} ({})'.format(
            substance.substance_type,
            substance.substance_name)
        )

    plt.xlim(-5, 500)
    plt.ylim(0, 3000)
    plt.xlabel('$P$ / GPa')
    plt.ylabel('$T$ / K')
    plt.savefig('01-field-of-input.png', dpi=300)

    # FIG 02

    plt.figure()

    print('Possible combinations of phases are:')

    for combination in system.find_combinations():

        print(' - {} with P in {} and T in {}'.format(combination, combination.get_pressure_range(), combination.get_temperature_range()))

        p_range = combination.get_pressure_range()
        t_range = combination.get_temperature_range()

        draw_rectangle(p_range, t_range)


    plt.xlim(-5, 500)
    plt.ylim(0, 3000)
    plt.xlabel('$P$ / GPa')
    plt.ylabel('$T$ / K')
    plt.savefig('02-field-of-combinations.png', dpi=300)

    # FIG 03

    plt.figure()

    from palettable.tableau import Tableau_10

    def classifier(P, T):

        combinations = system.find_combinations()
        combinations_gibbs_free_energies = [
            (idx, combination, combination.get_gibbs_free_energy(P, T)) for (idx, combination) in enumerate(combinations)
            if combination.get_gibbs_free_energy(P, T) is not numpy.inf
        ]

        if len(combinations_gibbs_free_energies) == 0: return -1

        idx = numpy.argmin([
            g for (_, _, g) in combinations_gibbs_free_energies
        ])

        combination_idx = combinations_gibbs_free_energies[idx][0]

        return combination_idx
    
    def mapper(v):
        if v != -1:
            return Tableau_10.mpl_colors[v]
        else:
            return (1, 1, 1)

    P = numpy.arange(0, 300, 5)
    T = numpy.arange(0, 2100, 30)

    P_grid, T_grid = numpy.meshgrid(P, T)

    C_grid = numpy.vectorize(classifier)(P_grid.flatten(), T_grid.flatten()).reshape(P_grid.shape)

    RGB_grid = numpy.zeros((T.shape[0], P.shape[0], 3))
    
    for i in range(P.shape[0]):
        for j in range(T.shape[0]):
            RGB_grid[j, i, :] = mapper(C_grid[j, i])

    plt.imshow(RGB_grid, extent=[0, 300, 0, 2100], aspect='auto')
    plt.savefig('03-full-phase-diagram.png', dpi=300)

    # FIG 04
    