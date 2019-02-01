import os
import yaml
from abstract import System
from plotters import PlotterManager


if __name__ == '__main__':
        
    os.chdir('example/Al2O3')
    
    with open('input.yml') as fp:
        config = yaml.load(fp)

    system = System(config)
    manager = PlotterManager(system)

    for plot_options in config['plots']:
        manager.plot(
            plot_options["type"],
            plot_options["output"],
            **plot_options["args"]
        )