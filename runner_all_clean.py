import subprocess


subprocess.run([
            "python",
            "clean_all.py"
        ])

subprocess.run([
            "python",
            "runner_all.py"
        ])