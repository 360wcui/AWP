import matplotlib.pyplot as plt
import numpy as np

samples = 201
time_cover = 300
p0 = 101325
L = 0.0065
T0 = 288.15
M = 0.0289652
g = 9.81
R = 8.31146
Cd = 0.5
A = 10
h = np.linspace(0, 20000, samples)
p = p0 * np.power((1-L*h / T0), (g*M / R / L))
T = T0 - L*h
ue = 2.4e3

rho = p0 * M / R / T0 * np.power((1 - L*h/T0),(g*M/R/L - 1))

V = 0.001 * np.ones((samples, 1))
a = np.zeros((samples, 1))

dm = 1.4e4

m = 2.8e6 * np.ones((samples, 1))
h = np.zeros((samples, 1))
time = np.linspace(0, time_cover, samples)
dt = time_cover/(samples - 1)
for i in range(samples):
    m[i] = m[i-1] - dm
    a[i] = -g - 0.5*rho[i-1]*V[i-1]*abs(V[i-1])*Cd*A/m[i-1] + V[i-1]/abs(V[i-1])*dm * ue/m[i-1]
    V[i] = V[i-1] + (a[i])*dt


fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Velocity and Acceleration')

ax1.plot(time, V, 'o-')
ax1.set_ylabel('Velocity (m/s)')

ax2.plot(time, a, '.-')
ax2.set_xlabel('time (s)')
ax2.set_ylabel('Acceleration (m/s^2)')

plt.show()
#
# plt.plot(time, V)
# plt.xlabel('Time(s)')
#
# ylabel('Velocity (m/s)')
# hold on
# yyaxis right
# plt.plot(time', a)
#
# ylabel('Acceleration (m/s^2)')
