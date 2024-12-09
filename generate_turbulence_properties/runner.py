import os
import argparse

def get_options():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate turbulence_properties for parallel meshing.")
    parser.add_argument("--output_folder", type=str, default="runfolder/", help="Folder to save turbulence properties.")
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


def generate_turb_prop(output_folder):
    """
    Generates turbulence properties dict
    """
    output_folder += "constant/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "turbulenceProperties")

    tur_prop_content = get_header_string("turbulenceProperties")

    tur_prop_content += """

simulationType      RAS;

RAS
{
    RASModel        kOmegaSST;

    turbulence      on;

    printCoeffs     on;
}


// ************************************************************************* //


"""

    with open(output_file, "w") as file:
        file.write(tur_prop_content)

    print(f"(I) turbulenceProperties created at: {output_file}")


def main():
    args = get_options()
    generate_turb_prop(args.output_folder)


if __name__ == "__main__":
    main()

