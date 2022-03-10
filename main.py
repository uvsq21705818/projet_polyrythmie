import tkinter as tk
#import numpy as np
import math
import random

WIDTH = 600
HEIGHT = 600
theta = (-1) * math.pi / 2
t0 = 3
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) / 2
omega = math.pi / 2
dt = 0.01 #s

#COULEURS (c'est juste pour le style)
LISTE_COULEUR =["#D6ECFF", "#CCE8FF", "#C5E5FF", "#BFE2FF", "#B8DFFF", "#A8D7FF", "#A1D4FF", "#95CFFF", "#8ACAFF", "#80C5FF"]

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval(((WIDTH / 2) - rayon_cercle), ((HEIGHT / 2) - rayon_cercle), ((WIDTH / 2) + rayon_cercle), ((HEIGHT / 2) + rayon_cercle), outline="#2FA0FF")
taille_objet = 20
objet_temps = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")

def coord_temps(temps):
    x = (WIDTH / 2) + rayon_cercle * math.cos(omega * (t0 + temps))
    y = (HEIGHT / 2) - rayon_cercle * math.sin(omega * (t0 + temps))
    return x, y

def move():
    global temps

    #print((omega * temps)/(math.pi*1000))
    dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
    dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])
    print(math.cos(omega * temps), math.sin(omega * temps))
    screen.move(objet_temps, dx, dy)
    temps += dt
    screen.after(int(dt*1000), move)


def trace_polyrythme(NOMBRE_DE_RYTHME):
    liste_points = []
    alpha = math.pi / 2
    color = random.choice(LISTE_COULEUR)

    while alpha <= (2 * math.pi) + (math.pi / 2):
        liste_points.append(coord_temps(alpha))
        alpha += (2 * math.pi) / NOMBRE_DE_RYTHME
    print(liste_points)
    for i in range(len(liste_points)):
        screen.create_line((WIDTH/2) + liste_points[i-1][0], (HEIGHT/2) + liste_points[i-1][1], (WIDTH/2) + liste_points[i][0], (HEIGHT/2) + liste_points[i][1], fill=color)

move()

screen.grid(column=0, row=0, rowspan=4)

root.mainloop()