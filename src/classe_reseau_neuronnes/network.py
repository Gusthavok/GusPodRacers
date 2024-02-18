from classe_reseau_neuronnes.nodes import*
from numpy.random import uniform, binomial, normal

class Reseau:
    def __init__(self, layer_zero:list=[], layers:list=[], atq:bool = True):
        self.layer_zero = layer_zero.copy() # il s'agit des inputs du réseau
        self.layers = layers.copy() # il s'agit des noeuds du réseau. Les deux derniers donnent vitesse angle
        self.attaque=atq

    def initialisation_aleatoire(self, inputs:list, nombre_de_noeuds_intermediaire:int):
        
        for input_name in inputs:
            self.add_input(input_name)
        
        nb_dep = nombre_de_noeuds_intermediaire + (2 if self.attaque else 3) # deux noeuds de sortie dans le cas d'un Pod d'attaque, 3 sinon

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
        
        if self.attaque:
            return min(1, max(-1, self.layers[-2].output)), min(1, max(0, self.layers[-1].output))
        else:
            return min(1, max(-1, self.layers[-3].output)), min(1, max(0, self.layers[-2].output)), min(1, max(-1, self.layers[-1].output))
    
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
            s+='#'+str(nd.index)+'/'+str(nd.offset)+'/'
            m = zip(nd.inputs, nd.params)
            for ndp, (a,b,c) in m:
                s+='@' + str(ndp.index) + '$' + str(a) + '$' + str(b) + '$' + str(c)
        
        return s

    def mutate(self, taux:float, proba_change:float):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i].inputs)):
                off, a, b, c = binomial(1,proba_change,4)*normal(0,taux, 4)
                self.layers[i].modify_offset(off*len(self.layer_zero))
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

def decompress(s:str, attaque:bool = True):
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
        new_nd.offset = float(u[1])
        for txt2 in u[2].split('@')[1:]:
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

def evolve_network(s:str, new_inputs:list = [], new_nodes:int = 0, aleat:float = 0.1, type_attaque = True):
    # Reload un reseau en lui rajoutant des paramètres

    ntw = decompress(s, attaque=type_attaque)

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