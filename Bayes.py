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

    def normaliser(data):
        datanormalise = data/np.sum(data)
        return datanormalise
    
    def changer_proba_uniforme(self):
        g = self.grille
        self.proba = np.full((g.TAILLE,g.TAILLE),1/(g.TAILLE**2),dtype=float)
        self.proba = Bayes.normaliser(self.proba)

    def changer_proba_centre(self):
        g = self.grille
        x, y = np.meshgrid(np.linspace(-1, 1, g.TAILLE), np.linspace(-1, 1, g.TAILLE))
        d = np.sqrt(x*x + y*y) 
        #sigma, miu = 0.5, 0.0
        proba = 1 - d/np.max(d)
    # S'assurer que toutes les valeurs sont non-négatives
        proba[proba < 0] = 0
        self.proba = proba
        self.proba = Bayes.normaliser(self.proba)
        print(self.proba)
        print(self.proba.sum())

    def changer_proba_bords(self):
        g = self.grille
        x, y = np.meshgrid(np.linspace(-1, 1, g.TAILLE), np.linspace(-1, 1, g.TAILLE))
        d = np.sqrt(x*x + y*y) 
        proba = d/np.max(d)
    # S'assurer que toutes les valeurs sont non-négatives
        proba[proba < 0] = 0
        self.proba = proba
        self.proba = Bayes.normaliser(self.proba)
        print(self.proba)
        print(self.proba.sum())

    def mise_a_jour_pi(self,x,y):
        pi_ancienne = self.proba[x,y]
        self.proba[x,y] = (1-self.ps)*pi_ancienne / (1 - self.ps*pi_ancienne)

        pi_diff = 1 - pi_ancienne*self.ps
        for i in range(len(self.proba)):
            for j in range(len(self.proba)):
                if (i,j) != (x,y):
                    self.proba[i,j] /= pi_diff
    
    def recherche_bayes(self,b,max_essais=200):
        
        for it in range(max_essais):
            #print(self.proba)
            k_aux = np.argmax(self.proba)
            k = np.unravel_index(k_aux, self.proba.shape)
            x,y = k

            if self.grille.getBateau(x,y) == b:
                detection = random.random() < self.ps
                #print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
                if detection:
                    print(f"L'objet a été détecté dans la case ({x}, {y}) après {it + 1} itérations.")
                    return (x, y), it+1
            else:
                detection = False
                #print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
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
    b.changer_proba_centre()
    b.recherche_bayes(torp)
    b.changer_proba_bords()
    b.recherche_bayes(torp)

            






