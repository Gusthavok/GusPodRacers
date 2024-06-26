from numpy.random import randint
from math import pi, sin, cos

## visualisation graphique
reduction_factor = 20
timing_frame = 50


## Pods 
def inputs_attaque_utilise(l:list):
    return l[:4] + l[8:12]

def inputs_defense_utilise(l:list):
    return l[:10]

shield_active_attaquant = False
boost_active_attaquant = False

shield_active_defenseur = True
boost_active_defenseur = True


## Paramtre console de jeu
# Collisions
collision_tab = [
    [True, True, True, True], 
    [True, True, True, True], 
    [True, True, True, True], 
    [True, True, True, True]
]

def collision_activee(i,j):
    return collision_tab[i][j]
nombre_de_dt = 20 # plus ce nombre est grand, plus la modélisation des collisions est précise mais plus l'algorithme est lent

# CPs
taille_cp = 600 # dans le vrai jeu c'est 600, idée : pour l'apprentissage attaque on met 570, et pour l'apprentissage de defense on met 630

# Autres :
nombre_de_tick_max = 1000
nombre_de_tick_max_sans_cp = 100 # 100 normalement
defaite_j2_possible = True
defaite_j1_possible = True

## evolution
nombre_de_generations = 5
placement_entrainement_defense_tp_x = [0 for _ in range(8)] # au plus 8 cp par carte
placement_entrainement_defense_tp_y = [0 for _ in range(8)]
orientation_defense_tp = [0 for _ in range(8)]
cp_tp = 0
def set_placement_entrainement_defense(rayon):
    global placement_entrainement_defense_tp_x, placement_entrainement_defense_tp_y, orientation_defense_tp
    for i in range(8):
        r = randint(rayon//2, rayon)
        ang = randint(-180, 180)
        placement_entrainement_defense_tp_x[i] = r * cos(ang/180*pi)
        placement_entrainement_defense_tp_y[i] = r * sin(ang/180*pi)
        orientation_defense_tp[i] = randint(-179, 181)

## Parametres Population
# Reproduction : 
descendants_par_bruitage = 10
descendants_par_mutation = 10
taux_mutation, proba_mutation = 1, 1/4
taux_scramble, proba_scramble = 1/2, 1/2

# Selection
nombre_anciens_reintroduits = 3
nombre_individus_selectionne = 7
nombre_individu_generation_0 = (descendants_par_mutation+descendants_par_bruitage) * nombre_individus_selectionne

# Calcul du score
nombre_de_carte_pour_score = 3
nombre_de_tour = 10
lcarte = [
    ## Type de carte à 3 CP : permutations cyclique du même type de carte
    [[11329, 2841], [7470, 6933], [5999, 5361]], 
    [[11322, 2808], [7516, 6954], [5980, 5376]],
    [[11329, 2830], [7493, 6943], [6003, 5388]], 
    [[11466, 6086], [9122, 1817], [5001, 5286]],
    [[11476, 6092], [9129, 1823], [4980, 5286]],

    [[5981, 5355], [11287, 2833], [7507, 6962]],
    [[5990, 5337], [11300, 2801], [7485, 6937]],
    [[6030, 5334], [11299, 2813], [7472, 6940]],

    [[7525, 6917], [6019, 5378], [11311, 2816]],
    [[7477, 6947], [6028, 5379], [11292, 2813]],

    ## 4 CP : 6 types observés (à des permutations cycliques près)
    # type 1
    [[13937, 1920], [8043, 3233], [2659, 7041], [10041, 5990]],
    [[8035, 3288], [2693, 7039], [10013, 5965], [13899, 1965]], # permutation cyclique

    # type 2
    [[13330, 5525], [9572, 1417], [3660, 4447], [8011, 7901]],
    [[13302, 5555], [9574, 1373], [3618, 4403], [7979, 7910]], 
    [[7975, 7887], [13321, 5554], [9567, 1375], [3660, 4408]], # permutation cyclique
    [[3661, 4400], [7984, 7919], [13282, 5514], [9557, 1391]], # permutation cyclique
    [[9541, 1413], [3626, 4440], [7993, 7902], [13283, 5550]], # permutation cyclique

    # type 3
    [[12968, 7201], [5627, 2554], [4124, 7430], [13502, 2335]],
    [[12960, 7225], [5640, 2600], [4075, 7436], [13480, 2350]],

    # type 4
    [[12438, 1339], [10539, 5969], [3590, 5168], [13570, 7616]],
    [[3559, 5152], [13560, 7590], [12439, 1325], [10556, 6004]], # permutation cyclique

    # type 5
    [[10300, 3366], [11174, 5436], [7256, 6657], [5417, 2848]], 
    [[10311, 3373], [11194, 5405], [7260, 6633], [5441, 2824]], 
    [[7257, 6682], [5398, 2845], [10332, 3385], [11222, 5402]], # permutation cyclique
    [[5437, 2811], [10351, 3376], [11174, 5444], [7249, 6678]], # permutation cyclique

    # type 6
    [[5962, 4227], [14653, 1408], [3445, 7234], [9400, 7223]], # unique


    ## 5 CP : 2 types détectés
    # type 1
    [[13054, 1878], [6577, 7846], [7462, 1380], [12699, 7098], [4062, 4646]],
    [[13049, 1905], [6537, 7828], [7491, 1365], [12670, 7105], [4073, 4654]],
    [[12726, 7074], [4046, 4684], [13045, 1908], [6540, 7849], [7461, 1377]], # permutation cyclique
    [[12704, 7079], [4070, 4650], [13067, 1893], [6534, 7835], [7466, 1344]], # permutation cyclique
    [[12670, 7072], [4090, 4655], [13065, 1926], [6532, 7815], [7500, 1331]], # permutation cyclique
    [[6589, 7811], [7461, 1330], [12676, 7083], [4048, 4661], [13033, 1917]], # permutation cyclique
    [[4087, 4666], [13017, 1896], [6542, 7860], [7454, 1346], [12708, 7100]], # permutation cyclique
    [[4050, 4652], [13025, 1884], [6589, 7868], [7472, 1357], [12720, 7125]], # permutation cyclique

    # type 2
    [[10707, 2258], [8713, 7453], [7186, 2186], [3580, 5265], [13813, 5060]],
    [[10672, 2253], [8713, 7441], [7195, 2186], [3623, 5268], [13857, 5105]], 


    ## 6 CP : 3 types détectés 
    # type 1
    [[10578, 5069], [13073, 2316], [4568, 2154], [7360, 4922], [3348, 7249], [14560, 7706]], 
    [[10568, 5058], [13092, 2333], [4553, 2169], [7370, 4916], [3325, 7220], [14577, 7715]],
    [[10538, 5086], [13116, 2290], [4549, 2187], [7359, 4922], [3327, 7208], [14598, 7677]], 
    [[3301, 7255], [14569, 7676], [10558, 5072], [13083, 2330], [4566, 2203], [7335, 4931]], # permutation cyclique

    # type 2
    [[10224, 4902], [6084, 2177], [2997, 5207], [6265, 7738], [14129, 7766], [13887, 1198]], 

    # type 3
    [[7650, 5971], [3147, 7543], [9549, 4355], [14509, 7789], [6347, 4292], [7797, 867]],
    [[6329, 4280], [7824, 880], [7656, 5948], [3137, 7550], [9505, 4373], [14502, 7750]] # permutation cyclique
]

echantillon_carte = [
    # 3 CP : 
    [[11329, 2841], [7470, 6933], [5999, 5361]], 


    # 4 CP : 
    [[13937, 1920], [8043, 3233], [2659, 7041], [10041, 5990]],
    [[13330, 5525], [9572, 1417], [3660, 4447], [8011, 7901]],
    [[12968, 7201], [5627, 2554], [4124, 7430], [13502, 2335]],
    [[12438, 1339], [10539, 5969], [3590, 5168], [13570, 7616]],
    [[10300, 3366], [11174, 5436], [7256, 6657], [5417, 2848]], 
    [[5962, 4227], [14653, 1408], [3445, 7234], [9400, 7223]], # unique

    # 5 CP :
    [[13054, 1878], [6577, 7846], [7462, 1380], [12699, 7098], [4062, 4646]],
    [[10707, 2258], [8713, 7453], [7186, 2186], [3580, 5265], [13813, 5060]],

    # 6 CP : 
    [[10578, 5069], [13073, 2316], [4568, 2154], [7360, 4922], [3348, 7249], [14560, 7706]], 
    [[10224, 4902], [6084, 2177], [2997, 5207], [6265, 7738], [14129, 7766], [13887, 1198]], 
    [[7650, 5971], [3147, 7543], [9549, 4355], [14509, 7789], [6347, 4292], [7797, 867]],
 
]