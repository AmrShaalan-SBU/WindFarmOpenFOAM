import subprocess
import os


def main():
    # Set paths
    geometry_script = "prepare_geometry/runner.py"
    blockmesh_script = "generate_blockmeshdict/runner.py"
    decomposePar_script = "generate_decomposepardict/runner.py"

    # Ensure runfolder exists
    os.makedirs("runfolder", exist_ok=True)

    # Step 1: Prepare Geometry
    print("Preparing geometry...")
    subprocess.run([
        "python", geometry_script,
        "--nturb", "3",
        "--dx", "7",
        "--dy", "2",
        "--diameter", "1.46"

    ])

    # Step 2: Generate BlockMeshDict
    print("Generating blockMeshDict...")
    subprocess.run([
        "python", blockmesh_script,
        "--nturb", "3",
        "--dx", "7",
        "--dy", "2",
        "--diameter", "1.46",
        "--max_cells", "120"
    ])

    print("Setup completed successfully.")

    # Step 3: Generate decomposeParDict
    print(f"Generating decomposeParDict")
    subprocess.run([
        "python", decomposePar_script,
        "--n_subdomains", "95",

    ])

    print("Setup completed successfully.")


if __name__ == "__main__":
    main()
