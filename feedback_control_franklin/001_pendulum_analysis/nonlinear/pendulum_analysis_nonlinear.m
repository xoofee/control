function [t, x, info] = pendulum_analysis_nonlinear(m, l, g, tau, t_final)
%PENDULUM_ANALYSIS_NONLINEAR Simulate the nonlinear torque-driven pendulum.
%   The equation is theta_ddot = tau/(m*l^2) - (g/l)*sin(theta).

if nargin < 1 || isempty(m), m = 1; end
if nargin < 2 || isempty(l), l = 1; end
if nargin < 3 || isempty(g), g = 9.81; end
if nargin < 4 || isempty(tau), tau = 1; end
if nargin < 5 || isempty(t_final), t_final = 10; end

validateattributes(m, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'm');
validateattributes(l, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'l');
validateattributes(g, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'g');
validateattributes(tau, {'numeric'}, {'scalar', 'real', 'finite'}, mfilename, 'tau');
validateattributes(t_final, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 't_final');

equilibrium_ratio = tau / (m * g * l);
has_static_equilibrium = abs(equilibrium_ratio) <= 1;
if has_static_equilibrium
    equilibrium_angle = asin(equilibrium_ratio);
else
    equilibrium_angle = NaN;
end

ode = @(~, state) [
    state(2);
    tau / (m * l^2) - (g / l) * sin(state(1))
];
[t, x] = ode45(ode, [0, t_final], [0; 0]);

info = struct();
info.mass = m;
info.length = l;
info.gravity = g;
info.torque = tau;
info.final_time = t_final;
info.input = 'Constant applied torque (N*m)';
info.output = 'Pendulum angle (rad)';
info.equation = 'theta_ddot = tau/(m*l^2) - (g/l)*sin(theta)';
info.has_static_equilibrium = has_static_equilibrium;
info.equilibrium_angle = equilibrium_angle;
info.max_angle = max(x(:, 1));
info.min_angle = min(x(:, 1));
info.max_angle_deg = info.max_angle * 180 / pi;
info.min_angle_deg = info.min_angle * 180 / pi;

fprintf('Nonlinear torque-driven pendulum simulation:\n');
fprintf('  Mass: %.6g kg\n', m);
fprintf('  Length: %.6g m\n', l);
fprintf('  Gravity: %.6g m/s^2\n', g);
fprintf('  Applied torque: %.6g N*m\n', tau);
if has_static_equilibrium
    fprintf('  Static equilibrium angle: %.6g rad\n', equilibrium_angle);
else
    fprintf('  No static equilibrium exists for this torque.\n');
end
fprintf('  Angle range: [%.6g, %.6g] rad\n', info.min_angle, info.max_angle);

figure('Name', 'Nonlinear Pendulum Angle Response');
plot(t, x(:, 1) * 180 / pi, 'LineWidth', 1.2);
grid on;
xlabel('Time (s)');
ylabel('Angle (deg)');
title('Nonlinear Torque-to-Angle Response');

figure('Name', 'Nonlinear Pendulum Phase Plot');
plot(x(:, 1) * 180 / pi, x(:, 2), 'LineWidth', 1.2);
grid on;
xlabel('Angle (deg)');
ylabel('Angular velocity (rad/s)');
title('Nonlinear Pendulum Phase Plot');
end
