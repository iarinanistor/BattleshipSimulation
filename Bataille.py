from Bateau import Bateau
from Grille import Grille

class Bataille:
    def __init__(self,nb_bateaux):
        b = Bateau.generation_aleatoire_bateau(nb_bateaux)
        self.grille = Grille()
        self.grille.bateaux = b
        self.grille.generer_grille()

    def joue(self,position):

    def victoire(self):

    def reset(self):

