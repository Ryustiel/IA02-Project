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




carte = {}
dimacsClauses=[]






		
	



def initialize(n,m):
    nbCases=n*m
    totVar = nbCases*13
    clause11=[]
    clause12=[]
    clause13=[]
    for i in range(nbCases): #on fait les at_least
        var=i*13
        clause11.append(var+11)
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

def case_to_variable(case, val):
    return 1+ val + 13*case[0] + 13*13*case[1]

def dimacs_write(filename, dimacs):
    f=open(filename, "w")
    intro = "p cnf "+ str(nbVar)+" "+str(len(dimacs)) + "\n"
    f.write(intro)
    for i in dimacs:
        for j in i:
            f.write(str(j)+" ")
        f.write(" 0\n")
    f.close()

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
    dimacs_write("dimacs.cnf", dimacs)
    if run_gophersat():
        return False
    else:
        return True


def var_to_case(var):
    typ=var%13-1
    if typ==0:
        typ=13
    #print(typ)
    case=var-typ
    i=0
    while case%(13*13)!=1:
        i+=1
        case-=13
    #print(i)
    j=case//(13*13)
    #print(j)
    return [i, j, t]

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
                            c=var_to_case(var)
                            carte[(c[0],c[1])] = c[2]
            if fini():
                return carte
            else:
                return False




#### fonction principale


def main():
    initialize()

    dimacs_write("dimacs.cnf",dimacsClauses)
    run_gophersat("dimacs.cnf")


if __name__ == "__main__":
    main()
