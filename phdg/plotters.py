from typing import List, Dict, Set

import matplotlib
from matplotlib import pyplot as plt
import numpy
from abstract import System, Substance
import copy

class Plotter:

    type_keywords: List[str]
    default_options: dict

    def __init__(self) -> None:
        pass
    
    def _load_kwargs(self, kwargs: dict) -> dict:
        options: dict = copy.copy(self.default_options)
        for key in options.keys():
            if key in kwargs.keys():
                options[key] = kwargs[key]
        return options

    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

def draw_rectangle(x, y, text=""):
    x_min, x_max = x
    y_min, y_max = y
    line, = plt.plot((x_min, x_max, x_max, x_min, x_min), (y_min, y_min, y_max, y_max, y_min))
    plt.text(x_max, y_max, text, ha='right', va='top', color=line.get_color())

class SubstanceFieldPlotter(Plotter):

    type_keywords: List[str] = [ "substances" ]
    default_options: dict = {
        "p_range": [-5, 500],
        "t_range": [0, 3000]
    }

    def __init__(self) -> None:
        super().__init__()


    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

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

        plt.xlim(*options['p_range'])
        plt.ylim(*options['t_range'])
        plt.xlabel('$P$ / GPa')
        plt.ylabel('$T$ / K')
        plt.savefig(output, dpi=300)

class CombinationFieldPlotter(Plotter):

    type_keywords: List[str] = [ "combinations" ]
    default_options: dict = {
        "p_range": [-5, 500],
        "t_range": [0, 3000]
    }

    def __init__(self) -> None:
        super().__init__()


    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

        plt.figure()

        print('Possible combinations of phases are:')

        for combination in system.find_combinations():

            print(' - {} with P in {} and T in {}'.format(combination, combination.get_pressure_range(), combination.get_temperature_range()))

            p_range = combination.get_pressure_range()
            t_range = combination.get_temperature_range()

            draw_rectangle(p_range, t_range)

        plt.xlim(*options['p_range'])
        plt.ylim(*options['t_range'])
        plt.xlabel('$P$ / GPa')
        plt.ylabel('$T$ / K')
        plt.savefig(output, dpi=300)

class GibbsDifferencePlotter(Plotter):

    type_keywords: List[str] = [ "gibbs_free_energy_difference" ]
    default_options: dict = {
        "p_range": [-5, 500],
        "t_range": [0, 3000],
        "t_step": 300
    }

    def __init__(self) -> None:
        super().__init__()


    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

        plt.figure()

        p_range = options['p_range']
        
        combinations = [
            combination for combination in system.find_combinations()
            if (not combination.get_pressure_range()[1] < p_range[0]) and (not combination.get_pressure_range()[0] > p_range[1])
        ]
        
        base_idx = 2

        line_style_keys = list(matplotlib.lines.lineStyles.keys())[:4] * 3

        linestyle_iter = iter(line_style_keys)

        t_array = numpy.arange(options['t_range'][0], options['t_range'][1], options['t_step'])

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
        plt.savefig(output, dpi=300)



class PhaseDiagramSlowPlotter(Plotter):

    type_keywords: List[str] = [ "phase_diagram_slow" ]
    default_options: dict = {
        "p_range": [-5, 300],
        "p_step": 5,
        "t_range": [0, 3000],
        "t_step": 30,
    }

    def __init__(self) -> None:
        super().__init__()

    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

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

        P = numpy.arange(*options["p_range"], options["p_step"])
        T = numpy.arange(*options["t_range"], options["t_step"])

        P_grid, T_grid = numpy.meshgrid(P, T)

        C_grid = numpy.vectorize(classifier)(P_grid.flatten(), T_grid.flatten()).reshape(P_grid.shape)

        RGB_grid = numpy.zeros((T.shape[0], P.shape[0], 3))
        
        for i in range(P.shape[0]):
            for j in range(T.shape[0]):
                RGB_grid[j, i, :] = mapper(C_grid[j, i])

        plt.imshow(RGB_grid, extent=options['p_range'] + options['t_range'], aspect='auto', origin='lower')
        plt.savefig(output, dpi=300)

class PlotterManager:

    '''
    The manager for all the plotters
    '''

    plotters: List[Plotter]
    system: System

    def __init__(self, system: System):
        self.plotters = [
            SubstanceFieldPlotter(),
            CombinationFieldPlotter(),
            GibbsDifferencePlotter(),
            PhaseDiagramSlowPlotter()
        ]
        self.system = system
    def register_plotter(self, plotter: Plotter):
        for keyword in plotter.type_keywords:
            if keyword in set(keyword for plotter in self.plotters for keyword in plotter.keywords):
                raise RuntimeError("Keyword {} is conflicting!".format(keyword))
        self.plotters.append(plotter)
    def unregister_plotter(self, plotter_type_keyword: str):
        self.plotters.remove(self.find_plotter(plotter_type_keyword))
    def find_plotter(self, plotter_type_keyword: str):
        try:
            return next(plotter for plotter in self.plotters if plotter_type_keyword in plotter.type_keywords)
        except StopIteration:
            raise RuntimeError("Keyword {} not found!".format(plotter_type_keyword))
    def plot(self, plotter_type_keyword: str, output, **kwargs):
        self.find_plotter(plotter_type_keyword).plot(self.system, output, **kwargs)