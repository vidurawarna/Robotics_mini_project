from tkinter import *
from link import *
from tkinter.messagebox import showinfo
import math
import serial 

class input_links:
    global no_of_links
    def __init__(self, master):
        self.root = master
        self.root.withdraw()
        self.master = Toplevel(master)
        self.master.geometry("400x100")
        self.master.title("Robot Control Box")
        self.frame = Frame(self.master)
        self.label = Label(self.frame,text = "Enter number of Links").grid(row=0,column=0)
        self.links = IntVar()
        self.links.set(4)
        self.spinbox = Spinbox(self.frame,from_=2,to=6,increment=1,textvariable = self.links).grid(row=0,column=1)
        self.button = Button(self.frame,bg='green', text='Ok', width=10, command=self.go_to_var_input).grid(row=1,column=1)
        self.frame.pack()
        
    
    def go_to_var_input(self):
        
        self.input_var_window = input_var(self.root,int(self.links.get()))
        
        self.master.withdraw()
    
class input_var:
    
    def __init__(self,master,l):
        
        self.root = master
        self.no_of_links = l
        self.master = Toplevel(self.root)
        self.master.title("Robot Control Box")

        self.selected = []
        self.min_vals = []
        self.max_vals = []
       
        init_min = ['0','0','-135','-90']
        init_max = ['180','180','0','90']
        
        for i in range(1,self.no_of_links+1):
            self.selected.append(StringVar())
            self.min_vals.append(StringVar())
            self.max_vals.append(StringVar())
            
        if len(init_max)==self.no_of_links:
            for i in range(self.no_of_links):
                self.min_vals[i].set(init_min[i])
                self.max_vals[i].set(init_max[i])
        else:
            for i in range(self.no_of_links):
                self.min_vals[i].set('0')
                self.max_vals[i].set('180')  
        self.frame = Frame(self.master)
        
        for i in range(1,self.no_of_links+1):
            
            Label(self.frame,text = "select the variable for link "+str(i)).grid(row=i-1,column=0)
            
            Label(self.frame,text = "       ").grid(row=i-1,column=1)
            
            self.selected[i-1].set('theta')
            Radiobutton(self.frame, text='d(cm)', value='d', variable=self.selected[i-1]).grid(row=i-1,column=2) 
            Radiobutton(self.frame, text='theta(deg)', value='theta', variable=self.selected[i-1]).grid(row=i-1,column=3)   
            
            Label(self.frame,text = "       ").grid(row=i-1,column=4)
               
            Label(self.frame,text = "Min ").grid(row=i-1,column=5)
            # self.min_vals[i-1].set('0')
            Entry(self.frame,width = 10,textvariable=self.min_vals[i-1]).grid(row=i-1,column=6)
            
            Label(self.frame,text = "Max ").grid(row=i-1,column=7)
            # self.max_vals[i-1].set('180')
            Entry(self.frame,width = 10,textvariable=self.max_vals[i-1]).grid(row=i-1,column=8)
        
  
        Button(self.frame, text='Ok',bg='green', width=15,command=self.go_to_control).grid(row=self.no_of_links+1,column = 4) 
        self.frame.pack()
        
    def go_to_control(self):

        for i in range(self.no_of_links):
            if len(self.min_vals[i].get())==0 or len(self.max_vals[i].get())==0 or len(self.selected[i].get())==0:
                self.error_msg()
                break
        else: 
            self.control_window = control_window(self.root,self.no_of_links,self.selected,self.min_vals,self.max_vals)         
            self.master.withdraw()
        
    def error_msg(self):
        showinfo(
        title='Error',
        message="Please input ranges and select variables"
        )   
        
class control_window:
    
    def __init__(self,master,l,var,mins,maxs):
        
        init_alpha = [90,0,0,0]
        init_a = [1.3,12,12,11]
        init_d = [9.5,0,0,0]
        init_theta = [0,90,-90,-90]
        init_ori = -90
        
        self.root = master
        self.no_of_links = l
        self.selected = var
        self.min_vals = mins
        self.max_vals = maxs
        
        self.links = []
            
        self.alpha = []
        self.a = []
        self.d = []
        self.theta = []
        
        self.pos  = [DoubleVar() for i in range(3)]
        self.EF_ori = IntVar()
        self.EF_ori.set(init_ori)
        self.pos_limit = 30
        self.solution = StringVar()
        self.joint_angles = []
        self.bg_color=StringVar()
        self.bg_color.set('red')
        
        self.output_mat_disp = [[StringVar() for m in range (4)] for n in range(4)]
        
        self.arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
              
        for i in range(self.no_of_links):
            self.a.append(DoubleVar())
            self.alpha.append(DoubleVar())
            self.d.append(DoubleVar())
            self.theta.append(DoubleVar())
            
        if self.no_of_links==len(init_a):
            for i in range(4):
                self.a[i].set(init_a[i])
                self.alpha[i].set(init_alpha[i])
                self.d[i].set(init_d[i])
                self.theta[i].set(init_theta[i])
                  
        for i in range(self.no_of_links):
            self.links.append(link(i+1,self.a[i].get(),math.radians(self.alpha[i].get()),self.d[i].get(),math.radians(self.theta[i].get())))
        
        self.master = Toplevel(self.root)
        self.master.geometry("1150x650")
        self.master.title("Robot Control Box")
            
        self.frame = Frame(self.master)

        # for i in range(self.no_of_links):
         
        #     f = Frame(self.frame,highlightbackground="black", highlightthickness=2)
            
        #     Label(f,text = "a_"+str(i+1)+" (cm)",width = 15).grid(row=0,column=0)
        #     Entry(f,width = 50,textvariable=self.a[i]).grid(row=0,column=1)
            
        #     Label(f,text = "alpha_"+str(i+1)+" (deg)",width = 15).grid(row=1,column=0)
        #     Entry(f,width = 50,textvariable=self.alpha[i]).grid(row=1,column=1)
            
        #     Label(f,text = "d_"+str(i+1)+" (cm)",width = 15).grid(row=2,column=0)
        #     if(self.selected[i].get()=="d"):
        #         Scale(f,length = 300,resolution=0.1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.d[i]).grid(row=2,column=1)     
        #     else:
        #         Entry(f,width = 50,textvariable=self.d[i]).grid(row=2,column=1)
                
        #     Label(f,text = "theta_"+str(i+1)+" (deg)",width = 15).grid(row=3,column=0)
        #     if(self.selected[i].get()=="theta"):
        #         Scale(f,length = 300,resolution=1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.theta[i]).grid(row=3,column=1)  
        #     else:
        #         Entry(f,width = 50,textvariable=self.theta[i]).grid(row=3,column=1)
        #     f.grid(row=i//3,column=i%3)
        
        # DH parameter setting
        label_width = 15
        text_width = 5
        scale_width = 300
        
        for i in range(self.no_of_links):
             
            f = Frame(self.frame)
            
            Label(f,text = "a_"+str(i+1)+" (cm)",width = label_width).grid(row=i,column=0)
            Entry(f,width = text_width,textvariable=self.a[i]).grid(row=i,column=1)
            
            Label(f,text = "alpha_"+str(i+1)+" (deg)",width = label_width).grid(row=i,column=2)
            Entry(f,width = text_width,textvariable=self.alpha[i]).grid(row=i,column=3)
            
            
            if(self.selected[i].get()=="d"):
                Label(f,text = "theta_"+str(i+1)+" (deg)",width = label_width).grid(row=i,column=4)
                Entry(f,width = text_width,textvariable=self.theta[i]).grid(row=i,column=5)
                Label(f,text = "d_"+str(i+1)+" (cm)",width = label_width).grid(row=i,column=6)
                Scale(f,length = scale_width,resolution=0.1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.d[i]).grid(row=i,column=7)  
                Spinbox(f,width=text_width,command=self.output_mat,from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),increment=0.1,textvariable = self.d[i]).grid(row=i,column=8)   
            elif(self.selected[i].get()=="theta"):
                Label(f,text = "d_"+str(i+1)+" (cm)",width = label_width).grid(row=i,column=4)
                Entry(f,width = text_width,textvariable=self.d[i]).grid(row=i,column=5)
                Label(f,text = "theta_"+str(i+1)+" (deg)",width = label_width).grid(row=i,column=6)
                Scale(f,length = scale_width,resolution=1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.theta[i]).grid(row=i,column=7)
                Spinbox(f,width=text_width,command=self.output_mat,from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),increment=1,textvariable = self.theta[i]).grid(row=i,column=8) 
            f.grid(row=i)
        
        # Display T matrix
        f = Frame(self.frame)
        Label(f,text="T_{}_to_{}".format(0,self.no_of_links),width = label_width,font='Helvetica 11 bold').grid(row=0)
        
        self.output_mat()
            
        for i in range(4):
            for j in range(4):            
                Label(f,textvariable = self.output_mat_disp[i][j],width = label_width).grid(row=i+2,column=j)   
                  
        f.grid(row=15)  
        
        # Inverse Kinematics
        f = Frame(self.frame)
        
        Label(f,text="Inverse Kinematics",width = 20,font='Helvetica 12 bold').grid(row=0)
        
        Label(f,text = "X coordinate",width = label_width).grid(row=1,column=0)
        Scale(f,length = scale_width*2,resolution=0.1,command=self.inverse_kinematics, from_=-self.pos_limit, to=self.pos_limit, orient='horizontal',variable=self.pos[0]).grid(row=1,column=1)  
        Spinbox(f,width=text_width,command=self.inverse_kinematics,from_=-self.pos_limit, to=self.pos_limit,increment=0.1,textvariable = self.pos[0]).grid(row=1,column=2) 
        
        Label(f,text = "Y coordinate",width = label_width).grid(row=2,column=0)
        Scale(f,length = scale_width*2,resolution=0.1,command=self.inverse_kinematics, from_=-self.pos_limit, to=self.pos_limit, orient='horizontal',variable=self.pos[1]).grid(row=2,column=1)
        Spinbox(f,width=text_width,command=self.inverse_kinematics,from_=-self.pos_limit, to=self.pos_limit,increment=0.1,textvariable = self.pos[1]).grid(row=2,column=2)   
        
        Label(f,text = "Z coordinate",width = label_width).grid(row=3,column=0)
        Scale(f,length = scale_width*2,resolution=0.1,command=self.inverse_kinematics, from_=0, to=self.pos_limit, orient='horizontal',variable=self.pos[2]).grid(row=3,column=1)  
        Spinbox(f,width=text_width,command=self.inverse_kinematics,from_=-self.pos_limit, to=self.pos_limit,increment=0.1,textvariable = self.pos[2]).grid(row=3,column=2) 
        
        Label(f,text = "EF Orientation",width = label_width).grid(row=4,column=0)
        Scale(f,length = scale_width*2,resolution=1,command=self.inverse_kinematics, from_= -90, to=90, orient='horizontal',variable=self.EF_ori).grid(row=4,column=1)  
        Spinbox(f,width=text_width,command=self.inverse_kinematics,from_=-90, to=90,increment=1,textvariable = self.EF_ori).grid(row=4,column=2) 
        
        self.ll=Label(f,textvariable=self.solution,width = label_width)
        self.ll.grid(row=5,column=1)
        
        f.grid(row=20)
               
        Button(self.frame, text='exit',bg='red',command=self.exit_cmd).grid(row=25,column=8) 
        Button(self.frame, text='Send to arm',bg='green',command=self.send_to_arm).grid(row=24,column=8) 
        # Button(self.frame, text='cal',bg='green',command=self.output_mat).grid(row=self.no_of_links+3) 
        self.frame.pack()
        
    def map_angle_range(self,val,in_min,in_max,out_min,out_max):
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
        
    def send_to_arm(self):
        data_array = [self.theta[i].get() for i in range(4)]
    
        data_array[2] = self.map_angle_range(data_array[2],-180,0,0,180)
        data_array[3] = self.map_angle_range(data_array[3],-90,90,0,180)
        
        data_string = ','.join(str(value) for value in data_array)
        data_string+=","
        # Send the data over the serial port
        self.arduino.write(data_string.encode())
        x = self.arduino.readline().decode()
        print(x)
        return [self.theta[i].get() for i in range(4)]
     
    def output_mat(self,event=0):
        T = np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]])
        for i in range(self.no_of_links):
            l = self.links[i]
            l.set_a(self.a[i].get())
            l.set_alpha(math.radians(self.alpha[i].get()))
            l.set_d(self.d[i].get())
            l.set_theta(math.radians(self.theta[i].get()))
            l.calcDH()
            T = T @ l.get_dh()
        
        T[abs(T)<10**-4] = 0.0
        T = np.round(T,4)
        for i in range(4):
            for j in range(4):
                x = str(T[i][j])
                self.output_mat_disp[i][j].set(x)
                
        self.pos[0].set(T[0][3])
        self.pos[1].set(T[1][3])
        self.pos[2].set(T[2][3])
        self.EF_ori.set(self.theta[1].get()+self.theta[2].get()+self.theta[3].get())
    
    def inverse_kinematics(self,event=0):
        joint_angles_default = [0,90,-90,-90]
        
        self.joint_angles=[]
        angles = []
        
        min_range = [0,0,-135,-90]
        max_range = [180,180,0,90]
        
        EF_orientation = self.EF_ori.get()
        pos = self.pos
        
        x,y,z = pos[0].get(),pos[1].get(),pos[2].get()
        
        # calculating theta 1
        theta_1 = [math.degrees(math.atan2(y,x)), math.degrees(math.atan2(y,x)) - 180]
        
        
        for t1 in theta_1:
            angle_subset1 = []
            angle_subset2 = []
            angle_subset1.append(round(t1))
            angle_subset2.append(round(t1))
            
            # calculating theta 3 and thata 2
            if y!=0:
                A = y/(12*math.sin(math.radians(t1))) - 0.108333 - 0.916667*math.cos(math.radians(EF_orientation))
            elif x!=0:
                A = x/(12*math.cos(math.radians(t1))) - 0.108333 - 0.916667*math.cos(math.radians(EF_orientation))
            else:
                break
            B = (z - 9.5 - 11*math.sin(math.radians(EF_orientation)))/12
            l = (A**2 + B**2 - 2)/(2)
            if(l**2<1):
                
                theta_3 = [math.degrees(math.atan2((1-l**2)**0.5, l)), math.degrees(math.atan2(-(1-l**2)**0.5, l))]
                    
                theta_2 = [0,0]
                
                theta_2[0] = math.degrees(math.atan2((-A*((1-l**2)**0.5) + B*(1+l)), (A*(1+l) + B*((1-l**2)**0.5))))
                theta_2[1] = math.degrees(math.atan2((B*(1+l) + A*((1-l**2)**0.5)),(-B*((1-l**2)**0.5) + A*(1+l))))
                
                theta_4 = [EF_orientation - theta_2[0] - theta_3[0], EF_orientation - theta_2[1] - theta_3[1]]
                
                angle_subset1.append(round(theta_2[0]))
                angle_subset2.append(round(theta_2[1]))
                angle_subset1.append(round(theta_3[0]))
                angle_subset2.append(round(theta_3[1]))
                angle_subset1.append(round(theta_4[0]))
                angle_subset2.append(round(theta_4[1]))
                
                angles.append(angle_subset1)
                angles.append(angle_subset2)
        # print(angles)
        for m in angles:
            for i in range(len(m)):
                a = m[i]
                if not((min_range[i]<=a<=max_range[i])):
                                     
                    break
            else:
                self.joint_angles.append(m)
                
        # print(self.joint_angles)       
        
                
        if len(self.joint_angles)>0: 
            self.solution.set("Solution Exists")       
            self.ll.config(bg="green")
            for i in range(4):
                self.theta[i].set(self.joint_angles[0][i])
        else:
            for i in range(4):
                self.theta[i].set(joint_angles_default[i])
            self.solution.set("No Solution !!! ") 
            self.ll.config(bg="red")
            
    
              
    def exit_cmd(self):
        self.root.destroy()

def main(): 
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
        root = Tk()
        root.overrideredirect(1)
        app = input_links(root)
    finally:
        root.mainloop()

if __name__ == '__main__':
    main()