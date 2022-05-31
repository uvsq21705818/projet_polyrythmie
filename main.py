#NK####aaaaaaaaaaaaaaaaaaaaa

from tempfile import tempdir
import tkinter as tk
import math
import random
from turtle import left, right

#-#-# Constantes #-#-#

WIDTH = 600
HEIGHT = 600
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) * 0.75
centre = (WIDTH/2, HEIGHT/2)
vitesse = 2
omega = (math.pi / 2) * vitesse
theta0 = (3 * math.pi) / 2
dt = 0.001 #secondes
taille_objet = 20
periode = (2 * math.pi) / omega #secondes
tours = 0
LISTE_POLYRYTHMES = []
is_paused = False
acceleration = 5 #mesure arbitraire de l'accélération d'une boule d'un rythme sur un segment
vitesse_trainee = 5
compteur_dt = 0
longueur_trainee = 13
durée_grossissement = 10
grossisement = False

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["orange", "blue", "pink", "purple", "green", "yellow", "red"]

#-#-# Fonctions #-#-#

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = centre[0] + rayon_cercle * math.cos((omega * temps) + theta0)
    y = centre[1] + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y


def move_temps():
    """Bouge les boules"""
    global temps, tours, compteur_dt

    if is_paused == False:
        dx = (coord_temps(temps + dt)[0] - coord_temps(temps)[0])
        dy = (coord_temps(temps + dt)[1] - coord_temps(temps)[1])

        for i in range(len(LISTE_POLYRYTHMES)):
            Rythme(LISTE_POLYRYTHMES[i]).move_rythm(LISTE_POLYRYTHMES[i])
            if compteur_dt == vitesse_trainee:
                Rythme(LISTE_POLYRYTHMES[i]).trainee()

                
        if compteur_dt == vitesse_trainee:
            compteur_dt = 0

        if temps - periode * tours > periode:
            tours +=1

        screen.move(objet_temps, dx, dy)
        temps += dt
        compteur_dt += 1
        screen.after(int(dt*1000), move_temps)


def trace_rythme(NOMBRE_DE_RYTHME):
    """Trace un motif polyrythmique avec un nombre N de mesures"""
    global LISTE_COULEUR

    coord_sommet = []
    alpha = theta0
    color = random.choice(LISTE_COULEUR)
    LISTE_COULEUR.remove(color)
    n = 0

    while n != NOMBRE_DE_RYTHME:
        x = centre[0] + rayon_cercle * math.cos(alpha)
        y = centre[1] - rayon_cercle * math.sin(alpha)
        coord_sommet.append([x, y])
        alpha += (2 * math.pi) / NOMBRE_DE_RYTHME
        n +=1



    
    nb_sommet = len(coord_sommet)
    #nombre de positions que peut prendre une boule pour un rythme en un tour
    nb_positions_rythme = periode // dt

    #nb de positions pour un segment
    nb_coord_1segment = int(nb_positions_rythme / nb_sommet)

    # Ici le problème est que en divisant le nombre total de coordonnées par le nombre de sommet pour avoir le nombre
    # de coordonnées dans un seul segment, nous devons avoir un nombre entier (int) de coordonnées pour 1 segment cependant comme on arrondit
    # cela modifie aussi le nombre total de coordonnées.
    # On peut donc se retrouver avec 2 rythmes qui on un nombre différent de coordonnées pour faire un tour du cercle
    # (par ex: 1330 pour un Rythme de 4 et 1332 pour un Rythme de 3).
    # Pour palier à cette différence (minime mais qui engendrera un léger décalage des objets à chaque tours),
    # on enregistre la différence de coordonnées par rapport à la base de coordonnées qu'on devrait avoir (nb_positions_rythme).
    # Cette différence sera en suite ajoutée aux coordonnées du dernier segment pour rééquilibrer les objets.
    #
    # Exemple: La base de coordonnées pour un tour est de 1331
    #
    # # L'objet du Rythme 4 possède un total de 1330 coordonnée 
    # # On ajoute donc 1 coordonnée au dernier segment (correction_nombre_coordonnee = 1)
    #
    # # L'objet du Rythme 3 possède un total de 1332 coordonnée
    # # On enlève donc 1 coordonnée au dernier segment (correction_nombre_coordonnee = -1)

    if nb_coord_1segment * nb_sommet != int(nb_positions_rythme):
        correction_nombre_coordonnee = int(nb_positions_rythme) - nb_coord_1segment * nb_sommet

    liste_coord = []

    for i in range(nb_sommet):
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill=color)
        screen.create_line(centre[0], centre[1], coord_sommet[i-1][0], coord_sommet[i-1][1], fill="gray")

        if i == nb_sommet-1 and correction_nombre_coordonnee != 0:
            
            for j in range(nb_coord_1segment + correction_nombre_coordonnee):

                accel = (math.exp(acceleration * ((j+1)/nb_coord_1segment)) / math.exp(acceleration)) * ((j+1) / nb_coord_1segment)

                coord_x = coord_sommet[i][0] + (coord_sommet[0][0] - coord_sommet[i][0]) * accel
                coord_y = coord_sommet[i][1] + (coord_sommet[0][1] - coord_sommet[i][1]) * accel
                liste_coord.append([coord_x, coord_y])


        else:
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

    objet = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2), centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2), fill=color)
    liste_rythme = [objet, 0, liste_coord, coord_sommet, [], color]

    LISTE_POLYRYTHMES.append(liste_rythme)


def cercle_bis(sommet):
    
    #for i in range(2):
    x0 = abs(sommet[i][0] - centre[0])
    y0 = abs(sommet[i][1] - centre[1])
    med0 = [x0/2, y0/2]
    pente_ortho0 = x0 / y0


    x1 = abs(sommet[1][0] - centre[0])
    y1 = abs(sommet[1][1] - centre[1])  
    med1 = [x1/2, y1/2]
    pente_ortho1 = x1 / y1
    
    a = np.array([pente_ortho0, -1], [pente_ortho1, -1])
    b = np.array([-med0[1]+pente_ortho0*med0[0]], [-med1[1]+pente_ortho1*med1[0]])

    sol = np.linalg.solve(a, b)

    return [sol[0], sol[1]]


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
        """Ici notre objet rythme sera une liste sous la forme [A, N, X, S, T, C] avec :
        # A l'objet associé à ce rythme,
        # N le numéro des coordonées ou se trouve l'objet (par rapport à la liste des coordonnées)
        # X la liste de toutes les coordonées parcourues par l'objet (sous la forme [[x,y], [x,y], ..., [x,y]])
        # S les coordonées de chaques sommets (sous la forme [[x1, y1], ..., [xn, yn]])
        # T la liste contenant tout les objets de la trainée (sous la forme [[Objet_1, Durée], ..., [Objet_n, Durée]])
        # C la couleur associée à ce rythme"""

        liste_points = liste[3].copy()

        nb_points = len(liste_points)

        objet = liste[0]
        numero_coordonnee = liste[1]
        liste_coordonees = liste[2]
        liste_trainee = liste[4]
        color = liste[5]
        liste_taille_double = []
        liste_gros = []

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.liste_coordonees = liste_coordonees
        self.numero_coordonee = numero_coordonnee
        self.liste_trainee = liste_trainee
        self.color = color

        if grossisement == True:

            for i in range(len(self.liste_coordonees)):
                for sommet in self.liste_points:
                    if self.liste_coordonees[i] == sommet:
                        liste_taille_double.append(i-durée_grossissement)
                        for j in range((-1)*durée_grossissement + 1, durée_grossissement + 1):
                            liste_gros.append(i+j)
        
                    
        self.liste_taille_double = liste_taille_double
        self.liste_gros = liste_gros


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

        if self.numero_coordonee in self.liste_taille_double:

            self.double_taille()

        elif self.numero_coordonee in self.liste_gros: 
            x1 = x - taille_objet
            y1 = y - taille_objet
            x2 = x + taille_objet
            y2 = y + taille_objet

            screen.coords(self.objet, x1, y1, x2, y2)
        else:

            x1 = x - (taille_objet / 2)
            y1 = y - (taille_objet / 2)
            x2 = x + (taille_objet / 2)
            y2 = y + (taille_objet / 2)

            screen.coords(self.objet, x1, y1, x2, y2)



    def trainee(self):
        "sale trainée"

        x = self.liste_coordonees[self.numero_coordonee - 1][0]
        y = self.liste_coordonees[self.numero_coordonee - 1][1]

        x1 = x - (taille_objet / 2)
        y1 = y - (taille_objet / 2)
        x2 = x + (taille_objet / 2)
        y2 = y + (taille_objet / 2)

        cercle_tempor = screen.create_oval(x1, y1, x2, y2, fill = self.color)
        self.liste_trainee.append([cercle_tempor, longueur_trainee])

    #print(self.liste_trainee)
        
        if self.liste_trainee[0][1] == 0:
                screen.delete(self.liste_trainee[0][0])
                self.liste_trainee.pop(0)
    

        for i in range(len(self.liste_trainee)):
            self.liste_trainee[i][1] -= 1

        #for objet in self.liste_trainee:
            #if objet[1] == 0:
                #self.liste_trainee.pop(0)

    def double_taille(self):

        objet = self.objet

        x0 = screen.coords(objet)[0] - taille_objet/2
        y0 = screen.coords(objet)[1] - taille_objet/2
        x1 = screen.coords(objet)[2] + taille_objet/2
        y1 = screen.coords(objet)[3] + taille_objet/2

        screen.coords(objet, x0, y0, x1, y1)


#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval((centre[0] - rayon_cercle), (centre[1] - rayon_cercle), (centre[0] + rayon_cercle), (centre[1] + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2), centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")
bouton_pause = tk.Button(text="PAUSE", command=pause)

for i in range(3,5):
    trace_rythme(i)
move_temps()

screen.grid(column=0, row=0)
bouton_pause.grid(row=1)

root.mainloop()
