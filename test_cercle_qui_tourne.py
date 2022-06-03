import tkinter as tk
import math

WIDTH = 600
HEIGHT = 600
temps = 0
rayon_cercle = (min(WIDTH, HEIGHT) / 2) * 0.75
centre = (WIDTH/2, HEIGHT/2)
coord_sommet = [[299.99999999999994, 525.0], [494.85571585149876, 187.50000000000017], [105.14428414850147, 187.49999999999972]]
vitesse_angulaire = math.pi
theta = vitesse_angulaire * temps
dt=100

def rotation():
    x1 = (-1)*rayon_cercle*vitesse_angulaire*math.sin(theta)
    y1 = rayon_cercle*vitesse_angulaire*math.cos(theta)
    x1 += WIDTH/2
    y1 -= HEIGHT/2
    return x1, y1

def move():
    global temps, theta
    temps += dt
    theta = vitesse_angulaire * temps
    screen.coords(ligne1, 494.85571585149876, 187.50000000000017, rotation()[0], rotation()[1])
    print(theta)
    screen.after(dt, move)



root = tk.Tk()

screen = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg="black")
cercle = screen.create_oval((centre[0] - rayon_cercle), (centre[1] - rayon_cercle), (centre[0] + rayon_cercle), (centre[1] + rayon_cercle), outline="#2FA0FF")

screen.grid(column=0, row=0)

ligne1 = screen.create_line(coord_sommet[0][0], coord_sommet[0][1], coord_sommet[1][0], coord_sommet[1][1], fill="red")

move()

root.mainloop() 