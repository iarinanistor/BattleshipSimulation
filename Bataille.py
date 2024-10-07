from Bateau import Bateau
from Grille import Grille

class Bataille:

    def __init__(self,nb_bateaux):
        '''
        Initialise une instance du jeu de bataille navale avec une grille et un ensemble de bateaux.
        Args:
            nb_bateaux: le nombre de bateaux à générer aléatoirement pour la partie.
        '''

        b = Bateau.generation_aleatoire_bateau(nb_bateaux)
        self.grille = Grille()
        self.grille.bateaux = b # Assignation des bateaux à la grille
        self.grille.generer_grille() # Génération de la grille avec les bateaux
        self.tirs=[] # Liste des tirs effectués
    

    
    def tirer(self,position):
        '''
        Permet de tirer sur une position donnée dans la grille et de mettre à jour l'état des bateaux.

        Args:
            position: un tuple (x, y) représentant les coordonnées sur lesquelles tirer.

        Returns:
            None: si le tir a déjà été effectué à cet endroit ou s'il n'y a pas de bateau.
        '''
        
        if position in self.tirs :
            #print("Deja tire")
             # Tir déjà effectué à cette position
            return None
        
        self.tirs.append(position) # Ajoute la position à la liste des tirs
        x,y = position
        bateau = self.grille.getBateau(x,y) # Obtient le bateau présent à la position, s'il y en a un
        
        if bateau :
            #print("on touche la bateau ")
            #bateau.print_bateau()
            #print("#######")

            # Si un bateau est touché, on détermine la section touchée
            bx,by = bateau.position

            if bateau.direction==1 : #SUD
                index = bx-x
            elif bateau.direction == 2:  # NORD
                index = x - bx
            elif bateau.direction == 3:  # VEST
                index = y - by
            elif bateau.direction == 4:  # EST
                index = by - y

            bateau.touche[index] = True # Marque la section du bateau comme touchée

            if bateau.status == 0 :
                bateau.status = 1  # Change l'état du bateau à "touché"

            if bateau.est_coule():
                bateau.status = 2  # Change l'état du bateau à "coulé"
                self.grille.effacer_bateau(bateau)
                #bateau.print_bateau()
                #print(" est coule")

    def victoire(self):
        '''
        Vérifie si tous les bateaux de la grille ont été coulés.

        Returns:
            bool: True si tous les bateaux sont coulés, sinon False.
        '''
        
        return all([b.est_coule() for b in self.grille.bateaux])


    def reset(self,positions_exactes):
        '''
         Réinitialise la grille et les bateaux pour une nouvelle partie.

        Args:
            positions_exactes: booléen, True si on veut garder les anciennes positions des bateaux, 
            False pour générer de nouvelles positions.

        Returns:
            None
        '''

        self.grille.refresh_grille() # Rafraîchit la grille en réinitialisant les tirs
        
        for b in self.grille.bateaux:
            b.reset_status(positions_exactes)  # Réinitialise l'état de chaque bateau
        self.tirs=[] # Vide la liste des tirs
        if not positions_exactes:
            self.grille.generer_grille() # Génère une nouvelle grille si on ne garde pas les anciennes positions
        else:
            self.grille.grille_ancienne()  # Utilise les anciennes positions des bateaux si indiqué


# if __name__=='__main__':
#     b = Bataille(0)
#     g = b.grille
#     torpi1 = Bateau('TORPILLEUR',(2,2),1)
#     g.ajoute_bateau(torpi1)
#     g.placer_bateau_positions(torpi1)
#     g.affiche_graph()
#     b.tirer((1,2))
#     print(torpi1.status,torpi1.touche)
#     print(b.victoire())
#     b.tirer((2,2))
#     t = g.getBateau(2,2)
#     print(torpi1.status,torpi1.touche)
#     print(t.status, t.touche)
#     print(t is None)
#     print(torpi1.est_coule())
#     print(b.victoire())

        # def joue(self):
        #     cpt = 0

