# gym-battleship
OpenAI Gym environment for console based Battleship


    Three possible game modes
    
      Single or Two Player
        Single Player:
          Goal is to destroy enemy ships in as few moves as possible.
          Forces Random Ship Placement
          
          Used for designing optimal firing strategies 
          
        Two Player:
          Goal is to destroy all enemy ships before the enemy destroys yours
          Either Random or Stragetic Ship Placement
          
          Used for comparing firing strategies
          Used for determnining optimal ship placement
          
      Random or Strategic Ship Placement:
        Random:
          Ships are placed randomly throughout grid
          
        Strategic:
          Ship placement determined by agent


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
