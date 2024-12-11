
import argparse
from generate_U import *
from generate_p import *
from generate_omega import *
from generate_k import *
from generate_nut import *

def get_options():
    """Parse and return command-line options."""
    parser = argparse.ArgumentParser(description="Generate snappyHexMeshDict for a multi-turbine setup.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
    parser.add_argument("--vel", type=float, required=True, help="Velocity Magnitude.")
    parser.add_argument("--p", type=float, required=True, help="guage pressure.")
    parser.add_argument("--omega", type=float, required=True, help="turbulence omega")
    parser.add_argument("--k", type=float, required=True, help="turbulence k")
    parser.add_argument("--nut", type=float, required=True, help="turbulence nut")
    parser.add_argument("--output_folder", type=str, default="runfolder", help="Folder to save snappyHexMeshDict.")
    return parser.parse_args()


def main():
    args = get_options()

    # Generate U
    generate_U(
        nturb=args.nturb,
        vel=args.vel,
        output_folder=args.output_folder
    )
    # Generate p
    generate_p(
        nturb=args.nturb,
        p=args.p,
        output_folder=args.output_folder
    )
    # Generate omega
    generate_omega(
        nturb=args.nturb,
        omega=args.omega,
        output_folder=args.output_folder
    )
    # Generate k
    generate_k(
        nturb=args.nturb,
        k=args.k,
        output_folder=args.output_folder
    )
    # Generate nut
    generate_nut(
        nturb=args.nturb,
        nut=args.nut,
        output_folder=args.output_folder
    )



if __name__ == "__main__":
    main()