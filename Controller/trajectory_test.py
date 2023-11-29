target = -60
T = 3

t = 0

while(t<T):
    q = target*((t/T)**2)*(3-2*t/T)
    print(int(q))
    t+=0.01