import numpy as np
from os import system

class Maze:
    """Generate mazes using the reverse backtracking algorithm"""
    def __init__(self, size):
        self.size = size
        # the maze is represented by a 2D-array
        # 1: wall, 0: path
        # initially, all tiles are set to 1
        self.tiles = [[1 for x in range(self.size)] for y in range(self.size)]
        self.tiles = np.array(self.tiles)

    # a method to set wall tiles to be path tiles
    # the maze is created by 'digging' through the walls
    def dig(self, x, y): 
        self.tiles[y][x] = 0
    
    # a method to check whether a tile has not been visited before by the maze generation algorithm
    def is_diggable(self, x, y):
        # check if (y,x) is in bounds
        if 0 <= x < self.size and 0 <= y < self.size:
            # if in bounds, has the tile not been visited before?
            return self.tiles[y][x] == 1 
        else:
            return False
    
    # the maze generation algorithm
    # a recursive method for digging paths 
    def dig_maze(self, x, y):
        # excavate the current position
        self.dig(x, y)
        
        # left, right, up, down
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        np.random.shuffle(directions)
        
        # in random order, check each direction...
        while len(directions) > 0:
            direction = directions.pop()
            target_x = x + (direction[0] * 2)
            target_y = y + (direction[1] * 2)
            # ... and if the target tile is a valid destination...
            if self.is_diggable(target_x, target_y):
                # ... dig a path to the target location
                self.dig(x + direction[0], y + direction[1])
                # recursion
                self.dig_maze(target_x, target_y)
        return self.tiles 

class Gridworld:
    """Creates an environment for the agent to interact with"""
    def __init__(self, size):
        # generate two mazes, one starting from the top left and one starting from the bottom right
        # then stick them together
        # 'size' needs to be an odd integer, otherwise the agent won't be able to reach the goal!
        self.grid = np.append(Maze(size).dig_maze(0,0),Maze(size).dig_maze(-0,-0), axis=1)
        #
        self.grid = np.repeat(np.repeat(self.grid,2,axis=0),2,axis=1)
        # place boundaries so that the agent doesn't escaoe
        self.grid = np.pad(self.grid, (1,1), 'constant', constant_values=(1,1))
        # create a list of all path tile coordinates
        self.paths = []
        for i in range(size):
            for j in range(size*2):
                if self.grid[i,j] == 0:
                    self.paths.append([i,j])
        
        # choose 10% percent of path tiles to be turned into special tiles
        sample = np.random.choice(len(self.paths),len(self.paths)//10, replace=False)
        # create a list of all special tile coordinates
        self.special_paths = [self.paths[x] for x in sample]
        # set path tiles to special tiles
        for i in self.special_paths:
            special_x = i[0]
            special_y = i[1]
            self.grid[special_x, special_y] = 3
                
        # define start position as top-left corner
        self.start = (1,1)
        self.y, self.x = self.start
        # define terminal state as bottom-right corner
        self.end = (size,size*2)
        
    def reset(self):
        self.y, self.x = self.start
        return self.y, self.x
    
    def step(self,action):
        # rewards
        collision = -1
        treasure = 100
        # stuff the function returns later
        reward = 0
        terminal = False
        
        # if the current tile is a special tile
        if self.grid[self.y,self.x] == 3:
            # pick a random direction to walk in
            action = np.random.choice(['left','right','up','down'], p=[0.25,0.25,0.25,0.25])
            # teleport to a random special tile?
            # teleport through adjacent wall?
        
        # actions are passed as strings
        if action == 'left':
            #self.position = tuple(map(lambda i, j: i + j, self.position, (0,-1)))
            # if the target is not a wall, move to the target
            if self.grid[self.y,self.x-1] == 0 or self.grid[self.y,self.x-1] == 3:
                self.x -= 1
            # if the target is a wall, give a negative reward
            else:
                reward += collision
        elif action == 'right':
            if self.grid[self.y,self.x+1] == 0 or self.grid[self.y,self.x+1] == 3:
                self.x += 1
            else:
                reward += collision
        elif action == 'up':
            if self.grid[self.y-1,self.x] == 0 or self.grid[self.y-1,self.x] == 3:
                self.y -= 1
            else:
                reward += collision
        elif action == 'down':
            if self.grid[self.y+1,self.x] == 0 or self.grid[self.y+1,self.x] == 3:
                self.y += 1
            else:
                reward += collision
        
        # if the new state is the terminal state, give a positive reward reward and set boolean to True
        if (self.y, self.x) == self.end:
            reward += treasure
            terminal = True
        
        return self.y, self.x, reward, terminal
    
    # a method for printing the gridworld
    def visualize(self):
            visualization = self.grid.copy()
            # represent the agent
            visualization[self.y, self.x] = 2
            print(visualization)
    
    # a method for assuming manual control of the agent
    # might move this to the agent class later? We could play one episode and then let the agent take over just to see what happens
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

            
class Agent():
    """"""
    
grid = Gridworld(7)
print(grid.paths)
#print(grid.special_paths)
grid.play()




        

    
    