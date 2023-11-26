from link import *

no_of_links = 3
links = [None]

a_array = [None, 0.3, 0.35, 0]
alpha_array = [None, 0, np.pi, 0]
d_array = [None, 0.4, 0, 0.2]
theta_array = [None, np.pi/6, np.pi/4, 0]

for i in range(1,no_of_links+1):
    links.append(link(i,a_array[i],alpha_array[i],d_array[i],theta_array[i]))
    if links[i].get_d() != None and links[i].get_theta() != None:
        links[i].calcDH()
        links[i].viewDH()

T_0_to_3 = np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [0,0,0,1]])

for i in range(1, no_of_links+1):
    T_0_to_3 = T_0_to_3 @ links[i].get_dh()
T_0_to_3[T_0_to_3 < 10**-3] = 0  

print("Final T matrix:")
print(T_0_to_3)
