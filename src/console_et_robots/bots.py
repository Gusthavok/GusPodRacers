from classe_reseau_neuronnes.network import*
from console_et_robots.calcul_angle import*
from math import sin, cos

# parametres[i][0], pod_j2_a, pod_j2_b, boost_j2, pod_j1_a, pod_j1_b, boost_j1, carte

def norm_ang(a):
    return a/18
def norm_dist(d):
    return d/5000
def norm_vit(v):
    return v/500


####  DEFENSE
    # bot_defense_2 : angle distance adversaire
    # bot_defense_4 : position CP adversaire
    # bot_defense_8 : vitesse adversaire - vitesse hero
    # bot_defense_10 : position CP+1


    
def bot_defense_10(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False):
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
    

    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed, shield = ntw.get_output()

    x_dir, y_dir = x + cos(ang*pi/10+pod_b[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_b[6]*pi/180) * 10000

    if shield>0.5:
        return ((0, 0, 0), (x_dir, y_dir, "SHIELD"))

    return ((0,0,0), (x_dir, y_dir, int(100*speed)))  
    
def bot_defense_8(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False):
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


    l = [
        norm_dist(dist_opponent),
        norm_ang(ang_opponent), 

        norm_dist(cp_adv_1_dist_hero),
        norm_ang(cp_adv_1_ang_hero), 

        norm_vit(v_hero),
        norm_ang(ang_hero), 

        norm_vit(v_opp),
        norm_ang(ang_opp)
        ]
    

    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed, shield = ntw.get_output()

    x_dir, y_dir = x + cos(ang*pi/10+pod_b[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_b[6]*pi/180) * 10000

    if shield>0.5:
        return ((0, 0, 0), (x_dir, y_dir, "SHIELD"))

    return ((0,0,0), (x_dir, y_dir, int(100*speed)))  

def bot_defense_4(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False):
    x,y = pod_b[2], pod_b[3]
    x_opp, y_opp =  pod_adversaire_a[2], pod_adversaire_a[3]
    
    dist_opponent = norme(x_opp - x, y_opp - y)
    ang_opponent = angle(x_opp - x, y_opp - y) - pod_b[6]

    cp1x, cp1y = carte[pod_adversaire_a[1]]
    cp_adv_1_dist_hero = norme(cp1x - x, cp1y- y)
    cp_adv_1_ang_hero = angle(cp1x - x, cp1y- y) - pod_b[6]

    l = [
        norm_dist(dist_opponent),
        norm_ang(ang_opponent), 

        norm_dist(cp_adv_1_dist_hero),
        norm_ang(cp_adv_1_ang_hero)
        ]
    

    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed, shield = ntw.get_output()

    x_dir, y_dir = x + cos(ang*pi/10+pod_b[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_b[6]*pi/180) * 10000

    if shield>0.5:
        return ((0, 0, 0), (x_dir, y_dir, "SHIELD"))

    return ((0,0,0), (x_dir, y_dir, int(100*speed)))  

def bot_defense_2(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False):
    x,y = pod_b[2], pod_b[3]
    x_opp, y_opp =  pod_adversaire_a[2], pod_adversaire_a[3]
    
    dist_opponent = norme(x_opp - x, y_opp - y)
    ang_opponent = angle(x_opp - x, y_opp - y) - pod_b[6]

    l = [
        norm_dist(dist_opponent),
        norm_ang(ang_opponent)
        ]
    

    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed, shield = ntw.get_output()

    x_dir, y_dir = x + cos(ang*pi/10+pod_b[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_b[6]*pi/180) * 10000

    if shield>0.5:
        return ((0, 0, 0), (x_dir, y_dir, "SHIELD"))

    return ((0,0,0), (x_dir, y_dir, int(100*speed)))


#### ATTAQUE

def bot_attaque_8(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False): 
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

    l = [norm_ang(normalized(pod_a[6] - ang_cp)), norm_dist(norme(deltx, delty)), norm_vit(norme(vx, vy)), norm_ang(normalized(angle(vx, vy) - ang_cp)), norm_dist(dist1), norm_ang(ang_1), norm_dist(dist2), norm_ang(ang_2)]
    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")

    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed= ntw.get_output()

    x_dir, y_dir = x + cos(ang*pi/10+pod_a[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_a[6]*pi/180) * 10000

    return ((x_dir, y_dir, int(100*speed)), (0,0,0))

def bot_attaque_6(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False): 
    x, y, next_cp_x, next_cp_y = pod_a[2], pod_a[3], carte[pod_a[1]][0], carte[pod_a[1]][1]
    deltx, delty = next_cp_x-x, next_cp_y - y
    vx, vy = pod_a[4], pod_a[5]
    ang_cp = angle(deltx, delty)

    cp_suiv_1_x, cp_suiv_1_y = carte[(pod_a[1]+1)%len(carte)][0]-carte[pod_a[1]][0], carte[(pod_a[1]+1)%len(carte)][1]-carte[pod_a[1]][1]
    dist1 = norme(cp_suiv_1_x, cp_suiv_1_y)
    ang_1 = angle(cp_suiv_1_x, cp_suiv_1_y) - ang_cp



    l = [norm_ang(normalized(pod_a[6] - ang_cp)), norm_dist(norme(deltx, delty)), norm_vit(norme(vx, vy)), norm_ang(normalized(angle(vx, vy) - ang_cp)), norm_dist(dist1), norm_ang(ang_1)]
    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed= ntw.get_output()



    x_dir, y_dir = x + cos(ang*pi/10+pod_a[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_a[6]*pi/180) * 10000

    return ((x_dir, y_dir, int(100*speed)), (0,0,0))

def bot_attaque_4(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False): 
    x, y, next_cp_x, next_cp_y = pod_a[2], pod_a[3], carte[pod_a[1]][0], carte[pod_a[1]][1]
    deltx, delty = next_cp_x-x, next_cp_y - y
    vx, vy = pod_a[4], pod_a[5]
    ang_cp = angle(deltx, delty)

    l = [norm_ang(normalized(pod_a[6] - ang_cp)), norm_dist(norme(deltx, delty)), norm_vit(norme(vx, vy)), norm_ang(normalized(angle(vx, vy) - ang_cp))]
    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed= ntw.get_output()



    x_dir, y_dir = x + cos(ang*pi/10+pod_a[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_a[6]*pi/180) * 10000

    return ((x_dir, y_dir, int(100*speed)), (0,0,0))

def bot_attaque_2(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte, show = False): 
    x, y, next_cp_x, next_cp_y = pod_a[2], pod_a[3], carte[pod_a[1]][0], carte[pod_a[1]][1]
    deltx, delty = next_cp_x-x, next_cp_y - y
    vx, vy = pod_a[4], pod_a[5]
    ang_cp = angle(deltx, delty)

    l = [norm_ang(normalized(pod_a[6] - ang_cp)), norm_dist(norme(deltx, delty))]
    if len(l) != len(ntw.layer_zero):
        raise ValueError("Attention, pas le bon nombre d'input donnés dans la fonction bots !")
    ntw.set_input(l[0:len(ntw.layer_zero)])
    ang, speed= ntw.get_output()



    x_dir, y_dir = x + cos(ang*pi/10+pod_a[6]*pi/180) * 10000, y + sin(ang*pi/10+pod_a[6]*pi/180) * 10000

    return ((x_dir, y_dir, int(100*speed)), (0,0,0))

# Pour ne rien faire : 

def exit_bot(ntw:Reseau, pod_a, pod_b, boost_hero, pod_adversaire_a, pod_adversaire_b, boost_adversaire, carte):
    return ((0,0,0), (0,0,0))