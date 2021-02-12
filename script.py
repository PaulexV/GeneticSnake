import pygame, sys, random
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.block_size = 40
        self.new_block = False

    def draw(self, win):
        for block in self.body:
            snk_x = int(block.x * self.block_size)
            snk_y = int(block.y * self.block_size)
            pygame.draw.rect(win, pygame.Color("white"), (snk_x, snk_y, self.block_size, self.block_size))

    def update(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def change_direction(self, direction):
        if direction == "up" and self.direction != Vector2(0, 1):
            self.direction = Vector2(0, -1)
        elif direction == "down" and self.direction != Vector2(0, -1):
            self.direction = Vector2(0, 1)
        elif direction == "left" and self.direction != Vector2(1, 0):
            self.direction = Vector2(-1, 0)
        elif direction == "right" and self.direction != Vector2(-1, 0):
            self.direction = Vector2(1, 0)

    def add_block(self):
        self.new_block = True


class Food:
    def __init__(self):
        self.block_size = 40

    def draw(self, win):
        pygame.draw.rect(win, pygame.Color("red"), (
            int(self.pos.x * self.block_size),
            int(self.pos.y * self.block_size),
            self.block_size,
            self.block_size,
        ))

    def randomize(self, win_size):
        self.x = random.randint(0, win_size - 1)
        self.y = random.randint(0, win_size - 1)
        self.pos = Vector2(self.x, self.y)
        
class Game:
    def __init__(self):
        pygame.font.init()
        self.block_size = 40
        self.win_size = 20
        
        self.win = pygame.display.set_mode((self.block_size*self.win_size, self.block_size*self.win_size))
        pygame.display.set_caption("Snake de PA LE BOGOSS")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 26)
        
        self.snake = Snake() 
        self.food = Food()
        
        self.food.randomize(self.win_size)
        
        self.running = True
    
    def run(self):
        while self.running:
            self.clock.tick(10)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.snake.change_direction("up")
            if keys[pygame.K_DOWN]:
                self.snake.change_direction("down")
            if keys[pygame.K_LEFT]:
                self.snake.change_direction("left")
            if keys[pygame.K_RIGHT]:
                self.snake.change_direction("right")
            
            self.snake.update()   
            if self.is_snake_dead():
                self.running = False
                return
            self.update_food_eaten()
            
            self.draw()
                
            pygame.display.update()
            
        
    def draw(self):
        self.win.fill((0, 0, 0))
        self.food.draw(self.win)
        self.snake.draw(self.win)
        
        self.win.blit(self.font.render(f"Score : {len(self.snake.body)-3}", True, pygame.Color("white")), (700, 760))
        
        
        
        
    def is_snake_dead(self):
        if (
            not 0 <= self.snake.body[0].x < self.win_size
            or not 0 <= self.snake.body[0].y < self.win_size
        ):
            return True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                return True
            
    def update_food_eaten(self):
        if self.food.pos == self.snake.body[0]:
            self.food.randomize(self.win_size)
            self.snake.add_block()
        
        while self.is_snake_on_food():
            self.food.randomize(self.win_size)

    def is_snake_on_food(self):
        for block in self.snake.body:
            if block == self.food.pos:
                return True
        return False

snake_game = Game()
snake_game.run()