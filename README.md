## Solver-shikaku

Projet Universitaire de l'université du Havre pour la matière d'intelligence artificielle (IA). Le but de ce projet est de mettre en oeuvre un solver de grille de shikaku utilisant le recuit simulé.

## Développement

L'algorithme du recuit simulé fonctionnera ici de la manière suivante :
1. Modélisation de la grille avec ses valeurs(taille fourni dans les fichiers de tests à la 1ère ligne et les valeurs sont fourni au ligne suivante avec la position et sa valeur)
2. Lancement du recuit simulé en calculant tout les rectangles possibles et le choix du rectangle sera aléatoire
3. Calcul du score de fitness -> solution
4. Création d'une nouvelle solution en modifiant la solutions actuelles
5. Re calcul du score de fitness de la nouvelle solution pour obtenir un nouveau score
6. En cas de meilleure score on accepte la solution
7. En cas de score moins bon on "accepte" une mauvaise solution selon une petite chance afin d'éviter l'optimal local

## Installation

Le solver-shikaku utilise les bibliothèques `numpy` et `matplotlib`.

1.  Si ils ne sont pas installés sur votre machine veuillez tout d'abord les installez :
    ```bash
    pip install numpy matplotlib
    ```
2.  Lancez le script :
    ```bash
    python Shikaku.py
    ```
3.  Le script charge une grille (par ex dans le code actuelle: `grids/medium/250513`) et affiche la solution trouvée. Il est bien sur possible de changer la grille et de prendre une nouveller ou d'en créer une soi-même afin de la tester il suffit de respecter
4.  la manière dont les fichiers de tests sont créer.

## Exemple de solution ( `grids/medium/250513`)

Voici a quoi devrait ressembler par exemple ici la solution pour la grille **250513** de niveau medium : 

![Solution grille niveau medium](/solutionImage/solution.png)