# filename: configuration_space.py
# by: abhay gupta
#
# date: 11/17/18
# description: expand wall's grid size to account for the point mass
# assumption of the turtlebot

import matplotlib.pyplot as plt
import math as m
import pickle
import numpy as np

output_file = 'outline_cs.pkl'

def expand_objects(H):

	J = np.argwhere(H>0)

	for c in range(0,len(J)):
		for n in range(-1,2):
			for m in range(-1,2):
				i = J[c][0]+n
				j = J[c][1]+m
				H[i][j] = 1
	return H

with open('outline.pkl','rb') as afile:
	H = pickle.load(afile)

D = np.copy(H)
H = expand_objects(H)
H = expand_objects(H)
H = expand_objects(H)
H = expand_objects(H)
H = expand_objects(H)

P = H - 0.5*D
q = 500
dt = 50

print(P[q-dt:q+dt,q-dt:q+dt])
plt.imshow(P[q-dt:q+dt,q-dt:q+dt], origin='lower')
plt.show()

plt.imshow(P, origin='lower')
plt.show()

with open(output_file,'wb') as afile:
	pickle.dump(P, afile)
		

