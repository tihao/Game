import pygame
import random

pygame.init()

#RGB color code
# Color for grass map
GREEN = (0, 200, 0)
LIGHTGREEN = (0, 255, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
SHADOW = (192, 192, 192)
WALL = (166, 186, 171)
DARKGREEN = (0, 100, 0)
BLACK = (0, 0, 0)
SPEED = 15

class Map:

    def __init__(self, width=1000, height=600):
        self.width = width
        self.height = height
        self.block_size = 20    #Set block size
        self.w = int(self.width/self.block_size)     #Max width with block size
        self.h = int(self.height/self.block_size)   #Max heigh with block size
        self.food = ()
        self.poison_food = list()
        self.display_map = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Smart Snake')
       

    def draw_map(self, first_color, second_color):

        #Set color and fill background
        self.first_color = first_color
        self.second_color = second_color
        self.display_map.fill(first_color)

        # Draw a grid map
        for x in range(self.w)[1:-1]:
            for y in range(self.h)[1:-1]:
                if x % 2 == 0 and y % 2 == 0:
                    pygame.draw.rect(self.display_map, second_color, (self.block_size*x, self.block_size*y, 
                                                                self.block_size, self.block_size))
                elif x % 2 == 1 and y % 2 == 1:
                    pygame.draw.rect(self.display_map, second_color, (self.block_size*x, self.block_size*y, 
                                                                self.block_size, self.block_size))
 

    def add_food(self):
        x = random.randint(1, self.w - 1)
        y = random.randint(1, self.h - 1)
        self.food = (x, y)
       
    def add_poison_food(self):
        x = random.randint(1, self.w - 1)
        y = random.randint(1, self.h - 1)
        self.poison_food.append((x, y))

    def draw_food(self):
        pygame.draw.circle(self.display_map, DARKGREEN, (self.block_size*self.food[0] + 10,self.block_size*self.food[1] + 10), int(self.block_size/2), self.block_size)  

    def draw_poison_food(self):
        for x, y in self.poison_food:
            pygame.draw.circle(self.display_map, BLACK, (self.block_size*x + 10,self.block_size*y + 10), int(self.block_size/2), self.block_size)  

class Snake(Map):
    def __init__(self, snake_color):
        super().__init__()
        self.snake_color = snake_color  #Snake color
        self.point = 0  
        self.x_direction = 0
        self.y_direction = 0
        self.head_snake = (int(self.w/2), self.h - 2)
        self.body_snake = [self.head_snake, (self.head_snake[0],self.head_snake[1] + 1), (self.head_snake[0], self.head_snake[1] + 2), (self.head_snake[0], self.head_snake[1] + 3)]
        

    def draw_body_snake(self):
        for x, y in self.body_snake:
            pygame.draw.rect(self.display_map, self.snake_color, (self.block_size*x, self.block_size*y, 
                                                                self.block_size, self.block_size))
        

    def keyboard_game_play(self):
        #Take input from user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()
                if event.key == pygame.K_RIGHT:
                    self.x_direction = 1
                    self.y_direction = 0
                if event.key == pygame.K_LEFT:
                    self.x_direction = -1
                    self.y_direction = 0
                if event.key == pygame.K_UP:
                    self.x_direction = 0
                    self.y_direction = -1
                if event.key == pygame.K_DOWN:
                    self.x_direction = 0
                    self.y_direction = 1
        
        # #Make a move
        self.make_move(self.x_direction, self.y_direction)
        self.draw_map(GREEN, LIGHTGREEN)
        
        if self.head_snake not in self.body_snake:
            self.body_snake.insert(0, self.head_snake)
            self.body_snake.pop()
            if self.is_eated():
                self.point = self.point + 1
                self.food = set()
                self.add_food()
                if self.food in self.poison_food or self.food in self.body_snake:
                    self.food = set()
                    self.add_food()
                self.add_poison_food()
                
        self.draw_food()
        if self.poison_food is not None:
            self.draw_poison_food()
        
        if self.is_poisoned():
            return True

        self.draw_body_snake()
        self.display_point()
        
        pygame.display.update()
        
        self.clock.tick(SPEED)
    def is_eated(self):
        if self.head_snake == self.food:
            return True
        else:
            return False

    def is_poisoned(self):
        for i in self.poison_food:
            if i in self.body_snake:
                return True

    def make_move(self, x_direction, y_direction):
        x = self.head_snake[0] + x_direction
        y = self.head_snake[1] + y_direction

        # Allow snake run through the map
        if x == -1:
            x = self.w
        elif x == (self.w + 1):
            x = 0
        elif y == -1:
            y = self.h
        elif y == (self.h + 1):
            y = 0
        if (x, y) not in self.body_snake:
            self.head_snake = (x, y)
    
    def display_point(self):
        font = pygame.font.SysFont('didot.ttc', 36)
        img = font.render("Point: " + str(self.point), True, BLACK)
        self.display_map.blit(img, (0, 0))
      
if __name__ == '__main__':
    snake = Snake(BLUE)
    
    snake.add_food()
    pygame.display.update()
    
    while True:
        a = snake.keyboard_game_play()
        if a == True:
            break
        
# pygame.quit()
# quit()
