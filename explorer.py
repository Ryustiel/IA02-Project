from testing2.hitman2 import *
import numpy as np
from generateur import get_random_maze, affichage
from enum import Enum

MAX_SIZE = 10

class AC(Enum):
    HORAIRE = 0
    ANTIHORAIRE = 1
    MOVE = 2
    KILL = 3
    GARDE = 4
    CIVIL = 5
    PASSER = 6
    PRENDRE = 7
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

class MazeExplorer():
    def __init__(self, grid: List[List[HC]]=None, start_pos = (0, 0)):
        """
        initialise et sauvegarde la grille de jeu pour l'exploration
        """
        # TECHNIQUE
        self.grid = np.array(grid) # plutot utiliser une variable globale !
        self.game = HitmanReferee(grid, start_pos) # instead, loads the FILE
        self.penalty = 0 # pénalité relative
        self.depth = 0 # profondeur de l'arbre

        # HEURISTIQUE
        self.last_rotation = None
        self.spam_rotation = 0

        current_width, current_height = self.grid.shape
        self.width = current_width
        self.height = current_height

        self.pos = self.grid_to_matrix(start_pos) # STORED AS PROF FORMAT

    def grid_to_matrix(self, indices):
        return indices[1], self.width - 1 - indices[0]
    
    def getPos(self):
        # returns the grid indice
        return self.matrix_to_grid(self.pos)
    
    def matrix_to_grid(self, pos):
        """
        this exists because our teacher decided to 
        index his arrays from the bottom to the top
        """
        return self.width - 1 - pos[1], pos[0]

    def getActions(self):
        """
        renvoie l'espace des actions possibles

        0 : tourne horaire; 1 : anti horaire; 2 : move; 3 : tuer_cible; 4 : neutraliser_garde
        (4) 5 : neutraliser civil; (3) 6 : récup costume; (3) 7 : prendre arme; 
        (5) 8 : passer costume
        """
        # 0, 1 : sont quasi toujours disponibles
        if self.spam_rotation > 3:
            self.spam_rotation = 0
            actions = [] # ne pas tourner trop de fois
        elif self.last_rotation is None:
            actions = [AC.HORAIRE, AC.ANTIHORAIRE]
        elif self.last_rotation: # evite gauche-droite droite-gauche
            actions = [AC.HORAIRE]
        else:
            actions = [AC.ANTIHORAIRE]

        # 2 seulement si il n'y a pas de mur
        # 4 : en fonction de ce qui est directement en face de soi

        if self.wall_conditions():
            actions.append(AC.WALL)




        # 5 : toujours actif entre : costume récupéré et costume enfilé
        

        # 3 : case sur laquelle on se tient
        

        ...
        
    def getScore(self):
        # points de score ajoutés :
        # petit bonus sur récupération du costume en fonction du nombre de gardes
        # petite pénalité pour chaque moment passé sans tuer la victime
        # => pas de pénalité parce que ça dépend directement de la longueur de l'arbre
        # de toutes façons on ne revient pas sur ses pas

        # calcul un score relatif au score qui précède l'action
        ...

    def branch(self, action: AC): # -> MazeRep(), score
        """
        renvoie une copie de cet objet, avec le nouvel état du jeu, et un score
        Met à jour la nouvelle grille : current position = -1
        """
        if action == AC.MOVE:
            status = self.game.move()
        # lister plus d'actions

        # wrapper l'erreur dans status...

        penalties = status['penalties']

        # faire un dupliqué, puis appeler branch, et récupérer la branche...
        return self, self.getScore(penalties)
    
    def __str__(self):
        return affichage(self.grid, self.getPos())



grid, starting = get_random_maze(max_size = MAX_SIZE)
m = MazeExplorer(grid, starting)

print(m)
print(m.getActions())

m, score = m.branch(1)
print(score)
print(m)

# à chaque étape de l'algorithme : 
# 1. récupérer les actions possibles,
# 2. faire un parcours vers une profondeur +1 en récupérant et en
# stockant les objets de représentation du jeu / étapes
# 3. obtenir les scores et décider quelles branches il faut mettre en
# tête de file, et quelles branche mettre à la fin