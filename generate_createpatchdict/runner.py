import os
import argparse


def get_options():
    """Parse and return command-line options."""
    parser = argparse.ArgumentParser(description="Generate snappyHexMeshDict for a multi-turbine setup.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
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


def generate_createpatchdict(nturb, output_folder):
    """Generates createpatchdict"""

    createpatchdict = get_header_string("createPatchDict")

    createpatchdict += """
pointSync false;

patches
{
"""
    for i in range(nturb):
        createpatchdict += f"""
    {{
        //- Master side patch
        name            AMI_turb{i}_1;
        patchInfo
        {{
            type            cyclicAMI;
            matchTolerance  0.1;
            neighbourPatch  AMI_turb{i}_2;
            transform       noOrdering;
	    lowWeightCorrection 0.05;
        }}
        constructFrom patches;
        patches (AMI_{i});
    }}

    {{
        //- Slave side patch
        name            AMI_turb{i}_2;
        patchInfo
        {{
            type            cyclicAMI;
            matchTolerance  0.1;
            neighbourPatch  AMI_turb{i}_1;
            transform       noOrdering;
	    lowWeightCorrection 0.05;
        }}
        constructFrom patches;
        patches (AMI_{i}_slave);
    }}

"""
    createpatchdict += """
}
"""

    # Write to file
    output_folder += "/system/"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "createPatchDict")

    with open(output_file, "w") as f:
        f.write(createpatchdict)

    print(f"(I) createPatch created at: {output_file}")

def main():
    args = get_options()

    # Generate dynamicMeshDict
    generate_createpatchdict(
        nturb=args.nturb,
        output_folder=args.output_folder
    )


if __name__ == "__main__":
    main()