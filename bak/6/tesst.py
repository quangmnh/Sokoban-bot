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
# b = np.array([1,2])
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







# from queue import PriorityQueue, Queue

# a = PriorityQueue()

# a.put((2.5, 'assdasdsa', 6))
# a.put((3.4, 'fsgsdfsdf', 1))
# a.put((1.0, 'FASFDSFSF', 5))
# a.put((2.3, 'adfasdfs', 2))
# a.put((5.2, 'sfsdgs', 7))
# a.put((4.4, 'sdfsadfg', 9))

# b = PriorityQueue()

# b.put((2.5, 'a2.5'))
# b.put((3.4, 'a3.4'))
# b.put((1.0, 'a1.0'))
# b.put((2.3, 'a2.3'))
# b.put((5.2, 'a5.2'))
# b.put((4.4, 'a4.4'))

# while (a.qsize()>0):
#     print(a.get()[0])
#     print(b.get()[0])




# import numpy as np

# a = np.array([[1,2],[3,4],[5,6]])
# b = np.array([[6,2],[1,3],[2,4]])

# def manhattan(a,b):
#     print(np.sum(abs(a-b)))
# manhattan(a,b)





# import numpy as np

# a = np.array([1,2,3,4])
# b = np.array([3,5,9,2])

# s = tuple()
# s = s + (a,)  
# s = s + (b,)
# print(s)
# print(type(s))
# print(type(s[0]))



# from collections import deque
# import numpy as np
# queue = deque()
# queue.append(np.array([1,2,3,4]))
# a = queue.popleft()
# print(a)
# print(queue)
# print(type(a))
# print(type(queue))



# import numpy as np

# a = np.array([1,2])
# b = (2,1)
# c = a+b
# a[0]  = 4
# print(c)
# print(type(c))
# print(a)




# import numpy as np

# a = np.array([[1,2,3,4],[5,3,6,7],[6,3,3,7]])
# b = np.array([1,2])

# print(a[b[0],b[1]])






# import numpy as np

# a = np.array([1,2])
# b = np.array([1,2,3,4])
# c = np.concatenate([a,b])
# a[0] = 1000
# print(a)
# print(c)
# print(type(c))


# import numpy as np
# arr = np.array([[1,2,3],[4,5,6]])
# row = np.array([7,8,9])
# arr = np.append(arr,[row],axis= 0)
# print(arr)



# import numpy as np

# a = np.array([1,2])
# b = np.array([0,4,1,2,4,8])
# print(b.reshape(-1,2))
# print(b)
# print((a==b.reshape(-1,2)).all(-1).any())
# print(b)


# import numpy as np

# b = np.array([0,4,1,2,4,8])
# a = b[2:]
# b[4] = 10000
# print(a)
# print(b)




# import numpy as np

# a = np.array([1,2])
# b = np.array([0,4,1,2,4,8])

# c = np.copy(b.reshape(-1,2))
# for i in c:
#     if (i==a).all():
#         i = np.array([4,10])
# print(b)
# print(c)



# import numpy as np
# a = np.array([1,2,3,4,5,6])
# b = np.array([3,2,1,2,5,6])
# print((a.reshape(-1,2)[:,None] == b.reshape(-1,2)).all(-1).any(-1).all())


# a= [1,2,4,5]
# b = 1
# c = a+[b]
# a[2]= 1000
# print(a)
# print(b)
# print(c)


# import numpy as np
# arr = np.array([[1,2,3],[4,5,6]])
# row = np.array([7,8,9])
# arr = np.append(arr,[row],axis= 0)
# print(arr)
# a = arr.reshape(1,-1)
# print(a)

# import numpy as np

# a = np.array([1,2,3,4,5,6])
# b = np.array([1,2])
# c = np.concatenate([a,b])



# import numpy as np
# a =np.array([1,2,3,4])
# b = np.array([a])
# c =np.append(b,[np.array([10,12,13,14])],axis=0)
# print(a)
# print(b)
# print(c)


# from collections import deque
# moves = deque()
# moves.append(["s"])

# a= moves.popleft()
# print(a)
# print(moves)



# import numpy as np
# new_crates = np.array([1,2,3,4,5,6])
# dest = np.array([[1,3],[5,6],[3,4]])
# print((new_crates.reshape(-1,2)[:,None] == dest).all(-1).any(-1).all())


# from collections import deque

# a= deque()
# a.append([1])
# a.append([2])
# a.append([3])
# a.append([4])
# a.append([5])
# while (a):
#     print(a.popleft())


# import numpy as np
# a = np.array([1,2])
# b = np.array([[4,5],[3,9],[1,2],[2,8]])
# c = np.array([100,100])
# print("false is 0, true is 1")
# print((a==b).all(-1))
# print(np.nonzero((a==b).all(-1)))
# b[np.nonzero((a==b).all(-1))[0][0]] = c
# print(a)
# print(b)
# print(c)

# import array
# arr1 = array.array('b', ['a', 'b', 'c'])
# arr1.append('d')
# print(arr1)


# import numpy as np
# a = np.array([1,2])
# b = np.array([[4,5],[3,9],[1,2],[2,8]])
# print(b.flatten())

# import numpy as np
# a = np.array([1,2,3,4])
# b =np.array([5,6,7,8])

# c= set()
# c.add(a)
# c.add(b)
# print(c)


# a = [1,2,3]
# b=[10]

# c = a + b
# a[0] = 54

# print(a)
# print(b)
# print(c)



# print((1,2)+(2,3))




# import numpy as np

# a = np.array([0,0,0,1])
# b = np.array([[1,0,1,0],[0,1,0,0],[1,1,1,0],[1,1,1,1]])
# # print((np.logical_or(np.logical_not(np.logical_xor(a,b)),a)))
# print((np.logical_and(b,a)==b).all(-1).any())




# import numpy as np

# a = np.array([1,1,2,0])
# b = np.array([[1,0,3,0],[0,1,1,0],[1,1,1,0],[1,1,1,1]])
# c = np.array([[1,0,1,0],[0,1,1,0],[1,1,1,0],[1,1,1,1]])
# # print((np.logical_or(np.logical_not(np.logical_xor(a,b)),a)))
# print(a==b)
# print((np.logical_and(a==b,c)==c).all(-1).any())




# import tracemalloc
# from time import sleep

# def f():
#     # a function that with growing
#     # memory consumption
#     a = 0
#     for i in range(1000):
#         a+=i
#     return a
# tracemalloc.start()
# f()
# print('Max memory usage:{}'.format(tracemalloc.get_traced_memory()[1]))

# a= ['s']

# for i in 'rrruulDrdLLuLDlddrrUdlluurDuurrdLulDllluurDRlldRR':
#     a.append(i)
# print(a)



import numpy as np

a = np.array([1,2,3,4])
b = np.array([[3,4],[2,1]])
print(a.reshape(-1,2)-b)


