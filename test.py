import numpy as np
y = 1
z = 0
x = 1
pitch = np.arctan2(y, z) * 180/np.pi
roll = np.arctan2(x, z) * 180/np.pi
print(pitch, roll)
