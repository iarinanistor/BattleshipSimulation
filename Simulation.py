from Bateau import Bateau
from Grille import Grille
import Combinatoire
from Bataille import Bataille
from Joueur import Joueur
from Bayes import Bayes
import random
import time
import copy

def demander_nombre_bateaux():
    while True:
        try:
            nb_bateaux = int(input("Combien de bateaux voulez-vous ? (entre 1 et 50): "))
            if 1 <= nb_bateaux <= 50:
                return nb_bateaux
            else:
                print("Veuillez entrer un nombre entre 1 et 20.")
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
    print("5. OPTION DE TEST 2 - bateaux nombreuses")
    print("6. OPTION DE TEST 3 - bateaux centrales ")

    while True:
        choix = input("Votre choix (1/2/3/..) : ")
        if choix == '1':
            nb_bateaux = random.randint(1,20)
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
        elif choix == '5':
            b1 = Bateau('CROISEUR' ,(3, 3), 2)
            b2 = Bateau('SOUS_MARIN', (4, 2), 4)
            b3 = Bateau('CROISEUR', (5, 7) ,2)
            b4 = Bateau('CONTRE_TORPILLEURS' ,(5, 9), 1)
            b5 = Bateau('CROISEUR' ,(9, 9), 1)
            b6 = Bateau('TORPILLEUR' ,(8, 6), 1)
            b7 = Bateau('TORPILLEUR', (5, 4), 1)
            b8 = Bateau('CONTRE_TORPILLEURS', (2, 3), 4)
            b9 = Bateau('SOUS_MARIN', (1, 4) ,4)
            b10 = Bateau('PORTE_AVIONS', (4, 6), 1)
            b11 = Bateau('CONTRE_TORPILLEURS', (5, 2), 4)
            b12 = Bateau('TORPILLEUR', (0, 7), 2)
            b13 = Bateau('CONTRE_TORPILLEURS', (8, 4), 1)
            b14 = Bateau('CROISEUR', (6, 5), 1)
            b15 = Bateau('TORPILLEUR' ,(2, 8), 3)
            return [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15]
        elif choix == '6':
            b1 = Bateau('CROISEUR' ,(3, 3), 2)
            b3 = Bateau('TORPILLEUR', (5, 4), 1)
            b4 = Bateau('TORPILLEUR', (4, 7), 2)
            b5 = Bateau('PORTE_AVIONS',(7,5),1)
            return [b1,b3,b4,b5]
        else:
            print("Choix invalide, veuillez entrer 1, 2,..,6.")
    print("\n")

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
    print("3. J'AI CHOISI UNE OPTION DE TEST ")


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
    return f"le nombre de façon de placer cette liste de bateaux sur une grille vide est {Combinatoire.nb_configurations_possibles_liste_bateaux_grille_vide(copy.deepcopy(grille.bateaux))}"

def estimation_grilles(grille):
    print(f"Pour {len(grille.bateaux)} bateaux c'est une estimation de {Combinatoire.estimation_nombre_grilles(grille)} grilles")
    print("\n")


def nb_facons(grille):
    print("Maintenant, on a une fonction qui permet de calculer le nombre de façon de placer une liste de bateaux sur une grille vide. \n Si vous avez choisi une liste de >=3 bateaux, on va utiliser vostre liste, sinon on va utiliser l'option 1.\n")
    if len(grille.bateaux)>=3 :
        l = copy.deepcopy(grille.bateaux)
    else:
        b1 = Bateau('TORPILLEUR',(9,1),3)
        b2 = Bateau('TORPILLEUR',(1,5),4)
        b3 = Bateau('PORTE_AVIONS',(4,9),1)
        b4 = Bateau('CROISEUR',(2,2),2)
        l = [b1,b2,b3,b4]
    g = Grille()
    for i in range(1,4):
        g.bateaux = l[:i]
        print("Les bateaux a placer sont:\n" + Bateau.nom_bateaux(l[:i]))
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
        debut = time.time()
        estimation_grilles(g)
        fin = time.time()
        temps_execution = fin - debut
        print(f"Temps d'exécution: {temps_execution} secondes")
        print("\n\n")
    # g = Grille()
    # g.bateaux = l
    # g.generer_grille()
    # estimation_grilles(g)

def choix_version(grille):
    while True:
        print("Choisissez une version du jeu :")
        print("1. Version Aléatoire")
        print("2. Version Heuristique")
        print("3. Version Probabiliste")
        print("4. Quitter")
        
        choix = input("Entrez votre choix (1-4) : ")

        j = Joueur(0)
        j.bataille.grille = copy.deepcopy(grille)
        print(f"Il y a {len(grille.bateaux)} qui occupent {grille.longueur_bateaux()} cases \n")

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
            print(j.simulation_proba_simplifie())

        elif choix == '4':
            print("Merci d'avoir joué !")
            break

        else:
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 4.")

        # Demander si l'utilisateur veut rejouer ou quitter
        rejouer = input("Voulez-vous rejouer ? (o/n) : ")
        if rejouer.lower() != 'o':
            print("Merci d'avoir joué ! À bientôt.")
            break

def demander_probabilite_detection():
    while True:
        try:
            # Demander la probabilité à l'utilisateur
            prob_detection = float(input("Veuillez entrer la probabilité de détection du capteur (entre 0 et 1) : "))
            
            # Vérifier que la valeur est bien comprise entre 0 et 1
            if 0 <= prob_detection <= 1:
                print(f"La probabilité de détection saisie est : {prob_detection}")
                return prob_detection
            else:
                print("Erreur : La probabilité doit être un nombre entre 0 et 1.")
        except ValueError:
            print("Erreur : Veuillez entrer un nombre valide.")

def demander_type_distribution():
    print("Veuillez choisir le type de distribution de probabilité pour la localisation de l'objet :")
    print("1. Uniforme")
    print("2. Privilégiant les bords")
    print("3. Privilégiant le centre")
    
    while True:
        choix = input("Entrez le numéro de votre choix (1-3) : ")
        if choix in ['1', '2', '3']:
            return int(choix)
        else:
            print("Erreur : Veuillez entrer un numéro valide (1-3).")

def recherche_Bayes(grille):

    print("Souhaitez-vous rechercher un bateau spécifique ou laisser l'algorithme choisir aléatoirement ?")
    type_recherche = input("Tapez 's' pour chercher un bateau spécifique, ou 'a' pour une recherche aléatoire : ").lower()
    if type_recherche == 'a':
        b = random.choice(grille.bateaux)
    elif type_recherche == 's':
        print("Les bateux sur la grille:")
        print(Bateau.nom_bateaux(grille.bateaux))
        while True:
            num = int(input("Tapez l'index 'index)' du bateau   ex: 1) TORPILLEUR -> '1'"))
            if num in range (len(grille.bateaux)):
                break
            print("Numero invalide")
        b = grille.bateaux[num]
    p = demander_probabilite_detection()
    d = demander_type_distribution()
    bayes = Bayes(grille,p)
    if d==1:
        bayes.changer_proba_uniforme()
    elif d==2:
        bayes.changer_proba_bords()
    elif d==3:
        bayes.changer_proba_centre()
    bayes.recherche_bayes(b)
    
def sim_bayes(grille):
    print("\nSi on veut rechercher un bateau coule?\nMaintenant, supposons que \n1. notre grille contient juste que des bateaux coules\n2. si on detecte une position (x,y) ou se trouve le bateau recherche, alors on l'a trouve")
    while True:
        recherche_Bayes(grille)
        rejouer = input("Voulez-vous reesayer ? (o/n) : ")
        if rejouer.lower() != 'o':
            print("Merci d'avoir joué ! À bientôt.")
            break



def main():
    print("Bonjour!\n")
    l = choix_bateaux()
    g = Grille()
    g.bateaux = l
    print("\n")
    placer_bateaux_sur_grille(g,l)
    for b in l :
        b.print_bateau()
    print("\n")
    g.affiche_graph()
    print(borne_superieure(g))
    nb_facons(g)
    for b in g.bateaux :
        b.print_bateau()
    g.affiche_graph()
    choix_version(g)
    g.affiche_graph()
    sim_bayes(g)
    

if __name__=='__main__':
    main()