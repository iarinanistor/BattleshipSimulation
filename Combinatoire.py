from Bateau import Bateau
from Grille import Grille

def nb_configurations_possibles_bateau(bateau,grille):
    nb = 0
    for x in range(grille.TAILLE):
        for y in range(grille.TAILLE):
            if grille.peut_placer(bateau,(x,y),2):
                nb+=1
            if grille.peut_placer(bateau,(x,y),3):
                nb+=1
    return nb

def nb_configurations_possibles_liste_bateaux(liste_bateaux,grille):
    if not liste_bateaux:
        return 1

    bateau = liste_bateaux[0]
    nb = 0
    directions = [2,3]
    
    for x in range(grille.TAILLE):
        for y in range(grille.TAILLE):
            pos = (x,y)
            for dir in directions:
                if grille.peut_placer(bateau,pos,dir):
                    grille.placer_bateau(bateau,pos,dir)
                    nb += nb_configurations_possibles_liste_bateaux(liste_bateaux[1:],grille)
                    grille.effacer_bateau(bateau)
    return nb

def proba_grille(grille):
    bateaux = grille.bateaux
    grille_aux = Grille()
    grille_aux.bateaux = grille.bateaux
    cpt = 0
    while True:
        cpt += 1
        grille_aux.generer_grille()
        if grille.eq(grille_aux):
            break
        grille_aux.refresh_grille()
    return cpt
    




# torpi = Bateau('TORPILLEUR')
# grille_vide = Grille()
# print(nb_configurations_possibles_bateau(torpi,grille_vide))

# #3 echantillons

# #le 1er juste avec un bateau de type torpilleur

# grille_vide1 = Grille()
# torpi1 = Bateau('TORPILLEUR')
# print(nb_configurations_possibles_liste_bateaux([torpi1],grille_vide1))



# #le 2eme avec 2 bateaux de type torpiulleur et porte-avions

# porte_avions = Bateau('PORTE_AVIONS')
# l1 = [torpi1,porte_avions]
# print(nb_configurations_possibles_liste_bateaux(l1,grille_vide1))

# #le 3eme avec 3 bateaux
# croiseur = Bateau('CROISEUR')
# l2 = [torpi1,porte_avions,croiseur]
# print(nb_configurations_possibles_liste_bateaux(l2,grille_vide1))

#TEST
torpi1 = Bateau('TORPILLEUR')
torpi2 = Bateau('TORPILLEUR')
torpi3 = Bateau('TORPILLEUR')
torpi4 = Bateau('TORPILLEUR')
torpi5 = Bateau('TORPILLEUR')
sm1 = Bateau('SOUS_MARIN')
sm2 = Bateau('SOUS_MARIN')
sm3 = Bateau('SOUS_MARIN')
porte_avions = Bateau('PORTE_AVIONS')
croiseur = Bateau('CROISEUR')
torpi = Bateau('TORPILLEUR')
pa = Bateau('PORTE_AVIONS')
pa2 = Bateau('PORTE_AVIONS')
g = Grille()
l2 = [torpi1,torpi2,torpi3,torpi4, torpi5,porte_avions,croiseur,torpi,pa,pa2,sm1,sm2,sm3]
g.bateaux = l2
g.generer_grille()
g.affiche_graph()
print(proba_grille(g))



