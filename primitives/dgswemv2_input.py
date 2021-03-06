from fort_14 import Fort14
from fort_15 import Fort15
from fort_dg import FortDG

import datetime

import yaml

class DGSWEMv2Input:
    def __init__(self,fort14,fort15,fortdg):
        self.mesh_node = {'format' : 'Adcirc',
                          'file_name' : fort14.filename}
        if fort15.ics == 1:
            self.mesh_node['coordinate_system'] = 'cartesian'
        else:
            self.mesh_node['coordinate_system'] = 'spherical'

        self.start_time = datetime.datetime(2015,05,11,12,00,00)
        self.timestepping_node = {}
        self.timestepping_node["start_time"] = self.start_time.strftime("%d-%m-%Y %H:%M")
        self.end_time = self.start_time + datetime.timedelta(fort15.rnday)
        self.timestepping_node["end_time"] = self.end_time.strftime("%d-%m-%Y %H:%M")
        self.timestepping_node["dt"] = float(fort15.dt)
        if fort15.nramp > 0:
            self.timestepping_node["ramp_duration"] = float(fort15.ramp_duration)

        self.timestepping_node["nstages"] = fortdg.rk_stage
        self.timestepping_node["order"]   = fortdg.rk_order

        self.polynomial_order = fortdg.p

        self.problem_node = {'name' : 'swe'}
        self.problem_node["g"] = float(fort15.g)

        if fort15.nolifa == 2:
            self.problem_node["wetting_drying"] = { "h_o" : float(fort15.h_o) }

    def dump(self,f):
        f.write(60*"#"+'\n')
        f.write("#\n")
        f.write("#  dgswem-v2 input\n")
        f.write("#\n")
        f.write("#  generated by gen-v2-input\n")
        f.write("#\n")
        f.write(60*"#"+2*"\n")

        yaml.dump({'mesh':self.mesh_node},f,default_flow_style=False)
        f.write("\n")

        yaml.dump({'timestepping':self.timestepping_node},f,default_flow_style=False)
        f.write("\n")

        yaml.dump({'polynomial_order': self.polynomial_order})
        f.write("\n")

        yaml.dump({'problem':self.problem_node},f,default_flow_style=False)