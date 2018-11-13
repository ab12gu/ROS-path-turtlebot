# filename: trajectory.py
# date 11/13/18
#
# by: Abhay Gupta

import pickle
import matplotlib.pyplot as plt
import numpy as np

with open('2d_grid.pkl', 'rb') as afile:
	P = pickle.load(afile)

with open('outline.pkl', 'rb') as afile:
	outline = pickle.load(afile)

plt.imshow(P, origin='lower')
plt.show()

print(P[500, 500]) #starting point is with value 1

x_end = 160
y_end = 630

dt = 5
print(P[x_end-dt:x_end+dt, y_end-dt:y_end+dt])

n = 1000

H = np.zeros([n,n])
H[x_end,y_end] = 1

x = x_end
y = y_end

lowest_nb = P[x,y];

while(1):
	for i in range(-1, 2):
		for j in range(-1, 2):
			x_nb = x + i
			y_nb = y + j
			#print('grid:', P[x_nb, y_nb])
			#print('start', lowest_nb)
			print('neighbor:' , P[x_nb,y_nb])
			print('current:', P[x,y])
			if P[x_nb, y_nb] < lowest_nb and P[x_nb, y_nb] > 0:
				lowest_nb = P[x_nb, y_nb]
				x_next = x_nb
				y_next = y_nb

	if x == x_next and y == y_next:
		break
	x = x_next
	y = y_next
	H[x,y] = 1
	if P[x,y] == 1:
		break
	print(x,y)

H = outline + H
plt.imshow(H, origin='lower')
plt.show()





				


