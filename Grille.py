import random
import matplotlib.pyplot as plt
import numpy as np

class Grille:
    TAILLE = 10   # Taille de la grille

    def __init__(self):
        # Initialiser la grille avec des zéros et une liste pour les bateaux

        self.grille = np.zeros((self.TAILLE, self.TAILLE), dtype=float)
        self.bateaux = []  
    
    def ajoute_bateau(self, bateau):
        '''
        Ajouter un bateau à la liste des bateaux
        '''
        self.bateaux.append(bateau)
    
    def peut_placer(self, bateau, position, direction):
        '''
        Vérifie si le bateau peut être placé à la position donnée avec la direction donnée
        Args:
            bateau: l'objet bateau à placer.
            position: tuple (x, y) représentant la position de placement.
            direction: direction du placement (1: SUD, 2: NORD, 3: OUEST, 4: EST).
        
        Returns:
            True si le placement est possible, False sinon.
        '''
        bateau_len = bateau.longueur   # Longueur du bateau
        x, y = position  # Décomposer la position en coordonnées x et y

        # Vérifier si la position est dans les limites de la grille       
        if x not in range(10):
            return False
        if y not in range(10):
            return False
        

        # Vérifier si le bateau peut être placé (doit être ok)
        if bateau.status != 0:
            return False

        if direction == 1:  # SUD
            if x - bateau_len + 1 < 0:  # Vérifie si le bateau dépasse le bord de la grille
                return False
            for i in range(bateau_len):
                if self.grille[x - i, y] != 0: # Vérifie si l'espace est libre
                    return False

        elif direction == 2:  # NORD
            if x + bateau_len > self.TAILLE:  # Vérifie si le bateau dépasse le bord de la grille
                return False
            for i in range(bateau_len):
                if self.grille[x + i, y] != 0: # Vérifie si l'espace est libre
                    return False

        elif direction == 3:  # OUEST  
            if y + bateau_len > self.TAILLE:  # Vérifie si le bateau dépasse le bord de la grille
                return False
            for i in range(bateau_len):
                if self.grille[x, y + i] != 0: # Vérifie si l'espace est libre
                    return False

        elif direction == 4:  # EST
            if y - bateau_len + 1 < 0:  # Vérifie si le bateau dépasse le bord de la grille
                return False
            for i in range(bateau_len):
                if self.grille[x, y - i] != 0: # Vérifie si l'espace est libre
                    return False

        return True
    

    # Fonction auxiliaire pour placer un bateau
    def placement(self, x, y, direction, bateau_len, val):
        '''
        Place un bateau sur la grille à la position donnée dans la direction spécifiée.
        Args:
            x: coordonnée x pour le placement.
            y: coordonnée y pour le placement.
            direction: direction du placement (1: SUD, 2: NORD, 3: OUEST, 4: EST).
            bateau_len: longueur du bateau.
            val: valeur à placer sur la grille (identifiant du bateau).
        '''
        if direction == 1:  # SUD
            for i in range(bateau_len):
                self.grille[x - i, y] = val

        elif direction == 2:  # NORD
            for i in range(bateau_len):
                self.grille[x + i, y] = val

        elif direction == 3:  # OUEST
            for i in range(bateau_len):
                self.grille[x, y + i] = val

        elif direction == 4:  # EST
            for i in range(bateau_len):
                self.grille[x, y - i] = val
        
    def ajouter_placement(self, x, y, direction, bateau_len, val):
        '''
        Ajoute une valeur val sur la grille à la position donnée dans la direction spécifiée.
        Args:
            x: coordonnée x pour le placement.
            y: coordonnée y pour le placement.
            direction: direction du placement (1: SUD, 2: NORD, 3: OUEST, 4: EST).
            bateau_len: longueur du bateau.
            val: valeur à ajouter sur la grille .
        '''
        if direction == 1:  # SUD
            for i in range(bateau_len):
                self.grille[x - i, y] += val

        elif direction == 2:  # NORD
            for i in range(bateau_len):
                self.grille[x + i, y] += val

        elif direction == 3:  # VEST
            for i in range(bateau_len):
                self.grille[x, y + i] += val

        elif direction == 4:  # EST
            for i in range(bateau_len):
                self.grille[x, y - i] += val

    
    def effacer_bateau(self, bateau):
        '''
        Efface le bateau de la grille.
        Args:
            bateau: l'objet bateau à effacer.
        '''
        x, y = bateau.position
        bateau_len = bateau.longueur
        direction = bateau.direction
        self.placement(x, y, direction, bateau_len, 0) # Remplacer par 0 sur la grille
        
        

    def placer_bateau(self, bateau, position, direction):
        '''
        Placer un bateau sur la grille à une position donnée dans une direction donnée.
        Args:
            bateau: l'objet bateau à placer.
            position: tuple (x, y) représentant la position de placement.
            direction: direction du placement (1: SUD, 2: NORD, 3: OUEST, 4: EST).
        '''

        self.effacer_bateau(bateau) # Effacer l'ancienne position
        if self.peut_placer(bateau, position, direction): # Vérifier si le placement est possible 
            x, y = position
            bateau_len = bateau.longueur
            id_prefixe = int(str(bateau.id)[0])  # On prend juste l'id du type de bateau pour l'identifier sur la grille
            self.placement(x, y, direction, bateau_len, id_prefixe)
            bateau.position = position
            bateau.direction = direction
        else:
            print(f"Impossible de placer {bateau.nom} ici.")  # Message d'erreur si impossible
            self.placer_bateau(bateau,bateau.position,bateau.direction) # Essayer de le placer à sa position actuelle


    def placer_bateau_positions(self,bateau):
        '''
        Placer le bateau selon sa position et direction.
        Args:
            bateau: l'objet bateau à placer.
        '''

        self.placer_bateau(bateau,bateau.position,bateau.direction)
    
    def place_alea(self, bateau):
        '''
        Place un bateau aléatoirement sur la grille.
        Args:
            bateau: l'objet bateau à placer aléatoirement.
        '''

        peut_placer = False
        if bateau.status != 0:  # Si le bateau n'est pas en état de placement
            peut_placer = True
        while not peut_placer:
            position = (random.randint(0, self.TAILLE - 1), random.randint(0, self.TAILLE - 1))  # Position aléatoire
            direction = random.randint(1, 4)  # Direction aléatoire
            if self.peut_placer(bateau, position, direction):
                self.placer_bateau(bateau, position, direction)
                peut_placer = True # Placement réussi
    
    def changer_direction(self, bateau, direction):
        '''
        Change la direction d'un bateau et le repositionne si nécessaire.
        Args:
            bateau: l'objet bateau dont on veut changer la direction.
            direction: nouvelle direction à assigner au bateau.
        '''

        if direction != bateau.direction: # Si la direction change
            x, y = bateau.position
            bateau_len = bateau.longueur
            # Vérifier les directions pour repositionner le bateau
            if bateau.direction == 1 or bateau.direction==2 :
                if direction == 2:
                    self.placer_bateau(bateau, (x - bateau_len + 1, y), 2)
                elif direction == 3:
                    self.placer_bateau(bateau, (x, y - bateau_len + 1), 3)
                elif direction == 4:
                    self.placer_bateau(bateau, (x, y + bateau_len - 1), 4)
                elif direction == 1:
                    self.placer_bateau(bateau, (x + bateau_len - 1, y), 1)
            elif bateau.direction == 3 or bateau.direction == 4:
                if direction == 1:
                    self.placer_bateau(bateau, (x + bateau_len - 1, y), 1)
                elif direction == 2:
                    self.placer_bateau(bateau, (x - bateau_len + 1, y), 2)
                elif direction == 4:
                    self.placer_bateau(bateau, (x, y + bateau_len - 1), 4)
                elif direction == 3:
                    self.placer_bateau(bateau, (x, y - bateau_len + 1), 3)

    def getBateau(self, x, y):
        '''
        Récupère le bateau qui occupe la position (x, y) sur la grille.
        Args:
            x: coordonnée x.
            y: coordonnée y.
        Returns:
            Le bateau s'il en existe un à la position (x, y), sinon None.
        '''

        # Vérifier si la position est valide
        if x < 0 or x >= self.TAILLE or y < 0 or y >= self.TAILLE:
            return None  # Les coordonnées sont hors de la grille
        
        # Parcourir tous les bateaux pour voir si un bateau occupe la position (x, y)
        for bateau in self.bateaux:
            bateau_len = bateau.longueur
            bx, by = bateau.position
            direction = bateau.direction
            
            # Vérifier si (x, y) est occupé par ce bateau selon sa direction
            if direction == 1:  # SUD
                if by == y and bx - bateau_len + 1 <= x <= bx:
                    return bateau
            
            elif direction == 2:  # NORD
                if by == y and bx <= x < bx + bateau_len:
                    return bateau
            
            elif direction == 3:  # OUEST
                if bx == x and by <= y < by + bateau_len:
                    return bateau
            
            elif direction == 4:  # EST
                if bx == x and by - bateau_len + 1 <= y <= by:
                    return bateau
        
        # Si aucune correspondance n'a été trouvée, retourner None
        return None


    
    def bouger(self,bateau,nb):
        '''
        Déplace un bateau de manière aléatoire un certain nombre de fois.
        Args:
            bateau: l'objet bateau à déplacer.
            nb: nombre de mouvements aléatoires.
        '''
        for _ in range(nb):
            direction = random.randint(1,4)
            self.changer_direction(bateau,direction)
            self.affiche_graph()
    
    def bouger_simultanement(self,nb):
        '''
        Déplace simultanément tous les bateaux sur la grille un certain nombre de fois.
        Args:
            nb: nombre de mouvements pour chaque bateau.
        '''
        for _ in range(nb):
            for bateau in self.bateaux:
                self.bouger(bateau,1)

        
    def affiche(self):
        '''
        Affiche la grille sous forme de tableau numérique.
        '''
        print(self.grille)

    def affiche_graph(self):
        '''
        Affiche la grille graphiquement avec Matplotlib.
        '''

        plt.imshow(self.grille, cmap='jet', origin='lower')  # Utilise le colormap 'jet' pour plus de contraste
        plt.colorbar()
        plt.gca().invert_yaxis()   # Inverser l'axe y pour que (0,0) soit en bas à gauche
        plt.title("Grille Display")
        plt.show()
    
    def eq(self, grilleB):
        '''
        Compare la grille actuelle avec une autre grille pour vérifier l'égalité.
        Args:
            grilleB: une autre instance de Grille à comparer.
        Returns:
            True si les deux grilles sont identiques, False sinon.
        '''

        return np.array_equal(self.grille, grilleB.grille)
    
    def estVide(self):
        '''
        Vérifie si la grille est vide (toutes les cases sont à 0).
        Returns:
            True si la grille est vide, False sinon.
        '''
        return np.array_equal(self.grille, np.zeros((self.TAILLE,self.TAILLE)))
    
    def grille_selecte(self,bateaux):
        '''
        Charge une sélection de bateaux dans la grille.
        Args:
            bateaux: une liste de bateaux à placer sur la grille.
        '''

        self.refresh_grille()
        self.bateaux = bateaux
        self.generer_grille()

    def grille_ancienne(self):
        '''
        Recharge la grille avec les positions précédentes des bateaux si elle est vide.
        '''
        
        if not self.estVide():
            return None
        for bateau in self.bateaux:
            self.placer_bateau_positions(bateau)

    def generer_grille(self):
        '''
        Génère une grille en plaçant aléatoirement les bateaux.
        '''
        
        for bateau in self.bateaux:
            self.place_alea(bateau)

    def refresh_grille(self):
        '''
        Réinitialise la grille à un tableau de zéros (vide).
        '''
        
        self.grille = np.zeros((self.TAILLE, self.TAILLE), dtype=float)
    
    def longueur_bateaux(self):
        """
        Calcule la somme des longueurs de tous les bateaux dans la grille.

        Args:
            self: L'instance de la classe qui contient une liste de bateaux (self.bateaux).

        Returns:
            int: La somme des longueurs de tous les bateaux.
        """
        s = 0
        for b in self.bateaux:
            s+=b.longueur
        return s
    