#!/usr/bin/env python

'''
ME 599 VA Robot
Dylan Reinsdorf
'''

# PURPOSE
# To move TurtleBot3 (tb3) in circle indefinitely in Gazebo environment through ROS.

# USE
# 1. Open launch tb3 in world: $ roslaunch turtlebot3_gazebo [desired world].launch
# 2. Run script in seperate terminal: $ python [path to this script]/tb3circle.py
# 3. Enter CTL+C to stop

import rospy
from geometry_msgs.msg import Twist # for expressing velocity in space with angular and linear terms

class tb3circle():
    def __init__(self):
        rospy.init_node('tb3circle', anonymous=False) # initiliaze node
        rospy.loginfo("To stop turtlebot enter CTRL + C") # tell user how to stop tb3
        rospy.on_shutdown(self.shutdown) # what function to call when you ctrl + c 
       
        self.cmd_vel = rospy.Publisher('cmd_vel', Twist, queue_size=10) # create a publisher that publishes to cmd_vel topic to tb3 which commands tb3 to move
        r = rospy.Rate(10); # publish at a rate of 10hz, else tb3 will stop
        move_cmd = Twist() # declare Twist datatype for velocity move command
        move_cmd.linear.x = 0.4 # define move velocity in x direction [m/s]
        move_cmd.angular.z = 0.2 # define rotation velocity (about z axis) [rad/s]

        while not rospy.is_shutdown(): # as long as you haven't ctrl + c keeping doing...
            self.cmd_vel.publish(move_cmd) # publish the velocity
            r.sleep() # wait for 0.1 seconds (10 HZ) and publish again
            
    def shutdown(self):
        rospy.loginfo("Stop turtlebot") # stop turtlebot
        self.cmd_vel.publish(Twist()) # a default Twist has linear.x of 0 and angular.z of 0, this therefore stops tb3
        rospy.sleep(1) # sleep ensures tb3 receives the stop command prior to shutting down the script
 
if __name__ == '__main__':
    try:
        tb3circle()
    except:
        rospy.loginfo("tb3circle node terminated.")

