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

global estado
estado = 0 

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

# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    global estado
    msg = String()
    
    if center > 0.5 and estado < 5:
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
    
    print('Estado = ')
    print (estado)            
    
    if estado == 5:
        print('PARADO - Estado = ')
        print (estado)
        msg.data = 'parado'
        pub.publish(msg)
    
    pub.publish(vel)
    
# -------------------------------------------------------------------

pub = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=1)
pub = rospy.Publisher('/topic1', String, queue_size=1)
odom_sub = rospy.Subscriber('/robot_1/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/robot_1/scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
