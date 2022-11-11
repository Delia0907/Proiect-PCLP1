import pygame
import sys
import random
from pygame.math import Vector2
class SNAKE:
    def __init__(self):
        self.body= [Vector2(5,10),Vector2(6,10),Vector2(7,10)]
        self.direction = Vector2(1,0)
        self.newblock = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            #ca metoda fruct
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(pygame.Color('blue')),block_rect)

    def move_snake(self):
        if self.newblock == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newblock = False
        else:
           body_copy = self.body[:-1]
           body_copy.insert(0,body_copy[0] + self.direction)
           self.body = body_copy[:]
    def grow(self):
        self.newblock = True

class FRUCT:
    def __init__(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number- 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
        #se alege pozitia x si y -> vector 2D
    #functie care deseneaza patratul(fructul)
    def draw_fruit(self):
        #pygame.Rect are nevoie de int dar ii dam float(valorile dintr-un vector sunt de tip float)
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y *cell_size),cell_size,cell_size)
        pygame.draw.rect(screen,(255,0,0),fruit_rect)
    def randomize(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number- 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUCT()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def check_collision(self):
        #daca fructul si capul sunt pe aceeasi pozitie,atunci munch
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow()

pygame.init()
cell_size = 40
cell_number = 20
#variabila care tine fereastra in care jocul se va intampla
screen = pygame.display.set_mode((cell_number*cell_size ,cell_number*cell_size ))
#clock este folosit pentru a stabiliza frame-rate-ul(la 60)
clock = pygame.time.Clock()
#un while care merge permanent,trebuie inchis dinauntru
SCREEN_UPDATE = pygame.USEREVENT
#this event will trigger every 150ms
pygame.time.set_timer(SCREEN_UPDATE,150)
main_game = MAIN()
while True:
    #daca ceva se intampla 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #daca ce s-a intamplat e sa dai pe X,quit.
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = (Vector2(0,-1))
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = (Vector2(0,1))
            if event.key == pygame.K_RIGHT:
               main_game.snake.direction = (Vector2(1,0))
            if event.key == pygame.K_LEFT:
               main_game.snake.direction = Vector2(-1,0)
    screen.fill((175,220,80))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)