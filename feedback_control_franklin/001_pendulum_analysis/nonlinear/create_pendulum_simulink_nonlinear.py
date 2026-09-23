#!/usr/bin/env python3
"""Create a nonlinear torque-driven pendulum Simulink model."""

from __future__ import annotations

import argparse
from pathlib import Path

import matlab
import matlab.engine


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the nonlinear pendulum Simulink model."
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
        default="pendulum_simulink_nonlinear",
        help="Name of the Simulink model.",
    )
    return parser.parse_args()


def matlab_string(value: float) -> str:
    return format(value, ".17g")


def main() -> None:
    args = parse_args()
    if args.mass <= 0 or args.length <= 0 or args.gravity <= 0:
        raise ValueError("mass, length, and gravity must all be positive")

    output_path = Path(__file__).resolve().with_name(
        "pendulum_simulink_nonlinear.slx"
    )
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
        if eng.bdIsLoaded(model):
            eng.eval(f"close_system('{model}', 0);", nargout=0)

        eng.new_system(model, nargout=0)
        eng.open_system(model, nargout=0)

        blocks = {
            "step": ("simulink/Sources/Step", [30, 75, 120, 105]),
            "torque_gain_linear": ("simulink/Math Operations/Gain", [150, 65, 250, 105]),
            "sum_linear": ("simulink/Math Operations/Sum", [290, 65, 320, 111]),
            "velocity_linear": ("simulink/Continuous/Integrator", [370, 65, 400, 105]),
            "angle_linear": ("simulink/Continuous/Integrator", [450, 65, 480, 105]),
            "gravity_gain_linear": ("simulink/Math Operations/Gain", [370, 180, 470, 220]),
            "rad2deg_linear": ("simulink/Math Operations/Gain", [520, 65, 600, 105]),
            "torque_gain_nonlinear": ("simulink/Math Operations/Gain", [150, 285, 250, 325]),
            "sum_nonlinear": ("simulink/Math Operations/Sum", [290, 285, 320, 331]),
            "velocity_nonlinear": ("simulink/Continuous/Integrator", [370, 285, 400, 325]),
            "angle_nonlinear": ("simulink/Continuous/Integrator", [450, 285, 480, 325]),
            "sin_angle": ("simulink/Math Operations/Trigonometric Function", [550, 350, 650, 390]),
            "gravity_gain_nonlinear": ("simulink/Math Operations/Gain", [370, 410, 470, 450]),
            "rad2deg_nonlinear": ("simulink/Math Operations/Gain", [520, 285, 600, 325]),
            "mux": ("simulink/Signal Routing/Mux", [680, 135, 710, 225]),
            "scope": ("simulink/Sinks/Scope", [760, 155, 820, 205]),
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
            f"{model}/sum_linear", "Inputs", "|+-", "IconShape", "round", nargout=0
        )
        eng.set_param(
            f"{model}/sum_nonlinear", "Inputs", "|+-", "IconShape", "round", nargout=0
        )
        eng.set_param(
            f"{model}/torque_gain_linear", "Gain", matlab_string(torque_gain), nargout=0
        )
        eng.set_param(
            f"{model}/torque_gain_nonlinear", "Gain", matlab_string(torque_gain), nargout=0
        )
        eng.set_param(f"{model}/sin_angle", "Operator", "sin", "Orientation", "left", nargout=0)
        eng.set_param(
            f"{model}/gravity_gain_linear",
            "Gain",
            matlab_string(gravity_gain),
            "Orientation",
            "left",
            nargout=0,
        )
        eng.set_param(
            f"{model}/gravity_gain_nonlinear",
            "Gain",
            matlab_string(gravity_gain),
            "Orientation",
            "left",
            nargout=0,
        )
        eng.set_param(f"{model}/mux", "Inputs", "2", nargout=0)
        eng.set_param(f"{model}/rad2deg_linear", "Gain", "180/pi", nargout=0)
        eng.set_param(f"{model}/rad2deg_nonlinear", "Gain", "180/pi", nargout=0)
        eng.set_param(
            f"{model}/scope",
            "Decimation",
            "1",
            "LimitDataPoints",
            "off",
            nargout=0,
        )
        for name in (
            "torque_gain_linear",
            "sum_linear",
            "velocity_linear",
            "angle_linear",
            "gravity_gain_linear",
            "rad2deg_linear",
            "torque_gain_nonlinear",
            "sum_nonlinear",
            "velocity_nonlinear",
            "angle_nonlinear",
            "sin_angle",
            "gravity_gain_nonlinear",
            "rad2deg_nonlinear",
        ):
            eng.set_param(f"{model}/{name}", "ShowName", "off", nargout=0)

        eng.eval(
            f"note1 = Simulink.Annotation('{model}/gravity_gain_label_linear'); "
            "note1.Text = 'gravity gain'; "
            "note1.position = [370 235 470 250]; "
            f"note2 = Simulink.Annotation('{model}/gravity_gain_label_nonlinear'); "
            "note2.Text = 'gravity gain'; "
            "note2.position = [370 465 470 480];",
            nargout=0,
        )

        lines = [
            ("step/1", "torque_gain_linear/1"),
            ("step/1", "torque_gain_nonlinear/1"),
            ("torque_gain_linear/1", "sum_linear/1"),
            ("sum_linear/1", "velocity_linear/1"),
            ("velocity_linear/1", "angle_linear/1"),
            ("angle_linear/1", "rad2deg_linear/1"),
            ("rad2deg_linear/1", "mux/1"),
            ("angle_linear/1", "gravity_gain_linear/1"),
            ("gravity_gain_linear/1", "sum_linear/2"),
            ("torque_gain_nonlinear/1", "sum_nonlinear/1"),
            ("sum_nonlinear/1", "velocity_nonlinear/1"),
            ("velocity_nonlinear/1", "angle_nonlinear/1"),
            ("angle_nonlinear/1", "rad2deg_nonlinear/1"),
            ("rad2deg_nonlinear/1", "mux/2"),
            ("angle_nonlinear/1", "sin_angle/1"),
            ("sin_angle/1", "gravity_gain_nonlinear/1"),
            ("gravity_gain_nonlinear/1", "sum_nonlinear/2"),
            ("mux/1", "scope/1"),
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
            nargout=0,
        )
        eng.save_system(model, str(output_path), nargout=0)
        print(f"Created {output_path}")
    finally:
        if eng.bdIsLoaded(model):
            eng.eval(f"close_system('{model}', 0);", nargout=0)
        del eng


if __name__ == "__main__":
    main()
