from testing2.hitman2 import *
import numpy as np
from generateur import get_random_maze, affichage
from enum import Enum
from copy import copy, deepcopy
from collections import deque

MAX_SIZE = 10

class AC(Enum):
    HORAIRE = 0
    ANTIHORAIRE = 1
    MOVE = 2
    KILL = 3
    GARDE = 4
    CIVIL = 5
    ENFILER = 6
    COSTUME = 7
    ARME = 8

# modéliser les actions à prendre, évaluer l'état du jeu, rechercher un maximum

# on va représenter le jeu sous la forme d'une liste d'états
# position du joueur, cases déjà visitées, cases visitables
# on veut juste une arborescence d'actions à prendre
# donc la question est : à un instant T : qu'est ce qui est possible ?
# on fait un branchement de l'arbre par action prise
# on grise les cases déjà empruntées, on empêche... => get actions !

# on va faire une recherche en largeur,
# et d'abord on va rechercher dans les branches où le
# score instantané est meilleur

# POSSIBILITE DE LIBERER L'INSTANCE DU LABYRINTHE UNE FOIS TOUS LES FILS GENERES
# mais l'impact sur la mémoire est à évaluer, ptet que y'en a pas besoin

# TO DO
# récupérer _Parent__pos mais ajouter un test au début du programme, 
# dans le main, pour vérifier que les dites valeurs sont toujours rendues accessibles
# par le prof, en cas de pépin, just to make sure

class MazeExplorer(HitmanReferee):
    def __init__(self, grid: List[List[HC]] = None, start_pos = (0, 0), depth = 0):
        """
        initialise et sauvegarde la grille de jeu pour l'exploration
        """
        if isinstance(grid, List):
            grid = np.array(grid)

        super().__init__()

        # GAME
        self._HitmanReferee__world = grid
        self._HitmanReferee__m = grid.shape[0]
        self._HitmanReferee__n = grid.shape[1]
        self._HitmanReferee__civil_count = self._HitmanReferee__compute_civil_count()
        self._HitmanReferee__guard_count = self._HitmanReferee__compute_guard_count()
        self._HitmanReferee__civils = self._HitmanReferee__compute_civils()
        self._HitmanReferee__guards = self._HitmanReferee__compute_guards()

        self.origin = self.grid_to_matrix(start_pos) # stored in PROF format, just like pos

        self.start_phase2() # running initialization
        self._HitmanReferee__pos = self.origin # setting custom position again
        self._HitmanReferee__seen_by_guard_num()
        self._HitmanReferee__seen_by_civil_num()

        # HEURISTIQUES
        self.last_rotation = None # previent des rotations successives qui s'annulent
        self.spam_rotation = 0 # previent les tours complets
        self.accessibility_matrix = self.makeAccessibilityMatrix(grid)

    # UTILITY

    def grid_to_matrix(self, indices):
        return indices[1], self._HitmanReferee__m - 1 - indices[0]
    
    def matrix_to_grid(self, pos):
        """
        this exists because our teacher decided to 
        index his arrays from the bottom to the top
        """
        return self._HitmanReferee__m - 1 - pos[1], pos[0]

    # GETTERS

    def hasWon(self):
        # target killed + back to the starting location
        if (
            self._HitmanReferee__is_target_down 
            and self._HitmanReferee__pos == self.origin
        ):
            return True
        return False

    def getPos(self):
        """
        renvoie la position au format grille
        """
        # returns the grid indice
        return self.matrix_to_grid(self._HitmanReferee__pos)

    def getScore(self):
        return self._HitmanReferee__phase2_penalties

    def getHistory(self):
        return self._HitmanReferee__phase2_history
    
    def getState(self):
        """
        renvoie un tuple qui représente l'état de cette instance
        pour comparer l'équivalence avec d'autres instances.
        """
        return (
            self._HitmanReferee__orientation,
            self._HitmanReferee__has_suit, 
            self._HitmanReferee__suit_on, 
            self._HitmanReferee__has_weapon, 
            self._HitmanReferee__is_target_down
        )

    # HEURISTIQUES COMPELXES

    def makeAccessibilityMatrix(self, grid):
        accessibility = np.zeros(grid.shape, dtype=np.int8)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if grid[i][j] in [HC.WALL, HC.GUARD_E, HC.GUARD_N, HC.GUARD_S, HC.GUARD_W]:
                    accessibility[i][j] = 2 # forbidden
                else:
                    accessibility[i][j] = 0 # accessible
        return accessibility
        # 1 is penalized : pénalité unique qui disparaît si on marche dessus

    def heuristiqueBackstep(self):
        # contrôle les aires qui nécessitent
        # un backstep pour les atteindre
        # trouve qu'il faut un backstep ssi un case
        # importante se retrouve dans une zone que
        # l'IA ne peut atteindre qu'en revenant sur ses pas
        # en faisant ça, 

        pos = self.getPos()
        # obtenir toutes les tiles à côté

        # trouver une region contigue autours du joueur
        traite = deepcopy(self.accessibility_matrix)
        traitement = [self.getPos()] # tuples de position

        while len(traitement) > 0: 
            
            ... # NOT IMPLEMENTED

        ...

    def getActions(self):
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

        # 4 : en fonction de ce qui est directement en face de soi

        vision = self._HitmanReferee__get_vision()
        pos = self.getPos()

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

        # 3 : case sur laquelle on se tient

        walking_on = self._HitmanReferee__world[pos[0]][pos[1]]
        if walking_on == HC.PIANO_WIRE:
            if not self._HitmanReferee__has_weapon: # assuming we arn't changing the grid state
                actions.append(AC.ARME)
        elif walking_on == HC.SUIT:
            if not self._HitmanReferee__has_suit:
                actions.append(AC.COSTUME)

        elif walking_on == HC.TARGET:
            if self._HitmanReferee__has_weapon:
                actions.append(AC.KILL)

        # 5 : toujours actif entre : costume récupéré et costume enfilé
        
        if self._HitmanReferee__has_suit and not self._HitmanReferee__suit_on:
            actions.append(AC.ENFILER)

        return actions

    def branch(self, action: AC) -> Tuple[int, bool]: # -> MazeRep(), score
        """
        Applique l'action sélectionnée au jeu, 
        renvoie le score atteint (int) et l'état de victoire (bool)
        """
        # faire un dupliqué, puis appeler branch, et récupérer la branche...
        # self._HitmanReferee__phase2_penalties += 1 # adding penalty for performing an action

        if action == AC.MOVE:
            self.move()
            self.spam_rotation = 0
            self.last_rotation = None # slaloming
        
        elif action == AC.HORAIRE:
            self.turn_clockwise()
            self.last_rotation = True
            self.spam_rotation += 1

        elif action == AC.ANTIHORAIRE:
            self.turn_anti_clockwise()
            self.last_rotation = False
            self.spam_rotation -= 1

        elif action == AC.ARME:
            self.take_weapon()
            self._HitmanReferee__phase2_penalties -= 10 # make it dependant on the maze's width

        elif action == AC.CIVIL: 
            self.neutralize_civil()
            self.last_rotation = None # rotating just for acting on a guard is allowed

        elif action == AC.GARDE: 
            self.neutralize_guard()
            self.last_rotation = None

        elif action == AC.COSTUME:
            self.take_suit()

        elif action == AC.ENFILER:
            self.put_on_suit()
            # this is not reseting rotation

        elif action == AC.KILL:
            self._HitmanReferee__phase2_penalties -= 10
            self.kill_target()

        # TO DO : wrapper l'erreur dans status...

        return self.getScore(), self.hasWon()
    
    def __str__(self):
        return affichage(np.array(self._HitmanReferee__world), self.getPos())
