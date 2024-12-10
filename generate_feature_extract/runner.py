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


def generate_surf_feat_ext_dict(nturb, output_folder):
    """Generate surfaceFeatureExtractDict for a multi-turbine setup."""
    features = get_header_string("surfaceFeatureExtractDict")

    for i in range(nturb):
        features += f"""
BladesAndHub_{i}.stl
{{
    #include "surfaceFeatureExtractDictDefaults"
}}
AMI_Refinement_Additional{i}.stl
{{
    #include "surfaceFeatureExtractDictDefaults"
}}
Features_{i}.stl
{{
    #include "surfaceFeatureExtractDictDefaults"
}}
HubRefinement_{i}.stl
{{
    #include "surfaceFeatureExtractDictDefaults"
}}
    """

    features += """
writeObj yes;"""




    # Write to file
    os.makedirs(f"{output_folder}/system", exist_ok=True)
    output_path = f"{output_folder}/system/surfaceFeatureExtractDict"
    with open(output_path, "w") as f:
        f.write(features)


    print("(I) surfaceFeatureExtractDict generated successfully")

    features_default = """
extractionMethod    extractFromSurface;
includedAngle       150;

trimFeatures
{
    minElem         10;
}

"""
    # Write to file
    os.makedirs(f"{output_folder}/system", exist_ok=True)
    output_path = f"{output_folder}/system/surfaceFeatureExtractDictDefaults"
    with open(output_path, "w") as f:
        f.write(features_default)

def main():
    args = get_options()

    # Generate snappyHexMeshDict
    generate_surf_feat_ext_dict(
        nturb=args.nturb,
        output_folder=args.output_folder
    )


if __name__ == "__main__":
    main()
