import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import math
import os
import task_5
import data
import random

os.system("python task_5.py")
os.system('data.py')

class Planet:
    def __init__(self, a, eccentricity, beta, period, threed):
        self.a = a # semi major axis
        self.eccentricity = float(eccentricity)
        self.beta = float(beta)*(np.pi/180)
        self.period = float(period)
        self.time_function = task_5.time_function(self.a, self.eccentricity, self.beta, self.period, 1)
        self.threed = threed

        
    def coords2d(self, theta):
        r = (self.a*(1-self.eccentricity**2))/(1-self.eccentricity*np.cos(theta))#distance between sun and planet
        x = r*np.cos(theta)
        y = r*np.sin(theta)
        #dist converted to coords, with sun as the origin
        return x, y

    def coords3d(self, theta):
        x, y = self.coords2d(theta)
        x = x*np.cos(self.beta)
        z = x*np.sin(self.beta)
        return x, y, z

        
    def tcoords(self, t):
        while t >= self.period:
            t = t - self.period
        theta = self.time_function(t)
        return self.coords(theta)

    def coords(self, theta):
        if self.threed:
            return self.coords3d(theta)
        else:
            return self.coords2d(theta)
class Solution:
    def __init__(self, system, threed=False):
        self.system = system
        self.system_name = str(data.get_values(['system_name'], self.system[0])).strip("[']")
        self.threed = threed
        self.fig, self.ax = plt.subplots()
        if self.threed:
            self.ax = self.fig.add_subplot(projection='3d')
            self.title = self.ax.text2D(0.55, 0.95,  "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                                      transform=self.ax.transAxes, ha="center")
        else:
            self.title = self.ax.text(0.5, 0.95,  "", bbox={'facecolor': 'w', 'alpha': 0.5, 'pad': 5},
                                      transform=self.ax.transAxes, ha="center")
        self.colours = self.random_colours(len(system))
        self.planets_pos = [() for l in range(len(system))]
        self.planets = []
        self.names = []
        values = ['a', 'ecc', 'beta', 'period']
        for i in range(len(system)):
            obj = Planet(*data.get_values(values, system[i]), threed)
            self.planets.append(obj)
            self.planets_pos[i], = self.ax.plot(*[[] for j in range(self.threed+2)], ls='', marker='o', color=self.colours[i])
            self.names.append(data.get_values(['name'], system[i]))

    def random_colours(self, n):
        hexadecimal_alphabets = '0123456789ABCDEF'
        colours = ["#" + ''.join([random.choice(hexadecimal_alphabets) for j in range(6)]) for i in range(n)]
        return colours

    def get_outer_planet(self):
        x_neglim = 0
        for planet in self.planets:
            x_neg = planet.coords(np.pi)[0]
            if x_neg < x_neglim:
                x_neglim = x_neg
                outer_planet = planet

        return outer_planet

    def plot(self):
        self.ax.set_facecolor('black')
        self.ax.set_xlabel('x/AU')
        self.ax.set_ylabel('y/AU')
        self.title.set_text('System: %s' % self.system_name)
        if self.threed:
            plt.plot(0, 0, 0, 'yo')
            self.ax.set_zlabel('z/AU')
        else:
            plt.plot(0, 0, 'yo')

    # background plots
        n_dimensions = self.threed + 2
        for i in range(len(self.planets)):
            coord_values = [[] for j in range(n_dimensions)]
            for theta in np.linspace(0, 2 * math.pi, 100):
                coords = self.planets[i].coords(theta)
                for k in range(n_dimensions):
                    coord_values[k].append(coords[k])

            plt.plot(*coord_values, color=self.colours[i], label=self.names[i])
        plt.legend(loc='upper left')

        
    def update(self, frame):
        self.title.set_text('System: %s, t=%d days' % (self.system_name, frame))
        for i in range(len(self.system)):
            coords = self.planets[i].tcoords(frame)
            self.planets_pos[i].set_data([coords[0]], [coords[1]])
            if self.threed:
                self.planets_pos[i].set_3d_properties(coords[2])
        return *self.planets_pos, self.title

        
    def animate(self):
        self.plot()
        anim_end = self.get_outer_planet().period*5
        ani = FuncAnimation(self.fig, self.update, frames=np.linspace(0, anim_end, 2000), blit=True, interval=5)
        plt.show()


solution = Solution(range(1947,1952), threed=False)
# input indexes of planets within dataset, whether threed or not
#solution.plot() just to plot the orbits
solution.plot()
plt.show()