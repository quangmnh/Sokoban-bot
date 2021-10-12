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

# import numpy as np
# a = np.array([[1,2],[3,4]])
# b = np.array([1,3])
# print((a==b).all(-1).any())
# print(a)
# print(b)


# import numpy as np
# a = np.array([1,2,3,4])
# a = [['r', 'r', 'u', 'r', 'r', 'u', 'u', 'l', 'l', 'l', 'd', 'l', 'l', 'u', 'u', 'rp', 'l', 'd', 'd', 'r', 'r', 'r', 'd', 'r', 'r', 'u', 'u', 'l', 'u', 'u', 'l', 'l', 'dp', 'l', 'l', 'd', 'd', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'up', 'd', 'r', 'r', 'u', 'r', 'r', 'u', 'u', 'l', 'l', 'd', 'l', 'up', 'r', 'r', 'u', 'u', 'l', 'l', 'dp', 'l', 'l', 'd', 'd', 'rp', 'rp', 'up', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'up', 'd', 'r', 'r', 'u', 'u', 'l', 'u', 'u', 'l', 'l', 'dp', 'dp', 'rp', 'd', 'd', 'd', 'l', 'l', 'u', 'u', 'rp', 'u', 'r', 'dp']]
# count = 1
# for i in a.moves[-1]:
#     print("move {}: {}".format(count,i))
#     count+=1







from queue import PriorityQueue, Queue

a = PriorityQueue()

a.put((2.5, 'assdasdsa', 6))
a.put((3.4, 'fsgsdfsdf', 1))
a.put((1.0, 'FASFDSFSF', 5))
a.put((2.3, 'adfasdfs', 2))
a.put((5.2, 'sfsdgs', 7))
a.put((4.4, 'sdfsadfg', 9))

while (a.qsize()>0):
    print(a.get()[0])





# import numpy as np

# a = np.array([[1,2],[3,4],[5,6]])
# b = np.array([[6,2],[1,3],[2,4]])

# def manhattan(a,b):
#     print(np.sum(abs(a-b)))
# manhattan(a,b)