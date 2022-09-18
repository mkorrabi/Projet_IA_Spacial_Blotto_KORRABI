# spatial-blotto
Spatial version of the Colonel Blotto game. Undergrad project (L3) at Sorbonne Univ. 2021-2022

## Présentation générale du projet

On se propose d'étudier une variante du problème du Colonel Blotto qui sera vu en TD en semaine 2.
Deux partis à une élection s'affrontent. On suppose qu'ils disposent du même nombre total de **militants**.  
Chaque parti doit décider d'allouer ses équipes de campagnes pour convaincre différents **électeurs**.
On suppose que le vote d'une électrice ou d'un électeur est remporté par le parti qui a alloué le plus de militants pour la ou le convaincre.

La variante que vous allez étudier est **itérée** et **spatialisée**:
* on suppose qu'une **campagne** se déroule sur plusieurs **jours**. Chaque jour, les équipes de militants se focalisent sur le même ensemble d'électeurs qui sont localisés dans des secteurs de la ville (par ex. des quartiers). Le jour d'après, les deux partis s'affrontent sur un autre ensemble d'électeurs qui peuvent être dans les mêmes secteurs ou pas, etc.
* on supposera dans un deuxième temps que les militants se déplacent de secteurs en secteurs et que ces déplacements ont un coût qui devra être pris en compte dans la stratégie.

Il est important de noter que les partis effectuent leur choix d'allocation après avoir pris connaissance de l'endroit où se situent les électrices et électeurs, chaque jour. Pour chaque parti, l'espace des stratégies est donc l'ensemble des allocations possible des militants aux électeurs. Cet ensemble de stratégies est donc potentiellement très grand.

Le parti qui a convaincu le plus d'électrices et électeurs à la fin de la campagne remporte l'élection.

## Exemple

Supposons que les deux partis A et B disposent de m=7 militants, à répartir pour convaincre 5 électeurs.

**Premier jour**:

| e1 | e2 | e3 | e4 | e5 |
|---|---|---|---|---|
| a1 | a2, a3 | | a4, a5 | a6, a7 |
| b1 | b2 | b3,b4, b5| b6 | b7 |

A l'issue du premier jour, on voit que e1 n'est remporté par aucun parti qui ont mobilisé chacun 1 militant, que e2 est remporté par le parti A (2 vs. 1), e3 par B (0 vs. 3), e4 par A (2 vs. 1) et enfin e5 par A (2 vs. 1).
Le parti A a donc remporté 3 électeurs au cours de cette journée, contre 1 pour le parti B.  

**Deuxième jour**:

| e1 | e2 | e3 | e4 | e5 |
|---|---|---|---|---|
| a1 | a2,a3 | | a4,a5 | a6, a7 |
| b1, b5 | b2, b3, b4 |  |  | b6, b7 |

La journée suivante, le parti A reste sur sa même stratégie, tandis que le parti B s'adapte. Cette fois, le parti A ne remporte qu'un électeur contre 2 au joueur B.
Si la campagne s'arrêtait après ces deux journées seulement, le parti A remporterait 4 voix, contre 3 pour le parti B.   



Dans ce projet, les campagnes seront représentées de manière graphique, et les militants des partis devront se déplacer physiquement sur la carte pour aller jusqu'aux électeurs. Nous utiliserons pour cela un module spécifique.



## Module pySpriteWorld

Pour la partie graphique, vous utiliserez le module `pySpriteWorld` (développé par Yann Chevaleyre) qui s'appuie sur `pygame` et permet de manipuler simplement des personnages (sprites), cartes, et autres objets à l'écran.

Une carte par défaut vous est proposée pour ce projet (`blottoMap`): elle comporte potentiellement 10 secteurs, représentés par des zones rectagulaires délimitées par des murs en bordure de carte. Les secteurs d'intérêt seront ceux dans lesquels se trouvent un votant (personnage homme ou femme). On a ici 5 votants disposés sur certaines secteurs.  
Les militants sont initialement situés au milieu de la carte.
Les cartes utilisent au moins trois calques:

* un calque `joueur`, où seront présents les personnages (ici les militants)
* un calque `ramassable`, qui contient les "objets" que les personnages pourraient utiliser (ici les électrices et les électeurs).
* un calque `obstacles`, pour les murs, qui sont infrnachissables par les personnages et contraignent les déplacements.

Les joueurs, ramassables, et obstacles sont des objets Python sur lesquels vous pouvez effectuer des opérations classiques.
Par exemple, il est possible récupérer leurs coordonnées sur la carte avec `o.get_rowcol(x,y)` ou à l'inverse fixer leurs coordonnées avec `o.set_rowcol(x,y)`.


Notez que vous pourrez ensuite éditer vos propres cartes à l'aide de l'éditeur [Tiled](https://www.mapeditor.org/), et exporter ces cartes au format `.json`. Vous pourrez alors modifier le nombre de secteurs ou de militants comme vous le souhaitez.

**Note**: on fait ici l'hypothèse que toutes les informations (positions de toutes les électrices et électeurs, et des autres militants) sont disponibles pour tous les partis.

**Note**: les déplacements des militants ne sont pas contraints par les autres militants, ie. ils peuvent se superposer.

## Travail demandé

Un fichier de prise en main `main.py` vous est fourni. Il illustre comment deux militants peuvent se déplacer vers une électrice et un électeur choisis au hasard. Le premier trouve son chemin avec l'algorithme A*, le deuxième effectue une marche aléatoire.

### semaine 1:
Prise en main de l'environnement, permettre à **tous** les militants de choisir un électeur au hasard et de se déplacer vers celui-ci en utilisant A* (en suivant le modèle du premier joueur). Lorsque tous les militants ont atteint leur objectif, afficher le score de cette journée, c'est-à-dire le nombre de voix remportés par chaque parti.

### semaine 2 et 3:
Jeu **sans budget de déplacement**: le jeu se déroule à présent sur un nombre donné de jours de campagne. Le jour suivant de campagne, les joueurs partent de l'endroit où ils sont arrivés le jour précédent. On suppose pour le moment que les électrices et électeurs restent chaque jour dans les mêmes secteurs.
Elaborer de premières stratégies, en particulier:
1. **aléatoire**: choisit les électeurs où allouer ses militants au hasard
2. **tétu**: joue toujours la même stratégie tout au long de la campagne
3. **stochastique expert**: choisit de manière probabiliste parmi k stratégies identifiées comme pertinentes (vous pourrez ici utiliser certaines idées vues en TD)
4. **meilleure réponse**: joue une meilleure réponse à la stratégie précédente de l'autre parti
5. **fictitious play**: joue en meilleure réponse pour l'utilité espérée selon la fréquence observée des stratégies de l'autre parti (cette stratégie basée sur de l'apprentissage sera étudiée en semaine 3 de TD)
6. autres stratégies...

### semaine 3

Jeu **avec budget de déplacement**: on suppose à présent que les militants sont contraints par un budget de temps qui limite les électeurs qu'ils peuvent atteindre dans la journée. De plus, les électeurs sont réalloués au hasard dans de nouveaux secteurs chaque jour.
* Dans la première variante, on suppose que le budget est fixe pour chaque journée (par ex. 12 pas de déplacement pour chaque militant de chaque parti).
* Dans la seconde variante, on suppose que le budget concerne la campagne entière: chaque jour le parti paye comme prix la somme des trajets réalisés par ses militants dans la journée.

### semaine 4:
**Soutenances**: vous décrirez les stratégies proposées et les résultats de tests en confrontation que vous aurez pu réaliser. Par exemple, tétu contre aléatoire, stochastique expert contre fictitious play, etc.
Votre rapport devra être rédigé en Markdown et déposé dans le répertoire `docs` (voir le template `rapport.md`)


## Bibliographie

* article [Colonel Blotto](https://en.wikipedia.org/wiki/Blotto_game) sur Wikipedia
