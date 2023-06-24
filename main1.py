from explorer1 import *
from generateur import affichage
from solve import *
from testing2.hitman2 import world_example

grid = world_example
knowledge = np.full((len(grid), len(grid[0])), HC.UNKNOWN)

for i in range(3):
    for j in range(3):
        knowledge[i, j] = world_example[i][j]

m = MazeUncoverer(knowledge, (0, 0))
#print(m.getActions())
#m.branch(AC.HORAIRE)
#m.branch(AC.HORAIRE)

m = find_path(knowledge, (0, 0))
# mettre la génération de MazeUncoverer et faire la recherche normalement

a = affichage(m.internal, m.pos)
print(a)
print(m.getActions())
print(m.penalties)
