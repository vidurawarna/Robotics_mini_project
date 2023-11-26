import numpy as np
import math

class link:
    def __init__(self,i,a,alpha,d,theta):
        # accept the angles from radians 
        self.i = i
        self.a = a
        self.alpha = alpha
        self.d = d
        self.theta = theta
               
    def viewDH(self):
        print(self.dh)
        
    def set_theta(self,theta):
        self.theta = theta
    
    def get_theta(self):
        return self.theta
        
    def set_d(self,d):
        self.d = d
    
    def get_d(self):
        return self.d
    
    def set_a(self,a):
        self.a = a
    
    def get_a(self):
        return self.a
    
    def set_alpha(self,alpha):
        self.alpha = alpha
    
    def get_alpha(self):
        return self.alpha
        
    def calcDH(self):
        self.dh = np.array([[math.cos(self.theta), -math.sin(self.theta)*math.cos(self.alpha), math.sin(self.theta)*math.sin(self.alpha), self.a*math.cos(self.theta)],
                            [math.sin(self.theta), math.cos(self.theta)*math.cos(self.alpha), -math.cos(self.theta)*math.sin(self.alpha), self.a*math.sin(self.theta)],
                            [0, math.sin(self.alpha), math.cos(self.alpha), self.d],
                            [0, 0, 0, 1]])
        
    def get_dh(self):
        return self.dh