import csv
from copy import deepcopy
import sys
from typing import Tuple
import numpy as np
import time
import random
from queue import PriorityQueue, Queue
class Sokoban:
    def __init__(self) -> None:
        pass
    
    def import_input(self, link:str):
        with open(link,newline='') as csvfile:
            board = csv.reader(csvfile)
            self.board = np.array(list(board))
            # print(self.board)
            self.get_dest()
            self.get_main()
            self.get_crates()
            self.y = self.board.shape[0]
            self.x = self.board.shape[1]
            self.directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            self.move_dir = {
                (0,1) : "r",
                (0,-1) : "l",
                (1,0) : "d",
                (-1,0) : "u"    
            }
            self.stuck_direction = ((0,2),(2,1),(1,3),(3,0))
            self.push_dir = {
                (0,1) : "rp",
                (0,-1) : "lp",
                (1,0) : "dp",
                (-1,0) : "up"    
            }
            self.isFound = False
            self.moves = []
            self.visited = []
            self.paths = PriorityQueue()
    def get_main(self):
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="m":
                    self.main = np.array([i,j])
                    self.board[i][j] = "s"
        return self.main
    
    def get_dest(self):
        a = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="d":
                    a.append([i,j])
                    self.board[i][j] = "s"
        self.dest = np.array(a)
        return self.dest   

    def get_crates(self):
        a = []
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if self.board[i][j] =="c":
                    a.append([i,j])
                    self.board[i][j] = "s"
        self.crates = np.array(a)
        return self.crates
    
    def isReachable(self, start:np.ndarray, destination:np.ndarray):
        """
        check if there is a possible route from the start to destination on the board

        :param start: starting cords
        :param destination: destination cords
        
        :return Bool: Whether there is possible route
        """
        visited = []
        queue = [start.tolist()]
        dest = destination.tolist()
        if (start==destination).all():
            return True
        if self.board[dest[0],dest[1]] == "w":
            return False
        while (len(queue)>0):
            first = queue.pop()
            # print(first)
            for direction in self.directions:
                a = first[0] + direction[0]
                b = first[1] + direction[1]
                c = [a,b]
                if (c not in visited):
                    if (self.board[a,b] == "s"):
                        if (c == dest):
                            return True
                        else:
                            queue.append(c)
                            visited.append(c)
        return False

    def isGoalState(self, game_state):
        """
        Check if the goal state is reached
        
        """
        if (game_state[1][:, None] == self.dest).all(-1).any(-1).all(-1):
            return True
        return False

    def isVisited(self, game_state, visited:list):
        """
        check if the game_state is visited or not

        :param game_state: [main, [crates]] with main is the main char cords adn crates the cords of crates to be pushed

        :return Bool: True if state is already visited, false otherwise
        """

        for past_state in visited:
            # print("gamestate: {}, past: {}".format(type(game_state[0]),type(past_state[0])))
            if (game_state[0] == past_state[0]).all() and (game_state[1][:, None] == past_state[1]).all(-1).any(-1).all(-1):
                return True
        return False
    def isInBoard(self,i,j):
        if i < self.y and i>=0 and j>=0 and j<self.x:
            return True
        return False    

    def isStuck(self, crate, crates):
        for i in self.stuck_direction:
            d1 = self.directions[i[0]]
            d2 = self.directions[i[1]]
            a = crate[0]+d1[0]
            b = crate[1]+d1[1]
            x = crate[0]+d2[0]
            y = crate[1]+d2[1]
            if (self.board[a,b] == "w" or (np.array([a,b]) == crates).all(-1).any()) and (self.board[x,y] == "w" or (np.array([x,y]) == crates).all(-1).any()):
                return True
        return False

    def generate_state_dfs_main(self, game_state:tuple, move:list, visited:list):
        main = game_state[0]
        crates = game_state[1]
        temp_visited = deepcopy(visited)
        temp_visited.append(game_state)
        if self.isFound:
            return True
        # if (len(self.moves)>0 and len(move)>len(self.moves[-1])):
        #     return
        
        for direction in self.directions:
            #[a, b] is the posssible new place of the main character.
            a = main[0] + direction[0]
            b = main[1] + direction[1]
            new_main = np.array([a,b])
            if self.isInBoard(a,b):
                isCrate = (new_main==crates).all(-1).any()
                if self.board[a,b] == "s" and (not isCrate):
                    new_crate =np.copy(crates)
                    new_state = (new_main,new_crate)
                    if not self.isVisited(new_state, temp_visited):
                        temp_move = deepcopy(move)
                        temp_move.append(self.move_dir[direction])
                        self.generate_state_dfs_main(new_state, temp_move, temp_visited)
                elif isCrate:
                    #[x,y] is possibly the new cords of the crate to be pushed
                    x = a + direction[0]
                    y = b + direction[1]
                    if self.isInBoard(x,y) and self.board[x,y] == "s":
                        new_crates = np.copy(crates)
                        temp_crate = new_main
                        for i in range(new_crates.shape[0]):
                            if (new_crates[i] == temp_crate).all():
                                new_crates[i] = np.array([x,y])
                        new_state = (new_main,new_crates)
                        temp_move = deepcopy(move)
                        temp_move.append(self.push_dir[direction])
                        if self.isGoalState(new_state):
                            self.moves.append(temp_move)
                            # print(temp_move)
                            self.isFound = True
                        elif (not self.isVisited(new_state, temp_visited)) and (not self.isStuck((x,y),new_crates)):
                            self.generate_state_dfs_main(new_state, temp_move, temp_visited)
        return False


    def fn(self, game_state, move):
        """
        calculate the fn of the path

        :param path: [gamestate[main, crates], move]
        :return float:  cost of the path
        """
        gn = len(move)
        hn = np.sum(abs(game_state[1]-self.dest))
        return (hn + gn)

    def generate_state_dfs_main_heuristic(self, game_state:list, move:list, visited:list):

        if self.isFound:
            return True
    
        cost = self.fn(game_state,move)
        self.paths.put((cost, game_state, move, visited))
        chosen_path = self.paths.get()
        
        main = chosen_path[1][0]
        crates = chosen_path[1][1]
        temp_visited = deepcopy(chosen_path[3])
        temp_visited.append(chosen_path[1])

        for direction in self.directions:
            #[a, b] is the posssible new place of the main character.
            a = main[0] + direction[0]
            b = main[1] + direction[1]
            new_main = np.array([a,b])
            if self.isInBoard(a,b):
                isCrate = (new_main==crates).all(-1).any()
                if self.board[a,b] == "s" and (not isCrate):
                    new_crate =np.copy(crates)
                    new_state = (new_main,new_crate)
                    if not self.isVisited(new_state, temp_visited):
                        temp_move = deepcopy(chosen_path[2])
                        temp_move.append(self.move_dir[direction])
                        self.generate_state_dfs_main_heuristic(new_state, temp_move, temp_visited)
                elif isCrate:
                    #[x,y] is possibly the new cords of the crate to be pushed
                    x = a + direction[0]
                    y = b + direction[1]
                    if self.isInBoard(x,y) and self.board[x,y] == "s":
                        new_crates = np.copy(crates)
                        temp_crate = new_main
                        for i in range(new_crates.shape[0]):
                            if (new_crates[i] == temp_crate).all():
                                new_crates[i] = np.array([x,y])
                        new_state = (new_main,new_crates)
                        temp_move = deepcopy(chosen_path[2])
                        temp_move.append(self.push_dir[direction])
                        if self.isGoalState(new_state):
                            self.moves.append(temp_move)
                            # print(temp_move)
                            self.isFound = True
                        elif (not self.isVisited(new_state, temp_visited)) and (not self.isStuck((x,y),new_crates)):
                            self.generate_state_dfs_main_heuristic(new_state, temp_move, temp_visited)

        return False

    def blind_search(self):
        initial_state = (self.main, self.crates)
        return (self.generate_state_dfs_main(initial_state,[],[]))
    def best_first_search(self):
        initial_state = [self.main, self.crates]
        return (self.generate_state_dfs_main_heuristic(initial_state,[],[]))
a = Sokoban()
a.import_input("input/minicosmos1.csv")
# sys.setrecursionlimit(10**6)
# print(a.board)
# print("dest: {} main: {}".format(a.dest,a.main))
# print(a.isReachable(a.main,a.dest[0]))
# print(a.board)



# start = time.time()
# a.blind_search()
# print("Total time: {}".format(time.time()-start))

# count = 1
# for i in a.moves[-1]:
#     print("move {}: {}".format(count,i))
#     count+=1

# start = time.time()
# a.best_first_search()
# print("Total time: {}".format(time.time()-start))

# count = 1
# for i in a.moves[-1]:
#     print("move {}: {}".format(count,i))
#     count+=1


start = time.time()
a.blind_search()
print("Blind Search: \nTotal time: {}\nTotal step: {}\n".format(time.time()-start,len(a.moves[-1])))
print(a.moves)

# start = time.time()
# a.best_first_search()
# print("Best-First Search: \nTotal time: {}\nTotal step: {}\n".format(time.time()-start,len(a.moves[-1])))
# print(a.moves)

