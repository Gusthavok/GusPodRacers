from math import *

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def calcul_tour_1(dist, angl, v_angl, vitesse):
    """
    cette fonction calcule la vitesse et l'angle optimal à viser en considérant que le chekpoint est en (0,0)
    et que le pod est en (-dist, 0),
    orienté par son angle "angl" avec le checkpoint, 
    et posséedant déja une vitesse carcactérisée par "v_angl" et sa norme "vitesse"
    """

    """
    méthode sans réseau neuronal : 
    On détermine l'angle optimal qui pertmettrait d'atteindre le cp le plus rapidement possible, et on s'oriente vers lui. 
    On regarde en fonction de notre orientation a quel point on doit accélérer
    """
    """
    On calcule d'abord une valeur etimée du nombre de tic 
    """
    if dist >3000:
        ntic = 20
    elif dist >1500:
        ntic = 12
    elif dist >800:
        ntic = 6
    elif dist > 400:
        ntic = 3
    else:
        ntic =2
    
    """
    l'angle optimal va dépendre de dist, v_angl, vitesse
    """
    
    if abs (vitesse/(ntic*100) * sin(v_angl)) <= 1:
        angle_optimal = asin(-vitesse/(ntic*100) * sin(v_angl))
    elif vitesse/(ntic*100) * sin(v_angl) > 1 : 
        angle_optimal = pi/2
    else: 
        angle_optimal = -pi/2


    """
    la l'accéleration doit dépendre de angl, vangl, vitesse et dist
    on veut accélerer ssi un mouvement nous permettrait de contrebalancer un mauvais angles de vitese du pod, ou d'accélerer vers le cp. 
    un cos de proximité avec l'angle optimal semble interessant
    """
    erreur = abs((angle_optimal-angl)/pi)
    if erreur > 1:
        accel = 0
    elif erreur >0.5:
        accel = 25
    elif erreur > 0.25:
        accel = 75
    else: 
        accel = 100


    return (angle_optimal,accel)

def agl(x1,y1):
    """calcul l'angle entre l'axe Ox et le vecteur (x1,y1)
    """
    if x1==0:
        if y1>=0 : 
            return pi/2
        else:
            return -pi/2
    elif x1 >0:
        return atan(y1/x1)
    else:
        return pi + atan(y1/x1)


def calc_angle(x1, y1, x2, y2):
    """ renvoie l'angle orienté entre le vecteur (x1,y1) et (x2,y2)
    """
    
    return agl(x2,y2) - agl(x1,y1)

def trouve(el, liste):
    """
    trouve l'indice de l'élément "el" dans la liste "liste"
    Si cet élément n'existe pas, elle affichera un message en sortie d'erreur avant de planter le programme
    """
    for ind,val in enumerate(liste):
        if val == el:
            return ind
    

def next_next(x_cp, y_cp, l_cp):
    """
    renvoie les coordonnées du chekpoint 2 fois après
    """
    indice = trouve((x_cp, y_cp), l_cp)
    if indice < len(l_cp)-1:
        return l_cp[indice+1]
    else:
        return l_cp[0]


def point_a_viser(x1,y1, x2,y2, x3,y3):
    """
    permet de construire un point intermédiraire si la distance (x1,y1) et (x2,y2) est suffisante
    le point crée alors permet de mieux relier les points (x2, y2) et (x3, y3)
    """

    return (x2,y2)

# game loop
# premier_tour = True
# x,y = 0,0
# depart = True
# liste_checkpoint = []
"""
decompte = 20
"""
def decision(premier_tour, x, y, old_x, old_y, depart, liste_checkpoint, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle):
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    
    if depart:
        if next_checkpoint_dist > 5000:
            return next_checkpoint_x, next_checkpoint_y, "BOOST", premier_tour, depart, liste_checkpoint, old_x, old_y
        else:
            return next_checkpoint_x, next_checkpoint_y, 100, premier_tour, depart, liste_checkpoint, old_x, old_y

        liste_checkpoint.append((next_checkpoint_x, next_checkpoint_y))
        depart = False
    else:
        """
        decompte -=1
        """

        if premier_tour:
            angle_vitesse = calc_angle( x-old_x, y-old_y,next_checkpoint_x -x, next_checkpoint_y -y)
            vitesse = sqrt((x-old_x)**2 + (y-old_y)**2)


            angl, v_calc = calcul_tour_1(next_checkpoint_dist,pi/180*next_checkpoint_angle, angle_vitesse, vitesse)

            x_dir = int(10000 * cos(agl(next_checkpoint_x -x, next_checkpoint_y -y) - angl)+x)
            y_dir = int(10000 * sin(agl(next_checkpoint_x -x, next_checkpoint_y -y) - angl)+y)

            if (next_checkpoint_x, next_checkpoint_y) == liste_checkpoint[0] and len(liste_checkpoint) >= 2:
                premier_tour = False
            elif (next_checkpoint_x, next_checkpoint_y) != liste_checkpoint[-1]:
                liste_checkpoint.append((next_checkpoint_x, next_checkpoint_y))
            

            return x_dir, y_dir, int(v_calc), premier_tour, depart, liste_checkpoint, old_x, old_y

            
        
            
               #pass
                
            
        
        else:
            # Dans le second tour, comme on connait l'enchainement des différent cps, on rajoute un point intermédiaire à viser 
            # permettant de faciliter l'enchainement des cps
            next_next_checkpoint_x, next_next_checkpoint_y = next_next(next_checkpoint_x,next_checkpoint_y, liste_checkpoint)

            angle_vitesse = calc_angle( x-old_x, y-old_y,next_checkpoint_x -x, next_checkpoint_y -y)
            vitesse = sqrt((x-old_x)**2 + (y-old_y)**2)

            point_a_viser_x, point_a_viser_y = point_a_viser(x, y, next_checkpoint_x,next_checkpoint_y,next_next_checkpoint_x, next_next_checkpoint_y)

            distance_point = sqrt((point_a_viser_x-x)**2 + (point_a_viser_y-y)**2)
            angle_au_point = next_checkpoint_angle - calc_angle(next_checkpoint_x-x, next_checkpoint_y-y, point_a_viser_x-x, point_a_viser_y-y)
            angl, v_calc = calcul_tour_1(distance_point,angle_au_point, angle_vitesse, vitesse)

            x_dir = int(10000 * cos(agl(point_a_viser_x -x, point_a_viser_y -y) - angl)+x)
            y_dir = int(10000 * sin(agl(point_a_viser_x -x, point_a_viser_y -y) - angl)+y)

            return x_dir, y_dir, int(v_calc), premier_tour, depart, liste_checkpoint, old_x, old_y
            
        """
        if decompte <=0:
            print(str(x)+" 0 100")
        else:
            print(str(x)+" 8000 100")
            """