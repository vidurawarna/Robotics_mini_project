from tkinter import *
from link import *
from tkinter.messagebox import showinfo

class input_links:
    global no_of_links
    def __init__(self, master):
        self.root = master
        self.root.withdraw()
        self.master = Toplevel(master)
        self.master.geometry("400x100")
        self.master.title("Forward Kinematics")
        self.frame = Frame(self.master)
        self.label = Label(self.frame,text = "Enter number of Links").grid(row=0,column=0)
        self.links = IntVar()
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
        self.master.title("Forward Kinematics")

        self.selected = []
        self.min_vals = []
        self.max_vals = []
        
        for i in range(1,self.no_of_links+1):
            self.selected.append(StringVar())
            self.min_vals.append(StringVar())
            self.max_vals.append(StringVar())
            
        self.frame = Frame(self.master)
        
        for i in range(1,self.no_of_links+1):
            
            Label(self.frame,text = "select the variable for link "+str(i)).grid(row=i-1,column=0)
            
            Label(self.frame,text = "       ").grid(row=i-1,column=1)
            
            self.selected[i-1].set('theta')
            Radiobutton(self.frame, text='d(cm)', value='d', variable=self.selected[i-1]).grid(row=i-1,column=2) 
            Radiobutton(self.frame, text='theta(deg)', value='theta', variable=self.selected[i-1]).grid(row=i-1,column=3)   
            
            Label(self.frame,text = "       ").grid(row=i-1,column=4)
               
            Label(self.frame,text = "Min ").grid(row=i-1,column=5)
            self.min_vals[i-1].set('0')
            Entry(self.frame,width = 10,textvariable=self.min_vals[i-1]).grid(row=i-1,column=6)
            
            Label(self.frame,text = "Max ").grid(row=i-1,column=7)
            self.max_vals[i-1].set('180')
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
        
        self.output_mat_disp = [[StringVar() for m in range (4)] for n in range(4)]
              
        for i in range(self.no_of_links):
            self.a.append(DoubleVar())
            self.alpha.append(DoubleVar())
            self.d.append(DoubleVar())
            self.theta.append(DoubleVar())
            
        for i in range(self.no_of_links):
            self.links.append(link(i+1,self.a[i].get(),math.radians(self.alpha[i].get()),self.d[i].get(),math.radians(self.theta[i].get())))
        
        self.master = Toplevel(self.root)
        self.master.geometry("1700x450")
        self.master.title("Forward Kinematics")
            
        self.frame = Frame(self.master)
        
        for i in range(self.no_of_links):
         
            f = Frame(self.frame,highlightbackground="black", highlightthickness=2)
            
            Label(f,text = "a_"+str(i+1)+" (cm)",width = 15).grid(row=0,column=0)
            Entry(f,width = 50,textvariable=self.a[i]).grid(row=0,column=1)
            
            Label(f,text = "alpha_"+str(i+1)+" (deg)",width = 15).grid(row=1,column=0)
            Entry(f,width = 50,textvariable=self.alpha[i]).grid(row=1,column=1)
            
            Label(f,text = "d_"+str(i+1)+" (cm)",width = 15).grid(row=2,column=0)
            if(self.selected[i].get()=="d"):
                Scale(f,length = 300,resolution=0.1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.d[i]).grid(row=2,column=1)     
            else:
                Entry(f,width = 50,textvariable=self.d[i]).grid(row=2,column=1)
                
            Label(f,text = "theta_"+str(i+1)+" (deg)",width = 15).grid(row=3,column=0)
            if(self.selected[i].get()=="theta"):
                Scale(f,length = 300,resolution=1,command=self.output_mat, from_=float(self.min_vals[i].get()), to=float(self.max_vals[i].get()),orient='horizontal',variable=self.theta[i]).grid(row=3,column=1)  
            else:
                Entry(f,width = 50,textvariable=self.theta[i]).grid(row=3,column=1)
            f.grid(row=i//3,column=i%3)
        
        
        
        f = Frame(self.frame)
        Label(f,text="T_{}_to_{}".format(0,self.no_of_links),width = 20,font='Helvetica 14 bold').grid(row=0)
        
        for i in range(4):
            for j in range(4):            
                Label(f,textvariable = self.output_mat_disp[i][j],width = 10).grid(row=i+2,column=j)   
                
       
        f.grid(row=15)  
               
        Button(self.frame, text='exit',bg='red',command=self.exit_cmd).grid(row=20,column=20) 
        # Button(self.frame, text='cal',bg='green',command=self.output_mat).grid(row=self.no_of_links+3) 
        self.frame.pack()
        
    
     
    def output_mat(self,event):
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