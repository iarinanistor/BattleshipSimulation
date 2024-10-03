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

def proba_grille(grille,max_tentatives=10000):
    bateaux = grille.bateaux
    grille_aux = Grille()
    grille_aux.bateaux = bateaux
    print(grille_aux.bateaux)
    cpt = 0
    while cpt <= max_tentatives:
        cpt += 1
        grille_aux.generer_grille()
        #print(grille_aux.grille)
        if grille.eq(grille_aux):
            return 1/cpt
        grille_aux.refresh_grille()
    print('On a pas trouve une grille exactement la meme')
    return None
    
#exercice 5 - on tire aleatoirement des positions pour les bateaux- esperqnce
#exercice 3 nb config possibles 100*95*93*... - fara directii si alte d qsteq, doar la nr de case
#poza 26.09




# torpi = Bateau('TORPILLEUR')
# grille_vide = Grille()
# print(nb_configurations_possibles_bateau(torpi,grille_vide))

# #3 echantillons

# #le 1er juste avec un bateau de type torpilleur

# grille_vide1 = Grille()
# torpi1 = Bateau('TORPILLEUR')
# # print(nb_configurations_possibles_liste_bateaux([torpi1],grille_vide1))



# # #le 2eme avec 2 bateaux de type torpiulleur et porte-avions

# porte_avions = Bateau('PORTE_AVIONS')
# # l1 = [torpi1,porte_avions]
# # print(nb_configurations_possibles_liste_bateaux(l1,grille_vide1))

# # #le 3eme avec 3 bateaux
# croiseur = Bateau('CROISEUR')
# l2 = [torpi1,porte_avions,croiseur]
# print(str(len(l2))+" " + str(nb_configurations_possibles_liste_bateaux(l2,grille_vide1)))
# g = Grille()
# g.bateaux = l2
# g.generer_grille()
# print(g.grille)

# print(proba_grille(g,max_tentatives=2229239))

# #TEST
# # torpi1 = Bateau('TORPILLEUR')
# # torpi2 = Bateau('TORPILLEUR')
# # torpi3 = Bateau('TORPILLEUR')
# # torpi4 = Bateau('TORPILLEUR')
# # torpi5 = Bateau('TORPILLEUR')
# # torpi6 = Bateau('TORPILLEUR')
# # torpi7 = Bateau('TORPILLEUR')
# # torpi8 = Bateau('TORPILLEUR')
# # sm1 = Bateau('SOUS_MARIN')
# # sm2 = Bateau('SOUS_MARIN')
# # sm3 = Bateau('SOUS_MARIN')
# # # sm4 = Bateau('SOUS_MARIN')
# # # sm5 = Bateau('SOUS_MARIN')
# # porte_avions = Bateau('PORTE_AVIONS')
# # croiseur = Bateau('CROISEUR')
# # torpi = Bateau('TORPILLEUR')
# # pa = Bateau('PORTE_AVIONS')
# # pa2 = Bateau('PORTE_AVIONS')
# # g = Grille()
# # l2 = [torpi1,torpi2,torpi3,torpi4, torpi5,porte_avions,croiseur,torpi,pa,pa2,sm1,sm2,sm3,torpi6,torpi7,torpi8]
# # g.bateaux = l2
# # g.generer_grille()
# # g.affiche_graph()

# # tor1 = Bateau('TORPILLEUR')
# # tor2 = Bateau('TORPILLEUR')
# # tor3 = Bateau('TORPILLEUR')
# # s1 = Bateau('SOUS_MARIN')
# # s2 = Bateau('SOUS_MARIN')
# # l = [tor1,tor2,tor3,s1,s2]
# # g1 = Grille()
# # g1.bateaux = l
# # g1.generer_grille()
# # g1.affiche_graph()
# # print(proba_grille(g1,max_tentatives=1000))



