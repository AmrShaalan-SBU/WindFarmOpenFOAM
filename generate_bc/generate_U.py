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


def generate_U(nturb, output_folder, vel):
    """Generates 0 file"""

    bc = get_header_string("U")

    bc += f"""
dimensions      [0 1 -1 0 0 0 0];
internalField   uniform (0   {vel}   0);

boundaryField
{{
    boundaries
    {{
        type symmetry;
    }}
    inlet
    {{
        type fixedValue;
        value $internalField;
    }}
    outlet
    {{
        type inletOutlet;
        inletValue uniform (0 0 0);
        value uniform (0 0 0);
    }}

"""

    for i in range(nturb):
        bc += f"""

    BladesAndHub_{i}
    {{
        type movingWallVelocity;
        value uniform (0 0 0);
    }}
    
    AMI_turb{i}_1
    {{
        type cyclicAMI;
        value $internalField;
    }}
    
    AMI_turb{i}_2
    {{
        type cyclicAMI;
        value $internalField;
    }}
"""
    bc += """
}
"""

    # Write to file
    output_folder += "/0/"
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "U")

    with open(output_file, "w") as f:
        f.write(bc)

    print(f"(I) U created at: {output_file}")


