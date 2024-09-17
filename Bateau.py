
class Bateau:
    ID_LONGUEURS_BATEAUX = {
    'PORTE_AVIONS': (1,5),
    'CROISEUR': (2,4),
    'CONTRE_TORPILLEURS': (3,3),
    'SOUS_MARIN': (4,3),
    'TORPILLEUR': (5,2)
    }
    
    CPT=0

    def __init__(self,nom):
        if nom not in self.ID_LONGUEURS_BATEAUX:
            raise ValueError(f"Le nom du bateau '{nom}' est invalide.")
        
        id_prefixe,longueur = self.ID_LONGUEURS_BATEAUX[nom]
        id = int(str(id_prefixe)+str(Bateau.CPT))

        Bateau.CPT += 1

        self.id = id
        self.nom = nom
        self.longueur = longueur
        self.position = (-1,-1)
    
    
    

    
