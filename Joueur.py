from Grille import Grille
from Bateau import Bateau
from Bataille import Bataille
import Combinatoire
import random
import matplotlib.pyplot as plt
import numpy as np

class Joueur:
    def __init__(self,nb_bateaux):
        self.bataille = Bataille(nb_bateaux)


    ###FONCTIONS VERSION ALEATOIRE
    
    def version_aleatoire(self):
        tirs = set()
        coups = 0
        while not self.bataille.victoire():
            while True:
                (x,y) = (random.randint(0,9),random.randint(0,9))
                if (x,y) not in tirs: #pour pas compter les tirs donnes dans la meme position
                    self.bataille.tirer((x,y))
                    coups += 1
                    tirs.add((x,y))
                    break
        return coups
    
    
    def simulation_version_aleatoire(self,nb_essais,liste_bateaux = []):
        nb_coups = 0
        res = []
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb = self.version_aleatoire()
            nb_coups += nb
            res.append(nb)
            self.bataille.reset(True)
        return nb_coups,res
    
    def graphe_distribution_aleatoire(self,nb_essais,liste_bateaux=[]):
        nb_coups, res = self.simulation_version_aleatoire(nb_essais,liste_bateaux)
        plt.hist(res, bins=30, density=True, alpha=0.75, color='blue')
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité')
        plt.title('Distribution du nombre de coups pour terminer une partie')
        plt.grid(True)
        plt.show()
    
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
        return nb_coups,res
    
    def graphe_distribution_heuristique(self,nb_essais,liste_bateaux=[]):
        nb_coups, res = self.simulation_version_heuristique(nb_essais,liste_bateaux)
        plt.hist(res, bins=30, density=True, alpha=0.75, color='blue')
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité')
        plt.title('Distribution du nombre de coups pour terminer une partie')
        plt.grid(True)
        plt.show()

    ###FONCTIONS VERSION probabiliste simplifiée
    
    def ajouter_probabilite(self,grille_prob, bateau, x, y):
        grille_zero = Grille()
        nb = Combinatoire.nb_configurations_possibles_bateau(bateau,grille_zero)
        longueur = bateau.longueur
        if grille_zero.peut_placer(bateau,(x,y),2):
                grille_prob.ajouter_placement(x,y,2,longueur,1/nb)
        if grille_zero.peut_placer(bateau,(x,y),3):
                grille_prob.ajouter_placement(x,y,3,longueur,1/nb)
    
    def probabilite_bateau(self,grille_prob, bateau):
            for x in range(grille_prob.TAILLE):
                for y in range(grille_prob.TAILLE):
                    self.ajouter_probabilite(grille_prob,bateau,x,y)
    
    
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
        
            bateau_touche = self.bataille.grille.getBateau(x, y)
        
            if bateau_touche is not None and bateau_touche.est_coule():
                print(f"Bateau coulé à la position: ({x}, {y})")
    
        return coups
        
    def simulation_version_proba_simplifie(self,nb_essais,liste_bateaux = []):
        nb_coups = 0
        res = []
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb = self.version_proba_simplifie()
            res.append(nb)
            nb_coups += nb
            self.bataille.reset(True)
        return nb_coups,res

###FONCTIONS VERSION MONTE-CARLO
    def verifier_contraintes(self,cases_touches):
        g = self.bataille.grille
        for case in cases_touches:
            if g.grille[case[0],case[1]] == 0: #si une case touche n'est pas ocupe par une bateau
                return False
    
    def peut_placer_bateau_montecarlo(self,bateau,x,y,direction,cases_touches,g):
        v1 = g.peut_placer(bateau,(x,y),direction)
        bateau_len = bateau.longueur

        if direction == 1 : #SUD
            if cases_touches and not any((x-i, y) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 2 : #NORD
            if cases_touches and not any((x+i, y) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 3 : #VEST
            if cases_touches and not any((x, y+i) in cases_touches for i in range(bateau_len)):
                return False
        elif direction == 4 : #EST
            if cases_touches and not any((x, y-i) in cases_touches for i in range(bateau_len)):
                return False
        return v1
    
    def placements_possibles(self,bateau,grille,cases_touches):
        places = []
        for x in range(grille.TAILLE):
            for y in range(grille.TAILLE):
                for dir in range(1,5):
                    if self.peut_placer_bateau_montecarlo(bateau,x,y,dir,cases_touches,grille):
                        places.append((x,y,dir))
        random.shuffle(places) #shuffle pour choisir aleatoirement
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
            nouveau_g.placer_bateau(bateau,position,direction)
            nouvelle_liste_bateaux = [b for b in bateaux_restants if b != bateau]

            resultat = self.generer_grille_aleatoire(nouvelle_liste_bateaux, nouveau_g, cases_touches)
            if resultat is not None:
                return resultat

        return None
    
    def creation_grille_probabilites(self,cases_touches,nb_simulations):
        """
        Effectue des simulations Monte-Carlo pour estimer la probabilité de présence d'un bateau sur chaque case.
        """
        probabilites = np.zeros((self.bataille.grille.TAILLE,self.bataille.grille.TAILLE))
        bateaux_restants = self.bataille.grille.bateaux
        
        for _ in range(nb_simulations):
            grille_vide = Grille()
            grille_simulee = self.generer_grille_aleatoire(bateaux_restants, grille_vide, cases_touches)
            
            if grille_simulee is not None:
                # Incrémenter la probabilité de chaque case qui contient un bateau
                grille_probabilites += (grille_simulee.grille > 0).astype(int)
        
        # Moyenne sur le nombre de simulations
        probabilites /= self.nb_simulations
        return probabilites
    
    def version_montecarlo(self,nb_sim):
        tirs = set()
        coups = 0
        
        while not self.bataille.victoire():
            grille_probabilites = self.creation_grille_probabilites(tirs,nb_sim)
            x, y = np.unravel_index(np.argmax(grille_probabilites), grille_probabilites.shape)
            
            if (x, y) not in tirs:
                self.bataille.tirer((x, y))
                tirs.add((x, y))
                coups += 1

                # Mise à jour si un bateau est coulé
                bateau_touche = self.bataille.grille.getBateau(x, y)
                if bateau_touche is not None and bateau_touche.est_coule():
                    print(f"Bateau coulé à la position: ({x}, {y})")
        
        return coups







j = Joueur(5)
j.bataille.grille.affiche_graph()
results = j.simulation_version_aleatoire(100)
print(results)
j.bataille.grille.affiche_graph()
nb_essais = 1000

res2 = j.simulation_version_heuristique(100)
print(res2)
j.bataille.grille.affiche_graph()

j.graphe_distribution_heuristique(100)

cpt = j.version_proba_simplifie()
print(cpt)
j.bataille.reset(True)
j.bataille.grille.affiche_graph()
cpt2 = j.version_proba_simplifie()
print(cpt2)

# res3 = j.simulation_version_proba_simplifie(100)
# print(res3)

cases_touches = [(2, 3), (4, 5)]
nb_simulations = 1000

