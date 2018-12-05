#!/usr/bin/env python
# https://stackoverflow.com/questions/26656943/how-to-get-data-in-python-from-ros-in-real-time
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

from filterpy.kalman import ExtendedKalmanFilter
from filterpy.kalman import KalmanFilter
import numpy as np
import math as m
from numpy import eye,dot
import tf

x = 1
theta = 1.57
x_odom = 0.4
y_odom = 0
theta_odom = 0.2
x_pose = 0
y_pose = 0
theta_pose = 0

x0 = np.array([[x_pose],[y_pose],[theta_pose]])
cov_mat = np.array([[x_pose],[y_pose],[theta_pose]])

# Prior covariance matrix
P = eye(3)

def EKF(v, w): 
	global x
	global P
	global x_pose
	global y_pose
	global theta_pose
	global x0
	global cov_mat
	#print(x)
	#print(v)
	#print(w)
	#print(x_odom)
	#print(y_odom)
	#print(theta_odom)
	print('mouse')
	x = x + 1
	t = 0.1

	# Extended Kalman Filter
	# Prediction step

	# State transition Matrix:
	A = eye(3)

	# Control Matrix:
	B = eye(3)
	u = np.array([[-v/w*m.sin(theta)+ v/w*m.sin(theta+w*t)],
				[v/w*m.cos(theta)- v/w*m.cos(theta+w*t)],
				[w*t]])

	# predicted belief
	bel = dot(A,x0)+dot(B,u)
	
	# Jacobian of State Transition Matrix (G in book)
	G = np.array([[1.,0., -v/w*m.cos(theta)+ v/w*m.cos(theta+w*t)],
				[0.,1., -v/w*m.sin(theta)+ v/w*m.sin(theta+w*t)],
				[0.,0., 1.]])

	# updated covariance of belief
	P = dot(G,P).dot(G.T)

	lin_kal = KalmanFilter(dim_x = 3, dim_z = 3)

	lin_kal.P = P
	lin_kal.x = bel

	z = np.array([[x_odom], [y_odom], [theta_odom]])
	
	# Kalman Filter Correction step:
	H = eye(3)
	R = eye(3)
	y = z - dot(H, bel)
	PHT = dot(P, H.T)
	S = dot(H, PHT) + R
	SI = np.zeros((3, 3)) # inverse system uncertainty
	SI = np.linalg.inv(S)
	K = dot(PHT,SI)
	I_KH = eye(3)-dot(K,H)
	P = dot(dot(I_KH, P), I_KH.T) + dot(dot(K, R), K.T)
	x_n = bel + dot(K,y)
	x0 = x_n
	print(bel)
	print(x_n)
	print(P)
	cov_mat = np.append([cov_mat],[P])
	print(cov_mat)
	print(cov_mat.shape)


	#Final Values: covariance: P && pose x_n

def velocity(data):
	#rospy.loginfo(rospy.get_caller_id()+"I heard %s",data)
	rospy.loginfo(rospy.get_caller_id())

	# inputs
	v = data.linear.x
	w = data.angular.z
	#rospy.rostime.wallsleep(10) #wait time between gathering data	

	EKF(v, w)

def odometry(data_odom):
	global x_odom
	global y_odom
	global theta_odom

	"""measurements"""
	#print(data_odom)
	ang_x = data_odom.pose.pose.orientation.x
	ang_y = data_odom.pose.pose.orientation.y
	ang_z = data_odom.pose.pose.orientation.z
	ang_w = data_odom.pose.pose.orientation.w

	(roll, pitch, yaw) = tf.transformations.euler_from_quaternion([
		ang_x,ang_y,ang_z,ang_w])          
	theta_odom = yaw
	#print('check')
	#print(roll)
	#print(pitch)
	#print(yaw)

	x_odom = data_odom.pose.pose.position.x
	y_odom = data_odom.pose.pose.position.y


def listener():
	rospy.init_node('listener', anonymous=True)
	odom_sub = rospy.Subscriber("odom", Odometry, odometry)
	vel_sub = rospy.Subscriber("cmd_vel", Twist, velocity)
	
	#rospy.spin()
	while not rospy.core.is_shutdown():
		if x == 10:
			import  pickle
			print(int(round(len(cov_mat)/3)))
			temp = cov_mat.reshape((int(round(len(cov_mat)/3)),3))
			print(temp)
			with open('covariance_matrices.pkl','wb') as afile:
				pickle.dump(temp,afile)
			quit()
		rospy.rostime.wallsleep(0.1)

if __name__ == '__main__':
	listener()
