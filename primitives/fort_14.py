import os.path
import numpy as np

class BoundaryTypes:
    land = 0
    tide = 1
    flow = 2
    weir = 24
    island = 1

class Fort14:
    def __init__(self,fname):
        assert os.path.isfile(fname)

        self.filename = os.path.abspath(fname)

        with open(fname,'r') as f:
            self.agrid = f.readline().strip()
            self.number_elements,self.number_nodes = [int(n) for n in f.readline().split()]
            #Don't read in node or element information
            for _ in range(self.number_nodes):
                f.readline()
            for _ in range(self.number_elements):
                f.readline()

            #Read in open boundaries
            number_of_open_boundaries = int(f.readline().split()[0])
            total_number_of_open_boundary_nodes = int(f.readline().split()[0])

            self.open_boundaries = []
            for _ in range(number_of_open_boundaries):
                num_nodes = int(f.readline().split()[0])
                self.open_boundaries.append(np.empty(num_nodes,dtype=int))

                for i in range(num_nodes):
                    self.open_boundaries[-1][i] = int(f.readline().strip())

            assert len(self.open_boundaries) == number_of_open_boundaries
            assert sum(len(arr) for arr in self.open_boundaries) == total_number_of_open_boundary_nodes

            #Read in land boundaries
            self.land_boundaries = []
            number_of_land_boundaries = int(f.readline().split()[0])
            total_number_of_land_boundary_nodes = int(f.readline().split()[0])

            for _ in range(number_of_land_boundaries):
                line = f.readline().split()
                num_nodes = int(line[0])
                b_type = int(line[1])

                if b_type == BoundaryTypes.land:
                    nodes = np.empty(num_nodes)
                    for i in range(num_nodes):
                        nodes[i] = int(f.readline().split()[0])

                    self.land_boundaries.append({ "type": BoundaryTypes.land,
                                                  "nodes": nodes})
                elif b_type == BoundaryTypes.island:
                    nodes = np.empty(num_nodes)
                    for i in range(num_nodes):
                        nodes[i] = int(f.readline().split()[0])

                    self.land_boundaries.append({"type" : BoundaryTypes.island,
                                                 "nodes": nodes})

                elif b_type == BoundaryTypes.weir:
                    nodes = np.empty((num_nodes,2),dtype=int) #front nodes
                    heights = np.empty(num_nodes)
                    #Coefficient of free surface sub(super)-critical flow
                    cfsbp = np.empty((num_nodes,2))

                    for i in range(num_nodes):
                        line = f.readline().split(None,5)
                        nodes[i,:] = [int(line[0]), int(line[1])]
                        heights[i] = np.float64(line[2])
                        cfsbp[i,0] = np.float64(line[3])
                        cfsbp[i,1] = np.float64(line[4])

                    self.land_boundaries.append({ "type": BoundaryTypes.weir,
                                                  "nodes": nodes,
                                                  "heights": heights,
                                                  "coeff_of_free_surface_flow": cfsbp })
                else:
                    print "FATAL ERROR!!! Unknown land boundary type {:d}".format(b_type)

            assert len(self.land_boundaries) == number_of_land_boundaries
            assert sum(bdry["nodes"].size for bdry in self.land_boundaries) == \
                total_number_of_land_boundary_nodes

    def get_number_open_boundary_nodes(self):
        return sum(len(arr) for arr in self.open_boundaries)

    def summarize(self):
        print "File located at: {}".format(self.filename)
        print ""
        print "Mesh description: {}".format(self.agrid)
        print "Number of nodes: {:d}".format(self.number_nodes)
        print "Number of elements: {:d}".format(self.number_elements)
        print ""
        print "Number of open boundaries: {:d}".format(len(self.open_boundaries))
        print "Number of open boundary nodes: {:d}".format(sum(len(arr) for arr in self.open_boundaries))
        print ""
        print "Number of land boundaries: {:d}".format(len(self.land_boundaries))
        print "Number of land boundary nodes: {:d}".format(sum(arr["nodes"].size for arr in self.land_boundaries))