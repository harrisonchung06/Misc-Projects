import math

N = 1000000
a=0
b=1
WIDTH = (b-a)/N
area = 0.0
for i in range(N):
    area += WIDTH * math.sqrt(1-pow(a+WIDTH*i, 2))
pi=4*area
print(pi)