import subprocess
import argparse

__all__ == ["run_program", "check_outputs"]


def run_program(executable, input_str, args=None):
    """Run a program with stdin input and return stdout, stderr."""
    cmd = [executable] + (args or [])
    result = subprocess.run(
        cmd,
        input=input_str.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode(), result.stderr.decode()


def check_outputs(files):
    """Check if output files exist."""
    missing = [f for f in files if not Path(f).is_file()]
    if missing:
        print("❌ Missing output files:")
        for f in missing:
            print(f"  - {f}")
    else:
        print("✅ All output files were generated successfully.")
