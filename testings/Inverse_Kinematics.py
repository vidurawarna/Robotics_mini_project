import math

def get_angles(pos,EF_ori):
    joint_angles_default = [0,90,90,-45]
    joint_angles = []
    
    angles = []
    
    min_range = [0,0,45,90]
    max_range = [360,180,315,270]
    
    EF_orientation = EF_ori
    
    x,y,z = pos[0],pos[1],pos[2]
    
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
        # A = y/(12*math.sin(math.radians(t1))) - 0.108333 - 0.916667*math.cos(math.radians(EF_orientation))
        B = (z - 9.5 - 11*math.sin(math.radians(EF_orientation)))/12
        l = (A**2 + B**2 - 2)/(-2)
        if(l**2<1):
            
            theta_3 = [math.degrees(math.atan2((1-l**2)**0.5, l)), math.degrees(math.atan2(-(1-l**2)**0.5, l))]
                
            theta_2 = [0,0]
            
            theta_2[0] = math.degrees(math.atan2((A*((1-l**2)**0.5) + B*(1-l)), (A*(1-l) - B*((1-l**2)**0.5))))
            theta_2[1] = math.degrees(math.atan2((B*(1-l) - A*((1-l**2)**0.5)),(B*((1-l**2)**0.5) + A*(1-l))))
            
            theta_4 = [EF_orientation - theta_2[0] - theta_3[0], EF_orientation - theta_2[1] - theta_3[1]]
            
            angle_subset1.append(round(theta_2[0]))
            angle_subset2.append(round(theta_2[1]))
            angle_subset1.append(round(theta_3[0]))
            angle_subset2.append(round(theta_3[1]))
            angle_subset1.append(round(theta_4[0]))
            angle_subset2.append(round(theta_4[1]))
            
            angles.append(angle_subset1)
            angles.append(angle_subset2)

    # for m in angles:
    #     for i in range(len(m)):
    #         a = m[i]
    #         if not((min_range[i]<=a<=max_range[i])):
    #             break
    #             # if not(min_range[i]<=(a+360)<=max_range[i]) and (i==2 or i==3):                  
    #             #     print(a)
    #             #     break
    #     else:
    #         joint_angles.append(m)
            
    joint_angles.append(angles)
    # for j in joint_angles:
    #     if j[3]<0:
    #         j[3] = j[3]+360   
            
    print(joint_angles)
         
    return 1
get_angles([21.3,0,14],-43)