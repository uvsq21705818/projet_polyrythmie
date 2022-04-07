#NK####

import tkinter as tk
import math
import random

#-#-# Constantes #-#-#

WIDTH = 1000
HEIGHT = 1000
temps = 0 #mesure le temps absolu(?)
rayon_cercle = (min(WIDTH, HEIGHT) / 2) / 2
omega = math.pi / 2 #vitesse angulaire
theta0 = (3 * math.pi) / 2 #angle de départ
dt = 0.02 #secondes
taille_objet = 20
periode = (2 * math.pi) / omega #secondes
tours = 0
LISTE_POLYRYTHMES = []
is_paused = False

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["purple", "brown", "pink", "orange", "yellow", "green", "blue", "red"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = (WIDTH / 2) + rayon_cercle * math.cos((omega * temps) + theta0)
    y = (HEIGHT / 2) + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y

def move_temps():
    """Permet de faire bouger la boule du temps"""
    global temps, tours

    dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
    dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])

    for i in range(len(LISTE_POLYRYTHMES)):
        Rythme(LISTE_POLYRYTHMES[i]).move_rythm(LISTE_POLYRYTHMES[i])

    if temps - periode * tours > periode:
        tours +=1

    screen.move(objet_temps, dx, dy)
    temps += dt
    if is_paused == False:
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

    for i in range(len(coord_sommet)):
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], 
                            coord_sommet[i][0], coord_sommet[i][1], fill=color)

    objet = screen.create_oval((WIDTH/2) - (taille_objet/2), ((HEIGHT/2) + rayon_cercle)
                                 - (taille_objet/2), (WIDTH/2) + (taille_objet/2), ((HEIGHT/2)
                                  + rayon_cercle) + (taille_objet/2), fill=color)
    coord_sommet.insert(0, objet)
    coord_sommet.insert(1, 0)

    LISTE_POLYRYTHMES.append(coord_sommet)

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
        """Ici notre objet rythme sera une liste sous la forme [A, K, [x1, y1], ..., [xn, yn]] 
        avec A l'objet associé à ce rythme, K le numéro du segment ou se trouve l'objet et [x, y]
        les coordonées de chaques sommets"""

        liste_points = liste.copy()
        liste_points.pop(0)
        liste_points.pop(0)
        nb_points = len(liste_points)

        objet = liste[0]
        segment = liste[1] #compteur n-eme segment où se trouve la boule

        self.nb_points = nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.segment = segment

    def move_rythm(self, liste):
        global LISTE_POLYRYTHMES

        t_segment = periode / self.nb_points
        #print(self.segment)
        if self.segment == 0:
            x = self.liste_points[1][0] - self.liste_points[0][0]
            y = self.liste_points[1][1] - self.liste_points[0][1]
            liste[1] = 1
        else:
            for i in range(self.nb_points + 1):
                if self.segment == i:
                
                    if (temps - periode * tours) / i <= periode / self.nb_points and i != self.nb_points:
                        x = self.liste_points[i][0] - self.liste_points[i-1][0]
                        y = self.liste_points[i][1] - self.liste_points[i-1][1]
                    else:
            

                        if i == self.nb_points - 1:
                            x = self.liste_points[0][0] - self.liste_points[i][0]
                            y = self.liste_points[0][1] - self.liste_points[i][1]

                            liste[1] += 1
                        
                        elif i == self.nb_points:
                            x = self.liste_points[0][0] - self.liste_points[i-1][0]
                            y = self.liste_points[0][1] - self.liste_points[i-1][1]

                            if (temps - periode * tours) >= periode:
                                liste[1] = 1
                                screen.coords(self.objet, (WIDTH/2) - (taille_objet/2), ((HEIGHT/2) 
                                              + rayon_cercle) - (taille_objet/2), (WIDTH/2) + 
                                              (taille_objet/2), ((HEIGHT/2) + rayon_cercle) + 
                                              (taille_objet/2))
                            
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
bouton_pause = tk.Button(text="PAUSE", command=pause)
bouton_avant = tk.Button(text="STEP", command = move_temps)

#for i in range(3,7):
    #trace_polyrythme(i)
trace_rythme(3)
trace_rythme(5)
move_temps()

screen.grid(column=0, row=0)
bouton_pause.grid(row=1)
bouton_avant.grid(row=1, column= 1)

root.mainloop()