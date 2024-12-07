import subprocess
import os


def main():
    # Set paths
    geometry_script = "prepare_geometry/runner.py"
    blockmesh_script = "generate_blockmeshdict/runner.py"
    decomposePar_script = "generate_decomposepardict/runner.py"

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


    # Ensure runfolder exists
    os.makedirs("runfolder", exist_ok=True)

    nturb = 3
    dx = 7
    dy = 7
    diameter = 1.46
    max_cells = 120
    n_subdomains = 95

    # running prepare geometry
    try:
        run_preparing_geometry(geometry_script=prepare_geometryScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter)
    except:
        raise Exception("ERROR: run_prepare_geometry Failed")
    else:
        print("(I) run_prepare_geometry ran successfully")


    # running blockmeshdict
    try:
        run_blockMeshDict_generator(blockmesh_script=generate_blockmeshdictScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter, max_cells=max_cells)
    except:
        raise Exception("ERROR: run_blockmeshdict Failed")
    else:
        print("(I) run_blockmeshdict ran successfully")


    # running decomposepardict
    try:
        run_decomposePar_generator(decomposePar_script=generate_decomposepardictScript, n_subdomains=n_subdomains)
    except:
        raise Exception("ERROR: run_decomposepardict Failed")
    else:
        print("(I) run_decomposepardict ran successfully")


    # running snappyhexmeshdict
    try:
        run_snappyHexMeshDict_generator(snappyhex_path=generate_snappyHexMeshDictScript, nturb=nturb, dx=dx, dy=dy, diameter=diameter)
    except:
        raise Exception("ERROR: run_snappyhexmesh Failed")
    else:
        print("(I) run_snappyhexmesh ran successfully")

    print("(I) Setup completed successfully.")


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

        print("decomposeParDict generation completed successfully.")
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
        print("prepare_geometry completed successfully.")
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

        print("blockMeshDict generation completed successfully.")
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
        print("snappyHexMeshDict generation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running snappyHexMeshDict generator: {e}")
        raise



if __name__ == "__main__":
    main()
