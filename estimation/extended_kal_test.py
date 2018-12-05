from filterpy.kalman import ExtendedKalmanFilter
import numpy as np
from filterpy.common import Q_discrete_white_noise
import math as m
from numpy import eye

# Extended Kalman Filter for prediction step
f = ExtendedKalmanFilter(dim_x= 3, dim_z= 3)

x = 0
y = 0
v = 0.4
w = 0.2
theta = 1.57
t = 0.1




quit()

#input
u = np.array([[v]])
f.F = eye(3)

print(-v/w*m.cos(theta)+ v/w*m.cos(theta+w*t))
quit()

f.B = eye(3)

# Process Noise
f.Q = Q_discrete_white_noise(dim=3, dt = 0.1, var = 0.13)

# Covariance Matrix
# Identity matrix multiplied by uncertainty
uncertainty = 1000.
f.P *= uncertainty

#
f.x = np.array([0., 0., 1.])

f.predict(u)

print(f.x_prior)

quit()

def H(x):
	D =  np.array([[x[1],1., 1.],
                [0.,1., 1.],
                [0.,1., 1.]])
	return D



#define initial state
# varables necessary: x, P, R, Q, F, H
#f.R = Q_discrete_white_noise(dim=3, dt = 0.1, var = 0.13)
f.H = np.array([1., 0., 0.])
z = np.array([[10., 10., 10.]])

f.predict_update(z,H,H)

print(f.x)
