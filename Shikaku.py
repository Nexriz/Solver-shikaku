"""
Nom du fichier : Shikaku.py
Auteur         : Corentin Derrien
Date           : 1 juin 2025
Description    : Script de résolution de grille Shikaku
Version        : 1.0
"""

#Import des librairies nécessaires
import math
from matplotlib import cm, patches
import numpy as np
import random
import matplotlib.pyplot as plt


def rectangles_possibles(x, y, valeur, largeur_grille, hauteur_grille):
    """
    Ajoute tous les rectangles possibles selon la position x et y de la valeur

    Args:
        x (int): coordonnée x de la grille
        y (int): coordonnée y de la grille
        valeur (float): valeur présente au coordonnée de la grille
        largeur_grille (int): Largeur de la grille
        hauteur_grille (int): Hauteur de la grille

    Returns:
        list[tuple[tuple[int, int], tuple[int, int]]]: Renvoie la liste de rectangles possibles de la valeur
    """
    valeur = int(valeur) # caste en entier
    rectangles = []
    
    #Parcours tous la largeur de la grille (ligne)
    for largeur in range(1, valeur+1):
        #Parcours tous la hauteur de la grille (colonne)
        for hauteur in range(1, valeur+1) :
            #Vérifie si la surface est égale à la valeur donnée par l'utilisateur
            if hauteur * largeur != valeur: 
                continue
            #Décalage autour de la position du rectangle possible
            for dx in range(largeur):
                for dy in range(hauteur):
                    #Calcule les coins du rectangles
                    x1 = x - dx
                    y1 = y - dy
                    
                    x2 = x1 + largeur - 1
                    y2 = y1 + hauteur - 1
                    
                    #Vérifie que le rectangles reste dans la grille
                    if 0 <= x1 <= x2 < largeur_grille and 0 <= y1 <= y2 < hauteur_grille:
                        #Ajoute le rectangle à la liste
                        rectangles.append(((x1, y1),(x2, y2)))
    return rectangles
                    
        
def evaluation_fitness(solution, grille) :
    """
    Evalue la solution, en vérifiant si elle respecte les règles du shikaku

    Args:
        solution (dictionnaire): Dictionnaire de la solution de la forme {(x, y) : ((x1, y1), (x2, y2))} avec (x, y) position de la valeur dans la grille,
                        ((x1, y1), (x2, y2)) les rectangles choisis
                                
        grille (list[list[int]]): grille de jeu

    Returns:
        int: Un nombre correspondant au score de la solution (plus on est proche de 0 plus la solution est meilleur)
    """
    
    penality = 0 # score de la solution
    largeur = grille[0].size 
    hauteur = grille[1].size
    NewGrille = np.zeros((largeur, hauteur)) # nouvelle grille initialisée avec des zeros
    
    for cle, rect in solution.items() :
        x, y = cle #Position de la valeur
        valeur = grille[x][y] #Aire attendue du rectangles
        
        #Coin du rectangle
        PosRect1, PosRect2 = rect
        x1, y1 = PosRect1
        x2, y2 = PosRect2
        
        #Règle 1 : vérifie les chevauchements et ajoute une pénalité en cas de chevauchement
        for i in range(x1, x2+1) :
            for j in range(y1, y2+1) :
                if NewGrille[i][j] == 2 : #Case déja marqué
                    penality += 10 #Ajout de la pénalité
                NewGrille[i][j] = 2 #Marquage de la case pour dire qu'elle est utilisée
        
        #Règle 4 : Vérifie l'aire du rectangle
        area = ((x2 - x1)+1)*((y2-y1)+1) #Calcule de l'aire du rectangle qu'on a 
        if area != valeur :
            penality += abs(area - valeur) * 2 
            
    #Règle 2 : Vérifie si la grille est entièrement couverte et ajoute une pénalité si une des cases n'est pas couverte
    penality += np.sum(NewGrille == 0) * 5 #Pénalité en cas de case non couverte
    
    return -penality
    

def voisin(solution, grille) :
    """
    Génère une nouvelle solution en modifiant un des rectangles de la solution actuelle

    Args:
        solution (dictionnaire): Dictionnaire de la solution de la forme {(x, y) : ((x1, y1), (x2, y2))} avec (x, y) position de la valeur dans la grille,
                        ((x1, y1), (x2, y2)) les rectangles choisis
                                
        grille (list[list[int]]): grille de jeu
    Returns:
        dictionnaire: nouvelle solution avec un des rectangles modifiée
    """
    
    NewSolution = solution.copy() #Copie de la solution actuelle
    largeur = grille[0].size
    hauteur = grille[1].size
    number = list(solution.keys()) #Liste des positions des valeurs dans la grille
    
    x, y = random.choice(number) #Choix aléatoire d'une des positions
    valeur = grille[x][y]
    
    #Génère tous les rectangles possibles pour cette position
    NewRectangles = rectangles_possibles(x, y, valeur, largeur, hauteur)
    
    #Filtre dans les rectangles possibles le rectangles de la solution actuelle pour éviter une solution identique à l'actuelle
    rectangles = list(filter(lambda rect: rect != solution[(x, y)], NewRectangles))

    #Si aucun des rectangles n'existe, on renvoie la solution actuelle
    if len(rectangles) == 0:
        return NewSolution

    #Choix aléatoire d'un nouveau rectangles
    NewSolution[(x, y)] = random.choice(rectangles)
    return NewSolution

def RecuitSimuleShikaku(grille, temperature, refroidissement, max_iter) :
    """
    Résolution de la grille Shikaku avec l'utilisation de recuit simulé

    Args:
        grille (list[list[int]]): grille de jeu
        temperature (int): Température initiale
        refroidissement (float): Facteur de refroidissement
        max_iter (int): Nombre maximum d'itération

    Returns:
        dictionnaire: Solution optimale trouvé
    """
    
    print(grille) #Affiche la grille
    
    T_initial = temperature
    solution = {}
    largeur = grille[0].size
    hauteur = grille[1].size
    
    #Initialisation d'une solution
    for x in range(largeur) :
        for y in range(hauteur) :
            valeur = grille[x][y]
            if valeur != 0 :
                rectangles = rectangles_possibles(x, y, valeur, largeur, hauteur)
                if rectangles:
                    solution[(x, y)] = random.choice(rectangles)
    
    scoreSolution = evaluation_fitness(solution, grille) #Calcule du score de la solution actuelle
    for i in range(max_iter) :
        if scoreSolution == 0 :
            #Solution optimale trouvée on peut s'arrêter
            break
            
        NewSolution = voisin(solution, grille) #Nouvelle solution par rapport à la solution actuelle
        NewScoreSolution = evaluation_fitness(NewSolution, grille) #Calcule du score de la nouvelle solution
        
        
        if NewScoreSolution >= scoreSolution :
            #Acceptation si la nouvelle solution à un meilleur score
            solution = NewSolution
            scoreSolution = NewScoreSolution
        else :
            #Acceptation de la solution avec une certaine probabilité (même si la solution peut être moins bonne)
            if random.random() < math.exp((NewScoreSolution - scoreSolution) / T_initial):
                solution = NewSolution
                scoreSolution = NewScoreSolution
        
        T_initial *= refroidissement #Refroidissement
    
    print("Score obtenu de la solution : ", scoreSolution)
    return solution
        

def generation_grille(filepath):
    """
    Génère une grille à partir d'un fichier txt

    Args:
        filepath (str): Chemin vers le fichier

    Returns:
        (list[list[int]]): grille de jeu
    """
    
    #Lecture du fichier
    with open(filepath) as fichier:
        lignes = fichier.read().splitlines()

    taille_x, taille_y = map(int, lignes[0].split()) #Récupération des dimensions de la grille (1ère ligne du fichier)
    
    #Création de la grille avec les dimensions récupérer
    grille = np.zeros((taille_x, taille_y))

    for ligne in lignes[1:]:  # on saute la première ligne (dimensions)
        x, y, valeur = map(int, ligne.split())
        grille[x][y] = valeur #Ajout de la valeur à la position (x, y)

    return grille


def afficher_solution(grille, solution):
    """
    Affiche la solution trouvée de la grille Shikaku avec matplotlib

    Args:
        grille (list[list[int]]): Grille de jeu
        solution (dictionnaire): Dictionnaire de la solution de la forme {(x, y) : ((x1, y1), (x2, y2))} avec (x, y) position de la valeur dans la grille,
                        ((x1, y1), (x2, y2)) les rectangles choisis
    """
    
    fig, ax = plt.subplots()
    #Dimension de la grille
    largeur = grille[0].size
    hauteur = grille[1].size
   
    ax.set_aspect('equal')
    #Définition des ticks pour dessiner la grille
    ax.set_xticks(range(largeur + 1))
    ax.set_yticks(range(hauteur + 1))
    ax.grid(True) 

    # Palette de couleurs
    couleurs = cm.get_cmap('tab20', len(solution))
    
    for i, ((x, y), ((x1, y1), (x2, y2))) in enumerate(solution.items()):
        width = y2 - y1 + 1 #Largeur du rectangle
        height = x2 - x1 + 1 #Hauteur du rectangle
        
        color = couleurs(i)  # Couleur unique pour chaque rectangle

        #Création du rectangle
        rect = patches.Rectangle((y1, x1), width, height, linewidth=1,
                                 edgecolor='black', facecolor=color, alpha=0.7)
        ax.add_patch(rect)

        # Affiche le nombre au centre de sa cellule
        ax.text(y + 0.5, x + 0.5, str(int(grille[x][y])), va='center',
                ha='center', fontsize=10, color='black')

    ax.set_title("Solution Shikaku trouvée") #Titre de la figure
    plt.show() #Affichage de la figure                        
    
#Charge la grille
grille = generation_grille("grids/medium/250513")


#Vérifie que la grille est bien chargée
if grille is not None:
    #Lancement du recuit simulé
    solution = RecuitSimuleShikaku(grille, 10, 0.999, 10000)
    afficher_solution(grille, solution)