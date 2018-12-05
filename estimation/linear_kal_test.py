from filterpy.kalman import KalmanFilter
import numpy as np

f = KalmanFilter (dim_x=2, dim_z=1)

f.x = np.array([[2.],    # position
                [2.]])   # velocity

u = np.array([[2.],    # position
                [3.]])   # velocity

B = np.array([[1.,0.], [0.,1.]])


F = np.array([[2.,1.], [0.,1.]])

H = np.array([[1.,10.]])

z = np.array([[10.]])

f.predict(u, B=B,F= F)
print(f.x_prior)
f.update(z, H=H)
print(f.x_post)
print(f.x)
quit()
