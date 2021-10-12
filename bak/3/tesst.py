import numpy as np
a = np.array([[1,2],[2,3],[4,3]])
b= np.array([[2,3],[4,3],[1,2]])
res = (a[:, None] == b).all(-1).any(-1).all(-1)
print(res)
for i in range(a.shape[0]):
    print(a[i])