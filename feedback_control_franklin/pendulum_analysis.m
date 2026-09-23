function [G, info] = pendulum_analysis(m, l, g)
%PENDULUM_ANALYSIS Analyze a torque-driven pendulum model.
%   G = PENDULUM_ANALYSIS() analyzes the unit-step torque response for a
%   pendulum with m = 1 kg, l = 1 m, and g = 9.81 m/s^2.
%
%   [G, INFO] = PENDULUM_ANALYSIS(M, L, G) uses the supplied mass M,
%   length L, and gravitational acceleration G. The transfer function is
%
%                 1 / (m*l^2)
%       G(s) = --------------------,
%                  s^2 + g/l
%
%   The input is applied torque and the output is angular displacement.

if nargin < 1 || isempty(m)
    m = 1;
end
if nargin < 2 || isempty(l)
    l = 1;
end
if nargin < 3 || isempty(g)
    g = 9.81;
end

validateattributes(m, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, ...
    mfilename, 'm');
validateattributes(l, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, ...
    mfilename, 'l');
validateattributes(g, {'numeric'}, {'scalar', 'real', 'finite', 'positive'}, ...
    mfilename, 'g');

G = tf(1 / (m * l^2), [1, 0, g / l]);
poles = pole(G);
zeros = zero(G);

info = struct();
info.mass = m;
info.length = l;
info.gravity = g;
info.input = 'Applied torque (N*m)';
info.output = 'Pendulum angle (rad)';
info.poles = poles;
info.zeros = zeros;
info.dc_gain = dcgain(G);
info.is_asymptotically_stable = all(real(poles) < 0);

fprintf('Torque-driven pendulum transfer function:\n');
fprintf('  Mass: %.6g kg\n', m);
fprintf('  Length: %.6g m\n', l);
fprintf('  Gravity: %.6g m/s^2\n\n', g);
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
step(G);
grid on;
title('Unit Step Torque to Pendulum Angle');

figure('Name', 'Pendulum Impulse Response');
impulse(G);
grid on;
title('Impulse Torque to Pendulum Angle');

figure('Name', 'Pendulum Bode Plot');
bode(G);
grid on;
title('Torque-to-Angle Bode Plot');
end
