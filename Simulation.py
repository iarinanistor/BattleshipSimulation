from Bateau import Bateau
from Grille import Grille
import Combinatoire
from Bataille import Bataille
from Joueur import Joueur
from Bayes import Bayes
import random

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
    print("4. OPTION DE TEST 1")

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
            b1
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
    print("3. OPTION DE TEST 1 ")


    while True:
        choix = input("Votre choix (1/2/3) : ")
        if choix == '1':
            grille.generer_grille()  # Placer les bateaux de façon aléatoire
            break
        elif choix == '2':
            for bateau in liste_bateaux:
                demander_position_bateau(grille,bateau) # Placer spécifiquement
            break
        else:
            print("Choix invalide, veuillez entrer 1 ou 2.")
    
def borne_superieure(grille):
    f"La borne supérieure simple du nombre de configurations possibles pour la liste complète de bateaux est {Combinatoire.borne_superieure_configurations(grille)}"

def main():
    l = choix_bateaux()
    g = Grille()
    g.bateaux = l
    for b in l :
        b.print_bateau()
    placer_bateaux_sur_grille(g,l)
    g.affiche_graph()
    

if __name__=='__main__':
    main()