import argparse

from primitives.fort_14 import Fort14
from primitives.fort_15 import Fort15

def generate_v2_input(fort14,fort15,fortdg,v2_input_file):
    v2_input_file.write('################################')

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Given dgswem input, generate input for dgswem-v2.")
    parser.add_argument("fort14",
                        help="ADCIRC-formatted mesh file",
                        type=str)
    parser.add_argument("fort15",
                        help="ADCIRC model parameter and periodic boundary condition file",
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

    generate_v2_input("14","15","dg",args.outfile)