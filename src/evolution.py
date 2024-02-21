from classe_reseau_neuronnes.population import *
from console_et_robots.bots import bot_defense_10, bot_defense_8, bot_defense_4, bot_defense_2, bot_attaque_6_bis, bot_attaque_8_bis, bot_attaque_12, bot_attaque_10, bot_attaque_8, bot_attaque_6, bot_attaque_4, bot_attaque_2, exit_bot
from console_et_robots.bots_ancien import reponse_ancien_bot
import entrainement.parametre as parametre
from console_et_robots.calcul_angle import norme
from math import sqrt

# Fonctions score attaque : il faudrait diviser le score par un score de référence. Comme ca il est pas ultra félicité sil réussit vite des courses rapides
def score_attaque_carre(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond):
    return (pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1])))**2 

def score_attaque_racine(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond):
    return sqrt(pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1]))) # on met un carré pour que les fails soient severment punis

def score_attaque_racine_debute_defense(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond):
    return -min(2, nb_rebond*0.1) +sqrt(pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1]))) # on met un carré pour que les fails soient severment punis

def score_attaque(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond):
    return pod_j1_a[0]*len(carte) + pod_j1_a[1] - min(1,(norme(pod_j1_a[2]-carte[pod_j1_a[1]][0], pod_j1_a[3]-carte[pod_j1_a[1]][1]))/norme(carte[(pod_j1_a[1]-1)%len(carte)][0]-carte[pod_j1_a[1]][0], carte[(pod_j1_a[1]-1)%len(carte)][1]-carte[pod_j1_a[1]][1]))

def score_defense(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond):
    return -1 * (pod_j2_a[0]*len(carte) + pod_j2_a[1] - min(1,(norme(pod_j2_a[2]-carte[pod_j2_a[1]][0], pod_j2_a[3]-carte[pod_j2_a[1]][1]))/norme(carte[(pod_j2_a[1]-1)%len(carte)][0]-carte[pod_j2_a[1]][0], carte[(pod_j2_a[1]-1)%len(carte)][1]-carte[pod_j2_a[1]][1])))

#### PHASE 0
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
        (150, 80, 10, 10, 1,  1/2,  1/4,  1,  3,  5),  # 2 inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1,  1/2,  1/4,  1,  6,  10), # 4 inputs - 0 noeuds intermediaire
        (200, 50, 10, 10, 1,  1/2,  1/4,  1,  6,  10) # 4 inputs - 1 noeuds intermediaire
        # Pour avoir un bot rapide et stylé
        #(300, 40, 10, 10, 1,  1/2,  1/4,  1,  10, 20), # 6 inputs - 1 noeuds intermediaire
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 15, 10), # 6 inputs - 2 noeuds intermédiaire
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 15, 10), # 6 inputs - 3 noeuds intermédiaires
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 15, 20), # 8 inputs - 3 noeuds intermédiaires
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 15, 20), # 8 inputs - 4 noeuds intermédiaires
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 20, 30),  # 8 inputs - 5 noeuds intermédiaires
        #(200, 35, 10, 10, 1,  1/2,  1/4,  1, 20, 40), # 8 inputs - 6 noeuds intermédiaires
        #(200, 35, 10, 10, 1/2,  1/3,  1/6,  1/2, 25, 30), # 8 inputs - 7 noeuds intermédiaires
        #(200, 35, 10, 10, 1/3,  1/3,  1/8,  1/4, 25, 30), # 8 inputs - 8 noeuds intermédiaires
        #(200, 35, 10, 10, 1/4,  1/4,  1/10,  1/6, 25, 40) # 8 inputs - 9 noeuds intermédiaires
    ]
    entrees_fonction_evolution = [
        (["angle cp", "distance cp"],        0, bot_attaque_2, exit_bot, score_attaque),
        (["norme vitesse", "angle vitesse"], 0, bot_attaque_4, exit_bot, score_attaque),
        ([],                                 1, bot_attaque_4, exit_bot, score_attaque),
        # Pour avoir un bot rapide et stylé
        #(["distance cp+1", "angle cp+1"],    0, bot_attaque_6, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_6, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_6, exit_bot, score_attaque_racine),
        #(["distance cp+2", "angle cp+2"],    0, bot_attaque_8, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_8, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_8, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_8, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_8, exit_bot, score_attaque_racine),
        #([],                                 1, bot_attaque_8, exit_bot, score_attaque_racine)
    ]

    if len(entrees_fonction_evolution) != len(liste_params):
        raise ValueError("probleme de taille entre la donnee des parametres et des inputs d'entrainements")
    liste_evolutions = list(zip(entrees_fonction_evolution, liste_params))

    fichier_base_evolution = "/PAS DE FICHIER/"
    #fichier_base_evolution = ""
    fichier_de_depos = "Phase_0"

    set_parametres_phase_0_statique()

    for indice, ((nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score), params) in enumerate(liste_evolutions):

        print("\nApprentissage suivant ({}/{})\n".format(indice+1, len(liste_evolutions)))

        set_parametres_phase_0(params)
        evolution(nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, fichier_de_depos, True, fichier_de_base=fichier_base_evolution)
        fichier_base_evolution = fichier_de_depos


#### PHASE 1 
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
    nombre_de_tick_max, nombre_de_tick_max_sans_cp, descendants_par_bruitage, descendants_par_mutation, taux_mutation, proba_mutation, taux_scramble, proba_scramble, nombre_de_carte_pour_score, rayon_tp, nombre_de_generations = tup

    parametre.nombre_de_tick_max = nombre_de_tick_max
    parametre.nombre_de_tick_max_sans_cp = nombre_de_tick_max_sans_cp

    parametre.descendants_par_bruitage = descendants_par_bruitage
    parametre.descendants_par_mutation = descendants_par_mutation
    parametre.taux_mutation = taux_mutation
    parametre.proba_mutation = proba_mutation
    parametre.taux_scramble = taux_scramble
    parametre.proba_scramble = proba_scramble

    parametre.nombre_de_carte_pour_score = nombre_de_carte_pour_score

    parametre.set_placement_entrainement_defense(rayon_tp)

    parametre.nombre_de_generations = nombre_de_generations

def evolution_globale_phase_1():
    liste_attaquants = []
    liste_defenseurs = []

    suite_apprentissage_defense = [
        ### apprentissage des techniques de bases de défense : 
        ([
        #(200, 80, 15, 15, 1/1,  1/4,  1/2,  1/2,  3,  200,  10),  # 2  inputs - 0 noeuds intermediaire
        #(200, 80, 15, 15, 1/1,  1/4,  1/2,  1/2,  3,  200,  10), # 2  inputs - 1 noeuds intermediaire
        #(200, 70, 10, 10, 1/2,  1/8,  1/3,  1/4,  10, 500,  10), # 4  inputs - 2 noeuds intermediaire
        #(200, 70, 10, 10, 1/2,  1/8,  1/4,  1/4,  10, 1000, 10), # 4  inputs - 3 noeuds intermediaire
        #(300, 70, 10, 10, 1/2,  1/12, 1/5,  1/8,  10, 1500, 20), # 8  inputs - 3 noeuds intermediaire
        #(200, 70, 10, 10, 1/2,  1/16, 1/7, 1/12,  15, 2000, 10), # 8  inputs - 4 noeuds intermédiaire
        #(200, 60, 10, 10, 1/3,  1/20, 1/9, 1/12,  15, 2500, 20),  # 8  inputs - 5 noeuds intermédiaires
    ], [
        #(["angle adversaire", "distance adversaire"],               0, bot_defense_2,  bot_attaque_4, score_defense, 1),
        #([],                                                        1, bot_defense_2,  bot_attaque_4, score_defense, 1), 
        #(["angle CP", "distance CP"],                               0, bot_defense_4,  bot_attaque_4, score_defense, 1), 
        #([],                                                        1, bot_defense_4,  bot_attaque_4, score_defense, 1), 
        #(["angle vitesse adversaire", "norme vitesse adversaire", 
        #  "angle vitesse hero",       "norme vitesse hero"       ], 0, bot_defense_8,  bot_attaque_4, score_defense, 1), 
        #([],                                                        1, bot_defense_8,  bot_attaque_4, score_defense, 1), 
        #([],                                                        1, bot_defense_8,  bot_attaque_4, score_defense, 1),
    ]), 

        ### réponse à un bot compététant en attaque
        ([
            #(200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 20), # 10 inputs - 5 noeuds intermédiaires
            #(200, 70, 10, 10, 1/2,  1/40, 1/7, 1/15,  15, 2500, 10),  # 10 inputs - 6 noeuds intermédiaires
            #(200, 60, 10, 10, 1/3,  1/50, 1/9, 1/20,  15, 2500, 10)   # 10 inputs - 7 noeuds intermédiaires
        ], [
            #(["angle CP+1", "distance CP+1"],  0, bot_defense_10,  bot_attaque_8_bis, score_defense, 2), 
            #([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2), 
            #([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2)
        ]), 

        ### succession d'entrainement anodin en réponse successive aux apprentissage de l'attaque

        ([
            (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
        ], [
            ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 8 noeuds intermédiaires
        ]), 

        ([
            (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
        ], [
            ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 9 noeuds intermédiaires
        ]), 

        ([
        (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
    ], [
        ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 10 noeuds intermédiaires
        ,]),

        ([
        (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
    ], [
        ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 10 noeuds intermédiaires
        ,]),

        ([
        (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
    ], [
        ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 10 noeuds intermédiaires
        ,]),

        ([
        (200, 70, 10, 10, 1/2,  1/30, 1/5,  1/12,  10, 2500, 50),
    ], [
        ([],                               1, bot_defense_10,  bot_attaque_8_bis, score_defense, 2) # 10 inputs - 10 noeuds intermédiaires
        ,])

    ]

    suite_apprentissage_attaque = [
    ## Apprentissage de l'attaque face a un défenseur
        ([
            #(200, 80, 15, 15, 1,  1/10,  1/4,  1/20,  5,  2500, 20),
            #(200, 80, 15, 15, 1,  1/10,  1/4,  1/20,  10, 2500, 25),  
            #(200, 80, 15, 15, 1,  1/10,  1/4,  1/20,  15, 2500, 30), 
            #(200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            #(["angle adversaire", "distance adversaire"],        0, bot_attaque_6_bis,  bot_defense_8, score_attaque_racine_debute_defense, 2),
            #(["vitesse adversaire", "angle vitesse adversaire"], 0, bot_attaque_8_bis,  bot_defense_8, score_attaque_racine_debute_defense, 2), 
            #([],                                                 1, bot_attaque_8_bis,  bot_defense_8, score_attaque_racine_debute_defense, 2), 
            #([],                                                 1, bot_attaque_8_bis,  bot_defense_8, score_attaque_racine_debute_defense, 2)
        ]), 

    ## apprentissage successif de réponse à un défenseur expérimenté
        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]), 

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]), 

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]), 

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]),

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]),

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]),

        ([
            (200, 70, 10, 10, 1,  1/10,  1/4,  1/20,  20, 2500, 40)
        ], [
            ([],                                           1, bot_attaque_8_bis,  bot_defense_10, score_attaque_racine_debute_defense, 2)
        ]) 
    ]

    if len(suite_apprentissage_attaque) != len(suite_apprentissage_defense):
        raise ValueError("Pas autant de phase d'apprentissage de défense que de phase d'apprentissage de l'attaque")
    
    #fichier_recuperation_defense = "/PAS DE FICHIER/"
    #fichier_recuperation_defense = "Phase_1-defense subphase-0"
    #fichier_recuperation_attaque = "Phase_0"
    fichier_recuperation_defense = "Phase_1-defense subphase-4"
    fichier_recuperation_attaque = "Phase_1-attaque subphase-4"
    nom_fichier_defense = "Phase_1-defense subphase-"
    nom_fichier_attaque = "Phase_1-attaque subphase-"

    pop_atq = Population('adv', True, bot_attaque_4, exit_bot, [Reseau()], score_attaque)
    pop_atq.reload(fichier_recuperation_attaque, [], 0, integre_meilleurs=False)
    liste_attaquants.append(pop_atq.get_meilleur())

    for indice in range(len(suite_apprentissage_defense)):
        print("Subphase "+str(indice)+"\n")
        print("#####  Training defense  #####\n\n")
        # On fait évoluer le réseau de défense 
        (liste_params, entree_fonction_evolution) = suite_apprentissage_defense[indice]
        fichier_depos_defense = nom_fichier_defense+str(indice+3)
        evolution_globale_phase_1_defense(liste_attaquants, liste_params, entree_fonction_evolution, fichier_recuperation_defense, fichier_depos_defense)
        fichier_recuperation_defense = fichier_depos_defense
        
        # on rajoute le nouveau défenseur à la liste des défenseurs
        pop_def = Population('adv', False, bot_defense_10, exit_bot, [Reseau()], score_defense)
        pop_def.reload(fichier_recuperation_defense, [], 0, integre_meilleurs=False)

        if False and indice<=1: # la population 0 corespond à un bot de défense de type 8 inputs, ceux d'aprés sont des 10 inputs
            liste_defenseurs = [pop_def.get_meilleur()]
        else:
            liste_defenseurs.append(pop_def.get_meilleur())


        # On fait évoluer le réseau d'attaque
        print("\n\nSubphase "+str(indice)+"\n") 
        print("#####  Training attaque  #####\n\n")
        (liste_params, entree_fonction_evolution) = suite_apprentissage_attaque[indice]
        fichier_depos_attaque = nom_fichier_attaque+str(indice+3)
        evolution_globale_phase_1_attaque(liste_defenseurs, liste_params, entree_fonction_evolution, fichier_recuperation_attaque, fichier_depos_attaque)
        fichier_recuperation_attaque = fichier_depos_attaque
        
        # on rajoute le nouveau défenseur à la liste des défenseurs
        pop_atq = Population('adv', True, bot_attaque_8_bis, exit_bot, [Reseau()], score_attaque)
        pop_atq.reload(fichier_recuperation_attaque, [], 0, integre_meilleurs=False)
        if False and indice==0: # la population initiale corespond à un bot d'attaque de type 8 inputs, ceux d'aprés sont des 12 inputs
            liste_attaquants = [pop_atq.get_meilleur()]
        else:
            liste_attaquants.append(pop_atq.get_meilleur())


# sous-fonctions d'évolution du modéle 
def evolution_globale_phase_1_defense(liste_adversaire:list, liste_params:list, entrees_fonction_evolution:list, fichier_base_evolution:str, fichier_de_depos:str):

    if len(entrees_fonction_evolution) != len(liste_params):
        raise ValueError("probleme de taille entre la donnee des parametres et des inputs d'entrainements")
    liste_evolutions = list(zip(entrees_fonction_evolution, liste_params))

    set_parametres_phase_1_statique()

    for indice, ((nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, nombre_de_cp_avant_tp), params) in enumerate(liste_evolutions):

        print("\nApprentissage suivant ({}/{})\n".format(indice+1, len(liste_evolutions)))
        set_parametres_phase_1(params)
        evolution(nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, fichier_de_depos, False, opponents = liste_adversaire, fichier_de_base=fichier_base_evolution, cp_avant_tp = nombre_de_cp_avant_tp, afficher_meilleur=False)
        fichier_base_evolution = fichier_de_depos

def evolution_globale_phase_1_attaque(liste_adversaire:list, liste_params:list, entrees_fonction_evolution:list, fichier_base_evolution:str, fichier_de_depos:str):

    if len(entrees_fonction_evolution) != len(liste_params):
        raise ValueError("probleme de taille entre la donnee des parametres et des inputs d'entrainements")
    liste_evolutions = list(zip(entrees_fonction_evolution, liste_params))

    set_parametres_phase_1_statique()

    for indice, ((nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, nombre_de_cp_avant_tp), params) in enumerate(liste_evolutions):

        print("\nApprentissage suivant ({}/{})\n".format(indice+1, len(liste_evolutions)))
        set_parametres_phase_1(params)
        evolution(nouveaux_inputs, nouveaux_noeuds, bot_j1, bot_j2, fonction_score, fichier_de_depos, True, opponents = liste_adversaire, fichier_de_base=fichier_base_evolution, cp_avant_tp = nombre_de_cp_avant_tp)
        fichier_base_evolution = fichier_de_depos


def evolution(inputs:list, nombre_de_noeuds_intermediaire:int, bot_j1, bot_j2, fonction_score, fichier_de_depos:str, type_attaque:bool, opponents = [Reseau()], fichier_de_base:str = "/PAS DE FICHIER/", cp_avant_tp = 2, afficher_meilleur =False):
    if fichier_de_base == "/PAS DE FICHIER/":
        populace = Population(fichier_de_depos, type_attaque, bot_j1, bot_j2, opponents, fonction_score, cp_avant_tp = cp_avant_tp)
        populace.initialisation_aleatoire(inputs, nombre_de_noeuds_intermediaire, parametre.nombre_individu_generation_0)
    else:
        populace = Population(fichier_de_depos, type_attaque, bot_j1, bot_j2, opponents, fonction_score, cp_avant_tp = cp_avant_tp)
        populace.reload(fichier_de_base, inputs, 0, integre_meilleurs=True) #initialisation aleatoire de aleat = 0.1

    for indice in range(parametre.nombre_de_generations):
        if fichier_de_base != "/PAS DE FICHIER/" or indice>0:
            populace.reproduction()
        print("generation " + str(indice) + ' sur ' + str(parametre.nombre_de_generations))
        populace.calculate_score()
        populace.selection(afficher_meilleur=True)

    
    populace.save()

    if afficher_meilleur:
        populace.afficher_meilleur(3)

def observer_vs_ancien_code(nom_fichier, type_bot_j1, fonction_score, nombe_de_carte = 3, timing_frame = 50):
    parametre.timing_frame = timing_frame
    populace = Population('poubelle', True, type_bot_j1, reponse_ancien_bot, [Reseau()], fonction_score, cp_avant_tp = 2)
    populace.reload(nom_fichier, [], 0, integre_meilleurs=False)
    populace.afficher_meilleur(nombe_de_carte)

def comparer_attaque(nom_fichier_j1, type_bot_j1, nom_fichier_j2, type_bot_j2, fonction_score, nombe_de_carte = 3, timing_frame = 50, cp_avant_tp = 2):
    parametre.timing_frame = timing_frame

    pops2 = Population('j2', True, type_bot_j2, type_bot_j1, [Reseau()], fonction_score)
    pops2.reload(nom_fichier_j2, [], 0, integre_meilleurs=False)
    meilleur_j2 = pops2.get_meilleur()

    populace = Population('j1', False, type_bot_j1, type_bot_j2, [meilleur_j2], fonction_score, cp_avant_tp = cp_avant_tp)
    populace.reload(nom_fichier_j1, [], 0, integre_meilleurs=False)

    populace.afficher_meilleur(nombe_de_carte)


#evolution_globale_phase_0()
evolution_globale_phase_1()

## Pour observer une map
#set_parametres_phase_0_statique()
set_parametres_phase_1_statique()
parametre.taille_cp = 600
parametre.set_placement_entrainement_defense(1000)
comparer_attaque("phase_1_save/second try/Phase_1-defense subphase-5", bot_defense_10, "phase_1_save/second try/Phase_1-attaque subphase-5", bot_attaque_8_bis,  score_attaque_racine, nombe_de_carte = 10, cp_avant_tp=2)
#observer_vs_ancien_code("phase_0_save/phase_0 save_6", bot_attaque_8, score_attaque_racine, nombe_de_carte = 10)

## Pour lancer l'entrainement

#evolution_globale_phase_0()

#pop_adv = Population('adv', True, bot_attaque_8, exit_bot, [Reseau()], score_attaque)
#pop_adv.reload("phase_0_save/phase_0 save_6", [], 0, integre_meilleurs=False)
#meilleur_adv = pop_adv.get_meilleur()
#evolution_globale_phase_1_defense([meilleur_adv])

#pop_adv = Population('adv', False, bot_attaque_8, exit_bot, [Reseau()], score_attaque)
#pop_adv.reload("phase_1_save/Phase_1_defense save_2", [], 0, integre_meilleurs=False)
#meilleur_adv = pop_adv.get_meilleur()
#evolution_globale_phase_1_attaque([meilleur_adv])

## Bug sur la 38
