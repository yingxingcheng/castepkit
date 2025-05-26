#!/usr/bin/env python3

from pathlib import Path
from .utils import run_program


def run_weighted_den(calc_name, input_file, suffix, output_format):
    """Run weighted_den.x with given input file and rename output."""
    tmp_fn = f"{calc_name}.wden_in"
    with open(tmp_fn, "w") as f:
        f.write(input_file)

    stdout, stderr = run_program("weighted_den.x", f"{output_format}\n", [calc_name])
    print(f"=== weighted_den.x STDOUT ({suffix}) ===")
    print(stdout)
    if stderr:
        print(f"=== weighted_den.x STDERR ({suffix}) ===")
        print(stderr)

    ext = {1: "pot", 2: "check", 3: "grd"}.get(output_format, "grd")
    output_file = f"{calc_name}_wden.{ext}"
    target_file = f"{calc_name}_{suffix}.{ext}"
    Path(output_file).rename(target_file)


def main():
    parser = argparse.ArgumentParser(description="Wrapper for weighted_den.x")
    parser.add_argument("calc_name", help="Calculation name prefix")
    parser.add_argument(
        "--wden_format",
        type=int,
        choices=[1, 2, 3],
        default=3,
        help="weighted_den.x output format",
    )

    args = parser.parse_args()

    run_weighted_den(
        args.calc_name,
        f"{args.calc_name}.shg_weight_veocc",
        "veocc",
        args.wden_format,
    )
    run_weighted_den(
        args.calc_name,
        f"{args.calc_name}.shg_weight_veunocc",
        "veunocc",
        args.wden_format,
    )


if __name__ == "__main__":
    main()
