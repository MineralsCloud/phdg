import numpy

class GibbsFreeEnergyGrid:

    num_formula_units: float

    def __init__(self, pressure_array, temperature_array, gibbs_free_energies):
        self._pressure_array = pressure_array
        self._temperature_array = temperature_array
        self._gibbs_free_energies = gibbs_free_energies

    @staticmethod
    def load_table_from_file(fname: str):
        with open(fname) as fp:
            row_index = numpy.array(fp.readline().split()[1:], dtype='float64')
            main_area = numpy.loadtxt(fp, dtype='float64')
            col_index = main_area[:, 0]
            data = main_area[:, 1:]
        return row_index, col_index, data

    @property
    def pressure_array(self) -> numpy.ndarray:
        return self._pressure_array
    @property
    def temperature_array(self) -> numpy.ndarray:
        return self._temperature_array
    @property
    def gibbs_free_energies(self):
        return self._gibbs_free_energies

    #@units.wraps(units.Ryd, (None, units.GPa, units.K))
    def g_pt(self, p, t):
        print((numpy.min(self.pressure_array), numpy.max(self.pressure_array)), '->', (numpy.min(p), numpy.max(p)))
        print((numpy.min(self.temperature_array), numpy.max(self.temperature_array)), '->', (numpy.min(t), numpy.max(t)))
        def _g_pt(p, t): 
            try:
                return self.gibbs_free_energies[
                    numpy.argmin(numpy.abs(numpy.array(self.temperature_array) - t)),
                    #self.temperature_array.tolist().index(t),
                    numpy.argmin(numpy.abs(numpy.array(self.pressure_array) - p))
                    #self.pressure_array.tolist().index(p)
                ]
            except IndexError as e:
                print(len(self.pressure_array.tolist()))
                print(len(self.temperature_array.tolist()))
                raise RuntimeError('(P = %f, T = %f) not found in raw data: %s' % (p, t))
        return numpy.vectorize(_g_pt)(p, t)