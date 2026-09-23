#!/usr/bin/env python3
"""Run the pendulum MATLAB analysis in an already-shared MATLAB session."""

from __future__ import annotations

import argparse
from pathlib import Path

import matlab.engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pendulum_analysis.m in the shared MATLAB session."
    )
    parser.add_argument("--mass", type=float, default=1.0, help="Mass in kg.")
    parser.add_argument("--length", type=float, default=1.0, help="Length in m.")
    parser.add_argument(
        "--gravity", type=float, default=9.81, help="Gravitational acceleration in m/s^2."
    )
    parser.add_argument(
        "--session",
        default="matlab",
        help="Shared MATLAB session name (default: matlab).",
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
        eng.pendulum_analysis(args.mass, args.length, args.gravity, nargout=0)
    finally:
        # Do not call eng.quit(): that would terminate the user's shared
        # MATLAB process. The engine handle is released when this process
        # exits, while MATLAB remains running.
        del eng


if __name__ == "__main__":
    main()
