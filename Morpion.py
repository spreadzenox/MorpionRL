import numpy as np
import random
import copy
import pygame as pg
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree

pg.init()
#Création de la grille vide
#Une croix x=1 et un rond o=-1 ou vide=0
Grille=[[0,0,0] for i in range (3)]
Grille=np.array(Grille)
#f = open('D:\PROJECTS\IA_POKER\DB_MORPION.txt', 'a')


Parties=[]
ResParties=[]
clf=MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(6, 2), random_state=1)


#PARTIE IA

def entraineur_joue(Joueur):
    Jouer(CoupHasard(Grille,Joueur),Joueur)
    pass

def Reset():
    Grille=[[0,0,0] for i in range (3)]
    Grille=np.array(Grille)
    pass



#Fonction d'évaluation de victoire
def iswon(Grille):
    #On regarde d'abord les victoires possibles sur les lignes et les colonnes en balayant le tableau
    l=0
    c=0
    for i in range(3):
        for j in range(3):
            l+=Grille[i][j]
            c+=Grille[j][i]
        if l>2 or c>2 :
            return(1)
        if l<-2 or c<-2 :
            return(-1)
        l=0
        c=0
    #Reste les victoire en diagonale avec deux possibles pour chaque joueur
    if Grille[0][0]+Grille[1][1]+Grille[2][2]>2:
        print(Grille)
        return(1)
    if Grille[2][0]+Grille[1][1]+Grille[0][2]>2:
        return(1)
    if Grille[0][0]+Grille[1][1]+Grille[2][2]<-2:
        return(-1)
    if Grille[2][0]+Grille[1][1]+Grille[0][2]<-2:
        return(-1)
    else:
        return(False)
def isFinish(Grille):
    if NumeroTour(Grille)==8 and iswon(Grille)==False:
        print("Null")
        return(True)
    elif iswon(Grille)!=False:
        return(True)
    else:
        return(False)



def isLegal(Coup,Grille):
    if Grille[Coup[0]][Coup[1]]== 0 :
        return(True)
    else:
        return(False)
def isReel(Grille):
    c=0
    r=0
    for j in range (3):
        for i in range(3):
            if Grille[i][j]==1 :
                c+=1
            if Grille[i][j]==-1 :
                r+=1
    if abs(c-r)>1 :
        return(False)
    if iswon(Grille)!=False :
        return(False)
    else:
        return(True)

def CoupsPossible(Grille):
    TotalCoups=[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
    Possibles=[]
    for Coup in TotalCoups :
        if isLegal(Coup,Grille)==True:
            Possibles.append(Coup)
    return(Possibles)

def NumeroTour(Grille):
    c=0
    r=0
    for j in range (3):
        for i in range(3):
            if Grille[i][j]==1 :
                c+=1
            if Grille[i][j]==-1 :
                r+=1
    return(c+r-1)
def Exploration(Grille,Joueur,NP,Val):
    for Coup in CoupsPossible(Grille):
            GrilleTemp2=copy.deepcopy(Grille)
            print("GrilleTemporaire tour joueur créé")
            GrilleTemp2[Coup[0]][Coup[1]]=Joueur
            print("COup joueur joué")
            print(GrilleTemp2)
            NP+=1
            print(NP)
            if isFinish(GrilleTemp2)==True:
                print("Partie finie detecté")
                if Joueur==iswon(GrilleTemp2):
                    Val+=1
                    print("Partie gagné")
                elif Joueur==-iswon(GrilleTemp2):
                    Val-=1
                    print("Partie Perdue")
            else:
                print("Coup enemie")
                for coupenemi in CoupsPossible(GrilleTemp2):
                    GrilleTemp3=copy.deepcopy(GrilleTemp2)
                    print("Grille temporaire tour enemi créé")
                    GrilleTemp3[coupenemi[0]][coupenemi[1]]=-Joueur
                    print("COup ennemi joué")
                    print(GrilleTemp3)
                    NP+=1
                    print(NP)
                    if isFinish(GrilleTemp3)==True:
                        print("Partie finie detecté")
                        if Joueur==iswon(GrilleTemp3):
                            Val+=1
                            print("Partie gagné")
                        elif Joueur==-iswon(GrilleTemp3):
                            Val-=1
                            print("Partie Perdue")
                    else:
                        print("Nouveau chemin")
                        res=Exploration(GrilleTemp3,Joueur,0,0)
                        Val+=res[0]
                        NP+=res[1]
    print("Sortie de boucle")
    return([Val,NP])
def BonCoup(Grille,Joueur):
    Arbre=[]
    nbpossible=str(len(CoupsPossible(Grille)))
    print("Nombre de coups à balayer="+nbpossible)
    for Coup in CoupsPossible(Grille):
        NP=1
        Val=0
        GrilleTemp=copy.deepcopy(Grille)
        GrilleTemp[Coup[0]][Coup[1]]=Joueur
        res=Exploration(GrilleTemp,Joueur,NP,Val)
        Val=res[0]/res[1]
        Arbre.append([Coup,Val])
        print("COUP DE LARBRE VALIDE")
        print(Arbre)
    meilleurcoup=Arbre[0]
    valmeilleur=Arbre[0][1]
    for coup in Arbre:
        if coup[1]>valmeilleur:
            meilleurcoup=coup
            valmeilleur=coup[1]
    return(meilleurcoup)

def AQuiDeJouer(Grille):
    somme=0
    for val in Grille:
        for val2 in val:
            somme+=val2
    if somme==0:
        return(1)
    if somme==-1:
        return(1)
    if somme==1:
        return(-1)

def CoupHasard(Grille,Joueur):
    return(CoupsPossible(Grille)[random.randint(0,len(CoupsPossible(Grille))-1)])

def Jouer(coup,joueur):
    Grille[coup[0]][coup[1]]=joueur
    pass




#Création de la fenêtre de jeu
pg.display.set_caption("Morpion")
screen=pg.display.set_mode((500,500))
grille_graph=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS\grille.jpg')
croix=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS\croix.png')
rond=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS/rond.png')
Bouton_hasard=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS/Bouton_hasard.png')
Bouton_statistique=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS/Bouton_statistique.png')
Fin=pg.image.load('D:\PROJECTS\IA_POKER\ASSETS/FIN.jpg')
running=True
print(Grille)
#Boucle de jeu
while running:
    #appliquer la grille
    screen.blit(grille_graph,(75,10))
    screen.blit(Bouton_statistique,(75,400))
    screen.blit(Bouton_hasard,(200,400))
    #On regarde la grille et on affiche en fonction

    for i in range(3):
        for j in range(3):
            if Grille[i][j]==1:
                screen.blit(croix,(75+j*350/3+10,10+i*350/3+10))
            elif Grille[i][j]==-1:
                screen.blit(rond,(75+j*350/3+10,10+i*350/3+10))
    #Récupération des coordonnées de la souris
    mouse = pg.mouse.get_pos()
    if isFinish(Grille)==True:
        mouse=[0,0]
        screen.blit(Fin,(0,0))

    #MAJ ecran
    pg.display.flip()


    for event in pg.event.get():
        if event.type == pg.QUIT :
            running=False
            pg.quit()
        if event.type == pg.MOUSEBUTTONDOWN :
            for i in range(3):
                for j in range(3):
                    if 85+j*350/3<mouse[0]<j*350/3+85+100 and 20+i*250/3<mouse[1]<20+i*350/3+100:
                        Jouer([i,j],AQuiDeJouer(Grille))
            if 75<mouse[0]<175 and 400<mouse[1]<423 :
                joueur=AQuiDeJouer(Grille)
                Jouer(BonCoup(Grille,joueur)[0],joueur)
            if 200<mouse[0]<300 and 400<mouse[1]<430 :
                joueur=AQuiDeJouer(Grille)
                Jouer(CoupHasard(Grille,joueur),joueur)




















#Création de la base de données



#for j in range (100):

 #   Grille=[[random.randint(-1,1) for i in range (3)] for j in range(3)]
  #  Grille=np.array(Grille)
#
 #   while isReel(Grille)==False or AQuiDeJouer(Grille)!=1 or isFinish(Grille)==True:
  #      Grille=[[random.randint(-1,1) for i in range (3)] for j in range(3)]
   #     Grille=np.array(Grille)
    #print(Grille)
    #Vecteur=[]
    #for val in Grille:
    #    for val2 in val:
    #        Vecteur.append(val2)
    #MeilleurCoup=BonCoup(Grille,1)[0]
    #NumeroCoup=MeilleurCoup[0]*3+MeilleurCoup[1]+1
    #f.write(str(Vecteur))
    #f.write(","+str(NumeroCoup))
    #f.write("\n")
#f.close()




