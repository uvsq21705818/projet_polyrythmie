from main import *
screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill="#090809", width=7)
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill="#201920", width=5)
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill="#50334F", width=3)
        screen.create_line(coord_sommet[i-1][0], coord_sommet[i-1][1], coord_sommet[i][0], coord_sommet[i][1], fill=color)
        screen.create_line(centre[0], centre[1], coord_sommet[i-1][0], coord_sommet[i-1][1], fill="gray")