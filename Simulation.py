from Bateau import Bateau
from Grille import Grille
import Combinatoire
from Bataille import Bataille
from Joueur import Joueur
from Bayes import Bayes
import random
import time

def demander_nombre_bateaux():
    while True:
        try:
            nb_bateaux = int(input("Combien de bateaux voulez-vous ? (entre 1 et 50): "))
            if 1 <= nb_bateaux <= 50:
                return nb_bateaux
            else:
                print("Veuillez entrer un nombre entre 1 et 50.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre.")

def demander_specification_bateaux():
    print(
        " (BATEAU: LONGUEUR) = (PORTE_AVIONS: 5), (CROISEUR: 4), (CONTRE_TORPILLEURS: 3), (SOUS_MARIN: 3), (TORPILLEUR: 2)        "
    )
    bateaux_specifiques = []
    nb_bateaux = demander_nombre_bateaux()

    for i in range(nb_bateaux):
        nom = (input(f"Entrez le nom du bateau {i + 1} (doit faire partie de la liste): "))
        while nom not in Bateau.ID_LONGUEURS_BATEAUX:
            print("Nom invalide, veuillez entrer un nom qui fait partie de la liste")
            nom = (input(f"Entrez le nom du bateau {i + 1} (doit faire partie de la liste): "))
        bateaux_specifiques.append(Bateau(nom))

    return bateaux_specifiques

#def demander_placement_bateaux

def choix_bateaux():
    print("Choisissez une option pour les bateaux:")
    print("1. Utiliser des bateaux aléatoires")
    print("2. Fournir une liste spécifique de bateaux")
    print("3. Spécifier un nombre de bateaux à générer aléatoirement")
    print("4. OPTION DE TEST 1 - bateaux aux peripheries")

    while True:
        choix = input("Votre choix (1/2/3/4) : ")
        if choix == '1':
            nb_bateaux = random.randint(1,50)
            return Bateau.generation_aleatoire_bateau(nb_bateaux)
        elif choix == '2':
            return demander_specification_bateaux()
        elif choix == '3':
            nb_bateaux = demander_nombre_bateaux()
            return Bateau.generation_aleatoire_bateau(nb_bateaux)
        elif choix == '4':
            b1 = Bateau('TORPILLEUR',(9,1),3)
            b2 = Bateau('TORPILLEUR',(1,5),4)
            b3 = Bateau('PORTE_AVIONS',(4,9),1)
            b4 = Bateau('CROISEUR',(2,2),2)
            b5 = Bateau('SOUS_MARIN',(9,4),3)
            return [b1,b2,b3,b4,b5]
        else:
            print("Choix invalide, veuillez entrer 1, 2, 3 ou 4.")

def demander_position_bateau(grille,bateau):
    """Demande à l'utilisateur où placer le bateau."""
    while True:
        try:
            x = int(input(f"Entrez la position x pour le bateau  {bateau.info_bateau()}: "))
            y = int(input(f"Entrez la position y pour le bateau  {bateau.info_bateau()}: "))
            direction = int(input("Entrez la direction (1: SUD, 2: NORD, 3: OUEST, 4: EST): "))
            if 0 <= x <= 9 and 0 <= y <= 9 and 1 <= direction <= 4 and grille.peut_placer(bateau,(x,y),direction):
                grille.placer_bateau(bateau,(x,y),direction)
                return (x, y), direction
            else:
                print("Veuillez entrer des coordonnées valides (0-9) et une direction valide (1-4).")
        except ValueError:
            print("Entrée invalide, veuillez réessayer.")

def placer_bateaux_sur_grille(grille, liste_bateaux):
    print("Voulez-vous placer les bateaux aléatoirement ou spécifiquement?")
    print("1. Aléatoirement")
    print("2. Spécifiquement")
    print("3. J'AI CHOISI OPTION DE TEST 1 ")


    while True:
        choix = input("Votre choix (1/2/3) : ")
        if choix == '1':
            grille.generer_grille()  # Placer les bateaux de façon aléatoire
            break
        elif choix == '2':
            for bateau in liste_bateaux:
                demander_position_bateau(grille,bateau) # Placer spécifiquement
            break
        elif choix == '3':
            for bateau in liste_bateaux:
                grille.placer_bateau_positions(bateau)
            break
        else:
            print("Choix invalide, veuillez entrer 1, 2 ou 3.")
    
def borne_superieure(grille):
    return f"La borne supérieure simple du nombre de configurations possibles pour la liste complète de bateaux est {Combinatoire.borne_superieure_configurations(grille)}"

def nb_facons_placement_bateaux(grille):
    return f"le nombre de façon de placer cette liste de bateaux sur une grille vide est {Combinatoire.nb_configurations_possibles_liste_bateaux_grille_vide(grille.bateaux)}"

def estimation_grilles(grille):
    print(f"Pour {len(grille.bateaux)} bateaux c'est une estimation de {Combinatoire.estimation_nombre_grilles(grille)} grilles")
    print("\n")


def nb_facons(grille):
    print("Maintenant, on a une fonction qui permet de calculer le nombre de façon de placer une liste de bateaux sur une grille vide. \n Si vous avez choisi une liste de >=3 bateaux, on va utiliser vostre liste, sinon on va utiliser l'option 1.\n")
    if len(grille.bateaux)>=3 :
        l = grille.bateaux
    else:
        b1 = Bateau('TORPILLEUR',(9,1),3)
        b2 = Bateau('TORPILLEUR',(1,5),4)
        b3 = Bateau('PORTE_AVIONS',(4,9),1)
        b4 = Bateau('CROISEUR',(2,2),2)
        l = [b1,b2,b3,b4]
    g = Grille()
    for i in range(1,4):
        g.bateaux = l[:i]
        print("Les bateaux a placer sont:" + Bateau.nom_bateaux(l[:i]))
        debut = time.time()
        print(nb_facons_placement_bateaux(g))
        fin = time.time()
        temps_execution = fin - debut
        print(f"Temps d'exécution: {temps_execution} secondes")
        print("\n\n")
    print("Donc, ca commence a prendre beaucouuuup de temps. Comment on fait?")
    print("Il nous reste a estimer le nombre total de grilles possibles, par une methode basée sur le calcul de l'espérance mathématique \n")
    for i in range(1,3):
        g.bateaux = l[:i]
        g.generer_grille()
        estimation_grilles(g)

def choix_version(grille):
    while True:
        print("Choisissez une version du jeu :")
        print("1. Version Aléatoire")
        print("2. Version Heuristique")
        print("3. Version Probabiliste")
        print("4. Quitter")
        
        choix = input("Entrez votre choix (1-4) : ")

        j = Joueur(0)
        j.bataille.grille = grille

        if choix == '1':
            # Jouer à la version aléatoire
            nb_essais = int(input("Entrez le nb d'essais : "))
            j.graphe_distribution_aleatoire(nb_essais)

        elif choix == '2':
            # Jouer à la version heuristique
            nb_essais = int(input("Entrez le nb d'essais : "))
            j.graphe_distribution_heuristique(nb_essais)

        elif choix == '3':
            # Jouer à la version probabiliste
            #(f"Nombre de coups joués dans la version probabiliste : {coups}")
            nb=1

        elif choix == '4':
            print("Merci d'avoir joué ! À bientôt.")
            break

        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")

        # Demander si l'utilisateur veut rejouer ou quitter
        rejouer = input("Voulez-vous rejouer ? (o/n) : ")
        if rejouer.lower() != 'o':
            print("Merci d'avoir joué ! À bientôt.")
            break


def main():
    l = choix_bateaux()
    g = Grille()
    g.bateaux = l
    for b in l :
        b.print_bateau()
    placer_bateaux_sur_grille(g,l)
    g.affiche_graph()
    print(borne_superieure(g))
    #nb_facons(g)
    choix_version(g)
    

if __name__=='__main__':
    main()