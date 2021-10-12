#                         _ooOoo_
#                        o8888888o
#                        88" . "88
#                        (| -_- |)
#                        O\  =  /O
#                     ____/`---'\____
#                   .'  \\|     |//  `.
#                  /  \\|||  :  |||//  \
#                 /  _||||| -:- |||||_  \
#                 |   | \\\  -  /'| |   |
#                 | \_|  `\`---'//  |_/ |
#                 \  .-\__ `-. -'__/-.  /
#               ___`. .'  /--.--\  `. .'___
#            ."" '<  `.___\_<|>_/___.' _> \"".
#           | | :  `- \`. ;`. _/; .'/ /  .' ; |
#           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#                         `=--=-'                    
#
#
#      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
#                 Buddha Bless: "No Bugs"
#
#
#=============================================================


#! usr/bin/python
from datetime import datetime
import os
import csv
from copy import deepcopy
import numpy as np
import time
from collections import deque
from queue import PriorityQueue
import tracemalloc
from tqdm import tqdm



class Sokoban:
    """
    Sokoban solver, made availabale as a module for easy importing

    Just import the class and call one of the function
        sokoban = Sokoban()
        sokoban.run_all_micro()
        sokoban.run_all_mini()
        sokoban.run_all_astar()
        sokoban.run_all()
        sokoban.run_one(<search method, ie, bfs or astar>, <level set, ie mini or micro>, <level number>)   
    """
    def __init__(self) -> None:
        pass
    
    def import_input(self, link:str):
        """
        Utility function for importing imput, from the csv files in the levels folder.
        The input files contain a map representing block on the boards:
            m  : Main character or player
            c  : Crate or box
            d  : Destination
            w  : Wall
            md : Main character standing on destination block
            cd : Crate standing on destination block

        :param link: String that is the location of csv file on device
        :return None: Actually nothing to return here, cause it's unlikely that the import would fail, provided we had all levels covered.

        In case you want to add another level, please check it carefully before running            
        """
        with open(link,newline='') as csvfile:
            
            board = csv.reader(csvfile) # import the csv file using csv reader module
            
            self.board = np.array(list(board)) #turn the result to a np.array for possiblt faster calculation
            self.org_board = deepcopy(self.board).tolist() #save an orginal board for back up 
            
            self.get_main()  #get cords of main character, result is a np.ndarray saved along with the instance
            self.get_crates() #get cords of the crates, result is a np.ndarray saved along with the instance
            self.get_dest() #get cords of destinations, result is a np.ndarray saved along with the instance
            
            self.directions = ((0, 1), (0, -1), (1, 0), (-1, 0)) # four directions around the main char, right, left, down, up in order
            
            #eight direction around the main char, right, left, down, up, up right, left down, up left, down right in order
            self.eight_directions = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1))

            # patterns indicating deadlock state of a crate, more information in the report, margin too short to write the explanation UmU
            self.stuck_pattern = np.array((
                                           (1,0,0,1,0,0,0,0),  #crate stuck in a corner of 2 walls
                                           (1,0,1,0,0,0,0,0),
                                           (0,1,1,0,0,0,0,0),
                                           (0,1,0,1,0,0,0,0),
                                           (2,0,0,2,0,0,1,0),  #crate stuck in a corner of 2 crates and 1 wall
                                           (2,0,2,0,1,0,0,0),
                                           (0,2,2,0,0,0,0,1),
                                           (0,2,0,2,0,1,0,0),
                                           (2,0,0,2,0,0,2,0),  #crate stuck in a corner with 3 crates
                                           (2,0,2,0,2,0,0,0),
                                           (0,2,2,0,0,0,0,2),
                                           (0,2,0,2,0,2,0,0),                               
                                           (0,1,0,2,0,1,0,0),  #crate stuck in a corner with 2 walls and 1 crate
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
     
            self.pattern_keyid = deepcopy(self.stuck_pattern) #key position of blockage, explanation in the report
            self.pattern_keyid[self.pattern_keyid>1]=1


            # 2 dicts for translating direction to moves, used to append moves while calculating
            self.push_dir = {
                (0,1) : "R",
                (0,-1) : "L",
                (1,0) : "D",
                (-1,0) : "U"    
            }
            self.move_dir = {
                (0,1) : "r",
                (0,-1) : "l",
                (1,0) : "d",
                (-1,0) : "u"    
            }

            self.moves = [] #save the move found. Initially want to find all solution, so i left this as a list

    def get_main(self):
        """
        utility function to find cords of the main char. Just loop and compare
        :return np.ndarray: cords of the main character
        """
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
        """
        utility function to find cords of the destination. Just loop and compare
        :return np.ndarray: cords of the destination
        """
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

        """
        utility function to find cords of the crates. Just loop and compare
        :return np.ndarray: cords of the crates, 2D matrix
        """
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
        """
        Get 8 blocks around the crates and compare with the patterns for dead lock detect

        :param crate: numpy array containing the cords of the crate to be checks
        :param crates: 2D numpy array containing the cordsof the crates currently on the boards
        :return bool: Whether or not the crate is stuck
        """
        if (crate==self.dest).all(-1).any():
            return False  # exclude the crate that already reach a destination, since the destination might be on one of the deadlock state
        state_pattern = np.zeros(8) #array containing the state of the 8 blocks around the crate, 1 for walls, 2 for crates.
        for i in range(8):
            pos = crate + self.eight_directions[i]
            if self.board[pos[0],pos[1]]=="w":
                state_pattern[i] = 1   #this block is a wall
            elif (pos==crates).all(-1).any():
                state_pattern[i] = 2   #this block is a crate
        #comparing logic, == operator for comparing with pattern, logical and for checking key position whether the crate has exact pattern.
        return (np.logical_and(state_pattern==self.stuck_pattern,self.pattern_keyid)==self.pattern_keyid).all(-1).any()
        

    def generate_state_bfs_main(self, initial_state:np.ndarray):
        """
        Main function for generating state space and search. Each state is defined by the main character's cords and the crates' cords
        Each step is taken when the character move 1 of the 4 direction (lef, right, up, down) or push a crate along a direction.
        The move is legal when the block moved to or pushed the crate to is empty space, denoted by "s" ion the board.

        :param initial_state: a numpy array with first 2 member being the main char cords and the remaning ones cords of the crates
        :return literal str: One of the 3 strings. 'timeout' means the search take too long (over 1500s) and was pruned. 'result gotten'
        means search was able to find a solution. When this happened, the solution is appended to the moves list of the instance.
        'no result' mean search was unable to do so.  
        """
        
        queue = deque() # a queue to keep track of states
        queue.append((initial_state,["s"])) # Actually the state is combined with the moves from start to create a tuple. queue stored these tuples.
        visited = {tuple(initial_state)} # visited states,saved in a set. the state is converte to a tuple for set hash.
        while (queue):
            if (time.time()-self.start>1500):
                self.time = 1500
                return "timeout"
            temp = queue.popleft() # pop the first state 
            game_state = temp[0] 
            move = temp[1]
            main = game_state[0:2]
            crates = game_state[2:]
            for direction in self.directions: # 4 directions
                #new_main is the new cords of the block main will move into
                new_main = main + direction
                reshaped_crate = crates.reshape(-1,2) #reshape the crate to a mx2 matrix for easier comparing 
                if (new_main == reshaped_crate).all(-1).any(): #check if the new main cords is a crate, when this happened, the move become a push operation
                    new_crate = new_main + direction #the new cords crate is one block ahead of the main
                    #check if the new crate's cords is really anempty space and not containing a crate
                    if self.board[new_crate[0], new_crate[1]] == "s" and not (new_crate == reshaped_crate).all(-1).any(): 
                        new_crates = np.copy(reshaped_crate)
                        new_crates[np.nonzero((new_main==new_crates).all(-1)==True)[0][0]] = new_crate #replace the old crate cords with the new one.
                        new_state = np.concatenate((new_main, new_crates.ravel())) #combine the new main's cords and the new crate's cords for a new state
                        new_move = move + [self.push_dir[direction]] #append the new move the list of current moves
                        if (new_crates[:,None] == self.dest).all(-1).any(-1).all(): #check if the state is the goal state then end the search
                            self.moves.append(new_move)
                            self.time = time.time() - self.start
                            self.max_queue_length = len(visited)
                            return "result gotten"
                        else: #if not goal state go on and append the new state and move to the queue if the state is not dead lock and has't been visited
                            temp_state = tuple(new_state)
                            if  temp_state not in visited and not self.isStuck(new_crate,new_crates):
                                visited.add(temp_state)
                                queue.append((new_state,new_move))
                elif self.board[new_main[0], new_main[1]] == "s": #if the new main's cords is free, just move forward
                    new_state = np.concatenate((new_main, crates)) #create new state and move and append like above
                    new_move = move + [self.move_dir[direction]]
                    temp_state = tuple(new_state)
                    if temp_state not in visited:
                        visited.add(temp_state)
                        queue.append((new_state,new_move))
        return "no result" #return this if no state left to visit

    def fn(self,move,game_state): 
        """
        Heuristic used to fasten the search for large state space. This function combine manhattan distance from the crates
        to destination and total moves from initial for an approximate cost.

        The push operation is considered superior to the plain move so we might only consider the push or give the moves 
        lesser impact on the cost. 

        :param move: list of moves made till to get to this state
        :param game_state: state of the game, combination of main's cords and crates' cords.
        :return int or float: return an int or a float number, approximate cost
        """
        gn = len([m for m in move if m.isupper()]) #+0.1*len([m for m in move if not m.isupper()])
        hn = np.sum(abs(game_state[2:]-self.destcon))
        return (gn + hn)
    

    def generate_state_astar_main(self, initial_state:np.ndarray):
        """
        Main function for generating state space and search, using A* algorithm. Basically the same to the above Bread-first Search, but 
        with the queue using Priority queue. Each state is tagged along with a cost for switching to the best branch available. 

        Since the code structure is largely based on the BFS above, we'll only denote some change. 

        :param initial_state: a numpy array with first 2 member being the main char cords and the remaning ones cords of the crates
        :return literal str: One of the 3 strings. 'timeout' means the search take too long (over 1500s) and was pruned. 'result gotten'
        means search was able to find a solution. When this happened, the solution is appended to the moves list of the instance.
        'no result' mean search was unable to do so.  
        """
        
        queue = PriorityQueue() # Priority queue from the queue module, it's implemented using heapq and i see no problem using this.
        queue.put((self.fn(["s"],initial_state),initial_state.tolist(),["s"])) #The tuples in the queue is pretty much the same, except the cost tagged along
        visited = {tuple(initial_state)}
        while (queue.qsize()>0):
            if (time.time()-self.start>3600):
                self.time = 3600
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
                            self.max_queue_length = len(visited)
                            return "result gotten"
                        else:
                            temp_state = tuple(new_state)
                            if not (temp_state in visited ) and not self.isStuck(new_crate,new_crates):
                                visited.add(temp_state)
                                queue.put((self.fn(new_move,new_state),new_state.tolist(),new_move)) #tuple is tagged with its cost

                elif self.board[new_main[0], new_main[1]] == "s":
                    new_state = np.concatenate((new_main, crates))
                    new_move = move + [self.move_dir[direction]]
                    temp_state = tuple(new_state)
                    if not (temp_state in visited):
                        visited.add(temp_state)
                        queue.put((self.fn(new_move,new_state),new_state.tolist(),new_move)) #tuple is tagged with its cost
        return "no result"
    def blind_search(self):
        """
        Wrapper function to search the state space using Bread-first Search and measuring searching time using time module
        and max memory usage using tracmalloc module.

        :return literal str: Just return the response from the search function 'timeout', 'result gotten', 'no result'
        """
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
        """
        Wrapper function to search the state space using A* algorithm and measuring searching time using time module
        and max memory usage using tracmalloc module.

        :return literal str: Just return the response from the search function 'timeout', 'result gotten', 'no result'
        """
        init_state = np.concatenate((self.main,self.crates.reshape(1,-1)[0]))
        self.start = time.time()
        tracemalloc.start()
        search = self.generate_state_astar_main(init_state)
        self.mem = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        tracemalloc.stop()
        return search

    def run_all_mini(self):
        """
        utility function used to import all input from mini cosmos and search using 2 algorithms, result stored in a folder name 
        result with the time the search start
        """
        mydir = 'result/result' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(mydir)
        for type in ['bfs', 'astar']:
            res_name = mydir + '/minicosmos_'+type+'.txt'
            with open(res_name,"w+") as file:
                print('Searching mini cosmos levels with '+type)
                for i in tqdm(range(1,41)):
                    file_name = 'levels/minicosmos' + str(i) + '.csv'
                    self.import_input(file_name)
                    if type == 'bfs':
                        search = self.blind_search()
                    else:
                        search = self.astar_search()
                    result =''
                    if search == "timeout":
                        result = 'Mini cosmos {} :  Time out errorr\n\n'.format(i)
                    elif search == "result gotten":
                        moves = ''
                        for move in self.moves[-1]:
                            if move!="s":
                                moves += move
                        result = 'Mini cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\nNumber of state visited: {}\n\n'.format(i,moves,self.time,self.mem[1],self.max_queue_length)
                    elif search == "no result":
                        result = 'Mini cosmos {} :  No result found\n\n'.format(i)
                    file.write(result)
    def run_all_micro(self):
        """
        utility function used to import all input from micro cosmos and search using 2 algorithms, result stored in a folder name 
        result with the time the search start
        """
        mydir = 'result/result' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(mydir)
        for type in ['bfs', 'astar']:
            res_name = mydir + '/microcosmos_'+type+'.txt'
            with open(res_name,"w+") as file:
                print('Searching micro cosmos levels with '+type)
                for i in tqdm(range(1,41)):
                    file_name = 'levels/minicosmos' + str(i) + '.csv'
                    self.import_input(file_name)
                    if type == 'bfs':
                        search = self.blind_search()
                    else:
                        search = self.astar_search()
                    result =''
                    if search == "timeout":
                        result = 'Mini cosmos {} :  Time out errorr\n\n'.format(i)
                    elif search == "result gotten":
                        moves = ''
                        for move in self.moves[-1]:
                            if move!="s":
                                moves += move
                        result = 'Mini cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\nNumber of state visited: {}\n\n'.format(i,moves,self.time,self.mem[1],self.max_queue_length)
                    elif search == "no result":
                        result = 'Mini cosmos {} :  No result found\n\n'.format(i)
                    file.write(result)
    
    def run_all_bfs(self):
        """
        utility function used to import all input from and search using Bread-first Search algorithm, result stored in a folder name 
        result with the time the search start
        """
        mydir = 'result/result' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(mydir)
        translate = {
            'mini' : 'Mini',
            'micro' : 'Micro',
            'bfs' : 'Bread-first Search',
            'astar': 'A *'
        }
        for level_set in ['mini', 'micro']:
            for type in ['bfs']:
                res_name = mydir + '/' + level_set + 'cosmos_'+type+'.txt'
                with open(res_name,"w+") as file:
                    print('Searching {} cosmos levels with {}'.format(level_set,type))
                    for i in tqdm(range(1,41)):
                        file_name = 'levels/' + level_set + 'cosmos' + str(i) + '.csv'
                        self.import_input(file_name)
                        if type == 'bfs':
                            search = self.blind_search()
                        else:
                            search = self.astar_search()
                        result =''
                        if search == "timeout":
                            result = '{} Cosmos {} :  Time out errorr\n\n'.format(translate[level_set],i)
                        elif search == "result gotten":
                            moves = ''
                            for move in self.moves[-1]:
                                if move!="s":
                                    moves += move
                            result = '{} Cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\nNumber of state visited: {}\n\n'.format(translate[level_set],i,moves,self.time,self.mem[1],self.max_queue_length)
                        elif search == "no result":
                            result = '{} Cosmos {} :  No result found\n\n'.format(translate[level_set],i)
                        file.write(result)
    
    def run_all_astar(self):
        """
        utility function used to import all input from and search using A* algorithm, result stored in a folder name 
        result with the time the search start
        """
        mydir = 'result/result' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(mydir)
        translate = {
            'mini' : 'Mini',
            'micro' : 'Micro',
            'bfs' : 'Bread-first Search',
            'astar': 'A *'
        }
        for level_set in ['mini', 'micro']:
            for type in ['astar']:
                res_name = mydir + '/' + level_set + 'cosmos_'+type+'.txt'
                with open(res_name,"w+") as file:
                    print('Searching {} cosmos levels with {}'.format(level_set,type))
                    for i in tqdm(range(1,41)):
                        file_name = 'levels/' + level_set + 'cosmos' + str(i) + '.csv'
                        self.import_input(file_name)
                        if type == 'bfs':
                            search = self.blind_search()
                        else:
                            search = self.astar_search()
                        result =''
                        if search == "timeout":
                            result = '{} Cosmos {} :  Time out errorr\n\n'.format(translate[level_set],i)
                        elif search == "result gotten":
                            moves = ''
                            for move in self.moves[-1]:
                                if move!="s":
                                    moves += move
                            result = '{} Cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\nNumber of state visited: {}\n\n'.format(translate[level_set],i,moves,self.time,self.mem[1],self.max_queue_length)
                        elif search == "no result":
                            result = '{} Cosmos {} :  No result found\n\n'.format(translate[level_set],i)
                        file.write(result)
    def run_all(self):
        """
        utility function used to import all input and seach using both algorithms result stored in a folder name 
        result with the time the search start
        """
        mydir = 'result/result' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(mydir)
        translate = {
            'mini' : 'Mini',
            'micro' : 'Micro',
            'bfs' : 'Bread-first Search',
            'astar': 'A *'
        }
        for level_set in ['mini', 'micro']:
            for type in ['bfs', 'astar']:
                res_name = mydir + '/' + level_set + 'cosmos_'+type+'.txt'
                with open(res_name,"w+") as file:
                    print('Searching {} cosmos levels with {}'.format(level_set,type))
                    for i in tqdm(range(1,41)):
                        file_name = 'levels/' + level_set + 'cosmos' + str(i) + '.csv'
                        self.import_input(file_name)
                        if type == 'bfs':
                            search = self.blind_search()
                        else:
                            search = self.astar_search()
                        result =''
                        if search == "timeout":
                            result = '{} Cosmos {} :  Time out errorr\n\n'.format(translate[level_set],i)
                        elif search == "result gotten":
                            moves = ''
                            for move in self.moves[-1]:
                                if move!="s":
                                    moves += move
                            result = '{} Cosmos {} :  {}\nTime taken: {} s\nPeak memory usage: {}\nNumber of state visited: {}\n\n'.format(translate[level_set],i,moves,self.time,self.mem[1],self.max_queue_length)
                        elif search == "no result":
                            result = '{} Cosmos {} :  No result found\n\n'.format(translate[level_set],i)
                        file.write(result)
    def run_one(self, method, level_set, level):
        """
        utility function used to run only one map, using one algorithm, result stored in a folder name 
        result with the time the search start.

        :param method: 'bfs' or 'astar', one of the 2 algorithms.
        :param level_set: 'mini' or 'micro', one of the 2 set of inputs.
        :param level: 1 to 40, one of the 40 maps the level set

        No return so please consider before running this function.
        """
        file_name = 'levels/{}cosmos{}.csv'.format(level_set,level)
        self.import_input(file_name)
        if method == 'bfs':
            search = self.blind_search()
        else:
            search = self.astar_search()
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
