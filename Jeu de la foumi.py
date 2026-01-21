import tkinter as tk

def speed(factor):
    global delay
    delay=int(factor)


root = tk.Tk()
root.title("Le jeu de la fourmi")
root.geometry("600x690")

fichier = open("fourmi.txt","w")

nb_cases = 51
Dim_Cnv = 600
Dim_C = Dim_Cnv // nb_cases
delay = 100  # Delai entre chaque animation 
Color_off = 'snow'
depart = (Dim_Cnv//2, Dim_Cnv//2, 'N')
stopped = False

canvas = tk.Canvas(root, width=Dim_Cnv, height=Dim_Cnv,background=Color_off)

#Creation de la grille
for i in range(nb_cases):
    for j in range(nb_cases):
        x1 = j * Dim_C
        y1 = i * Dim_C
        x2 = x1 + Dim_C
        y2 = y1 + Dim_C
        canvas.create_rectangle(x1,y1,x2,y2,fill = Color_off)


#creation du dictionnaire qui donnera les coordonnées de chaque cases
L_cases = {}
for i in range(nb_cases):
    for j in range(nb_cases):
        L_cases[i*nb_cases + j+1] = (i*Dim_C, j*Dim_C)

#creation de la liste qui comporte toute les cases
grille = []

for i in range(nb_cases):
    for j in range(nb_cases):
        grille.append(i*nb_cases + j+1)


#setup de départ
position = grille[nb_cases**2//2]
orientation = 'E'

visités = []
historique = []

y,x, = L_cases[position]
fourmi = canvas.create_polygon(x,y,x,y+Dim_C,x+Dim_C,y+(Dim_C//2), fill='purple')

###########################################################################################################

def mvmt():
    global orientation, position
    historique.append((position,orientation))
    fichier = open("fourmi.txt","w")
    fichier.write(str(historique))
    fichier.close()

    if position not in visités :
        visités.append(position)
        couleurs(position)

        if orientation == 'N':
            if position - nb_cases not in grille:
                position+= nb_cases**2 -nb_cases
            else :
                position -=nb_cases
            new_drctn = 'E'

        elif orientation == 'S':
            if position + nb_cases not in grille:
                position+= nb_cases - nb_cases**2
            else :
                position +=nb_cases
            new_drctn = 'W'

        elif orientation == 'E':
            if position + 1 not in grille:
                position= 1
            else:
                position +=1
            new_drctn = 'S'

        elif orientation == 'W':
            if position - 1 not in grille:
                position= nb_cases**2
            else:
                position -=1
            new_drctn = 'N'

    elif position in visités :
        visités.remove(position)
        couleurs(position)
        if orientation == 'N':
            if position + nb_cases not in grille:
                position-= nb_cases**2 -nb_cases
            else :
                position +=nb_cases
            new_drctn = 'W'

        elif orientation == 'S':
            if position - nb_cases not in grille:
                position-= nb_cases - nb_cases**2
            else :
                position -=nb_cases
            new_drctn = 'E'

        elif orientation == 'E':
            if position - 1 not in grille:
                position= nb_cases**2
            else:
                position -=1
            new_drctn = 'N'

        elif orientation == 'W':
            if position + 1 not in grille:
                position= 1
            else:
                position +=1
            new_drctn = 'S'
    
    else:
        print("Error, with visités or position")
    orientation = new_drctn
    dessiner_fourmi(position)

###########################################################################################################

#changement de couleur de la case a chaque fois que passage dessus en fonction de si dans liste "visités"
def couleurs(pos):
    y,x = L_cases[pos]
    if pos in visités:
        state = True
    else:
        state=False

    if state == True:
        canvas.create_rectangle(x,y,x+Dim_C,y+Dim_C, fill='black')
    elif state == False:
        canvas.create_rectangle(x,y,x+Dim_C,y+Dim_C, fill='snow')

###########################################################################################################


def dessiner_fourmi(pos):
    global fourmi, position
    y,x = L_cases[position]
    canvas.delete(fourmi)
    if pos in visités:
        if orientation == 'W':
            fourmi = canvas.create_polygon(x,y,x,y+Dim_C,x+Dim_C,y+(Dim_C//2), fill='purple')
        elif orientation=='E':
            fourmi = canvas.create_polygon(x+Dim_C, y, x, y+(Dim_C//2), x+Dim_C, y+Dim_C, fill='purple')
        elif orientation=='N':
            fourmi = canvas.create_polygon(x,y,x+(Dim_C//2),y+Dim_C, x+Dim_C, y, fill="purple")
        elif orientation=='S':
            fourmi = canvas.create_polygon(x,y+Dim_C, x+(Dim_C//2),y,x+Dim_C, y+Dim_C, fill='purple')
    elif pos not in visités:
        if orientation == 'E':
            fourmi = canvas.create_polygon(x,y,x,y+Dim_C,x+Dim_C,y+(Dim_C//2), fill='purple')
        elif orientation=='W':
            fourmi = canvas.create_polygon(x+Dim_C, y, x, y+(Dim_C//2), x+Dim_C, y+Dim_C, fill='purple')
        elif orientation=='S':
            fourmi = canvas.create_polygon(x,y,x+(Dim_C//2),y+Dim_C, x+Dim_C, y, fill="purple")
        elif orientation=='N':
            fourmi = canvas.create_polygon(x,y+Dim_C, x+(Dim_C//2),y,x+Dim_C, y+Dim_C, fill='purple')
###########################################################################################################

def next():
    global historique
    mvmt()

def stop():
    global stopped
    stopped = True
    Start.config(text="Start", command=start)

###########################################################################################################

def bouger():
    global historique
    mvmt()
    if not stopped:
        root.after(delay, bouger)

def start():
    global stopped
    Start.config(text="stop", command=stop)
    stopped = False
    bouger()

###########################################################################################################

#commande pour retour en arriere
def previous():
    global position, orientation, fourmi, visités
    position, orientation = historique[-1]
    canvas.delete(fourmi)

    if len(historique) == 1:
        position, orientation = historique[0]
        visités.clear()
        couleurs(position)
        couleurs(position)
        y,x, = L_cases[position]
        fourmi = canvas.create_polygon(x,y,x,y+Dim_C,x+Dim_C,y+(Dim_C//2), fill='purple')

    else:
        if position in visités:
            visités.remove(position)
        elif position not in visités:
            visités.append(position)

        couleurs(position)
        historique.pop()
        fichier = open("fourmi.txt","w")
        fichier.write(str(historique))
        fichier.close()
        dessiner_fourmi(position)


###########################################################################################################

tk.Button(text="Previous", command=previous).grid(column=3, row=2, sticky=tk.NSEW)
tk.Button(text="Quitter", command=lambda:exit()).grid(column=4, row=2, sticky=tk.NSEW)
Start = tk.Button(text="Start", command=start)
tk.Button(text="Next", command=next).grid(column=1, row=2, sticky=tk.NSEW)
scale = tk.Scale(from_ =1, to = delay*3, orient = "horizontal",label='delay', command=speed)
scale.set(delay)
scale.grid(column=2, row=2, sticky=tk.NSEW)
Start.grid(column=0, row=2, sticky=tk.NSEW)
canvas.grid(column=0,row=0, columnspan=5)

root.mainloop()