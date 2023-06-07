from hitman.hitman import HC, HitmanReferee, complete_map_example, world_example
from pprint import pprint
from train_utilities import MazeRep, MAX_SIZE
from generateur import get_random_maze

def main():
    #m = MazeRep(world_example, start_pos = (0, 0))

    grid, start_pos = get_random_maze(max_size=10)

    m = MazeRep(grid, start_pos)

    print("\nINTERNAL\n", m.toINT(), end="\n\n")

    class Net():
        """
        deterministic net for testing purposes
        """
        def __init__(self): 
            self.state = 0
            self.actions = [
                [0, 1],
                [0, 0],
                [1, 0]
            ]

        def activate(self, input):
            if self.state >= len(self.actions):
                return [0, 0]
            else:
                self.state += 1
                return self.actions[self.state - 1]
    
    #p = m.evaluate(Net())
    #print(p)
    m.action_interface(1)
    print(m)

    enc = m.getEncoding()
    # print(enc)
    print(len(enc)) # should be 5 * 

    o = """
    best = (None, 0)
    for _ in range(1): # 2000
        grid, starting = get_random_maze(MAX_SIZE)
        mze = MazeRep(grid, starting)
        r = mze.evaluate(Net())
        print(r)
        if r > best[1]:
            best = (mze, r)
    print(best[0], best[1])
    """

    #pprint(hr.send_content({(0, 0): HC.EMPTY}))
    #pprint(hr.send_content(complete_map_example))
    #complete_map_example[(7, 0)] = HC.EMPTY
    #pprint(hr.send_content(complete_map_example))


if __name__ == "__main__":
    main()
