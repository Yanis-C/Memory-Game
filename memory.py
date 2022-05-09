from tkinter import *
from random import shuffle, randrange
from pygame import mixer

def start():
    for ligne in range(nb_lignes):
        for col in range(nb_col):
            centre=(x0+col*cote, y0+ligne*cote) #Centre de chaque case
            index= tableau[ligne][col]
            log=logos[index] 
            id_image=canv.create_image(centre, image=log)
            id_cover= canv.create_image(centre, image=cover)
            ids_cover[ligne][col] = id_cover


def melange():
    cartes = []
    cartes=list(range(nb_paires))*2 #Liste avec chaque numéro deux fois (forme une paire)
    shuffle(cartes)
    tableau=[]
    k=0
    for ligne in range(nb_lignes):
        row=[]
        for col in range(nb_col):
            row.append(cartes[k])
            k+=1
        tableau.append(row)
    #On coupe la liste selon le nb de lignes/colonnes
    return tableau



def afficher(event):
    x, y = event.x, event.y
    ligne = y//cote
    col = x//cote
    global essai,test1,pos1,coups

    if tableau[ligne][col]=="Fini": #Si la case est déjà dévoilée -> annuler
        return
    if (essai%2)==0:
        #On récupère l'id de la carte et sa position, puis on supprime la couverture
        test1=tableau[ligne][col]
        cov_id=ids_cover[ligne][col]
        canv.delete(cov_id)
        pos1= (ligne, col)
        essai+=1
        return essai, test1, pos1
    elif (essai%2)==1:
        #On récupère l'id de la carte et sa position, puis on supprime la couverture
        pos2= (ligne, col)
        if pos1==pos2: #Si on clique sur la même case pour les deux coups -> annuler
            return    
        c=cpt.get() #On incrémente le compteur de coups après le deuxième clic
        cpt.set(c+1)
        test2=tableau[ligne][col]
        cov_id=ids_cover[ligne][col]
        canv.delete(cov_id)        
        comp(test1, test2, pos1, pos2)
        essai+=1

        return essai
    
#Fonction de comparaison des deux cases
def comp(test1, test2, pos1, pos2): 
    global trouve
    if test1==test2:
        ligne, col = pos1
        tableau[ligne][col]="Fini"
        ligne, col = pos2
        tableau[ligne][col]="Fini"
        #On enleve l'id du tableau pour ne pas rejouer avec les cases dévoilées
        trouve+=1
        pair_cpt.set(trouve)
        win(nb_paires, trouve)
        return tableau, trouve
    else:
        canv.unbind("<Button>")
        canv.after(800, recouvrir, pos1)
        canv.after(800, recouvrir, pos2)
        #On recouvre les cases si elles ne sont pas identiques

def recouvrir(pos):
    ligne, col=pos
    c = (x0 + col * cote, y0 + ligne * cote)
    id_cover=canv.create_image(c, image=cover)
    ids_cover[ligne][col]=id_cover
    canv.bind("<Button>", afficher)


def play(path):
    mixer.init()
    mixer.music.load(path)
    mixer.music.play()


def win(nb_paires, trouve):
    if nb_paires==trouve:
        play(winpath)
        lbl_win=Label(fenet1, text="Bravo !!", font="Arial 18")
        lbl_win.pack()
        return


# Variables

winpath = r"./res/win.mp3"

#Dimensions
cote=130
#Il est possible de changer le nombre de lignes (max 4) et de colonnes (max 5)
nb_lignes=4
nb_col=4
width=cote*nb_col
height=cote*nb_lignes
x0=y0=cote//2
nb_paires=(nb_lignes*nb_col)//2

logos=[]
tableau = melange()  #Mélange des cartes en console

#Création fenetre et canvas
fenet1 = Tk()
fenet1.withdraw()

canv = Canvas(fenet1, width=width, height=height, background='grey')
canv.pack(side=LEFT)
cover= PhotoImage(file='./res/case.gif')
ids_cover=[[None for j in range(nb_col)] for i in range(nb_lignes)]

cpt = IntVar()
pair_cpt= IntVar()


#Variables temporaires
test1=0
test2=0
pos1 = 0
essai=0
trouve=0
status="Fini"


#Programme principal
def init():
    global fenet1
    fenet1.deiconify()
    fenet1.title("Memory Game")


    #Compteur de coups
    cpt_label=Label(fenet1, text="Nb de coups", font="Arial 12")
    cpt_label.pack(padx=10, pady=10)
    cpt.set(0)
    cpt_aff=Label(fenet1, textvariable=cpt, font="courier 20 bold")
    cpt_aff.pack()

    #Compteur de paires
    pair_label=Label(fenet1, text="Paires Trouvées", font="Arial 12")
    pair_label.pack(padx=10, pady=10)
    pair_cpt.set(0)
    pair_aff=Label(fenet1, textvariable=pair_cpt, font="courier 20 bold")
    pair_aff.pack()

    #Liste contenant toutes les images du memory
    for i in range(nb_paires):
        logo=PhotoImage(file="./res/pair%s.gif" %(i+1))
        logos.append(logo)


    start() #Début de la partie, affichage des cartes et des couvertures sur l'interface

    canv.bind("<Button>", afficher) 

    fenet1.mainloop()

init()