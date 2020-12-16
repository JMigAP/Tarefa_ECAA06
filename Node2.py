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

global estado, mat
estado = 0 
mat = 0

# CALLBACKS ---------------------------------------------------------
def odomCallBack(msg):
    global odom
    odom = msg
    
def scanCallBack(msg):
    global center, right, left
    center = min(msg.ranges[450:630])
    right = min(msg.ranges[200:280])
    left = min(msg.ranges[800:880])
    print(center, right, left)

def topCallBack(msgp):
    global mat
    mat = msgp

# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    global estado, msgp
    
    if center > 0.5 and estado < 5 and mat == 1:
        vel.linear.x = 0.1
        vel.angular.z = 0
        #estado = estado + 1
        
        if center < 0.5:
            vel.linear.x = 0
            vel.angular.z = 0.1
            #estado = estado + 1
            
            if right < 0.5 or left < 0.5:
                vel.angular.z = 0
                vel.linear.x = 0
                estado = estado + 1
    
    print('Estado (2) = ')
    print (estado)            
    
    if estado == 5:
        print('PARADO 2 - Estado = ')
        print (estado)

    pub.publish(vel)
    
    
# -------------------------------------------------------------------

pub = rospy.Publisher('/robot_2/cmd_vel', Twist, queue_size=1)
sub = rospy.Subscriber('/topic1', int, topCallBack)
odom_sub = rospy.Subscriber('/robot_2/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/robot_2/scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()