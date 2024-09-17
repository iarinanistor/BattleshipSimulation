import Bateau 
import numpy as np
import matplotlib.pyplot as plt
import random

class Grille:
    TAILLE = 10

    def __init__(self):
        self.grille = np.zeros((self.TAILLE,self.TAILLE),dtype=int)
        self.bateux = []
    
    def ajoute_bateau(self,bateau):
        self.bateux.append(bateau)
    
    def peut_placer(self,bateau,position,direction):
        #direction 1 pour NORD
        #direction 2 pour SUD
        #direction 3 pour EST
        #direction 4 pour VEST
        
        len = bateau.longueur
        x,y = position

        if direction == 1 : #NORD
            if x + len > self.TAILLE:
                return False
            for i in range(len):
                if self.grille[x+i,y] != 0:
                    return False
        elif direction == 2 : #SUD
            if x - len < -1:
                return False
            for i in range(len):
                if self.grille[x-i,y] != 0:
                    return False
        elif direction == 3 : #EST
            if y + len > self.TAILLE:
                return False
            for i in range(len):
                if self.grille[x,y+i] != 0:
                    return False
        elif direction == 4 : #VEST
            if y - len < -1:
                return False
            for i in range(len):
                if self.grille[x,y-i] != 0:
                    return False
                
        return True

    def placer_bateau(self, bateau, position, direction):

        if self.peut_placer(bateau,position,direction):
            
            bateau.position = position
            x,y = position
            len = bateau.longueur
            id_prefixe = int(str(bateau.id)[0])  #on met sur la grille juste le nb pour le type de bateau qu'on a

            if direction == 1 : #NORD
                for i in range(len):
                    self.grille[x+i,y] = id_prefixe 
            elif direction == 2 : #SUD
                for i in range(len):
                    self.grille[x-i,y] = id_prefixe
            elif direction == 3 : #EST
                for i in range(len):
                    self.grille[x,y+i] = id_prefixe
            elif direction == 4 : #VEST
                for i in range(len):
                    self.grille[x,y-i] = id_prefixe
        
        else:
            raise ValueError(f"Impossible de placer {bateau.nom} ici.")
    
    def place_alea(self, bateau):
        peut_placer = False
        while not peut_placer:
            position = (random.randint(0,self.TAILLE-1),random.randint(0,self.TAILLE-1))
            direction = random.randint(1,4)
            if self.peut_placer(bateau,position,direction):
                self.placer_bateau(bateau,position,direction)
                peut_placer = True
    
    def affiche(self):
        plt.imshow(self.grille, cmap='jet', origin='lower')  # Use 'jet' colormap for better color differentiation
        plt.colorbar()
        plt.gca().invert_yaxis()  # Invert y-axis to place (0,0) in the bottom-left corner
        plt.title("Grille Display")
        plt.show()
    
    def eq(self, grilleB):
        return np.array_equal(self.grille, grilleB.grille)
    
    def generer_grille(self):
        for bateau in self.bateux :
            self.place_alea(bateau)
    









