from typing import List
from abstract import System
from plotters import Plotter, SubstanceFieldPlotter, CombinationFieldPlotter, GibbsDifferencePlotter, PhaseDiagramSlowPlotter

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