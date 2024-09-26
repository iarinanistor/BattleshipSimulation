from Grille import Grille
from Bateau import Bateau
from Bataille import Bataille
import random

class Joueur:
    def __init__(self,nb_bateaux):
        self.bataille = Bataille(nb_bateaux)
    
    def version_aleatoire(self):
        tirs = set()
        coups = 0
        while not self.bataille.victoire():
            while True:
                (x,y) = (random.randint(0,9),random.randint(0,9))
                if (x,y) not in tirs: #pour pas compter les tirs donnes dans la meme position
                    self.bataille.tirer((x,y))
                    coups += 1
                    break
        return coups


j = Joueur(5)
j.bataille.grille.affiche_graph()
print(j.version_aleatoire())
j.bataille.grille.affiche_graph()