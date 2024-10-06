from Bateau import Bateau
from Grille import Grille
import Combinatoire
from Joueur import Joueur
from Bataille import Bataille
import numpy as np
import random

class Bayes:
    
    def __init__(self,g,ps):
        #uniforme par defaut
        self.proba = np.full((g.TAILLE,g.TAILLE),1/(g.TAILLE**2),dtype=float)
        self.grille = g
        self.ps = ps

    def changer_proba_centre(self):
        x, y = np.meshgrid(np.linspace(-1, 1, g.TAILLE), np.linspace(-1, 1, g.TAILLE))
        d = np.sqrt(x*x + y*y) 
        sigma, miu = 0.5, 0.0
        self.proba = np.exp(-( (d - miu)**2 / ( 2.0 * sigma**2 ) ))
        self.proba /= self.proba.sum()

    def changer_proba_bords(self):
        self.proba = np.zeros((self.grille.TAILLE,self.grille.TAILLE))
        self.proba[0, :] = 1  # bord haut
        self.proba[-1, :] = 1  # bord bas
        self.proba[:, 0] = 1  # bord gauche
        self.proba[:, -1] = 1  # bord droit

        # Normaliser la distribution pour que la somme soit 1
        self.proba /= self.proba.sum()

    def mise_a_jour_pi(self,x,y):
        pi_ancienne = self.proba[x,y]
        self.proba[x,y] = (1-self.ps)*pi_ancienne / (1 - self.ps*pi_ancienne)

        pi_diff = 1 - pi_ancienne*self.ps
        for i in range(len(self.proba)):
            for j in range(len(self.proba)):
                if (i,j) != (x,y):
                    self.proba[i,j] /= pi_diff
    
    def recherche_bayes(self,b,max_essais=100):
        for it in range(max_essais):
            k_aux = np.argmax(self.proba)
            k = np.unravel_index(k_aux, self.proba.shape)
            x,y = k

            if self.grille.getBateau(x,y) == b:
                detection = random.random() < self.ps
                print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
                if detection:
                    print(f"L'objet a été détecté dans la case ({x}, {y}) après {it + 1} itérations.")
                    return (x, y), it+1
            else:
                detection = False
                print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
            self.mise_a_jour_pi(x,y)


        print("L'objet n'a pas été trouvé après le nombre maximal d'itérations.")
        return (-1,-1),101

if __name__ == "__main__" :   
    g = Grille()
    torp = Bateau('TORPILLEUR')
    print("#####")
    print(torp.id)
    g.ajoute_bateau(torp)
    g.placer_bateau(torp,(4,6),1)
    b = Bayes(g,0.6)
    b.recherche_bayes(torp)
    b = Bayes(g,0.9,False)
    b.recherche_bayes(torp)

            






