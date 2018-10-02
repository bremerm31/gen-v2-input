import argparse
import os

from primitives.fort_14 import Fort14,BoundaryTypes
from primitives.fort_15 import Fort15,Tide
from primitives.fort_dg import FortDG
from primitives.dgswemv2_input import DGSWEMv2Input

def writeBCIS(fort14,fort15):
    mesh_name_base = os.path.splitext(fort14.filename)[0]
    f = open(mesh_name_base+".bcis",'w')

    #Write out all open boundary nodes
    offset = 0
    for i in range(len(fort14.open_boundaries)):
        bdry = fort14.open_boundaries[i]
        num_nodes = len(bdry)

        f.write(str(BoundaryTypes.tide)+"  "+str(num_nodes)+"\n")
        f.write("{:d}\n".format(fort15.nbfr))
        for constituent,tide in enumerate(fort15.tides):
            f.write(str(tide.amig)+" "+str(tide.ff)+" "+str(tide.fface)+"\n")
            for n in range(num_nodes):
                f.write("{:d} {:23.16f} {:23.16f}\n".format(bdry[n],
                                                            tide.emo[n+offset],
                                                            tide.efa[n+offset]))
        offset += num_nodes


    for bdry in fort14.land_boundaries:
        if bdry["type"] == BoundaryTypes.weir:
            f.write("{:d} {:d}".format(BoundaryTypes.weir,
                                       bdry["nodes"].shape[0]))
            for n in range(bdry["nodes"].shape[0]):
                f.write("{:d} {:d} {:23.16f} {:23.16f} {:23.16f}".format(bdry["nodes"][n][0],
                                                                         bdry["nodes"][n][1],
                                                                         bdry["heights"][n],
                                                                         bdry["coeff_of_free_surface_flow"][n][0],
                                                                         bdry["coeff_of_free_surface_flow"][n][1]))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Given dgswem input, generate input for dgswem-v2.")
    parser.add_argument("fort14",
                        help="ADCIRC-formatted mesh file",
                        type=str)
    parser.add_argument("fort15",
                        help="ADCIRC model parameters and periodic boundary conditions",
                        type=str)
    parser.add_argument("fortdg",
                        help="dgswem discontinuous Galerkin input file",
                        type=str)
    parser.add_argument("-o", "--outfile",
                        nargs="?",
                        type=argparse.FileType('w'),
                        help="Name of generated dgswem-v2 input file",
                        default=open('dgswemv2_input.15','w'))
    args = parser.parse_args()

    print 60*"#"
    print "Reading in fort.14"
    print 60*"#"
    fort14 = Fort14(args.fort14)
    fort14.summarize()
    print ""
    print 60*"#"
    print "Reading in fort.15"
    print 60*"#"
    fort15 = Fort15(args.fort15, fort14.get_number_open_boundary_nodes())
    fort15.summarize()
    print ""
    print 60*"#"
    print "Reading in fort.dg"
    print 60*"#"
    fortdg = FortDG(args.fortdg)
    fortdg.summarize()

    v2_input = DGSWEMv2Input(fort14,fort15,fortdg)
    v2_input.dump("dgswemv2_input.15")

    writeBCIS(fort14,fort15)