#!/usr/bin/env python3
"""Run the nonlinear pendulum analysis in an already-shared MATLAB session."""

from __future__ import annotations

import argparse
from pathlib import Path

import matlab.engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pendulum_analysis_nonlinear.m in MATLAB."
    )
    parser.add_argument("--mass", type=float, default=1.0, help="Mass in kg.")
    parser.add_argument("--length", type=float, default=1.0, help="Length in m.")
    parser.add_argument(
        "--gravity", type=float, default=9.81, help="Gravitational acceleration in m/s^2."
    )
    parser.add_argument("--torque", type=float, default=1.0, help="Applied torque in N*m.")
    parser.add_argument(
        "--duration", type=float, default=10.0, help="Simulation duration in seconds."
    )
    parser.add_argument(
        "--session", default="matlab", help="Shared MATLAB session name (default: matlab)."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_dir = Path(__file__).resolve().parent

    print(f"Connecting to shared MATLAB session '{args.session}'...")
    try:
        eng = matlab.engine.connect_matlab(args.session)
    except Exception as exc:
        raise RuntimeError(
            f"Could not connect to shared MATLAB session '{args.session}'. "
            "Start MATLAB, run matlab.engine.shareEngine('matlab'), and try again."
        ) from exc

    try:
        eng.addpath(str(repo_dir), nargout=0)
        _, _, info = eng.pendulum_analysis_nonlinear(
            args.mass,
            args.length,
            args.gravity,
            args.torque,
            args.duration,
            nargout=3,
        )
        print(
            "Angle range: "
            f"[{float(info['min_angle']):.6g}, "
            f"{float(info['max_angle']):.6g}] rad; "
            f"[{float(info['min_angle_deg']):.6g}, "
            f"{float(info['max_angle_deg']):.6g}] deg"
        )
    finally:
        # Do not call eng.quit(): that would terminate the user's MATLAB process.
        del eng


if __name__ == "__main__":
    main()
