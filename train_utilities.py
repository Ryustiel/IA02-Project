from typing import List, Dict
import numpy as np
import hitman.hitman as hitman
from generateur import get_random_maze, affichage
from enum import Enum

# TRAINING CONSTANTS

MAX_SIZE = 10
BITS_PER_CELL = 5 # bits per cell for the encoding
MAX_ITERATION = 30
PENALTY_UNDISCOVERED = 15 # penalty when a tile has not been discovered

class DHC(Enum): # elements for AI discovery
    # compter par l'arrière pour l'encodage binaire
    # est une heuristique
    PLAYER = 31
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
        self.has_failed = False
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
            self.has_failed = True

        
    def action_interface(self, code: int):
        if not self.has_failed:
            if code == 0:
                status = self.referee.turn_anti_clockwise()
            elif code == 1:
                status = self.referee.turn_clockwise()
            else:
                status = self.referee.move()

            self.update_state(status)

    def check_enclosed_space(self):
        """
        vérifie si l'espace découvert est contigu, et transforme le reste en murs
        => pour les salles bizarres
        """
        ...



    def get_penalty_for_missing(self):
        self.penalties += PENALTY_UNDISCOVERED * np.sum(self.discovered > 20) # values that mean undiscovered
        
        # print("FOUND", np.sum(self.discovered > 20), "TOTAL", self.width * self.height)

    def not_yet_complete(self) -> bool:
        return np.any(self.discovered > 20)
    
    def max_penalty(self):
        # returns the maximum penalty value
        return self.width * self.height * (PENALTY_UNDISCOVERED) # guards + moving 


    # MOST IMPORTANT METHOD =================================================================

    def evaluate(self, net): # -> (isWon[bool], score[int]=None)
        # net is a randomly generated net that should be able to play the game
        # échec = 2 * 5 * grid_size squared
        # lorsqu'echec, -10 par case non découverte
        
        i = 0

        while self.not_yet_complete():
            i += 1 # counting loop iterations

            input_data = self.getEncoding()

            output = net.activate(input_data) # besoin que de 2 output

            print(output, end=" ")

            if output[0] > 0:
                status = self.referee.move()
            else:
                if output[1] > 0:
                    status = self.referee.turn_anti_clockwise()
                else:
                    status = self.referee.turn_clockwise()

            self.update_state(status)

            # print(self)
        
            if i > MAX_ITERATION or self.has_failed:
                self.get_penalty_for_missing()
                break

        bonus = self.max_penalty() - self.penalties
        return 0 if bonus < 0 else int(bonus) # floored to zero



    def toINT(self) -> List[List[int]]: 
        # -> numpy array
        f = np.vectorize(lambda x: x.value)
        int_grid = f(self.getGrid())
        # int_grid[self.get_pos()] = DHC.PLAYER.value
        return int_grid


    def encode_cell(self, cell):
        # binary_code = format(cell, f"0{BITS_PER_CELL}b")
        # bits = [int(bit) for bit in binary_code]
        # return bits

        # [is undiscovered, is wall, is guard, direction 1, direction 2]

        if cell == DHC.UNKNOWN.value: # undiscovered
            return [0, 0, 0, 0, 0] # TEMPORARY
        elif cell == hitman.HC.EMPTY.value: # wall
            return [1, 1, 0, 0, 0]
        
        elif cell == DHC.PLAYER.value: # player
            if self.orientation == hitman.HC.N.value:
                return [1, 0, 0, 0, 0] # direction the player is facing
            elif self.orientation == hitman.HC.E.value:
                return [1, 0, 0, 1, 0]
            elif self.orientation == hitman.HC.W.value:
                return [1, 0, 0, 0, 1]
            elif self.orientation == hitman.HC.S.value:
                return [1, 0, 0, 1, 1]
        
        elif cell >= 26: # SPECIAL MARKINGS
            return [0, 0, 1, 0, 0]
        
        # guards
        elif cell == hitman.HC.GUARD_N.value:
            return [1, 1, 1, 0, 0]
        elif cell == hitman.HC.GUARD_E.value:
            return [1, 1, 1, 1, 0]
        elif cell == hitman.HC.GUARD_W.value:
            return [1, 1, 1, 0, 1]
        elif cell == hitman.HC.GUARD_S.value:
            return [1, 1, 1, 1, 1]
        
        else:
            return [1, 0, 0, 0, 0] # walkable
        

    def getEncoding(self):
        CELL_LEN = 5

        # Create an empty array with shape (grid_shape[0], grid_shape[1], num_objects)
        encoded_array = np.empty(self.max_size**2 * CELL_LEN + CELL_LEN, dtype=int)
        
        # Get the object the player is standing on
        player_pos_type = self.discovered[self.get_pos()]
        self.discovered[self.get_pos()] = DHC.PLAYER.value # assigns the player to this location
        pos_type_binary = self.encode_cell(player_pos_type)
        
        # print(pos_type_binary, len(pos_type_binary))
        
        encoded_array[0 : BITS_PER_CELL] = pos_type_binary # stores the object at the beginning of the encoded array


        index = CELL_LEN # because the first 5 bits are
        # dedicated to the player's standing position

        # Iterate over each cell in the maze
        for i in range(self.max_size):
            for j in range(self.max_size):
                bits = self.encode_cell(self.discovered[i, j])
                encoded_array[index:index + BITS_PER_CELL] = bits
                index += BITS_PER_CELL # increment to next position for the next grid slot

        # swaps back the object on the player position
        self.discovered[self.get_pos()] = player_pos_type

        return encoded_array


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