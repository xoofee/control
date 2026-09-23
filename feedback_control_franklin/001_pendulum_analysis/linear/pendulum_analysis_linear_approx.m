function [G, info] = pendulum_analysis_linear_approx(m, l, g, tau)
%PENDULUM_ANALYSIS_LINEAR_APPROX Analyze a linearized torque-driven pendulum.

if nargin < 1 || isempty(m), m = 1; end
if nargin < 2 || isempty(l), l = 1; end
if nargin < 3 || isempty(g), g = 9.81; end
if nargin < 4 || isempty(tau), tau = 1; end

validateattributes(m, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'm');
validateattributes(l, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'l');
validateattributes(g, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, mfilename, 'g');
validateattributes(tau, {'numeric'}, {'scalar', 'real', 'finite'}, mfilename, 'tau');

G = tf(1 / (m * l^2), [1, 0, g / l]);
poles = pole(G);
zeros = zero(G);

info = struct();
info.mass = m;
info.length = l;
info.gravity = g;
info.torque = tau;
info.input = 'Applied torque (N*m)';
info.output = 'Pendulum angle (rad)';
info.poles = poles;
info.zeros = zeros;
info.dc_gain = dcgain(G);
info.is_asymptotically_stable = all(real(poles) < 0);
t_final = 10;
step_time = linspace(0, t_final, 1001);
[step_angle, step_time] = step(tau * G, step_time);
info.step_angle_min_rad = min(step_angle);
info.step_angle_max_rad = max(step_angle);
info.step_angle_min_deg = info.step_angle_min_rad * 180 / pi;
info.step_angle_max_deg = info.step_angle_max_rad * 180 / pi;

fprintf('Torque-driven pendulum transfer function:\n');
fprintf('  Mass: %.6g kg\n', m);
fprintf('  Length: %.6g m\n', l);
fprintf('  Gravity: %.6g m/s^2\n\n', g);
fprintf('  Applied torque: %.6g N*m\n', tau);
disp(G);
fprintf('Poles:\n');
disp(poles);
fprintf('Zeros:\n');
disp(zeros);
fprintf('DC gain: %.6g\n', info.dc_gain);
if info.is_asymptotically_stable
    fprintf('Stability: asymptotically stable\n');
else
    fprintf('Stability: not asymptotically stable (undamped pendulum)\n');
end

figure('Name', 'Pendulum Unit Step Torque Response');
[step_angle, step_time] = step(tau * G, step_time);
plot(step_time, step_angle * 180 / pi, 'LineWidth', 1.2);
grid on;
xlabel('Time (s)');
ylabel('Angle (deg)');
title('Unit Step Torque to Pendulum Angle');

figure('Name', 'Pendulum Impulse Response');
impulse_time = linspace(0, t_final, 1001);
[impulse_angle, impulse_time] = impulse(tau * G, impulse_time);
plot(impulse_time, impulse_angle * 180 / pi, 'LineWidth', 1.2);
grid on;
xlabel('Time (s)');
ylabel('Angle (deg)');
title('Impulse Torque to Pendulum Angle');

figure('Name', 'Pendulum Bode Plot');
bode(G);
grid on;
title('Torque-to-Angle Bode Plot');
end
