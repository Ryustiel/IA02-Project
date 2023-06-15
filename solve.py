from explorer import *

handmade_instructions_world_example = [
    AC.MOVE, AC.HORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE,
    AC.MOVE, AC.HORAIRE, AC.MOVE, AC.ARME, AC.HORAIRE, AC.HORAIRE,
    AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.HORAIRE,
    AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, 
    AC.MOVE, AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.KILL, AC.ANTIHORAIRE,
    AC.ANTIHORAIRE, AC.MOVE, AC.MOVE, AC.HORAIRE, AC.MOVE, AC.MOVE,
    AC.HORAIRE, AC.MOVE, AC.MOVE, AC.MOVE, AC.MOVE, AC.HORAIRE, AC.MOVE,
    AC.MOVE, AC.ANTIHORAIRE, AC.MOVE
]

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


# ===================================================== SOLVER

def solve(grid, starting): # STARTING IN MATRIX FORMAT
    """
    Gère une file d'instances de jeu à différents niveaux d'avancement,
    recherche les fils des instances triées par minimum de pénalité.
    
    Intègre une heuristique "pas repasser par le même état avec
    un score pire".
    """
    origin = grid_to_matrix(starting, len(grid))
    print(starting, origin)

    instances = deque()
    instances.appendleft(MazeExplorer(HitmanReferee(grid, origin))) # trié en par profondeur
    
    heuristique_min_penalty = None # penalite minimale pour atteindre l'arme déduite
    # laisse tout de même la possibilité à l'arbre de faire des compromis pour atteindre
    # une arme avec un meilleur angle

    # demi trajet évite de revenir au noeud de départ
    # (orientation, has_suit, suit_on, has_weapon, target_down)
    # dérivée de a*
    # [orientations * etats]
    heuristique_demi_trajet = []
    for i in range(len(grid)):
        heuristique_demi_trajet.append(list())
        for _ in range(len(grid[0])):
            heuristique_demi_trajet[i].append(list())
    
    MAX_ITERATION = 10000 # IDEE : LE FAIRE DEP DE LA TAILLE DE LA CARTE

    while MAX_ITERATION > 0 and len(instances) > 0:

        maze = instances.popleft()
        # up to date with the maze's history

        status = maze.referee.start_phase2() # COPIER LE REFEREE A JOUR SYSTEMATIQUEMENT
        for act in maze.history:
            status = perform(maze.referee, act)

        pos = matrix_to_grid(status['position'], status['m']) # EN FAIRE DES OBJETS MATRICE
        for action in maze.getActions(status, grid[pos[0]][pos[1]]):

            new_instance = deepcopy(maze)
            # créer une copie du referee pour chaque euh... branche
            # dropper la copie après
            status = new_instance.branch(action)
            # done = true dès que solution
            done = has_won(status, origin)
            # penalties mis à jour dans new_instance

            # ajouter les décalages de scores
            if action == AC.ARME or action == AC.KILL:
                new_instance.penalties -= 2 # bonus spontané pour guider le bot
                # IDEE : PROPORTIONNEL A LA PENALITE MINIMALE NECESSAIRE POUR L'ATTEINDRE

            if done:
                print("DONE")
                return new_instance

            # ELSE
            # verifie si ça vaut le coup de conserver l'array

            state = make_state(status) # VIRER METHODES UTILITAIRES
            pos = matrix_to_grid(status['position'], status['m'])
            if state not in heuristique_demi_trajet[pos[0]][pos[1]]: # pas déjà parcouru
                # (score < stored_score) jamais le cas cas on
                # parcours du plus petit au plus grand score 
                heuristique_demi_trajet[pos[0]][pos[1]].append(state)

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
                
        MAX_ITERATION -= 1

        # DISPLAY
        if MAX_ITERATION % 100 == 0:
            print(MAX_ITERATION // 100, " : ", len(instances))
            print(affichage(grid, matrix_to_grid(status['position'], status['m'])))
            l = np.zeros((len(grid), len(grid[0])), dtype=np.int8)
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    l[i, j] = len(heuristique_demi_trajet[i][j])
            print(l)

    if len(instances) > 0:
        raise ValueError("There Should be a solution")
        return instances.popleft()
    raise ValueError("Ended with empty stack")