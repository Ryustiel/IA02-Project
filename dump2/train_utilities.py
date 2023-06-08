from typing import List, Dict
import numpy as np
import hitman.hitman as hitman
from generateur import get_random_maze, affichage
from enum import Enum

# TRAINING CONSTANTS

MAX_SIZE = 10
BITS_PER_CELL = 6
PENALTY_UNDISCOVERED = 15 # penalty when a tile has not been discovered

class DHC(Enum): # elements for AI discovery
    # compter par l'arrière pour l'encodage binaire
    # est une heuristique
    UNKNOWN = 30
    HEAR_PERS_1 = 29
    HEAR_PERS_2 = 28
    HEAR_PERS_3 = 27

class MazeRep():
    """
    Un conteneur pour matrice d'objets labyrinthe
    Le met à jour automatiquement avec les données apportées par
    * L'arbitre de jeu
    * La modélisation SAT

    permet d'afficher le labyrinthe, 
    de le convertir en une matrice int output pour le modèle,
    de lancer l'inférence SAT,
    et de mettre à jour le labyrinthe avec les différentes sources
    """
    def __init__(self, grid: List[List[hitman.HC]]=None, start_pos = (0, 0), max_size = MAX_SIZE):
        self.max_size = max_size
        self.is_done = False
        self.penalties = 0
        self.orientation = hitman.HC.N.value

        # faire la différence entre la vraie grille, 
        # la grille des indices (avec des murs fixés sur les zones hors jeu)
        # et la grille à passer à l'IA (grille à indices avec les bords)
        # Get the current maze dimensions

        self.grid = np.array(grid)

        current_width, current_height = self.grid.shape
        self.width = current_width
        self.height = current_height

        self.pos = self.grid_to_matrix(start_pos) # STORED AS PROF FORMAT

        # print("START POS", start_pos, "PASSED COORDS", self.pos, "GETPOS", self.get_pos(), "SHAPE", self.grid.shape)

        self.referee = hitman.HitmanReferee(
                world = self.grid, 
                pos = self.pos
                )

        self.discovered = np.full((self.width, self.height), DHC.UNKNOWN.value) # part de la grille découverte

        # self.grid is a record of the full maze state, for pretty printing
        # self.grid = np.pad(grid, ((0, max_size - self.width), (0, max_size - self.height)), constant_values=hitman.HC.WALL)
        
        # Pad the maze with the specified padding value (walls)
        # self.discovered is the internal, known state of the maze
        self.discovered = np.pad( 
            self.discovered,
            ((0, max_size - self.width), (0, max_size - self.height)),
            constant_values = (hitman.HC.WALL.value)
            )

    def get_pos(self):
        # returns the grid indice
        return self.matrix_to_grid(self.pos)
    
    def matrix_to_grid(self, pos):
        """
        this exists because our teacher decided to 
        index his arrays bottom to top
        """
        return self.width - 1 - pos[1], pos[0]

    def grid_to_matrix(self, indices):
        return indices[1], self.width - 1 - indices[0]
    
    def update_state(self, data: Dict):
        # mettre à jour le champ de vision par rapport à l'objet détecté en premier
        # vérifier si la pièce est fermée à tout moment
        
        # print(data['vision'], "\n", data['position'], data['orientation'], data['penalties'])
        
        self.penalties = int(data['penalties'])
        for pos, type in data['vision']:
            self.discovered[self.matrix_to_grid(pos)] = type.value
        self.pos = data['position']
        self.orientation = data['orientation'].value # hitman.HC.E (...)

        # print(data)

        if data['status'] != 'OK':
            self.is_done = True


    def check_enclosed_space(self):
        """
        vérifie si l'espace découvert est contigu, et transforme le reste en murs
        => pour les salles bizarres
        """
        ...


    def set_penalty_for_failing(self):
        self.penalties += PENALTY_UNDISCOVERED * np.sum(self.discovered > 20) # values that mean undiscovered
        
        # print("FOUND", np.sum(self.discovered > 20), "TOTAL", self.width * self.height)

    
    def max_penalty(self):
        # returns the maximum penalty value
        return self.width * self.height * (PENALTY_UNDISCOVERED) # guards + moving 

    def penalty_to_reward(self):
        bonus = self.max_penalty() - self.penalties
        return 0 if bonus < 0 else int(bonus) # floored to zero

    # MOST IMPORTANT METHOD =================================================================
    
    def step(self, action: int):
        if action == 0:
            status = self.referee.turn_anti_clockwise()
        elif action == 1:
            status = self.referee.turn_clockwise()
        else:
            status = self.referee.move()

        self.update_state(status)
        
        if self.is_done:
            self.set_penalty_for_failing()

        self.is_done


    def toINT(self) -> List[List[int]]: 
        # -> numpy array
        f = np.vectorize(lambda x: x.value)
        int_grid = f(self.getGrid())
        # int_grid[self.get_pos()] = DHC.PLAYER.value
        return int_grid
    
    def getEncoding(self):
        encoding = np.zeros((self.max_size, self.max_size, BITS_PER_CELL))

        pos = self.get_pos()

        for i in range(self.max_size):
            for j in range(self.max_size):
                # [is discovered, is wall, is guard, direction 1, direction 2, is_player]

                cell = self.discovered[i, j]

                # DHC.UNKNOWN.value: (0, 0, 0, 0, 0, 0)
                # hitman.HC.EMPTY.value: (1, 1, 0, 0, 0, 0)
                # DHC.PLAYER.value && HC.N: (1, 0, 0, 0, 0, 0)
                # HC.S = (1, 0, 0, 1, 1, 0); HC.W = (1, 0, 0, 0, 1, 0)
                # HC.E = (1, 0, 0, 1, 0, 0)
                
                if cell < 17: # is it discovered
                    encoding[i, j, 0] = 1

                if ( # is it walkable
                    cell == hitman.HC.WALL.value
                ):
                    encoding[i, j, 1] = 1

                if ( # is it a guard
                    (cell >= hitman.HC.GUARD_N.value and cell <= hitman.HC.GUARD_W.value)
                ):
                    encoding[i, j, 1] = 1
                    encoding[i, j, 2] = 1 # is guard

                if (cell >= 26 and cell < 30): # SPECIAL MARKINGS : potential guards
                    encoding[i, j, 2] = 1 # mais pas indice 1 : walkable

                if ( # south or east
                    cell == hitman.HC.GUARD_S
                    or cell == hitman.HC.GUARD_E
                ):
                    encoding[i, j, 3] = 1  
                
                if ( # south or west
                    cell == hitman.HC.GUARD_S
                    or cell == hitman.HC.GUARD_W
                ):
                    encoding[i, j, 4] = 1
                

                if (i, j) == pos: # if it's a player
                    encoding[i, j, 5] = 1
                    if self.orientation == hitman.HC.S or self.orientation == hitman.HC.E:
                        encoding[i, j, 3] = 1
                    if self.orientation == hitman.HC.S or self.orientation == hitman.HC.W:
                        encoding[i, j, 4] = 1

        return encoding



    def getResult(self):
        return self.grid[:self.size, :self.size]

    def getGrid(self):
        return self.grid

    def __str__(self):
        # gets the result grid and pretty prints

        # swaps the player location with a custom value for display
        player_pos_type = self.discovered[self.get_pos()]
        self.discovered[self.get_pos()] = 77
        s = str(self.discovered[0:self.width, 0:self.height])
        # s = str(self.discovered)
        self.discovered[self.get_pos()] = player_pos_type # puts the original value back
        return s + "\n"