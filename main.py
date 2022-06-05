#NK####aaaaaaaaaaaaaaaaaaaaa

import tkinter as tk
import math
import random
from tkinter import colorchooser
from turtle import left, right, width
import PIL
from PIL import ImageTk, Image
import winsound
from pysound.buffer import BufferParams
from pysound.oscillators import sine_wave
from pysound.oscillators import square_wave
from pysound import soundfile


#-#-# Constantes #-#-#

WIDTH = 900
HEIGHT = 900
dt = 0.001 #secondes
rayon_cercle = (min(WIDTH, HEIGHT) / 2) * 0.75
centre = (WIDTH / 2, HEIGHT / 2)
taille_objet = rayon_cercle / 12 #diamètre d'une boule
theta0 = (3 * math.pi) / 2
params = BufferParams(length=1000)

#COMPTEURS
temps = 0
tours = 0
compteur_dt = 0

#VARIABLES
vitesse = 0
acceleration = 10 #mesure arbitraire de l'accélération d'une boule d'un rythme sur un segment
vitesse_trainee = 6
longueur_trainee = 10
periode =  2 * math.pi
duree_de_vie_rebond = 50
vitesse_rebond = 0.5

LISTE_POLYRYTHMES = []
rythmes = []

is_paused = True
afficher_rebond = False
son = False
mode_avec_un_seul_son = False
frequence_du_son = 10

#COULEURS (c'est juste pour le style)#
LISTE_COULEUR = ["orange", "blue", "purple", "green", "yellow", "red", "aquamarine2", "indigo", "SlateBlue1", "DeepPink", "lime", "tan", "salmon"]
LISTE_CAMAIEU = ["#779CFF", "#77C3FF", "#77E8FF", "#77FFD8", "#77FF9A", "#ABFF77", "#D6FF77", "#FFFD77", "#FFD877", "#FFB377", "#FF8777"]

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
    """Bouge les boules ( ͡° ͜ʖ ͡°)"""
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
    color = LISTE_CAMAIEU[NOMBRE_DE_RYTHME-2]
    #LISTE_COULEUR.remove(color)
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
    #car on rajoute la correction au dernier segment                
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
                    
                    if j == 0:
                        coord_x = co_som[i][0]
                        coord_y = co_som[i][1]
                        liste_coord.append([coord_x, coord_y])

                    else:
                        coord_x = co_som[i][0] + (co_som[0][0] - co_som[i][0]) * accel
                        coord_y = co_som[i][1] + (co_som[0][1] - co_som[i][1]) * accel
                        liste_coord.append([coord_x, coord_y])

                else:

                    coord_x = co_som[i][0] + (co_som[i+1][0] - co_som[i][0]) * accel
                    coord_y = co_som[i][1] + (co_som[i+1][1] - co_som[i][1]) * accel
                    liste_coord.append([coord_x, coord_y])

    return liste_coord

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
        """Ici notre objet rythme sera une liste sous la forme [O, N, X, S, T, C, R] avec :
        # O l'objet associé à ce rythme,
        # N le numéro des coordonées ou se trouve l'objet (par rapport à la liste des coordonnées)
        # X la liste de toutes les coordonées parcourues par l'objet (sous la forme [[x,y], [x,y], ..., [x,y]])
        # S les coordonées de chaques sommets (sous la forme [[x1, y1], ..., [xn, yn]])
        # T la liste contenant tout les objets de la trainée (sous la forme [[Objet_1, Durée], ..., [Objet_n, Durée]])
        # C la couleur associée à ce rythme
        # R la liste contenant les objets des rebond"""

        liste_points = liste[3].copy()

        nb_points = len(liste_points)

        objet = liste[0]
        numero_coordonnee = liste[1]
        liste_coordonees = liste[2]
        liste_trainee = liste[4]
        color = liste[5]
        rebond = liste[6]

        self.nb_points= nb_points
        self.liste_points = liste_points
        self.objet = objet
        self.liste_coordonees = liste_coordonees
        self.numero_coordonee = numero_coordonnee
        self.liste_trainee = liste_trainee
        self.color = color
        self.rebond = rebond


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
                        winsound.PlaySound(creer_son(50), winsound.SND_ASYNC | winsound.SND_ALIAS)
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

        #réinitialiser le numéro et la position de l'objet au bout d'un tour
        if self.numero_coordonee == len(self.liste_coordonees):
            x = self.liste_coordonees[0][0]
            y = self.liste_coordonees[0][1]

            liste[1] = 0

        else:
            x = self.liste_coordonees[self.numero_coordonee][0]
            y = self.liste_coordonees[self.numero_coordonee][1]

            liste[1] += 1

        
        x1, y1, x2, y2 = transfo4(x, y, x, y, taille_objet/2)

        screen.coords(self.objet, x1, y1, x2, y2)




    def trainee(self):
        """sale trainée"""

        x = self.liste_coordonees[self.numero_coordonee - 1][0]
        y = self.liste_coordonees[self.numero_coordonee - 1][1]

        x1, y1, x2, y2 = transfo4(x, y, x, y, taille_objet/2)

        cercle_tempor = screen.create_oval(x1, y1, x2, y2, fill=self.color, outline=self.color)
        self.liste_trainee.append([cercle_tempor, longueur_trainee])

        
        if self.liste_trainee[0][1] == 0:
                screen.delete(self.liste_trainee[0][0])
                self.liste_trainee.pop(0)
    

        for i in range(len(self.liste_trainee)):
            self.liste_trainee[i][1] -= 1
            a = screen.coords(self.liste_trainee[i][0])[0]
            b = screen.coords(self.liste_trainee[i][0])[1]
            c = screen.coords(self.liste_trainee[i][0])[2]
            d = screen.coords(self.liste_trainee[i][0])[3]
            screen.coords(self.liste_trainee[i][0], a+1, b+1, c-1, d-1)


def transfo4(a, b, c, d, objet):
    """calcul intermédiaire"""
    x0 = a - objet
    y0 = b - objet
    x1 = c + objet
    y1 = d + objet
    return x0, y0, x1, y1


## FONTIONS LIEES AUX WIDGETS ##

def valider():
    global omega, periode, acceleration, longueur_trainee, vitesse_trainee, is_paused
    vitesse = s_speed.get()
    acceleration = s_acceleration.get()
    longueur_trainee = s_trace.get()
    vitesse_trainee = 50 / (s_trace_speed.get())
    omega = (math.pi / 2) *vitesse
    periode = (2 * math.pi) / omega

    for i in rythmes:
        trace_rythme(i)

    if is_paused == True:
        is_paused = False
        move_temps()
        butt.configure(text = 'Arrêter', command=arreter)
        #effacer tt dans le canvas et dans les listes 
    else : 
        is_paused = True
        butt.configure(text = 'Reprendre')

def arreter():
    global LISTE_POLYRYTHMES, cercle, rythmes, objet_temps, is_paused, temps, tours, compteur_dt
    is_paused = True
    screen.delete("all")
    LISTE_POLYRYTHMES = []
    rythmes = []
    temps = 0
    tours = 0
    compteur_dt = 0

    cercle = screen.create_oval((centre[0] - rayon_cercle), (centre[1] - rayon_cercle), (centre[0] + rayon_cercle),
                             (centre[1] + rayon_cercle), outline="gray")

    objet_temps = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2),
                                  centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2),
                                 fill="#EAF3FB", outline="#A2B5C7")

    butt.configure(text = 'Commencer', command=valider)


def etat(parametre):
    '''configure l'état d'une variable bouléenne. fonction liée aux Checkbuttons'''
    if parametre == False :
        parametre = True
    else :
        parametre = False


def etat_rebond():
    '''configure l'affichage ou non du rebond'''
    global afficher_rebond
    if afficher_rebond == False:
        afficher_rebond = True
        bouton_rebound.select()
    else : 
        afficher_rebond = False
        bouton_rebound.deselect()

def etat_son():
    global son
    if son == False :
        son = True
        bouton_son.select()
        bouton_mode_son.configure(state = 'normal')
    else : 
        son = False
        bouton_son.deselect()
        bouton_mode_son.configure(state = 'disabled')

def etat_mode_son():
    global mode_avec_un_seul_son
    if mode_avec_un_seul_son == False:
        mode_avec_un_seul_son = True
        bouton_mode_son.select()
    else :
        mode_avec_un_seul_son = False
        bouton_mode_son.deselect()


def input_rythm():
    global rythmes, pho
    if e_rythm.get() == "georges":
        textimage1 = Image.open("lesasa.JPG")
        textimage = textimage1.resize((HEIGHT, WIDTH))
        pho = ImageTk.PhotoImage(textimage)
        im = tk.Label(screen, image = pho)
        im.grid(row = 1)
    elif e_rythm.get() == "modolo":
        textimage1 = Image.open("modulo.JPG")
        textimage = textimage1.resize((HEIGHT, WIDTH))
        pho = ImageTk.PhotoImage(textimage)
        im = tk.Label(screen, image = pho)
        im.grid(row = 1)

    rythmes.append(int(e_rythm.get()))
    e_rythm.delete(0, 'end')


def info():
    global ph

    #####ça marche
    info_panel = tk.Toplevel()
    titre = tk.Label(info_panel, text = 'QUELQUES INFORMATIONS')
    textimage = Image.open("infos.png")
    ph = ImageTk.PhotoImage(textimage)
    im = tk.Label(info_panel, image = ph) 

    titre.grid(row = 0)
    im.grid(row = 1)
    

#-#-# Boucle Tkinter #-#-#

root = tk.Tk()
root.iconphoto(True, tk.PhotoImage(file='joscoo.png'))
root.title("aaaaaaaaaaaaaaaaaaa")

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval((centre[0] - rayon_cercle), (centre[1] - rayon_cercle), (centre[0] + rayon_cercle),
                             (centre[1] + rayon_cercle), outline="gray")
objet_temps = screen.create_oval(centre[0] - (taille_objet/2), (centre[1] + rayon_cercle) - (taille_objet/2),
                                  centre[0] + (taille_objet/2), (centre[1] + rayon_cercle) + (taille_objet/2),
                                 fill="#EAF3FB", outline="#A2B5C7")

infos = tk.Button(root, text = 'Infos ?', command = info)
v = tk.Label(root, text = 'vitesse')
a = tk.Label(root, text = 'accélération')
t = tk.Label(root, text = 'Traînée')
lt = tk.Label(root, text = 'longueur de la traînée')
vt = tk.Label(root, text = 'vitesse de trainée')
r = tk.Label(root, text = 'RYTHMES :')
s_speed = tk.Scale(root, orient = 'horizontal', from_ = 1, to = 10, tickinterval = 1, length = 250, label = 'vitesse')
s_acceleration = tk.Scale(root, orient = 'horizontal', from_ = 0, to = 15, tickinterval = 2, length = 300, label = 'accélération')
s_trace = tk.Scale(root, orient = 'horizontal', from_ = 0, to = 100, tickinterval = 10, length = 350,
                   label = 'longueur de la traînée')
s_trace_speed = tk.Scale(root, orient = 'horizontal', from_ = 5, to = 30, tickinterval = 5, length = 300,
                         label = 'vitesse de traînée')
s_duree_rebond = tk.Scale(root, orient = 'horizontal', from_ = 10, to = 80, tickinterval = 10, length = 300,
                         label = 'durée de vie du rebond')
bouton_rebound = tk.Checkbutton(root, text = 'rebonds aux sommets',cursor = 'gumby', command = etat_rebond)
bouton_son = tk.Checkbutton(root, text = 'son', command = etat_son)
bouton_mode_son = tk.Checkbutton(root, text = 'mode son unique', state = 'disabled', command = etat_mode_son)
e_rythm = tk.Entry(root, width = 10)
bouton_rythme = tk.Button(root, text = 'Ajouter', command = input_rythm)
bouton_pause = tk.Button(text = "PAUSE", command = pause)
butt = tk.Button(root, text = 'Commencer', command  = valider)

#Réglage par défaut
s_speed.set(2)
s_acceleration.set(5)
s_trace.set(10)
s_trace_speed.set(5)
s_duree_rebond.set(50)

#placement des widgets
screen.grid(column=3, row=0 , rowspan = 10)
#v.grid(row = 0, padx = 10)
infos.grid(column = 0, row = 0)
s_speed.grid(column = 0, row = 1, padx = 15, pady = 5, columnspan = 3)
#a.grid(row = 1, column = 0, padx = 10)
s_acceleration.grid(row =2, column = 0, padx = 15, pady = 5, columnspan = 3) 
t.grid(row = 3, column = 0, columnspan = 3)
#lt.grid(row = 3, column = 0, padx = 10)
s_trace.grid(row = 4, column = 0, padx = 15, pady = 5, columnspan = 3)
#vt.grid(row = 4, column = 0, padx = 10)
s_trace_speed.grid(row = 5, column = 0, padx = 15, pady = 5, columnspan = 3)
bouton_rebound.grid(row = 6, column = 0)
s_duree_rebond.grid(row = 6, column = 1, padx = 15, pady = 5, sticky = 'e')
bouton_son.grid(row = 7, column = 0)
bouton_mode_son.grid(row = 7, column = 1)
r.grid(row = 8, column = 0, padx = 10)
e_rythm.grid(row = 8, column = 1, padx = 10)
bouton_rythme.grid(row = 8, column = 2, padx = 10)
bouton_pause.grid(row = 9, column = 0, padx = 15)
butt.grid(row = 9, column = 1 , padx = 15)

root.mainloop()
