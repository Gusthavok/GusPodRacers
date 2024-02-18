class Node:
    def __init__(self, index, inputs = [], params = [], offset = 0):
        self.inputs = inputs.copy() # attention, les inputs doivent se situer précédemment dans la liste des paramètres
        self.params = params.copy() # Autant de couples que d'input
        self.offset = offset
        self.index = index
        self.output = 0

    def calc_output(self):
        somme = self.offset
        for i, noeud in enumerate(self.inputs):
            bit1 = max(0, (noeud.output-self.params[i][0]))
            bit2 = max(0, (-noeud.output+self.params[i][0]))
            somme += max(-1, min(1, bit1*self.params[i][1] + bit2*self.params[i][2]))
        self.output = somme

    def add_input(self, noeud, param_a = 0, param_b = 0, param_c = 0):
        est_present = False
        for n in self.inputs:
            if n is noeud:
                est_present = True
                print(n)
        if not est_present:
            self.inputs.append(noeud)
            self.params.append((param_a, param_b, param_c))
        else:
            print("échec de l'ajout d'un noeud dans les inputs d'un autre, car déja présent")
    
    def add_offset(self, value):
        self.offset += value
    
    def modify_param(self, indice, value_a, value_b, value_c):
        a, b, c = self.params[indice]
        self.params[indice] = (a + value_a, b + value_b, c + value_c)

    def modify_offset(self, new_offset):
        self.offset+=new_offset

    def incr_index(self):
        self.index+=1

    def __str__(self):
        str_n = "### Noeud " + str(self.index) + " ###\nOffset : "+ str(self.offset)+ "\nInputs : \n"
        for i, noeud in enumerate(self.inputs):
            str_n += "Noeud " + str(noeud.index) + " / params : " + str(self.params[i][0]) +" "+ str(self.params[i][1]) +" "+ str(self.params[i][2]) + "\n"
        
        str_n +="############\n"

        return str_n

class Node_layer_zero:
    def __init__(self, name, index):
        self.output = 0
        self.name = name
        self.index = index
    
    
    def change_value(self, value):
        self.output = value
    
    def __str__(self):
        str_n = "### Input (noeud de layer zero) " + str(self.index) + " ###\n"
        str_n +="############\n"
        return str_n



