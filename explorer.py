from testing2.hitman2 import *
import numpy as np
from generateur import get_random_maze, affichage
from copy import copy, deepcopy
from collections import deque
from utilities import *

MAX_SIZE = 10

# modéliser les actions à prendre, évaluer l'état du jeu, rechercher un maximum

# on va représenter le jeu sous la forme d'une liste d'états
# position du joueur, cases déjà visitées, cases visitables
# on veut juste une arborescence d'actions à prendre
# donc la question est : à un instant T : qu'est ce qui est possible ?
# on fait un branchement de l'arbre par action prise
# on grise les cases déjà empruntées, on empêche... => get actions !

class MazeExplorer():
    def __init__(self, referee, start_pos = (0, 0)):
        """
        initialise et sauvegarde la grille de jeu pour l'exploration
        """
        # TRACKING        
        self.history = []
        self.penalties = None
        self.referee = referee

        # HEURISTIQUES
        self.last_rotation = None # previent des rotations successives qui s'annulent
        self.spam_rotation = 0 # previent les tours complets

    # GETTERS

    def getHistory(self):
        return self.history

    def getActions(self, status, standing_on):
        """
        renvoie l'espace des actions possibles (objets AC)
        """
        # 0, 1 : sont quasi toujours disponibles
        if self.spam_rotation > 1 or self.spam_rotation < -1: # non disponibles si deux fois consécutifs
            self.spam_rotation = 0
            actions = [] # ne pas tourner trop de fois
        elif self.last_rotation is None:
            actions = [AC.HORAIRE, AC.ANTIHORAIRE]
        elif self.last_rotation: # evite gauche-droite droite-gauche
            actions = [AC.HORAIRE]
        else:
            actions = [AC.ANTIHORAIRE]

        # est en fonction de ce qui est directement en face de soi

        vision = status['vision']
        pos = status['position']

        if len(vision) > 0: # if vision is empty
            object = vision[0][1] # vision = List[Tuple[(pos, object)]]

            if object in [HC.GUARD_E, HC.GUARD_N, HC.GUARD_W, HC.GUARD_S]:
                actions.append(AC.GARDE)

            elif object in [HC.CIVIL_E, HC.CIVIL_N, HC.CIVIL_W, HC.CIVIL_S]:
                actions.append
                actions.append(AC.CIVIL)

            # 2 : autres objets bloquants (à part les gardes)
            elif object != HC.WALL: # is otherwise walkable
                actions.append(AC.MOVE)

        # dépend de la case sur laquelle on se tient

        if standing_on == HC.PIANO_WIRE:
            if not status['has_weapon']: # assuming we arn't changing the grid state
                actions.append(AC.ARME)
        elif standing_on == HC.SUIT:
            if not status['has_suit']:
                actions.append(AC.COSTUME)

        elif standing_on == HC.TARGET:
            if status['has_weapon']:
                actions.append(AC.KILL)

        # toujours actif à partir de costume récupéré jusqu'à costume enfilé
        
        if status['has_suit'] and not status['is_suit_on']:
            actions.append(AC.ENFILER)

        return actions

    def branch(self, action: AC): # ret status, bool
        """
        Applique l'action sélectionnée au jeu, 
        renvoie le score atteint (int) et l'état de victoire (bool)
        """
        # faire un dupliqué, puis appeler branch, et récupérer la branche...
        self.history.append(action)

        # interacting with an object on self pos is not resetting last_rotation
        if action == AC.MOVE:
            self.spam_rotation = 0
            self.last_rotation = None # slaloming allowed
        
        elif action == AC.HORAIRE:
            self.last_rotation = True
            self.spam_rotation += 1

        elif action == AC.ANTIHORAIRE:
            self.last_rotation = False
            self.spam_rotation -= 1

        elif action == AC.CIVIL: 
            self.last_rotation = None # rotating just for acting on a guard is allowed

        elif action == AC.GARDE:
            self.last_rotation = None

        status = perform(self.referee, action)

        # TO DO : wrapper l'erreur dans status...

        self.penalties = status['penalties']
        return status