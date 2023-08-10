import matplotlib.pyplot as plt
import math
import numpy as np
import os

import data
import task_5
#os.system('data.py')
#os.system("python task_5.py")
class Planet:
    def __init__(self, a, eccentricity, beta, period, name):
        self.a = float(a) # semi major axis
        self.period = float(period)
        self.eccentricity = float(eccentricity)
        self.beta = float(beta)*(math.pi/180)
        self.time_function = task_5.time_function(self.a, self.eccentricity, self.beta, self.period, 1.5)
        self.current_pos = (0, 0)
        self.name = name
    def coords(self, theta):
        r = (self.a*(1-self.eccentricity**2))/(1-self.eccentricity*math.cos(theta))#distance between sun and planet
        x = r*math.cos(theta)
        y = r*math.sin(theta)
        #dist converted to coords, with sun as the origin
        return x, y

    def tcoords(self, t):
        while t > self.period:
            t = t - self.period
        theta = self.time_function(t)
        r = (self.a * (1 - self.eccentricity ** 2)) / (1 - self.eccentricity * math.cos(theta))
        x = r*math.cos(theta)
        y = r*math.sin(theta)
        return x, y

    def spirograph(self, dt, n):
        x_values = []
        y_values = []
        for t in np.arange(0, n, dt):
            x, y = self.tcoords(t)
            x_values.append(x)
            y_values.append(y)
        return x_values, y_values



def spirograph(planet1, planet2):
    if planet1.period > planet2.period:
        n = 10 * planet1.period
    else:
        n = 10 * planet2.period
    dt = n/2000
    x1, y1 = planet1.spirograph(dt, n)
    x2, y2 = planet2.spirograph(dt, n)
    for i in range(len(x1)):
        plt.plot([x1[i], x2[i]], [y1[i], y2[i]], color='white', lw=0.35)

def solution(planet1, planet2):
    colour1 = 'r'
    colour2 = 'b'
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.set_aspect(adjustable='box', aspect='equal')

    spirograph(planet1, planet2)
    x1_values = []
    y1_values = []
    x2_values = []
    y2_values = []
    for theta in np.linspace(0, 2*np.pi, 1000):
        x1, y1 = planet1.coords(theta)
        x2, y2 = planet2.coords(theta)
        x1_values.append(x1)
        y1_values.append(y1)
        x2_values.append(x2)
        y2_values.append(y2)

    plt.plot(x1_values, y1_values, color=colour1, label=planet1.name)
    plt.plot(x2_values, y2_values, color=colour2, label=planet2.name)
    plt.title(planet1.name+' and ' + planet2.name+' Spirograph')
    plt.xlabel('x/AU')
    plt.ylabel('y/AU')
    plt.legend()
    plt.show()

pl1_index = 1
pl2_index = 1

planet1 = Planet(*data.get_values(['a', 'ecc', 'beta', 'period', 'name'], pl1_index))
planet2 = Planet(*data.get_values(['a', 'ecc', 'beta', 'period', 'name'], pl2_index))

solution(planet1, planet2)
