# Calling MATLAB from Python

This guide explains how to connect Python to an already-running MATLAB
session through the MATLAB Engine API.

For python-matlab connection config, see https://xoofee.github.io/posts/2026/09/connect-matlab-r2020a-python-engine-ubuntu/

## Default execution workflow

MATLAB `.m` files and MATLAB command lines should be run from Python in the
already-launched shared MATLAB session by default. This reuses the existing
MATLAB process and avoids the startup cost of a separate MATLAB session.

Running a script directly from MATLAB, or launching a separate MATLAB session,
requires an explicit request.

## Prerequisites

- MATLAB is running.
- The MATLAB Engine API for Python is available in the Python environment.
- The local MATLAB Python environment is activated:

  ```bash
  source ~/pyenvs/matlab/bin/activate
  ```

## Share MATLAB

Run this command in the MATLAB console:

```matlab
matlab.engine.shareEngine('matlab')
```

The argument `'matlab'` is the name that Python will use to find the shared
session. Keep MATLAB running while Python is connected.

## Connect from Python

Start Python after activating the environment, then import the MATLAB Engine
module before using `matlab.engine`:

```python
import matlab.engine

eng = matlab.engine.connect_matlab("matlab")
eng.eval("1+3")
```

Expected result:

```text
4.0
```

The import is required. Running `matlab.engine.connect_matlab("matlab")`
before `import matlab.engine` raises:

```text
NameError: name 'matlab' is not defined
```

## Troubleshooting

### Python cannot find `matlab`

Activate the intended environment before starting Python:

```bash
source ~/pyenvs/matlab/bin/activate
python
```

Then verify the import:

```python
import matlab.engine
```

### Python cannot connect to the session

Check that MATLAB is still running and that the sharing command was executed
with the same session name:

```matlab
matlab.engine.shareEngine('matlab')
```

The Python call must use that exact name:

```python
eng = matlab.engine.connect_matlab("matlab")
```

## Running a MATLAB analysis from Python

For example, run the pendulum torque step-response analysis from the repository
root with:

```bash
source ~/pyenvs/matlab/bin/activate
python run_pendulum_analysis.py --mass 1 --length 1 --gravity 9.81
```

The runner connects to the existing shared session, adds the repository to the
MATLAB path, and calls `pendulum_analysis.m`. The analysis treats the input as
applied torque and the output as pendulum angle, then displays the unit-step,
impulse, and Bode plots in MATLAB.

The MATLAB function can also be called from Python with different parameters:

```python
eng.pendulum_analysis(0.5, 0.8, 9.81, nargout=0)
```

The runner does not start MATLAB automatically. If the shared session is not
available, share the already-running MATLAB session first:

```matlab
matlab.engine.shareEngine('matlab')
```

### MATLAB was closed

The Python engine handle depends on the MATLAB process. Start MATLAB again,
share the engine again, and reconnect from Python.
