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

global estado, center, right, left
estado = 0 

# CALLBACKS ---------------------------------------------------------
def odomCallBack(msg):
    global odom
    odom = msg
    
def scanCallBack(msg):
    right = min(msg.ranges[50:70])
    center = min(msg.ranges[170:190])
    left = min(msg.ranges[290:310])
    #print(right, center, left)
    
# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    print (center)
    if center > 0.5 and estado < 5:
        print (center)
        print ('--')
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
    
    print('Estado (1) = ')
    print (estado)            
    
    if estado == 5:
        print('PARADO (2) - Estado = ')
        print (estado)
        msgp = 1
        
    
    pub.publish(vel)
    
# -------------------------------------------------------------------

pub = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=10)
odom_sub = rospy.Subscriber('/robot1/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/robot1/scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
