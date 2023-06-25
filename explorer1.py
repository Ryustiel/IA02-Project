from testing2.hitman2 import *
import numpy as np
from utilities import *

MAX_VISION = 3 # en nombre de cases
BLOCKING = [HC.WALL, HC.GUARD_E, HC.GUARD_N, HC.GUARD_S, HC.GUARD_W]

class MazeUncoverer():
    """
    Contient une représentation du jeu limitée aux données que le joueur a.
    Peut trouver un chemin vers la première case à découvrir.
    """
    def __init__(self, internal, start_pos = (0, 0)):
        """
        initialise et sauvegarde la grille de jeu pour l'exploration
        """
        # TRACKING        
        self.history = [] # local history : les actions depuis le point jusqu'à l'arrivée
        self.penalties = 0

        self.internal = internal # internal grid
        self.n = len(internal)
        self.m = len(internal[0])
        self.pos = start_pos # grid_format
        self.orientation = HC.N

        # self.internal[start_pos] = HC.EMPTY

        # HEURISTIQUES
        self.last_rotation = None # previent des rotations successives qui s'annulent
        self.spam_rotation = 0 # previent les tours complets

    # INTERNAL REP

    def isDone(self):
        """
        vérifie si toute la grille a été découverte
        returns True if everything has been uncovered
        """
        test = np.all(self.internal != HC.UNKNOWN)
        if not test:
            # TESTER si les coins sont inatteignables aussi <==<==
            ... # update test here if inatteignables
        return test

    def foundUnknown(self, vision=None):
        """
        returns True si une inconnue est entré dans le champ de vision (faced)
        """
        if vision == None:
            vision = self.getVision()
            if vision is None:
                vision = [HC.WALL]
        if HC.UNKNOWN in vision:
            return True
        return False

    def getVision(self):
        """
        returns le type de case dans le champ de vision.
        (n'oublions pas que le champ de vision s'arrête à la première case)
        """
        offset = self.pos

        cases = [] # out of bounds option

        for i in range(3):
        
            # updating offset
            if self.orientation == HC.N:
                offset = (offset[0] - 1, offset[1])
            elif self.orientation == HC.S:
                offset = (offset[0] + 1, offset[1])
            elif self.orientation == HC.E:
                offset = (offset[0], offset[1] + 1) # est c'est vers la droite
            else:
                offset = (offset[0], offset[1] - 1)
            
            if (offset[0] >= 0 and offset[1] >= 0
                and offset[0] < self.n and offset[1] < self.m):

                case = self.internal[offset]
                cases.append(case)
                if case != HC.EMPTY: # if is empty case
                    break

            else:
                break

        if len(cases) == 0:
            return None
        return cases


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

            skip = False
            # 2 : autres objets bloquants (à part les gardes)
            for item in vision:
                if item in BLOCKING: # is otherwise walkable
                    skip = True
                    break
            if not skip:
                actions.append(AC.MOVE)

        return actions
    
    def perform(self, action):
        if action == AC.HORAIRE:
            if self.orientation == HC.N: self.orientation = HC.E
            elif self.orientation == HC.E: self.orientation = HC.S
            elif self.orientation == HC.S: self.orientation = HC.W
            elif self.orientation == HC.W: self.orientation = HC.N
        elif action == AC.ANTIHORAIRE:
            if self.orientation == HC.N: self.orientation = HC.W
            elif self.orientation == HC.W: self.orientation = HC.S
            elif self.orientation == HC.S: self.orientation = HC.E
            elif self.orientation == HC.E: self.orientation = HC.N
        elif action == AC.MOVE:
            # validité de l'action déjà vérifiée
            if self.orientation == HC.N: self.pos = (self.pos[0] - 1, self.pos[1])
            elif self.orientation == HC.S: self.pos = (self.pos[0] + 1, self.pos[1])
            elif self.orientation == HC.E: self.pos = (self.pos[0], self.pos[1] + 1)
            elif self.orientation == HC.W: self.pos = (self.pos[0], self.pos[1] - 1)

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