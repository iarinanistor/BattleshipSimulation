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

    def esperance_theoretique(self):
        '''
        Calcule l'espérance théorique du nombre de coups nécessaires pour gagner la partie.

        Returns:
            float: L'espérance théorique.
        '''
        k = self.bataille.grille.longueur_bateaux()
        nb_bateaux = len(self.bataille.grille.bateaux)
        n = self.bataille.grille.TAILLE**2
        s = 0
        for i in range(nb_bateaux):
            s += (n-i)/(k-i)
        return s




    ###FONCTIONS VERSION ALEATOIRE
        
    
    
    def version_aleatoire(self):
        '''
        Effectue une partie avec une stratégie aléatoire, c'est-à-dire en tirant au hasard jusqu'à la victoire.

        Returns:
            coups: Nombre de coups nécessaires pour terminer la partie.
        '''

        tirs = set() # Ensemble des tirs déjà effectués
        coups = 0
        while not self.bataille.victoire(): # Boucle jusqu'à la victoire
            while True:
                (x,y) = (random.randint(0,9),random.randint(0,9))  # Tir aléatoire

                if (x,y) not in tirs: # Assure que la même position n'est pas tirée deux fois
                    self.bataille.tirer((x,y)) # Tire sur la case
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

            nb = self.version_aleatoire()  # Exécute une partie aléatoire
            nb_coups += nb
            res.append(nb)
            self.bataille.reset(True)   # Réinitialise la bataille
            
            
        return nb_coups/nb_essais,res  # Retourne la moyenne et les résultats
    

    def graphe_distribution_aleatoire(self, nb_essais, liste_bateaux=[]):
        moyenne, res = self.simulation_version_aleatoire(nb_essais, liste_bateaux)
        median = np.median(res)  # Calcul de la médiane
        ecart_type = np.std(res)  # Calcul de l'écart-type
        
        print(f"Nb moyen de coups pour avoir une victoire dans la version aleatoire : {moyenne} \n")
        print(f"Les {nb_essais} résultats de nombre de coups qu'on a obtenu: {res}")

        # calculer l'histogramme
        counts, bins = np.histogram(res, bins=30, density=True)  # density=True normalise l'histogramme

        # normaliser - sum=1
        total_counts = np.sum(counts)
        normalized_counts = counts / total_counts if total_counts > 0 else counts  # Eviter la division par zéro

        # plot
        plt.bar(bins[:-1], normalized_counts, width=np.diff(bins), alpha=0.75, color='blue', edgecolor='black')

        # ajouter des labels
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité (Normalisée)')
        plt.title('Distribution du nombre de coups pour terminer une partie - ALEATOIRE')
        plt.grid(True)
        plt.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Médiane = {median:.2f}')

        # supraface pour ecart - type
        plt.axvspan(moyenne - ecart_type, moyenne + ecart_type, color='orange', alpha=0.3, label=f'1 écart-type')

        # afficher la moyenne et la mediane
        plt.text(moyenne + 0.1, max(normalized_counts), f'Moyenne: {moyenne:.2f}', color='red')
        plt.text(median + 0.1, max(normalized_counts) - 0.02, f'Médiane: {median:.2f}', color='green')  # Ajuster la position pour qu'elle ne soit pas cachée par la barre

        # afficher les probas
        for count, x in zip(normalized_counts, bins[:-1]):  
            if count > 0:  
                plt.text(x + (bins[1] - bins[0]) / 2, count, f'{count:.2f}', ha='center', va='bottom')

        plt.legend()
        plt.show()


    # res = self.simulation_version_aleatoire(nb_essais,liste_bateaux)
    
    ###FONCTIONS VERSION HEURISTIQUE

    def ajouter_voisins(self,x, y, tirs_a_venir,taille):
        """Ajoute les cases voisines à vérifier autour de la case (x, y) si elles n'ont pas été tirées.

        Args:
            x (int): Coordonnée x de la case.
            y (int): Coordonnée y de la case.
            tirs_a_venir (set): Ensemble des cases à tirer.
            taille (int): Taille de la grille.
        """
        voisins = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
        for voisin in voisins:
         # Ajouter uniquement les voisins qui n'ont pas encore été tirés
            (i,j) = voisin
            if i in range(taille) and j in range(taille):
                tirs_a_venir.add(voisin)

    def version_heuristique(self):
        '''
        Effectue une partie avec une stratégie heuristique, en priorisant les tirs sur les cases voisines.

        Returns:
            int: Nombre de coups nécessaires pour terminer la partie.
        '''
        tirs = set()
        tirs_a_venir = set()
        coups = 0
        while not self.bataille.victoire():  # Boucle jusqu'à la victoire
            while True:
                if not tirs_a_venir:
                    x,y = random.randint(0, 9), random.randint(0, 9)  # Si aucune case à venir, tirer aléatoirement
                    if (x, y) not in tirs:
                        #print(f"{x} {y}\t")
                        self.bataille.tirer((x, y))  # Tire sur la case
                        tirs.add((x, y))  # Ajoute le tir à la liste des tirs effectués
                        coups += 1
                        if self.bataille.grille.getBateau(x, y) is not None:  # Si un bateau est touché
                            self.ajouter_voisins(x, y, tirs_a_venir,self.bataille.grille.TAILLE)  # Ajoute les voisins à vérifier
                    break
                else:
                    while tirs_a_venir:
                        x, y = tirs_a_venir.pop()
                        if (x, y) not in tirs:
                            #print(f"{x} {y}\t")
                            self.bataille.tirer((x, y))  # Tire sur la case
                            tirs.add((x, y))  # Ajoute le tir à la liste des tirs effectués
                            coups += 1
                            if self.bataille.grille.getBateau(x, y) is not None:
                                self.ajouter_voisins(x, y, tirs_a_venir,self.bataille.grille.TAILLE)
                    break
        return coups
    



    
    def simulation_version_heuristique(self,nb_essais,liste_bateaux = []):
        '''
        Simule plusieurs parties avec une stratégie heuristique.

        Args:
            nb_essais (int): Nombre d'essais/simulations à réaliser.
            liste_bateaux (list): Liste optionnelle de bateaux pour fixer les bateaux dans la simulation.

        Returns:
            tuple: Nombre moyen de coups dans toutes les simulations et une liste de coups pour chaque simulation.
        '''
        nb_coups = 0
        res = []
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb = self.version_heuristique()  # Exécute une partie heuristique
            res.append(nb)
            nb_coups += nb
            self.bataille.reset(True)  # Réinitialise la bataille
        return nb_coups/nb_essais,res
    


    def graphe_distribution_heuristique(self, nb_essais, liste_bateaux=[]):
        '''
        Trace la distribution du nombre de coups pour terminer une partie avec la version heuristique.

        Args:
            nb_essais (int): Nombre d'essais/simulations à réaliser.
            liste_bateaux (list): Liste optionnelle de bateaux pour fixer les bateaux dans la simulation.
        '''
        moyenne, res = self.simulation_version_heuristique(nb_essais, liste_bateaux)
        median = np.median(res) # Calcul de la médiane
        ecart_type = np.std(res) # Calcul de l'écart-type
        
        print(f"Nb moyen de coups pour avoir une victoire dans la version heuristique : {moyenne} \n")
        print(f"Les {nb_essais} résultats de nombre de coups qu'on a obtenu: {res}")

        # Calcul de l'histogramme
        counts, bins = np.histogram(res, bins=30, density=True)  # density=True normalise l'histogramme

        # Normalisation - somme = 1
        total_counts = np.sum(counts)
        normalized_counts = counts / total_counts if total_counts > 0 else counts  # Eviter la division par zéro

        # Traçage de l'histogramme
        plt.bar(bins[:-1], normalized_counts, width=np.diff(bins), alpha=0.75, color='blue', edgecolor='black')

        # Ajouter des labels
        plt.xlabel('Nombre de coups')
        plt.ylabel('Densité (Normalisée)')
        plt.title('Distribution du nombre de coups pour terminer une partie - HEURISTIQUE')
        plt.grid(True)
        plt.axvline(median, color='green', linestyle='dashed', linewidth=2, label=f'Médiane = {median:.2f}')

        # Supraface pour écart-type
        plt.axvspan(moyenne - ecart_type, moyenne + ecart_type, color='orange', alpha=0.3, label=f'1 écart-type')

         # Afficher la moyenne et la médiane
        plt.text(moyenne + 0.1, max(normalized_counts), f'Moyenne: {moyenne:.2f}', color='red')
        plt.text(median + 0.1, max(normalized_counts) - 0.02, f'Médiane: {median:.2f}', color='green')  # Ajuster la position pour qu'elle ne soit pas cachée par la barre

        # Afficher les probabilités
        for count, x in zip(normalized_counts, bins[:-1]): 
            if count > 0:  
                plt.text(x + (bins[1] - bins[0]) / 2, count, f'{count:.2f}', ha='center', va='bottom')

        plt.legend()
        plt.show()



    ###FONCTIONS VERSION probabiliste simplifiée
    
    def ajouter_probabilite(self,grille_prob, bateau, x, y):
        """
        Ajoute la probabilité de placer un bateau à la position (x, y) dans la grille de probabilités.

        Args:
            grille_prob (Grille): Grille des probabilités.
            bateau (Bateau): Bateau à placer.
            x (int): Coordonnée x de la grille.
            y (int): Coordonnée y de la grille.
        """

        grille_zero = Grille()  # Grille vide pour vérifier les placements
        #nb = Combinatoire.nb_configurations_possibles_bateau(bateau,grille_zero)
        longueur = bateau.longueur

        # Vérifie si le bateau peut être placé verticalement (direction 2) et horizontalement (direction 3)
        if grille_zero.peut_placer(bateau,(x,y),2):
                grille_prob.ajouter_placement(x,y,2,longueur,1)
        if grille_zero.peut_placer(bateau,(x,y),3):
                grille_prob.ajouter_placement(x,y,3,longueur,1)
    
    def probabilite_bateau(self,grille_prob, bateau):
        """
        Calcule la probabilité d'un bateau en itérant sur toutes les positions de la grille.

        Args:
            grille_prob (Grille): Grille des probabilités.
            bateau (Bateau): Bateau pour lequel la probabilité est calculée.
        """

        for x in range(grille_prob.TAILLE):
            for y in range(grille_prob.TAILLE):
                self.ajouter_probabilite(grille_prob,bateau,x,y)
        
        # Normalisation des probabilités
        grille_prob.grille /= grille_prob.grille.sum()

    
    def creation_grille_proba(self,grille_prob):
        """
        Crée la grille des probabilités pour tous les bateaux restants.

        Args:
            grille_prob (Grille): Grille des probabilités à remplir.
        """

        for bateau in self.bataille.grille.bateaux:
            if not bateau.est_coule():
                self.probabilite_bateau(grille_prob,bateau)


    

    def version_proba_simplifie(self):
        """
        Joue une partie en utilisant une stratégie probabiliste simplifiée.

        Returns:
            int: Le nombre de coups nécessaires pour gagner.
        """

        tirs = set()    # Ensemble des tirs déjà effectués
        coups = 0
        grille_prob = Grille()  # Grille pour stocker les probabilités
    
        while not self.bataille.victoire():
            self.creation_grille_proba(grille_prob)  # Crée la grille de probabilités
        
        # Trouve la case avec la probabilité maximale
            x, y = np.unravel_index(np.argmax(grille_prob.grille), grille_prob.grille.shape)
        
             # Vérifie si la case a déjà été tirée
            while (x, y) in tirs:
                grille_prob.grille[x, y] = 0
                x, y = np.unravel_index(np.argmax(grille_prob.grille), grille_prob.grille.shape)
        
            self.bataille.tirer((x, y))
            tirs.add((x, y))  
            coups += 1
        
            # bateau_touche = self.bataille.grille.getBateau(x, y)
        
            # if bateau_touche is not None and bateau_touche.est_coule():
            #     print(f"Bateau coulé à la position: ({x}, {y})")
        self.bataille.reset(True)  # Réinitialise la partie
    
        return coups
    
    def simulation_proba_simplifie(self):
        """
        Simule une partie en utilisant la version probabiliste simplifiée.

        Returns:
            str: Message indiquant le nombre de coups nécessaires.
        """

        coups = self.version_proba_simplifie()
        return f"Dans la version probabiliste simplifiée on a besoin de {coups} coups."
        
        

###FONCTIONS VERSION MONTE-CARLO
    def verifier_contraintes(self,cases_touches):
        """
        Vérifie si toutes les cases touchées contiennent un bateau.

        Args:
            cases_touches (set): Ensemble des cases touchées.

        Returns:
            bool: True si toutes les cases sont occupées par un bateau, sinon False.
        """

        g = self.bataille.grille
        for case in cases_touches:
            if g.grille[case[0],case[1]] == 0: #si une case touche n'est pas ocupe par une bateau
                return False
        return True
    
    def peut_placer_bateau_montecarlo(self,bateau,x,y,direction,cases_touches,g):
        """
        Vérifie si un bateau peut être placé dans une direction donnée.

        Args:
            bateau (Bateau): Bateau à placer.
            x (int): Coordonnée x.
            y (int): Coordonnée y.
            direction (int): Direction (1: SUD, 2: NORD, 3: OUEST, 4: EST).
            cases_touches_non_occ (set): Cases touchées qui ne sont pas occupées.
            g (Grille): Grille actuelle.

        Returns:
            bool: True si le bateau peut être placé, sinon False.
        """

        v1 = g.peut_placer(bateau,(x,y),direction)
        if not v1: 
            return False
        bateau_len = bateau.longueur

        # Vérification des contraintes en fonction de la direction

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
        return True
    
    def placements_possibles(self,bateau,grille,cases_touches_non_occ):
        """
        Trouve tous les placements possibles pour un bateau sur la grille.

        Args:
            bateau (Bateau): Bateau à placer.
            grille (Grille): Grille actuelle.
            cases_touches_non_occ (set): Cases touchées qui ne sont pas occupées.

        Returns:
            set: Ensemble des placements possibles sous forme de tuples (x, y, direction).
        """

        places = set()
        for x in range(grille.TAILLE):
            for y in range(grille.TAILLE):
                for dir in range(1,5):  # Directions possibles
                    if self.peut_placer_bateau_montecarlo(bateau,x,y,dir,cases_touches_non_occ,grille):
                        places.add((x,y,dir)) 
        return places
    
    def generer_grille_aleatoire(self, bateaux_restants, grille, cases_touches):
        """
        Génère une grille aléatoire en plaçant les bateaux restants tout en respectant les contraintes.

        Args:
            bateaux_restants (list): Liste des bateaux restants à placer.
            grille (Grille): Grille actuelle.
            cases_touches (set): Cases touchées.

        Returns:
            Grille or None: Grille avec les bateaux placés ou None si impossible.
        """

        if not bateaux_restants:
            # Si tous les bateaux sont placés, on vérifie les contraintes
            if self.verifier_contraintes(cases_touches):
                return grille
            else:
                return None

        bateau = random.choice(bateaux_restants)  # Choisit un bateau aléatoirement
        placements_pos= self.placements_possibles(bateau, grille,cases_touches)

        for placement in placements_pos:
            nouveau_g = Grille()
            nouveau_g.grille = np.copy(grille.grille) # Copie la grille actuelle

            position = (placement[0],placement[1])
            direction = placement[2]

            present = False

             # Vérifie si la position est déjà touchée
            if position in cases_touches:
                present = True
                cases_touches.remove(position)  # Enlève de la liste si elle est touchée

            nouveau_g.placer_bateau(bateau,position,direction)  # Place le bateau 
            nouvelle_liste_bateaux = [b for b in bateaux_restants if b != bateau] # Bateaux restants

            resultat = self.generer_grille_aleatoire(nouvelle_liste_bateaux, nouveau_g, cases_touches)
            if present:
                cases_touches.add(position)  # Réajoute si elle était touchée
            if resultat is not None:
                return resultat  # Retourne la grille valide

        return None  # Retourne None si aucun placement valide
    
    def creation_grille_probabilites(self,cases_touches,nb_simulations):
        """
        Effectue des simulations Monte-Carlo pour estimer la probabilité de présence d'un bateau sur chaque case.

        Args:
            cases_touches (set): Cases touchées.
            nb_simulations (int): Nombre de simulations à réaliser.

        Returns:
            np.ndarray: Matrice des probabilités.
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
            print("Warning: skip normalsation , sum = 0")
        return probabilites
        
    
    def version_montecarlo(self,nb_sim):
        """
        Joue une partie en utilisant la méthode de Monte-Carlo pour choisir les tirs.

        Args:
            nb_sim (int): Nombre de simulations à réaliser.

        Returns:
            int: Le nombre de coups nécessaires pour gagner.
        """

        tirs = set()  # Ensemble des tirs déjà effectués
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

    j = Joueur(0)

    # b1 = Bateau('TORPILLEUR',(9,1),3)
    # b2 = Bateau('TORPILLEUR',(1,5),4)
    # b3 = Bateau('PORTE_AVIONS',(4,9),1)
    # b4 = Bateau('CROISEUR',(2,2),2)
    # b5 = Bateau('SOUS_MARIN',(9,4),3)
    # l = [b1,b2,b3,b4,b5]

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

    b1 = Bateau('CROISEUR' ,(3, 3), 2)
    b3 = Bateau('TORPILLEUR', (5, 4), 1)
    b4 = Bateau('TORPILLEUR', (4, 7), 2)
    b5 = Bateau('PORTE_AVIONS',(7,5),1)
    l = [b1,b3,b4,b5]


    j.bataille.grille.bateaux = l
    j.bataille.grille.grille_ancienne()
    g = j.bataille.grille
    g.affiche_graph()
    print(f"Il y a {len(g.bateaux)} bateaux qui occupent {g.longueur_bateaux()} cases sur la grille de taille {g.TAILLE}")
    print(f"L'esperance theoretique est de {j.esperance_theoretique()} de coups.\n")

    print(j.simulation_proba_simplifie())
    j.graphe_distribution_aleatoire(100)
    j.graphe_distribution_heuristique(100)
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

    # cpt= j.version_proba_simplifie()
    # j.bataille.grille.affiche_graph()
    # print(cpt)
    # j.bataille.reset(True)
    # j.bataille.grille.affiche_graph()
    # cpt2 = j.version_proba_simplifie()
    # print(cpt2)

    # # res3 = j.simulation_version_proba_simplifie(100)
    # # print(res3)

    # cases_touches = [(2, 3), (4, 5)]
    # nb_simulations = 1000

