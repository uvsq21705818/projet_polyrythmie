#NK####

from tempfile import tempdir
import tkinter as tk
import math
import random

from matplotlib.ft2font import HORIZONTAL

#-#-# Constantes #-#-#

WIDTH = 800
HEIGHT = 800
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) * 0.75
vitesse = 2 
omega = (math.pi / 2) * vitesse
theta0 = (3 * math.pi) / 2
dt = 0.001 #secondes
taille_objet = 20
periode = (2 * math.pi) / omega #secondes
tours = 0
LISTE_POLYRYTHMES = []
is_paused = False
acceleration = 0 #mesure arbitraire de l'accélération d'une boule d'un rythme sur un segment


#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["orange", "blue", "pink", "purple", "green", "yellow", "red"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = (WIDTH / 2) + rayon_cercle * math.cos((omega * temps) + theta0)
    y = (HEIGHT / 2) + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y


def move_temps():
    """Bouge les boule du temps"""
    global temps, tours

    if is_paused == False:
        dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
        dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])

        for i in range(len(LISTE_POLYRYTHMES)):
            Rythme(LISTE_POLYRYTHMES[i]).move_rythm(LISTE_POLYRYTHMES[i])

        if temps - periode * tours > periode:
            tours +=1

        screen.move(objet_temps, dx, dy)
        temps += dt
        screen.after(int(dt*1000), move_temps)


def trace_rythme(NOMBRE_DE_RYTHME):
    """Trace un motif polyrythmique avec un nombre N de mesures"""
    coord_sommet = []
    alpha = theta0
    color = random.choice(LISTE_COULEUR)
    n = 0

    while n != NOMBRE_DE_RYTHME:
        x = (WIDTH / 2) + rayon_cercle * math.cos(alpha)
        y = (HEIGHT / 2) - rayon_cercle * math.sin(alpha)
        coord_sommet.append([x, y])
        alpha += (2 * math.pi) / NOMBRE_DE_RYTHME
        n +=1

    nb_sommet = len(coord_sommet)
    #nombre de positions que peut prendre une boule pour un rythme en un tour
    nb_positions_rythme = periode // dt 

    ### Pour n'avoir aucun décalage il faut le nombre de coordonées et le nobre de sommet soit entiers entre eux:
    while (nb_positions_rythme % nb_sommet) != 0:
        nb_positions_rythme +=1

    #nb de positions pour un segment
    nb_coord_1segment = int(nb_positions_rythme / nb_sommet)
    liste_coord = []

    for i in range(nb_sommet):
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill=color)

        for j in range(nb_coord_1segment):
            
            #facteur
            accel = (math.exp(acceleration * ((j+1)/nb_coord_1segment)) / math.exp(acceleration)) * ((j+1) / nb_coord_1segment)

            if i == nb_sommet-1:
                coord_x = coord_sommet[i][0] + (coord_sommet[0][0] - coord_sommet[i][0]) * accel
                coord_y = coord_sommet[i][1] + (coord_sommet[0][1] - coord_sommet[i][1]) * accel
                liste_coord.append([coord_x, coord_y])
            else:
                coord_x = coord_sommet[i][0] + (coord_sommet[i+1][0] - coord_sommet[i][0]) * accel
                coord_y = coord_sommet[i][1] + (coord_sommet[i+1][1] - coord_sommet[i][1]) * accel
                liste_coord.append([coord_x, coord_y])

    objet = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill=color)
    liste_rythme = [objet, 0, liste_coord, coord_sommet]

    LISTE_POLYRYTHMES.append(liste_rythme)

def pause():
    global is_paused
    if is_paused == False:
        is_paused = True
    else:
        is_paused = False
        move_temps()

#-#-# Classes #-#-#

class Rythme:

    def __init__(self, liste):
        """Ici notre objet rythme sera une liste sous la forme [A, N, C, S] avec :
        # A l'objet associé à ce rythme,
        # N le numéro des coordonées ou se trouve l'objet (par rapport à la liste des coordonnées)
        # C la liste de toutes les coordonées parcourues par l'objet (sous la forme [[x,y], [x,y], ..., [x,y]])
        # S les coordonées de chaques sommets (sous la forme [[x1, y1], ..., [xn, yn]])"""

        liste_points = liste[3].copy()

        nb_points = len(liste_points)


        objet = liste[0]
        numero_coordonnee = liste[1]
        liste_coordonees = liste[2]

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.liste_coordonees = liste_coordonees
        self.numero_coordonee = numero_coordonnee

    def move_rythm(self, liste):
        global LISTE_POLYRYTHMES

        if self.numero_coordonee == len(self.liste_coordonees):
            x = self.liste_coordonees[0][0]
            y = self.liste_coordonees[0][1]

            liste[1] = 0

        else:
            x = self.liste_coordonees[self.numero_coordonee][0]
            y = self.liste_coordonees[self.numero_coordonee][1]

            liste[1] += 1

        x1 = x - (taille_objet / 2)
        y1 = y - (taille_objet / 2)
        x2 = x + (taille_objet / 2)
        y2 = y + (taille_objet / 2)

        screen.coords(self.objet, x1, y1, x2, y2)

    

def change_vitesse(val):

    global vitesse
    vitesse = val
    for i in range(3,5):
        trace_rythme(i)
    move_temps()

#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

curseur_v = tk.Scale(root, from_= 1, to = 10, orient = 'horizontal', command = change_vitesse )
c_v_label = tk.Label(root, text = 'vitesse')

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval(((WIDTH / 2) - rayon_cercle), ((HEIGHT / 2) - rayon_cercle), ((WIDTH / 2) + rayon_cercle), ((HEIGHT / 2) + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")
bouton_pause = tk.Button(text="PAUSE", command=pause)

for i in range(3,5):
    trace_rythme(i)
move_temps()

screen.grid(column=0, row=0, rowspan = 2 )
bouton_pause.grid(column=1, row = 0, padx = 10, rowspan = 2 )
curseur_v.grid(column = 2, row =0, padx = 10)
c_v_label.grid(column = 2, row = 1)


root.mainloop()