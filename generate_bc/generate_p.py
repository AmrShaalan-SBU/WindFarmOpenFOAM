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
    class       volScalarField;
    location    "0";
    object      {dictName};
}}

// ************************************************************************* //
"""

    return header_string


def generate_p(nturb, output_folder, p):
    """Generates 0 file"""

    bc = get_header_string("p")

    bc += f"""
dimensions      [0 2 -2 0 0 0 0];

internalField   uniform {p};

boundaryField
{{
    boundaries
    {{
        type symmetry;
    }}
    inlet
    {{
        type zeroGradient;
    }}
    outlet
    {{
        type fixedValue;
        value uniform 0;
    }}
"""

    for i in range(nturb):
        bc += f"""

    BladesAndHub_{i}
    {{
        type zeroGradient;
    }}
    AMI_turb{i}_1
    {{
        type cyclicAMI;
        value uniform 0;
    }}
    AMI_turb{i}_2
    {{
        type cyclicAMI;
        value uniform 0;
    }}
"""
    bc += """
}
"""

    # Write to file
    output_folder += "/0/"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "p")

    with open(output_file, "w") as f:
        f.write(bc)

    print(f"(I) p created at: {output_file}")


