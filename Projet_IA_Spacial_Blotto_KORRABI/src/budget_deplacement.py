def play_v1(players, val_budget, paths):
    """Fonction qui prends en argument la liste des joueurs, la valeure du budget par joueur et la liste des paths pour arriver au but. Elle renvoie la liste des joueurs
    qui peuvent arriver a leurs buts sous contrainte de budget""" 
    CanPlay=[]
    for p in range(len(players)):
        if len(paths[p])< val_budget:
            CanPlay.append(players[p])
    return CanPlay, len(CanPlay)

def play_v2(players, budget_camp, paths):
        """Fonction qui prends en argument la liste des joueurs, la valeure du budget par campagne et la liste des paths pour arriver au but. Elle renvoie la liste des joueurs
    qui peuvent arriver a leurs buts sous contrainte de budget de campagne""" 
    can_play=[]
    somme=len(paths[0])
    i=0
    print(len(paths))
    while somme<= budget_camp:
        can_play.append(players[i])
        i+=1
        if i>= len(paths):
            break
        somme+=len(paths[i])
    return can_play, len(can_play)
