#!/usr/bin/env python3

from pathlib import Path
from .utils import run_program, check_outputs


def main():
    parser = argparse.ArgumentParser(description="Wrapper for computing SHG.")
    parser.add_argument("calc_name", help="Calculation name prefix")
    parser.add_argument(
        "--direction", default="123", help="Direction index (e.g. 111, 123)"
    )
    parser.add_argument(
        "--scissors", type=float, default=0.0, help="Scissors correction in eV"
    )
    parser.add_argument(
        "--band_resolved",
        type=int,
        choices=[0, 1],
        default=1,
        help="Band resolved analysis (0/1)",
    )
    parser.add_argument(
        "--rank_number", type=int, default=0, help="Number of ranked contributions"
    )
    parser.add_argument(
        "--unit", type=int, choices=[0, 1], default=0, help="Output unit: 0=pm/V, 1=esu"
    )
    parser.add_argument(
        "--output_level",
        type=int,
        choices=range(2),
        default=0,
        help="Output verbosity level (0–1)",
    )
    parser.add_argument(
        "--is_metal",
        type=int,
        choices=[1, 2],
        default=2,
        help="Metallic system? 1=Yes, 2=No",
    )
    parser.add_argument(
        "--energy_range",
        type=int,
        choices=[0, 1, 2],
        default=0,
        help="Set energy range? 0/1/2",
    )

    args = parser.parse_args()

    _inputs = [
        args.scissors,
        args.direction,
        args.band_resolved,
        args.rank_number,
        args.unit,
        args.output_level,
        args.is_metal,
        args.energy_range,
    ]
    shg_inputs = "\n".join([str(_inp) for _inp in _inputs]) + "\n"

    stdout, stderr = run_program("NewSHG_ZY-XTIPC.x", shg_inputs, [args.calc_name])
    print("=== SHG STDOUT ===")
    print(stdout)
    if stderr:
        print("=== SHG STDERR ===")
        print(stderr)

    # TODO: add outputs
    # print("\n=== Output File Check ===")
    # check_outputs(outputs)


if __name__ == "__main__":
    main()
