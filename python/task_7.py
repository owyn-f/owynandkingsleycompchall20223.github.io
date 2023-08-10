import matplotlib.pyplot as plt
import matplotlib.colors
import math
import numpy as np
import os
import random
import data
import task_5
os.system("python task_5.py")
os.system('data.py')

class Planet:
    def __init__(self, a, eccentricity, beta, period, name):
        self.a = float(a) # semi major axis
        self.eccentricity = float(eccentricity)
        self.beta = float(beta)*(math.pi/180)
        self.period = float(period)
        self.time_function = task_5.time_function(self.a, self.eccentricity, self.beta, self.period, 1)
        self.name = name
    def coords(self, theta):
        r = (self.a*(1-self.eccentricity**2))/(1-self.eccentricity*math.cos(theta))#distance between sun and planet
        x = r*math.cos(theta)
        y = r*math.sin(theta)
        #dist converted to coords, with sun as the origin
        return x, y

    def coords3d(self, theta):
        x, y = self.coords(theta)
        x = x*math.cos(self.beta)
        z = x*math.sin(self.beta)
        return x, y, z

    def tcoords(self, t):
        while t >= self.period:
            t = t - self.period
        theta = self.time_function(t)
        x, y = self.coords(theta)
        return x, y

def dispvector(origin, planet, t):
    x = planet.tcoords(t)[0]-origin.tcoords(t)[0]
    y = planet.tcoords(t)[1]-origin.tcoords(t)[1]
    return x, y

def random_colour():
    colour = random.choice(list(matplotlib.colors.CSS4_COLORS.keys()))
    return colour

def get_outer_planet(system):
    x_neglim = 0
    for planet in system:
        x_neg = planet.coords(np.pi)[0]
        if x_neg < x_neglim:
            x_neglim = x_neg
            outer_planet = planet

    return outer_planet
def solution(system_name, idx):
    plt.style.use('dark_background')
    system_indexes = [5483, 5484, 5485, 5486, 5487, 5488, 5489, 5490, 5491 ]
    system = []
    for i in system_indexes:
        system.append(Planet(*data.get_values(['a', 'ecc', 'beta', 'period', 'name'], i)))

    origin = system[idx]
    system.pop(idx)
    max_t = get_outer_planet(system).period*5
    for i in range(len(system)):
        x_values = []
        y_values = []
        for t in np.linspace(0, max_t, 5000):
            x, y = dispvector(origin, system[i], t)
            x_values.append(x)
            y_values.append(y)
        plt.plot(x_values, y_values, color=random_colour(), label=system[i].name)
        plt.plot(0, 0, 'wo')
    plt.title('System: ' + system_name +', Origin: '+ origin.name)
    plt.legend(loc='upper left')
    plt.show()

solution('solar', 8  )