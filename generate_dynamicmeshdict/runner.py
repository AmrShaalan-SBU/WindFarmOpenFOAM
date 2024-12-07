import os
import argparse


def get_options():
    """Parse and return command-line options."""
    parser = argparse.ArgumentParser(description="Generate snappyHexMeshDict for a multi-turbine setup.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
    parser.add_argument("--dx", type=float, required=True, help="Downstream spacing as a multiple of turbine diameter.")
    parser.add_argument("--dy", type=float, required=True, help="Crosswind spacing as a multiple of turbine diameter.")
    parser.add_argument("--rps", type=float, required=True, help="Rotation of turbine in rps.")
    parser.add_argument("--output_folder", type=str, default="runfolder", help="Folder to save snappyHexMeshDict.")
    return parser.parse_args()


def get_header_string(dictName):
    """Returns a string with the OpenFOAM dict header using the input dictionary name"""

    header_string = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2312                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      {dictName};
}}
// ************************************************************************* //
"""

    return header_string


def generate_dynamicmeshdict(nturb, dx, dy, rps, output_folder):
    """Generates dynamicMeshDict with same RPM for nturb"""

    dynamicmeshdict = get_header_string("dynamicMeshDict")

    dynamicmeshdict += """
dynamicFvMesh dynamicMotionSolverFvMesh;
motionSolverLibs (fvMotionSolvers);
motionSolver multiSolidBodyMotionSolver;
multiSolidBodyMotionSolverCoeffs
{
"""
    for i in range(nturb):
        dynamicmeshdict += f"""
    turbine_{i}
    {{
        solidBodyMotionFunction rotatingMotion;
        rotatingMotionCoeffs
        {{
            origin ({dx*i} {dy*i} 0);
            axis (0 1 0);
            omega {rps};
        }}
    }}
"""
    dynamicmeshdict += "}\n"

    # Write to file
    os.makedirs(output_folder+"/constant", exist_ok=True)

    with open(output_folder+"/constant/dynamicMeshDict", "w") as f:
        f.write(dynamicmeshdict)

    print("(I) dynamicMeshDict generated successfully.")

def main():
    args = get_options()

    # Generate dynamicMeshDict
    generate_dynamicmeshdict(
        nturb=args.nturb,
        dx=args.dx,
        dy=args.dy,
        rps=args.rps,
        output_folder=args.output_folder
    )


if __name__ == "__main__":
    main()