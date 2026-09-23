# Repository Guide

This repository contains notes and reference material for learning control
systems.

## Navigation

- [`docs/matlab.md`](docs/matlab.md) — connect Python to a shared MATLAB
  session through the MATLAB Engine API.
- [`books/`](books/) — reference books, including the control-systems PDF.

## Franklin exercise naming

Exercises based on Franklin's control-systems book are organized in a
zero-padded problem directory with descriptive subdirectories for different
modeling approaches:

```text
NNN_<problem>/<model_or_method>/<file>.<extension>
```

The sequence number belongs to the problem directory, not to files inside it.
Files inside a problem directory should use normal descriptive names without
numeric prefixes. Increment `NNN` for a distinct book problem; use a
subdirectory such as `linear` or `nonlinear` for distinct modeling approaches.
For example:

```text
001_pendulum_analysis/linear/pendulum_analysis_linear_approx.m
001_pendulum_analysis/linear/run_pendulum_analysis_linear_approx.py
001_pendulum_analysis/linear/pendulum_analysis_linear_approx.md
001_pendulum_analysis/linear/create_pendulum_simulink.py
001_pendulum_analysis/nonlinear/pendulum_analysis_nonlinear.m
001_pendulum_analysis/nonlinear/run_pendulum_analysis_nonlinear.py
001_pendulum_analysis/nonlinear/create_pendulum_simulink_nonlinear.py
```

## Simulink layout rules

Keep generated diagrams simple and readable:

- Treat the Step block as the applied torque input and place the torque gain
  immediately after it, before the dynamics sum.
- Configure pendulum Sum blocks with the MATLAB R2020a equivalent
  `Inputs = |+-` so the positive input is on the left and the main forward
  signal stays horizontal. (`|+x` is rejected by R2020a.)
- Keep the forward-path blocks aligned on one horizontal row.
- Orient gravity feedback blocks, including `sin(theta)` and its gain, to the
  left so the right-to-left feedback-like signal flow is visually clear.
- Remove To Workspace blocks from these teaching models; use Scope for viewing.
- Keep the model state and feedback signals in radians, and place a `rad2deg`
  Gain block with `Gain = 180/pi` immediately before displayed angle signals.
- For smooth Scope curves, keep the solver variable-step but set a suitable
  maximum step size, such as `MaxStep = 0.01` seconds for this pendulum, and
  set Scope `Decimation = 1` with data-point limiting disabled.
- For nonlinear comparisons, run linear and nonlinear paths in parallel and
  connect both to a two-input Mux before the Scope.

Preserve existing reference material and top-level artifacts unless a task
explicitly targets them.

When a task involves MATLAB and Python integration, read
[`docs/matlab.md`](docs/matlab.md) first.
