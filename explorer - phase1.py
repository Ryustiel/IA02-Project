from testing2.hitman2 import *
import numpy as np
from generateur import get_random_maze, affichage
from copy import copy, deepcopy
from collections import deque
from utilities import *
from collections import Enum

class HCL(HC):
    UNKNOWN = 99 # very high value

MAX_VISION = 3 # en nombre de cases
BLOCKING = [HCL.WALL, HCL.GUARD_E, HCL.GUARD_N, HCL.GUARD_S, HCL.GUARD_W]
UNKNOWN = [HCL.UNKNOWN]

class MazeUncoverer():
    """
    Contient une représentation du jeu limitée aux données que le joueur a.
    Peut trouver un chemin vers la première case à découvrir.
    """
    def __init__(self, n, m, start_pos = (0, 0)):
        """
        initialise et sauvegarde la grille de jeu pour l'exploration
        """
        # TRACKING        
        self.history = [] # local history : les actions depuis le point jusqu'à l'arrivée
        self.penalties = 0

        self.interal = np.full((n, m), HCL.UNKNOWN) # internal grid
        self.n = n
        self.m = m
        self.pos = start_pos # grid_format
        self.orientation = AC.N

        self.internal[start_pos] = HCL.EMPTY

        # HEURISTIQUES
        self.last_rotation = None # previent des rotations successives qui s'annulent
        self.spam_rotation = 0 # previent les tours complets

    # INTERNAL REP

    def isFullyDone(self):
        """
        vérifie si toute la grille a été découverte
        returns True if everything has been uncovered
        """
        test = np.all(self.internal not in UNKNOWN)
        if not test:
            # TESTER si les coins sont inatteignables aussi <==<==
            ... # update test here if inatteignables
        return test

    def isDone(self):
        """
        returns True si une inconnue est entré dans le champ de vision (faced)
        """
        if self.getVision() is not None:
            if self.getVision() == HCL.UNKNOWN:
                return True
        return False

    def getVision(self):
        """
        returns le type de case dans le champ de vision.
        (n'oublions pas que le champ de vision s'arrête à la première case)
        """
        offset = self.pos

        case = HC.WALL # out of bounds option

        for i in range(3):
        
            # updating offset
            if self.orientation == HC.N:
                offset[0] += 1
            elif self.oriantation == HC.S:
                offset[0] -= 1
            elif self.orientation == HC.E:
                offset[1] += 1 # est c'est vers la droite
            else:
                offset[1] -= 1
            
            if (offset[0] >= 0 and offset[1] >= 0
                and offset[0] < self.n and offset[1] < self.m):

                case = self.internal(offset)
                if case != HC.EMPTY: # if is empty case
                    return case

            else: break

        return case


    def updatePenalties(self):
        """
        augmente la pénalité en fonction de l'état du joueur :
        * check si il est vu par un garde
        * incrémente suite au déplacement
        """
        self.penalties += 1
        ... # is in guard range ?

    def updateFromStatus(self, status):
        """
        updates the matrix from the status
        """
        # récupère la vision et l'intègre à la grille en checkant si ce n'est pas
        # déjà dedans
        ...

    def updateFromSAT(self):
        ...

    # GETTERS

    def getHistory(self):
        return self.history

    def getActions(self):
        """
        renvoie l'espace des actions possibles (objets AC)

        utilise la grille locale pour déterminer les actions : 
        * il n'est pas possible de sortir de la grille
        * il n'est pas possible de marcher sur une case inconnue ou sur un garde
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

        vision = self.getVision()
        # + self.pos

        if vision is not None: # not out of bounds

            # 2 : autres objets bloquants (à part les gardes)
            if vision not in BLOCKING: # is otherwise walkable
                actions.append(AC.MOVE)

        # toujours actif à partir de costume récupéré jusqu'à costume enfilé
        
        #if self.status['has_suit'] and not self.status['is_suit_on']:
        #    actions.append(AC.ENFILER)

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

        self.perform(action)
        self.updatePenalties()
        # répéter ça
        # then run hitman using the new history 
        # et finalement faire updateFromStatus avec la sortie vision de hitman