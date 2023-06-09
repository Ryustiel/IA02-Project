from enum import Enum
import time

class AC(Enum):
    HORAIRE = 0
    ANTIHORAIRE = 1
    MOVE = 2
    KILL = 3
    GARDE = 4
    CIVIL = 5
    COSTUME = 6
    ARME = 7

def generate_phase1_solution(n, m, fill_object):
    """
    génère un dictionnaire composé uniquement de 
    """
    solution = {}
    for i in range(n):
        for j in range(m):
            solution[(n, m)] = fill_object
    return solution
    

def get_ellapsed_string(start_time):
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_str = str(minutes)+'min '+str(seconds)+'s' if minutes > 0 else str(seconds)+'s'
    return time_str

def has_won(status, origin):
    # target killed + back to the starting location
    if (
        status['is_target_down']
        and status['position'] == origin
    ):
        return True
    return False

def grid_to_matrix(indices, height):
    return indices[1], height - 1 - indices[0]
    
def matrix_to_grid(pos, height):
    """
    this exists because our teacher decided to 
    index his arrays from the bottom to the top
    """
    return height - 1 - pos[1], pos[0]

def make_state(status, ignore_suit): # transformer en lecteur de status
    """
    renvoie un tuple formatté qui représente l'état de cette 
    instance pour comparer l'équivalence avec d'autres instances.
    Pour la phase 2
    """
    if ignore_suit:
        return (
        status['orientation'],
        status['has_weapon'],
        status['is_target_down']
    )
    return (
        status['orientation'],
        status['is_suit_on'],
        status['has_weapon'],
        status['is_target_down']
    )

def make_state_phase1(maze_uncoverer):
    """
    identique à make_state, pour la phase 1
    il n'y a que l'orientation qui est vraiment différente
    entre les différents états du personnage
    """
    return maze_uncoverer.orientation

def perform(hitman, action):
    status = None
    if action == AC.MOVE: status = hitman.move()
        
    elif action == AC.HORAIRE: status = hitman.turn_clockwise()

    elif action == AC.ANTIHORAIRE: status = hitman.turn_anti_clockwise()

    elif action == AC.ARME: status = hitman.take_weapon()

    elif action == AC.CIVIL: status = hitman.neutralize_civil()

    elif action == AC.GARDE: status = hitman.neutralize_guard()

    elif action == AC.COSTUME:
        hitman.take_suit()
        status = hitman.put_on_suit()

    elif action == AC.KILL: status = hitman.kill_target()

    if status is None: raise Exception(f"No status | action = {action}")
    return status