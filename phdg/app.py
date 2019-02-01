import os
import yaml
from pathlib import Path
import sys

from abstract import System
from plotters import PlotterManager


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.stderr.write('Usage: {} CONFIG.yml\n'.format(sys.argv[0]))
        exit()

    config_path = Path(sys.argv[1])

    os.chdir(config_path.parent)
        
    with open(config_path.name) as fp:
        config = yaml.load(fp)

    system = System(config)
    manager = PlotterManager(system)

    for plot_options in config['plots']:
        manager.plot(
            plot_options["type"],
            plot_options["output"],
            **plot_options["args"]
        )