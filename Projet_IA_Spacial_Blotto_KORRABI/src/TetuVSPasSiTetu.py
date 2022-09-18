# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme

from strategies import *

from matplotlib import pyplot as plt


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
    nbCampagne=40
    #for arg in sys.argv:
    nbJours =40 # default
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


    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    print("Trouvé ", nbPlayers, " militants")



    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    #print ("Init states:", initStates)



    eq1=[] #partie1
    eq2=[] #partie2
    for p in range(len(players)):
        if initStates[p][1]==9:
            eq1.append(players[p])
        else:
            eq2.append(players[p])

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

    pointsA=0
    pointsB=0

    stratA=StrategieAleatoire(eq1,goalStates)


    Score_CampA=0
    Score_CampB=0
    nb_parties_egales=0
    histo=[]

    for c in range(nbCampagne):
        print("Campagne ",c)
        lTermine=[]

        pointsA=0
        pointsB=0

        for o in goalStates:
            dRepartitionA[o]= 0
            dRepartitionB[o]= 0

        tabA=StrategieTetu(stratA)
        if c==0:
            tabB=StrategieAleatoire(eq2,goalStates)
        else:
            tabB=StrategiePasSiTetu(strategiePrec,score, eq2,goalStates)

        strategiePrec=tabB



        tab=[x[i] for i in range(len(eq1)) for x in [tabA,tabB]]


        strategiePrecAdv=tabA


        paths=[]
        for i in range(nbPlayers):
            p = ProblemeGrid2D(initStates[i],tab[i],g,'manhattan')
            path = probleme.astar(p)
            paths.append(path)
            #print ("Chemin trouvé:", path)


        for i in range(nbJours):

            # on fait bouger chaque joueur séquentiellement

            for j in range(nbPlayers):
                if players[j] not in lTermine :
                    row,col = paths[j][i]
                    posPlayers[j]=(row,col)
                    players[j].set_rowcol(row,col)
                    if paths[j][i] == tab[j]:
                        lTermine.append(players[j])
                        initStates[j]=tab[j]
                        if players[j] in eq1:
                            dRepartitionA[tab[j]]+=1
                        else:
                            dRepartitionB[tab[j]]+=1
            # on passe a l'iteration suivante du jeu
            game.mainiteration()



        for o in goalStates:
            if dRepartitionA[o]>dRepartitionB[o]:
                pointsA+=1
            elif dRepartitionB[o]>dRepartitionA[o]:
                pointsB+=1


        score=pointsB-pointsA

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


    plt.hist(np.array(histo), bins=3, color='red')

    plt.title("Têtu VS Pas si têtu")
    plt.xlabel('Répartition des points')
    plt.ylabel('Nombre de campagnes')

    plt.show()




    pygame.quit()




    #-------------------------------









if __name__ == '__main__':
    main()
