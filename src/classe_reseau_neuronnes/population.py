from classe_reseau_neuronnes.network import *
import entrainement.parametre as parametre
from numpy.random import randint
from numpy import argmax
from math import pi
from console_et_robots.console import jeu
from grahismes.visualisation_graphique import affgame
import operator

# RMQ : C'est moche d'importer ici reduction factor, il vaudrait surement mieux de gérer tout l'affichage du cote de visualisation_graphique.py
class Population:
    def __init__(self, name:str, type_attaque:int, type_bot_hero, type_bot_vilain, opponents_networks:list[Reseau], fonction_score, individus:list[Reseau] = [], meilleurs_anciennes_generations:list[Reseau] = [], score:list = [], anciens_score:list = [], cp_avant_tp = 100) -> None:
        # ATTENTION, ON FAIT UNE COPIE DE LA LISTE individus, SI CETTE DERNIERE EST NON VIDE, LES POINTEURS QU'ELLE CONTIENT SONT EGAUX
        # meme chose pour la liste des reseaux de l'opponent
        
        self.name = name
        self.type_attaque = type_attaque
        self.individus = individus.copy()
        self.meilleurs_anciennes_generations = meilleurs_anciennes_generations.copy() # liste de couple composée du meilleur de chaque génération et de son score depuis la génération 0
        self.type_bot_hero = type_bot_hero
        self.type_bot_vilain = type_bot_vilain
        self.opponents = opponents_networks.copy()
        self.fonction_score = fonction_score
        self.cp_avant_tp = cp_avant_tp

        if len(score) == 0: 
            score = [0 for _ in individus]
        if len(anciens_score) == 0:
            anciens_score = [0 for _ in individus]
        
        self.score = score.copy()
        self.anciens_score = anciens_score.copy()

    def nouvel_individu(self, r:Reseau, score:float, ancien_score:float):
        self.individus.append(r)
        self.score.append(score)
        self.anciens_score.append(ancien_score)

    def reinit_individus(self):
        self.individus = []
        self.score = []
        self.anciens_score = []

    def initialisation_aleatoire(self, inputs:list[str], nombre_de_noeuds_intermediaire:int, taille_population:int):
        if len(self.individus) > 0:
            print("Attention, methode initialisation_aléatoire utilisée sur une population non vide")
        for _ in range(taille_population):
            r = Reseau(atq = self.type_attaque)
            r.initialisation_aleatoire(inputs, nombre_de_noeuds_intermediaire)
            self.nouvel_individu(r, 0, 0)

    def selection(self, ajouter_meilleur_au_anciens:bool = True, afficher_meilleur:bool = False):
        match = zip(self.individus, self.score)
        l = sorted(match, key=operator.itemgetter(1), reverse = True)
        if afficher_meilleur:
            print("Score max : " + str(l[0][1]))

        self.reinit_individus()

        for ind in range(min(len(self.meilleurs_anciennes_generations), parametre.nombre_anciens_reintroduits)):
            sc = self.meilleurs_anciennes_generations[-ind-1][1] # on rajoute les derniers élémens qui ont étés ajoutés a la liste
            self.nouvel_individu(self.meilleurs_anciennes_generations[-ind-1][0], sc, sc)
        
        for ind in range(max(0, parametre.nombre_individus_selectionne-len(self.individus))):
            sc = l[ind][1]
            self.nouvel_individu(l[ind][0], sc, sc)

        # en plus de selectionner, on ajoute le meilleur element aux meilleurs elements des anciennes generations
        if ajouter_meilleur_au_anciens:
            self.meilleurs_anciennes_generations.append(l[0])

    def reproduction(self):

        n = len(self.individus)
        for ind in range(n):
            for _ in range(parametre.descendants_par_mutation):
                u = self.individus[ind].copy()

                u.mutate(parametre.taux_mutation, parametre.proba_mutation)
                self.nouvel_individu(u, 0, self.score[ind])

            for _ in range(parametre.descendants_par_bruitage):
                u = self.individus[ind].copy()

                u.mutate(parametre.taux_scramble, parametre.proba_scramble)
                self.nouvel_individu(u, 0, self.score[ind])

    def calculate_score(self):
        self.score = [0 for _ in self.individus]
        score_max_global = 0
        for _ in range(parametre.nombre_de_carte_pour_score):
            carte = parametre.lcarte[randint(0, len(parametre.lcarte))]
            nb_courses = len(self.individus)

            opponent = self.opponents[randint(0, len(self.opponents))]
            rsx = [(indiv, opponent) for indiv in self.individus]

            mem, nb_rebond = jeu(carte, parametre.nombre_de_tour, self.type_bot_hero, self.type_bot_vilain, rsx, nombre_de_course=nb_courses, cp_avant_teleportation=self.cp_avant_tp, entrainement_attaque=self.type_attaque)

            sc = []
            for i, l in enumerate(mem):
                (pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b) = l[-1]
                sc.append(self.fonction_score(carte, pod_j1_a, pod_j1_b, pod_j2_a, pod_j2_b, nb_rebond[i]))
            
            max_sc = max(sc)
            score_max_global += max_sc
            if self.type_attaque == 1:
                for i in range(len(self.individus)):
                    self.score[i]+= (sc[i]/max_sc)/ parametre.nombre_de_carte_pour_score
            elif self.type_attaque == -1:
                for i in range(len(self.individus)):
                    self.score[i]+= sc[i]/parametre.nombre_de_carte_pour_score
            else:
                print("Et la fonction score bgeww ?")

        if self.type_attaque == 1:
            for i in range(len(self.individus)):
                self.score[i]*=(10+score_max_global/parametre.nombre_de_carte_pour_score)
        

            
    def reload(self, population_name:str, new_inputs:list, new_nodes:int, aleat:float = 0.1, integre_meilleurs:bool = False):
        if len(self.individus)>0:
            print("Attention, des pods sont reloads dans une population non vide")

        with open(population_name+".txt", "r") as fichier:
            lignes = fichier.read().split('\n')
            indice = 0
            if lignes[0] != "######## Population actuelle ########":
                print("Le fichier qui a été reload n'est pas un fichier de bots")
            else:
                indice+=1
            
            while lignes[indice] != "######## Meilleurs individus ########":
                if lignes[indice][0:5]== 'SCORE':
                    sc = float(lignes[indice].split(' ')[2])

                    s = lignes[indice+1]+'\n'+lignes[indice+2]
                    r = evolve_network(s, new_inputs=new_inputs, new_nodes=new_nodes, aleat=aleat, type_attaque=self.type_attaque)
                    self.nouvel_individu(r, sc, sc)
                    indice+=3
                indice +=1
            
            if integre_meilleurs:
                n = len(lignes)
                while indice<n:
                    if lignes[indice][0:10]== 'Generation':
                        indice+=1
                        sc = float(lignes[indice].split(' ')[2])

                        s = lignes[indice+1]+'\n'+lignes[indice+2]
                        r = evolve_network(s, new_inputs=new_inputs, new_nodes=new_nodes, aleat=0, type_attaque=self.type_attaque)
                        self.meilleurs_anciennes_generations.append((r, sc))
                        indice+=3
                    indice +=1

    def save(self):
        with open(self.name+".txt", "w") as fichier:
            fichier.write("######## Population actuelle ########\n\n")
            for ind, rsx in enumerate(self.individus):
                fichier.write("SCORE : " + str(self.score[ind]) + "\n")
                fichier.write(rsx.compress())
                fichier.write("\n\n")
            
            fichier.write("\n\n######## Meilleurs individus ########\n\n")
            for ind, (rsx, score) in enumerate(self.meilleurs_anciennes_generations):
                fichier.write("Generation " + str(ind) + "\n")
                fichier.write("SCORE : " + str(score) + "\n")
                fichier.write(rsx.compress())
                fichier.write("\n\n")

    def get_meilleur(self):
        meilleur = argmax(self.score)
        return self.individus[meilleur]

    def afficher_meilleur(self, nombre_de_carte:int, nb_tour:int = 3):
        for t in range(nombre_de_carte):
            indice_carte = randint(0, len(parametre.lcarte))
            carte = parametre.lcarte[indice_carte]
            print("indice carte : ", indice_carte)

            meilleur = argmax(self.score)

            mem, nb_rebond = jeu(carte, nb_tour, self.type_bot_hero, self.type_bot_vilain, [(self.individus[meilleur], self.opponents[randint(0, len(self.opponents))])], nombre_de_course=1, cp_avant_teleportation=self.cp_avant_tp, entrainement_attaque = self.type_attaque)

            exemple = mem[0]

            lpod1 = []
            for _, l in enumerate(exemple):
                lpod1.append([[int(l[i][2]/parametre.reduction_factor), int(l[i][3]/parametre.reduction_factor), l[i][6]/180*pi]for i in range(4)])
            carte_cp_reduite = []

            for x,y in carte:
                carte_cp_reduite.append((x/parametre.reduction_factor, y/parametre.reduction_factor))
            affgame(carte_cp_reduite, lpod1)

    def ajoute_noeud_fin(self): # utlile pour une transfarmation d'une population une fois singulière
        for ntw in self.individus:
            n = len(ntw.layers)
            ntw.add_node(n)
            for i in range(len(ntw.layer_zero)):
                ntw.add_input_in_node(n, -i-1)
            for i in range(n):
                ntw.add_input_in_node(n, i)
        
        for ntw, _ in self.meilleurs_anciennes_generations:
            n = len(ntw.layers)
            ntw.add_node(n)
            for i in range(len(ntw.layer_zero)):
                ntw.add_input_in_node(n, -i-1)
            for i in range(n):
                ntw.add_input_in_node(n, i)

def f():
    pass

def update_population_attaque(fichier_ancien:str, fichier_nouveau:str):
    pops = Population(fichier_nouveau, 1, f, f, [Reseau()], f)
    pops.reload(fichier_ancien, [], 0, integre_meilleurs=True)
    pops.ajoute_noeud_fin()
    pops.save()