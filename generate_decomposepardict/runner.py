import argparse
import os

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


def generate_decomposeParDict(output_folder, n_subdomains):
    """
    Generates a decomposeParDict file with the specified number of subdomains.
    """
    decomposeParDict_content = get_header_string("decomposeParDict")

    decomposeParDict_content +=f"""

numberOfSubdomains {n_subdomains};

method          scotch;


// ************************************************************************* //
"""
    output_folder += "system/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "decomposeParDict")

    with open(output_file, "w") as file:
        file.write(decomposeParDict_content)

    print(f"(I) decomposeParDict created at: {output_file}")


def get_options():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate decomposeParDict for parallel meshing.")
    parser.add_argument("--output_folder", type=str, default="runfolder/", help="Folder to save decomposeParDict.")
    parser.add_argument("--n_subdomains", type=int, required=True, help="Number of subdomains for decomposition.")
    return parser.parse_args()


def main():
    args = get_options()
    generate_decomposeParDict(args.output_folder, args.n_subdomains)


if __name__ == "__main__":
    main()
