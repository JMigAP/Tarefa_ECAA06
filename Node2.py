import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import tf
import math

odom = Odometry()
scan = LaserScan()
vel = Twist()
msgs = String()

rospy.init_node('cmd_node2')

estado = 0
center = 1
left = 1
right = 1
st = 'inicial'

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
    
def topCallBack(msgs):
    global st
    st = msgs.data
    
# TIMER - Control Loop ----------------------------------------------
def timerCallBack(event):
    global center, right, left
    global estado
    global st
    
    print (right,center,left,st)
    
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
        vel.angular.z = 0.1
        estado = estado + 1
    
    if right < 0.59 and estado == 2:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
    
    if center < 0.5 and estado == 3:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = 0.1
        estado = estado + 1
        
    if center > 1 and estado == 4:
        estado = estado + 1
    
    if right < 0.59 and estado == 5:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
        pub.publish(vel)
    
    if center < 0.5 and estado == 6:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = 0.1
        estado = estado + 1
        
    if center > 1 and estado == 7:
        estado = estado + 1
    
    if right < 0.59 and estado == 8:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
        pub.publish(vel)
    
    if center < 0.5 and estado == 9:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = 0.1
        estado = estado + 1
        
    if center > 1 and estado == 10:
        estado = estado + 1
    
    if right < 0.59and estado == 11:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
        pub.publish(vel)
    pub.publish(vel)
    
    if center < 0.5 and estado == 12:
        print (right,center,left)
        print (estado)
        vel.linear.x = 0
        vel.angular.z = 0.1
        estado = estado + 1
        
    if center > 1 and estado == 13:
        estado = estado + 1
    
    if right < 0.59 and estado == 14:
        print (right,center,left)
        print (estado)
        vel.linear.x = -0.1
        vel.angular.z = 0
        estado = estado + 1
        pub.publish(vel)

    if center < 0.5 and estado == 15:
        print ('Parado')
        vel.linear.x = 0
        vel.angular.z = 0

    
# -------------------------------------------------------------------

pub = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=10)
#ndois_sub = rospy.Subscriber('/topic1', String, topCallBack)
odom_sub = rospy.Subscriber('/robot2/odom', Odometry, odomCallBack)
scan_sub = rospy.Subscriber('/robot2/scan', LaserScan, scanCallBack)

timer = rospy.Timer(rospy.Duration(0.05), timerCallBack)

rospy.spin()
