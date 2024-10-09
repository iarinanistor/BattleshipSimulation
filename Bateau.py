import random

class Bateau:

    # Dictionnaire définissant les longueurs de différents types de bateaux
    ID_LONGUEURS_BATEAUX = {
    'PORTE_AVIONS': (1,5),
    'CROISEUR': (2,4),
    'CONTRE_TORPILLEURS': (3,3),
    'SOUS_MARIN': (4,3),
    'TORPILLEUR': (5,2)
    }
    
    CPT=0 # Variable de classe pour compter le nombre d'instances de bateaux créées

    def __init__(self,nom,position=(-1,-1),direction=-1):
        '''
        Initialiser un nouvel objet bateau
        Args :
            nom (str) : Nom/type du bateau
            position (tuple) : Position initiale du bateau sur la grille
            direction (int) : Direction du bateau, par défaut -1 (non définie)
        '''

        if nom not in self.ID_LONGUEURS_BATEAUX:
            raise ValueError(f"Le nom du bateau '{nom}' est invalide.")
        
        # Récupérer la longueur et générer un ID unique pour le bateau
        id_prefixe,longueur = self.ID_LONGUEURS_BATEAUX[nom]
        id = int(str(id_prefixe)+str(Bateau.CPT))

        Bateau.CPT += 1

        self.id = id
        self.nom = nom
        self.longueur = longueur
        self.position = position
        self.direction = direction 
        self.status = 0  # Statut du bateau : 0 (ok), 1 (touché), 2 (coulé)
        self.touche = [False]*self.longueur # Liste pour suivre les coups portés au bateau
    
    def set_position_direction(self,position,direction):
        '''
        Méthode pour mettre à jour la position et la direction du bateau
        '''
        self.position = position
        self.direction = direction
    
    def est_coule(self):
        '''
        Méthode pour vérifier si le bateau est coulé
        Returns:
            True si est coulé, False sinon
        '''
        return all(self.touche)
    
    def reset_status(self,positions_exactes):
        '''
        Méthode pour réinitialiser le statut du bateau
        Args :
            positions_exactes (bool) : Si False, réinitialiser la position et la direction
        '''

        self.status = 0    # Réinitialiser le statut à ok
        self.touche = [False]*self.longueur  # Réinitialiser la liste des coups
        
        if not positions_exactes:
            self.position = (-1,-1)   # Définir la position à invalide
            self.direction = -1  # Définir la direction à non définie

    def print_bateau(self):
        '''
        Méthode pour afficher les détails du bateau
        '''

        print("Bateau",self.id,self.nom, self.position, self.direction,sep=" ")

    def info_bateau(self):
        return f"Bateau {self.id} {self.nom} Position: {self.position} Direction: {self.direction}"
    
    @staticmethod
    def info_bateaux(liste_bateaux):
        st = ''
        for bateau in liste_bateaux:
            st += bateau.info_bateau()+"\t"
        return st
    
    @staticmethod
    def nom_bateaux(liste_bateaux):
        st = ''
        i = 0
        for bateau in liste_bateaux:
            st += f"{i}) {bateau.nom} {bateau.id}\n"
            i += 1
        return st

    @staticmethod
    def generation_aleatoire_bateau(cpt):
        '''
        Méthode statique pour générer une liste de bateaux aléatoires
        Args :
            cpt (int) : Nombre de bateaux à générer
        Returns:
            list[bateau]
        '''
        l=[]
        for _ in range(cpt):
            nb = random.randint(0,4)
            bateau = list(Bateau.ID_LONGUEURS_BATEAUX.keys())[nb]
            l.append(Bateau(bateau))
        return l

