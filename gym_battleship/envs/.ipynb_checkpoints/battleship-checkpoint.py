import gym
from gym import spaces
from gym.utils import seeding

import numpy as np

class BattleshipEnv(gym.Env):
    metadata = {
        'render.modes': ['human'],
        'game.modes': ['single', 'two']
    }
    
    def __init__(self, board_size=(10,10)):
        
        fleet = [Ship('AircraftCarrier',5),
                      Ship('Battleship',4),
                      Ship('Submarine',3),
                      Ship('Cruiser',3),
                      Ship('Destroyer',2)]
        
        self.game_mode = 'single'
        
        # Create a seed so we can replicate the random placement of ships
        self.np_random, self.seed = seeding.np_random()
        
        # Set who's turn it is
        self.player_turn = 0
        
        # Create the game board
        n_players = 1 if self.game_mode == 'single' else 2
        self.board = Board(n_players, board_size, fleet, self.seed)
        
        # One action, to select a single position on the board
        # board is 'numbered' left to right, top to bottom
        # indexed: row, columns
        n_action = self.board.shape[0] * self.board.shape[1]
        self.action_space = spaces.Discrete(n_action)   
        
        # 2D array of board state, misses and hits
        self.observation_space = spaces.Box(low=0, high=2,
                                            shape=self.board.shape,
                                            dtype=np.int8)
        
        return
    
    
    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        
        y, x = divmod(action,self.board.shape[0])
    
        n = self.player_turn
        
        # Penalty for taking a show
        reward = -1
        
        # Penalty for shotting where already placed
        if  self.board.shots[n][y, x] == 1:
            reward += -10

        # Place the shot on the board
        self.board.shots[n][y, x] = 1
        
        # create the semi-observable board
        ships = np.nan_to_num(self.board.ships[n]/self.board.ships[n])
        observation = self.board.shots[n] + (self.board.shots[n] * ships)
        
        # Reward for a hit
        if observation[y, x] == 2:
            reward += 5
      
        # Check which ships have been sunk
        unique, counts = np.unique(self.board.shots[n] * self.board.ships[n], return_counts=True)
        # remove 0 from unique and counts
        if unique[0] == 0:
            unique = unique[1:]
            counts = counts[1:]
        
        sunk = []
        for i in range(len(self.board.fleet)):
            if i+1 in unique:
                j = np.where(unique==i+1)
                sunk.append((self.board.fleet[i].length == counts[j])[0])
            else:
                sunk.append(False)
        
        
        done = np.all(sunk)
        ships = {self.board.fleet[i].name : sunk[i] for i in range(len(self.board.fleet))}
        
        # change turn based on game mode
        if self.game_mode == 'single':
            pass
        else:
            self.player_turn = (self.player_turn + 1) % 2
        
        return observation, reward, done, ships
    
  
    def render(self, mode='human'):
        return NotImplemented
    
    def reset(self):
        self.state = 0
        return self.state



class Ship():
    
    def __init__(self, name, length):
        
        assert type(name) is str, "%r (%s) invalid, must be str"%(name, type(name))
        self.name = name
        
        assert type(length) is int, "%r (%s) invalid, must be int"%(length, type(length))
        assert length > 0, "%r invalid, must be great than 0"%(length)
        self.length = length

        
    
class Board():
    
    def __init__(self, n_players, shape, fleet, seed, ships=None):
        
        self.shape = shape
        self.fleet = fleet
        
        # NOTE: Players shoot at thier opponents board, in their ID's index
        # When ships are set, they are set to the opponents ID
        # E.g. player A sets ships at index 1
        self.shots = [np.zeros(self.shape) for i in range(n_players)]

        # place the ships
        if n_players == 1:
            self.ships = (self.place_ships(seed), None)
        
        elif n_players == 2:
            self.ships = (self.place_ships(seed), self.place_ships(seed))
        
        return
    
    def place_ships(self, seed):
        """
        For a ship length of n > 2, and board shape (x,y) where x > n and y > n
        There are ((x-n+1) * y) + (x * (y-n+1)) possible positions on the board
        
        A given ship will blow a number spaces from another ship
        This number depends on the proximity to the edge, the length of both ships, and board size
        
        For a ship of length 2, a positioned ship of length 3 will block at most 10 spaces
        and at minimum 2 (for a grid of 3x1) or 5 on the smalled possible board for both ships
        
        For parallel ships, the number of spaces blocked for ship n by placed ship p is: p+(n-1)
        For perpendicular ships, the number of spcaes block for ship n by placed ship p is: p*n
        Therefore, the maximum number of blocked spaces is: (p*n)+(p+n-1)
        
        The number of spaces blocked by the edges:
        For each parallel edge, the number of possible spaces removed is: (n-dx-1)*p
        For each perpendicular edge, the number of possible spcaces removed is: (n-dx-1)
        The total is then calculated with the different distances to edges
        
        """
        
        # TO-DO - make the seed actually do something
        
        ships = np.zeros(self.shape)
        ship_id = 1
        
        # just pick random positions and directions until all of them fit
        for ship in self.fleet:
            
            while True:
                pos = np.random.randint(self.shape[0]*self.shape[1])
                direction =  np.random.randint(2)
            
                y, x = divmod(pos,self.shape[0])
            
                if direction == 0:
                    space = ships[y, x:x+ship.length]
                else:
                    space = ships[y:y+ship.length, x]
                
                u, c = np.unique(space, return_counts=True)
                
                if u[0] == 0 and c[0] == ship.length:
                    if direction == 0:
                        ships[y, x:x+ship.length] = ship_id
                    else:
                        ships[y:y+ship.length, x] = ship_id
                    
                    ship_id += 1
                    break
        
        return ships
    
    

def main():
    return BattleshipEnv()


if __name__ == '__main__':
    main()