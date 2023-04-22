import matplotlib.pyplot as plt
import numpy as np

samples = 1001
time_cover = 1000
p0 = 101325
L = 0.0065
T0 = 288.15
M = 0.0289652
g = 9.81
R = 8.31146
Cd = 0.5
A = 10
h = np.linspace(0, 20000, samples)
p = np.power(p0*(1-L*h/T0), (g*M/R/L))
T = T0 - L*h
ue = 2.4e3

rho = p0*M/R/T0*np.power((1 - L*h/T0),(g*M/R/L - 1))

rx = np.zeros((samples, 1))
ry = np.zeros((samples, 1))
Vx = 0.000*np.ones((samples, 1))
Vy = 0.001*np.ones((samples, 1))
ax = np.zeros((samples, 1))
ay = np.zeros((samples, 1))

dm = 2e4  # each falcon 9 engine uses 230 kg fuel

m = np.zeros((samples, 1)) #400 tonne
m[0] = 4.21e6

hh = np.zeros((samples, 1))
time = np.linspace(0, time_cover, samples)
dt = time_cover/(samples - 1)
initial_turn = 150
engine_cutoff = 210
for i in range(1, samples, 1):
    if i < initial_turn:
        m[i] = m[i-1] - dm
        V = np.sqrt(np.power(Vx[i - 1],2) + np.power(Vy[i - 1],2))
        ay[i] = -g  + dm * ue/m[i-1]
        # % ay[i] = -g  + Vy[i-1]/abs(Vy[i-1])*dm * ue/m[i-1]
        ax[i] = 0
    elif i == initial_turn:
        m[i] = m[i-1] - dm
        theta = .1
        V = np.sqrt(np.power(Vx[i - 1],2) + np.power(Vy[i - 1],2))
        a =  dm * ue/m[i-1]
        ay[i] = -g + a * np.cos(theta)
        ax[i] = a * np.sin(theta)
    elif i < engine_cutoff:
        m[i] = m[i-1] - dm
        theta = np.arctan2(abs(ry[i] - ry[i - 1]), abs(rx[i] - rx[i - 1]))
        V = np.sqrt(np.power(Vx[i - 1],2) + np.power(Vy[i - 1],2))
        a = dm * ue/m[i-1]
        ay[i] = -g + a * np.cos(theta)
        ax[i] = a * np.sin(theta)
    else:
        m[i] = m[i-1]
        theta = np.arctan2(abs(ry[i] - ry[i - 1]), abs(rx[i] - rx[i - 1]))
        V = np.sqrt(np.power(Vx[i - 1],2) + np.power(Vy[i - 1],2))
        a = 0
        ay[i] = -g*0.8 + a * np.cos(theta)
        ax[i] = a * np.sin(theta)

    Vy[i] = Vy[i - 1] + ay[i-1] * dt
    Vx[i] = Vx[i - 1] + ax[i-1] * dt
    ry[i] = ry[i - 1] + Vy[i-1] * dt
    rx[i] = rx[i - 1] + Vx[i-1] * dt


fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(rx / 1000, ry / 1000, 'o-')
ax1.set_ylabel('(km)')
ax1.set_xlabel('(km)')

ax2.plot(time, m, '.-')
ax2.set_xlabel('Time(s)')
ax2.set_ylabel('mass (kg)')
# ax2.set_xlabel('(km)')
# ax2.set_ylabel('(km)')

plt.show()

#
#
# figure(2)
# plot(Vx, Vy)
# xlabel('Vx (m/s)')
# grid on
# ylabel('Vy (m/s)')
# hold on
#
# figure(3)
# plot(ax, ay, ".")
# xlabel('ax (m/s^2)')
# grid on
# ylabel('ay (m/s^2)')
# hold on
#
# figure(4)
# plot(m)
# ylabel('m')
# xlabel('time')
# figure(5)
# plot(Vx)
# ylabel('Vx  (m/s)')
# xlabel('time')
#
# figure(6)
# plot(Vy)
# ylabel('Vy  (m/s)')
# xlabel('time')
#
# figure(7)
# plot(ax)
# ylabel('ax (m/s^2)')
# xlabel('time')
# figure(8)
# plot(ay)
# ylabel('ay (m/s^2)')
# xlabel('time')
# % yyaxis
# % yyaxis right
# % plot(time', a) \
#
#            % ylabel('Acceleration (m/s^2)')
