import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random



m1 = 1
m2 = 2
m3 = 100000
def random_values():
    a = 200  # scalar
    b = 0.1# another scalar
    x1 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*a
    x2 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*a
    x3 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*a
    v1 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*b
    v2 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*b
    v3 = np.array([random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-4, 4)])*b
    return x1, x2, x3, v1, v2, v3

# equilateral triangle values
def equi_triangle():
    a = 150 # scalar
    b = 0.25 # another scalar
    x1 = np.array([-3, -np.sqrt(3), 2])*a
    x2 = np.array([3, -np.sqrt(3), 1])*a
    x3 = np.array([0, 2*np.sqrt(3), 3])*a
    v1 = np.array([-1/2, np.sqrt(3)/2, 0.5])*b
    v2 = np.array([-1/2, -np.sqrt(3)/2, 1])*b
    v3 = np.array([1, 0, 0])*b
    return x1, x2, x3, v1, v2, v3

def sun_moon_earth():
    G = 6.674*10**-11
    mearth = 5.9722*10**24
    msun = 1.9891*10**30
    mmoon = 7.34767309*10**22
    v2 = np.array([0, np.sqrt(G*msun/147000000), 0]) # earth
    v3 = np.array([0, np.sqrt(G*mearth/363396), 0]) # moon
    v1 = np.array([0, 0, 0]) # sun
    x1 = np.array([0, 0, 0])
    x2 = np.array([-147000, 0, 0])
    x3 = np.array([-147000-363396, 0, 0])
    return x1, x2, x3, v1, v2, v3

def restricted_problem():
    x1 = np.array([0, 0, 0])
    v1 = np.array([0, 1, 1])
    x2 = np.array([100, 0, 0])
    v2 = np.array([0, 2, 0])
    x3 = np.array([200, 0, 0])
    v3 = np.array([0, 4, 0])

    return x1, x2, x3, v1, v2, v3

x1, x2, x3, v1, v2, v3 = restricted_problem()

def magnitude(x, y, z):
    return np.sqrt(float(x)**2+float(y)**2+float(z)**2)

def accelerations(x1, x2, x3):
    #distances between bodies cubed
    d1 = magnitude(*(np.subtract(x2, x1)))**3
    d2 = magnitude(*(np.subtract(x3, x1)))**3
    d3 = magnitude(*(np.subtract(x3, x2)))**3

    G = 30
    a1 = G*((m2*np.subtract(x2, x1))/d1 + (m3*np.subtract(x3, x1))/d2)
    a2 = G*((m3*np.subtract(x3, x2))/d3 + (m1*np.subtract(x1, x2))/d1)
    a3 = G*((m1*np.subtract(x1, x3))/d2 + (m2*np.subtract(x2, x3))/d2)

    return a1, a2, a3

def avg_accelerations_rk4(v1, v2, v3, x1, x2, x3, h):
    k1 = np.array(accelerations(x1, x2, x3))
    k2 = np.array(accelerations(x1+v1*h/2+(k1[0]*(h/2)**2)/2, x2+v2*(h/2)+(k1[1]*(h/2)**2)/2, x3+v3*h/2+(k1[2]*(h/2)**2)/2))
    k3 = np.array(accelerations(x1 + v1 * h / 2 + (k2[0] * (h / 2) ** 2) / 2, x2 + v2 * (h / 2) + (k2[1] * (h/2) ** 2) / 2,
                                x3 + v3 * h / 2 + (k2[2] * (h / 2) ** 2) / 2))
    k4 = np.array(accelerations(x1 + v1 * h + (k3[0] * h ** 2) / 2, x2 + v2 * h + (k3[1] * h ** 2) / 2,
                                x3 + v3 * h + (k3[2] * h ** 2) / 2))
    return np.array((k1+2*k2+2*k3+k4)/6)

def velocities_rk4(v1, v2, v3, accelerations, h):
    #v = u+at
    return np.array([v1, v2, v3]) + accelerations*h


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

plt.style.use('dark_background')

n=300000# number of data points
p1_values = np.array([[0, 0, 0] for i in range(n)], dtype=float)
p2_values = np.array([[0, 0, 0] for i in range(n)], dtype=float)
p3_values = np.array([[0, 0, 0] for i in range(n)], dtype=float)


ln1, = ax.plot([], [], [], color='r')
ln2, = ax.plot([], [], [], color='b')
ln3, = ax.plot([], [], [], color='g')
dot1, = ax.plot([], [], [], color='r', marker='o', ms=2)
dot2, = ax.plot([], [], [], color='b', marker='o', ms=2)
dot3, = ax.plot([], [], [], color='g', marker='o', ms=2)

ln1_data = [[], [], []]
ln2_data = [[], [], []]
ln3_data = [[], [], []]


def init():
    h = 0.1
    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)
    ax.set_zlim(-10000, 10000)
    current_x1 = x1
    current_x2 = x2
    current_x3 = x3
    current_v1 = v1
    current_v2 = v2
    current_v3 = v3

    for i in range(n):
        p1_values[i], p2_values[i], p3_values[i] = current_x1, current_x2, current_x3
        a1, a2, a3 = avg_accelerations_rk4(current_v1, current_v2, current_v3, current_x1, current_x2, current_x3, h)
        #s = ut+1/2at**2 with a being avg acceleration
        current_x1 = current_x1 + current_v1 * h + (a1*h**2)/2
        current_x2 = current_x2 + current_v2 * h + (a2*h**2)/2
        current_x3 = current_x3 + current_v3 * h + (a3*h**2)/2

        velocities = velocities_rk4(current_v1, current_v2, current_v3, np.array([a1, a2, a3]), h)
        current_v1, current_v2, current_v3 = velocities[0], velocities[1], velocities[2]

    return ln1, ln2, ln3, dot1, dot2, dot3

def update(i):
    dot1.set_data(p1_values[i][0:2])
    dot1.set_3d_properties(p1_values[i][2])
    dot2.set_data(p2_values[i][0:2])
    dot2.set_3d_properties(p2_values[i][2])
    dot3.set_data(p3_values[i][0:2])
    dot3.set_3d_properties(p3_values[i][2])
    for j in range(3):
        ln1_data[j].append(p1_values[i][j])
        ln2_data[j].append(p2_values[i][j])
        ln3_data[j].append(p3_values[i][j])
    ln1.set_data(*ln1_data[0:2])
    ln1.set_3d_properties(ln1_data[2])
    ln2.set_data(*ln2_data[0:2])
    ln2.set_3d_properties(ln2_data[2])
    ln3.set_data(*ln3_data[0:2])
    ln3.set_3d_properties(ln3_data[2])
    return ln1, ln2, ln3, dot1, dot2, dot3
plt.style.use('dark_background')
ani = FuncAnimation(fig, update, init_func=init, frames=np.arange(0, n, 1000), blit=True, interval=10)
ani.save('three_bodies4.gif', fps=60)


print(x1)
print(x2)
print(x3)
print(v1)
print(v2)
print(v3)
print(m1)
print(m2)
print(m3)
print('done')
