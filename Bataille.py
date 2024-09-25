from Bateau import Bateau
from Grille import Grille

class Bataille:
    def __init__(self,nb_bateaux):
        b = Bateau.generation_aleatoire_bateau(nb_bateaux)
        self.grille = Grille()
        self.grille.bateaux = b
        self.grille.generer_grille()
        self.tirs=[]
    
    def tirer(self,position):
        if position in self.tirs :
            print("Deja tire")
            return None
        self.tirs.append(position)
        x,y = position
        bateau = self.grille.getBateau(x,y)
        if bateau :
            bx,by = bateau.position

            if bateau.direction==1 : #SUD
                index = bx-x
            elif bateau.direction == 2:  # NORD
                index = x - bx
            elif bateau.direction == 3:  # VEST
                index = y - by
            elif bateau.direction == 4:  # EST
                index = by - y
            bateau.touche[index] = True
            if bateau.status == 0 :
                bateau.status = 1
            if bateau.est_coule():
                bateau.status = 2
                self.grille.effacer_bateau(bateau)
                bateau.print_bateau()
                print(" est coule")

    def victoire(self):
        return all([b.est_coule() for b in self.grille.bateaux])


    def reset(self):
        self.grille.refresh_grille()
        for b in self.grille.bateaux:
            b.reset_status()
        self.tirs=[]
        self.grille.generer_grille()


    # def joue(self):
    #     cpt = 0

