import gamelib
import random
import math
import warnings
from sys import maxsize


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

Additional functions are made available by importing the AdvancedGameState
class from gamelib/advanced.py as a replcement for the regular GameState class
in game.py.

You can analyze action frames by modifying algocore.py.

The GameState.map object can be manually manipulated to create hypothetical
board states. Though, we recommended making a copy of the map to preserve
the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        random.seed()

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]


    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        #game_state.suppress_warnings(True)  #Uncomment this line to suppress warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safey be replaced for your custom algo.
    """
    def starter_strategy(self, game_state):

        self.build_defences(game_state)

        """
        Finally deploy our information units to attack.
        """
        self.deploy_attackers(game_state)


    def build_defences(self, game_state):
        for i in range (3,16):
            if game_state.can_spawn(FILTER, [i,10]):
                game_state.attempt_spawn(FILTER, [i,10])
        for i in range (19,25):
            if game_state.can_spawn(FILTER, [i,10]):
                game_state.attempt_spawn(FILTER, [i,10])

        if game_state.can_spawn(ENCRYPTOR, [15,9] ):
            game_state.attempt_spawn(ENCRYPTOR, [15,9])

        if game_state.can_spawn(ENCRYPTOR, [19,9] ):
            game_state.attempt_spawn(ENCRYPTOR, [19,9])

        destructor_locations = [[4,12],[7,12],[10,12],[13,12],[16,12],[19,12],[22,12],[25,12]]
        gamelib.debug_write('Cores = ' + str(game_state.CORES))
        while(game_state.CORES > 3):
            rand = random.randint(0,len(destructor_locations)-1)
            gamelib.debug_write('Cores = ' + str(game_state.CORES))
            if(game_state.can_spawn(DESTRUCTOR, destructor_locations[rand])):
                game_state.attempt_spawn(DESTRUCTOR, destructor_locations[rand])

    def deploy_attackers(self, game_state):
        if(game_state.turn_number < 10):
            if(game_state.turn_number % 2 == 0):
                for i in range(5):
                    if game_state.can_spawn(PING, [11,2]):
                        game_state.attempt_spawn(PING, [11,2])
            else:
                if game_state.can_spawn(EMP, [11,2]):
                        game_state.attempt_spawn(EMP, [11,2])
                if game_state.can_spawn(PING, [11,2]):
                    game_state.attempt_spawn(PING, [11,2])
        else:
            if(game_state.turn_number % 2 == 0):
                for i in range(2):
                    if game_state.can_spawn(PING, [11,2]):
                        game_state.attempt_spawn(PING, [11,2])
            else:
                if(game_state.turn_number % 2 == 0):
                    for i in range(2):
                        if game_state.can_spawn(EMP, [11,2]):
                            game_state.attempt_spawn(EMP, [11,2])
                    while(game_state.BITS >= 1):
                        if game_state.can_spawn(PING, [11,2]):
                            game_state.attempt_spawn(PING, [11,2])
                else:
                    for i in range(2):
                        if game_state.can_spawn(SCRAMBLER, [11,2]):
                            game_state.attempt_spawn(SCRAMBLER, [11,2])
                    while(game_state.BITS >= 1):
                        if game_state.can_spawn(PING, [11,2]):
                            game_state.attempt_spawn(PING, [11,2])



    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
