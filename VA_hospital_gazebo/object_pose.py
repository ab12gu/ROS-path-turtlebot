# filename: object_pose.py
# by: abhay gupta
#
# date: 11/11/18

# There should be 23 of each wall

import re
import matplotlib.pyplot as plt
import numpy as np
import math as m
import itertools
import pickle

def reformat_numbers(obj):
	"""convert all strings to split floats"""
	temp = {}
	pose = []
	for c, x in enumerate(obj):
		temp_pose = x.split(' ')
		for y in temp_pose:
			pose.append(float(y)+0)
		temp[c] = pose
		pose = []
	return(temp)

def round_values(obj_list, offset):
	"""round all coordinates for grid size"""
	# initialize values
	x = []
	y = []
	rot = []

	for i in obj_list:
		# find all x, y values
		x.append(obj_list[i][0])
		y.append(obj_list[i][1])

		# find if walls were rotated 90 degrees
		temp = obj_list[i][-1]
		print(temp)
		temp = round(temp)/2
		rot.append(temp) # store rotation

	# map coordinates to grid dimensions
	y = [round(100*(10*val+offset))/100 for val in y]
	x = [round(100*(10*val+offset))/100 for val in x]

	return x, y, rot

def wall_expand(H, x, y, rot, obj_list, w, wall_len, lim = 0):
	""" expand wall out of center of mass and add it to grid"""

	rot = [abs(u)%2 for u in rot]

	# loop through all 
	for i in range(0, len(obj_list)):
		y_temp = [m.ceil(y[i]), m.ceil(y[i])-1]
		x_temp = [m.ceil(x[i]), m.ceil(x[i])-1]

		temp = list(itertools.product(y_temp,x_temp))
		for j in temp:
			if lim == 0:
				H[j[0],j[1]] = w

				# add walls
				if rot[i] == 1:
					dy = 0
					dx = 1
				else:
					dy = 1
					dx = 0
				for k in range(1,round(10*wall_len/2+1)):
					H[j[0] + dx*k, j[1] + dy*k] = w
					H[j[0] - dx*k, j[1] - dy*k] = w
			elif lim == -1:
				H[j[0],j[1]] = w

				# remove walls
				if rot[i] == 1:
					dy = 0
					dx = 1
				else:
					dy = 1
					dx = 0
				for k in range(1,round(10*wall_len/2+1)+lim):
					H[j[0] + dx*k, j[1] + dy*k] = w
					H[j[0] - dx*k, j[1] - dy*k] = w
	return H
	
def neighbor_check(P, x, y, t):
	for i in range(-1,2):
		for j in range(-1,2):
			x_nb = x+i
			y_nb = y+j
			if P[x_nb,y_nb] == 0:
				P[x_nb,y_nb] = t
				print(np.amax(P))
				neighbor_check(P, x_nb, y_nb, t+1)
		
# initialize variables
back_wall = set()
side1_wall = set()
side2_wall = set()
door_wall = set()
open_wall = set()

width = 0.15
long_wall = 6
height = 2.5
short_wall = 4
door_width = 1.2

# import in world
with open('gupta_custom.world') as world:
	world_txt = world.read()

object_script = world_txt.splitlines()

# extract the pose of every wall
for c,x in enumerate(object_script):
	if c == len(object_script)-1:
		break

	pose_line = object_script[c+1]
	pose_line = pose_line.replace('<', '>')
	if '>' in pose_line:
		pose = pose_line.split('>')[2]
		if pose == '':
			continue
		#back_wall
		if 'link name=\'Wall_26' in x:
			back_wall.add(pose)
		#side1_wall
		elif 'link name=\'Wall_28' in x: 
			side1_wall.add(pose)
		#side2_wall
		elif 'link name=\'Wall_30' in x: 
			side2_wall.add(pose)
		#door_wall
		elif 'link name=\'Wall_29' in x: 
			door_wall.add(pose)
		#open wall
		elif 'link name=\'Wall_36' in x: 
			open_wall.add(pose)

# reformat numbers from strings to floats
back_wall = reformat_numbers(back_wall)
side1_wall = reformat_numbers(side1_wall)
side2_wall = reformat_numbers(side2_wall)
door_wall = reformat_numbers(door_wall)
open_wall = reformat_numbers(open_wall)

# create nxn grid
# reasonable grid: 1000x1000
n = 1000
H = np.zeros((n,n))
offset = n/2-1


# backwall
weight = 1
# round off wall values
x, y, rot = round_values(back_wall, offset)
# expand wall and add it to grid
H = wall_expand(H, x, y, rot, back_wall, weight, long_wall)

#side1_wall
weight = 1
# round off wall values
x, y, rot = round_values(side1_wall, offset)
# expand wall and add it to grid
H = wall_expand(H, x, y, rot, side1_wall, weight, long_wall)

#side1_wall
weight = 1
# round off wall values
x, y, rot = round_values(side2_wall, offset)
# expand wall and add it to grid
H = wall_expand(H, x, y, rot, side2_wall, weight, long_wall)

#door_wall
weight = 1
# round off wall values
x, y, rot = round_values(door_wall, offset)
# expand wall and add it to grid
H = wall_expand(H, x, y, rot, door_wall, weight, long_wall)

#open_wall
weight = 1
# round off wall values
x, y, rot = round_values(open_wall, offset)
# expand wall and add it to grid
H = wall_expand(H, x, y, rot, open_wall, weight, short_wall)

#door
weight = 0.0
# round off wall values
x, y, rot = round_values(door_wall, offset)

print(rot)
for c, z in enumerate(rot):
	if z == 0:
		x[c] = x[c]+(0.025+door_width/2)*10
	elif z == 1:
		y[c] = y[c]+(0.025+door_width/2)*10
	elif z == 1.5:
		x[c] = x[c]-(0.025+door_width/2)*10
	elif z == -1:
		y[c] = y[c]-(0.025+door_width/2)*10
	elif z == -1.5:
		x[c] = x[c]-(0.025+door_width/2)*10

# expand wall and add it to grid
H = wall_expand(H, x, y, rot , door_wall, weight, door_width, lim = -1)

#plt.scatter(x,y)
#plt.show()
plt.imshow(H, origin='lower')
plt.show()

#path planning algorithm

x_start = 500
y_start = 500

x_end = 630
y_end = 160

P = H*-1+0

with open('outline.pkl','wb') as afile:
	pickle.dump(P, afile)

quit()


search = []
search.append((x_start, y_start))
P[x_start,y_start] = 1
q = 500
dt = 50

print(P[q-dt:q+dt,q-dt:q+dt])
plt.imshow(P[q-dt:q+dt,q-dt:q+dt], origin='lower')
plt.show()

t = 1

while(1):
	x = search[0][0]
	y = search[0][1]
	for i in range(-1,2):
		for j in range(-1,2):
			x_nb = x+i
			y_nb = y+j
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


with open('2d_grid.pkl','wb') as afile:
	pickle.dump(P, afile)

		
		


		

