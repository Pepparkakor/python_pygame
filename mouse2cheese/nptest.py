import numpy as np

room = np.array([0,0,0])
a = np.array([0,0,0])
b = np.array([0,0,0])
c = np.dstack((room, a))
c = np.dstack((c, b))
print(c)

