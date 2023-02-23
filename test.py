# import numpy as np

import math

rho = 1
phi = math.radians(90)

x = rho * math.cos(phi)
y = rho * math.sin(phi)

# x = 0
# y = 1
# 
# rho = math.sqrt(x**2 + y**2)
# phi = math.atan2(y, x)

print(f"x= {x} y= {y}")
print(f"rho= {rho} phi= {math.degrees(phi)}")