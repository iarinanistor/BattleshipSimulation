from Grille import Grille
from Bateau import Bateau
from Bataille import Bataille
import Combinatoire
import random
import matplotlib.pyplot as plt
import numpy as np

class Joueur:

    def __init__(self,nb_bateaux):
        '''
        Initialise un joueur avec une partie de bataille navale contenant un certain nombre de bateaux.

        Args:
            nb_bateaux: Nombre de bateaux à placer sur la grille.
        '''
        
        self.bataille = Bataille(nb_bateaux)
        self.bateaux_restants = self.bataille.grille.bateaux  # Utilisé pour Monte-Carlo


    ###FONCTIONS VERSION ALEATOIRE
    
    def version_aleatoire(self):
        '''
        Effectue une partie avec une stratégie aléatoire, c'est-à-dire en tirant au hasard jusqu'à la victoire.

        Returns:
            coups: Nombre de coups nécessaires pour terminer la partie.
        '''

        tirs = set() # Ensemble des tirs déjà effectués
        coups = 0
        while not self.bataille.victoire():
            while True:
                (x,y) = (random.randint(0,9),random.randint(0,9)) 

                if (x,y) not in tirs: # Assure que la même position n'est pas tirée deux fois
                    self.bataille.tirer((x,y))
                    coups += 1
                    tirs.add((x,y)) # Ajoute le tir dans l'ensemble des tirs
                    break

        return coups
    
    
    def simulation_version_aleatoire(self,nb_essais,liste_bateaux = []):
        '''
         Simule plusieurs parties avec une stratégie aléatoire.

        Args:
            nb_essais: Nombre d'essais/simulations à réaliser.
            liste_bateaux: Liste optionnelle de bateaux pour fixer les bateaux dans la simulation.

        Returns:
            nb_coups: Nombre total de coups dans toutes les simulations.
            res: Liste contenant le nombre de coups pour chaque simulation.
        '''
        
        nb_coups = 0
        res = []

        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):

            nb = self.version_aleatoire()
            nb_coups += nb
            res.append(nb)
            self.bataille.reset(True)
            
        return nb_coups/nb_essais,res
    
    def graphe_distribution_aleatoire(self,nb_essais,liste_bateaux=[]):
        moyenne, res = self.simulation_version_aleatoire(nb_essais,liste_bateaux)
        print(f"Nb moyen de coups pour avoir une victoire dans la version aleatoire : {moyenne} \n")
        print(f"Les {nb_essais} resulats de nombre de coups qu'on a obtenu: {res}")
        plt.hist(res, bins=30, density=True, alpha=0.75, color='blue')
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité')
        plt.title('Distribution du nombre de coups pour terminer une partie')
        plt.grid(True)
        plt.show()

    # res = self.simulation_version_aleatoire(nb_essais,liste_bateaux)
    
    ###FONCTIONS VERSION HEURISTIQUE

    def ajouter_voisins(self,x, y, tirs_a_venir):
        """Ajoute les cases voisines à vérifier autour de la case (x, y) si elles n'ont pas été tirées."""
        voisins = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for voisin in voisins:
         # Ajouter uniquement les voisins qui n'ont pas encore été tirés
            tirs_a_venir.add(voisin)

    def version_heuristique(self):
        tirs = set()
        tirs_a_venir = set()
        coups = 0
        while not self.bataille.victoire():
            while True:
                if not tirs_a_venir:
                    x,y = random.randint(0, 9), random.randint(0, 9)
                    if (x, y) not in tirs:
                        self.bataille.tirer((x, y))  # Tire sur la case
                        tirs.add((x, y))  # Ajoute le tir à la liste des tirs effectués
                        coups += 1
                        if self.bataille.grille.getBateau(x, y) is not None:
                            self.ajouter_voisins(x, y, tirs_a_venir)
                    break
                else:
                    while tirs_a_venir:
                        x, y = tirs_a_venir.pop()
                        if (x, y) not in tirs:
                            self.bataille.tirer((x, y))  # Tire sur la case
                            tirs.add((x, y))  # Ajoute le tir à la liste des tirs effectués
                            coups += 1
                            if self.bataille.grille.getBateau(x, y) is not None:
                                self.ajouter_voisins(x, y, tirs_a_venir)
                    break
        return coups


    
    def simulation_version_heuristique(self,nb_essais,liste_bateaux = []):
        nb_coups = 0
        res = []
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb = self.version_heuristique()
            res.append(nb)
            nb_coups += nb
            self.bataille.reset(True)
        return nb_coups/nb_essais,res
    
    def graphe_distribution_heuristique(self,nb_essais,liste_bateaux=[]):
        moyenne, res = self.simulation_version_heuristique(nb_essais,liste_bateaux)
        print(f"Nb moyen de coups pour avoir une victoire dans la version heuristique : {moyenne} \n")
        print(f"Les {nb_essais} resulats de nombre de coups qu'on a obtenu: {res}")
        plt.hist(res, bins=30, density=True, alpha=0.75, color='blue')
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité')
        plt.title('Distribution du nombre de coups pour terminer une partie')
        plt.grid(True)
        plt.show()

    ###FONCTIONS VERSION probabiliste simplifiée
    
    def ajouter_probabilite(self,grille_prob, bateau, x, y):
        grille_zero = Grille()
        #nb = Combinatoire.nb_configurations_possibles_bateau(bateau,grille_zero)
        longueur = bateau.longueur
        if grille_zero.peut_placer(bateau,(x,y),2):
                grille_prob.ajouter_placement(x,y,2,longueur,1)
        if grille_zero.peut_placer(bateau,(x,y),3):
                grille_prob.ajouter_placement(x,y,3,longueur,1)
    
    def probabilite_bateau(self,grille_prob, bateau):
        for x in range(grille_prob.TAILLE):
            for y in range(grille_prob.TAILLE):
                self.ajouter_probabilite(grille_prob,bateau,x,y)
        grille_prob.grille /= grille_prob.grille.sum()

    
    def creation_grille_proba(self,grille_prob):
        for bateau in self.bataille.grille.bateaux:
            if not bateau.est_coule():
                self.probabilite_bateau(grille_prob,bateau)


    

    def version_proba_simplifie(self):
        tirs = set()  
        coups = 0
        grille_prob = Grille()
    
        while not self.bataille.victoire():
            self.creation_grille_proba(grille_prob)
        
            x, y = np.unravel_index(np.argmax(grille_prob.grille), grille_prob.grille.shape)
        
            while (x, y) in tirs:
                grille_prob.grille[x, y] = 0
                x, y = np.unravel_index(np.argmax(grille_prob.grille), grille_prob.grille.shape)
        
            self.bataille.tirer((x, y))
            tirs.add((x, y))  
            coups += 1
        
            # bateau_touche = self.bataille.grille.getBateau(x, y)
        
            # if bateau_touche is not None and bateau_touche.est_coule():
            #     print(f"Bateau coulé à la position: ({x}, {y})")
        self.bataille.reset(True)
    
        return coups
    
    def simulation_proba_simplifie(self):
        coups = self.version_proba_simplifie()
        return f"Dans la version probabiliste simplifiée on a besoin de {coups} coups."
        
        
    # def simulation_version_proba_simplifie(self,nb_essais,liste_bateaux = []):
    #     nb_coups = 0
    #     res = []
    #     if liste_bateaux != [] :
    #         self.bataille.grille.grille_selecte(liste_bateaux)
        
    #     for _ in range(nb_essais):
    #         nb = self.version_proba_simplifie()
    #         res.append(nb)
    #         nb_coups += nb
    #         self.bataille.reset(True)
    #     return nb_coups,res
    
    

###FONCTIONS VERSION MONTE-CARLO
    def verifier_contraintes(self,cases_touches):
        g = self.bataille.grille
        for case in cases_touches:
            if g.grille[case[0],case[1]] == 0: #si une case touche n'est pas ocupe par une bateau
                return False
        return True
    
    def peut_placer_bateau_montecarlo(self,bateau,x,y,direction,cases_touches_non_occ,g):
        v1 = g.peut_placer(bateau,(x,y),direction)
        if not v1: 
            return False
        bateau_len = bateau.longueur

        if direction == 1 : #SUD
            if cases_touches_non_occ and not any((x-i, y) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 2 : #NORD
            if cases_touches_non_occ and not any((x+i, y) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 3 : #VEST
            if cases_touches_non_occ and not any((x, y+i) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 4 : #EST
            if cases_touches_non_occ and not any((x, y-i) in cases_touches for i in range(bateau_len)):
                return False
        return True
    
    def placements_possibles(self,bateau,grille,cases_touches_non_occ):
        places = set()
        for x in range(grille.TAILLE):
            for y in range(grille.TAILLE):
                for dir in range(1,5):
                    if self.peut_placer_bateau_montecarlo(bateau,x,y,dir,cases_touches_non_occ,grille):
                        places.add((x,y,dir)) 
        return places
    
    def generer_grille_aleatoire(self, bateaux_restants, grille, cases_touches):
        """
        Génère une grille aléatoire en plaçant les bateaux restants tout en respectant les contraintes (cases touchées, bateaux coulés).
        """
        if not bateaux_restants:
            # Si tous les bateaux sont placés, on vérifie les contraintes
            if self.verifier_contraintes(cases_touches):
                return grille
            else:
                return None

        bateau = random.choice(bateaux_restants)
        placements_pos= self.placements_possibles(bateau, grille,cases_touches)

        for placement in placements_pos:
            nouveau_g = Grille()
            nouveau_g.grille = np.copy(grille.grille)

            position = (placement[0],placement[1])
            direction = placement[2]

            present = False
            if position in cases_touches:
                present = True
                cases_touches.remove(position)

            nouveau_g.placer_bateau(bateau,position,direction)
            nouvelle_liste_bateaux = [b for b in bateaux_restants if b != bateau]

            resultat = self.generer_grille_aleatoire(nouvelle_liste_bateaux, nouveau_g, cases_touches)
            if present:
                cases_touches.add(position)
            if resultat is not None:
                return resultat

        return None
    
    def creation_grille_probabilites(self,cases_touches,nb_simulations):
        """
        Effectue des simulations Monte-Carlo pour estimer la probabilité de présence d'un bateau sur chaque case.
        """
        probabilites = np.zeros((self.bataille.grille.TAILLE,self.bataille.grille.TAILLE))
        bateaux_restants = self.bateaux_restants
        
        for _ in range(nb_simulations):
            grille_vide = Grille()
            grille_simulee = self.generer_grille_aleatoire(bateaux_restants, grille_vide, cases_touches)
            
            if grille_simulee is not None:
                # Incrémenter la probabilité de chaque case qui contient un bateau
                for x in range(self.bataille.grille.TAILLE):
                    for y in range(self.bataille.grille.TAILLE):
                        if grille_simulee.grille[x,y] != 0:
                            probabilites[x,y] +=1
        probabilites /= nb_simulations
        # Moyenne sur le nombre de simulations
        total = probabilites.sum()
        if total > 0:
            probabilites /= total
        else:
            print("Warning: total probability is zero, skipping normalization.")
        return probabilites
        
    
    def version_montecarlo(self,nb_sim):
        tirs = set()
        coups = 0
        
        while not self.bataille.victoire():
            print(coups)
            grille_probabilites = self.creation_grille_probabilites(tirs,nb_sim)
            print(grille_probabilites)
            x, y = np.unravel_index(np.argmax(grille_probabilites), grille_probabilites.shape)
            
            if (x, y) not in tirs:
                self.bataille.tirer((x, y))
                tirs.add((x, y))
                coups += 1

                # Mise à jour si un bateau est coulé
                bateau_touche = self.bataille.grille.getBateau(x, y)
                if bateau_touche is not None and bateau_touche.est_coule():
                    self.bateaux_restants.remove(bateau_touche)
                    print(f"Bateau coulé à la position: ({x}, {y})")
        self.bateaux_restants = self.bataille.grille.grille
        
        return coups





if __name__=='__main__':

    j = Joueur(5)
    # j.bataille.grille.affiche_graph()
    # results = j.simulation_version_aleatoire(100)
    # print(results)
    # j.bataille.grille.affiche_graph()
    # nb_essais = 1000
    # g = Grille()
    # j.creation_grille_proba(g)
    # print(g.grille)
    # print(g.grille.sum())
    # print("##########atentie monte-carlo")
    # cases_touches = set()
    # cases_touches.add((2,2))
    # cases_touches.add((2,2))
    # cases_touches.add((4,4))
    # print(j.creation_grille_probabilites(cases_touches,10))
    # print(j.creation_grille_probabilites(set(),10))
    # print(j.version_montecarlo(10))



    # res2 = j.simulation_version_heuristique(100)
    # print(res2)
    # j.bataille.grille.affiche_graph()

    # j.graphe_distribution_heuristique(100)
    # j.graphe_distribution_aleatoire(100)

    cpt= j.version_proba_simplifie()
    j.bataille.grille.affiche_graph()
    print(cpt)
    # j.bataille.reset(True)
    # j.bataille.grille.affiche_graph()
    # cpt2 = j.version_proba_simplifie()
    # print(cpt2)

    # # res3 = j.simulation_version_proba_simplifie(100)
    # # print(res3)

    # cases_touches = [(2, 3), (4, 5)]
    # nb_simulations = 1000

