
import csv
from copy import deepcopy
import sys
class Sokoban:
    def __init__(self) -> None:
        pass
    
    def import_input(self, link:str):
        with open(link,newline='') as csvfile:
            board = csv.reader(csvfile)
            self.board = list(board)
            self.get_dest()
            self.get_main()
            self.state = []
            self.y = len(self.board)
            self.x = len(self.board[0])
            self.prev_boards =[]
            self.moves = []
            self.count = 0
            self.test = []

    def get_main(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] =="m":
                    self.main = [i,j]
                    return self.main
    
    def get_dest(self):
        self.dest = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] =="d":
                    self.dest.append([i,j])
                    return self.dest
    


    def isInBoard(self,i,j):
        if i < self.y and i>=0 and j>=0 and j<self.x:
            return True
        return False

    def isGoal(self, board):
        for i in self.dest:
            if board[i[0]][i[1]] != "c":
                # print(board[i[0]][i[1]])
                return False
        print('hmmmmmmmmmmmmmmmmmmm')
        # self.print_board(board)
        # # exit()
        return True

    def isStuck(self, board, i, j):
        if self.isInBoard(i,j+1) and self.isInBoard(i+1,j) and (board[i][j+1] == "w" and board[i+1][j] == "w"):
            return True
        elif self.isInBoard(i+1,j) and self.isInBoard(i,j-1) and (board[i+1][j] == "w" and board[i][j-1] == "w"):
            return True
        elif self.isInBoard(i,j-1) and self.isInBoard(i-1,j) and (board[i][j-1] == "w" and board[i-1][j] == "w"):
            return True
        elif self.isInBoard(i-1,j) and self.isInBoard(i,j+1) and (board[i-1][j] == "w" and board[i][j+1] == "w"):
            return True
        # self.test.append(board)
        return False
    def state_generate_dfs(self, move:list, board, prev_board:list, i, j):
        # self.print_move_board(move,board)
        # self.count+=1
        # print(self.count)

        if self.isInBoard(i,j+2)  and self.isInBoard(i,j+1) and board[i][j+1] ==  "c" and (board[i][j+2] == "s" or board[i][j+2] == "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("rp")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i][j+1] = "m"
            temp_board[i][j+2] = "c"
            if self.isGoal(temp_board):
                self.moves.append(temp_move)
                if len(temp_move)<40:
                    print(temp_move)
                    exit()
            elif temp_board not in prev_board and not self.isStuck(temp_board,i,j+2):
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i,j+1)

        if self.isInBoard(i,j-2)  and self.isInBoard(i,j-1) and board[i][j-1] ==  "c" and (board[i][j-2] == "s" or board[i][j-2] == "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("lp")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i][j-1] = "m"
            temp_board[i][j-2] = "c"
            if self.isGoal(temp_board):
                self.moves.append(temp_move)
                # exit()
            elif temp_board not in prev_board and not self.isStuck(temp_board,i,j-2):
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i,j-1)

        if self.isInBoard(i+2,j)  and self.isInBoard(i+1,j) and board[i+1][j] ==  "c" and (board[i+2][j] == "s" or board[i+2][j] == "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("dp")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i+1][j] = "m"
            temp_board[i+2][j] = "c"
            if self.isGoal(temp_board):
                self.moves.append(temp_move)
                # exit()
            elif temp_board not in prev_board and not self.isStuck(temp_board,i+2,j):
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i+1,j)


        if self.isInBoard(i-2,j)  and self.isInBoard(i-1,j) and board[i-1][j] ==  "c" and (board[i-2][j] == "s" or board[i-2][j] == "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("up")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i-1][j] = "m"
            temp_board[i-2][j] = "c"
            if self.isGoal(temp_board):
                self.moves.append(temp_move)
                # exit()
            elif temp_board not in prev_board and not self.isStuck(temp_board,i-2,j):
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i-1,j)



        if self.isInBoard(i,j+1) and (board[i][j+1] ==  "s" or board[i][j+1] ==  "d"):
            # print('r')
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("r")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i][j+1] = "m"
            if temp_board not in prev_board:
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i,j+1)
                



        if self.isInBoard(i,j-1) and (board[i][j-1] ==  "s" or board[i][j-1] ==  "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("l")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i][j-1] = "m"
            if temp_board not in prev_board:
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i,j-1)




        if self.isInBoard(i+1,j) and (board[i+1][j] ==  "s" or board[i+1][j] ==  "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("d")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i+1][j] = "m"
            if temp_board not in prev_board:
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i+1,j)




        if self.isInBoard(i-1,j) and (board[i-1][j] ==  "s" or board[i-1][j] ==  "d"):
            temp_board = deepcopy(board)
            temp_move = deepcopy(move)
            temp_move.append("u")
            temp_prev = deepcopy(prev_board)
            if [i,j] in self.dest:
                temp_board[i][j] = "d"
            else:
                temp_board[i][j] = "s"
            temp_board[i-1][j] = "m"
            if temp_board not in prev_board:
                temp_prev.append(temp_board)
                self.state_generate_dfs(temp_move, temp_board, temp_prev, i-1,j)


    def print_move_board(self, move:list, board:list):
        if len(move) == 0:
            print('No move taken yet')
        else:
            print("Move taken: {}".format(move[-1]))
        for i in board:
            print(i)
    def print_board(self, board):
        for i in board:
            print(i)
    def print_prev_board(self):
        for i in range(len(self.prev_boards)):
            print("=====================================================================")
            print(self.moves[i])
            for j in range(len(self.prev_boards[i])):
                if j>0:
                    print("Move: {}".format(self.moves[i][j-1]))
                else: 
                    print("Move next:")
                for k in self.prev_boards[i][j]:
                    print(k)
    def state_search_DFS(self):
        self.state_generate_dfs([], self.board, [self.board], self.main[0],self.main[1])
a = Sokoban()
a.import_input("input/minicosmos1.csv")
sys.setrecursionlimit(10**6)
a.state_search_DFS()
print(a.moves)
# a.print_prev_board()
# print(a.count)
