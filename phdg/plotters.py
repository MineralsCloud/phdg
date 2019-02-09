from typing import List, Dict
import copy

import numpy
import matplotlib
from matplotlib import pyplot as plt

from abstract import System, Substance

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

def draw_rectangle(x, y, options: dict, text=""):
    x_min, x_max = x
    y_min, y_max = y
    #c = next(plt.gca().get_prop_cycle())
    #print(dir(c))

    c = numpy.random.random(3).tolist()
    fc = tuple(c + [.1])
    ec = tuple(c + [.7])
    #line, = plt.plot((x_min, x_max, x_max, x_min, x_min), (y_min, y_min, y_max, y_max, y_min))
    rect = matplotlib.patches.Rectangle((x_min, y_min), -numpy.subtract(*x), -numpy.subtract(*y), facecolor=fc, edgecolor=ec)
    plt.gca().add_patch(rect)
    plt.text(x_max, y_max, text, ha='right', va='top', color=ec, fontsize="small")
    plt.text(x_min, y_min, text, ha='left', va='bottom', color=ec, fontsize="small")
    return text, rect

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

            draw_rectangle(p_range, t_range, options, '{} ({})'.format(
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

            draw_rectangle(p_range, t_range, options)

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
        "t_step": 300,
        "base": 0
    }

    def __init__(self) -> None:
        super().__init__()


    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

        plt.figure(figsize=(9, 6))

        p_range = options['p_range']
        
        combinations = [
            combination for combination in system.find_combinations()
            if (not combination.get_pressure_range()[1] < p_range[0]) and (not combination.get_pressure_range()[0] > p_range[1])
        ]
        
        if isinstance(options['base'], int):
            base_idx = options['base']
        else:
            raise NotImplementedError()

        line_style_keys = list(matplotlib.lines.lineStyles.keys())[:4] * 3

        linestyle_iter = iter(line_style_keys)

        t_array = numpy.arange(options['t_range'][0], options['t_range'][1], options['t_step'])

        from palettable.cartocolors.qualitative import Prism_10
        from cycler import cycler

        for combination in combinations:

            print(' - {} with P in {} and T in {}'.format(combination, combination.get_pressure_range(), combination.get_temperature_range()))

            line_style = next(linestyle_iter)

            t_min, t_max = combination.get_temperature_range()
            p_min, p_max = combination.get_pressure_range()

            p_array = numpy.arange(max(p_min, p_range[0]), min(p_max, p_range[1]), 1)
            if len(p_array.tolist()) == 0: continue



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
        ], bbox_to_anchor=(1.04, .5), loc="center left")
        plt.xlabel('$P$ / GPa')
        plt.ylabel(r'$\Delta G$ / Ryd')
        plt.tight_layout(rect=[0, 0, 0.8, 1])
        plt.savefig(output, dpi=300)

