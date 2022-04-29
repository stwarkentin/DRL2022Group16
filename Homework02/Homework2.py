import numpy as np
from os import system

class Maze:
    """"""
    def __init__(self, size):
        self.size = size
        self.tiles = [[1 for x in range(self.size)] for y in range(self.size)]
        self.tiles = np.array(self.tiles)
        
    def dig(self, x, y): 
        self.tiles[y][x] = 0
        
    def is_diggable(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.tiles[y][x] == 1 
        else:
            return False
        
    def dig_maze(self, x, y):
        self.dig(x, y)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        np.random.shuffle(directions)
        while len(directions) > 0:
            direction = directions.pop()
            #next_tile = tuple(map(lambda i, j: i + j, tile, next_direction))
            next_x = x + (direction[0] * 2)
            next_y = y + (direction[1] * 2)
            if self.is_diggable(next_x, next_y):
                self.dig(x + direction[0], y + direction[1])
                self.dig_maze(next_x, next_y)
        return self.tiles 

class Gridworld:
    """"""
    
    def __init__(self, size):
        self.grid = np.append(MazeMaker(size).dig_maze(0,0),MazeMaker(size).dig_maze(-0,-0), axis=1)
        #self.grid = np.repeat(np.repeat(self.grid,2, axis=0), 2, axis=1)
        self.grid = np.pad(self.grid, (1,1), 'constant', constant_values=(1,1))
        self.paths = []
        for i in range(size):
            for j in range(size*2):
                if self.grid[i,j] == 0:
                    self.paths.append([i,j])
        self.special_paths = np.random.choice(self.paths, size=len(self.paths)//10, replace=False)
                
        
        self.start = (1,1)
        self.y, self.x = self.start
        self.end = (size,size*2)
        
    def reset(self):
        self.y, self.x = self.start
        return self.y, self.x
    
    def step(self,action):
        collision = -1
        treasure = 100
        reward = 0
        terminal = False
        if action == 'left':
            #self.position = tuple(map(lambda i, j: i + j, self.position, (0,-1)))
            if self.grid[self.y,self.x-1] == 0:
                self.x -= 1
            else:
                reward += collision
        elif action == 'right':
            #self.position = tuple(map(lambda i, j: i + j, self.position, (0,1)))
            if self.grid[self.y,self.x+1] == 0:
                self.x += 1
            else:
                reward += collision
        elif action == 'up':
            #self.position = tuple(map(lambda i, j: i + j, self.position, (-1,0)))
            if self.grid[self.y-1,self.x] == 0:
                self.y -= 1
            else:
                reward += collision
        elif action == 'down':
            #self.position = tuple(map(lambda i, j: i + j, self.position, (1,0)))
            if self.grid[self.y+1,self.x] == 0:
                self.y += 1
            else:
                reward += collision
        
        if (self.y, self.x) == self.end:
            reward += treasure
            terminal = True
        
        return self.y, self.x, reward, terminal
    
    def visualize(self):
            visualization = self.grid.copy()
            # represent the agent
            visualization[self.y, self.x] = 2
            print(visualization)

    def play(self):
        input_directions = {
            'w': 'up',
            'a': 'left',
            's': 'down',
            'd': 'right'
        }
        reward = 0
        t= False
        while True:
            system('clear')
            self.visualize()
            print(reward)
            print(t)
            print(self.y, self.x)
            action = input_directions[input('WASD >>>')]
            y,x,r,t = self.step(action)
            reward += r

grid = Gridworld(7)
print(grid.paths)
print(grid.paths.type)
print(grid.special_paths)
#grid.play()




        

    
    