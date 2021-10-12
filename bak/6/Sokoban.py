#! usr/bin/python
from datetime import datetime
import os
import csv
from copy import deepcopy
import numpy as np
import time
from collections import deque
from numpy.ma.core import concatenate, left_shift
from queue import PriorityQueue
import tracemalloc
from tqdm import tqdm

# class PriorityQueue:
#     def __init__(self):
#         self.heap = []
#         self.qsize = 0
#     def put(self, priority, item):
#         heapq.heappush(self.heap, (priority, item))
#         self.qsize+=1
#     def get(self):
#         (_, item) = heapq.heappop(self.heap)
#         self.qsize-=1
#         return item
class Sokoban:
    def __init__(self) -> None:
        pass
    
    def import_input(self, link:str):
        with open(link,newline='') as csvfile:
            board = csv.reader(csvfile)
            self.board = np.array(list(board))
            self.org_board = deepcopy(self.board).tolist()
            # self.org_board = list(board)
            # print(self.board)
            
            self.get_main()
            self.get_crates()
            self.get_dest()
            # self.get_outmost_wall()

            self.y = self.board.shape[0]
            self.x = self.board.shape[1]

            self.directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            # self.directions2 = ((-1, 0), (1, 0), (0, -1), (0, 1))
            self.eight_directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1))
            # self.four_directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            # self.four_corners = ((1, 1), (-1, -1), (-1, 1), (1, -1))

            self.move_dir = {
                (0,1) : "r",
                (0,-1) : "l",
                (1,0) : "d",
                (-1,0) : "u"    
            }
            # self.stuck_direction = ((0,2,3,0),(2,1,1,3),(1,3,2,1),(3,0,0,2))
            # self.stuck_pattern = np.array([[0,0,0,1,0,1,1,0],
            #                                [1,0,0,0,1,0,1,0],
            #                                [0,0,1,0,1,0,0,1],
            #                                [0,1,0,0,0,1,0,1],
            #                                [1,0,0,1,0,0,0,0],
            #                                [1,0,1,0,0,0,0,0],
            #                                [0,1,1,0,0,0,0,0],
            #                                [0,1,0,1,0,0,0,0]])
            self.stuck_pattern = np.array((
                                           (1,0,0,1,0,0,0,0),
                                           (1,0,1,0,0,0,0,0),
                                           (0,1,1,0,0,0,0,0),
                                           (0,1,0,1,0,0,0,0),
                                           (2,0,0,2,0,0,1,0),
                                           (2,0,2,0,1,0,0,0),
                                           (0,2,2,0,0,0,0,1),
                                           (0,2,0,2,0,1,0,0),
                                           (1,0,0,1,0,0,1,0),
                                           (1,0,1,0,1,0,0,0),
                                           (0,1,1,0,0,0,0,1),
                                           (0,1,0,1,0,1,0,0),
                                           (2,0,0,2,0,0,2,0),
                                           (2,0,2,0,2,0,0,0),
                                           (0,2,2,0,0,0,0,2),
                                           (0,2,0,2,0,2,0,0),
                                           
                                           (0,1,0,2,0,1,0,0),
                                           (0,2,0,1,0,1,0,0),
                                           (0,1,2,0,0,0,0,1),
                                           (0,2,1,0,0,0,0,1),
                                           (1,0,2,0,1,0,0,0),
                                           (2,0,1,0,1,0,0,0),
                                           (1,0,0,2,0,0,1,0),
                                           (2,0,0,1,0,0,1,0),
                                           (1,0,2,0,0,0,0,1),
                                           (0,2,1,0,0,1,0,0),
                                           (0,1,0,2,0,0,1,0),
                                           (2,0,0,1,1,0,0,0)
                                        ))
     
            self.pattern_keyid = deepcopy(self.stuck_pattern)
            self.pattern_keyid[self.pattern_keyid>1]=1
            self.stuck_direction = ((0,2),(2,1),(1,3),(3,0))
            self.push_dir = {
                (0,1) : "R",
                (0,-1) : "L",
                (1,0) : "D",
                (-1,0) : "U"    
            }
            self.moves = []
            self.stuckTime = 0
    def get_main(self):
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="m":
                    self.main = np.array([i,j])
                    self.board[i][j] = "s"
                elif self.board[i][j] == "md":
                    self.main = np.array([i,j])
                    self.board[i][j] = "d"
        return self.main
    
    def get_dest(self):
        a = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="d":
                    a.append([i,j])
                    self.board[i][j] = "s"
        self.dest = np.array(a)
        self.destcon = deepcopy(self.dest).ravel()
        return self.dest   

    def get_crates(self):
        a = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="c":
                    a.append([i,j])
                    self.board[i][j] = "s"
                elif self.board[i][j] =="cd":
                    a.append([i,j])
                    self.board[i][j] = "d"
        self.crates = np.array(a)
        return self.crates
 

    def isStuck(self, crate:np.ndarray, crates:np.ndarray):
        start = time.time()
        if (crate==self.dest).all(-1).any():
            return False
        state_pattern = np.zeros(8)
        for i in range(8):
            pos = crate + self.eight_directions[i]
            if self.board[pos[0],pos[1]]=="w":
                state_pattern[i] = 1
            elif (pos==crates).all(-1).any():
                state_pattern[i] = 2
        res = (np.logical_and(state_pattern==self.stuck_pattern,self.pattern_keyid)==self.pattern_keyid).all(-1).any()
        self.stuckTime+=time.time()-start
        return res
        

    def generate_state_bfs_main(self, initial_state:np.ndarray):
        """
        :param game_state: [main0,main1,crate10,crate11,crate20,crate21,....]
        :return bool: 
        """
        
        queue = deque()
        queue.append((initial_state,["s"])) 
        visited = {tuple(initial_state)}
        while (queue):
            if (time.time()-self.start>1500):
                self.time = 1500
                return "timeout"
            temp = queue.popleft()
            game_state = temp[0]
            move = temp[1]
            main = game_state[0:2]
            crates = game_state[2:]
            for direction in self.directions:
                #new_main is the new cords of the main.
                new_main = main + direction
                reshaped_crate = crates.reshape(-1,2)
                if (new_main == reshaped_crate).all(-1).any():
                    new_crate = new_main + direction
                    if self.board[new_crate[0], new_crate[1]] == "s" and not (new_crate == reshaped_crate).all(-1).any():
                        new_crates = np.copy(reshaped_crate)
                        new_crates[np.nonzero((new_main==new_crates).all(-1)==True)[0][0]] = new_crate
                        new_state = np.concatenate((new_main, new_crates.ravel()))
                        new_move = move + [self.push_dir[direction]]
                        if (new_crates[:,None] == self.dest).all(-1).any(-1).all():
                            self.moves.append(new_move)
                            self.time = time.time() - self.start
                            return "result gotten"
                        else:
                            temp_state = tuple(new_state)
                            if  temp_state not in visited and not self.isStuck(new_crate,new_crates):
                                visited.add(temp_state)
                                queue.append((new_state,new_move))
                elif self.board[new_main[0], new_main[1]] == "s":
                    new_state = np.concatenate((new_main, crates))
                    new_move = move + [self.move_dir[direction]]
                    temp_state = tuple(new_state)
                    if temp_state not in visited:
                        visited.add(temp_state)
                        queue.append((new_state,new_move))
        return "no result"

    def fn(self,move,game_state):
        gn = len([m for m in move if m.isupper()])
        hn = np.sum(abs(game_state[2:]-self.destcon))
        return (gn + hn)
    

    def generate_state_astar_main(self, initial_state:np.ndarray):
        """
        :param game_state: [main0,main1,crate10,crate11,crate20,crate21,....]
        :return bool: 
        """
        
        queue = PriorityQueue()
        queue.put((self.fn(["s"],initial_state),initial_state.tolist(),["s"]))
        visited = {tuple(initial_state)}
        while (queue.qsize()>0):
            if (time.time()-self.start>1500):
                self.time = 1500
                return "timeout"
            temp =queue.get()
            game_state = np.array(temp[1])
            move = temp[2]
            
            main = game_state[0:2]
            crates = game_state[2:]
            for direction in self.directions:
                #new_main is the new cords of the main.
                new_main = main + direction
                reshaped_crate = crates.reshape(-1,2)
                if (new_main == reshaped_crate).all(-1).any():
                    new_crate = new_main + direction
                    if self.board[new_crate[0], new_crate[1]] == "s" and not (new_crate == reshaped_crate).all(-1).any():
                        new_crates = np.copy(reshaped_crate)
                        new_crates[np.nonzero((new_main==new_crates).all(-1)==True)[0][0]] = new_crate
                        new_state = np.concatenate((new_main, new_crates.ravel()))
                        new_move = move + [self.push_dir[direction]]
                        if (new_crates[:,None] == self.dest).all(-1).any(-1).all():
                            self.moves.append(new_move)
                            self.time = time.time()-self.start
                            return "result gotten"
                        else:
                            temp_state = tuple(new_state)
                            if not (temp_state in visited ) and not self.isStuck(new_crate,new_crates):
                                visited.add(temp_state)
                                queue.put((self.fn(new_move,new_state),new_state.tolist(),new_move))

                elif self.board[new_main[0], new_main[1]] == "s":
                    new_state = np.concatenate((new_main, crates))
                    new_move = move + [self.move_dir[direction]]
                    temp_state = tuple(new_state)
                    if not (temp_state in visited):
                        visited.add(temp_state)
                        queue.put((self.fn(new_move,new_state),new_state.tolist(),new_move))
        return "no result"
    def blind_search(self):
        init_state = np.concatenate((self.main,self.crates.reshape(1,-1)[0]))
        self.start = time.time()
        tracemalloc.start()
        search = self.generate_state_bfs_main(init_state)
        self.mem = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        tracemalloc.stop()
        # print(self.mem)
        return search

    def astar_search(self):
        init_state = np.concatenate((self.main,self.crates.reshape(1,-1)[0]))
        self.start = time.time()
        tracemalloc.start()
        search = self.generate_state_astar_main(init_state)
        self.mem = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        tracemalloc.stop()
        return search

    def run_all_mini(self):
        for type in ['bfs', 'astar']:
            res_name = 'result/minicosmos_'+type+'.txt'
            with open(res_name,"w+") as file:
                print('Searching mini cosmos levels with '+type)
                for i in tqdm(range(1,40)):
                    file_name = 'levels/minicosmos' + str(i) + '.csv'
                    self.import_input(file_name)
                    if type == 'bfs':
                        search = self.blind_search()
                    else:
                        search = self.astar_search()
                    # print(search)
                    result =''
                    if search == "timeout":
                        result = 'Mini cosmos {} :  Time out errorr\n\n'.format(i)
                    elif search == "result gotten":
                        moves = ''
                        for move in self.moves[-1]:
                            if move!="s":
                                moves += move
                        result = 'Mini cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\n\n'.format(i,moves,self.time,self.mem[1])
                    elif search == "no result":
                        result = 'Mini cosmos {} :  No result found\n\n'.format(i)
                    file.write(result)
                    # print(result)
    def run_one(self, method, level_set, level):
        file_name = 'levels/{}cosmos{}.csv'.format(level_set,level)
        self.import_input(file_name)
        # print(self.org_board)
        # print(self.crates)
        if method == 'bfs':
            search = self.blind_search()
        else:
            search = self.astar_search()
        # print(search)
        result =''
        if search == "timeout":
            result = '{} {} cosmos {} :  Time out errorr\n\n'.format(method,level_set,level)
        elif search == "result gotten":
            moves = ''
            for i in self.moves[-1]:
                if i!="s":
                    moves += i
            result = '{} {} cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\n\n'.format(method,level_set,level,moves,self.time,self.mem[1])
        elif search == "no result":
            result = '{} {} cosmos {} :  No result found\n\n'.format(method,level_set,level)
        print(result)

a = Sokoban()
# a.run_all_mini()

a.run_one('astar', 'micro', 1)
print(a.stuckTime)


                    



