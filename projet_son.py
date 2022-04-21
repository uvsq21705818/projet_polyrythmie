#NK####

from tempfile import tempdir
import tkinter as tk
import math
import random
import numpy as np
from pysound.buffer import BufferParams
from pysound.oscillators import sine_wave
from pysound.oscillators import square_wave
from pysound import soundfile
from playsound import playsound
from threading import Thread

params = BufferParams(length=4410)

#-#-# Constantes #-#-#

WIDTH = 700
HEIGHT = 700
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) / 2
vitesse = 1
omega = (math.pi / 2) * vitesse
omega0 = (3 * math.pi) / 2
dt = 0.001 #secondes
taille_objet = 20
temps_rotation = (2 * math.pi) / omega #secondes
tours = 0
LISTE_POLYRYTHMES = []
is_paused = False
acceleration = 3
son = True

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["orange", "blue", "pink", "purple", "green", "yellow", "red"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = (WIDTH / 2) + rayon_cercle * math.cos((omega * temps) + omega0)
    y = (HEIGHT / 2) + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y

def creer_son(nombre_rythme):
    """Créer un son selon le nombre de rythme et renvoie le nom de ce son qui pourra être utilisé"""

    frequence = int(50 * nombre_rythme)
    wav_name = str(frequence) + ".wav"
    path = r"C:\Users\Lucas\Documents\PYTHON\projet_polyrythmie""\\" +  wav_name
    out = square_wave(params, frequency=frequence)
    soundfile.save(params, wav_name, out)


    return path


def move():
    """Permet de faire bouger la boule du temps"""
    global temps, tours

    if is_paused == False:
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

    nombre_sommet = len(liste_points)

    son = creer_son(nombre_sommet)

    nombre_de_coordonnees_rythme = temps_rotation // dt

    ### Pour n'avoir aucun décalage il faut le nombre de coordonées et le nobre de sommet soit entiers entre eux:
    while (nombre_de_coordonnees_rythme % nombre_sommet) != 0:
        nombre_de_coordonnees_rythme +=1

    nombre_de_coordonnees_segment = int(nombre_de_coordonnees_rythme / nombre_sommet)
    liste_coord = []

    for i in range(nombre_sommet):
        screen.create_line(liste_points[i-1][0], liste_points[i-1][1], liste_points[i][0], liste_points[i][1], fill=color)

        for j in range(nombre_de_coordonnees_segment):

            accel = (math.exp(acceleration * ((j+1)/nombre_de_coordonnees_segment)) / math.exp(acceleration)) * ((j+1) / nombre_de_coordonnees_segment)

            if i == nombre_sommet-1:
                coord_x = liste_points[i][0] + (liste_points[0][0] - liste_points[i][0]) * accel
                coord_y = liste_points[i][1] + (liste_points[0][1] - liste_points[i][1]) * accel
                liste_coord.append([coord_x, coord_y])
            else:
                coord_x = liste_points[i][0] + (liste_points[i+1][0] - liste_points[i][0]) * accel
                coord_y = liste_points[i][1] + (liste_points[i+1][1] - liste_points[i][1]) * accel
                liste_coord.append([coord_x, coord_y])

    objet = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill=color)
    liste_rythme = [objet, 0, liste_coord, liste_points, son]

    LISTE_POLYRYTHMES.append(liste_rythme)

def pause():
    global is_paused
    if is_paused == False:
        is_paused = True
    else:
        is_paused = False
        move()

#-#-# Classes #-#-#

class Rythme:

    def __init__(self, liste):
        """Ici notre objet rythme sera une liste sous la forme [A, N, C, S] avec :
        # A l'objet associé à ce rythme,
        # N le numéro des coordonées ou se trouve l'objet (par rapport à la liste des coordonnées)
        # C la liste de toutes les coordonées parcourues par l'objet (sous la forme [[x,y], [x,y], ..., [x,y]])
        # S les coordonées de chaques sommets (sous la forme [[x1, y1], ..., [xn, yn]])
        # M le son joué sur chaque sommet"""


        liste_points = liste[3].copy()

        nb_points = len(liste_points)


        objet = liste[0]
        numero_coordonnee = liste[1]
        liste_coordonees = liste[2]
        son = liste[4]
        numeros_sommets = []

        for i in range (nb_points):
            numeros_sommets.append(len(liste_coordonees) * ((i+1) / nb_points))

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.liste_coordonees = liste_coordonees
        self.numero_coordonee = numero_coordonnee
        self.numeros_sommets = numeros_sommets
        self.son = son

    def move(self, liste):
        global LISTE_POLYRYTHMES

        if self.numero_coordonee == len(self.liste_coordonees):
            x = self.liste_points[0][0]
            y = self.liste_points[0][1]

            liste[1] = 0

        else:
            x = self.liste_coordonees[self.numero_coordonee][0]
            y = self.liste_coordonees[self.numero_coordonee][1]

            liste[1] += 1

        x1 = x - (taille_objet / 2)
        y1 = y - (taille_objet / 2)
        x2 = x + (taille_objet / 2)
        y2 = y + (taille_objet / 2)

        if son == True:
            for numero in self.numeros_sommets:
                if self.numero_coordonee == numero:
                    playsound(self.son)

        screen.coords(self.objet, x1, y1, x2, y2)

    



#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval(((WIDTH / 2) - rayon_cercle), ((HEIGHT / 2) - rayon_cercle), ((WIDTH / 2) + rayon_cercle), ((HEIGHT / 2) + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle) - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")
bouton_pause = tk.Button(text="PAUSE", command=pause)

for i in range(3,9):
    trace_polyrythme(i)
move()

screen.grid(column=0, row=0)
bouton_pause.grid(row=1)

root.mainloop()