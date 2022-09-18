# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain


import pygame
from matplotlib import pyplot as plt

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

from strategies import *


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'blottoMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player

def main():
    nbCampagne=40 #Nombre de campagnes dans la simulation 
    #for arg in sys.argv:
    nbJours = 40 # dpar défaut, chaque campagne contient 40 jours 
    if len(sys.argv) == 2:
        nbJours = int(sys.argv[1])
    print ("nbJours: ")
    print (nbJours)


    init()



    #-------------------------------
    # Initialisation
    #-------------------------------

    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize


    players = [o for o in game.layers['joueur']] #Chargement de tout les joueurs dans une liste appelé players 
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")



    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players] #"Liste contenant les coordonées initiales de chaque joueur 
    #print ("Init states:", initStates)


    #Division des joueurs en 2 équipes 
    eq1=[] #partie1
    eq2=[] #partie2
    for p in range(len(players)): #Parcourir tout les joueurs 
        if initStates[p][1]==9: #Les joueurs a gauche dans leurs emplacement initiale ont x=9 dans leur coordonée sont dans l'équipe 1 
            eq1.append(players[p])
        else:
            eq2.append(players[p]) #Les joueurs a droite dans leurs emplacement initiale ont x=10 dans leur coordonée sont dans l'équipe 2 

    # on localise tous les secteurs d'interet (les votants)
    # sur le layer ramassable
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    #print ("Goal states:", goalStates)


    # on localise tous les murs
    # sur le layer obstacle
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)

    def legal_position(row,col):
        # une position legale est dans la carte et pas sur un mur
        return ((row,col) not in wallStates) and row>=0 and row<nbLignes and col>=0 and col<nbCols


    g =np.ones((nbLignes,nbCols),dtype=bool)  # par defaut la matrice comprend des True
    for w in wallStates:            # putting False for walls
        g[w]=False




    #-------------------------------
    # Boucle principale de déplacements
    #-------------------------------


    posPlayers = initStates


    dRepartitionA=dict()
    dRepartitionB= dict()


    stratA=StrategieAleatoire(eq1,goalStates) #Generation de la strategie tetu qui va etre utilisé tout au long de la simulation 

    #Scores initiliasés a 0 au debut des campagnes 
    Score_CampA=0
    Score_CampB=0
    nb_parties_egales=0 #Parties egales 
    histo=[] #Initialisation de la liste pour la construction de l'histogram 

    for c in range(nbCampagne): #Parcours des campagnes 
        print("Campagne ",c)
        lTermine=[] #Liste contenant les joueurs qui sont deja arrivés a leurs buts 

        #Initialisation du nombre de points pour les journees 
        pointsA=0
        pointsB=0

        for o in goalStates: #Dictionaire contenant le nombre de joueurs qui sont arrivés a chaqur but pour chaque équipe 
            dRepartitionA[o]= 0
            dRepartitionB[o]= 0

        tabA=StrategieTetu(stratA)
        if c==0: #Au debut, meme le joueur qui joue la strategie Mailleur équipe joue aleatoirement 
            tabB=StrategieAleatoire(eq2,goalStates)
        else:
            tabB=StrategieMeilleureReponse(strategiePrecAdv,goalStates)



        tab=[x[i] for i in range(len(eq1)) for x in [tabA,tabB]] #Join des buts des joueurs des deux equipes 


        strategiePrecAdv=tabA #Stock de la strategie precedente du joueurs adversaire pour l'utiliser lors du prochain appel a la strategie meilleur reponse


        paths=[] #Liste contenant les paths pour tout les joueurs vers leurs buts 
        for i in range(nbPlayers):
            p = ProblemeGrid2D(initStates[i],tab[i],g,'manhattan')
            path = probleme.astar(p)
            paths.append(path)
            #print ("Chemin trouvé:", path)


        for i in range(nbJours): #Parcours des jours pour chaque campagne 

            # on fait bouger chaque joueur séquentiellement

            for j in range(nbPlayers): #Parcours des joueurs 
                if players[j] not in lTermine : #Si le joueur n'est pas arrivé a son but, il doit se déplacer sinon il ne se déplace pas 
                    row,col = paths[j][i]
                    posPlayers[j]=(row,col)
                    players[j].set_rowcol(row,col)
                    if paths[j][i] == tab[j]:
                        lTermine.append(players[j])
                        initStates[j]=tab[j]
                        #incrementation des scores 
                        if players[j] in eq1:
                            dRepartitionA[tab[j]]+=1 
                        else:
                            dRepartitionB[tab[j]]+=1
            # on passe a l'iteration suivante du jeu
            game.mainiteration()

        #comparaison points chaque equipe

        for o in goalStates:
            if dRepartitionA[o]>dRepartitionB[o]:
                pointsA+=1
            elif dRepartitionB[o]>dRepartitionA[o]:
                pointsB+=1
        #Incrementation des points pour la partie qui a gagné la campagne 
        if pointsA > pointsB:
            Score_CampA+=1
            histo.append("Camp A")
        elif pointsA < pointsB:
            Score_CampB+=1
            histo.append("Camp B")
        else:
            nb_parties_egales+=1
            histo.append("Égalité")

        print("Le parti A a remporté : ",Score_CampA," points dans la campagne\n")
        print("Le parti B a remporté : ",Score_CampB," points dans la campagne\n")
        print("Parties egales: ",nb_parties_egales,"\n")
        
    # Affichage de l'histogram 
    plt.hist(np.array(histo), bins=3, color='red')

    plt.title("MeilleureReponse VS Tetu")
    plt.xlabel('Répartition des points')
    plt.ylabel('Nombre de campagnes')

    plt.show()



    pygame.quit()




    #-------------------------------









if __name__ == '__main__':
    main()
