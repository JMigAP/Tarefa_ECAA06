import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import tf
import math

odom = Odometry()
scan = LaserScan()
vel = Twist()

rospy.init_node('cmd_node1')

estado = 0
center = 1
left = 1
right = 1

# CALLBACKS ---------------------------------------------------------
def odomCallBack(msg):
    global odom
    odom = msg
    
def scanCallBack(msg):
    global center, left, right
    right = min(msg.ranges[50:70])
    center = min(msg.ranges[170:190])
    left = min(msg.ranges[290:310])
    #print(right, center, left)
    
# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    global center, right, left
    global estado
    
    print (right,center,left)
    
    if center > 0.5 and estado == 0:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
    
    if center < 0.5 and estado == 1:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = -0.1
        estado = estado + 1
    
    if left < 0.59 and estado == 2:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
    
    if center < 0.5 and estado == 3:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = -0.1
        estado = estado + 1
        
    if center > 0.6 and estado == 4:
        estado = estado + 1
    
    if left < 0.58 and estado == 5:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
        pub.publish(vel)
    
    pub.publish(vel)
    
# -------------------------------------------------------------------

pub = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=10)
odom_sub = rospy.Subscriber('/robot1/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/robot1/scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
