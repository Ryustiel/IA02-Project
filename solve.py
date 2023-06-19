from explorer import *
import time

# CONSTANT VALUES
MAX_ITERATION_COEFFICIENT = 20 # sera multiplé par le nombre de cases
# pour déterminer une limite d'exploration
DISPLAY_EVERY_X_ITERATION = 100
IGNORE_SUIT = True

def tryout(actions, grid, origin):
    print(affichage(grid, matrix_to_grid(origin, len(grid))))
    print("\n\n")

    explorer = MazeExplorer(HitmanReferee(grid, origin))
    status = explorer.referee.start_phase2()
    pos = status['position']
    for instruction in actions:
        # print(explorer.getActions(status, grid[pos[0]][pos[1]]))
        status = explorer.branch(instruction)
        done = has_won(status, origin)
        coords = matrix_to_grid(status['position'], status['m'])
        
        print(instruction)
        print(affichage(grid, coords))
        print(done, status['penalties'], "\n")

def calculate_penalties(actions, grid, origin):
    explorer = MazeExplorer(HitmanReferee(grid, origin))
    status = explorer.referee.start_phase2()
    for instruction in actions:
        status = explorer.branch(instruction)
        
    return status['penalties']

# ===================================================== SOLVER

def solve(grid, origin, ignore_suit=IGNORE_SUIT): # STARTING IN MATRIX FORMAT
    """
    Gère une file d'instances de jeu à différents niveaux d'avancement,
    recherche les fils des instances triées par minimum de pénalité.
    
    Intègre une heuristique "pas repasser par le même état avec
    un score pire".
    """
    starting = matrix_to_grid(origin, len(grid))
    print(starting, origin)

    instances = deque()

    maze = MazeExplorer(HitmanReferee(grid, origin))
    maze.status = maze.referee.start_phase2() # init value of STATUS
    instances.appendleft(maze) # élément initial

    heuristique_min_penalty_arme = None # lorsqu'un objectif de jeu est atteint,
    # soustrait la pénalité minimale à l'agent
    # permet d'explorer en priorité les chemins qui partent de cet objectif
    heuristique_min_penalty_kill = None

    # demi trajet évite de revenir au noeud de départ
    # (orientation, has_suit, suit_on, has_weapon, target_down)
    # dérivée de a*
    # [orientations * etats]
    heuristique_sans_repetition = []
    for i in range(len(grid)):
        heuristique_sans_repetition.append(list())
        for _ in range(len(grid[0])):
            heuristique_sans_repetition[i].append(list())
    
    MAX_ITERATION = MAX_ITERATION_COEFFICIENT * len(grid[0]) * len(grid)
    print("MAX_ITERATION :", MAX_ITERATION)
    start_time = time.time()

    while MAX_ITERATION > 0 and len(instances) > 0:

        maze = instances.popleft()
        # up to date with the maze's history

        for action in maze.getActions(grid):

            new_instance = deepcopy(maze)
            # créer une copie du referee pour chaque euh... branche
            # dropper la copie après
            status = new_instance.branch(action)
            # done = true dès que solution
            done = has_won(status, origin)
            # penalties mis à jour dans new_instance

            # MANIPULATION DES SCORES POUR L'EXPLORATION
            #if action == AC.HORAIRE or action == AC.ANTIHORAIRE:
                #new_instance.penalties += 1
                # rotation coûte plus chère que avancer, mais pas trop

            #elif action == AC.ARME:
                # on enlève min_penalty à chaque fois que l'objectif est atteint
                #if heuristique_min_penalty_arme is None:
                    #heuristique_min_penalty_arme = new_instance.penalties
                #new_instance.penalties -= heuristique_min_penalty_arme

            #elif action == AC.ARME:
                #if heuristique_min_penalty_kill is None:
                    #heuristique_min_penalty_kill = new_instance.penalties
                #new_instance.penalties -= heuristique_min_penalty_kill

            if done:
                print("DONE")
                return new_instance, get_ellapsed_string(start_time)

            # ELSE
            # verifie si ça vaut le coup de conserver l'array

            state = make_state(status, ignore_suit) # VIRER METHODES UTILITAIRES
            pos = matrix_to_grid(status['position'], status['m'])
            if state not in heuristique_sans_repetition[pos[0]][pos[1]]: # pas déjà parcouru
                # (score < stored_score) jamais le cas cas on
                # parcours du plus petit au plus grand score 
                heuristique_sans_repetition[pos[0]][pos[1]].append(state)

                # ajouter à la file en triant

                i = 0
                l = len(instances)
                while i < l:
                    if instances[i].penalties >= new_instance.penalties: 
                        # ON VEUT MINIMISER PENALTIES
                        # si score plus grand insérer
                        # ou égal pour éviter de parcourir les == pour rien
                        instances.insert(i, new_instance)
                        break
                    i += 1
                if i == l:
                    instances.append(new_instance)

            # else : #ne pas récupérer les enfants parce qu'on en arrive à un état déjà parcouru

        # note : la référence à l'instance maze est perdue à ce moment (mémoire)
        MAX_ITERATION -= 1

        # TRACKING
        if MAX_ITERATION % DISPLAY_EVERY_X_ITERATION == 0:
            # gathering info
            time_str = get_ellapsed_string(start_time)

            # printing ingo
            print(f"{MAX_ITERATION // 100} batches left : {len(instances)} instances : {time_str} ellapsed")
            print(affichage(grid, matrix_to_grid(status['position'], status['m'])))

            # printing exploration matrix
            l = np.zeros((len(grid), len(grid[0])), dtype=np.int8)
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    ntried = len(heuristique_sans_repetition[i][j]) // 3
                    l[i, j] = ntried
            print(l)

    if len(instances) > 0:
        raise ValueError("Found No solution (try increasing MAX_ITERATION_COEFFICIENT)")
        return instances.popleft(), get_ellapsed_string(start_time)
    raise ValueError("Ended with empty stack")


def solve_phase1():
    """
    runs the exact same algorithm as solve_phase2, 
    except that it won't be initializing a referee,
    but a starting instance of MazeUncoverer
    """
    ...