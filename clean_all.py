import os
import shutil


def main():
    runfolder_path = "runfolder"

    if os.path.exists(runfolder_path):
        # Confirm deletion
        user_input = input(f"Are you sure you want to delete all contents of '{runfolder_path}'? (y/N): ").strip().lower()
        if user_input in ['y', 'yes']:
            # Remove the directory and recreate it empty
            shutil.rmtree(runfolder_path)
            os.makedirs(runfolder_path, exist_ok=True)
            print(f"All contents of '{runfolder_path}' have been deleted.")
        else:
            print("Operation canceled. No files were deleted.")
    else:
        print(f"Directory '{runfolder_path}' does not exist. Nothing to clean.")


if __name__ == "__main__":
    main()
