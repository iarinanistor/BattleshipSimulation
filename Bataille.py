from Bateau import Bateau
from Grille import Grille

class Bataille:
    def __init__(self,nb_bateaux):
        b = Bateau.generation_aleatoire_bateau(nb_bateaux)
        self.grille = Grille()
        self.grille.bateaux = b
        self.grille.generer_grille()
        self.tirs=[]
        #vezi cum vrei sa faci: aleatoire sau nu
    

    
    def tirer(self,position):
        if position in self.tirs :
            #print("Deja tire")
            return None
        self.tirs.append(position)
        x,y = position
        bateau = self.grille.getBateau(x,y)
        
        if bateau :
            #print("on touche la bateau ")
            #bateau.print_bateau()
            #print("#######")

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
                #bateau.print_bateau()
                #print(" est coule")

    def victoire(self):
        return all([b.est_coule() for b in self.grille.bateaux])


    def reset(self,positions_exactes):
        #positions_exactes - True si on veut les positions anciennes et False sinon
        self.grille.refresh_grille()
        for b in self.grille.bateaux:
            b.reset_status(positions_exactes)
        self.tirs=[]
        if not positions_exactes:
            self.grille.generer_grille()
        else:
            self.grille.grille_ancienne()


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

