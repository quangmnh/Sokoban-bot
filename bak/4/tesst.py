# import numpy as np
# a = np.array([[1,2],[2,3],[4,3]])
# b= np.array([[2,3],[4,3],[1,2]])
# res = (a[:, None] == b).all(-1).any(-1).all(-1)
# print(res)
# for i in range(a.shape[0]):
#     print(a[i])


# a =[1,2,3]
# b = 1
# c =[a,b]
# print(c)
# print(type(c))
# print(a.append(b))

# di = {
#     (1,2) : 123,
#     (3,4) : 124
# }

# print(di[(1,2)])

# def update(move:list, new):
#     move.append(new)
#     return move

# move =[1,2,3,4]
# print(update(move,5))
# print(move)




# import numpy as np
# a = np.array([[1,2],[3,4]])
# for i in range(a.shape[0]):
#     if (a[i]==np.array([1,2])).all():
#         a[i] = np.array([5,6])
# print(a)

import numpy as np
a = np.array([[1,2],[3,4]])
b = np.array([1,3])
print((a==b).all(-1).any())
print(a)
print(b)