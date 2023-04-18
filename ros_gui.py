#! /usr/bin/env python3
   
from mimetypes import init
import rospy
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from geometry_msgs.msg import PoseStamped 
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap

class Path1:
    def __init__(self):
        self.x = []
        self.y = []
        self.obstacle = False
        self.goal_reached = False
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], []) 
        self.text_object1 = self.fig.text(0.05, 0.5, "")
        self.text_object2 = self.fig.text(0.05, 0.5, "")

        self.anim = FuncAnimation(self.fig, self.update_plot, interval=1000)
        
    def update_plot(self, frame):
        self.text_object1.set_text(' ')
        self.text_object2.set_text(' ')
        self.ax.clear()
        self.line.set_xdata(self.x)  # Update x data
        self.line.set_ydata(self.y)  # Update y data
        colors = cm.rainbow(np.linspace(1, 0.5, len(self.y)))
        
        
        border_width = 30
        

        if self.obstacle:
            self.message = 'OBSTACLE DETECTED'
            border_color = np.array([228, 235,75])/255
            colors = cm.rainbow(np.linspace(1, 0.8, len(y)))
            fontsz = 60

        elif self.goal_reached:
            self.message = 'Goal: REACHED'
            border_color = np.array([58, 199, 105])/255  
            fontsz = 40 
        else:
            self.message = 'Goal: ROOM 030'
            border_color = np.array([1,1,1])
            fontsz = 40
            
        for i in range(len(self.x)-1):
        	self.ax.plot(self.x[i:i+2], self.y[i:i+2], color=colors[i], linewidth=20)

        self.text_object1 = self.fig.text(0.05, 0.5, f"{self.message}", va='center', rotation=-90, fontsize=fontsz)
        
        self.text_object2 = self.fig.text(0.9, 0.5, f"{self.message}", va='center', rotation=90, fontsize=fontsz)
        self.fig.patch.set_edgecolor(border_color)
        self.fig.patch.set_linewidth(border_width)
        self.ax.axis("off")
        self.ax.relim()  # Recompute the data limits
        self.ax.autoscale_view()  # Autoscale the plot


    def Callback(self,data):
        self.points = []
        #self.obstacle = False
        #self.goal_reached = False
        for i in data.poses:
            pt = [0.0, 0.0]
            new_origin = [self.robot_x, self.robot_y]
            pt[0] = i.pose.position.x - self.robot_x
            pt[1] = i.pose.position.y - self.robot_y
            self.points.append(pt)
        self.points = np.array(self.points)
        if len(self.points) > 5:
            self.x, self.y = (self.points).T
        elif len(self.points) == 4:
            self.goal_reached = True
        #self.update_plot()


    def odom_callback(self, data):
        self.robot_x = data.pose.pose.position.x  # Update robot's x position
        self.robot_y = data.pose.pose.position.y  # Update robot's y position
        q = data.pose.pose.orientation


    def path_sub(self):
        rospy.init_node('path', anonymous=True)
        self.ps_sub = rospy.Subscriber('/move_base/NavfnROS/plan', Path, self.Callback,queue_size=1)
        self.ps_sub1 = rospy.Subscriber('/odom', Odometry, self.odom_callback, queue_size=1)
        plt.show()
        rospy.spin()

 
if __name__ == '__main__':
    try:
        path = Path1()
        path.path_sub()
        

 
    except rospy.ROSInterruptException: pass

