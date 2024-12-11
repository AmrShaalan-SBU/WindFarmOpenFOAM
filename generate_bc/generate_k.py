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


def generate_k(nturb, output_folder, k):
    """Generates 0 file"""

    bc = get_header_string("k")

    bc += f"""
dimensions      [0 0 -1 0 0 0 0];
internalField   uniform {k};

boundaryField
{{
    boundaries
    {{
        type symmetry;
    }}
    inlet
    {{
        type fixedValue;
        value uniform {k};
    }}
    outlet
    {{
        type inletOutlet;
        inletValue uniform {k};
        value uniform {k};
    }}

"""

    for i in range(nturb):
        bc += f"""

    BladesAndHub_{i}
    {{
        type kqRWallFunction;
        value uniform {k};
    }}
    AMI_turb{i}_1
    {{
        type cyclicAMI;
    }}
    AMI_turb{i}_2
    {{
        type cyclicAMI;
    }}
"""
    bc += """
}
"""

    # Write to file
    output_folder += "/0/"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "k")

    with open(output_file, "w") as f:
        f.write(bc)

    print(f"(I) k created at: {output_file}")


