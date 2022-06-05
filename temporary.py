#NK####aaaaaaaaaaaaaaaaaaaaa

import tkinter as tk
import math
import random
from tkinter import colorchooser
from turtle import left, right, width
import winsound
from pysound.buffer import BufferParams
from pysound.oscillators import sine_wave
from pysound.oscillators import square_wave
from pysound import soundfile

params = BufferParams(length=2205)

#-#-# Constantes #-#-#

WIDTH = 900
HEIGHT = 900
dt = 0.001 #secondes
rayon_cercle = (min(WIDTH, HEIGHT) / 2) * 0.75
centre = (WIDTH / 2, HEIGHT / 2)
taille_objet = rayon_cercle / 12 #diamètre d'une boule
theta0 = (3 * math.pi) / 2
rythmes = {3,4}
moyenne_des_rythmes = sum(rythmes)/len(rythmes)
son = False

#COMPTEURS
temps = 0
tours = 0
compteur_dt = 1

#VARIABLES 
vitesse = 2
acceleration = 0 #mesure arbitraire de l'accélération d'une boule d'un rythme sur un segment
vitesse_trainee = 2
longueur_trainee = 0
durée_grossissement = 10

omega = (math.pi / 2) * vitesse
periode = (2 * math.pi) / omega #secondes

LISTE_POLYRYTHMES = []
is_paused = False

##Grossissement c'est pas très beau et ça fait bugger le programme
afficher_grossisement = False

mode_avec_un_seul_son = True
frequence_du_son = 10 #entre 1 et 10 (on peut aller plus haut mais ça fait mal aux oreilles)

afficher_rebond = True
duree_de_vie_rebond = 50
vitesse_rebond = 0.5

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR =["orange", "blue", "pink", "purple", "green", "yellow", "red"]

#-#-# Fonctions #-#-#

def creer_son(nombre_rythme):
    """Créer un son selon le nombre de rythme et renvoie le nom de ce son qui pourra être utilisé"""

    frequence = int(50 * nombre_rythme)
    wav_name = str(frequence) + ".wav"
    path = r"C:\Users\Lucas\Documents\PYTHON\projet_polyrythmie""\\" +  wav_name
    out = square_wave(params, frequency=frequence)
    soundfile.save(params, wav_name, out)


    return wav_name

def coord_temps(temps):
    """Calcule les coordonnées de la boule à un instant donné"""
    x = centre[0] + rayon_cercle * math.cos((omega * temps) + theta0)
    y = centre[1] + rayon_cercle * math.sin((omega * temps) + math.pi/2)

    return x, y


def move_temps():
    """Bouge les boules"""
    global temps, tours, compteur_dt

    if is_paused == False:
        #pour l'objet temps
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

    else:
        correction_nombre_coordonnee = 0


    for i in range(nb_sommet):

        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill=color)
        screen.create_line(centre[0], centre[1], coord_sommet[i-1][0], coord_sommet[i-1][1], fill="gray")

    liste_coord = calcul_coord(nb_sommet, correction_nombre_coordonnee, nb_coord_1segment, coord_sommet)

    
    objet = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2), centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2), fill=color)
    liste_rythme = [objet, 0, liste_coord, coord_sommet, [], color, []]

    LISTE_POLYRYTHMES.append(liste_rythme)


def calcul_coord (n, corr, coord_par_seg, co_som):
    """retourne une liste contenant toutes les positions de la boule pour un polygone à n sommets, 
    avec une certaine correction corr, et un nombre de coordonnées par segement déja défini, la liste
    des coordonnées des sommets déjà connue,  en tenant compte de l'acceleration"""
    liste_coord = []
    for  i in range(n):
        if i == n-1 and corr != 0:
                
            for j in range(coord_par_seg + corr):

                if j == 0:
                    coord_x = co_som[i][0]
                    coord_y = co_som[i][1]
                    liste_coord.append([coord_x, coord_y])

                else:

                    accel = (math.exp(acceleration * ((j+1)/coord_par_seg)) / math.exp(acceleration)) * ((j+1) / coord_par_seg)

                    coord_x = co_som[i][0] + (co_som[0][0] - co_som[i][0]) * accel
                    coord_y = co_som[i][1] + (co_som[0][1] - co_som[i][1]) * accel
                    liste_coord.append([coord_x, coord_y])

        else:
            for j in range(coord_par_seg):
                
                #facteur
                accel = (math.exp(acceleration * ((j+1)/coord_par_seg)) / math.exp(acceleration)) * ((j+1) / coord_par_seg)

                if i == n-1:
                    
                    coord_x = co_som[i][0] + (co_som[0][0] - co_som[i][0]) * accel
                    coord_y = co_som[i][1] + (co_som[0][1] - co_som[i][1]) * accel
                    liste_coord.append([coord_x, coord_y])

                else:

                    coord_x = co_som[i][0] + (co_som[i+1][0] - co_som[i][0]) * accel
                    coord_y = co_som[i][1] + (co_som[i+1][1] - co_som[i][1]) * accel
                    liste_coord.append([coord_x, coord_y])

    return liste_coord



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
        # C la couleur associée à ce rythme
        # G la liste contenant les objets des rebond"""

        liste_points = liste[3].copy()

        nb_points = len(liste_points)

        objet = liste[0]
        numero_coordonnee = liste[1]
        liste_coordonees = liste[2]
        liste_trainee = liste[4]
        color = liste[5]
        liste_taille_double = []
        liste_gros = []
        rebond = liste[6]

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.liste_coordonees = liste_coordonees
        self.numero_coordonee = numero_coordonnee
        self.liste_trainee = liste_trainee
        self.color = color
        self.rebond = rebond

        if afficher_grossisement == True:

            for i in range(len(self.liste_coordonees)):
                for sommet in self.liste_points:
                    if self.liste_coordonees[i] == sommet:
                        liste_taille_double.append(i-durée_grossissement)
                        for j in range((-1)*durée_grossissement + 1, durée_grossissement + 1):
                            liste_gros.append(i+j)
        
                    
        self.liste_taille_double = liste_taille_double
        self.liste_gros = liste_gros


    def move_rythm(self, liste):
        global LISTE_POLYRYTHMES, son

        ##REBOND

        if afficher_rebond == True:

            if self.liste_coordonees[self.numero_coordonee-1] in self.liste_points:

            

                if self.liste_coordonees[self.numero_coordonee-1] != self.liste_points[0]:
                    if mode_avec_un_seul_son == False:
                        winsound.PlaySound(creer_son(self.nb_points), winsound.SND_ASYNC | winsound.SND_ALIAS)
                    else:
                        winsound.PlaySound(creer_son(frequence_du_son), winsound.SND_ASYNC | winsound.SND_ALIAS)
                    son = True

                elif son == True:
                    if mode_avec_un_seul_son == False:
                        winsound.PlaySound(creer_son(moyenne_des_rythmes), winsound.SND_ASYNC | winsound.SND_ALIAS)
                    else:
                        winsound.PlaySound(creer_son(frequence_du_son), winsound.SND_ASYNC | winsound.SND_ALIAS)
                    son = False
                    
                

                x_rebond = self.liste_coordonees[self.numero_coordonee-1][0]
                y_rebond = self.liste_coordonees[self.numero_coordonee-1][1]
                cercle = screen.create_oval(x_rebond + 5, y_rebond + 5, x_rebond - 5, y_rebond - 5, width=(duree_de_vie_rebond/5), outline=self.color)
                self.rebond.append([cercle, duree_de_vie_rebond])

            for objet in self.rebond:
                if objet[1] >= 0:
                    x1_objet = screen.coords(objet[0])[0] - vitesse_rebond
                    y1_objet = screen.coords(objet[0])[1] - vitesse_rebond
                    x2_objet = screen.coords(objet[0])[2] + vitesse_rebond
                    y2_objet = screen.coords(objet[0])[3] + vitesse_rebond

                    epaisseur_objet = objet[1]/5

                    objet[1] -= vitesse_rebond

                    screen.coords(objet[0], x1_objet, y1_objet, x2_objet, y2_objet)
                    screen.itemconfig(objet[0], width = epaisseur_objet)

                else:
                    screen.delete(objet[0])
                    self.rebond.remove(objet)

        ##COORDONNEES

        if self.numero_coordonee == len(self.liste_coordonees):
            x = self.liste_coordonees[1][0]
            y = self.liste_coordonees[1][1]

            liste[1] = 1

        else:
            x = self.liste_coordonees[self.numero_coordonee][0]
            y = self.liste_coordonees[self.numero_coordonee][1]

            liste[1] += 1

        if self.numero_coordonee in self.liste_taille_double:

            self.double_taille()

        elif self.numero_coordonee in self.liste_gros: 
            x1, y1, x2, y2 = transfo4(x, y, x, y, taille_objet)

            screen.coords(self.objet, x1, y1, x2, y2)

        else: 
            x1, y1, x2, y2 = transfo4(x, y, x, y, taille_objet/2)

            screen.coords(self.objet, x1, y1, x2, y2)



    def trainee(self):
        """sale trainée"""

        x = self.liste_coordonees[self.numero_coordonee - 1][0]
        y = self.liste_coordonees[self.numero_coordonee - 1][1]

        x1, y1, x2, y2 = transfo4(x, y, x, y, taille_objet/2)

        cercle_tempor = screen.create_oval(x1, y1, x2, y2, fill = self.color)
        self.liste_trainee.append([cercle_tempor, longueur_trainee])

        
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

        x0, y0, x1, y1 = transfo4(screen.coords(objet)[0], screen.coords(objet)[1],
                                     screen.coords(objet)[2], screen.coords(objet)[3], taille_objet/2)


        screen.coords(objet, x0, y0, x1, y1)


def transfo4(a, b, c, d, objet):
    """calcul intermédiaire"""
    x0 = a - objet
    y0 = b - objet
    x1 = c + objet
    y1 = d + objet
    return x0, y0, x1, y1

#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval((centre[0] - rayon_cercle), (centre[1] - rayon_cercle), (centre[0] + rayon_cercle), (centre[1] + rayon_cercle), outline="#2FA0FF")
objet_temps = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2), centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2), fill="#EAF3FB", outline="#A2B5C7")
bouton_pause = tk.Button(text="PAUSE", command=pause)



for i in rythmes:
    trace_rythme(i)

move_temps()


screen.grid(column=0, row=0)
bouton_pause.grid(row=1)

print()

root.mainloop()
