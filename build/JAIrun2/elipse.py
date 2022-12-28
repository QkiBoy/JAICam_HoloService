#################################################
import numpy as np
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt
import math

points = [(344,207),(205,341),(-217,145),(-329,-132),(-143,-357),(147,-220)]

a_points = np.array(points)
x = a_points[:, 0]
y = a_points[:, 1]

ell = EllipseModel()
ell.estimate(a_points)

xc, yc, a, b, theta = ell.params
angles = np.array([0, np.pi/2, np.pi, 3*np.pi/2])

aq = [math.pow(a, 2) * math.pow(np.cos([theta, 2)]) + math.pow(b, 2) *math.pow(np.sin(theta), 2)]
bq = 0
cq = - math.pow(a, 2) * math.pow(b, 2)


#x1 = -math.sqrt(-4* aq * cq) + xc
#y1 = 0 - yc

#print(x1, y1)

ellaxes = ell.predict_xy(angles)

print("center = ",  (xc, yc))
print("angle of rotation = ",  theta)
print("axes = ", (a,b))


fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
axs[0].scatter(x,y)

axs[1].scatter(x, y)
axs[1].scatter(xc, yc, color='red', s=100)
axs[1].set_xlim(x.min()-100, x.max()+100)
axs[1].set_ylim(y.min()-100, y.max()+100)
axs[1].scatter(ellaxes[:,1], ellaxes[:,0])

ell_patch = Ellipse((xc, yc), 2*a, 2*b, theta*180/np.pi,
edgecolor='red', facecolor='none')

axs[1].add_patch(ell_patch)
plt.show()
################################################