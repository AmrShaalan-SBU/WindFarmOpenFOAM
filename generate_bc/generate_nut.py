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
    format      binary;
    arch        "LSB;label=32;scalar=64";
    class       volVectorField;
    location    "0";
    object      {dictName};
}}

// ************************************************************************* //
"""

    return header_string


def generate_nut(nturb, output_folder, nut):
    """Generates 0 file"""

    bc = get_header_string("nut")

    bc += f"""
dimensions      [0 0 -1 0 0 0 0];
internalField   uniform {nut};

boundaryField
{{
    boundaries
    {{
        type symmetry;
    }}
    inlet
    {{
        type fixedValue;
        value uniform {nut};
    }}
    outlet
    {{
        type inletOutlet;
        value uniform {nut};
    }}

"""

    for i in range(nturb):
        bc += f"""

    BladesAndHub_{i}
    {{
        type nutkWallFunction;
        value uniform {nut};
    }}
    AMI_turb{i}_1
    {{
        type cyclicAMI;
        value uniform {nut};
    }}
    AMI_turb{i}_2
    {{
        type cyclicAMI;
        value uniform {nut};
    }}
"""
    bc += """
}
"""

    # Write to file
    output_folder += "/0/"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "nut")

    with open(output_file, "w") as f:
        f.write(bc)

    print(f"(I) nut created at: {output_file}")


