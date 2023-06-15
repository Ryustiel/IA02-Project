from solve import *

grid, starting = get_random_maze(max_size = 20)

grid = [[HC.WALL, HC.WALL, HC.WALL, HC.EMPTY, HC.EMPTY,
  HC.PIANO_WIRE, HC.WALL, HC.EMPTY, HC.WALL,
  HC.WALL, HC.WALL, HC.EMPTY],
 [HC.WALL, HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.EMPTY,
  HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.WALL, HC.WALL,
  HC.EMPTY, HC.EMPTY],
 [HC.WALL, HC.WALL, HC.EMPTY, HC.GUARD_W, HC.GUARD_S,
  HC.EMPTY, HC.GUARD_E, HC.EMPTY, HC.EMPTY, HC.WALL,
  HC.EMPTY, HC.EMPTY],
 [HC.EMPTY, HC.EMPTY, HC.WALL, HC.EMPTY, HC.EMPTY,
  HC.CIVIL_S, HC.EMPTY, HC.EMPTY, HC.EMPTY,
  HC.CIVIL_E, HC.EMPTY, HC.EMPTY],
 [HC.EMPTY, HC.GUARD_W, HC.WALL, HC.EMPTY, HC.CIVIL_E,
  HC.EMPTY, HC.SUIT, HC.EMPTY, HC.EMPTY, HC.EMPTY,
  HC.WALL, HC.EMPTY],
 [HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.TARGET,
  HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.EMPTY, HC.EMPTY,
  HC.EMPTY, HC.EMPTY]]

starting = (0, 3)


grid, starting = world_example, (5, 0)
#handmade_solution()


res = solve(grid, starting)

# et là il va falloir utiliser les instructions, tester le tout
print("================= RESULTS =================")
print(res)
print(res.getScore())
print("WINSTATE", res.hasWon(), "HISTORY", len(res.getHistory()))
h = res.getHistory()
print(len(h), h[0:10])

ref = MazeExplorer(grid, starting)
print(ref)
for instruction in res.getHistory():
    print(ref.getActions())
    print(instruction)
    ref.branch(instruction)
    print(ref)
    print(ref.getState())
    print(ref.hasWon(), "\n", ref.getScore(), "\n\n")