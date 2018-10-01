import os.path
import re
import numpy as np

class FortDG:
    def __init__(self,fname):
        assert os.path.isfile(fname)

        fort_dg_dict = {}

        regex = re.compile("(\w+) = ([\w.-]+)( +!.*)?")
        with open(fname,'r') as f:
            for line in f:
                result = regex.match(line)
                if result:
                    fort_dg_dict[result.group(1)] = result.group(2)

        pl = int(fort_dg_dict["pl"])
        ph = int(fort_dg_dict["ph"])
        px = int(fort_dg_dict["px"])

        assert pl == ph and pl == px

        self.p = pl

        self.rk_stage = int(fort_dg_dict["rk_stage"])
        self.rk_order = int(fort_dg_dict["rk_order"])

    def summarize(self):
        print "Polynomial order: {:d}".format(self.p)
        print "Using SSP-RK scheme of order {:d}".format(self.rk_order)
        print "  with {:d} stages per step".format(self.rk_stage)