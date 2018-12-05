#!/usr/bin/env python
# https://stackoverflow.com/questions/26656943/how-to-get-data-in-python-from-ros-in-real-time
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

def callback(data):
    #rospy.loginfo(rospy.get_caller_id()+"I heard %s",data)
    rospy.loginfo(rospy.get_caller_id())
    print(data.linear.x)
    print(data.angular.z)
    #rospy.rostime.wallsleep(10) #wait time between gathering data

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.spin()
    #while not rospy.core.is_shutdown():
    #     rospy.rostime.wallsleep(0.5)



if __name__ == '__main__':
    listener()
