# Linearized pendulum period

The default parameters are:

\[
m = 1\ \mathrm{kg}, \qquad l = 1\ \mathrm{m}, \qquad g = 9.81\ \mathrm{m/s^2}
\]

The pendulum model in `pendulum_analysis_linear_approx.m` is a
small-angle, undamped approximation. Its equation of motion is

\[
m l^2 \ddot{\theta} + m g l\,\theta = \tau,
\]

where \(\theta\) is the angular displacement and \(\tau\) is the applied
torque. Dividing by \(m l^2\) gives

\[
\ddot{\theta} + \frac{g}{l}\theta
= \frac{1}{m l^2}\tau.
\]

Taking the Laplace transform with zero initial conditions produces the
transfer function

\[
G(s) = \frac{\Theta(s)}{\Tau(s)}
= \frac{1/(m l^2)}{s^2 + g/l}.
\]

## Natural frequency

The standard second-order denominator is

\[
s^2 + \omega_n^2,
\]

so the natural frequency is

\[
\omega_n = \sqrt{\frac{g}{l}}.
\]

For the default length and gravity:

\[
\omega_n = \sqrt{\frac{9.81}{1}}
= \sqrt{9.81}
\approx 3.132\ \mathrm{rad/s}.
\]

The poles are therefore

\[
s = \pm j\omega_n \approx \pm j3.132.
\]

They lie on the imaginary axis because the model has no damping.

## Period

Angular frequency and period are related by

\[
\omega_n = \frac{2\pi}{T}.
\]

Therefore,

\[
T = \frac{2\pi}{\omega_n}
= 2\pi\sqrt{\frac{l}{g}}.
\]

Substituting the defaults gives

\[
T = 2\pi\sqrt{\frac{1}{9.81}}
\approx 2.006\ \mathrm{s}.
\]

This is why the simulated oscillation has a period of nearly 2 seconds.

The mass does not appear in the period formula. It changes the torque-to-angle
gain, \(1/(m l^2)\), but it does not change the natural frequency of this
ideal pendulum.

## Relation to the step response

For a unit step torque, the response is

\[
\theta(t) = \frac{1}{m l g}
\left(1 - \cos\left(\sqrt{g/l}\,t\right)\right).
\]

For the default \(m=1\) and \(l=1\), this becomes

\[
\theta(t) = \frac{1}{g}
\left(1 - \cos\left(\sqrt{g/l}\,t\right)\right).
\]

The cosine term repeats every
approximately 2.006 seconds, so the response reaches its first maximum after
approximately 1.003 seconds and then repeats.

This period is the small-angle pendulum result. The full nonlinear equation is

\[
m l^2 \ddot{\theta} + m g l\sin(\theta) = \tau.
\]

The linear model uses \(\sin(\theta) \approx \theta\), which is accurate for
small angular displacements. For larger oscillation amplitudes, the nonlinear
pendulum period becomes amplitude-dependent and is slightly longer than the
small-angle value.
