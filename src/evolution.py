from classe_reseau_neuronnes.population import *
from console_et_robots.bots import bot_defense_10, bot_defense_8, bot_defense_4, bot_defense_2, bot_attaque_8, bot_attaque_6, bot_attaque_4, bot_attaque_2, exit_bot
from console_et_robots.bots_ancien import reponse_ancien_bot
import entrainement.parametre as parametre
from console_et_robots.calcul_angle import norme

# Fonctions score attaque : il faudrait diviser le score par un score de référence. Comme ca il est pas ultra félicité sil réussit vite des courses rapides
def score_attaque_carre(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b):
    return (pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1])))**2 # on met un carré pour que les fails soient severment punis

def score_attaque(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b):
    return pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1]))

def score_defense(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b):
    return -1 * (pod_j2_a[0]*len(carte) + pod_j2_a[1] - min(1,(norme(pod_j2_a[2]-carte[pod_j2_a[1]][0], pod_j2_a[3]-carte[pod_j2_a[1]][1]))/norme(carte[(pod_j2_a[1]-1)%len(carte)][0]-carte[pod_j2_a[1]][0], carte[(pod_j2_a[1]-1)%len(carte)][1]-carte[pod_j2_a[1]][1])))

# Parametres a modifier pour l'evolution
def set_parametres_phase_0_statique():
    parametre.nombre_de_dt = 1
    parametre.collision_tab = [
        [False, False, False, False], 
        [False, False, False, False], 
        [False, False, False, False], 
        [False, False, False, False]
    ]
    parametre.taille_cp = 570 # pour tous les algos on va prendre 570
    parametre.defaite_j2_possible = False
    parametre.nombre_de_tour = 10
    parametre.nombre_anciens_reintroduits = 3
    parametre.nombre_individus_selectionne = 7
    parametre.nombre_individu_generation_0 = (parametre.descendants_par_mutation+parametre.descendants_par_bruitage) * (parametre.nombre_individus_selectionne+1)

def set_parametres_phase_0(tup):
    nombre_de_tick_max, nombre_de_tick_max_sans_cp, descendants_par_bruitage, descendants_par_mutation, taux_mutation, proba_mutation, taux_scramble, proba_scramble, nombre_de_carte_pour_score, nombre_de_generations = tup

    parametre.nombre_de_tick_max = nombre_de_tick_max
    parametre.nombre_de_tick_max_sans_cp = nombre_de_tick_max_sans_cp

    parametre.descendants_par_bruitage = descendants_par_bruitage
    parametre.descendants_par_mutation = descendants_par_mutation
    parametre.taux_mutation = taux_mutation
    parametre.proba_mutation = proba_mutation
    parametre.taux_scramble = taux_scramble
    parametre.proba_scramble = proba_scramble

    parametre.nombre_de_carte_pour_score = nombre_de_carte_pour_score

    parametre.nombre_de_generations = nombre_de_generations

def evolution_globale_phase_0():
    liste_params = [
        (150, 80, 10, 10, 1/1,  1/4,  1/2,  1/2,  3,  5),  # 2 inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1/2,  1/8,  1/3,  1/4,  6,  10), # 4 inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1/2,  1/8,  1/4,  1/4,  6,  10), # 4 inputs - 1 noeuds intermediaire
        (300, 40, 10, 10, 1/2,  1/12, 1/5,  1/8,  10, 20), # 6 inputs - 1 noeuds intermediaire
        (200, 35, 10, 10, 1/2,  1/16, 1/7, 1/12, 15, 10), # 6 inputs - 2 noeuds intermédiaire
        (200, 35, 10, 10, 1/3,  1/20, 1/9, 1/12, 15, 10), # 6 inputs - 3 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 15, 20), # 8 inputs - 3 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 15, 10), # 8 inputs - 4 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 20, 20),  # 8 inputs - 4 noeuds intermédiaires
        (200, 35, 10, 10, 1/6, 1/32, 1/10, 1/20, 20, 30), # 8 inputs - 5 noeuds intermédiaires
        (200, 35, 10, 10, 1/6, 1/42, 1/10, 1/30, 20, 30), # 8 inputs - 6 noeuds intermédiaires
        (200, 35, 10, 10, 1/6, 1/60, 1/10, 1/40, 20, 40),  # 8 inputs - 7 noeuds intermédiaires
        (200, 35, 10, 10, 1/6, 1/32, 1/10, 1/20, 20, 50), # 8 inputs - 8 noeuds intermédiaires
        (200, 35, 10, 10, 1/8, 1/42, 1/12, 1/30, 20, 50), # 8 inputs - 9 noeuds intermédiaires
        (200, 35, 10, 10, 1/8, 1/60, 1/12, 1/40, 20, 50)  # 8 inputs - 10 noeuds intermédiaires
    ]
    entrees_fonction_evolution = [
        (["angle cp", "distance cp"],        0, bot_attaque_2, exit_bot, score_attaque),
        (["norme vitesse", "angle vitesse"], 0, bot_attaque_4, exit_bot, score_attaque),
        ([],                                 1, bot_attaque_4, exit_bot, score_attaque),
        (["distance cp+1", "angle cp+1"],    0, bot_attaque_6, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_6, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_6, exit_bot, score_attaque_carre),
        (["distance cp+2", "angle cp+2"],    0, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 0, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre),
        ([],                                 1, bot_attaque_8, exit_bot, score_attaque_carre)
    ]

    if len(entrees_fonction_evolution) != len(liste_params):
        raise ValueError("probleme de taille entre la donnee des parametres et des inputs d'entrainements")
    liste_evolutions = list(zip(entrees_fonction_evolution, liste_params))

    fichier_base_evolution = "/PAS DE FICHIER/"
    #fichier_base_evolution = "Phase_0 save_3"
    fichier_de_depos = "Phase_0"

    set_parametres_phase_0_statique()

    for indice, ((nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score), params) in enumerate(liste_evolutions):

        print("\nApprentissage suivant ({}/{})\n".format(indice+1, len(liste_evolutions)))

        set_parametres_phase_0(params)
        evolution(nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, fichier_de_depos, True, fichier_de_base=fichier_base_evolution)
        fichier_base_evolution = fichier_de_depos


def set_parametres_phase_1_statique():
    parametre.nombre_de_dt = 20
    parametre.collision_tab = [
        [False, False, False, False], 
        [False, False, True , False], 
        [False, True , False, False], 
        [False, False, False, False]
    ]
    parametre.taille_cp = 630
    parametre.defaite_j1_possible = False
    parametre.nombre_de_tour = 10
    parametre.nombre_anciens_reintroduits = 3
    parametre.nombre_individus_selectionne = 7
    parametre.nombre_individu_generation_0 = (parametre.descendants_par_mutation+parametre.descendants_par_bruitage) * (parametre.nombre_individus_selectionne+1)
    parametre.nombre_de_tick_max_sans_cp = 150 # on ne veut pas qu'un pod qui par chance réussisse a bloquer pendant 100 ticks l'attquant marque tant de points.

def set_parametres_phase_1(tup):
    nombre_de_tick_max, nombre_de_tick_max_sans_cp, descendants_par_bruitage, descendants_par_mutation, taux_mutation, proba_mutation, taux_scramble, proba_scramble, nombre_de_carte_pour_score, nombre_de_generations = tup

    parametre.nombre_de_tick_max = nombre_de_tick_max
    parametre.nombre_de_tick_max_sans_cp = nombre_de_tick_max_sans_cp

    parametre.descendants_par_bruitage = descendants_par_bruitage
    parametre.descendants_par_mutation = descendants_par_mutation
    parametre.taux_mutation = taux_mutation
    parametre.proba_mutation = proba_mutation
    parametre.taux_scramble = taux_scramble
    parametre.proba_scramble = proba_scramble

    parametre.nombre_de_carte_pour_score = nombre_de_carte_pour_score

    parametre.nombre_de_generations = nombre_de_generations


def evolution_globale_phase_1_defense(liste_adversaire:list):
    liste_params = [
        (200, 80, 15, 15, 1/1,  1/4,  1/2,  1/2,  3,  20),  # 2  inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1/2,  1/8,  1/3,  1/4,  6,  10), # 4  inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1/2,  1/8,  1/4,  1/4,  6,  10), # 4  inputs - 1 noeuds intermediaire
        (300, 40, 10, 10, 1/2,  1/12, 1/5,  1/8,  10, 20), # 8  inputs - 1 noeuds intermediaire
        (200, 35, 10, 10, 1/2,  1/16, 1/7, 1/12, 15, 10),  # 8  inputs - 2 noeuds intermédiaire
        (200, 35, 10, 10, 1/3,  1/20, 1/9, 1/12, 15, 10),  # 8  inputs - 3 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 15, 20), # 10 inputs - 3 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 15, 10), # 10 inputs - 4 noeuds intermédiaires
        (200, 35, 10, 10, 1/4,  1/25, 1/10, 1/20, 20, 20), # 10 inputs - 5 noeuds intermédiaires
        (200, 35, 10, 10, 1/6, 1/32, 1/10, 1/20, 20, 30),  # 10 inputs - 6 noeuds intermédiaires
    ]
    entrees_fonction_evolution = [
        (["angle adversaire", "distance adversaire"],               0, bot_defense_2,  bot_attaque_8, score_defense, 1), 
        (["angle CP", "distance CP"],                               0, bot_defense_4,  bot_attaque_8, score_defense, 1), 
        ([],                                                        1, bot_defense_4,  bot_attaque_8, score_defense, 1), 
        (["angle vitesse adversaire", "norme vitesse adversaire", 
          "angle vitesse hero",       "norme vitesse hero"       ], 0, bot_defense_8,  bot_attaque_8, score_defense, 1), 
        ([],                                                        1, bot_defense_8,  bot_attaque_8, score_defense, 1), 
        ([],                                                        1, bot_defense_8,  bot_attaque_8, score_defense, 1), 
        (["angle CP+1, distance CP+1"],                             0, bot_defense_10, bot_attaque_8, score_defense, 2), 
        ([],                                                        1, bot_defense_10, bot_attaque_8, score_defense, 2),
        ([],                                                        1, bot_defense_10, bot_attaque_8, score_defense, 2),
        ([],                                                        1, bot_defense_10, bot_attaque_8, score_defense, 2)
            ]


    if len(entrees_fonction_evolution) != len(liste_params):
        raise ValueError("probleme de taille entre la donnee des parametres et des inputs d'entrainements")
    liste_evolutions = list(zip(entrees_fonction_evolution, liste_params))

    fichier_base_evolution = "/PAS DE FICHIER/"
    #fichier_base_evolution = "Phase_1 save_3"
    fichier_de_depos = "Phase_1_defense"

    set_parametres_phase_1_statique()

    for indice, ((nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, nombre_de_cp_avant_tp), params) in enumerate(liste_evolutions):

        print("\nApprentissage suivant ({}/{})\n".format(indice+1, len(liste_evolutions)))
        set_parametres_phase_1(params)
        evolution(nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, fichier_de_depos, False, opponents = liste_adversaire, fichier_de_base=fichier_base_evolution, cp_avant_tp = nombre_de_cp_avant_tp, afficher_meilleur=True)
        fichier_base_evolution = fichier_de_depos


def evolution(inputs:list, nombre_de_noeuds_intermediaire:int, bot_j1, bot_j2, fonction_score, fichier_de_depos:str, type_attaque:bool, opponents = [Reseau()], fichier_de_base:str = "/PAS DE FICHIER/", cp_avant_tp = 2, afficher_meilleur =False):
    if fichier_de_base == "/PAS DE FICHIER/":
        populace = Population(fichier_de_depos, type_attaque, bot_j1, bot_j2, opponents, fonction_score, cp_avant_tp = cp_avant_tp)
        populace.initialisation_aleatoire(inputs, nombre_de_noeuds_intermediaire, parametre.nombre_individu_generation_0)
    else:
        populace = Population(fichier_de_depos, type_attaque, bot_j1, bot_j2, opponents, fonction_score, cp_avant_tp = cp_avant_tp)
        populace.reload(fichier_de_base, inputs, 0, integre_meilleurs=True) #initialisation aleatoire de aleat = 0.1
        populace.reproduction()

    for indice in range(parametre.nombre_de_generations):
        print("generation " + str(indice) + ' sur ' + str(parametre.nombre_de_generations))
        populace.calculate_score()
        populace.selection(afficher_meilleur=True)
        if indice<parametre.nombre_de_generations-1:
            populace.reproduction()

    populace.save()

    if afficher_meilleur:
        populace.afficher_meilleur(3)

def observer_vs_ancien_code(nom_fichier, type_bot_j1, fonction_score, nombe_de_carte = 3, timing_frame = 50):
    parametre.timing_frame = timing_frame
    populace = Population('poubelle', True, type_bot_j1, reponse_ancien_bot, [Reseau()], fonction_score, cp_avant_tp = 2)
    populace.reload(nom_fichier, [], 0, integre_meilleurs=False)
    populace.afficher_meilleur(nombe_de_carte)

def comparer_attaque(nom_fichier_j1, type_bot_j1, nom_fichier_j2, type_bot_j2, fonction_score, nombe_de_carte = 3, timing_frame = 50):
    parametre.timing_frame = timing_frame

    pops2 = Population('j2', True, type_bot_j2, type_bot_j1, [Reseau()], fonction_score)
    pops2.reload(nom_fichier_j2, [], 0, integre_meilleurs=False)
    meilleur_j2 = pops2.get_meilleur()

    populace = Population('j1', True, type_bot_j1, type_bot_j2, [meilleur_j2], fonction_score, cp_avant_tp = 2)
    populace.reload(nom_fichier_j1, [], 0, integre_meilleurs=False)

    populace.afficher_meilleur(nombe_de_carte)


## Pour observer une map
#set_parametres_phase_0_statique()
#parametre.taille_cp = 600
#comparer_attaque("phase_0_save/phase_0 save_6", bot_attaque_8, "phase_0_save/phase_0 save_1", bot_attaque_8, score_attaque_carre, nombe_de_carte = 10)
#observer_vs_ancien_code("phase_0_save/phase_0 save_6", bot_attaque_8, score_attaque_carre, nombe_de_carte = 10)

## Pour lancer l'entrainement

#evolution_globale_phase_0()

pop_adv = Population('adv', True, bot_attaque_8, exit_bot, [Reseau()], score_attaque)
pop_adv.reload("phase_0_save/phase_0 save_6", [], 0, integre_meilleurs=False)
meilleur_adv = pop_adv.get_meilleur()
evolution_globale_phase_1_defense([meilleur_adv])

## Bug sur la 38