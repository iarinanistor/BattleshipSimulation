from Grille import Grille
from Bateau import Bateau
from Bataille import Bataille
import random
import matplotlib.pyplot as plt

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
    
    
    def simulation_version_aleatoire(self,nb_essais,liste_bateaux = []):
        nb_coups = 0
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb_coups += self.version_aleatoire()
            self.bataille.reset(True)
        return nb_coups
    
    # def tire(self,x,y,tirs,tirs_a_venir): #tirs- set
    #     if (x,y) not in tirs: #pour pas compter les tirs donnes dans la meme position
    #         self.bataille.tirer((x,y))
    #         if self.bataille.grille.getBateau(x,y) != None:
    #             victime = True
    #             tirs_a_venir.add((x,y+1))
    #             tirs_a_venir.add((x+1,y+1))
    #             tirs_a_venir.add((x+1,y))
    #             coups += 1
    #             break

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
        if liste_bateaux != [] :
            self.bataille.grille.grille_selecte(liste_bateaux)
        
        for _ in range(nb_essais):
            nb_coups += self.version_heuristique()
            self.bataille.reset(True)
        return nb_coups








j = Joueur(5)
j.bataille.grille.affiche_graph()
results = j.simulation_version_aleatoire(100)
print(results)
j.bataille.grille.affiche_graph()
nb_essais = 1000

res2 = j.simulation_version_heuristique(100)
print(res2)
j.bataille.grille.affiche_graph()

# plt.hist(results, bins=30, density=True, alpha=0.75, color='blue')
# plt.xlabel('Nombre de coups')
# plt.ylabel('Densité')
# plt.title(f'Distribution du nombre de coups pour terminer une partie ({nb_essais} essais)')
# plt.grid(True)
# plt.show()