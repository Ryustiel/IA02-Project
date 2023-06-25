from explorer1 import *
from generateur import affichage
from solve import *
from utilities import *
from testing2.hitman2 import world_example

grid = world_example
knowledge = np.full((len(grid), len(grid[0])), HC.UNKNOWN)

for i in range(6):
    for j in range(7):
        if (i, j) != (2, 2):
            knowledge[i, j] = world_example[i][j]

origin = (0, 0)

# Le referee doit exister à l'extérieur de solve (multiphases)
# Referee a été modifié pour accepter des cartes customisées faute
# d'implémentation appropriée à la base
referee = HitmanReferee(world_example, matrix_to_grid(origin, len(knowledge)))

#result, history, penalties, ellapsed_time = solve_phase1(referee, knowledge, origin)
# mettre la génération de MazeUncoverer et faire la recherche normalement

result, ellapsed_time = find_path(knowledge, origin)
a = affichage(knowledge, matrix_to_grid(origin, len(knowledge)))
print(a)
print(origin, result.history)
# using result : end_phase1 and check penalties
#print(penalties)