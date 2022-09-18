import random
import operator
import numpy as np
from collections import Counter
from math import inf

def StrategieAleatoire(Players,objectifs):
    """Fonction qui renvoie une liste des objectifs choisi aleatoirement pour
    chacun des joueurs"""
    random.shuffle(objectifs)
    tab=[]
    for i in range(len(Players)):
        tab.append(objectifs[random.randint(0,4)])
    return tab

def StrategieTetu(strategie):
    """Fonction qui prends en argument la strategie choisie et renvoie un tableau contenant
    cette strategie nbJours fois"""
    #dictElecteurs=dict()
    #for n in nbChamps:
    #    dict[n]=objectifs[n]

    if strategie != []:
        return strategie


def StrategieMeilleureReponse(strategiePrecAdv,objectifs):
    """Fonction prenant en argument la stratégie précédente de l'adversaire ainsi que la liste des objectifs à atteindre
    Elle retourne une stratégie permettant de battre la stratégie précédente de l'adversaire (une meilleure réponse)"""
    #recuperation des repartitions
    repartitionPrecAdv=[]
    for o in range(len(objectifs)):
        cpt=0
        for s in range(len(strategiePrecAdv)):
            if strategiePrecAdv[s]==objectifs[o]:
                cpt+=1
        repartitionPrecAdv.append(cpt)


    sorted_index= np.argsort(repartitionPrecAdv)
    repartitionPrecAdv=np.array(repartitionPrecAdv)
    sorted_repart=repartitionPrecAdv[sorted_index]


    ajout=sorted_repart[len(sorted_repart)-1]

    for s in range(len(sorted_repart)):
        if s !=len(sorted_repart)-1 and ajout>0:
            sorted_repart[s]+=1
            ajout-=1
        elif s==len(sorted_repart)-1 and ajout>=0:
            sorted_repart[s]=ajout
            ajout=0


    #remettre dans ordre objectifs
    un_sort=np.argsort(sorted_index)
    unsorted_repart=sorted_repart[un_sort]



    tab=[]
    for u in range(len(unsorted_repart)):
        temp=unsorted_repart[u]
        while temp>0:
            tab.append(objectifs[u])
            temp-=1

    return tab



def StrategieStochastiqueExp(objPertinent, listeProb):
    """Fonction prenant en argument une liste de k repartitions pertinantes.
    Elle retourne une des repartition selon des probabilités prédifinies dans listeProb qui
    est passé en argument"""
    #on suppose que les probabilité sont en ordre croissant
    #Generation aleatoire de la probabilité:
    p= random.uniform(0, 1)
    while p>listeProb[len(listeProb)-1]:
        p= random.uniform(0, 1)
    for i in range(len(listeProb)):
        if i==0:
            if p<listeProb[i]:
                return objPertinent[i]
        elif p<listeProb[i] and p>listeProb[i-1]:
            return objPertinent[i]


def UpdateListProb(objPertinent,listeProb,strategiePrec,scorePrec):
    """Fonction prenant en argument une liste de stratégies pertinentes, la liste de probabilité d'apparition associée, la stratégie précédente du joueur et son score associé.
    Elle met à jour liste de stratégies pertinentes ou la liste de probabilité si la stratégie précédente s'est avérée efficace (gagnante contre l'adversaire).  """
    if scorePrec>0:
        for i in range(len(objPertinent)):
            if objPertinent[i]==strategiePrec:
                if i!=len(objPertinent)-1:
                    temp=objPertinent[i+1]
                    objPertinent[i+1]=strategiePrec
                    objPertinent[i]=temp
                


def StrategiePasSiTetu(strategiePrec,scorePrec, Players,objectifs):
    """"Fonction prenant en argument la stratégie précédente du joueur, le score de la campagne précédente du joueur (nombre de points qu'il a gagné/perdu) ,ses militants et la liste des objectifs à atteindre.
    Elle retourne la même stratégie que précédemment si celle-ci le fai gagner, sinon elle retourne une nouvelle stratégie aléatoire"""
    if scorePrec<=0:
        return StrategieAleatoire(Players,objectifs)
    else:
        return strategiePrec


def StrategieImitation(strategiePrecAdv,strategiePrec,scorePrec):
    """ Fonction prenant en argument la stratégie précédente de l'adversaire, la stratégie précédente du joueur et le score associé.
    Elle retourne la stratégie précédente de l'adversaire si celle-ci est bat celle du joueur, sinon elle garde la stratégie utilisée précédemment"""
    if scorePrec<=0:
        return strategiePrecAdv
    return strategiePrec

def generateGains(ls_historique, coups):
    """ Fonction prenant en argument la liste de l'historiaue de l'dversaire et le coups du coueur courant. elle calcule les gain et renvoie un
    dictionnaire contenant les gain pour chaque couple (coup_adversaire, coup_joueur)"""
    grille= dict() #dictionnaire prenant comme cles les couples de coups possible et le gain comme valeure
    for i in coups:
        #Pour chaque coup possible, trouver le gain
        for j in ls_historique:
            gain = 0
            for k in range(len(j)):
                if i[k]> j[k]:
                    gain +=1 #le joueur gagne
                elif i[k] < j[k]:
                    gain -=1
            # Nous avons le gain pour le couple (i, j)
            if gain > 0:
                grille[(tuple(i), tuple(j))]= 1
            elif gain < 0:
                grille[(tuple(i), tuple(j))]= -1
            else:
                grille[(tuple(i), tuple(j))]= 0
    return grille

def trouver_gains_esperes(grille,  historique_repeat, coups, coup_transform, nb_jours):
    """Fonction qui calcule le gain éspére pour chaque coup possible. Elle prends en argumet la grille des scores, 
    la liste contenant le nombre de fois qu'une stratégie a été utilisé par l'adversaire historique_repeat, la liste des coups, 
    la liste des coups aprés transformation par la fonction "transformer" et le nombre de jours totale. Elle renvoie les gains éspérés pour chaqye coup """
    gains_esperes=dict()
    for i in range(len(coups)):
        s= 0
        cpt=0
        for g in grille: #chercher toutes les posibilités dans la grille contre lequelles le coup i pourra jouer
            if g[0]==coup_transform[i]:
                cpt+=1 #pour optimiser le parcours du dictionnaire
                proba =  historique_repeat[g[1]]/nb_jours
                s+= proba*grille[g] #pour faire la somme du gain esperé
            if cpt==len(historique_repeat): #on arrete le parcours de la grille une fois arrivé au nombre maximum de coups adv possibles
                break
        gains_esperes[tuple(coups[i])]=s
    return gains_esperes

def transformer(liste_coups, objectifs):
    """Fonction prenant en argument une liste de coups et une liste d'objectifs et elle renvoie une liste d'entiers representant le nombre d'agents ayant un but
    dans la liste des objectifs"""
    ltot=[]
    for i in liste_coups:
        d= dict()
        for key, val in Counter(i).items():
            d[key]= val
        lsous=[]
        for j in objectifs:
            if j in d.keys():
                lsous.append(d[j])
            else:
                lsous.append(0)
        ltot.append(lsous)
    return ltot


def StrategieFictitiousPlay(ls_historique, objectifs, nbPlayers):
    """Fonction prenant en argument la liste de touts les strategies joués par le
    joueur adversaire et retournant la repartition adequate"""
    
    historique_transform= transformer(ls_historique, objectifs)

    #Appel a la fonction meilleur reponse pour construire les coups possibles du joueur
    historique_repeat=dict()
    uniq=[]
    coups=[]
    for i in range(len(ls_historique)):
        if not (historique_transform[i] in uniq):
            historique_repeat[tuple(historique_transform[i])]=1
            uniq.append(historique_transform[i])
            coups.append(StrategieMeilleureReponse(ls_historique[i], objectifs))
        else:
            historique_repeat[tuple(historique_transform[i])]+=1 #Combien de fois ce coup a ete joué par ladversaire

    #Pour la creation de la grille, on doit transformer les coups en une liste d'entiers

    coups_transforme= transformer(coups, objectifs)


    #Creation du tableau de gains: jeu a somme nulle donc 1, 0 ou -1
    grille = generateGains(historique_transform, coups_transforme)

    #Calculer le gain éspéré
    gains_esperes= trouver_gains_esperes(grille, historique_repeat, coups, coups_transforme, len(ls_historique))


    #Trouver le coup ayant le mailleur gain esperé

    maxi= -inf
    best_coup=0
    if len(gains_esperes)==1:
        best_coup=list(gains_esperes.keys())[0]
    else:
        for k in gains_esperes:
            if gains_esperes[k]>maxi:
                best_coup= list(k)
                maxi= gains_esperes[k]


    return best_coup
