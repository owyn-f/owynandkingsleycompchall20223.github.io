import numpy as np
import matplotlib.pyplot as plt

x__values = np.array([ (29.63)**2, (84.75)**2, (11.86)**2, (166.34)**2, (248.35)**2, (1.88)**2, (0.62)**2, (0.24)**2, (1)**2])
Y_values =np.array([ (9.58)**3, (19.29)**3, (5.20)**3, (30.25)**3, (39.51)**3, (1.523)**3, (0.723)**3, (0.387)**3, (1.00)**3])

a, b = np.polyfit(x__values, Y_values, 1)
plt.title("Keplers 3rd law")

plt.scatter(x__values, Y_values)
plt.xlabel("Orbitle period y^2")
plt.ylabel("cube of the semi-major axis Au^3")
#line of best fit 
plt.plot(x__values, a*x__values+b, color='purple', linestyle='--', linewidth=2)
plt.text(1, 60000, 'y= ' + '{:.2f}'.format(b) + '+{:.2f}'.format(a) + 'x', size=14)
plt.plot