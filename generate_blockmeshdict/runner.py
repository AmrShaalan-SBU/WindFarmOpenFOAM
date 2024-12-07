import os
import argparse


def get_options():
    """Parse and return command-line options."""
    parser = argparse.ArgumentParser(description="Generate blockMeshDict and turbine STL files for a multi-turbine setup.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
    parser.add_argument("--dx", type=float, required=True, help="Downstream spacing as a multiple of turbine diameter.")
    parser.add_argument("--dy", type=float, required=True, help="Crosswind spacing as a multiple of turbine diameter.")
    parser.add_argument("--diameter", type=float, required=True, help="Turbine diameter (in meters).")
    parser.add_argument("--max_cells", type=int, required=True, help="Maximum number of cells in the largest dimension.")
    parser.add_argument("--output_folder", type=str, default="runfolder", help="Folder to save blockMesh.")
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


def generate_blockMeshDict(nturb, dx, dy, diameter, max_cells):
    """Generates a blockMeshDict with uniform cubic cells."""
    D = diameter
    upwind_length = 5 * D
    downwind_length = 10 * D + dx * D * (nturb - 1)
    lateral_width = 5 * D * 2 + dy * D * (nturb - 1)
    height = 5 * D * 2

    # Determine the largest dimension
    domain_length = downwind_length + upwind_length
    largest_dimension = max(lateral_width, domain_length, height)

    # Calculate uniform cell size
    cell_size = largest_dimension / max_cells

    # Calculate number of cells in each direction
    nx = round(lateral_width / cell_size)
    ny = round(domain_length / cell_size)
    nz = round(height / cell_size)

    print(f"(II) Cell size: {cell_size:.3f}m, Resolutions: nx={nx}, ny={ny}, nz={nz}")

    # Define vertices
    vertices = [
        (-lateral_width / 2, -upwind_length, -height / 2),
        (lateral_width / 2, -upwind_length, -height / 2),
        (lateral_width / 2, downwind_length, -height / 2),
        (-lateral_width / 2, downwind_length, -height / 2),
        (-lateral_width / 2, -upwind_length, height / 2),
        (lateral_width / 2, -upwind_length, height / 2),
        (lateral_width / 2, downwind_length, height / 2),
        (-lateral_width / 2, downwind_length, height / 2),
    ]
    nl = "\n"
    # Create blockMeshDict content
    blockMeshDict = get_header_string("blockMeshDict")
    
    blockMeshDict += f"""\
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

scale   1;

vertices
(
{"".join(f"    ({v[0]} {v[1]} {v[2]}){nl}" for v in vertices)}
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ({nx} {ny} {nz}) simpleGrading (1 1 1)
);

edges
(
);

boundary
(
    inlet
    {{
        type patch;
        faces
        (
            (0 1 5 4)
        );
    }}
    outlet
    {{
        type patch;
        faces
        (
            (3 7 6 2)
        );
    }}
    sides
    {{
        type patch;
        faces
        (
            (1 2 6 5)
            (0 4 7 3)
        );
    }}
    topAndBottom
    {{
        type patch;
        faces
        (
            (4 5 6 7)
            (0 1 2 3)
        );
    }}
);
"""

    # Write to file
    os.makedirs("runfolder/system", exist_ok=True)

    with open("runfolder/system/blockMeshDict", "w") as f:
        f.write(blockMeshDict)

    print("(I) blockMeshDict generated successfully.")

def main():
    args = get_options()

    # Generate blockMeshDict
    generate_blockMeshDict(
        nturb=args.nturb,
        dx=args.dx,
        dy=args.dy,
        diameter=args.diameter,
        max_cells=args.max_cells,
    )


if __name__ == "__main__":
    main()
