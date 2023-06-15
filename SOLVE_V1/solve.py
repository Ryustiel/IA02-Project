from explorer import *

def handmade_solution():
    m = MazeExplorer(world_example, (5, 0))
    print(m, "\n\n")

    instructions = [
        AC.MOVE, AC.HORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE,
        AC.MOVE, AC.HORAIRE, AC.MOVE, AC.ARME, AC.HORAIRE, AC.HORAIRE,
        AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.HORAIRE,
        AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, 
        AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.KILL, AC.ANTIHORAIRE,
        AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.HORAIRE, AC.MOVE, AC.MOVE,
        AC.HORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE, AC.HORAIRE, AC.MOVE,
        AC.MOVE, AC.ANTIHORAIRE, AC.MOVE
    ]
    for instruction in instructions:
        print(m.getActions())
        m.branch(instruction)
        print(m)
        print(m.accessibility_matrix)
        print(m.getState())
        print(m.hasWon(), "\n", m.getScore(), "\n\n")


# ===================================================== SOLVER

def solve(grid, starting):
    """
    Gère une file d'instances de jeu à différents niveaux d'avancement,
    recherche les fils des instances triées par minimum de pénalité.
    
    Intègre une heuristique "pas repasser par le même état avec
    un score pire".
    """
    instances = deque()
    instances.appendleft(MazeExplorer(grid, starting)) # trié en par profondeur
    threshold = 0 # détermine dans quel file les noeuds vont être insérés

    # demi trajet évite de revenir au noeud de départ
    # (orientation, has_suit, suit_on, has_weapon, target_down)
    # dérivée de a*
    # [orientations * etats]
    heuristique_demi_trajet = []
    for i in range(len(grid)):
        heuristique_demi_trajet.append(list())
        for _ in range(len(grid[0])):
            heuristique_demi_trajet[i].append(list())
    
    MAX_ITERATION = 10000
    done = False

    while MAX_ITERATION > 0 and len(instances) > 0:

        maze = instances.popleft()
        for action in maze.getActions():

            new_instance = deepcopy(maze)
            score, done = new_instance.branch(action) # done = true dès que solution
            # on veut minimiser le score à la fin

            # SPECIAL DEBUG ESPACE D'ACTIONS
            o = """
            if new_instance.getPos() == (1, 6):
                print("ORIENTATION", new_instance.getState())
                print("ACTIONS, ", new_instance.getActions())
                print("VISION", new_instance._HitmanReferee__get_vision()[0][1])
            """
                
            if done:
                print("DONE")
                return new_instance

            # verifie si ça vaut le coup de conserver l'array

            state = new_instance.getState()
            pos = new_instance.getPos()
            if state not in heuristique_demi_trajet[pos[0]][pos[1]]: # pas déjà parcouru
                # (score < stored_score) jamais le cas cas on
                # parcours du plus petit au plus grand score 
                heuristique_demi_trajet[pos[0]][pos[1]].append(state)

                # ajouter à la file en triant

                i = 0
                l = len(instances)
                while i < l:
                    if instances[i].getScore() >= score: # si score plus grand insérer
                        # ou égal pour éviter de parcourir les == pour rien
                        instances.insert(i, new_instance)
                        break
                    i += 1
                if i == l:
                    instances.append(new_instance)

            # else : #ne pas récupérer les enfants parce qu'on en arrive à un état déjà parcouru
                
        MAX_ITERATION -= 1

        # DISPLAY
        if MAX_ITERATION % 100 == 0:
            print(MAX_ITERATION // 100, " : ", len(instances))

        o = """
        if MAX_ITERATION % 10 == 0:
            print(instances[0])
            # print(instances[0].getHistory())
            print(instances[0].getScore())
            print(instances[0].getState())

            l = np.zeros((len(grid), len(grid[0])), dtype=np.int8)
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    l[i][j] = len(heuristique_demi_trajet[i][j])
            print("\nLENGTH OF PARCOURS")
            for line in l:
                print(line)

            print(heuristique_demi_trajet[1][6])
            
            print("\n\n\n")
        """

    if len(instances) > 0:
        raise ValueError("There Should be a solution")
        return instances.popleft()
    raise ValueError("Ended with empty stack")



