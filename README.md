# gym-battleship

gym-battleship is a texted-basd gym environment for the classic game of Battleship. It was designed to allow the development of optimal strategic agents, and to develop agents in an adversial environment.


## Game Modes

### Single Player

Single player mode allows the creation of optimal firing agents. This mode randomly positions an opponents ships, then allows for the agent to take consecutive shots until all ships have been sunk.

Since it is impossible to react to an opponent firing on your ship, the goal of the game becomes to sink all the opponents ships before they sink yours. Therefore, the goal is to minimize the number of shots required to sink all the opponents ships.


### Two Player

Two player mode allows two agents to play against eachother.



## Technical Details

### Action Space

### Observation Space

### Reward

### Game Parameters





    Four boards:
      ships = (player a, player b)
      shots = [player a, player b]
    
    Can observe where you previously fired shots and what were hits
    and know which ships have been sunk
    
    OpponentBoard:
      Empty: 0
      Miss: 1
      Hit: 2
    
    OpponentShipsSunk:
      Alive: 0
      Sunk: 1
    """
    
    """
    Parameters:
      game_mode:
        options: ['single', 'two_random', 'two_strategic']
        default: 'single'
        
      ships:
        dict of ship names and lengths
        default: {'Carrier':5,'Battleship':4,'Submarine':3,
                  'Cruiser':3,'Destroyer':2}
        
      board_size:
        tuple of board x y dimensions
        default: (10,10)
        
    """
    
    """
    Possible Actions:
      Fire, on any location on the board
      
    Observation Space:
      Partially observable opponents board, showing misses and hits
    """
