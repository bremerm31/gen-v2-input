import os.path
import numpy as np

class Tide:
    def __init__(self):
        self.amig = 0.0
        self.ff = 0.0
        self.fface = 0.0
        self.emo = np.array([])
        self.efa = np.array([])

class Fort15:
    def __init__(self,fname, num_open_boundary_nodes):
        assert os.path.isfile(fname)

        with open(fname,'r') as f:
            self.rundes = f.readline().split()[0]
            self.runid = f.readline().split()[0]
            _ = f.readline() #ignore NFOVER
            _ = f.readline() #ignore NABOUT
            self.nscreen = int(f.readline().split()[0])
            self.ihot = int(f.readline().split()[0])
            self.ics = int(f.readline().split()[0])
            _ = f.readline() #ignore IM -- model type
            self.nolibf = int(f.readline().split()[0])
            self.nolifa = int(f.readline().split()[0])
            _ = f.readline() #ignore NOLICA always running with advection
            _ = f.readline() #  and NOLICAT

            self.nwp = int(f.readline().split()[0])
            assert self.nwp == 0 #other types not supported at the moment

            self.ncor = int(f.readline().split()[0])
            _ = f.readline() #ignore NTIP for now

            self.nws = int(f.readline().split()[0])

            self.nramp = int(f.readline().split()[0])
            self.g = np.float64(f.readline().split()[0])

            #ignore GWCE terms
            _ = f.readline()

            self.dt = np.float64(f.readline().split()[0])
            self.statim = np.float64(f.readline().split()[0])
            self.reftim = np.float64(f.readline().split()[0])
            self.rnday = np.float64(f.readline().split()[0])
            self.ramp_duration = np.float64(f.readline().split()[0])

            _ = f.readline() #more gwce terms

            self.h0 = np.float64(f.readline().split()[0])

            self.slam0, self.sfea0,_ = f.readline().split(None,2)
            self.slam0 = np.float64(self.slam0)
            self.sfea0 = np.float64(self.sfea0)

            self.ffactor, self.hbreak, self.ftheta, self.fgamma, _ = f.readline().split(None,4)
            self.ffactor = np.float64(self.ffactor)
            self.hbreak = np.float64(self.hbreak)
            self.ftheta = np.float64(self.ftheta)
            self.fgamma = np.float64(self.fgamma)

            self.esl = np.float64(f.readline().split()[0])
            self.cori = np.float64(f.readline().split()[0])
            self.ntif = int(f.readline().split()[0])
            assert self.ntif == 0

            self.nbfr = int(f.readline().split()[0])
            self.tides = {}
            for i in range(self.nbfr):
                tag = f.readline().split()[0]
                self.tides[tag] = Tide()
                line = f.readline().split()

                self.tides[tag].amig  = np.float64(line[0])
                self.tides[tag].ff    = np.float64(line[1])
                self.tides[tag].fface = np.float64(line[2])

            for i in range(self.nbfr):
                tag = f.readline().split()[0]
                self.tides[tag].emo = np.empty(num_open_boundary_nodes)
                self.tides[tag].efa = np.empty(num_open_boundary_nodes)
                for j in range(num_open_boundary_nodes):
                    line = f.readline().split()
                    self.tides[tag].emo[i] = np.float64(line[0])
                    self.tides[tag].efa[i] = np.float64(line[1])

    def summarize(self):
        print "Run description: {}".format(self.rundes)
        print "Run description 2: {}".format(self.runid)
        print "Frequency written to stdout: {}".format(self.nscreen)
        if self.ihot == 0:
            print "Run in cold started"
        else:
            print "Run is hot started"
        if self.ics == 1:
            print "Using Cartesian coordinates"
        else:
            print "Using Spherical coordinates"

        print "Gravity is set to {:.2f}".format(self.g)

        print "The simulation starts at {:.4f}".format(self.statim)
        print "  and runs for {:.4f} days".format(self.rnday)
        print "  with a timestep of {:.4f} seconds".format(self.dt)
        if self.nramp == 0:
            print "  with no ramping of source terms"
        else:
            print "  and a ramp duration of {:.4f} days".format(self.nramp)

        #Print out all friction information

        #print out coriolis information

        #print out wind forcing information
