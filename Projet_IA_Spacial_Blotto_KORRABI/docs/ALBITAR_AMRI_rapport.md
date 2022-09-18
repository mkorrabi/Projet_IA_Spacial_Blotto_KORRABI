# Rapport de projet

## Groupe
* AMRI Malek
* ALBITAR Nadia


## Description des choix importants d'implémentation

### Fichiers disponibles : 

Dans docs : rapport ALBITAR_AMRI_rapport.md, fichiers png : histogrammes des résultats de score des tests

Dans src : strategies.py (contient les stratégies et des fonctions utilisées avec les stratégies), budget_deplacecement.py : fonctions pour la simulation avec budget de déplacements, les tests (ex : MeilleurVSTêtu.py) : main à lancer pour générer un test des deux stratégies donnés dans le nom du fichier.

### Le fichier MeilleureVSTêtu.py contient des commentaires avec les explications plus en détail du déroulement d'un test classique

### Stratégies :

**Aléatoire :** Fonction prenant en argument la liste des joueurs ainsi que celle des objectifs. Elle range les objectifs aléatoirement pour tous les joueurs et renvoie la liste aleatoire finale. 

**Têtu :** renvoie la stratégie en argument. Appelée à chaque nouvelle campagne : renvoie toujours la même stratégie, choisie aléatoirement avec le lancement des campagnes.

**MeilleureRéponse :** récupère la répartition des objectifs grâce à l'analyse de la stratégie précédente de l'adversaire. 

Cette répartition est classée par ordre croissant pour récupérer le plus grand nombre de militant alloué à un objectif. 

Ce nombre est réparti entre les autres objectifs, de manière croissante, en ajoutant +1 à chaque objectif. S'il reste des points, on l'alloue au dernier objectif. 
La répartition retrouve ensuite sont ordre d'origine ce qui permet de générer la nouvelle stratégie.

**Stochastique expert :** prend une liste de stratégies pertinentes et une autre liste avec leur probabilité d'apparition (en ordre croissant). 

La liste des stratégie a été établi par simulation (inspiration du td 2) : seules les meilleures ont été gardé.

Ces listes sont définies en dehors de la stratégie. Choix de la stratégie en générant un nombre aléatoirement et en choississant la stratégie dont la probabilité est la plus proche de ce nombre.

**Fictitious play :** fonction qui prends en argument la liste de l'historique des strategies jouées par l'adversaie ainsi que la list d'objectifs et le nombre de joueurs. Elle fait appel a la strategie Mailleur Reponse pour trouver les meilleur coup a jouer contre chaque strategie dans la liste ls_historique. Ensuite, elle crée la grille des scores en suivant les regles du jeu a somme nulle. Elle calcule les gain éspérés de tout les coups renvoyés par Meilleure Reponse et elle renvoie la strategie ayant le plus grand gain éspéré.  

**PasSiTêtu :** Fonctionne de la même manière de têtu tant que la stratégie utilisée n'est pas battue. Si c'est le cas, on choisit une nouvelle stratégie aléatoirement.

**Imitation :** Imite l'adversaire en reprenant sa dernière stratégie utilisée si celle-ci avait battu la nôtre. Si ce n'est pas le cas, on garde notre stratégie précédente.


### Fonctions :
**UpdateListProb :** Utilisée avec Stochastique expert. Permet de mettre à jour la liste des stratégies pertinentes si l'une d'entre elle s'avère gagne contre celle de l'adversaire. Cette mise à jour s'effectue en échangeant sa place dans la liste avec la stratégie suivante : elle récupère donc la probabilité correspondante (plus élevée).

**transformer:** Foction qui prends en argument la liste des coups a trasformer et la liste des objectifs. 
Exemple de transformation faite: 
liste_coups= [(1,1), (1,1), (16, 18), (1, 8), (6,1)] 
objectifs= [(16, 18), (1,1), (6,1), (1, 8), (8, 3)]
la liste renvoyé par la fonction: [1, 2, 1, 1, 0]
Cette liste nous sera utile lors du calcul des gains 

**generateGains(ls_historique, coups) :** Foction prenant en arguments une liste de tout les coups joués par l'adversaire dans les jours précédents ainsi
que les coups possible renvoyés par la fonction meilleure reponse. ces deux listes ont été transformé grace a la fonction "transformer". la fonction calcule le 
score du joueur. 1 si il gagne, 0 si c'est une égalité et -1 si il perd. 

**trouver_gains_esperes:** Fonction qui calcule le gain éspére pour chaque coup possible.  Elle prends en argumet la grille des scores, la liste contenant le nombre de fois qu'une stratégie a été utilisé par l'adversaire historique_repeat, la liste des coups, la liste 
des coups aprés transformation par la fonction "transformer" et le nombre de jours totale. Cette fonction parcour la liste des coups et calcule le gai éspéré pour chaque coup.
proba= probabilite du coup joué par l'adversaire 
Formule gain éspéré: la somme des probabilités fois le gain (0, 1 ou -1) associé dans la grille 
La fonction renvoie un dictionnaire ayant tous les coups comme clés et le gain éspéré associé comme valeures. 


### Fonctions dans budget :

Les fonctions faite pour la partie 3 du projet se trouvent dans le fichier budget_deplacement.py 

**play_v1:** Fonction prenant en argument la liste des joueurs, la valeure de budget de déplacement associé a chaque joueur. La
fonction parcours la liste des joueurs et vérifie la longeur du path pour arriver a son but. si la longeure du path (nombre de pas) pour arriver au but est plus 
grande que la valeure du budget, donc le joueur ne piurra pas jouer, sinon, il pourra jouer. la fonction renvoie une liste des joueurs qui peuvent jouer et ainsi que sa longeure. 

**play_v2 :** Fonction prenant en argument le nombre de pas maximum pour toute la campagne, la liste des joueurs et leurs paths. Elle parcours la liste des joeurs et incremente un compteur de la valeure de leurs path associé tant que ce compteur ait une valeure inférieure a budget_camp. Le parcours s'arrete une fois cette valeure dépassé. Elle ajoute les joueurs parcouru a une liste au fur et a mesure. A la fin du parcours, la liste des joueurs qui peuvent jour ainsi que sa longeure sont renvoyés. 

## Description des résultats

### Tests :
Réalisés sur 40 campagnes de 40 jours.

Score = nombre de campagnes gagnées.

Histogrammes : voir fichiers .png avec noms correspondants. Exemple : Meilleure réponse VS Aléatoire, voir MeilleureVSAléatoire.png

**Meilleure réponse VS Aléatoire :**

Identifiation des stratégies :

Camp A : Aléatoire

Camp B : Meilleure réponse


Scores:  

Camp A = 9

Camp B = 11

Égalité = 20

Victoire de la stratégie meilleure réponse. Néanmoins, elle n'est pas si efficace si la stratégie adverse est aléatoire (et donc change à chaque nouvelle campagne).
La stratégie générée pour battre la stratégie précédente peut ne pas être efficace contre la nouvelle stratégie aléatoire. On note tout de même qu'il s'agit d'une amélioration d'une stratégie, ce qui la rend potentiellement plus forte ou permet, au moins, de rivaliser avec l'aléatoire.

**Têtu VS Aléatoire :**

Identifiation des stratégies :

Camp A : Aléatoire

Camp B : Têtu


Scores:  

Camp A = 7

Camp B = 11

Égalité = 22

Les joueurs tetu ont gagné le jeu. Cela peut etre du hasard vu que les strategies sont générés aléatoirement. les strategies générés peuvent etre toutes moins puissantes que celle utilisé par tetu 

**Têtu VS Imitation :**

Identifiation des stratégies :

Camp A : Têtu

Camp B : Imitation


Scores:  

Camp A = 0

Camp B = 0

Égalité = 40

Ici, les deux camps sont toujours à égalité. Le camp B a imité la stratégie du coup A après avoir égalisé avec celle-ci au premier tour. En règne général, le camp A peut gagner un point au début mais est ensuite imité, ce qui provoque des égalités pour le reste de la campagne.
La stratégie imitation n'est donc pas intéressante si l'adversaire utilise la stratégie têtu.

**Têtu VS Meilleure réponse :**

Identifiation des stratégies :

Camp A : Têtu

Camp B : Meilleure réponse


Scores:  

Camp A = 1

Camp B = 39

Égalité = 0

Meilleure réponse plus efficace car elle renvoie une stratégie permettant de battre la stratégie donnée par têtu.


**Têtu VS Pas si têtu :**

Identifiation des stratégies :

Camp A : Têtu

Camp B : Pas si Têtu


Scores:  

Camp A = 1

Camp B = 37

Égalité = 2

Stratégie pas si têtu efficace contre têtu : même si elle perd un peu, elle peut rebondir immédiatement en générant une nouvelle stratégie aléatoire lui donnant une nouvelle chance de battre l'adversaire.
 

**Têtu VS Fictitious play :**

Identifiation des stratégies :

Camp A : Têtu

Camp B : Fictitious play


Scores:  

Camp A = 1

Camp B = 39

Égalité = 0

Stratégies fictitious play très efficace contre têtu. Têtu utilise la meme strategie tout au long de la campagne et fictitious play renvoie une meilleure strategie a chaque appel en utilisant la strategie "Meilleure réponse" et en calculant le gain éspéré c'est pour cette raison que cette derniere gagne beaucoup plus de campagnes. 

**Stochastique VS Imitation :**

Identifiation des stratégies :

Camp A : Stochastique expert

Camp B : Imitation


Scores:  

Camp A = 3 

Camp B = 10

Égalité = 27

La stratégie imitation efficace contre stochastique expert : l'imite quand elle a une bonne stratégie. Inconvénient : ne permet pas forcément de gagner mais de rapprocher les scores (beaucoup d'égalité).

**Stochastique VS Meilleure réponse :**

Identifiation des stratégies :

Camp A : Stochastique expert

Camp B : Meilleure Réponse


Scores:  

Camp A = 3 

Camp B = 25

Égalité = 12

La stratégie stochastique expert est dominée par la stratégie meilleure réponse.
En effet, si elle peut gagner au début, cela induit que la probabilité de tomber sur la même stratégie (dans la liste des stratégies pertinentes) augmente avec la mise à jour qui suit.
Or, meilleure réponse peut donc générer une stratégie lui permettant de la battre.

**Stochastique VS Fictitious play :**

Identifiation des stratégies :

Camp A : Stochastique expert

Camp B : Fictitious play


Scores:  

Camp A = 21

Camp B = 3

Égalité = 16

La stratégie stochastique expert domine légèrement celle de fictitious play (beaucoup d'égalité donc pas de domination totale).
Cela peut s'expliquer par le choix des stratégies pertinentes (qui sont très efficaces) et la mise à jour de ses stratégies en cas de victoire, ce qui renforce la stratégie stochastique expert.

### Tests avec budget

**Stochastique VS Fictitious play avec budget première variante:**

Identifiation des stratégies : 

Camp A : Stochastique expert

Camp B : Fictitious play


Scores:  

Camp A = 23

Camp B = 0

Égalité = 17

Seulement le joueurs ayant un path de longeure inferieur au budget individuel ont pu jouer 

**Stochastique VS Fictitious play avec budget deuxième variante:**

Identifiation des stratégies :

Camp A : Stochastique expert

Camp B : Fictitious play


Scores:  

Camp A = 1

Camp B = 39

Égalité = 0

Seulement le joueurs pour lesquels la somme des longeurs des paths est inférieur au budget de la campagne ont pu jouer 


