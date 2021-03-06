import gamelib
import random
import math
import warnings
from sys import maxsize


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


    def starter_strategy(self, game_state):

        self.build_defences(game_state)
        self.deploy_attackers(game_state)


    def build_defences(self, game_state):

        """Turn ONE"""
        turnOneFilters = [[0,13],[1,13],[2,13],[3,13],[4,12],[26,13],[25,12],[10,12],[15,12]]
        turnOneDestructors = [[1,12],[2,12],[3,12],[27,13],[26,12],[25,12],[10,11],[15,11]]
        for i in turnOneFilters:
            if game_state.can_spawn(FILTER, i):
                game_state.attempt_spawn(FILTER, i)
        for i in turnOneDestructors:
            if game_state.can_spawn(DESTRUCTOR, i):
                game_state.attempt_spawn(DESTRUCTOR, i)

        """ the  wall """

        starterWall = [[5,12],[6,12],[7,12],[8,12],[9,12],[10,12],[11,12],[12,12],[13,12],
                    [14,12],[15,12],[16,12],[17,12],[18,12],[19,12],[20,12],[21,12],[22,12]]

        for i in starterWall:
            if game_state.can_spawn(FILTER, i):
                game_state.attempt_spawn(FILTER, i)

        if game_state.can_spawn(ENCRYPTOR, [21,11]):
            game_state.attempt_spawn(ENCRYPTOR, [21,11])

        """ Wall of DESTRUCTOR """
        destructorWall = [[18,11],[20,11],[22,11],[19,11],[6,11],[8,11],[10,11],[12,11],[14,11],[16,11]]

        for place in destructorWall:
            if game_state.can_spawn(DESTRUCTOR, place):
                game_state.attempt_spawn(DESTRUCTOR, place)

        """Extend the Wall"""

        for i in range(4,22,3):
            if game_state.can_spawn(DESTRUCTOR, [i,13]):
                game_state.attempt_spawn(DESTRUCTOR, [i,13])

        """Add ENCRYPTOR to the wall"""

        for i in range(8,22,3):
            if game_state.can_spawn(ENCRYPTOR, [i,13]):
                game_state.attempt_spawn(ENCRYPTOR, [i,13])

        





    def deploy_attackers(self, game_state):
        if game_state.get_resource(game_state.BITS) > 10:
            for i in range(10):
                game_state.attempt_spawn(EMP, [3,10])


    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
