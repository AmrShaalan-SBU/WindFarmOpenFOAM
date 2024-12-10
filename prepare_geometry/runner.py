import os
import shutil
import argparse


def copy_stls(stl_folder, output_folder, nturb, dx, dy, diameter):
    """Copies and modifies STL files for multi-turbine setup."""
    D = diameter
    stl_files = [
        "BladesAndHub.stl",
        "AMI.stl",
        "AMI_Refinement.stl",
        "AMI_Refinement_Additional.stl",
        "BladeWakeRefinement.stl",
        "Features.stl",
        "HubRefinement.stl",
        "LeadingEdge.stl",
        "TipTrailingEdge.stl",
    ]

    output_folder += 'constant/triSurface/'
    os.makedirs(output_folder, exist_ok=True)

    for i in range(nturb):
        x_offset = (i % 2) * dy * D  # Alternate turbines in crosswind direction
        y_offset = i * dx * D       # Spacing in downstream direction

        for stl_file in stl_files:
            src_file = os.path.join(stl_folder, stl_file)
            if not os.path.exists(src_file):
                print(f"Warning: {stl_file} not found in {stl_folder}")
                continue

            dest_file = os.path.join(output_folder, f"{stl_file.split('.')[0]}_{i}.stl")

            with open(src_file, "r") as infile, open(dest_file, "w") as outfile:
                for line in infile:
                    if "vertex" in line:
                        parts = line.split()
                        new_coords = [
                            float(parts[1]) + x_offset,
                            float(parts[2]) + y_offset,
                            float(parts[3]),
                        ]
                        outfile.write(f"    vertex {' '.join(map(str, new_coords))}\n")
                    else:
                        outfile.write(line)

    print(f"(I) STL files copied and adjusted for {nturb} turbines in {output_folder}.")


def get_options():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Prepare geometry by copying STL files.")
    parser.add_argument("--stl_folder", type=str, default="Geometry", help="Path to folder containing the base STL files.")
    parser.add_argument("--output_folder", type=str, default="runfolder/", help="Path to output folder for prepared STL files.")
    parser.add_argument("--nturb", type=int, required=True, help="Number of turbines.")
    parser.add_argument("--dx", type=float, required=True, help="Downstream spacing as a multiple of turbine diameter.")
    parser.add_argument("--dy", type=float, required=True, help="Crosswind spacing as a multiple of turbine diameter.")
    parser.add_argument("--diameter", type=float, required=True, help="Turbine diameter (in meters).")
    return parser.parse_args()


def main():
    args = get_options()
    copy_stls(
        stl_folder=args.stl_folder,
        output_folder=args.output_folder,
        nturb=args.nturb,
        dx=args.dx,
        dy=args.dy,
        diameter=args.diameter,
    )


if __name__ == "__main__":
    main()
