from Grille import Grille
from Bateau import Bateau
import numpy as np

def placement_specifique():
    grille = Grille()
    porte_avion = Bateau("PORTE_AVIONS")
    sous_marin = Bateau("SOUS_MARIN")

    grille.ajoute_bateau(porte_avion)
    grille.ajoute_bateau(sous_marin)

    grille.placer_bateau(porte_avion,(2,2),2)
    grille.affiche()
    grille.placer_bateau(sous_marin,(8,8),4)

    porte_avion.print_bateau()
    sous_marin.print_bateau()


    grille.affiche()
    print("#############################")

    #grille.effacer_bateau(sous_marin)
    #grille.effacer_bateau(sous_marin)
    grille.affiche()
    grille.affiche_graph()
    sous_marin.print_bateau()
    #print(grille.peut_placer(sous_marin,(6,8),2))

    grille.changer_direction(sous_marin,2)
    sous_marin.print_bateau()

    grille.affiche()
    grille.affiche_graph()
    print("#############################")

def placement_aleatoire():
    g = Grille()
    list_bateaux = Bateau.generation_aleatoire_bateau(2)
    for bateau in list_bateaux:
        g.ajoute_bateau(bateau)
    g.generer_grille()
    g.affiche_graph()
    g.bouger_simultanement(3)
    #g.affiche_graph()

placement_aleatoire()
