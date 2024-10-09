from Bateau import Bateau
from Grille import Grille

def nb_configurations_possibles_bateau(bateau,grille):
    '''
    Calcule le nombre de configurations possibles pour placer un bateau 
    sur une grille donnée, en considérant les directions Nord et Ouest.

    Args:
        bateau: un objet de type Bateau que l'on souhaite placer sur la grille.
        grille: un objet de type Grille représentant la grille sur laquelle on veut placer le bateau.

    Returns:
        int: Le nombre de configurations valides pour placer le bateau.
    '''

    nb = 0
    for x in range(grille.TAILLE):
        for y in range(grille.TAILLE):
            if grille.peut_placer(bateau,(x,y),2): # Vérification pour la direction Nord/Sud 
                nb+=1
            if grille.peut_placer(bateau,(x,y),3): # Vérification pour la direction Ouest/Est
                nb+=1
    return nb

def nb_configurations_bateau_grille_vide(bateau):
    '''
    Calcule le nombre de configurations possibles pour placer un bateau 
    sur une grille vide.

    Args:
        bateau: un objet de type Bateau représentant le bateau que l'on souhaite placer.

    Returns:
        int: Le nombre de configurations valides pour placer le bateau sur une grille vide.
    '''

    grille = Grille()  # Crée une nouvelle grille vide
    return nb_configurations_possibles_bateau(bateau,grille)

def borne_superieure_configurations(grille):
    '''
    Calcule la borne superieure du  nombre de configurations possibles pour placer un liste des bateaux.

    Args:
        grille: un objet de type Grille représentant la grille sur laquelle on veut placer les bateaux.

    Returns:
        int : La borne superieure pour les configurations possibles.
    '''
    nb = 1
    for bateau in grille.bateaux :
        nb *= nb_configurations_bateau_grille_vide(bateau)
    return nb

def nb_configurations_possibles_liste_bateaux(liste_bateaux,grille):
    '''
     Calcule le nombre de configurations possibles pour une liste de bateaux à placer sur une grille.

    Args:
        liste_bateaux: une liste d'objets Bateau que l'on souhaite placer.
        grille: un objet Grille représentant la grille sur laquelle les bateaux doivent être placés.

    Returns:
        int: Le nombre de configurations possibles pour placer tous les bateaux de la liste.
    '''

    if not liste_bateaux:  # Si la liste est vide, il y a une seule configuration possible
        return 1

    bateau = liste_bateaux[0]
    nb = 0
    directions = [2,3]  # Directions possibles : Nord/Sud (2) et Ouest/Est (3)
    
    for x in range(grille.TAILLE):
        for y in range(grille.TAILLE):
            pos = (x,y)
            for dir in directions:
                if grille.peut_placer(bateau,pos,dir):
                    grille.placer_bateau(bateau,pos,dir)  # Place le bateau si possible
                    nb += nb_configurations_possibles_liste_bateaux(liste_bateaux[1:],grille)  # Recursive pour le reste des bateaux
                    grille.effacer_bateau(bateau) # Efface le bateau pour tester d'autres configurations
    return nb

def nb_configurations_possibles_liste_bateaux_grille_vide(liste_bateaux):
    '''
     Calcule le nombre de configurations possibles pour une liste de bateaux à placer sur une grille vide.

    Args:
        liste_bateaux: une liste d'objets Bateau que l'on souhaite placer.
        grille: un objet Grille représentant la grille sur laquelle les bateaux doivent être placés.

    Returns:
        int: Le nombre de configurations possibles pour placer tous les bateaux de la liste.
    '''
    g = Grille()
    return nb_configurations_possibles_liste_bateaux(liste_bateaux,g)

def proba_grille(grille,max_tentatives=1000000000):
    '''
    Calcule le nombre de tentatives nécessaires pour obtenir la même configuration de bateaux 
    sur une grille générée aléatoirement.

    Args:
        grille: un objet Grille représentant la grille cible avec une certaine configuration de bateaux.
        max_tentatives: un entier représentant le nombre maximum de tentatives (par défaut 10 000).

    Returns:
        int: Le nombre de tentatives nécessaires pour retrouver la même grille.
        None: Si la même grille n'a pas été trouvée après le nombre maximal de tentatives.
    '''

    bateaux = grille.bateaux
    grille_aux = Grille() # Grille auxiliaire pour tester les placements
    grille_aux.bateaux = bateaux

    cpt = 0
    while cpt <= max_tentatives:
        cpt += 1

        grille_aux.generer_grille() # Génère une nouvelle grille
        if grille.eq(grille_aux): # Compare les deux grilles
            return cpt # Retourne le nombre de tentatives si elles sont identiques
            
        grille_aux.refresh_grille()   # Réinitialise la grille auxiliaire pour une nouvelle tentative
    print("On n a pas trouvé une grille exactement identique.")
    return None

def estimation_nombre_grilles(grille, iterations=100):
    cpt= 0
    for _ in range(iterations):
        essais = proba_grille(grille)
        cpt += essais
    return cpt/iterations

    # if nb == 0:
    #     return "La grille cible n'a pas été générée, augmentez le nombre d'itérations."

    # proportion = nb / iterations
    # estimation_total = 1 / proportion
    # return estimation_total
    
#exercice 5 - on tire aleatoirement des positions pour les bateaux- esperqnce
#exercice 3 nb config possibles 100*95*93*... - fara directii si alte d qsteq, doar la nr de case
#poza 26.09


if __name__=='__main__':
    g = Grille()
    torpi = Bateau('TORPILLEUR')
    porte_avions = Bateau('PORTE_AVIONS')
    g.ajoute_bateau(torpi)
    g.placer_bateau(torpi,(4,4),1)
    g.ajoute_bateau(porte_avions)
    g.placer_bateau(porte_avions,(7,1),3)

    b1 = Bateau('TORPILLEUR',(9,1),3)
    b2 = Bateau('TORPILLEUR',(1,5),4)
    b3 = Bateau('PORTE_AVIONS',(4,9),1)
    b4 = Bateau('CROISEUR',(2,2),2)
    b5 = Bateau('SOUS_MARIN',(9,4),3)
    g.affiche_graph()
    print("#########")
    print(nb_configurations_possibles_liste_bateaux_grille_vide([b1,b2]))
    print(nb_configurations_bateau_grille_vide(porte_avions))
    for b in [b1,b2,b3,b4,b5]:
        print(nb_configurations_bateau_grille_vide(b))
    #print(proba_grille(g))
    print(borne_superieure_configurations(g))

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



