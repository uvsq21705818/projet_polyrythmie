#NK####

import tkinter as tk
import math
import random

#-#-# Constantes #-#-#

WIDTH = 1200
HEIGHT = 800
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) / 2
omega = math.pi / 2
omega0 = (3 * math.pi) / 2
dt = 0.02 #secondes
taille_objet = 20

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["#D6ECFF", "#CCE8FF", "#C5E5FF", "#BFE2FF", "#B8DFFF", "#A8D7FF", "#A1D4FF", "#95CFFF", "#8ACAFF", "#80C5FF"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule du temps"""
    x = (WIDTH / 2) + rayon_cercle * math.cos((omega * temps) + omega0)
    y = (HEIGHT / 2) - rayon_cercle * math.sin((omega * temps) + omega0)
    return x, y

def move():
    """Permet de faire bouger la boule du temps"""
    global temps

    dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
    dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])

    screen.move(objet_temps, dx, dy)
    temps += dt
    screen.after(int(dt*1000), move)


def trace_polyrythme(NOMBRE_DE_RYTHME):
    """Trace un motif polyrythmique avec un nombre N de mesures"""
    liste_points = []
    alpha = (3 * math.pi) / 2
    color = random.choice(LISTE_COULEUR)

    while alpha <= (2 * math.pi) + ((3 * math.pi) / 2):
        x = (WIDTH / 2) + rayon_cercle * math.cos(alpha)
        y = (HEIGHT / 2) - rayon_cercle * math.sin(alpha)
        liste_points.append([x, y])
        alpha += (2 * math.pi) / NOMBRE_DE_RYTHME

    for i in range(len(liste_points)):
        screen.create_line(liste_points[i-1][0], liste_points[i-1][1], liste_points[i][0], liste_points[i][1], fill=color)

#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval(((WIDTH / 2) - rayon_cercle), ((HEIGHT / 2) - rayon_cercle), ((WIDTH / 2) + rayon_cercle), ((HEIGHT / 2) + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")

trace_polyrythme(5)
move()

screen.grid(column=0, row=0, rowspan=4)

root.mainloop()