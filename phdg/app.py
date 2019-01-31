from abstract import System, Substance

import matplotlib
from matplotlib import pyplot as plt
import numpy

import yaml


def draw_rectangle(x, y, text=""):
    x_min, x_max = x
    y_min, y_max = y
    line, = plt.plot((x_min, x_max, x_max, x_min, x_min), (y_min, y_min, y_max, y_max, y_min))
    plt.text(x_max, y_max, text, ha='right', va='top', color=line.get_color())


def plot_fig_01(system):

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

def plot_fig_02(system):

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


def plot_fig_03(system):

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

def plot_fig_04(system, p_range):

    plt.figure()
    
    combinations = [
        combination for combination in system.find_combinations()
        if (not combination.get_pressure_range()[1] < p_range[0]) and (not combination.get_pressure_range()[0] > p_range[1])
    ]
    
    base_idx = 0

    line_style_keys = list(matplotlib.lines.lineStyles.keys())[:4] * 3

    linestyle_iter = iter(line_style_keys)

    t_array = numpy.arange(0, 2000, 300)

    for combination in combinations:

        print(' - {} with P in {} and T in {}'.format(combination, combination.get_pressure_range(), combination.get_temperature_range()))

        line_style = next(linestyle_iter)

        t_min, t_max = combination.get_temperature_range()
        p_min, p_max = combination.get_pressure_range()

        p_array = numpy.arange(max(p_min, p_range[0]), min(p_max, p_range[1]), 1)
        if len(p_array.tolist()) == 0: continue

        from palettable.cartocolors.qualitative import Prism_10
        from cycler import cycler

        ax = plt.gca()
        ax.set_prop_cycle(cycler('color', Prism_10.mpl_colors))


        for t in t_array:
            if t > t_max or t < t_min: continue
            name = ' + '.join(s[1].substance_name for s in combination.substances)
            plt.plot(
                p_array,
                combination.get_gibbs_free_energy_unsafe(p_array, t) - combinations[base_idx].get_gibbs_free_energy_unsafe(p_array, t),
                label="{} at {} K".format(name, t),
                linestyle=line_style
            )
        
    plt.gca().legend([
        matplotlib.lines.Line2D([0], [0], color=c)
        for (t, c) in zip(t_array, Prism_10.mpl_colors[:len(t_array)])
    ] + [
        matplotlib.lines.Line2D([0], [0], linestyle=s, c='k')
        for (c, s) in zip(combinations, line_style_keys[:len(combinations)])
    ], [ "$T$ = {} K".format(t) for t in t_array ] + [ 
      ' + '.join(s[1].substance_name for s in combination.substances)
      for combination in combinations
    ])
    plt.xlabel('$P$ / GPa')
    plt.ylabel(r'$\Delta G$ / Ryd')
    plt.savefig('04-partial-g-p-{}-{}.png'.format(p_range[0], p_range[1]), dpi=300)



if __name__ == "__main__":

    import os
    
    os.chdir('example/AlOOH')
    
    with open('input.yml') as fp:
        config = yaml.load(fp)
    
    system = System(config)

    plot_fig_01(system)
    plot_fig_02(system)
    # plot_fig_03(system)
    plot_fig_04(system, (30, 100))
    plot_fig_04(system, (120, 300))
    plot_fig_04(system, (30, 300))