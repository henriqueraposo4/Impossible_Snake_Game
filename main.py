import pygame,random,sys
from pygame.math import Vector2
from pygame import mixer

pygame.init()

#General variables
clock=pygame.time.Clock()
fps= 60
score= 0
snake_speed = 125 #in ms
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,snake_speed)

#Screen
cell_size= 35
cell_number = 20
screen= pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
pygame.display.set_caption("Impossible Snake")

#colors
fruit_color= (120,120,120)
snake_color=(180,110,120)
initial_bg_color=(0,0,0)
screen_color=(175,215,70)
grass_color= (167,209,61)
score_color=(0,0,0)
screen_bg= pygame.image.load('BG_Snake.jpeg').convert_alpha()

#variable
game_status = False
inicial_text_animation=False
can_start= False
change_phase= False
phase_2= False

global possible_pos
        
possible_pos = []

#have difficulties 
#change speed with score as well


def create_possible_pos():
    for i in range(20):
        for n in range(20):
            x=[i,n]
            possible_pos.append(x)

class Level():
    def __init__(self):
        self.fruit=Fruit()
        self.snake=Snake()
        self.bomb=Bomb()
        self.lose_5= Lose_5()
        global score
        score = 0
        
    def collision(self):
        global score
        if self.fruit.pos == self.snake.body[0]:
            if score < 10:
                self.snake.addblock()
                score += 1
                self.fruit.randomize()

            elif 10 <= score < 20:
                self.snake.addblock()
                score += 1
                self.lose_5.create_lose_5()
                self.fruit.randomize()

            elif score >= 20:
                self.snake.addblock()
                score += 1
                self.bomb.create_bomb()
                self.bomb.create_bomb()
                self.fruit.randomize()

        for i in range(len(self.snake.body)):
            if self.fruit.pos == self.snake.body[i]:
                self.fruit.randomize()

        for i in range(len(self.bomb.bomb_positions)):
            if self.snake.body[0] == self.bomb.bomb_positions[i]:
                print('hit bomb')
                self.game_over()
                break

        for i in range(len(self.lose_5.lose_5_positions)):
            if self.snake.body[0] == self.lose_5.lose_5_positions[i]:
                score= score - 5
                self.lose_5.lose_5_positions.pop(i)
                self.lose_5.lose_5.pop(i)
                break

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print('hit body')
                self.game_over()
    
    def out_of_bounds(self):
        if not 0 <= self.snake.body[0].x < cell_number:
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            
    def game_over(self):
        global score
        possible_pos.clear()
        create_possible_pos()
        self.bomb.erase()
        self.lose_5.erase_lose_5()
        pygame.time.wait(400)
        self.snake.direction= Vector2(1,0)
        self.snake.body= [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.snake.head= self.snake.head_left
        score = 0
        self.frame_interation= 0

    def draw_grass(self):
        for row in range(cell_number):
            if row %2 ==0:
                for col in range(cell_number):
                    if col %2 ==0:
                        grass_rect= pygame.Rect(col*cell_size, row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range (cell_number):
                    if col %2 !=0:
                        grass_rect= pygame.Rect(col*cell_size, row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def draw_score(self):
        font = pygame.font.Font(('NineTsukiRegular.ttf'), 60)
        img=font.render(str(score),True,score_color)
        screen.blit(img, ((cell_number-2)*cell_size,(cell_number-2)*cell_size))

    def win(self):
        if score >= 30:
            self.bomb.erase()
            self.lose_5.erase_lose_5()
            pygame.time.wait(400)
            self.snake.direction = Vector2(1, 0)
            self.snake.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
            self.snake.head = self.snake.head_left
            self.frame_interation = 0
            text_animation('You Won', (160, 17), 100, 300)

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.bomb.draw_bomb()
        self.lose_5.draw_lose_5()
        self.draw_score()

    def run(self):
        #self.draw_grass()
        #self.draw_score()
        self.snake.update()
        #self.fruit.draw_fruit()
        #self.snake.draw_snake()
        self.collision()
        self.out_of_bounds()
        #self.bomb.draw_bomb()
        #self.lose_5.draw_lose_5()
        self.win()

class Fruit():
    def __init__(self):
        self.randomize()
        self.apple= pygame.image.load('apple_40x40.png').convert_alpha()
        
    def randomize(self):
        self.possible_pos_index= random.randint(0, len(possible_pos)-1)
        self.x= possible_pos[self.possible_pos_index][0]
        self.y= possible_pos[self.possible_pos_index][1]
        self.pos= Vector2(self.x,self.y)
    
    def draw_fruit(self):
        self.fruit_rect= pygame.Rect((self.x*cell_size)-8, (self.y*cell_size)-8, cell_size, cell_size)
        screen.blit(self.apple, self.fruit_rect)
        
class Snake(): 
    def __init__(self):
        self.body= [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction= Vector2(1,0)
        self.new_block=False
        self.movement=True
		
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        
        self.head= self.head_right
        self.tail= self.tail_left
        
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            self.block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,self.block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail,self.block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,self.block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,self.block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,self.block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,self.block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,self.block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,self.block_rect)
                        
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

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): 
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): 
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): 
            self.tail = self.tail_down
            
    def move_snake(self):
        if self.new_block == True:
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            self.new_block = False
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
    
    def get_input(self):
        global run
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.direction.y != 1:
                        self.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    if self.direction.y != -1:
                        self.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT:
                    if self.direction.x != -1:
                        self.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT:
                    if self.direction.x != 1:
                        self.direction = Vector2(-1, 0)
            if event.type == pygame.QUIT:
                run = False

    def addblock(self):
        self.new_block=True

    def stop_moving(self):
        self.movement= False

    def allow_moving(self):
        self.movement= True
        
    def update(self):
        if self.movement:
            #self.get_input()
            self.move_snake()

class Bomb():
    def __init__(self):
        self.bombs = []
        self.bomb_graphic=pygame.image.load('bomb_circle.png').convert_alpha()
        self.bomb_positions=[]

    def create_bomb(self):
        self.possible_pos_index= random.randint(0, len(possible_pos)-1)
        self.x= possible_pos[self.possible_pos_index][0]
        self.y= possible_pos[self.possible_pos_index][1]
        self.pos = Vector2(self.x, self.y)
        self.bomb_positions.append(self.pos)
        bomb_rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        self.bombs.append(bomb_rect)
        possible_pos.remove(self.pos)

    def draw_bomb(self):
        for bomb in self.bombs:
            screen.blit(self.bomb_graphic,bomb)

    def erase(self):
        self.bombs.clear()
        self.bomb_positions.clear()

class Lose_5():
    def __init__(self):
        self.lose_5 = []
        self.lose_5_graphics= pygame.image.load('Circle_minus_five.png').convert_alpha()
        self.lose_5_positions=[]

    def create_lose_5(self):
        self.possible_pos_index_5= random.randint(0,len(possible_pos)-1)
        self.x= possible_pos[self.possible_pos_index_5][0]
        self.y= possible_pos[self.possible_pos_index_5][1]
        self.position= Vector2(self.x,self.y)
        self.lose_5_positions.append(self.position)
        lose_5_rect= pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)
        self.lose_5.append(lose_5_rect)
        possible_pos.remove(self.position)

    def draw_lose_5(self):
        for element in self.lose_5:
            screen.blit(self.lose_5_graphics,element)

    def erase_lose_5(self):
        self.lose_5.clear()
        self.lose_5_positions.clear()

def draw_text(text,font,font_size,text_color,x,y):
    text_font=pygame.font.Font(('NineTsukiRegular.ttf'), font_size)
    img= text_font.render(text,True,text_color)
    screen.blit(img, (x,y))

def text_animation(str, tuple,font_size,time):
    text_font=pygame.font.Font(('NineTsukiRegular.ttf'), font_size)
    x, y = tuple
    y = y*10 ##shift text down by one line
    char = ''        ##new string that will take text one char at a time. Not the best variable name I know.
    letter = 0
    count = 0
    for i in range(len(str)):
        pygame.event.clear() ## this is very important if your event queue is not handled properly elsewhere. Alternativly pygame.event.pump() would work.
        pygame.time.wait(time) ##change this for faster or slower text animation
        char = char + str[letter]
        text = text_font.render(char, True, (152, 0, 0)) #First tuple is text color, second tuple is background color
        textrect = text.get_rect(topleft=(x, y)) ## x, y's provided in function call. y coordinate amended by line height where needed
        screen.blit(text, textrect)
        pygame.display.update(textrect) ## update only the text just added without removing previous lines.
        count += 1
        letter += 1

def intro():
    mixer.music.load('Duel_of_the_Fates.mp3')
    mixer.music.play(loops=0)
    pygame.time.wait(10000)
    text_animation('Welcome', (200, 17), 100, 300)
    text_animation('To', (300, 27), 100, 300)
    text_animation('Impossible Snake', (45, 37), 100, 400)
    erase()
    text_animation('Your Goal', (160, 17), 100, 300)
    text_animation('is to Reach',(100,27),100,300)
    text_animation('30 Points',(100,37),160,400)
    erase()
    text_animation('But',(150,27),250,700)
    erase()
    text_animation("This isn't",(150,17),100,300)
    text_animation('Normal Snake',(130,27),100,300)
    erase()
    text_animation("Because",(100,27),250,380)
    erase()
    text_animation('I will',(40,10),200,350)
    text_animation('stop you!',(50,25),200,350)
    #end aroun 0:56
    text_animation('I will',(40,10),200,350)
    text_animation('throw bombs', (40, 20), 200, 350)
    text_animation('at you', (40, 30), 200, 350)
    erase()
    text_animation('I will',(40,10),200,350)
    text_animation('take away', (40, 20), 200, 350)
    text_animation('your point', (40, 30), 200, 350)
    erase()
    text_animation('I will', (40, 10), 200, 350)
    text_animation('mess up', (40, 20), 200, 350)
    text_animation('your inputs', (40, 30), 200, 350)
    erase()
    ##final from 1:32
    text_animation('So...', (100, 27), 300, 500)
    erase()
    text_animation('Are you ready?',(50,27),150,300)
    erase()
    text_animation('to rage',(15,27),200,400)
    erase()
    text_animation('to suffer', (15, 27), 200, 400)
    erase()
    text_animation('to die!', (10, 27), 300, 500)
    erase()
    text_animation('The Joruney', (10,17), 300, 500)
    text_animation('starts', (10, 27), 300, 500)
    text_animation('now!', (10, 37), 300, 500)
    erase()
    text_animation('Good Luck...', (10, 27), 300, 500)

def erase():
    pygame.time.wait(2000)
    screen.fill((0,0,0))
    pygame.display.update()

def stop_game():
    global change_phase
    global game_status
    game_status= False
    change_phase= True


create_possible_pos()
phase_1=Level()

run=True 
while run:
    
    screen.fill((0,0,0))
    
    if game_status == False and change_phase==False:
        if inicial_text_animation==False:
            #intro()
            inicial_text_animation=True
        
        if inicial_text_animation==True:
            screen.blit(screen_bg,(0,0))
            can_start=True
            draw_text("Press Space to Start", None, 80, (255,255,255), 30 , cell_number*cell_size/2-50)
    
    if game_status:
        screen.fill(screen_color)
        phase_1.draw_elements()
        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
        if game_status and can_start and phase_2==False:  
            if event.type == SCREEN_UPDATE:
                phase_1.run()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if phase_1.snake.direction.y != 1:
                    phase_1.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if phase_1.snake.direction.y != -1:
                    phase_1.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if phase_1.snake.direction.x != -1:
                    phase_1.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if phase_1.snake.direction.x != 1:
                    phase_1.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_SPACE:
                game_status= True
    
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
sys.exit()