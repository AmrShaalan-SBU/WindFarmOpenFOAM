import subprocess
import os


def main():
    # Set paths

    prepare_geometryScript = os.path.join(os.path.dirname(__file__), "prepare_geometry/runner.py")
    if not os.path.exists(prepare_geometryScript):
        raise FileNotFoundError(f"Script {prepare_geometryScript} not found. Ensure it exists in the same directory.")

    generate_blockmeshdictScript = os.path.join(os.path.dirname(__file__), "generate_blockmeshdict/runner.py")
    if not os.path.exists(generate_blockmeshdictScript):
        raise FileNotFoundError(f"Script {generate_blockmeshdictScript} not found. Ensure it exists in the same directory.")

    generate_decomposepardictScript = os.path.join(os.path.dirname(__file__), "generate_decomposepardict/runner.py")
    if not os.path.exists(generate_decomposepardictScript):
        raise FileNotFoundError(f"Script {generate_decomposepardictScript} not found. Ensure it exists in the same directory.")

    generate_snappyHexMeshDictScript = os.path.join(os.path.dirname(__file__), "generate_snappyHexMeshDict/runner.py")
    if not os.path.exists(generate_snappyHexMeshDictScript):
        raise FileNotFoundError(f"Script {generate_snappyHexMeshDictScript} not found. Ensure it exists in the same directory.")

    generate_dynamicmeshdictScript = os.path.join(os.path.dirname(__file__), "generate_dynamicmeshdict/runner.py")
    if not os.path.exists(generate_dynamicmeshdictScript):
        raise FileNotFoundError(f"Script {generate_snappyHexMeshDictScript} not found. Ensure it exists in the same directory.")

    generate_turbPropScript = os.path.join(os.path.dirname(__file__), "generate_turbulence_properties/runner.py")
    if not os.path.exists(generate_turbPropScript):
        raise FileNotFoundError(f"Script {generate_turbPropScript} not found. Ensure it exists in the same directory.")

    generate_tranPropScript = os.path.join(os.path.dirname(__file__), "generate_transportProperties/runner.py")
    if not os.path.exists(generate_tranPropScript):
        raise FileNotFoundError(f"Script {generate_tranPropScript} not found. Ensure it exists in the same directory.")

    generate_createpatchScript = os.path.join(os.path.dirname(__file__), "generate_createpatchdict/runner.py")
    if not os.path.exists(generate_createpatchScript):
        raise FileNotFoundError(f"Script {generate_createpatchScript} not found. Ensure it exists in the same directory.")

    generate_surf_feat_ext_script = os.path.join(os.path.dirname(__file__), "generate_feature_extract/runner.py")
    if not os.path.exists(generate_surf_feat_ext_script):
        raise FileNotFoundError(f"Script {generate_surf_feat_ext_script} not found. Ensure it exists in the same directory.")

    generate_fvFiles_script = os.path.join(os.path.dirname(__file__), "generate_fvFiles/runner.py")
    if not os.path.exists(generate_fvFiles_script):
        raise FileNotFoundError(f"Script {generate_fvFiles_script} not found. Ensure it exists in the same directory.")

    # Ensure runfolder exists
    os.makedirs("runfolder", exist_ok=True)

    nturb = 3
    dx = 7
    dy = 7
    diameter = 1.46
    max_cells = 120
    n_subdomains = 95
    rps = 15.96

    # running prepare geometry
    try:
        run_preparing_geometry(geometry_script=prepare_geometryScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter)
    except:
        raise Exception("ERROR: run_prepare_geometry Failed")

    # running blockmeshdict
    try:
        run_blockMeshDict_generator(blockmesh_script=generate_blockmeshdictScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter, max_cells=max_cells)
    except:
        raise Exception("ERROR: run_blockmeshdict Failed")

    # running decomposepardict
    try:
        run_decomposePar_generator(decomposePar_script=generate_decomposepardictScript, n_subdomains=n_subdomains)
    except:
        raise Exception("ERROR: run_decomposepardict Failed")

    # running snappyhexmeshdict
    try:
        run_snappyHexMeshDict_generator(snappyhex_path=generate_snappyHexMeshDictScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter)
    except:
        raise Exception("ERROR: run_snappyhexmesh Failed")

    # running dynamicMeshDict
    try:
        run_dynamicmeshdict_generator(dynamicmesh_path=generate_dynamicmeshdictScript, nturb=nturb, dx=dx, dy=dy, rps=rps)
    except:
        raise Exception("ERROR: run_dynamicmeshdict Failed")

    # running turbProp
    try:
        run_turbProp_generator(turbulence_prop_path=generate_turbPropScript)
    except:
        raise Exception("ERROR: run_turb_prop Failed")

    # running tranProp
    try:
        run_tranProp_generator(transport_prop_path=generate_tranPropScript)
    except:
        raise Exception("ERROR: run_tran_prop Failed")

    # running createPatch
    try:
        run_createpatch_generator(createpatch_path=generate_createpatchScript, nturb=nturb)
    except:
        raise Exception("ERROR: run_createpatch Failed")

    # running surfaceFeatureExtract
    try:
        run_surf_feat_ext_generator(surf_feat_ext_path=generate_surf_feat_ext_script, nturb=nturb)
    except:
        raise Exception("ERROR: run_surf_feat_ext Failed")

    # running fvFiles
    try:
        run_fvFiles_generator(fvFiles_path=generate_fvFiles_script)
    except:
        raise Exception("ERROR: run_fvFiles Failed")


def run_dynamicmeshdict_generator(dynamicmesh_path, nturb, dx, dy, rps):
    """
    Runs the dynamicMeshDict generator script.
    """
    try:
        subprocess.run([
            "python", dynamicmesh_path,
            "--nturb", str(nturb),
            "--dx", str(dx),
            "--dy", str(dy),
            "--rps", str(rps)

        ])

        check=True

    except subprocess.CalledProcessError as e:
        print(f"Error while running decomposeParMeshDict generator: {e}")
        raise


def run_decomposePar_generator(decomposePar_script, n_subdomains):
    """
    Runs the decomposeParDict generator script.

    Args:
        n_subdomains (int): Number of processors.
    """
    try:
        subprocess.run([
            "python", decomposePar_script,
            "--n_subdomains", str(n_subdomains)

        ])

        check=True

    except subprocess.CalledProcessError as e:
        print(f"Error while running decomposeParMeshDict generator: {e}")
        raise


def run_preparing_geometry(geometry_script, nturb, dx, dy, diameter):
    """
    Runs the prepare_geometry script.

    Args:
        nturb (int): Number of turbines.
        dx (float): Downstream spacing as a multiple of turbine diameter.
        dy (float): Crosswind spacing as a multiple of turbine diameter.
        diameter (float): Turbine diameter (in meters).
    """
    try:
        subprocess.run([
            "python", geometry_script,
            "--nturb", str(nturb),
            "--dx", str(dx),
            "--dy", str(dy),
            "--diameter", str(diameter)

        ])
        check=True
    except subprocess.CalledProcessError as e:
        print(f"Error while running prepare_geometry: {e}")
        raise


def run_blockMeshDict_generator(blockmesh_script, nturb, dx, dy, diameter, max_cells):
    """
    Runs the blockMeshDict generator script.

    Args:
        nturb (int): Number of turbines.
        dx (float): Downstream spacing as a multiple of turbine diameter.
        dy (float): Crosswind spacing as a multiple of turbine diameter.
        diameter (float): Turbine diameter (in meters).
        max_cells (int): Maximum number of cells in the largest dimension.
    """
    try:
        subprocess.run(
            [
                "python", blockmesh_script,
                "--nturb", str(nturb),
                "--dx", str(dx),
                "--dy", str(dy),
                "--diameter", str(diameter),
                "--max_cells", str(max_cells)
            ])

        check=True

    except subprocess.CalledProcessError as e:
        print(f"Error while running blockMeshDict generator: {e}")
        raise


def run_snappyHexMeshDict_generator(snappyhex_path, nturb, dx, dy, diameter):
    """
    Runs the snappyHexMeshDict generator script.

    Args:
        nturb (int): Number of turbines.
        dx (float): Downstream spacing as a multiple of turbine diameter.
        diameter (float): Turbine diameter (in meters).
        output_folder (str): Folder to save the snappyHexMeshDict.
    """

    try:
        subprocess.run(
            [
                "python", snappyhex_path,
                "--nturb", str(nturb),
                "--dx", str(dx),
                "--dy", str(dy),
                "--diameter", str(diameter)
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running snappyHexMeshDict generator: {e}")
        raise


def run_turbProp_generator(turbulence_prop_path):
    """
    Runs the turbulence generator script.
    """

    try:
        subprocess.run(
            [
                "python", turbulence_prop_path
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running turbulenceProperties generator: {e}")
        raise


def run_tranProp_generator(transport_prop_path):
    """
    Runs the transportProperties generator script.
    """

    try:
        subprocess.run(
            [
                "python", transport_prop_path
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running transportProperties generator: {e}")
        raise


def run_createpatch_generator(createpatch_path, nturb):
    """
    Runs the transportProperties generator script.
    """

    try:
        subprocess.run(
            [
                "python", createpatch_path,
                "--nturb", str(nturb)
            ],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Error while running createPatchDict generator: {e}")
        raise


def run_surf_feat_ext_generator(surf_feat_ext_path, nturb):
    """
    Runs the surfaceFeatureExtractDict generator script.
    """

    try:
        subprocess.run(
            [
                "python", surf_feat_ext_path,
                "--nturb", str(nturb)
            ],
            check=True
        )

    except subprocess.CalledProcessError as e:
        print(f"Error while running surfaceFeatureExtractDict generator: {e}")
        raise

def run_fvFiles_generator(fvFiles_path):
    """
    Runs the transportProperties generator script.
    """

    try:
        subprocess.run(
            [
                "python", fvFiles_path
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error while running fvFiles generator: {e}")
        raise

if __name__ == "__main__":
    main()
