import tkinter as tk
import entrainement.parametre as parametre 
from math import cos, sin

class AnimationApp:
    def __init__(self, root, static_positions, moving_positions, timing_frame):
        self.root = root
        self.static_positions = static_positions
        self.moving_positions = moving_positions
        self.timing_frame = timing_frame
        self.canvas = tk.Canvas(root, width=int(16000/parametre.reduction_factor), height=int(9000/parametre.reduction_factor))
        self.canvas.pack()

        # Créer des objets statiques
        self.static_objects = [self.canvas.create_oval(x - 600/parametre.reduction_factor , y - 600/parametre.reduction_factor, x + 600/parametre.reduction_factor , y + 600/parametre.reduction_factor, fill="green") for x, y in static_positions]
        self.static_texte = [self.canvas.create_text(x, y, text=str(ind)) for ind, (x, y) in enumerate(static_positions)]
        # Créer des objets en mouvement
        self.moving_objects = [self.canvas.create_oval(- 400/parametre.reduction_factor , - 400/parametre.reduction_factor, 400/parametre.reduction_factor , 400/parametre.reduction_factor, fill=("yellow" if i<=1 else "red")) for i in range(len(moving_positions[0]))]
        self.orientation_pods = [self.canvas.create_line(50, 60,150, 60, width=5, arrow='last', arrowshape=(18,30, 8)) for i in range(len(moving_positions[0]))]
        self.move_pods(0)


    def move_pods(self, index):
        if index < len(self.moving_positions):
            for i in range(len(self.moving_positions[index])):
                x, y, orientation = self.moving_positions[index][i]
                dx = cos(orientation)
                dy = sin(orientation)
                self.canvas.coords(self.moving_objects[i], x - 400/parametre.reduction_factor , y - 400/parametre.reduction_factor, x + 400/parametre.reduction_factor , y + 400/parametre.reduction_factor)  # Met à jour la position de l'objet en mouvement
                self.canvas.coords(self.orientation_pods[i], x - dx*400/parametre.reduction_factor , y - dy*400/parametre.reduction_factor, x + dx*400/parametre.reduction_factor , y + dy*400/parametre.reduction_factor)  # Met à jour la position de l'objet en mouvement
            self.root.after(self.timing_frame, lambda: self.move_pods(index + 1))  # Attendre 1000 millisecondes avant d'animer le prochain objet en mouvement
        else:
            print("Fin de la Partie")

def affgame(position_CP, mouvements_pods, timing_frame = parametre.timing_frame):
    static_positions = position_CP
    moving_positions = mouvements_pods  
    root = tk.Tk()
    app = AnimationApp(root, static_positions, moving_positions, timing_frame)
    root.mainloop()