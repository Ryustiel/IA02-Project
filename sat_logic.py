from typing import Dict
import launcher
import hitman

class Guesser:
    def __init__(self, map_info):
        infos_monde = {} # coords : type
        # uniquement la liste des états certains
        previous_dimacs = []
        remaining_guards = map_info['guard_count'] # integers
        remaining_civilians = map_info['civil_count']

    def run_solver(self, map_info: Dict):
        """
        génère la liste des états à partir des previous dimacs et des nouvelles infos
        appelle gophersat avec tout le délire
        """
        ...

    def choose_move_direction(self, map_info: Dict):
        """
        toutes les heuristiques qui guident le choix de l'action de hitman
        """
        ...

    def make_dimacs(map_info: Dict):
        ...

