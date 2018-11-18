# filename: breath_first.py
# by: abhay gupta
#
# date: 11/17/18
# description: create a breath first search gradient of map with a 
# explicit starting point

# There should be 23 of each wall

import re
import matplotlib.pyplot as plt
import numpy as np
import math as m
import itertools
import pickle

#path planning algorithm

input_file = 'outline_cs.pkl'
output_file = '2d_grid_cs.pkl'

x_start = 500
y_start = 500

x_end = 630
y_end = 160

with open(input_file,'rb') as afile:
	H = pickle.load(afile)

P = H*-1+0

search = []
search.append((x_start, y_start))
P[x_start,y_start] = 1
q = 500
dt = 50

print(P[q-dt:q+dt,q-dt:q+dt])
plt.imshow(P[q-dt:q+dt,q-dt:q+dt], origin='lower')
plt.show()

t = 1

neigh = [(0,1), (1,0), (-1,0), (0,-1)]

while(1):
	x = search[0][0]
	y = search[0][1]
	#for i in range(-1,2):
		#for j in range(-1,2):
			#x_nb = x+i
			#y_nb = y+j
	for i in neigh:
		x_nb = x+i[0]
		y_nb = y+i[1]
		if P[x_nb,y_nb] == 0:
			P[x_nb,y_nb] = P[x,y]+1
			search.append((x_nb,y_nb))
	search.pop(0)
	print(len(search))
	print(np.amax(P))
	if not search:
		break

dr = 5
print(P[q-dr:q+dr,q-dr:q+dr])
plt.imshow(P[q-dt:q+dt,q-dt:q+dt], origin='lower')
plt.show()
plt.imshow(P, origin='lower')
plt.show()
print(np.amax(P))


with open(output_file,'wb') as afile:
	pickle.dump(P, afile)
		

