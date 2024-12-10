import os
import argparse

def get_options():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate transport properties for parallel meshing.")
    parser.add_argument("--output_folder", type=str, default="runfolder", help="Folder to save transport properties.")
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


def generate_fvSolution(output_folder):
    """
    Generates fvSolution dict
    """
    output_folder += "/system/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "fvSolution")

    fvSol = get_header_string("fvSolution")

    fvSol += """


solvers
{
    "pcorr.*"
    {
        solver          GAMG;
        tolerance       1e-2;
        relTol          0;
        smoother        DICGaussSeidel;
        cacheAgglomeration no;
        maxIter         50;
    }

    p
    {
        $pcorr;
        tolerance       1e-5;
        relTol          0.01;
    }

    pFinal
    {
        $p;
        tolerance       1e-6;
        relTol          0;
    }

    "(U|k|omega)"
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-6;
        relTol          0.1;
    }

    "(U|k|omega)Final"
    {
        solver          smoothSolver;
        smoother        symGaussSeidel;
        tolerance       1e-6;
        relTol          0;
    }
}

PIMPLE
{
    correctPhi          no;
    nOuterCorrectors    5;
    nCorrectors         3;
    nNonOrthogonalCorrectors 0;
}

relaxationFactors
{
    "(U|k|omega).*"   0.7;
}

cache
{
    grad(U);
}
"""

    with open(output_file, "w") as file:
        file.write(fvSol)

    print(f"(I) fvSolution created at: {output_file}")


def generate_fvSchemes(output_folder):
    """
    Generates fvSchemes dict
    """
    output_folder += "/system/"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, "fvSchemes")

    fvScheme = get_header_string("fvSchemes")

    fvScheme += """


ddtSchemes
{
    default         Euler;
}

gradSchemes
{
    default         Gauss linear;
    grad(p)         Gauss linear;
    grad(U)         cellLimited Gauss linear 1;
}

divSchemes
{
    default         none;

    div(phi,U)      Gauss linearUpwind grad(U);

    turbulence      Gauss upwind;
    div(phi,k)      $turbulence;
    div(phi,omega) $turbulence;

    div((nuEff*dev2(T(grad(U))))) Gauss linear;
}

laplacianSchemes
{
    default         Gauss linear limited corrected 0.33;
}

interpolationSchemes
{
    default         linear;
}

snGradSchemes
{
    default         limited corrected 0.33;
}

wallDist
{
    method          meshWave;
}
"""

    with open(output_file, "w") as file:
        file.write(fvScheme)

    print(f"(I) fvSchemes created at: {output_file}")


def main():
    args = get_options()
    generate_fvSolution(args.output_folder)
    generate_fvSchemes(args.output_folder)


if __name__ == "__main__":
    main()

