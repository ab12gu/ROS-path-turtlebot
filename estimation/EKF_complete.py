##
# filname: EKF_complete.py
# date: 12/3/18
#
# by: Abhay Gupta
##

from filterpy.kalman import ExtendedKalmanFilter
import numpy as np
from filterpy.common import Q_discrete_white_noise

def H(x):
	D =  np.array([[x[1],1., 1.],
                [0.,1., 1.],
                [0.,1., 1.]])
	return H


def Hx(x):
	D =  np.array([[x[1],1., 1.],
                [0.,1., 1.],
                [0.,1., 1.]])
	return D


f = ExtendedKalmanFilter(dim_x= 3, dim_z= 3)
print(f.x)

#define initial state
# varables necessary: x, P, R, Q, F, H
f.x = np.array([0., 0., 0.])

print(f.x)
f.P *= 1000.

f.R = Q_discrete_white_noise(dim=3, dt = 0.1, var = 0.13)
f.Q = Q_discrete_white_noise(dim=3, dt = 0.1, var = 0.13)

f.F = np.array([[1.,1., 1.],
                [0.,1., 1.],
                [0.,1., 1.]])

f.H = np.array([1., 0., 0.])
z = np.array([[10., 10., 10.]])

for t in range(1,10):
	f.predict()
	print(f.x)
	f.update(z,H,H)

	print(f.x)
