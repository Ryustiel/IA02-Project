from solve import *

#grid = [[0]]
#while len(grid) < 22 or len(grid[0]) < 12:
grid, starting = get_random_maze(max_size = 25)

from examples import giant_grid
grid, starting = giant_grid, (21, 0)

#grid, starting = world_example, (5, 0)

result, ellapsed = solve(grid, starting)

# et là il va falloir utiliser les instructions, tester le tout
print("================= RESULTS =================")
print(result.penalties)
print(len(result.history), result.history[0:10], end="\n\n")

origin = grid_to_matrix(starting, len(grid))
# tryout(result.history, grid, origin)
penalties = calculate_penalties(result.history, grid, origin)

print(f"solution found in {ellapsed}, ends up with {penalties} penalties")