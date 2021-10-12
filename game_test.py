from copy import deepcopy
import pygame
# from Sokoban import Sokoban
import numpy as np
from enum import Enum
from math import dist
import pygame
from pygame import time
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.time import set_timer
import pygame.freetype
from Sokoban import Sokoban
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SQUARE_SIZE = 69
WIDTH, HEIGHT = 960, 540 
pygame.init()
class State(Enum):
    MAIN_MENU = 1
    SET_CHOOSING = 2
    MINI_CHOOSING = 3
    WAIT_FOR_SEARCHING = 4
    AUTO_ITER = 5
    MANUAL_ITER = 6
    ERROR = 7
    MICRO_CHOOSING = 8
    TIMEOUT = 9

placement = ((104,141),(216,141),(330,141),(431,141),(543,141),(657,141),(770,141),(871,141),
            (104,223),(216,223),(330,223),(431,223),(543,223),(657,223),(770,223),(871,223),
            (104,302),(216,302),(330,302),(431,302),(543,302),(657,302),(770,302),(871,302),
            (104,384),(216,384),(330,384),(431,384),(543,384),(657,384),(770,384),(871,384),
            (104,467),(216,467),(330,467),(431,467),(543,467),(657,467),(770,467),(871,467))
class screen:
    def __init__(self):
        self.state = State.MAIN_MENU
        self.assets_load()
        self.result =''
        self.font = pygame.freetype.Font("assets/RobotoMono-Bold.ttf", 24)
        self.font2 = pygame.freetype.Font("assets/RobotoMono-Bold.ttf", 36)
        self.isNum = False
        self.chosenNum = 0
    def assets_load(self):
        self.main_menu = pygame.image.load('assets/mainmenu.png')
        self.set_choosing = pygame.image.load('assets/setchoosing.png')
        self.mini = pygame.image.load('assets/mini.png')
        self.micro = pygame.image.load('assets/micro.png')
        self.timeout = pygame.image.load('assets/timeout.png')
        self.error = pygame.image.load('assets/error.png')
        self.searching = pygame.image.load('assets/searching.png')
        self.main_char = pygame.image.load('assets/main.png')
        self.brick = pygame.image.load('assets/brick.png')
        self.crate = pygame.image.load('assets/crate.png')
        self.marked = pygame.image.load('assets/marked.jpg')
        self.space = pygame.image.load('assets/space.png')
        self.left = pygame.image.load('assets/keyboard_key_left.png')
        self.right = pygame.image.load('assets/keyboard_key_right.png')
        self.x = pygame.image.load('assets/keyboard_key_x.png')
        self.z = pygame.image.load('assets/keyboard_key_z.png')
        self.c = pygame.image.load('assets/keyboard_key_c.png')
        self.a = pygame.image.load('assets/keyboard_key_a.png')
        self.d = pygame.image.load('assets/keyboard_key_d.png')
        
        self.left = pygame.transform.scale(self.left, (SQUARE_SIZE, SQUARE_SIZE))
        self.right = pygame.transform.scale(self.right, (SQUARE_SIZE, SQUARE_SIZE))
        self.x = pygame.transform.scale(self.x, (SQUARE_SIZE, SQUARE_SIZE))
        self.z = pygame.transform.scale(self.z, (SQUARE_SIZE, SQUARE_SIZE))
        self.c = pygame.transform.scale(self.c, (SQUARE_SIZE, SQUARE_SIZE))
        self.a = pygame.transform.scale(self.a, (SQUARE_SIZE, SQUARE_SIZE))
        self.d = pygame.transform.scale(self.d, (SQUARE_SIZE, SQUARE_SIZE))
        self.main_char = pygame.transform.scale(self.main_char, (SQUARE_SIZE, SQUARE_SIZE))
        self.brick = pygame.transform.scale(self.brick, (SQUARE_SIZE, SQUARE_SIZE))
        self.crate = pygame.transform.scale(self.crate, (SQUARE_SIZE, SQUARE_SIZE))
        self.marked = pygame.transform.scale(self.marked, (SQUARE_SIZE, SQUARE_SIZE))
        self.space = pygame.transform.scale(self.space, (SQUARE_SIZE, SQUARE_SIZE))
    def assign_board(self, board: list, moves: list, main:list):
        self.board = board
        self.org_board = deepcopy(board)
        self.moves = moves
        self.main = main
        self.org_main = deepcopy(main)
        self.move_counter = 0
    def resize_window(self,win):
        win = pygame.display.set_mode((len(self.board[0])*SQUARE_SIZE, (len(self.board)+2.8)*SQUARE_SIZE))
        self.floor = pygame.image.load('assets/floor.png')
        self.floor = pygame.transform.scale(self.floor, (len(self.board[0])*SQUARE_SIZE, (len(self.board)+2.8)*SQUARE_SIZE))
        
        self.push_effect = pygame.mixer.Sound('assets/push.mp3')
        self.rewind_effect = pygame.mixer.Sound('assets/back.wav')
    def resize_window_org(self,win):
        win = pygame.display.set_mode((WIDTH, HEIGHT))
    def draw(self, win):
        if self.state == State.MAIN_MENU:
            win.blit(self.main_menu,(0,0))
        elif self.state == State.SET_CHOOSING:
            win.blit(self.set_choosing,(0,0))
        elif self.state == State.MINI_CHOOSING:
            win.blit(self.mini,(0,0))
            if self.isNum:
                self.font.render_to(win,(90,50),str(self.chosenNum//10)+'_',(255,0,0))
        elif self.state == State.MICRO_CHOOSING:
            win.blit(self.micro,(0,0))
            if self.isNum:
                self.font.render_to(win,(90,50),str(self.chosenNum//10)+'_',(255,0,0))
        elif self.state == State.WAIT_FOR_SEARCHING:
            win.blit(self.searching,(0,0))
            # self.font.render_to(win,(0,0),'AUTO',(random.randint(0,255),0,0))
        elif self.state == State.ERROR:
            win.blit(self.error,(0,0))
        elif self.state == State.TIMEOUT:
            win.blit(self.timeout,(0,0))   
        elif self.state == State.MANUAL_ITER:
            self.draw_cubes(win)
            self.font.render_to(win,((len(self.board[0])//2)*SQUARE_SIZE, (len(self.board)+0.2)*SQUARE_SIZE),'AUTO',(255,0,0))
        elif self.state == State.AUTO_ITER:
            self.draw_cubes(win)
            self.font.render_to(win,((len(self.board[0])//2)*SQUARE_SIZE, (len(self.board)+0.2)*SQUARE_SIZE),'MANU',(255,0,0))
            

    def draw_cubes(self, win):
        win.blit(self.floor,(0,0))    
        # win.fill(BLACK)     
        self.font.render_to(win,(SQUARE_SIZE//4, (len(self.board)+1.6)*SQUARE_SIZE),self.result[0],(255,0,0))
        self.font.render_to(win,(SQUARE_SIZE//4, (len(self.board)+1.9)*SQUARE_SIZE),self.result[1],(255,0,0))
        self.font.render_to(win,(SQUARE_SIZE//4, (len(self.board)+2.2)*SQUARE_SIZE),self.result[2],(255,0,0))
        self.font.render_to(win,(SQUARE_SIZE//4, (len(self.board)+2.5)*SQUARE_SIZE),str(len(self.moves)-1)+' steps taken to goal',(255,0,0))

        win.blit(self.a,(0, (len(self.board)+0.5)*SQUARE_SIZE))
        win.blit(self.d,(((len(self.board[0])-1)*SQUARE_SIZE), (len(self.board)+0.5)*SQUARE_SIZE))
        win.blit(self.z,((len(self.board[0])//2-1)*SQUARE_SIZE, (len(self.board)+0.5)*SQUARE_SIZE))
        win.blit(self.x,((len(self.board[0])//2)*SQUARE_SIZE, (len(self.board)+0.5)*SQUARE_SIZE))
        win.blit(self.c,((len(self.board[0])//2+1)*SQUARE_SIZE, (len(self.board)+0.5)*SQUARE_SIZE))


        self.font.render_to(win,(0, (len(self.board)+0.2)*SQUARE_SIZE),'PREV',(255,0,0))
        self.font.render_to(win,(((len(self.board[0])-1)*SQUARE_SIZE), (len(self.board)+0.2)*SQUARE_SIZE),'NEXT',(255,0,0))
        self.font.render_to(win,((len(self.board[0])//2-1)*SQUARE_SIZE, (len(self.board)+0.2)*SQUARE_SIZE),'BACK',(255,0,0))
        self.font.render_to(win,((len(self.board[0])//2+1)*SQUARE_SIZE, (len(self.board)+0.2)*SQUARE_SIZE),'RESET',(255,0,0))
        

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
        

    def backward_move(self):
        self.rewind_effect.play()
        if self.move_counter>0:
            if self.moves[self.move_counter]!="s":
                if self.moves[self.move_counter]=="l":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]][self.main[1]+1] == "s":
                        self.board[self.main[0]][self.main[1]+1] = "m"
                    elif self.board[self.main[0]][self.main[1]+1] == "d":
                        self.board[self.main[0]][self.main[1]+1] = "md"

                    self.main[1]+=1
                
                if self.moves[self.move_counter]=="r":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]][self.main[1]-1] == "s":
                        self.board[self.main[0]][self.main[1]-1] = "m"
                    elif self.board[self.main[0]][self.main[1]-1] == "d":
                        self.board[self.main[0]][self.main[1]-1] = "md"

                    self.main[1]-=1

                if self.moves[self.move_counter]=="d":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]-1][self.main[1]] == "s":
                        self.board[self.main[0]-1][self.main[1]] = "m"
                    elif self.board[self.main[0]-1][self.main[1]] == "d":
                        self.board[self.main[0]-1][self.main[1]] = "md"
 
                    self.main[0]-=1

                if self.moves[self.move_counter]=="u":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]+1][self.main[1]] == "s":
                        self.board[self.main[0]+1][self.main[1]] = "m"
                    elif self.board[self.main[0]+1][self.main[1]] == "d":
                        self.board[self.main[0]+1][self.main[1]] = "md"

                    self.main[0]+=1

                if self.moves[self.move_counter]=="R":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "c"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "cd"
                    if self.board[self.main[0]][self.main[1]-1] == "s":
                        self.board[self.main[0]][self.main[1]-1] = "m"
                    elif self.board[self.main[0]][self.main[1]-1] == "d":
                        self.board[self.main[0]][self.main[1]-1] = "md"
                    if self.board[self.main[0]][self.main[1]+1] == "c":
                        self.board[self.main[0]][self.main[1]+1] = "s"
                    elif self.board[self.main[0]][self.main[1]+1] == "cd":
                        self.board[self.main[0]][self.main[1]+1] = "d"
                    self.main[1]-=1

                if self.moves[self.move_counter]=="L":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "c"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "cd"
                    if self.board[self.main[0]][self.main[1]+1] == "s":
                        self.board[self.main[0]][self.main[1]+1] = "m"
                    elif self.board[self.main[0]][self.main[1]+1] == "d":
                        self.board[self.main[0]][self.main[1]+1] = "md"
                    if self.board[self.main[0]][self.main[1]-1] == "c":
                        self.board[self.main[0]][self.main[1]-1] = "s"
                    elif self.board[self.main[0]][self.main[1]-1] == "cd":
                        self.board[self.main[0]][self.main[1]-1] = "d"
                    self.main[1]+=1

                if self.moves[self.move_counter]=="U":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "c"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "cd"
                    if self.board[self.main[0]+1][self.main[1]] == "s":
                        self.board[self.main[0]+1][self.main[1]] = "m"
                    elif self.board[self.main[0]+1][self.main[1]] == "d":
                        self.board[self.main[0]+1][self.main[1]] = "md"
                    if self.board[self.main[0]-1][self.main[1]] == "c":
                        self.board[self.main[0]-1][self.main[1]] = "s"
                    elif self.board[self.main[0]-1][self.main[1]] == "cd":
                        self.board[self.main[0]-1][self.main[1]] = "d"
                    self.main[0]+=1

                if self.moves[self.move_counter]=="D":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "c"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "cd"
                    if self.board[self.main[0]-1][self.main[1]] == "s":
                        self.board[self.main[0]-1][self.main[1]] = "m"
                    elif self.board[self.main[0]-1][self.main[1]] == "d":
                        self.board[self.main[0]-1][self.main[1]] = "md"
                    if self.board[self.main[0]+1][self.main[1]] == "c":
                        self.board[self.main[0]+1][self.main[1]] = "s"
                    elif self.board[self.main[0]+1][self.main[1]] == "cd":
                        self.board[self.main[0]+1][self.main[1]] = "d"
                    self.main[0]-=1

            self.move_counter-=1
            
    def forward_move(self):
        
        if self.move_counter<len(self.moves)-1: 
            self.move_counter+=1 
            if self.moves[self.move_counter].isupper():
                self.push_effect.play()      
            if self.moves[self.move_counter]!="s":
                if self.moves[self.move_counter]=="r":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]][self.main[1]+1] == "s":
                        self.board[self.main[0]][self.main[1]+1] = "m"
                    elif self.board[self.main[0]][self.main[1]+1] == "d":
                        self.board[self.main[0]][self.main[1]+1] = "md"


                    self.main[1]+=1
                
                if self.moves[self.move_counter]=="l":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]][self.main[1]-1] == "s":
                        self.board[self.main[0]][self.main[1]-1] = "m"
                    elif self.board[self.main[0]][self.main[1]-1] == "d":
                        self.board[self.main[0]][self.main[1]-1] = "md"
                    
                    self.main[1]-=1

                if self.moves[self.move_counter]=="u":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]-1][self.main[1]] == "s":
                        self.board[self.main[0]-1][self.main[1]] = "m"
                    elif self.board[self.main[0]-1][self.main[1]] == "d":
                        self.board[self.main[0]-1][self.main[1]] = "md"
                    
                    self.main[0]-=1

                if self.moves[self.move_counter]=="d":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
                        self.board[self.main[0]][self.main[1]] = "d"
                    if self.board[self.main[0]+1][self.main[1]] == "s":
                        self.board[self.main[0]+1][self.main[1]] = "m"
                    elif self.board[self.main[0]+1][self.main[1]] == "d":
                        self.board[self.main[0]+1][self.main[1]] = "md"             
                    self.main[0]+=1

                if self.moves[self.move_counter]=="R":
                    if self.board[self.main[0]][self.main[1]] == "m":
                        self.board[self.main[0]][self.main[1]] = "s"
                    elif self.board[self.main[0]][self.main[1]] == "md":
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
                    elif self.board[self.main[0]][self.main[1]] == "md":
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
                    elif self.board[self.main[0]][self.main[1]] == "md":
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
                    elif self.board[self.main[0]][self.main[1]] == "md":
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

def check_placement(point, square):
    if point[0]>=square[0] and point[0]<=square[0]+SQUARE_SIZE and point[1]>=square[1] and point[1]<=square[1]+SQUARE_SIZE:
        return True
    return False
class game:
    def __init__(self):
        self.scr = screen() 
        self.FPS = 60
        
    def start_windows(self):
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Sokoban')

    def main(self):
        run = True
        clock = pygame.time.Clock()
        isNum = False
        chosenNum = 0

        pygame.mixer.music.load('assets/sus.mp3')
        pygame.mixer.music.play(-1)
        while(run):
            clock.tick(self.FPS)
            events = pygame.event.get()
            next_move = pygame.USEREVENT + 10
            for event in events:
                if event.type  == pygame.QUIT:
                    run = False
            if self.scr.state == State.MAIN_MENU:
                for event in events:
                    if event.type  == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.scr.state = State.SET_CHOOSING
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.scr.state = State.SET_CHOOSING
            elif self.scr.state == State.SET_CHOOSING:
                for event in events:
                    if event.type  == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.scr.state = State.MINI_CHOOSING
                        elif event.key == pygame.K_RIGHT:
                            self.scr.state = State.MICRO_CHOOSING
                        elif event.key == pygame.K_z:
                            self.scr.state = State.MAIN_MENU
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if pos[0]>20 and pos[0]<70 and pos[1]>20 and pos[1]<70:
                            self.scr.state = State.MAIN_MENU
                            self.chosen = False 
                        elif pos[1]>90:
                            if pos[0] > 480:
                                self.scr.state = State.MICRO_CHOOSING
                            elif pos[0] <480:
                                self.scr.state = State.MINI_CHOOSING
            elif self.scr.state == State.MINI_CHOOSING:
                for event in events:
                    if event.type  == pygame.KEYUP:
                        if event.key == pygame.K_z:
                            self.scr.state = State.SET_CHOOSING
                            self.chosen = False    
                        elif not isNum: 
                            if event.key == pygame.K_0:
                                chosenNum = 0
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_1:
                                chosenNum = 10
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_2:
                                chosenNum = 20
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_3:
                                chosenNum = 30
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_4:
                                chosenNum = 40
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                        elif isNum: 
                            if event.key == pygame.K_0:
                                chosenNum += 0
                                self.chosen =True
                            elif event.key == pygame.K_1:
                                chosenNum += 1
                                self.chosen =True
                            elif event.key == pygame.K_2:
                                chosenNum += 2
                                self.chosen =True
                            elif event.key == pygame.K_3:
                                chosenNum += 3
                                self.chosen =True
                            elif event.key == pygame.K_4:
                                chosenNum += 4
                                self.chosen =True
                            elif event.key == pygame.K_5:
                                chosenNum += 5
                                self.chosen =True
                            elif event.key == pygame.K_6:
                                chosenNum += 6
                                self.chosen =True
                            elif event.key == pygame.K_7:
                                chosenNum += 7
                                self.chosen =True 
                            elif event.key == pygame.K_8:
                                chosenNum += 8
                                self.chosen =True
                            elif event.key == pygame.K_9:
                                chosenNum += 9
                                self.chosen =True   
                            if self.chosen:
                                if chosenNum==0:
                                    self.chosen = False
                                elif chosenNum>40:
                                    self.chosen = False
                                    chosenNum = 40
                                else:
                                    isNum =False
                                    self.scr.isNum = False
                                    self.chosen_set = 'mini'
                                    self.chosen_level = chosenNum
                                    self.scr.state = State.WAIT_FOR_SEARCHING      
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if pos[0]>20 and pos[0]<70 and pos[1]>20 and pos[1]<70:
                            self.scr.state = State.SET_CHOOSING
                            self.chosen = False 
                        else:
                            for i in range(len(placement)):
                                if dist(pos,placement[i])<30:
                                    self.chosen = True
                                    self.chosen_level = i + 1
                                    self.chosen_set = 'mini'
                                    self.scr.state = State.WAIT_FOR_SEARCHING
            elif self.scr.state == State.MICRO_CHOOSING:
                for event in events:
                    if event.type  == pygame.KEYUP:
                        if event.key == pygame.K_z:
                            self.scr.state = State.SET_CHOOSING
                            self.chosen = False   
                        elif not isNum: 
                            if event.key == pygame.K_0:
                                chosenNum = 0
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_1:
                                chosenNum = 10
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_2:
                                chosenNum = 20
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_3:
                                chosenNum = 30
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                            elif event.key == pygame.K_4:
                                chosenNum = 40
                                isNum = True
                                self.scr.isNum =True
                                self.scr.chosenNum = chosenNum
                        elif isNum: 
                            if event.key == pygame.K_0:
                                chosenNum += 0
                                self.chosen =True
                            elif event.key == pygame.K_1:
                                chosenNum += 1
                                self.chosen =True
                            elif event.key == pygame.K_2:
                                chosenNum += 2
                                self.chosen =True
                            elif event.key == pygame.K_3:
                                chosenNum += 3
                                self.chosen =True
                            elif event.key == pygame.K_4:
                                chosenNum += 4
                                self.chosen =True
                            elif event.key == pygame.K_5:
                                chosenNum += 5
                                self.chosen =True
                            elif event.key == pygame.K_6:
                                chosenNum += 6
                                self.chosen =True
                            elif event.key == pygame.K_7:
                                chosenNum += 7
                                self.chosen =True 
                            elif event.key == pygame.K_8:
                                chosenNum += 8
                                self.chosen =True
                            elif event.key == pygame.K_9:
                                chosenNum += 9
                                self.chosen =True   
                            if self.chosen:
                                if chosenNum==0:
                                    self.chosen = False
                                elif chosenNum>40:
                                    self.chosen = False
                                    chosenNum = 40
                                else:
                                    isNum =False
                                    self.scr.isNum = False
                                    self.chosen_set = 'micro'
                                    self.chosen_level = chosenNum
                                    self.scr.state = State.WAIT_FOR_SEARCHING  
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if pos[0]>20 and pos[0]<70 and pos[1]>20 and pos[1]<70:
                            self.scr.state = State.SET_CHOOSING
                            self.chosen = False 
                        else:
                            for i in range(len(placement)):
                                if dist(pos,placement[i])<30:
                                    self.chosen = True
                                    self.chosen_set = 'micro'
                                    self.chosen_level = i + 1
                                    self.scr.state = State.WAIT_FOR_SEARCHING
            elif self.scr.state ==State.WAIT_FOR_SEARCHING:
                if self.chosen:
                    sokoban = Sokoban()
                    file_name = 'levels/'+ str(self.chosen_set) + 'cosmos' + str(self.chosen_level) + '.csv'
                    sokoban.import_input(file_name)
                    tmp = deepcopy(sokoban.main)
                    res = sokoban.astar_search()
                    if res == 'timeout':
                        self.scr.state = State.TIMEOUT
                    elif res == 'result gotten' :
                        self.scr.state = State.MANUAL_ITER
                        self.scr.assign_board(sokoban.org_board,sokoban.moves[-1],[tmp[0],tmp[1]])
                        self.scr.resize_window(self.WIN)
                        self.scr.result = ['Time taken: {} s'.format(sokoban.time),'Peak memory usage: {}'.format(sokoban.mem[1]),'{} states visited'.format(sokoban.max_queue_length)]
                    elif res == 'error':
                        self.scr.state = State.ERROR
            elif self.scr.state == State.MANUAL_ITER:
                for event in events:
                    if event.type  == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            if self.chosen_set =='micro':
                                self.scr.state = State.MICRO_CHOOSING
                                self.chosen = False
                            elif self.chosen_set =='mini':
                                self.scr.state = State.MINI_CHOOSING
                                self.chosen = False
                            self.scr.resize_window_org(self.WIN)
                        elif event.key == pygame.K_LEFT:
                            self.scr.backward_move()
                        elif event.key == pygame.K_RIGHT:
                            self.scr.forward_move()
                        elif event.key == pygame.K_a:
                            self.scr.backward_move()
                        elif event.key == pygame.K_d:
                            self.scr.forward_move()
                        elif event.key == pygame.K_x:
                            self.scr.state = State.AUTO_ITER
                            pygame.time.set_timer(next_move, 200)
                        elif event.key == pygame.K_c:
                            self.scr.board = deepcopy(self.scr.org_board)
                            self.scr.main = deepcopy(self.scr.org_main)
                            self.scr.move_counter = 0     

                    elif event.type == MOUSEBUTTONUP:
                        pos= pygame.mouse.get_pos()
                        if check_placement(pos,(0, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.backward_move()
                        elif check_placement(pos,(((len(self.scr.board[0])-1)*SQUARE_SIZE), (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.forward_move()
                        elif check_placement(pos,((len(self.scr.board[0])//2-1)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            if self.chosen_set =='micro':
                                self.scr.state = State.MICRO_CHOOSING
                                self.chosen = False
                            elif self.chosen_set =='mini':
                                self.scr.state = State.MINI_CHOOSING
                                self.chosen = False
                            self.scr.resize_window_org(self.WIN)
                        elif check_placement(pos,((len(self.scr.board[0])//2)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.state = State.AUTO_ITER
                            pygame.time.set_timer(next_move, 200)
                        elif check_placement(pos,((len(self.scr.board[0])//2+1)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.board = deepcopy(self.scr.org_board)
                            self.scr.main = deepcopy(self.scr.org_main)
                            self.scr.move_counter = 0  
                        
            elif self.scr.state == State.AUTO_ITER:
                for event in events:
                    if event.type  == pygame.KEYDOWN:
                        if event.key == pygame.K_z:
                            if self.chosen_set =='micro':
                                self.scr.state = State.MICRO_CHOOSING
                                self.chosen =False
                            elif self.chosen_set =='mini':
                                self.scr.state = State.MINI_CHOOSING
                                self.chosen = False
                            self.scr.resize_window_org(self.WIN)
                        elif event.key == pygame.K_x:
                            self.scr.state = State.MANUAL_ITER   
                        elif event.key == pygame.K_LEFT:
                            self.scr.state = State.MANUAL_ITER
                            self.scr.backward_move()
                        elif event.key == pygame.K_RIGHT:
                            self.scr.state = State.MANUAL_ITER  
                            self.scr.forward_move()
                        elif event.key == pygame.K_a:
                            self.scr.state = State.MANUAL_ITER
                            self.scr.backward_move()
                        elif event.key == pygame.K_d:
                            self.scr.state = State.MANUAL_ITER  
                            self.scr.forward_move()   
                        elif event.key == pygame.K_c:
                            self.scr.board = deepcopy(self.scr.org_board)
                            self.scr.main = deepcopy(self.scr.org_main)     
                            self.scr.move_counter = 0             
                    elif event.type == next_move:
                        self.scr.forward_move()
                        pygame.time.set_timer(next_move, 200)
                    elif event.type == MOUSEBUTTONUP:
                        pos= pygame.mouse.get_pos()
                        if check_placement(pos,(0, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.state = State.MANUAL_ITER
                        elif check_placement(pos,(((len(self.scr.board[0])-1)*SQUARE_SIZE), (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.state = State.MANUAL_ITER
                        elif check_placement(pos,((len(self.scr.board[0])//2-1)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            if self.chosen_set =='micro':
                                self.scr.state = State.MICRO_CHOOSING
                                self.chosen = False
                            elif self.chosen_set =='mini':
                                self.scr.state = State.MINI_CHOOSING
                                self.chosen = False
                            
                            self.scr.resize_window_org(self.WIN)
                        elif check_placement(pos,((len(self.scr.board[0])//2)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.state = State.MANUAL_ITER   
                        elif check_placement(pos,((len(self.scr.board[0])//2+1)*SQUARE_SIZE, (len(self.scr.board)+0.5)*SQUARE_SIZE)):
                            self.scr.board = deepcopy(self.scr.org_board)
                            self.scr.main = deepcopy(self.scr.org_main)
                            self.scr.move_counter = 0 
            elif self.scr.state == State.ERROR or self.scr.state == State.TIMEOUT:
                for event in events:
                    if event.type  == pygame.KEYDOWN or pygame.MOUSEBUTTONDOWN:
                        self.scr.state = State.MAIN_MENU
                        self.chosen = False
            

            self.scr.draw(self.WIN)
            pygame.display.update()
        pygame.quit()

g = game()
g.start_windows()
g.main()