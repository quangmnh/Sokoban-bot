import csv
from copy import deepcopy
import sys
import numpy as np
import time

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
            self.state = []
            self.y = len(self.board)
            self.x = len(self.board[0])
            self.directions = ((0, 1), (0, -1), (1, 0), (-1, 0))
            self.move_dir = {
                (0,1) : "lp",
                (0,-1) : "rp",
                (1,0) : "up",
                (-1,0) : "dp"    
            }
            self.states = []
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

    def isVisited(self, game_state):
        """
        check if the game_state is visited or not

        :param game_state: [main, [crates]] with main is the main char cords adn crates the cords of crates to be pushed

        :return Bool: True if state is already visited, false otherwise
        """

        for past_state in self.visited:
            if self.isReachable(game_state[0], past_state[0]) and (game_state[1][:, None] == past_state[1]).all(-1).any(-1).all(-1):
                return True
        return False

    def update_state(self, game_state:list):
        """
        update the state and return a list of state that might progress the game

        :param game_state: [main, [crates]] with main is the main char cords adn crates the cords of crates to be pushed
        
        :return list: a list of states that can be generate by main char pushing a crate
        """
        res_state =[]
        #game_state[1] is the cords of the crates, crate is now cords of a single crate to be pushed
        for i in range(game_state[1].shape[0]):
            # directions contain the 4 direction that main char can come and push the crate, direction is one of them 
            for direction in self.directions:
                a = game_state[1][i][0] + direction[0]
                b = game_state[1][i][1] + direction[1]
                c = [a,b]
                x = game_state[1][i][0] - direction[0]
                y = game_state[1][i][1] - direction[1]
                # [a, b] is one of the cell main can reach, in one of the 4 direction around the crate.
                # Hence, [x, y] is the new place crate pushed to. It have to be "s" so the crate can be pushed to.
                if self.isReachable(game_state[0], np.array([a,b])) and self.board[x,y] == "s":
                    temp_crate =np.copy(game_state[1])
                    temp_crate[i] = np.array([x,y])
                    new_state = [np.array([game_state[1][i][0],game_state[1][i][1]]), temp_crate]
                    if not self.isVisited(new_state):
                        res_state.append(new_state)
                        self.visited.append(new_state)
        return res_state

    def isGoalState(self, game_state):
        """
        Check if the goal state is reached
        
        """
        if (game_state[1][:, None] == self.dest).all(-1).any(-1).all(-1):
            return True
        return False

    def generate_state_bfs(self):
        #game start state, with initial main cords and crates cords
        self.visited = [] # list of state visited, not to get there again
        init_state = [self.main, self.crates]
        self.queue = [init_state]
        self.route = []
        while (len(self.queue)>0):
            newstates = self.update_state(init_state)
            self.states.append(newstates)
            print(newstates)
            for state in newstates:
                if not self.isGoalState(state):
                    self.queue.append(state)
                    # self.visited.append(state)
                else:
                    # print(self.visited)
                    return True
        return False

a = Sokoban()
a.import_input("input/minicosmos1.csv")
sys.setrecursionlimit(10**6)
# print(a.board)
# print("dest: {} main: {}".format(a.dest,a.main))
# print(a.isReachable(a.main,a.dest[0]))
a.generate_state_bfs()
for i in a.states:
    print(i)