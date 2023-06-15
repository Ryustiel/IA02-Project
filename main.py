from solve import *

#grid = [[0]]
#while len(grid) < 22 or len(grid[0]) < 12:
grid, starting = get_random_maze(max_size = 25)

from examples import giant_grid
grid, starting = giant_grid, (21, 0)

result = solve(grid, starting)

# et là il va falloir utiliser les instructions, tester le tout
print("================= RESULTS =================")
print(result.penalties)
print(len(result.history), result.history[0:10])

tryout(result.history, grid, origin = grid_to_matrix(starting, len(grid)))
print(starting)