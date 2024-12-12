import os
import argparse


def get_options():
    """Parse and return command-line options."""
    parser = argparse.ArgumentParser(description="Generate snappyHexMeshDict for a multi-turbine setup.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
    parser.add_argument("--dx", type=float, required=True, help="Downstream spacing as a multiple of turbine diameter.")
    parser.add_argument("--dy", type=float, required=True, help="Crosswind spacing as a multiple of turbine diameter.")
    parser.add_argument("--diameter", type=float, required=True, help="Turbine diameter (in meters).")
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


def get_snappy_preamble():
    """Returns a string meshing options on/off"""
    preamble_string = """castellatedMesh true;
snap true;
addLayers true;
mergeTolerance 1e-6;
"""

    return preamble_string


def generate_snappy_geometry(nturb, dx, dy, D):
    """Generate snappyHexMeshDict geometry section"""

    geometry = f"""
geometry
{{
    """
    # Generate Geometry section for each turbine
    for i in range(nturb):
        x_start = i * dx * D  # Turbine's approximate x-position
        y_start = i * dy * D  # Turbine's y-position for crosswind placement

        # STL-based geometries
        geometry += f"""


    BladesAndHub_{i}.stl
    {{
        type triSurfaceMesh;
        name Turbine{i}_Surface;
    }}
        LeadingEdge_{i}.stl
    {{
        type triSurfaceMesh;
    }}
    TipTrailingEdge_{i}.stl
    {{
        type triSurfaceMesh;
    }}
    AMI_{i}.stl
    {{
        type triSurfaceMesh;
        name AMI_{i};
        regions
        {{
            AMI
            {{
                name AMI_{i};
            }}
        }}
    }}
    AMI_Refinement_{i}.stl
    {{
        type triSurfaceMesh;
    }}
    Turb_WakeRefinement_{i}
    {{
        type searchableCylinder;
        point1 ({dx*(i)} {dy*(i)} 0);
        point2 ({dx*(i)} {dy*(i) + 10*D} 0.5);
        radius {1.2*D/2};
    }}
    """
    geometry += """}
    """
    return geometry


def generate_ref_reg(nturb):
    """Called by generate_castellated_mesh. Creates refinement region subsection"""
    refinement_regions = """
    refinementRegions
    {"""

    for i in range(nturb):
        refinement_regions += f"""
        AMI_{i}
        {{
            mode inside;
            levels ((1 4));
        }}

        LeadingEdge_{i}.stl
        {{
            mode inside;
            levels ((1 5));
        }}

        TipTrailingEdge_{i}.stl
        {{
            mode inside;
            levels ((1 9));
        }}

       Turb_WakeRefinement_{i}
        {{
            mode inside;
            levels ((1 4));
        }}
        
        BladeWakeRefinement_{i}
        {{
            mode inside;
            levels ((1 4));
        }}
        """
    refinement_regions += """
    }"""

    return refinement_regions


def generate_ref_surf(nturb, dx, dy):
    """Called by generate_castellated_mesh. Creates refinement surfaces subsection"""

    refinement_surfaces = """
    refinementSurfaces
    {"""

    for i in range(nturb):
        refinement_surfaces += f"""

        AMI_{i}
        {{
            level (1 5);
        
            faceType boundary;
            cellZone turbine_{i};
            faceZone turbine_{i};
            cellZoneInside insidePoint;
            insidePoint ({dx*(i)} {-0.25+dy*(i)} -0.18);
        }}
        """
        refinement_surfaces += f"""
        BladesAndHub_{i}
        {{
            level (8 8);
        }}

    """
    refinement_surfaces += """
    }"""
    return refinement_surfaces


def generate_features(nturb):
    """Generate Explicit feature edge refinement"""
    features = """
    features
    ("""

    for i in range(nturb):
        features += f"""
        {{
            file "BladesAndHub_{i}.eMesh";
            level 4;
        }}
        
        {{
            file "AMI_Refinement_Additional_{i}.eMesh";
            level 4;
        }}
        
        {{
            file "Features_{i}.eMesh";
            level 6;
        }}
        
        {{
            file "HubRefinement_{i}.eMesh";
            level 6;
        }}
"""

    features += """
    );"""

    return features


def generate_castellated_mesh(nturb, dx, dy):
    """Generate casteallted mesh section: surface refinement and region refinement"""

    # Refinement Parameters
    castellated_mesh = ""

    castellated_mesh += """

castellatedMeshControls
{    
    maxLocalCells 10000000;
    maxGlobalCells 40000000;
    minRefinementCells 10;
    maxLoadUnbalance 0.1;
    nCellsBetweenLevels 3;
    resolveFeatureAngle 20;
    locationInMesh (5 10 0);
    allowFreeStandingZoneFaces true;
    """

    castellated_mesh += generate_ref_surf(nturb, dx, dy)
    castellated_mesh += "\n"
    castellated_mesh += generate_ref_reg(nturb)
    castellated_mesh += "\n"
    castellated_mesh += generate_features(nturb)

    castellated_mesh += """
}
"""
    return castellated_mesh


def generate_snap_controls():
    """generate snap control section of snappyHexMeshDict"""
    snap_controls = """
snapControls
{
    nSmoothPatch 2;
    nSmoothInternal 30;
    tolerance 5.0;
    nSolveIter 400;
    nRelaxIter 10;
    nFeatureSnapIter 25;
    implicitFeatureSnap false;
    explicitFeatureSnap true;
    multiRegionFeatureSnap true;
}"""

    return snap_controls


def generate_addLayers(nturb):
    """Generate AddLayersControls section of SnappyHexMeshDict"""
    addLayers = """
    
addLayersControls
{    
    relativeSizes false;
    layers
    {
"""

    for i in range(nturb):
        addLayers += f"""
        BladesAndHub_{i}
        {{
            nSurfaceLayers 5;
            expansionRatio 1.2;
            firstLayerThickness 0.0001;
            minThickness 0;
            
        }}
        """

    addLayers += """
    }
    
    expansionRatio 1.2;
    firstLayerThickness 0.0001;
    minThickness 0;
    nGrow 0;
    featureAngle 180;
    mergePatchFacesangle 60;
    maxFacethicknessRatio 50;
    slipFeatureAngle 30;
    layerTerminationAngle -180;
    nRelaxIter 20;
    nSmoothSurfaceNormals 12;
    nSmoothNormals 5;
    nSmoothThickness 10;
    maxThicknessToMedialRatio 0.3;
    minMedialAxisAngle 90;
    concaveAngle 180;
    nBufferCellsNoExtrude 0;
    nLayerIter 60;
}
"""

    return addLayers


def generate_mesh_quality():
    """Generates mesh quality section of SnappyHexMeshDict"""
    meshQuality = """
meshQualityControls
{
    maxNonOrtho 65;
    maxBoundarySkewness 4;
    maxInternalSkewness 4;
    maxConcave 180;
    minVol 1e-13;
    minTetQuality -1;
    minArea -1;
    minTwist 0.01;
    minDeterminant 0.01;
    minFaceWeight 0.05;
    minVolRatio 0.01;
    minTriangleTwist -1;
    nSmoothScale 4;
    errorReduction 0.1;
    relaxed
    {
        maxNonOrtho 60;
    }
}
"""
    return meshQuality


def generate_snappy_hex_mesh_dict(nturb, dx, dy, diameter, output_folder):
    """Generate snappyHexMeshDict for a multi-turbine setup."""
    D = diameter
    refinement_diameter = 1.2 * D
    wake_region_length = 15 * D  # Example wake region length

    # Create geometry and refinement region definitions
    geometry = ""
    refinement_regions = ""

    snappyHexMeshDict = get_header_string("snappyHexMeshDict") + "\n"

    snappyHexMeshDict += get_snappy_preamble()

    snappyHexMeshDict += generate_snappy_geometry(nturb=nturb, dx=dx, dy=dy, D=D)

    snappyHexMeshDict += generate_castellated_mesh(nturb=nturb, dx=dx, dy=dy)

    snappyHexMeshDict += generate_snap_controls()

    snappyHexMeshDict += generate_addLayers(nturb=nturb)

    snappyHexMeshDict += generate_mesh_quality()

    # SnappyHexMeshDict content

    snappyHexMeshDict += """

// ************************************************************************* //
"""

    # Write to file
    output_folder += "/system/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "snappyHexMeshDict")
    with open(output_file, "w") as f:
        f.write(snappyHexMeshDict)

    print(f"(I) snappyHexMeshDict created at: {output_file}")


def main():
    args = get_options()

    # Generate snappyHexMeshDict
    generate_snappy_hex_mesh_dict(
        nturb=args.nturb,
        dx=args.dx,
        dy=args.dy,
        diameter=args.diameter,
        output_folder=args.output_folder,
    )


if __name__ == "__main__":
    main()
