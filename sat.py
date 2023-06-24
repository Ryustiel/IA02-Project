"""
[IA02] TP SAT/Sudoku template python
author:  Sylvain Lagrue
version: 1.1.0
"""

from hitman2 import *
from typing import List, Tuple
import os
import subprocess
from copy import deepcopy


nbCases=40
nbVarPCase=13
nbVar=nbCases*nbVarPCase
cordeTouve=False
cibleTouve=False
costumeTouve=False



carte = {}
dimacsClauses=[]


# alias de types
Grid = List[List[int]] 
PropositionnalVariable = int
Literal = int
Clause = List[Literal]
ClauseBase = List[Clause]
Model = List[Literal]



"""

		
	


#### fonctions fournies

"""
"""
def write_dimacs_file(dimacs: str, filename: str):
	with open(filename, "w", newline="") as cnf:
        	cnf.write(dimacs)


def generator(


def scaner(hitman: HitmanReferee):
	nbPers= hitman.__get_listening()
	pos=hitman.__pos
	if nbPers == 0:
		for i in range (-2,2):
			for j in range(-2,2)
				for k in range(3,10):
					write_dimacs_file("-" +str(cell_to_variable(hitman.pos[0]+i,hitman.pos[1]+j, k) + " 0", "dimacs.cnf"))
	elif nbPers >= 1:
	
	vue=hitman.__get_vision(3)
	for i in range(len(vision)):
		if hitman.__orientation==HC.N:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0],hitman.pos[1]+i, vision[i]) +"0", "dimacs.cnf"))
		elif hitman.__orientation==HC.S:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0],hitman.pos[1]-i, vision[i]) +"0", "dimacs.cnf"))
		elif hitman.__orientation==HC.E:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0]+i,hitman.pos[1], vision[i]) +"0", "dimacs.cnf"))
		else:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0]-i,hitman.pos[1], vision[i]) +"0", "dimacs.cnf"))
		
	
	







def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:
    
    filename = os.path.join(os.getcwd(), filename)
    print(filename)
    
    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False, []

    model = lines[2][2:-2].split(" ")

    return True, [int(x) for x in model]


#### extension : modelisation du soudoukou


def cell_to_variable(i: int, j: int, val: int) -> PropositionnalVariable:
    return PropositionnalVariable(1+ val + 17*i + 17*17*j )


def at_least_one(variables: List[PropositionnalVariable]) -> Clause:
    # chaine de "or"
    assert False not in (v > 0 for v in variables)
    return variables


def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    # xi => non xj pour chaque j != i pour chaque i
    assert False not in (v > 0 for v in variables)
    base = list()
    base.append(at_least_one(variables))
    n_vars = len(variables)
    for i in range(n_vars):
    	for j in range(i + 1, n_vars):
            base.append([-variables[i], -variables[j]])
    return base
    
    
def create_box_constraints() -> ClauseBase:
    clauses = list()
    for x_start in [k*3 for k in range(3)]:
        for y_start in [k*3 for k in range(3)]:
            # valeurs au sein d'une sous grille
            for val in range(9):
                litteraux = []
                for i in range(3): # représente une sous grille
                    for j in range(3):
                        litteraux.append(cell_to_variable(x_start + i, y_start + j, val))
                clauses.append(at_least_one(litteraux)) # ClauseBase.append(Clause)
    return clauses
    
def create_lin_constraints() -> ClauseBase:
    clauses = list()
    for i in range(9):
        for val in range(9):
            litteraux = []
            for j in range(9): # représente une ligne
                litteraux.append(cell_to_variable(i, j, val))
            clauses.append(at_least_one(litteraux)) # ClauseBase.append(Clause)
    return clauses
    
def create_column_constraints() -> ClauseBase:
    clauses = list()
    for j in range(9):
        for val in range(9):
            litteraux = []
            for i in range(9): # représente une colonne
                litteraux.append(cell_to_variable(j, i, val))
            clauses.append(at_least_one(litteraux)) # ClauseBase.append(Clause)
    return clauses
    
def create_value_constraints(grid: Grid) -> ClauseBase:
    # iterer sur colonne + lignes + 3x3 (par repere) <= grille carree
    # renseigner "chaque valeur au moins une fois" parce que le nombre est limite.
    # faire une regle sur au moins une des cases de la liste (case 1,1 ou case 1,2, ou ...), pour chaque chiffre
    grid_length = len(grid[0])
    base = list()
    
    # individual cell constraints
    for i in range(grid_length):
    	for j in range(grid_length): # cell y
            cell_variables = [cell_to_variable(i, j, val) for val in range(9)]
            base.extend(unique(cell_variables))
    	    
    base.extend(create_box_constraints())
    base.extend(create_lin_constraints())
    base.extend(create_column_constraints())
    	    
    return base
    

def generate_problem(grid: Grid) -> ClauseBase:
    # ajouter les cases fixees
    base = create_value_constraints(grid)
    for i, line in enumerate(grid):
    	for j, value in enumerate(line):
    	    if value: # value is not 0 (unset)
                base.append([cell_to_variable(i, j, value - 1)]) # ClauseBase.append(PropositionnalVariable)
    return base
    
#### extension : appel au solveur



def clauses_to_

def clauses_to_dimacs(clauses: ClauseBase, nb_vars: int) -> str:
    # self explanatory.
    print(len(clauses))
    fstring = f"p cnf {nb_vars} {len(clauses)}"
    for clause in clauses:
        fstring += "\n"
        for litteral in clause:
            fstring += f" {litteral}" # litteral => string
    print(fstring)
    return fstring

"""
def initialize():
    #nbCases= len(lab)*len(lab[0])

    print(nbCases)
    totVar = nbCases*(nbVarPCase)
    clause11=[]
    clause12=[]
    clause13=[]
    for i in range(nbCases): #on fait les at_least
        var=i*13
        clause11.append(var + 11)
        clause12.append(var+12)
        clause13.append(var+13)
    dimacsClauses.append(clause11)
    dimacsClauses.append(clause12)
    dimacsClauses.append(clause13)
    for i in range(nbCases):
        clause11=[]
        clause12=[]
        clause13=[]
        for j in range(nbCases):
            if j!= i:
                clause11.append(-(j*13+11))
                clause12.append(-(j*13+12))
                clause13.append(-(j*13+13))
            else:
                clause11.append(j*13+11)
                clause12.append(j*13+12)
                clause13.append(j*13+13)
        dimacsClauses.append(clause11)
        dimacsClauses.append(clause12)
        dimacsClauses.append(clause13)

def case_to_variable(case, val) -> PropositionnalVariable:
    return PropositionnalVariable(1+ val + 13*case[0] + 13*13*case[1] )
"""
def signalCordeTrouve(case):
    cordeTouve=True
    caseVariable=case_to_variable(case,13)
    for i in range(0,nbVar,13):
        if i!=caseVariable:
            dimacsClauses.append([-i])

def signalCostumeTrouve(case):
    CostumeTouve=True
    caseVariable=case_to_variable(case,12)
    for i in range(0,nbVar,12):
        if i!=caseVariable:
            dimacsClauses.append([-i])

def signalCibleTrouve(case):
    CibleTouve=True
    caseVariable=case_to_variable(case,11)
    for i in range(0,nbVar,12):
        if i!=caseVariable:
            dimacsClauses.append([-i])
"""
"""
def unique(variables: List[PropositionnalVariable]) -> ClauseBase:
    # xi => non xj pour chaque j != i pour chaque i
    assert False not in (v > 0 for v in variables)
    base = list()
    base.append(at_least_one(variables))
    n_vars = len(variables)
    for i in range(n_vars):
    	for j in range(i + 1, n_vars):
            base.append([-variables[i], -variables[j]])
    return base
"""
def dimacs_write(filename, dimacs):
    f=open(filename, "w")
    intro = "p cnf "+ str(nbVar)+" "+str(len(dimacs)) + "\n"
    f.write(intro)
    for i in dimacs:
        for j in i:
            f.write(str(j)+" ")
        f.write(" 0\n")
    f.close()
"""
def scaner(hitman: HitmanReferee):
	nbPers= hitman.__get_listening()
	pos=hitman.__pos
	if nbPers == 0:
		for i in range (-2,2):
			for j in range(-2,2)
				for k in range(3,10):
					write_dimacs_file("-" +str(cell_to_variable(hitman.pos[0]+i,hitman.pos[1]+j, k) + " 0", "dimacs.cnf"))
	elif nbPers >= 1:

	vue=hitman.__get_vision(3)
	for i in range(len(vision)):
		if hitman.__orientation==HC.N:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0],hitman.pos[1]+i, vision[i]) +"0", "dimacs.cnf"))
		elif hitman.__orientation==HC.S:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0],hitman.pos[1]-i, vision[i]) +"0", "dimacs.cnf"))
		elif hitman.__orientation==HC.E:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0]+i,hitman.pos[1], vision[i]) +"0", "dimacs.cnf"))
		else:
			write_dimacs_file(str(cell_to_variable(hitman.pos[0]-i,hitman.pos[1], vision[i]) +"0", "dimacs.cnf"))
"""
def run_gophersat(filename):
    output = subprocess.run(["/home/osboxes/Documents/IA02/IA02-Project/testing2/gophersat", filename], capture_output=True, check=True, encoding="utf8")
    string = str(output.stdout)
    lines = string.splitlines()
    if lines[1] != "s SATISFIABLE":
        #print("not satisFIABLE")
        return False, []
    model = lines[2][2:-2].split(" ")
    #print("satisFIABLE")
    return True, [int(x) for x in model]


def fini():
    dimacs_write("dimacs.cnf",dimacsClauses)
    modele=run_gophersat("dimacs.cnf")
    negation=[]
    for i in range(len(modele)):
        negation[i]=(-modele[i])
    dimacs2= deepcopy(dimacsClauses)
    dimacs2.append(negation)
    if run_gophersat:
        return False
    else:
        return True


def var_to_case(var):
    case=[]
    case[0]=var%13
    case[1]=

def ConnuDansZone(pos):
    dejaVu=[]
    for i in range(-2,3):
        for j in range(-2,3):
            for k in range(1,14):
                if [case_to_variable( (pos[0]+i, pos[1]+j), k)] in dimacsClauses:
                    dejaVu.append((pos[0]+i, pos[1]+j))
    return dejaVu

def PersConnuDansZone(pos):
    dejaVu=[]
    for i in range(-2,3):
        for j in range(-2,3):
            for k in range(3,11):
                if [case_to_variable( (pos[0]+i, pos[1]+j), k)] in dimacsClauses:
                    dejaVu.append((pos[0]+i, pos[1]+j))
    return dejaVu


def scaner(pos, grille, ecoute):
    dejaVu = ConnuDansZone(pos)#on ne parcours pas les cases dans laquelle on sait déja ce qu'il y a
    persConnu = PersConnuDansZone(pos)
    nbPersUnk = nbPers-len(persConnu)
    if nbPersUnk == 0:
        for i in range (-2,3):
            for j in range(-2,3):
                if (pos[0]+i,pos[1]+j) not in dejaVu:
                    for k in range(3,11):
                        var=case_to_variable((pos[0]+i, pos[1]+j),k)
                        if [-var] not in dimacsClauses:
                            dimacsClauses.append([-var])
                        #write_dimacs_file("-" +str(cell_to_variable(hitman.pos[0]+i,hitman.pos[1]+j, k) + " 0", "dimacs.cnf"))
    else:
        clauseAtLeast=[]
        for i in range (-2,3):
            for j in range(-2,3):
                if (pos[0]+i,pos[1]+j) not in dejaVu:
                    for k in range(3,11):
                        var=case_to_variable((pos[0]+i, pos[1]+j),k)
                        clauseAtLeast.append([var])
                        if nbPers<5:
                            for l in range(i,3):#on fait les clauses uniques
                                for m in range(j,3):#pour chaque case, toutes il y a non(cetteCase) OU non(toute les autres cases)
                                    if (pos[0]+l,pos[1]+m) not in dejaVu:
                                        for n in range(k, 11):
                                            if var!=var+13*l+13*13*m+n:
                                                if nbPersUnk==1:
                                                    clauseUnique=[-var, -(var+13*l+13*13*m+n)]
                                                    if clauseUnique not in dimacs.Clauses:
                                                        dimacsClauses.append(clauseUnique)
                                                else:
                                                    for l2 in range(l,3):
                                                        for m2 in range(m,3):
                                                            if (pos[0]+l2,pos[1]+m2) not in dejaVu:
                                                                for n2 in range(n, 11):
                                                                    if var+13*l+13*13*m+n != var+13*l2+13*13*m2+n2:
                                                                        if nbPersUnk==2:
                                                                            clauseUnique = [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2)]
                                                                            if clauseUnique not in dimacs.Clauses:
                                                                                dimacsClauses.append(clauseUnique)
                                                                        else:
                                                                            for l3 in range(l2,3):
                                                                                for m3 in range(m3,3):
                                                                                    if (pos[0]+l3,pos[1]+m3) not in dejaVu:
                                                                                        for n3 in range(n3, 11):
                                                                                            if var+13*l2+13*13*m2+n2 != var+13*l3+13*13*m3+n3:
                                                                                                if nbPersUnk==3:
                                                                                                    clauseUnique = [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2), -(var+13*l3+13*13*m3+n3)]
                                                                                                    if clauseUnique not in dimacs.Clauses:
                                                                                                        dimacsClauses.append(clauseUnique)
                                                                                                else:
                                                                                                    for l4 in range(l2,3):
                                                                                                        for m4 in range(m3,3):
                                                                                                            if (pos[0]+l4,pos[1]+m4) not in dejaVu:
                                                                                                                for n4 in range(n4, 11):
                                                                                                                    if var+13*l4+13*13*m4+n4 != var+13*l3+13*13*m3+n3:
                                                                                                                        clauseUnique = [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2), -(var+13*l3+13*13*m3+n3), -(var+13*l4+13*13*m4+n4)]                                                                                                      [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2), -(var+13*l3+13*13*m3+n3), -(var+13*l4+13*13*m4+n4)]
                                                                                                                        if clauseUnique not in dimacs.Clauses:
                                                                                                                            dimacsClauses.append(clauseUnique)
            if clauseAtLeast not in dimacsClauses:
                dimacsClauses.append(clauseAtLeast)
            aTester=[]
            for i in dimacsClauses:
                if len(i)>1:
                    for j in i:
                        if abs(j) not in aTester:
                            aTester.append(abs(j))
            for i in aTester:
                dimacsClauses2=deepcopy(dimacsClauses)
                dimacsClauses2.append(-i)
                write_dimacs_file("dimacs.cnf", dimacsClauses2)
                if run_gophersat("dimacs.cnf") == False:
                    dimacsClauses.append([i])
                    for k in range(0,14):
                        var=i-i%13+k-1
                        if var != i and [-var] not in dimacsClauses:
                            dimacsClauses.append([-var])
                            #ajouter au dico case=var_to_case(i)
                if fini():
                    return carte
                else:
                    return False
                            #ajouter au dictionnaire

"""
                                        if nbPers==2:
                                for l in range(i,3):#on fait les clauses uniques
                                    for m in range(j,3):#pour chaque case, toutes il y a non(cetteCase) OU non(toute les autres cases)
                                        if (pos[0]+l,pos[1]+m]) not in dejaVu:
                                            for n in range(k, 11):
                                                if var!=var+13*l+13*13*m+n:
                                                    for l2 in range(l,3):
                                                        for m2 in range(m,3):
                                                            if (pos[0]+l2,pos[1]+m2]) not in dejaVu:
                                                                for n2 in range(n, 11):
                                                                    if var+13*l+13*13*m+n != var+13*l2+13*13*m2+n2:
                                                                        clauseUnique = [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2)]
                                                                        if clauseUnique not in dimacs.Clauses:
                                                                            dimacsClauses.append(clauseUnique)
                            if nbPers==3:
                                for l in range(i,3):#on fait les clauses uniques
                                    for m in range(j,3):#pour chaque case, toutes il y a non(cetteCase) OU non(toute les autres cases)
                                        if (pos[0]+l,pos[1]+m]) not in dejaVu:
                                            for n in range(k, 11):
                                                if var!=var+13*l+13*13*m+n:
                                                    for l2 in range(l,3):
                                                        for m2 in range(m,3):
                                                            if (pos[0]+l2,pos[1]+m2]) not in dejaVu:
                                                                for n2 in range(n, 11):
                                                                    if var+13*l+13*13*m+n != var+13*l2+13*13*m2+n2:
                                                                        for l3 in range(l2,3):
                                                                            for m3 in range(m3,3):
                                                                                if (pos[0]+l3,pos[1]+m3]) not in dejaVu:
                                                                                    for n3 in range(n3, 11):
                                                                                        if var+13*l2+13*13*m2+n2 != var+13*l3+13*13*m3+n3:
                                                                                            clauseUnique = [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2), -(var+13*l3+13*13*m3+n3)]
                                                                                            if clauseUnique not in dimacs.Clauses:
                                                                                                dimacsClauses.append(clauseUnique)
                            if nbPers==4:
                                for l in range(i,3):#on fait les clauses uniques
                                    for m in range(j,3):#pour chaque case, toutes il y a non(cetteCase) OU non(toute les autres cases)
                                        if (pos[0]+l,pos[1]+m]) not in dejaVu:
                                            for n in range(k, 11):
                                                if var!=var+13*l+13*13*m+n:
                                                    for l2 in range(l,3):
                                                        for m2 in range(m,3):
                                                            if (pos[0]+l2,pos[1]+m2]) not in dejaVu:
                                                                for n2 in range(n, 11):
                                                                    if var+13*l+13*13*m+n != var+13*l2+13*13*m2+n2:
                                                                        for l3 in range(l2,3):
                                                                            for m3 in range(m3,3):
                                                                                if (pos[0]+l3,pos[1]+m3]) not in dejaVu:
                                                                                    for n3 in range(n3, 11):
                                                                                        if var+13*l2+13*13*m2+n2 != var+13*l3+13*13*m3+n3:
                                                                                            for l4 in range(l2,3):
                                                                                                for m4 in range(m3,3):
                                                                                                    if (pos[0]+l4,pos[1]+m4]) not in dejaVu:
                                                                                                        for n4 in range(n4, 11):
                                                                                                            if var+13*l4+13*13*m4+n4 != var+13*l3+13*13*m3+n3:
                                                                                                                clauseUnique =                                                                                                       [-var, -(var+13*l+13*13*m+n), -(var+13*l2+13*13*m2+n2), -(var+13*l3+13*13*m3+n3), -(var+13*l4+13*13*m4+n4)]
                                                                                                                if clauseUnique not in dimacs.Clauses:
                                                                                                                    dimacsClauses.append(clauseUnique)
"""





"""
def exec_gophersat(
    filename: str, cmd: str = "gophersat", encoding: str = "utf8"
) -> Tuple[bool, List[int]]:

    filename = os.path.join(os.getcwd(), filename)
    print(filename)

    result = subprocess.run(
        [cmd, filename], capture_output=True, check=True, encoding=encoding
    )

"""




#### fonction principale


def main():
    initialize()
    #p=cell_to_variable((1,4),11)
    #print(p)
    #signalCibleTrouve((1,7))
    dimacs_write("dimacs.cnf",dimacsClauses)
    run_gophersat("dimacs.cnf")



"""
    write_dimacs_file(dimacs, filename = 'sudoku_dimacs.txt')

    exec_gophersat('sudoku_dimacs.txt', cmd = "gophersat", encoding = "utf8") # Tuple[bool, List[int]]: 
"""

if __name__ == "__main__":
    main()
