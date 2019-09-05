from gym.envs.registration import register

register(
    id='Battleship-v0',
    entry_point='gym_battleship.envs:BattleshipEnv',
)