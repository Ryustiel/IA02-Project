import random, copy
from enum import Enum
from testing2.hitman2 import HC
import numpy as np

'''
HC.WALL or | = mur 
HC.EMPTY or . = vide
N = garde qui regarde au nord
S = garde qui regarde au sud
E ......
W .......

n = civil qui regarde au nord
s ......
e .......
w ........

X = cible
A = arme 
D = deguisement

& = depart

'''

import random

def affichage(grille, pos):
    affic=copy.deepcopy(grille)
    for i in range (len(grille)):
        for j in range (len(grille[i])):
            if grille[i][j]==HC.EMPTY:
                affic[i][j]='.'
            if grille[i][j]==HC.WALL:
                affic[i][j]='|'
            if grille[i][j]==HC.GUARD_N:
                affic[i][j]='N'
            if grille[i][j]==HC.GUARD_E:
                affic[i][j]='E'
            if grille[i][j]==HC.GUARD_S:
                affic[i][j]='S'
            if grille[i][j]==HC.GUARD_W:
                affic[i][j]='W'
            if grille[i][j]==HC.CIVIL_N:
                affic[i][j]='n'
            if grille[i][j]==HC.CIVIL_E:
                affic[i][j]='e'
            if grille[i][j]==HC.CIVIL_S:
                affic[i][j]='s'
            if grille[i][j]==HC.CIVIL_W:
                affic[i][j]='w'
            if grille[i][j]==HC.TARGET:
                affic[i][j]='X'
            if grille[i][j]==HC.SUIT:
                affic[i][j]='D'
            if grille[i][j]==HC.PIANO_WIRE:
                affic[i][j]='A'

    affic[pos[0]][pos[1]] = '&'
    return str(affic)

def get_random_maze(max_size: int):
    valide=False
    while valide==False:
            # Dimensions du labyrinthe
        largeur = random.randint(6, max_size)
        hauteur = random.randint(6, max_size)
        probaMur=random.uniform(1/2,1/5)
        probaGarde = random.uniform(1/20,2/25)
        probaCivil = random.uniform(1/15,2/20) 
        probaPilier = random.uniform(1/5, 1/12)
        # Créer une grille vide
        grille = [[HC.EMPTY for _ in range(hauteur)] for _ in range(largeur)]
        
        # Ajouter les bords avec des HC.WALL
        for i in range(largeur):
            grille[i][0] = HC.WALL
            grille[i][hauteur - 1] = HC.WALL
        
        for i in range(hauteur):
            grille[0][i] = HC.WALL
            grille[largeur - 1][i] = HC.WALL
            
        for i in range (1, largeur-2):
            for j in range (1,hauteur-2):
                if grille[i][j] == HC.EMPTY and random.random()<probaPilier:
                    grille[i][j]=HC.WALL
        
        for i in range (1, largeur-2):
            for j in range (1,hauteur-2):
                if grille[i][j] == HC.EMPTY and random.random() < probaMur and (grille[i-1][j]==HC.WALL or grille[i+1][j]==HC.WALL or grille[i][j-1]==HC.WALL or grille[i][j+1]==HC.WALL):
                    grille[i][j]=HC.WALL
            
            
            
            

        for i in range (1, largeur-2):
            for j in range (1,hauteur-2):
                if grille[i][j] == HC.EMPTY:
                    if random.random() < probaGarde:
                        direct=random.random()
                        if direct < 0.25:
                            grille[i][j]=HC.GUARD_N
                        elif direct < 0.5:
                            grille[i][j]=HC.GUARD_S
                        elif direct < 0.75:
                            grille[i][j]=HC.GUARD_E  
                        else:
                            grille[i][j]=HC.GUARD_W
                    elif random.random() <probaCivil:
                        direct=random.random()
                        if direct < 0.25:
                            grille[i][j]=HC.CIVIL_N
                        elif direct < 0.5:
                            grille[i][j]=HC.CIVIL_S
                        elif direct < 0.75:
                            grille[i][j]=HC.CIVIL_E  
                        else:
                            grille[i][j]=HC.CIVIL_W
        
        
        
        X=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        while grille[X[0]][X[1]] != HC.EMPTY:
            X=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        
        grille[X[0]][X[1]]=HC.TARGET
        
        
        A=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        while grille[A[0]][A[1]] != HC.EMPTY:
            A=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
           
        grille[A[0]][A[1]]=HC.PIANO_WIRE
        
        
        D=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        while grille[D[0]][D[1]] != HC.EMPTY:
            D=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        
        grille[D[0]][D[1]]=HC.SUIT
        
        Dep=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        while grille[Dep[0]][Dep[1]] != HC.EMPTY:
            Dep=(random.randint(1,largeur-2),random.randint(1,hauteur-2))
        
        grille[Dep[0]][Dep[1]]=HC.EMPTY
        
        
        verify=copy.deepcopy(grille)
        
        nbModif=1
        init=False
        while nbModif != 0:
            nbModif=0
            for i in range (1, largeur-1):
                for j in range (1,hauteur-1):
                    if verify[i][j]==HC.EMPTY and init==False:
                        verify[i][j]=','
                        init=True
                    if init==True and (verify[i][j] == HC.EMPTY or verify[i][j] == HC.TARGET or verify[i][j] == HC.CIVIL_N or verify[i][j] == HC.CIVIL_S or verify[i][j] == HC.CIVIL_E or verify[i][j] == HC.CIVIL_W or verify[i][j] == HC.SUIT or verify[i][j]==HC.PIANO_WIRE) and (verify[i-1][j]==',' or verify[i+1][j]==',' or verify[i][j-1]==',' or verify[i][j+1]==','):
                        verify[i][j]=','
                        nbModif+=1
        valide=True
        
        for i in range (1, largeur-1):
            for j in range (1,hauteur-1):
                if verify[i][j] == HC.EMPTY or verify[i][j] == HC.TARGET or verify[i][j] == HC.CIVIL_N or verify[i][j] == HC.CIVIL_S or verify[i][j] == HC.CIVIL_E or verify[i][j] == HC.CIVIL_W or verify[i][j] == HC.SUIT or verify[i][j]==HC.PIANO_WIRE:
                    valide=False

    # converting to numpy format for convenience
    grille = np.array(grille)

    return grille[1:largeur-1, 1:hauteur-1], (Dep[0] - 1, Dep[1] - 1)




# Afficher la grille
# grille, size_x, size_y = get_random_maze(10)
# print(size_x, size_y)
# affic = affichage(grille)
# for ligne in affic:
    # print(' '.join(ligne))