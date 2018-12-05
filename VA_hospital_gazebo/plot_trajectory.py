# filename: plot_trajectory.py
# date 12/03/18
#
# by: Abhay Gupta

import pickle
import matplotlib.pyplot as plt

with open('trajectory_xy.pkl', 'rb') as afile:
	P = pickle.load(afile)

import pickle
import gzip
import numpy
import numpy as np
D = np.empty(2)
with open('covariance_matrices.pkl', 'rb') as f:
    u = pickle._Unpickler(f)
    u.encoding = 'latin1'
    p = u.load()

for c,n in enumerate(p):
	if 0 == (c)%3:
		continue
	if c == 0:
		continue
	D = np.append([D],[n[0], n[1]])
D = D.reshape(round(len(D)/2),2)
D = np.delete(D, [0],0)


x = P[:,0]
y = P[:,1]
fig = plt.figure(0)

ax = fig.add_subplot(111, aspect='equal')
plt.plot(x,y, color = 'black')

import numpy as np

mu = np.array([0.4,0.4])
sigma = np.array([[1,0.01],[0.02,1]])

for c, i in enumerate(range(0,9),1):
	mu = np.append([mu], [x[i*55],y[i*55]])
	
Mu = mu.reshape((round(len(mu)/2),2))

for c, i in enumerate(range(1,9),1):
	j = 2*i
	import matplotlib.pyplot as plt
	from matplotlib.patches import Ellipse
	sigma = np.array([[D[j,0], D[j,1]],[D[j+1,0],D[j+1,1]]])

	# compute eigenvalues and associated eigenvectors
	vals, vecs = np.linalg.eigh(sigma)

	# compute "tilt" of ellipse using first eigenvector
	x, y = vecs[:, 0]
	theta = np.degrees(np.arctan2(y, x))

	# eigenvalues give length of ellipse along each eigenvector
	w, h = vals
	ax.add_artist(Ellipse(Mu[i,:], 8*w, 8*h, theta))
	#ax.add_patch(Ellipse(Mu[i,:], w, h, theta))

ax.set_xlim(-40, 5)
ax.set_ylim(-5, 15)
ax.set_xlabel('x (meters)')
ax.set_ylabel('y (meters)')
plt.show()




