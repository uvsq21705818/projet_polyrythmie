#NK####

import tkinter as tk
import math
import random

#-#-# Constantes #-#-#

WIDTH = 1200
HEIGHT = 1200
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) / 2
omega = math.pi / 8 #vitesse angulaire
theta0 = (3 * math.pi) / 2 #angle de départ
dt = 0.02 #secondes
taille_objet = 20
temps_rotation = (2 * math.pi) / omega #secondes
tours = 0
LISTE_POLYRYTHMES = []

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["#D6ECFF", "#CCE8FF", "#C5E5FF", "#BFE2FF", "#B8DFFF", "#A8D7FF", "#A1D4FF", "#95CFFF", "#8ACAFF", "#80C5FF"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = (WIDTH / 2) + rayon_cercle * math.cos((omega * temps) + theta0)
    y = (HEIGHT / 2) + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y

def move():
    """Permet de faire bouger la boule du temps"""
    global temps, tours

    dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
    dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])

    for i in range(len(LISTE_POLYRYTHMES)):
        Rythme(LISTE_POLYRYTHMES[i]).move(LISTE_POLYRYTHMES[i])

    if temps - temps_rotation * tours > temps_rotation:
        tours +=1

    screen.move(objet_temps, dx, dy)
    temps += dt
    screen.after(int(dt*1000), move)


def trace_polyrythme(NOMBRE_DE_RYTHME):
    """Trace un motif polyrythmique avec un nombre N de mesures"""
    liste_points = []
    alpha = (3 * math.pi) / 2
    color = random.choice(LISTE_COULEUR)
    n = 0

    while n != NOMBRE_DE_RYTHME:
        x = (WIDTH / 2) + rayon_cercle * math.cos(alpha)
        y = (HEIGHT / 2) - rayon_cercle * math.sin(alpha)
        liste_points.append([x, y])
        alpha += (2 * math.pi) / NOMBRE_DE_RYTHME
        n +=1

    for i in range(len(liste_points)):
        screen.create_line(liste_points[i-1][0], liste_points[i-1][1], liste_points[i][0], liste_points[i][1], fill=color)

    objet = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#A2B5C7")
    liste_points.insert(0, objet)
    liste_points.insert(1, 0)

    LISTE_POLYRYTHMES.append(liste_points)


#-#-# Classes #-#-#

class Rythme:

    def __init__(self, liste):
        """Ici notre objet rythme sera une liste sous la forme [A, K, [x1, y1], ..., [xn, yn]] avec A l'objet associé à ce rythme,
        K le numéro du segment ou se trouve l'objet et [x, y] les coordonées de chaques sommets"""

        liste_points = liste.copy()
        liste_points.pop(0)
        liste_points.pop(0)
        nb_points = len(liste_points)

        objet = liste[0]
        segment = liste[1]

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.segment = segment

    def move(self, liste):
        global LISTE_POLYRYTHMES

        t_segment = temps_rotation / self.nb_points

        if self.segment == 0:
            x = self.liste_points[1][0] - self.liste_points[0][0]
            y = self.liste_points[1][1] - self.liste_points[0][1]
            liste[1] = 1
        else:
            for i in range(self.nb_points + 1):
                if self.segment == i:
                
                    if (temps - temps_rotation * tours) / i <= temps_rotation / self.nb_points:
                        x = self.liste_points[i][0] - self.liste_points[i-1][0]
                        y = self.liste_points[i][1] - self.liste_points[i-1][1]
                    else:
                        if i == self.nb_points - 1 or i == self.nb_points:
                            x = self.liste_points[0][0] - self.liste_points[i][0]
                            y = self.liste_points[0][1] - self.liste_points[i][1]

                            if (temps - temps_rotation * tours) > temps_rotation:
                                liste[1] = 1
                       
                        else:
                            x = self.liste_points[i+1][0] - self.liste_points[i][0]
                            y = self.liste_points[i+1][1] - self.liste_points[i][1]
                            liste[1] += 1           

        dx = (x * dt) / t_segment
        dy = (y * dt) / t_segment

        screen.move(self.objet, dx, dy)


    



#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval(((WIDTH / 2) - rayon_cercle), ((HEIGHT / 2) - rayon_cercle), ((WIDTH / 2) + rayon_cercle), ((HEIGHT / 2) + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")

#for i in range(3,7):
    #trace_polyrythme(i)
trace_polyrythme(3)
move()

screen.grid(column=0, row=0, rowspan=4)

root.mainloop()