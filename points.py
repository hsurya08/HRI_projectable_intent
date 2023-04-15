#! /usr/bin/env python3
   
from mimetypes import init
import rospy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from geometry_msgs.msg import PoseStamped 
from nav_msgs.msg import Path

class Path1:
    def __init__(self):
        self.x = []
        self.y = []
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])         
        self.anim = FuncAnimation(self.fig, self.update_plot, interval=1000)
        
    def update_plot(self, frame):
        self.line.set_xdata(self.x)  # Update x data
        self.line.set_ydata(self.y)  # Update y data
        self.ax.relim()  # Recompute the data limits
        self.ax.autoscale_view()  # Autoscale the plot
        #self.fig.canvas.draw()  # Redraw the plot
        
    def Callback(self,data):
        #print(len(data.poses))
        self.points = []
        for i in data.poses:
            pt = [0.0, 0.0]
            pt[0] = i.pose.position.x
            pt[1] = -i.pose.position.y
            #print(pt)
            self.points.append(pt)
        self.points = np.array(self.points)
        if len(self.points) > 0:
            self.x, self.y = (self.points).T
        #self.update_plot()
        

        


    def path_sub(self):
        rospy.init_node('path', anonymous=True)
        self.ps_sub = rospy.Subscriber('/move_base/NavfnROS/plan', Path, self.Callback,queue_size=1)
        plt.show()
        rospy.spin()

 

 
if __name__ == '__main__':
    try:
        path = Path1()
        path.path_sub()
        

 
    except rospy.ROSInterruptException: pass

