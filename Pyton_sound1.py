import pygame
import sys
import random 
from pygame.math import Vector2
class SNAKE:
    def __init__(self):
       self.body= [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
       self.direction = Vector2(0,0)
       self.newblock = False

       self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
       self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
       self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
       self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()

       self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
       self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
       self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
       self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

       self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
       self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

       self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
       self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
       self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
       self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
       self.crunch_sound=pygame.mixer.Sound('Sound/crunch.wab')
       

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            self.tail = self.tail_left
            return self.tail
        elif tail_relation == Vector2(-1,0): 
            self.tail = self.tail_right
            return self.tail
        elif tail_relation == Vector2(0,1): 
            self.tail = self.tail_up
            return self.tail
        elif tail_relation == Vector2(0,-1): 
            self.tail = self.tail_down
            return self.tail
    def draw_snake(self):
       self.update_head_graphics()
       self.update_tail_graphics()

       #pentru marimea snake-ului
       for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            #directia sarpelui
            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) -1:
                screen.blit(self.tail,block_rect)
                #snake middle blocks
            else: 
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                    #snake corners
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)  
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect) 
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect) 
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)                
                   
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
             self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down
    def move_snake(self):
        #se creste sarpele miscandu-l cu o pozitie in directie fara sa se taie ultimul Vector
        if self.newblock == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newblock = False
        else:
        #se misca sarpele miscandu-l cu o pozitie in directie dar se taie ultima pozitie pentru a pastra marimea 
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    def grow(self):
        self.newblock = True
    def play_crunch_sound(self):
        self.crunch_sound_play()

    def reset (self):
        self.body= [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
class FRUCT:
    def __init__(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number - 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
        #se alege pozitia x si y ->vector 2D
        #functie care deseneaza patratul (fructul)
    def draw_fruit(self):
        #pygame.Rect are nevoie de int dar ii dam float (valorile dintr-un vector sunt de tip float)
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y *cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(255,0,0),fruit_rect)
        #se aleg x,y(coordate dint-un vector) la intamplare
    def randomize(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number- 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
class MAIN:
    #folosita pentru ca codul sa arate mai bine + snake si fruct in aceeasi metoda -> mai usor sa realizez munch
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUCT()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        #daca fructul si capul sunt pe aceeasi pozitie,atunci munch
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow()
            self.snake_play_crunch_sound()
        for block in self.snake.body[1:]
          if block== self.fruit.pos:
            self.friut.randomize()

    def draw_grass(self):
        grass_color = (52,136,60)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 ==0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 !=0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def check_fail(self):
        if not (0 <= self.snake.body[0].x < cell_number) or not (0 <= self.snake.body[0].y < cell_number):
           self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        #check if snake hits itself

    def game_over(self):
       self.snake.reset()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_front.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)
        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,12),bg_rect)
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
#variabola care tine fereastra in timpul in care jocul se intampla
screen = pygame.display.set_mode((cell_number*cell_size ,cell_number*cell_size))
#clock este folosit pentru a stabiliza frame-rate-ul(la 60)
clock = pygame.time.Clock()
#exemplu de importat grafica(graficile marului)
apple = pygame.image.load('graphics/apple.png').convert_alpha()
game_front = pygame.font.Font('graphics/subatomic.ttf', 25)
#un while care merge permanent,trebuie inchis dinauntu
SCREEN_UPDATE = pygame.USEREVENT
#this event will trigger every 150ms
pygame.time.set_timer(SCREEN_UPDATE,150)
main_game = MAIN()
while True:
    #daca ceva se inampla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #daca ce s-a intamplat e sa dai pe X,quit.
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = (Vector2(0,-1))
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:

                    main_game.snake.direction = (Vector2(0,1))
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = (Vector2(1,0))
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x !=1: 
                    main_game.snake.direction = (Vector2(-1,0))
    screen.fill((21,119,40))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
    
    