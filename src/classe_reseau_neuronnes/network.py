from classe_reseau_neuronnes.nodes import*
from numpy.random import uniform, binomial, normal, randint

class Reseau:
    def __init__(self, layer_zero:list=[], layers:list=[], atq:int = 1):
        self.layer_zero = layer_zero.copy() # il s'agit des inputs du réseau
        self.layers = layers.copy() # il s'agit des noeuds du réseau. Les deux derniers donnent vitesse angle
        self.attaque=atq # 1 correspond à attaque, -1 à défense, 0 à général

    def initialisation_aleatoire(self, inputs:list, nombre_de_noeuds_intermediaire:int): 
        
        if self.attaque == 0:
            raise ValueError("Attention : Un réseau global est initialisé aléatoirement")

        for input_name in inputs:
            self.add_input(input_name)
        
        nb_dep = nombre_de_noeuds_intermediaire + (2 if (self.attaque==1) else 3) # deux noeuds de sortie dans le cas d'un Pod d'attaque, 3 sinon

        for j in range(nb_dep):
            self.add_node(0, offset = uniform(-1,1,1)[0]*len(inputs))
            

        n = len(inputs)

        for i in range(n):
            for j in range(nb_dep):
                if i<=1:
                    self.add_input_in_node(j, -i-1, uniform(-1,1,1)[0], uniform(-1,1,1)[0], uniform(-1,1,1)[0])
                else:
                    self.add_input_in_node(j, -i-1, 0, 0, 0)

        for i in range(nb_dep-1):
            for j in range(i+1, nb_dep):
                self.add_input_in_node(j, i, uniform(-1,1,1)[0], uniform(-1,1,1)[0], uniform(-1,1,1)[0])
    
    def set_input(self, l_value: list):
        for i, val in enumerate(l_value):
            self.layer_zero[i].output = val
    
    def get_output(self):
        # renvoie un nombre entre -1 et 1 (angle du quel il faut tourner entre -18 et 18) et unautre entre 0 et 1 (Thrust divisée par 100)
        for node in self.layers:
            node.calc_output()
        
        if self.attaque==1 or self.attaque==-1:
            return min(1, max(-1, self.layers[-3].output)), min(1, max(0, self.layers[-2].output)), min(1, max(-1, self.layers[-1].output))
        else:
            return (
                min(1, max(-1, self.layers[-8].output)), # angle pod 1 
                min(1, max(0, self.layers[-7].output)), # puissance pod 1
                min(1, max(0, self.layers[-6].output)), # utilisation du shield ? 
                min(1, max(0, self.layers[-5].output)), # utilisation du boost ?
                min(1, max(-1, self.layers[-4].output)), # angle pod 2
                min(1, max(0, self.layers[-3].output)), # puissance pod 2
                min(1, max(0, self.layers[-2].output)), # utilisation du shield ?
                min(1, max(0, self.layers[-1].output)) # utilisation du boost ?
            )
        
    def add_node(self, index, l_inputs = [], l_params = [], offset = 0):
        n = Node(index, l_inputs, l_params, offset)
        for noeud in self.layers[index:len(self.layers)]:
            noeud.incr_index()
        self.layers = self.layers[0:index] + [n] + self.layers[index:len(self.layers)]

    def add_input_in_node(self, indice_1, indice_2, param_a = 0, param_b = 0, param_c = 0):
        if indice_2 >= indice_1:
            print("échec de la construction d'un input : il est interdit de mettre en entrée un des sucesseurs du noeud")
        else:
            if indice_2 < 0:# on essaye de rajouter un noeud de layer zero (un input du reseau)
                self.layers[indice_1].add_input(self.layer_zero[-indice_2-1], param_a, param_b, param_c)
            else:
                self.layers[indice_1].add_input(self.layers[indice_2], param_a, param_b, param_c)

    def add_input(self, nom):
        n = Node_layer_zero(nom, -len(self.layer_zero)-1)
        self.layer_zero.append(n)

    def change_param(self, indice_1, indice_2, param_a, param_b, param_c):
        self.layers[indice_1].modify_param(indice_2, param_a, param_b, param_c)

    def copy(self):
        lay_z = []
        for nd in self.layer_zero:
            new_nd = Node_layer_zero(nd.name, nd.index)
            lay_z.append(new_nd)
        
        lay = []
        for nd in self.layers:
            new_nd = Node(nd.index)
            new_nd.offset = nd.offset
            new_nd.age = nd.age
            for indice, input in enumerate(nd.inputs):
                j = input.index
                a, b, c = nd.params[indice]
                if j <0:
                    new_nd.add_input(lay_z[-j - 1], a, b, c)
                else:
                    new_nd.add_input(lay[j], a, b, c)

            lay.append(new_nd)
        
        

        copie = Reseau(lay_z, lay, atq = self.attaque)

        return copie

    def compress(self):
        s = 'inputs:'

        for nd in self.layer_zero:
            s+='#'+str(nd.index)+'/'+str(nd.name)
        
        s+='\nnoeuds:'
        for nd in self.layers:
            s+='#'+str(nd.index)+'/'+str(nd.age)+'/'+str(nd.offset)+'/'
            m = zip(nd.inputs, nd.params)
            for ndp, (a,b,c) in m:
                s+='@' + str(ndp.index) + '$' + str(a) + '$' + str(b) + '$' + str(c)
        
        return s

    def mutate(self, taux:float, proba_change:float):
        for i, noeud in enumerate(self.layers):
            for j in range(len(noeud.inputs)):
                off, a, b, c = binomial(1,proba_change/(noeud.age+1),4)*normal(0,taux/(noeud.age+1), 4)
                noeud.modify_offset(off*len(self.layer_zero))
                self.change_param(i, j, a, b, c) 

    def __str__(self):
        str_r =  "------------------ RESEAU DE NEURONE ------------------\n\n\n"

        str_r += "------------- Inputs -------------\n"
        for node in self.layer_zero:
            str_r+= "nom : " + node.name + ", index : " + str(node.index) + "\n"
        str_r += "------------- ------ -------------\n\n\n"

        str_r += "------------- Noeuds -------------"
        for node in self.layers:
            str_r+= "\n" + node.__str__() 
        str_r += "------------- ------ -------------\n"

        str_r += "\n------------------ ------------------ ------------------\n"

        return str_r


    # def new_node(self, portion_inputs_selectionnes:float):
    #     n = len(self.layers)
    #     i =  randint(0, n)
    #     l = []
    #     while len(l)==0:
    #         for j in range(len(self.layers[i].inputs)):
    #             if uniform(0.0, 1.0) < portion_inputs_selectionnes:
    #                 l.append(j)
        
    #     self.add_node(i)
        
    #     for j in l:
                       
def decompress(s:str, attaque:bool = 1):
    l = s.split('\n')

    lay_z = []
    for txt in l[0].split('#')[1:]:
        u = txt.split('/')
        new_nd = Node_layer_zero(u[1], int(u[0]))
        lay_z.append(new_nd)
    
    lay = []
    for txt in l[1].split('#')[1:]:
        u = txt.split('/')
        new_nd = Node(int(u[0]))
        if len(u)==4: ## pour rester compatible avec les modeles générés par les anciennes versions
            new_nd.age = int(u[1])
            eps = 1
        else:
            new_nd.age = int(u[0])
            eps = 0
        new_nd.offset = float(u[1+eps])
        for txt2 in u[2+eps].split('@')[1:]:
            u2 = txt2.split('$')
            j = int(u2[0])
            a, b, c = float(u2[1]),float(u2[2]),float(u2[3])
            if j <0:
                new_nd.add_input(lay_z[-j - 1], a, b, c)
            else:
                new_nd.add_input(lay[j], a, b, c)

        lay.append(new_nd)
    
    copie = Reseau(lay_z, lay, atq=attaque)

    return copie

def evolve_network(s:str, new_inputs:list = [], new_nodes:int = 0, aleat:float = 0.1, type_attaque = 1):
    # Reload un reseau en lui rajoutant des paramètres

    ntw = decompress(s, attaque=type_attaque)

    if new_nodes>0:
        for nd in ntw.layers:
            nd.incr_age()

    for _ in range(new_nodes):
        ntw.add_node(0, offset = uniform(-aleat, aleat)*(len(ntw.layer_zero)+len(new_inputs)))
        for i in range(len(ntw.layer_zero)):
            ntw.add_input_in_node(0, -i-1, uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0])
        for j in range(1, len(ntw.layers)):
            ntw.add_input_in_node(j, 0, uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0])

    k = len(ntw.layer_zero)
    n = len(new_inputs)

    for input_name in new_inputs:
        ntw.add_input(input_name)

    for i in range(n):
        for j in range(len(ntw.layers)):
            ntw.add_input_in_node(j, -i-1-k, uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0], uniform(-aleat,aleat,1)[0])
    
    return ntw

def reunite(ntw_attaque:Reseau, ntw_defense:Reseau):
    # Pour éviter de modifier en place les valeurs des indices des ntw : 

    ntw_attaque = ntw_attaque.copy()

    ntw_defense = ntw_defense.copy()

    nb_de_noeud_atq = len(ntw_attaque.layers)
    for noeud in ntw_defense.layers[:len(ntw_defense.layers)-3]:
        noeud.incr_index(value = nb_de_noeud_atq-2)
    
    for noeud in ntw_defense.layers[len(ntw_defense.layers)-3:]:
        noeud.incr_index(value = nb_de_noeud_atq)

    ntw_attaque.add_node(nb_de_noeud_atq)# on rajoute un nouveaux output pour le "BOOST"

    ntw_defense.add_node(len(ntw_defense.layers))


    l_atq = ntw_attaque.layers
    l_def = ntw_defense.layers # question : est ce qu'on relie tous les noeuds entre attaquant et défenseurs ? 

    lays = l_atq[:len(l_atq)-4] + l_def[:len(l_def)-4] + l_atq[len(l_atq)-4:] + l_def[len(l_def)-4 :]
    lay_z = ntw_attaque.layer_zero+ntw_defense.layer_zero 

    val = len(ntw_attaque.layer_zero)
    for nd in lay_z[val:]:
        nd.index -= val

    ntw = Reseau(lay_z, lays, atq=0)

    return ntw


