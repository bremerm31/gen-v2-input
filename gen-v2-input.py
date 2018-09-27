import argparse


def generate_v2_input(fort14,fort15,fortdg,v2_input_file):
    v2_input_file.write('################################')

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Given dgswem input, generate input for dgswem-v2.")
    parser.add_argument("fort.14",
                        help="ADCIRC-formatted mesh file",
                        type=str)
    parser.add_argument("fort.15",
                        help="ADCIRC model parameter and periodic boundary condition file",
                        type=str)
    parser.add_argument("fort.dg",
                        help="dgswem discontinuous Galerkin input file",
                        type=str)
    parser.add_argument("-o", "--outfile",
                        nargs="?",
                        type=argparse.FileType('w'),
                        help="Name of generated dgswem-v2 input file",
                        default=open('dgswemv2_input.15','w'))
    args = parser.parse_args()
    #fort14 = Fort14(
    generate_v2_input("14","15","dg",args.outfile)