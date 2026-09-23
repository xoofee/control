#!/usr/bin/env python3
"""Create a Simulink model for the torque-driven pendulum analysis.

The model is created in an already-running, shared MATLAB session.  It uses
the continuous-time equation

    theta_ddot = torque / (m*l^2) - (g/l)*theta

which is equivalent to pendulum_analysis_linear_approx.m's transfer function.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matlab.engine
import matlab


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a torque-driven pendulum Simulink model."
    )
    parser.add_argument("--mass", type=float, default=1.0, help="Mass in kg.")
    parser.add_argument("--length", type=float, default=1.0, help="Length in m.")
    parser.add_argument(
        "--gravity", type=float, default=9.81, help="Gravitational acceleration in m/s^2."
    )
    parser.add_argument("--torque", type=float, default=1.0, help="Applied torque in N*m.")
    parser.add_argument(
        "--session", default="matlab", help="Shared MATLAB session name."
    )
    parser.add_argument(
        "--model-name",
        default="pendulum_simulink",
        help="Name of the Simulink model.",
    )
    return parser.parse_args()


def matlab_string(value: float) -> str:
    """Format a finite Python float for a MATLAB parameter expression."""
    return format(value, ".17g")


def main() -> None:
    args = parse_args()
    if args.mass <= 0 or args.length <= 0 or args.gravity <= 0:
        raise ValueError("mass, length, and gravity must all be positive")

    output_path = Path(__file__).resolve().with_name("pendulum_simulink.slx")
    torque_gain = 1.0 / (args.mass * args.length**2)
    gravity_gain = args.gravity / args.length

    print(f"Connecting to shared MATLAB session '{args.session}'...")
    try:
        eng = matlab.engine.connect_matlab(args.session)
    except Exception as exc:
        raise RuntimeError(
            f"Could not connect to shared MATLAB session '{args.session}'. "
            "Start MATLAB, run matlab.engine.shareEngine('matlab'), and try again."
        ) from exc

    model = args.model_name
    try:
        # Ensure a repeatable rebuild when the model is already open.
        if eng.bdIsLoaded(model):
            eng.eval(f"close_system('{model}', 0);", nargout=0)

        eng.new_system(model, nargout=0)
        eng.open_system(model, nargout=0)

        blocks = {
            "step": ("simulink/Sources/Step", [30, 75, 120, 105]),
            "torque_gain": ("simulink/Math Operations/Gain", [150, 65, 250, 105]),
            "sum": ("simulink/Math Operations/Sum", [290, 65, 320, 111]),
            "velocity": ("simulink/Continuous/Integrator", [370, 65, 400, 105]),
            "angle": ("simulink/Continuous/Integrator", [450, 65, 480, 105]),
            "gravity_gain": ("simulink/Math Operations/Gain", [370, 180, 470, 220]),
            "rad2deg": ("simulink/Math Operations/Gain", [520, 65, 600, 105]),
            "scope": ("simulink/Sinks/Scope", [660, 67, 720, 113]),
        }
        for name, (library_path, position) in blocks.items():
            eng.add_block(
                library_path,
                f"{model}/{name}",
                "Position",
                matlab.double(position),
                nargout=0,
            )

        eng.set_param(
            f"{model}/step",
            "Time",
            "0",
            "Before",
            "0",
            "After",
            matlab_string(args.torque),
            nargout=0,
        )
        eng.set_param(
            f"{model}/sum", "Inputs", "|+-", "IconShape", "round", nargout=0
        )
        eng.set_param(
            f"{model}/torque_gain",
            "Gain",
            matlab_string(torque_gain),
            nargout=0,
        )
        eng.set_param(
            f"{model}/gravity_gain",
            "Gain",
            matlab_string(gravity_gain),
            "Orientation",
            "left",
            nargout=0,
        )
        eng.set_param(f"{model}/rad2deg", "Gain", "180/pi", nargout=0)
        eng.set_param(
            f"{model}/scope",
            "Decimation",
            "1",
            "LimitDataPoints",
            "off",
            nargout=0,
        )
        for name in ("torque_gain", "sum", "velocity", "angle", "gravity_gain", "rad2deg"):
            eng.set_param(f"{model}/{name}", "ShowName", "off", nargout=0)

        eng.eval(
            f"note = Simulink.Annotation('{model}/gravity_gain_label'); "
            "note.Text = 'gravity gain'; "
            "note.position = [370 235 470 250];",
            nargout=0,
        )

        lines = [
            ("step/1", "torque_gain/1"),
            ("torque_gain/1", "sum/1"),
            ("sum/1", "velocity/1"),
            ("velocity/1", "angle/1"),
            ("angle/1", "rad2deg/1"),
            ("rad2deg/1", "scope/1"),
            ("angle/1", "gravity_gain/1"),
            ("gravity_gain/1", "sum/2"),
        ]
        for source, destination in lines:
            eng.add_line(model, source, destination, "autorouting", "on", nargout=0)

        eng.set_param(
            model,
            "StopTime",
            "10",
            "Solver",
            "ode45",
            "SolverType",
            "Variable-step",
            "MaxStep",
            "0.01",
            "SaveOutput",
            "on",
            nargout=0,
        )
        eng.save_system(model, str(output_path), nargout=0)
        print(f"Created {output_path}")
    finally:
        if eng.bdIsLoaded(model):
            # Use MATLAB syntax here so the numeric save flag is not
            # mistaken for close_system's optional new-name argument.
            eng.eval(f"close_system('{model}', 0);", nargout=0)
        del eng


if __name__ == "__main__":
    main()
