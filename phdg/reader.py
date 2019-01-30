from gibbs import GibbsFreeEnergyGrid

class GibbsFreeEnergyGridTableReader:
    @staticmethod
    def load_table_from_file(fname: str):
        with open(fname) as fp:
            row_index = numpy.array(fp.readline().split()[1:], dtype='float64')
            main_area = numpy.loadtxt(fp, dtype='float64')
            col_index = main_area[:, 0]
            data = main_area[:, 1:]
        return row_index, col_index, data
    
    @staticmethod
    def read_gibbs_free_energy(fname: str):
        return GibbsFreeEnergyGrid(*self.load_table_from_file(fname))