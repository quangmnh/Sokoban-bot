import pygame
from Sokoban import Sokoban
import numpy as np

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = 69

class Board:
    def __init__(self, board:list, moves:list, main:np.ndarray):
        # print(board)
        self.board = board
        # print(self.board)
        self.moves = moves
        self.main = main.tolist()
        self.move_counter = 0
        self.assets_load()

    def assets_load(self):
        self.main_char = pygame.image.load('assets/main.png')
        self.brick = pygame.image.load('assets/brick.png')
        self.crate = pygame.image.load('assets/crate.png')
        self.marked = pygame.image.load('assets/marked.jpg')
        self.space = pygame.image.load('assets/space.png')


        self.main_char = pygame.transform.scale(self.main_char, (SQUARE_SIZE, SQUARE_SIZE))
        self.brick = pygame.transform.scale(self.brick, (SQUARE_SIZE, SQUARE_SIZE))
        self.crate = pygame.transform.scale(self.crate, (SQUARE_SIZE, SQUARE_SIZE))
        self.marked = pygame.transform.scale(self.marked, (SQUARE_SIZE, SQUARE_SIZE))
        self.space = pygame.transform.scale(self.space, (SQUARE_SIZE, SQUARE_SIZE))


    def draw_cubes(self, win):
        win.fill(BLACK)
            
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if (self.board[row][col] == "w"):
                    win.blit(self.brick,(col*SQUARE_SIZE,row*SQUARE_SIZE))
                # elif (self.board[row][col] == "s"):
                #     win.blit(self.space,(col*SQUARE_SIZE,row*SQUARE_SIZE))
                elif (self.board[row][col] == "c" or self.board[row][col] == "cd"):
                    win.blit(self.crate,(col*SQUARE_SIZE,row*SQUARE_SIZE))
                elif (self.board[row][col] == "m" or self.board[row][col] == "md"):
                    win.blit(self.main_char,(col*SQUARE_SIZE,row*SQUARE_SIZE))
                elif (self.board[row][col] == "d"):
                    win.blit(self.marked,(col*SQUARE_SIZE,row*SQUARE_SIZE))
        if self.move_counter<len(self.moves)-1: 
            self.move_counter+=1       
            if self.moves[self.move_counter]!="s":
                if self.moves[self.move_counter]=="r":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]][self.main[1]+1] == "s":
                            self.board[self.main[0]][self.main[1]+1] = "m"
                        elif self.board[self.main[0]][self.main[1]+1] == "d":
                            self.board[self.main[0]][self.main[1]+1] = "md"
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]][self.main[1]+1] == "s":
                            self.board[self.main[0]][self.main[1]+1] = "m"
                        elif self.board[self.main[0]][self.main[1]+1] == "d":
                            self.board[self.main[0]][self.main[1]+1] = "md"
                    self.main[1]+=1
                
                if self.moves[self.move_counter]=="l":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]][self.main[1]-1] == "s":
                            self.board[self.main[0]][self.main[1]-1] = "m"
                        elif self.board[self.main[0]][self.main[1]-1] == "d":
                            self.board[self.main[0]][self.main[1]-1] = "md"
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]][self.main[1]-1] == "s":
                            self.board[self.main[0]][self.main[1]-1] = "m"
                        elif self.board[self.main[0]][self.main[1]-1] == "d":
                            self.board[self.main[0]][self.main[1]-1] = "md"
                    self.main[1]-=1

                if self.moves[self.move_counter]=="u":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]-1][self.main[1]] == "s":
                            self.board[self.main[0]-1][self.main[1]] = "m"
                        elif self.board[self.main[0]-1][self.main[1]] == "d":
                            self.board[self.main[0]-1][self.main[1]] = "md"
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]-1][self.main[1]] == "s":
                            self.board[self.main[0]-1][self.main[1]] = "m"
                        elif self.board[self.main[0]-1][self.main[1]] == "d":
                            self.board[self.main[0]-1][self.main[1]] = "md"
                    self.main[0]-=1

                if self.moves[self.move_counter]=="d":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]+1][self.main[1]] == "s":
                            self.board[self.main[0]+1][self.main[1]] = "m"
                        elif self.board[self.main[0]+1][self.main[1]] == "d":
                            self.board[self.main[0]+1][self.main[1]] = "md"
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]+1][self.main[1]] == "s":
                            self.board[self.main[0]+1][self.main[1]] = "m"
                        elif self.board[self.main[0]+1][self.main[1]] == "d":
                            self.board[self.main[0]+1][self.main[1]] = "md"
                    self.main[0]+=1

                if self.moves[self.move_counter]=="R":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]][self.main[1]+1] == "c":
                            self.board[self.main[0]][self.main[1]+1] = "m"
                        elif self.board[self.main[0]][self.main[1]+1] == "cd":
                            self.board[self.main[0]][self.main[1]+1] = "md"
                        if self.board[self.main[0]][self.main[1]+2] == "s":
                            self.board[self.main[0]][self.main[1]+2] = "c"
                        elif self.board[self.main[0]][self.main[1]+2] == "d":
                            self.board[self.main[0]][self.main[1]+2] = "cd"
                
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]][self.main[1]+1] == "c":
                            self.board[self.main[0]][self.main[1]+1] = "m"
                        elif self.board[self.main[0]][self.main[1]+1] == "cd":
                            self.board[self.main[0]][self.main[1]+1] = "md"
                        if self.board[self.main[0]][self.main[1]+2] == "s":
                            self.board[self.main[0]][self.main[1]+2] = "c"
                        elif self.board[self.main[0]][self.main[1]+2] == "d":
                            self.board[self.main[0]][self.main[1]+2] = "cd" 
                    self.main[1]+=1

                if self.moves[self.move_counter]=="L":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]][self.main[1]-1] == "c":
                            self.board[self.main[0]][self.main[1]-1] = "m"
                        elif self.board[self.main[0]][self.main[1]-1] == "cd":
                            self.board[self.main[0]][self.main[1]-1] = "md"
                        if self.board[self.main[0]][self.main[1]-2] == "s":
                            self.board[self.main[0]][self.main[1]-2] = "c"
                        elif self.board[self.main[0]][self.main[1]-2] == "d":
                            self.board[self.main[0]][self.main[1]-2] = "cd"
                
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]][self.main[1]-1] == "c":
                            self.board[self.main[0]][self.main[1]-1] = "m"
                        elif self.board[self.main[0]][self.main[1]-1] == "cd":
                            self.board[self.main[0]][self.main[1]-1] = "md"
                        if self.board[self.main[0]][self.main[1]-2] == "s":
                            self.board[self.main[0]][self.main[1]-2] = "c"
                        elif self.board[self.main[0]][self.main[1]-2] == "d":
                            self.board[self.main[0]][self.main[1]-2] = "cd" 
                    self.main[1]-=1

                
                if self.moves[self.move_counter]=="D":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]+1][self.main[1]] == "c":
                            self.board[self.main[0]+1][self.main[1]] = "m"
                        elif self.board[self.main[0]+1][self.main[1]] == "cd":
                            self.board[self.main[0]+1][self.main[1]] = "md"
                        if self.board[self.main[0]+2][self.main[1]] == "s":
                            self.board[self.main[0]+2][self.main[1]] = "c"
                        elif self.board[self.main[0]+2][self.main[1]] == "d":
                            self.board[self.main[0]+2][self.main[1]] = "cd"
                
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]+1][self.main[1]] == "c":
                            self.board[self.main[0]+1][self.main[1]] = "m"
                        elif self.board[self.main[0]+1][self.main[1]] == "cd":
                            self.board[self.main[0]+1][self.main[1]] = "md"
                        if self.board[self.main[0]+2][self.main[1]] == "s":
                            self.board[self.main[0]+2][self.main[1]] = "c"
                        elif self.board[self.main[0]+2][self.main[1]] == "d":
                            self.board[self.main[0]+2][self.main[1]] = "cd"
                    self.main[0]+=1

                if self.moves[self.move_counter]=="U":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                        if self.board[self.main[0]-1][self.main[1]] == "c":
                            self.board[self.main[0]-1][self.main[1]] = "m"
                        elif self.board[self.main[0]-1][self.main[1]] == "cd":
                            self.board[self.main[0]-1][self.main[1]] = "md"
                        if self.board[self.main[0]-2][self.main[1]] == "s":
                            self.board[self.main[0]-2][self.main[1]] = "c"
                        elif self.board[self.main[0]-2][self.main[1]] == "d":
                            self.board[self.main[0]-2][self.main[1]] = "cd"
                
                    if self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                        if self.board[self.main[0]-1][self.main[1]] == "c":
                            self.board[self.main[0]-1][self.main[1]] = "m"
                        elif self.board[self.main[0]-1][self.main[1]] == "cd":
                            self.board[self.main[0]-1][self.main[1]] = "md"
                        if self.board[self.main[0]-2][self.main[1]] == "s":
                            self.board[self.main[0]-2][self.main[1]] = "c"
                        elif self.board[self.main[0]-2][self.main[1]] == "d":
                            self.board[self.main[0]-2][self.main[1]] = "cd"
                    self.main[0]-=1
class game:
    def __init__(self):
        self.sokoban = Sokoban()
        self.sokoban.import_input('levels/microcosmos1.csv')
        # self.sokoban.blind_search()
        # tmp_move =['s','l', 'u', 'l', 'l', 'u', 'R', 'R', 'R', 'l', 'l', 'u', 'u', 'r', 'r', 'D', 'r', 'D', 'L', 'L', 'r', 'u', 'u', 'l', 'l', 'd', 'D', 'l', 'd', 'R', 'u', 'r', 'D', 'D', 'r', 'r', 'U', 'r', 'u', 'L', 'L', 'L', 'r', 'u', 'u', 'l', 'l', 'd', 'D', 'r', 'd', 'L', 'r', 'd', 'r', 'r', 'd', 'd', 'l', 'l', 'U', 'U']
        # tmp_move = ['s', 'l', 'u', 'u', 'r', 'r', 'D', 'D', 'l', 'l', 'u', 'l', 'l', 'u', 'R', 'R', 'R', 'l', 'l', 'u', 'u', 'r', 'r', 'D', 'r', 'D', 'L', 'L', 'd', 'd', 'r', 'r', 'U', 'r', 'u', 'L', 'L', 'u', 'u', 'l', 'l', 'd', 'D', 'l', 'd', 'R', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'L', 'r', 'u', 'u', 'l', 'l', 'd', 'D', 'r', 'r', 'r', 'd', 'd', 'l', 'l', 'd', 'd', 'r', 'r', 'U', 'U', 'U', 'r', 'u', 'L', 'L', 'L', 'D', 'L', 'U', 'd', 'r', 'D', 'r', 'r', 'd', 'd', 'l', 'l', 'U', 'U']
        tmp_move = ['s', 'r', 'r', 'r', 'u', 'u', 'l', 'D', 'r', 'd', 'L', 'L', 'u', 'L', 'D', 'l', 'd', 'd', 'r', 'r', 'U', 'd', 'l', 'l', 'u', 'u', 'r', 'D', 'u', 'u', 'r', 'r', 'd', 'L', 'u', 'l', 'D', 'l', 'l', 'l', 'u', 'u', 'r', 'D', 'R', 'l', 'l', 'd', 'R', 'R']
        self.board = Board(self.sokoban.org_board,tmp_move,self.sokoban.main)
        self.WIDTH, self.HEIGHT = len(self.board.board[0])*SQUARE_SIZE, len(self.board.board)*SQUARE_SIZE
        self.FPS = 60
        
    def start_windows(self):
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Sokoban')
    
    def main(self):
        run = True
        clock = pygame.time.Clock()

        while(run):
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type  == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    pass
            pygame.time.wait(500)
            self.board.draw_cubes(self.WIN)
            pygame.display.update()
            
        pygame.quit()




g = game()
g.start_windows()
g.main()