from classe_reseau_neuronnes.network import*
from console_et_robots.calcul_angle import*
from math import sin, cos
import entrainement.parametre as parametre

# parametres[i][0], pod_j2_a, pod_j2_b, boost_j2, pod_j1_a, pod_j1_b, boost_j1, carte

def norm_ang(a):
    return normalized(a)/18
def norm_dist(d):
    return d/5000
def norm_vit(v):
    return v/500

##### Bot global : 

# on fait un truc propre : 
# on fait des noeuds de sortie qui sont en parallèles (i.e. indépendants des autres noeuds de sortie)
# on rajoute dans le réseau la possibilité de modifier un lien (a la place de l'entrée de certains input dans un noeud, on retire leur pondération et on la remplace par un noeud intermédiaire)

# P 0 : on entraine les premiers neurones (rapidement sur 4 inputs : angle cp, distance cp ,vitesse, angle vitesse)
# P 1 : on rajoute rapidement les bots de defense, qui sont simplement deux neurones supplémentaires au même raiseau
# P 2 : on rajoute rapidement la capacité de shield (avant que il y ait trop de noeud intermédiaire pour les 2 bots) -> 6 noeuds finaux
# P 3 : on rajoute le noeud de boost. 

# On rajoute full noeud intermédiaires pour faire des courses de plus en plus rapide ou les pods tiennent en compte les uns des autres.
# Inchallah ca donne un résultat pas trop mal


# Liste d'input : 

# -> par rapport au bot attaque : 
# position des autres bots (6 inputs) -> initialement pas car dépend uniquement de la position
# position du nextCP, du CP+1, du CP+2
# boost disponible ?
# nombre de CP avant la fin du jeu

# -> par rapport au bot de défense : 
# position des autres bots par rapport à lui
# (position des autres pods par rapport au bot d'attaque => déja dans les inputs du bot d'attaque) 
# (boost disponible => déja dans les inputs du bot d'attaque)
# boost adverse disponible
# position du CP, CP+1, CP+2, CP+3 par rapport au pod atttaque adverse et par rapport au bot 
# nombre de CP de l'adversaire restant

# Liste output : 

# bot d'attaque  : utilisation du boost, puissance, shield, angle
# bot de defense : utilisation du boost, puissance, shield, angle


    
def liste_bot_defense(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte):
    x,y = pod_b[2], pod_b[3]
    x_opp, y_opp =  pod_adversaire_a[2], pod_adversaire_a[3]
    
    dist_opponent = norme(x_opp - x, y_opp - y)
    ang_opponent = angle(x_opp - x, y_opp - y) - pod_b[6]

    cp1x, cp1y = carte[pod_adversaire_a[1]]
    cp_adv_1_dist_hero = norme(cp1x - x, cp1y- y)
    cp_adv_1_ang_hero = angle(cp1x - x, cp1y- y) - pod_b[6]

    vx_hero, vy_hero = pod_b[4], pod_b[5]
    v_hero = norme(vx_hero, vy_hero)
    ang_hero = angle(vx_hero, vy_hero) - pod_b[6]

    vx_opp, vy_opp = pod_adversaire_a[4], pod_adversaire_a[5]
    v_opp = norme(vx_opp, vy_opp)
    ang_opp = angle(vx_opp, vy_opp) - pod_b[6]

    cp2x, cp2y = carte[(pod_adversaire_a[1]+1)%len(carte)]
    cp_adv_2_dist_hero = norme(cp2x - x, cp2y- y)
    cp_adv_2_ang_hero = angle(cp2x - x, cp2y- y) - pod_b[6]

    l = [
        norm_dist(dist_opponent),
        norm_ang(ang_opponent), 

        norm_dist(cp_adv_1_dist_hero),
        norm_ang(cp_adv_1_ang_hero), 

        norm_vit(v_hero),
        norm_ang(ang_hero), 

        norm_vit(v_opp),
        norm_ang(ang_opp), 

        norm_dist(cp_adv_2_dist_hero),
        norm_ang(cp_adv_2_ang_hero)
        ]
    
    return l

#### ATTAQUE
def liste_bot_attaque(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte): 
    x, y, next_cp_x, next_cp_y = pod_a[2], pod_a[3], carte[pod_a[1]][0], carte[pod_a[1]][1]
    deltx, delty = next_cp_x-x, next_cp_y - y
    vx, vy = pod_a[4], pod_a[5]
    ang_cp = angle(deltx, delty)

    cp_suiv_1_x, cp_suiv_1_y = carte[(pod_a[1]+1)%len(carte)][0]-carte[pod_a[1]][0], carte[(pod_a[1]+1)%len(carte)][1]-carte[pod_a[1]][1]
    dist1 = norme(cp_suiv_1_x, cp_suiv_1_y)
    ang_1 = angle(cp_suiv_1_x, cp_suiv_1_y) - ang_cp

    cp_suiv_2_x, cp_suiv_2_y = carte[(pod_a[1]+2)%len(carte)][0]-carte[(pod_a[1]+1)%len(carte)][0], carte[(pod_a[1]+2)%len(carte)][1]-carte[(pod_a[1]+1)%len(carte)][1]
    dist2 = norme(cp_suiv_2_x, cp_suiv_2_y)
    ang_2 = angle(cp_suiv_2_x, cp_suiv_2_y) - ang_cp

    opp_x, opp_y = pod_adversaire_b[2], pod_adversaire_b[3]
    dist_opp = norme(opp_x - x, opp_y - y) 
    ang_opp = angle(opp_x-x, opp_y-y) - ang_cp

    opp_vx, opp_vy = pod_adversaire_b[4], pod_adversaire_b[5]
    vit_opp = norme(opp_vx, opp_vy)
    ang_vit_opp = angle(opp_vx, opp_vy) - ang_cp

    l = [norm_ang(pod_a[6] - ang_cp),
         norm_dist(norme(deltx, delty)),

         norm_vit(norme(vx, vy)),
         norm_ang(angle(vx, vy) - ang_cp),

         norm_dist(dist1),
         norm_ang(ang_1),

         norm_dist(dist2),
         norm_ang(ang_2), 
         
         norm_dist(dist_opp),
         norm_ang(ang_opp), 
         
         norm_vit(vit_opp),
         norm_ang(ang_vit_opp)]
    
    return l


def bot_global(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False): 

    ### ATTENTION AUX INPUTS SELECTIONNES AVEC LES FONCTION parametre.inputs_attaque_utilise et inputs_defense_utilise
    l = []
    l += parametre.inputs_attaque_utilise(liste_bot_attaque(ntw, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte))
    l += parametre.inputs_defense_utilise(liste_bot_defense(ntw, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte))

    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")

    ntw.set_input(l)
    (
        ang_pod_attaque,
        speed_pod_attaque,
        shield_pod_attaque,
        boost_pod_attaque, 
        ang_pod_defense,
        speed_pod_defense,
        shield_pod_defense,
        boost_pod_defense
    ) = ntw.get_output()

    x_attaquant, y_attaquant = pod_a[2] + cos(ang_pod_attaque*pi/10+pod_a[6]*pi/180) * 10000, pod_a[3] + sin(ang_pod_attaque*pi/10+pod_a[6]*pi/180) * 10000
    x_defenseur, y_defenseur = pod_b[2] + cos(ang_pod_defense*pi/10+pod_b[6]*pi/180) * 10000, pod_b[3] + sin(ang_pod_defense*pi/10+pod_b[6]*pi/180) * 10000

    if parametre.shield_active_attaquant and shield_pod_attaque>0.5:
        pow_attaquant = "SHIELD"
    elif parametre.boost_active_attaquant and boost_pod_attaque>0.5:
        pow_attaquant = "BOOST"
    else:
        pow_attaquant = 100*speed_pod_attaque
    
    if parametre.shield_active_defenseur and shield_pod_defense>0.5:
        pow_defenseur = "SHIELD"
    elif parametre.boost_active_defenseur and boost_pod_defense>0.5:
        pow_defenseur = "BOOST"
    else:
        pow_defenseur = 100*speed_pod_defense

    return ((x_attaquant, y_attaquant, pow_attaquant), (x_defenseur,y_defenseur,pow_defenseur))


#def liste_input_totaux