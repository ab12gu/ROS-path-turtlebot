import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import message_filters


def callback(image, camera_info):
	print(1)
  # Solve all of perception here...

rospy.init_node('listener', anonymous=True)
image_sub = message_filters.Subscriber('cmd_vel', Twist)
info_sub = message_filters.Subscriber('odom', Odometry)

ts = message_filters.TimeSynchronizer([image_sub, info_sub], 10)
ts.registerCallback(callback)
rospy.spin()
