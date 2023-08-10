
import math
import numpy as np
import matplotlib.pyplot as plt
import scipy
class Planet:
    def __init__(self, a, eccentricity, beta, period):
        self.a = a # semi major axis
        self.eccentricity = eccentricity
        self.beta = beta*(math.pi/180)
        self.period = period
        self.k = self.period*((1-self.eccentricity**2)**(3/2)/(2*math.pi)) # constant to multiply integral

    def integrate(self, N, theta0, theta):
        h = (theta - theta0) / N
        s = self.f(theta0) + self.f(theta)
        for i in range(1, N, 2):
            s += 4 * self.f(theta0 + i * h)
        for i in range(2, N - 1, 2):
            s += 2 * self.f(theta0 + i * h)
        return s * h / 3
    def f(self, theta):
        return 1/(1-self.eccentricity*math.cos(theta))**2

    def orbit_vs_time(self, n):
        x_values = []
        y_values = []
        for theta in np.linspace(0, 2*n*math.pi, 1000):
            y_values.append(theta)
            x_values.append(self.k * self.integrate(1000, 0, theta))

        return x_values, y_values


    def time_function(self, n):
        x_values, y_values = self.orbit_vs_time(n)
        return scipy.interpolate.interp1d(x_values, y_values)



def time_function(a, eccentricity, beta, period, n):
    planet = Planet(a, eccentricity, beta, period)
    return planet.time_function(n)

def presentation():
    pluto = Planet(39.509, 0.25, 17.5, 248.348)
    circle_pluto = Planet(39.509, 0, 17.5, 248.348)
    line1, = plt.plot(pluto.orbit_vs_time(3)[0], pluto.orbit_vs_time(3)[1], color='r')
    line2, = plt.plot(circle_pluto.orbit_vs_time(3)[0], circle_pluto.orbit_vs_time(3)[1], color='b')
    line1.set_label('epsilon = 0.25')
    line2.set_label('epsilon = 0')
    plt.legend()

    plt.title('Orbit angle vs time for Pluto')
    plt.xlabel('t/ Years')
    plt.ylabel('Orbit polar angle/rad')
    plt.show()

presentation()