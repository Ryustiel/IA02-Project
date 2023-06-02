from typing import List
import numpy as np
import hitman.hitman as hitman

# CONSTANTS

MAX_SIZE = 10

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
    def __init__(self, grid: List[List[hitman.HC]], wall_value: int, size: int, max_size = MAX_SIZE):
        # Get the current maze dimensions
        grid = np.array(grid)
        current_height, current_width = grid.shape

        # Pad the maze with the specified padding value
        self.grid = np.pad(grid, ((0, max_size), (0, max_size)), constant_values=wall_value)
        self.max_size = max_size
        self.size = size

        super().__init__(grid)

    def toINT(self) -> List[List[int]]:
        # -> numpy array
        f = np.vectorize(lambda x: x.value)
        int_grid = f(self.getGrid())
        int_grid[self.get_pos()] = 0
        return int_grid

    def getResult(self):
        return self.grid[:self.size, :self.size]

    def getGrid(self):
        return self.grid
    
    def __str__(self):
        # gets the result grid and pretty prints
        ...

def get_random_training_maze():
    """
    generates a random training maze
    as an integer matrix
    """
    ...

def evaluate_score(): # -> (isWon[bool], score[int]=None)
    ...
    # échec = 2 * 5 * grid_size squared

def is_goal_state():
    ...

def update_maze_state():
    ...


init_grid = [
    [hitman.HC.EMPTY, hitman.HC.EMPTY, hitman.HC.EMPTY],
    [hitman.HC.EMPTY, hitman.HC.WALL, hitman.HC.EMPTY],
    [hitman.HC.EMPTY, hitman.HC.WALL, hitman.HC.WALL]
]
m = MazeRep(init_grid, wall_value=hitman.HC.WALL, size=3)

print("hi")

print(m.toINT(), end="\n\n")
# print(m.getGrid(), end="\n\n")