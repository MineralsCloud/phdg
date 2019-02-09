from typing import List

import numpy

import matplotlib
import matplotlib.pyplot as plt

from abstract import Substance, Combination, System

from plotters import Plotter

class PhaseDiagramPlotter(Plotter):
    '''
    This module plots a phase diagram over a given range. It plot the entire diagram piece by piece.
    '''

    type_keywords: List[str] = [ "phase_diagram" ]
    default_options: dict = {
        "p_range": [-5, 300],
        "p_step": 5,
        "t_range": [0, 3000],
        "t_step": 30,
        "custom_colors": [],
        "boundary_line": False,
        "highlight_overlay": True,
        "highlight_alpha": 0.5
    }

    def __init__(self) -> None:
        super().__init__()
    
    def fill_patch(self, combinations: Combination, p_range: tuple, t_range: tuple, options: dict) -> numpy.ndarray:
        '''
        For each patch, all the combinations should exist. Then we could use the unsafe version of the Gibbs free energy getter.
        But we need to match back the combination key when we are back.
        '''

        if len(combinations) == 0: return -1

        P = numpy.arange(*p_range, options['p_step'])
        T = numpy.arange(*t_range, options['t_step'])

        P_grid, T_grid = numpy.meshgrid(P, T)

        G_grid = numpy.empty((P_grid.shape[0], P_grid.shape[1], len(combinations)))

        for k, combination in enumerate(combinations):

            G_grid[:, :, k] = combination.get_gibbs_free_energy_unsafe(P_grid, T_grid)

        C_grid = numpy.argmin(G_grid, axis=2)

        return C_grid

    def plot(self, system: System, output: str, **kwargs):

        options = self._load_kwargs(kwargs)

        plt.figure()

        combinations = system.find_combinations()

        p_min, p_max = numpy.ceil(numpy.array(options['p_range']) / options['p_step']) * options['p_step']
        t_min, t_max = numpy.ceil(numpy.array(options['t_range']) / options['t_step']) * options['t_step']

        # Get patch boundaries

        p_bounds = set([p_min, p_max, p_max + options['p_step']])
        t_bounds = set([t_min, p_max, t_max + options['t_step']])

        for combination in combinations:

            combination_p_min, combination_p_max = numpy.ceil(numpy.array(combination.get_pressure_range()) / options['p_step']) * options['p_step']
            combination_t_min, combination_t_max = numpy.ceil(numpy.array(combination.get_temperature_range()) / options['t_step']) * options['t_step']

            if p_min < combination_p_min and combination_p_min < p_max: p_bounds.add(combination_p_min)
            if p_min < combination_p_max and combination_p_max < p_max: p_bounds.add(combination_p_max)
            if t_min < combination_t_min and combination_t_min < t_max: t_bounds.add(combination_t_min)
            if t_min < combination_t_max and combination_t_max < t_max: t_bounds.add(combination_t_max)
        
        # Get patches

        p_bounds = sorted(list(p_bounds))
        t_bounds = sorted(list(t_bounds))

        P = numpy.arange(p_min, p_max + options['p_step'], options['p_step'])
        T = numpy.arange(t_min, t_max + options['t_step'], options['t_step'])

        P_grid, T_grid = numpy.meshgrid(P, T)
        C_grid = numpy.zeros(P_grid.shape, dtype=int)

        for patch_p_min, patch_p_max in zip(p_bounds[:-1], p_bounds[1:]):
            for patch_t_min, patch_t_max in zip(t_bounds[:-1], t_bounds[1:]):

                # Find combinations for this area (<= or <)

                patch_combinations = [
                    combination for combination in combinations
                    if  combination.get_pressure_range()[0]    <= patch_p_min and patch_p_min < combination.get_pressure_range()[1]
                    and combination.get_temperature_range()[0] <= patch_t_min and patch_t_min < combination.get_temperature_range()[1]
                ]

                # Fill patch

                C_patch = self.fill_patch(patch_combinations, (patch_p_min, patch_p_max), (patch_t_min, patch_t_max), options)

                C_patch_converted = numpy.copy(C_patch)

                # Convert keys

                for combination in patch_combinations:
                    C_patch_converted[C_patch == patch_combinations.index(combination)] = combinations.index(combination)

                C_grid[
                    int((patch_t_min - t_min) / options['t_step']):int((patch_t_max - t_min) / options['t_step']),
                    int((patch_p_min - p_min) / options['p_step']):int((patch_p_max - p_min) / options['p_step'])
                ] = C_patch_converted

        contour_levels = numpy.arange(-1.5, .5 + len(combinations), 1)
        contour_level_colors = [(1, 1, 1)] + [
            (numpy.random.random(), numpy.random.random(), numpy.random.random())
            for _ in range(len(combinations))
        ]

        plt.imshow(
            C_grid,
            cmap=matplotlib.colors.ListedColormap(contour_level_colors),
            norm=matplotlib.colors.BoundaryNorm(contour_levels, len(combinations) + 1),
            extent=[
                p_min - .5 * options['p_step'],
                p_max + .5 * options['p_step'],
                t_min - .5 * options['t_step'],
                t_max + .5 * options['t_step']
            ], aspect='auto', zorder=1, origin='lower')

        # Overlay

        if options['highlight_overlay']:
            c = numpy.ones((255, 1, 4))
            c[:, 0, 3] = numpy.linspace(0, options['highlight_alpha'], 255)
            plt.imshow(c, extent=[p_min, p_max, t_min, t_max], aspect='auto', zorder=1, origin='lower')

        if options['boundary_line']:
            for p in p_bounds: plt.axvline(p, c='w', lw=.3, alpha=.3)
            for t in t_bounds: plt.axhline(t, c='w', lw=.3, alpha=.3)
        
        plt.legend([
            matplotlib.patches.Patch(facecolor=c, ec=c, alpha=.7)
            for c in contour_level_colors[:]
            if contour_level_colors.index(c) - 1 in set(C_grid.flatten().tolist()) and contour_level_colors.index(c) != 0
        ], [
            ' + '.join(s[1].substance_name for s in combination.substances)
            for combination in combinations
            if combinations.index(combination) in set(C_grid.flatten().tolist())
        ])

        plt.xlabel("$P$ / GPa")
        plt.ylabel("$T$ / K")

        plt.savefig(output, dpi=300)
