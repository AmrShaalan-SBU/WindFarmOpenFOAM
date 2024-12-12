import os
import argparse

def get_options():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate transport properties for parallel meshing.")
    parser.add_argument("--output_folder", type=str, default="runfolder", help="Folder to save transport properties.")
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


def generate_controldict(output_folder):
    """
    Generates fvSolution dict
    """
    output_folder += "/system/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "controlDict")

    fvSol = get_header_string("controlDict")

    fvSol += """


application     pimpleFoam;

startFrom       latestTime;

startTime       0;

stopAt          endTime;

endTime         30;

deltaT          1e-7;

writeControl    adjustable;

writeInterval   0.1;

purgeWrite      0;

writeFormat     binary;

writePrecision  6;

writeCompression off;

timeFormat      general;

timePrecision   6;

runTimeModifiable true;

adjustTimeStep  yes;

maxCo           10.0;

functions
{
    #includeFunc Q

    AMIWeights1
{
    // Mandatory entries
    type             AMIWeights;
    libs             (fieldFunctionObjects);
    writeFields     true;

    // Optional (inherited) entries
    writePrecision   10;
    writeToFile      true;
    useUserTime      false;

    region          region0;
    enabled         true;
    log             true;
    timeStart       0;
    timeEnd         1000;
    executeControl  timeStep;
    executeInterval 1;
    writeControl    writeTime;
    writeInterval  -1;
}
}
"""

    with open(output_file, "w") as file:
        file.write(fvSol)

    print(f"(I) fvSolution created at: {output_file}")



def main():
    args = get_options()
    generate_controldict(args.output_folder)


if __name__ == "__main__":
    main()

