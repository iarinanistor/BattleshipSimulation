import random
import matplotlib.pyplot as plt
import numpy as np

class Grille:
    TAILLE = 10

    def __init__(self):
        self.grille = np.zeros((self.TAILLE, self.TAILLE), dtype=int)
        self.bateaux = []  
    
    def ajoute_bateau(self, bateau):
        self.bateaux.append(bateau)
    
    def peut_placer(self, bateau, position, direction):
        # direction 1 = SUD, 2 = NORD, 3 = VEST, 4 = EST
        bateau_len = bateau.longueur
        x, y = position

        if x not in range(10):
            return False
        if y not in range(10):
            return False
        if bateau.status != 0:
            return False

        if direction == 1:  # SUD
            if x - bateau_len + 1 < 0:
                return False
            for i in range(bateau_len):
                if self.grille[x - i, y] != 0:
                    return False

        elif direction == 2:  # NORD
            if x + bateau_len > self.TAILLE:
                return False
            for i in range(bateau_len):
                if self.grille[x + i, y] != 0:
                    return False

        elif direction == 3:  # VEST
            if y + bateau_len > self.TAILLE:
                return False
            for i in range(bateau_len):
                if self.grille[x, y + i] != 0:
                    return False

        elif direction == 4:  # EST
            if y - bateau_len + 1 < 0:
                return False
            for i in range(bateau_len):
                if self.grille[x, y - i] != 0:
                    return False

        return True
    

    #fonction auxiliaire
    def placement(self, x, y, direction, bateau_len, val):
        if direction == 1:  # SUD
            for i in range(bateau_len):
                self.grille[x - i, y] = val

        elif direction == 2:  # NORD
            for i in range(bateau_len):
                self.grille[x + i, y] = val

        elif direction == 3:  # VEST
            for i in range(bateau_len):
                self.grille[x, y + i] = val

        elif direction == 4:  # EST
            for i in range(bateau_len):
                self.grille[x, y - i] = val

    
    def effacer_bateau(self, bateau):
        x, y = bateau.position
        bateau_len = bateau.longueur
        direction = bateau.direction
        self.placement(x, y, direction, bateau_len, 0)
        
        

    def placer_bateau(self, bateau, position, direction):
        self.effacer_bateau(bateau)
        if self.peut_placer(bateau, position, direction):
              # on efface l'ancienne position 
            x, y = position
            bateau_len = bateau.longueur
            id_prefixe = int(str(bateau.id)[0])  # on met juste id du type de bateau
            self.placement(x, y, direction, bateau_len, id_prefixe)
            bateau.position = position
            bateau.direction = direction
        else:
            print(f"Impossible de placer {bateau.nom} ici.")
            self.placer_bateau(bateau,bateau.position,bateau.direction)

    def placer_bateau_positions(self,bateau):
        self.placer_bateau(bateau,bateau.position,bateau.direction)
    
    def place_alea(self, bateau):
        peut_placer = False
        if bateau.status != 0:
            peut_placer = True
        while not peut_placer:
            position = (random.randint(0, self.TAILLE - 1), random.randint(0, self.TAILLE - 1))
            direction = random.randint(1, 4)
            if self.peut_placer(bateau, position, direction):
                self.placer_bateau(bateau, position, direction)
                peut_placer = True
    
    def changer_direction(self, bateau, direction):
        if direction != bateau.direction:
            x, y = bateau.position
            bateau_len = bateau.longueur
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
        # Vérifier si les coordonnées sont dans la grille
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
            
            elif direction == 3:  # VEST
                if bx == x and by <= y < by + bateau_len:
                    return bateau
            
            elif direction == 4:  # EST
                if bx == x and by - bateau_len + 1 <= y <= by:
                    return bateau
        
        # Si aucune correspondance n'a été trouvée, retourner None
        return None


    
    def bouger(self,bateau,nb):
        for i in range(nb):
            direction = random.randint(1,4)
            self.changer_direction(bateau,direction)
            self.affiche_graph()
    
    def bouger_simultanement(self,nb):
        for i in range(nb):
            for bateau in self.bateaux:
                self.bouger(bateau,1)

        
    def affiche(self):
        print(self.grille)

    def affiche_graph(self):
        plt.imshow(self.grille, cmap='jet', origin='lower')  # 'jet' colormap pour plus des couleurs
        plt.colorbar()
        plt.gca().invert_yaxis()  # Invert y-axis to place (0,0) in the bottom-left corner
        plt.title("Grille Display")
        plt.show()
    
    def eq(self, grilleB):
        return np.array_equal(self.grille, grilleB.grille)
    
    def estVide(self):
        return np.array_equal(self.grille, np.zeros((self.TAILLE,self.TAILLE)))
    
    def grille_selecte(self,bateaux):
        self.refresh_grille()
        self.bateaux = bateaux
        self.generer_grille()

    def grille_ancienne(self):
        if not self.estVide():
            return None
        for bateau in self.bateaux:
            self.placer_bateau_positions(bateau)

    def generer_grille(self):
        for bateau in self.bateaux:
            self.place_alea(bateau)

    def refresh_grille(self):
        self.grille = np.zeros((self.TAILLE, self.TAILLE), dtype=int)
    