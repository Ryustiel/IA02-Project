from typing import List, Dict
import numpy as np
import hitman.hitman as hitman
from generateur import get_random_maze, affichage
from enum import Enum

# TRAINING CONSTANTS

MAX_SIZE = 10
MAX_BITS = 5 # bits per cell for the encoding

class DHC(Enum): # elements for AI discovery
    # compter par l'arrière pour l'encodage binaire
    # est une heuristique
    PLAYER = 31
    UNKNOWN = 30
    HEAR_PERS_1 = 29
    HEAR_PERS_2 = 28
    HEAR_PERS_3 = 27

class MazeRep(hitman.HitmanReferee):
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

        # faire la différence entre la vraie grille, 
        # la grille des indices (avec des murs fixés sur les zones hors jeu)
        # et la grille à passer à l'IA (grille à indices avec les bords)

        if grid is None:
            grid, self.width, self.height, new_pos = get_random_maze(max_size=MAX_SIZE)
            super().__init__(world = grid)
            self._pos = new_pos
        else:
            # Get the current maze dimensions
            grid = np.array(grid)
            current_height, current_width = grid.shape

            self.width = current_width
            self.height = current_height

            super().__init__(world = grid)
            self._pos = start_pos
        
        self.discovered = np.full((self.width, self.height), DHC.UNKNOWN.value) # part de la grille découverte

        # Pad the maze with the specified padding value
        self.grid = np.pad(grid, ((0, max_size - self.width), (0, max_size - self.height)), constant_values=hitman.HC.WALL)
        self.discovered = np.pad(
            self.discovered,
            ((0, max_size - self.width), (0, max_size - self.height)),
            constant_values = (hitman.HC.WALL.value)
            )

        # self.discovered[self.get_pos()] = DHC.PLAYER.value

    def get_pos(self):
        return self._pos

    def update_state(self, data: Dict):
        # mettre à jour le champ de vision par rapport à l'objet détecté en premier
        # vérifier si la pièce est fermée à tout moment
        print(data['vision'])
        for pos, type in data['vision']:
            self.discovered[pos] = type.value

        
    def action_interface(self, code: int):
        if code == 0:
            status = self.turn_anti_clockwise()
        elif code == 1:
            status = self.turn_clockwise()
        else:
            status = self.move()

        self.update_state(status)

    def check_enclosed_space(self):
        """
        vérifie si l'espace découvert est contigu, et transforme le reste en murs
        """
        ...

    def set_random_training_maze(self):
        """
        generates a random training maze
        as an integer matrix
        """
        ...

    def evaluate_score(self, net): # -> (isWon[bool], score[int]=None)
        # net is a randomly generated net that should be able to play the game
        # échec = 2 * 5 * grid_size squared
        ...

    def toINT(self) -> List[List[int]]: 
        # -> numpy array
        f = np.vectorize(lambda x: x.value)
        int_grid = f(self.getGrid())
        # int_grid[self.get_pos()] = DHC.PLAYER.value
        return int_grid[0:self.width, 0:self.height]
    
    def getEncoding(self):
        max_bits = MAX_BITS
        max_integer = 2**MAX_BITS - 1  # Number of possible object types (0 to 31 is the default)
        
        # Create an empty array with shape (grid_shape[0], grid_shape[1], num_objects)
        encoded_array = np.empty(self.max_size**2 * max_bits + max_bits, dtype=int)
        
        # Get the object the player is standing on
        player_pos_type = self.discovered[self.get_pos()]
        self.discovered[self.get_pos()] = DHC.PLAYER.value # assigns the player to this location
        pos_type_binary = format(player_pos_type, f"0{max_bits}b")
        pos_type_binary = [int(bit) for bit in pos_type_binary]
        print(pos_type_binary, len(pos_type_binary))
        encoded_array[0 : max_bits] = pos_type_binary # stores the object at the beginning of the encoded array


        index = max_bits # because the first 5 bits are
        # dedicated to the player's standing position

        # Iterate over each cell in the maze
        for i in range(self.max_size):
            for j in range(self.max_size):
                binary_code = format(self.discovered[i, j], f"0{max_bits}b")
                bits = [int(bit) for bit in binary_code]
                encoded_array[index:index + max_bits] = bits
                index += max_bits # increment to next position for the next grid slot


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
        self.discovered[self.get_pos()] = player_pos_type # puts the original value back
        return s + "\n"


init_grid = [
    [hitman.HC.EMPTY, hitman.HC.EMPTY, hitman.HC.EMPTY],
    [hitman.HC.EMPTY, hitman.HC.WALL, hitman.HC.EMPTY],
    [hitman.HC.EMPTY, hitman.HC.WALL, hitman.HC.WALL]
]
m1 = MazeRep(init_grid, start_pos = (0, 0))
m = MazeRep()

print(m.toINT(), end="\n\n")
print(m)
m.action_interface(1)
print(m)
m.action_interface(1)
print(m)
# print(m.getGrid(), end="\n\n")