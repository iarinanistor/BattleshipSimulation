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
        """
        Initialise l'instance de la classe Bayes.

        Args:
            g (Grille): La grille dans laquelle les bateaux sont placés.
            ps (float): Probabilité de succès de la détection.
        """
        self.proba = np.full((g.TAILLE,g.TAILLE),1/(g.TAILLE**2),dtype=float)
        self.grille = g
        self.ps = ps

    @staticmethod
    def normaliser(data):
        """
        Normalise un tableau de données pour que la somme soit égale à 1.

        Args:
            data (np.ndarray): Les données à normaliser.

        Returns:
            np.ndarray: Les données normalisées.
        """

        datanormalise = data/np.sum(data)
        return datanormalise
    
    def changer_proba_uniforme(self):
        """
        Réinitialise les probabilités à une distribution uniforme.
        """

        g = self.grille
        self.proba = np.full((g.TAILLE,g.TAILLE),1/(g.TAILLE**2),dtype=float)
        self.proba = Bayes.normaliser(self.proba)

    def changer_proba_centre(self):
        """
        Modifie les probabilités pour favoriser le centre de la grille.
        """

        g = self.grille
        x, y = np.meshgrid(np.linspace(-1, 1, g.TAILLE), np.linspace(-1, 1, g.TAILLE))
        d = np.sqrt(x*x + y*y) 
        proba = 1 - d/np.max(d) # Plus proche du centre, plus de probabilité
    # S'assurer que toutes les valeurs sont non-négatives
        proba[proba < 0] = 0
        self.proba = proba
        self.proba = Bayes.normaliser(self.proba) # Normaliser les probabilités
        #print(self.proba)
        #print(self.proba.sum())

    def changer_proba_bords(self):
        """
        Modifie les probabilités pour favoriser les bords de la grille.
        """

        g = self.grille
        x, y = np.meshgrid(np.linspace(-1, 1, g.TAILLE), np.linspace(-1, 1, g.TAILLE))
        d = np.sqrt(x*x + y*y) 
        proba = d/np.max(d)  # Plus proche des bords, plus de probabilité
    # S'assurer que toutes les valeurs sont non-négatives
        proba[proba < 0] = 0
        self.proba = proba
        self.proba = Bayes.normaliser(self.proba)  # Normaliser les probabilités
        #print(self.proba)
        print(self.proba.sum())

    def mise_a_jour_pi(self,x,y):
        """
        Met à jour les probabilités après avoir sondé une case.

        Args:
            x (int): Coordonnée x de la case sondée.
            y (int): Coordonnée y de la case sondée.
        """

        pi_ancienne = self.proba[x,y]
        self.proba[x,y] = (1-self.ps)*pi_ancienne / (1 - self.ps*pi_ancienne) # Mise à jour de la probabilité

        pi_diff = 1 - pi_ancienne*self.ps
        for i in range(len(self.proba)):
            for j in range(len(self.proba)):
                if (i,j) != (x,y):
                    self.proba[i,j] /= pi_diff  # Mise à jour des autres probabilités
    
    def recherche_bayes(self,b,max_essais=500):
        """
        Recherche un objet dans la grille en utilisant une approche bayésienne.

        Args:
            b (Bateau): Bateau à rechercher.
            max_essais (int): Nombre maximum d'essais pour la recherche.

        Returns:
            tuple: Position trouvée et nombre d'itérations, ou (-1, -1) si non trouvé.
        """

        
        for it in range(max_essais):
            #print(self.proba)
            k_aux = np.argmax(self.proba)  # Trouve l'indice avec la probabilité maximale
            k = np.unravel_index(k_aux, self.proba.shape)
            x,y = k

            if self.grille.getBateau(x,y) == b:
                detection = random.random() < self.ps   # Détection selon la probabilité
                #print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
                if detection:
                    print(f"L'objet a été détecté dans la case ({x}, {y}) après {it + 1} itérations.")
                    return (x, y), it+1
            else:
                detection = False
                #print(f"Iteration {it + 1}: Case sondée ({x}, {y}), Detection: {detection}")
            self.mise_a_jour_pi(x,y)   # Met à jour les probabilités après la recherche


        print("L'objet n'a pas été trouvé après le nombre maximal d'itérations.")
        return (-1,-1),101  # Retourne (-1, -1) si non trouvé

if __name__ == "__main__" :   
    g = Grille()
    b1 = Bateau('TORPILLEUR',(9,1),3)
    b2 = Bateau('TORPILLEUR',(1,5),4)
    b3 = Bateau('PORTE_AVIONS',(4,9),1)
    b4 = Bateau('CROISEUR',(2,2),2)
    b5 = Bateau('SOUS_MARIN',(9,4),3)
    l = [b1,b2,b3,b4,b5]

    # b1 = Bateau('CROISEUR' ,(3, 3), 2)
    # b2 = Bateau('SOUS_MARIN', (4, 2), 4)
    # b3 = Bateau('CROISEUR', (5, 7) ,2)
    # b4 = Bateau('CONTRE_TORPILLEURS' ,(5, 9), 1)
    # b5 = Bateau('CROISEUR' ,(9, 9), 1)
    # b6 = Bateau('TORPILLEUR' ,(8, 6), 1)
    # b7 = Bateau('TORPILLEUR', (5, 4), 1)
    # b8 = Bateau('CONTRE_TORPILLEURS', (2, 3), 4)
    # b9 = Bateau('SOUS_MARIN', (1, 4) ,4)
    # b10 = Bateau('PORTE_AVIONS', (4, 6), 1)
    # b11 = Bateau('CONTRE_TORPILLEURS', (5, 2), 4)
    # b12 = Bateau('TORPILLEUR', (0, 7), 2)
    # b13 = Bateau('CONTRE_TORPILLEURS', (8, 4), 1)
    # b14 = Bateau('CROISEUR', (6, 5), 1)
    # b15 = Bateau('TORPILLEUR' ,(2, 8), 3)
    # l= [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15]

    # b1 = Bateau('CROISEUR' ,(3, 3), 2)
    # b3 = Bateau('TORPILLEUR', (5, 4), 1)
    # b4 = Bateau('TORPILLEUR', (4, 7), 2)
    # b5 = Bateau('PORTE_AVIONS',(7,5),1)
    # l = [b1,b3,b4,b5]

    g.bateaux = l
    g.grille_ancienne()
    g.affiche_graph()
    ps = 0.8
    b = Bayes(g,ps)
    b2 = Bayes(g,ps)
    b2.changer_proba_bords()
    b3 = Bayes(g,ps)
    b3.changer_proba_centre()
    elem = random.choice(l)
    b.recherche_bayes(elem)
    b2.recherche_bayes(elem)
    b3.recherche_bayes(elem)


            






