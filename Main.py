from Bateau import Bateau 
from Grille import Grille

#g = Grille()
b1 = Bateau('PORTE_AVIONS')
b2 = Bateau('CONTRE_TORPILLEURS')
b3 = Bateau('TORPILLEUR')

print(b1.id)
print(b1.position)
print(b2.id)

g = Grille()
g.ajoute_bateau(b1)
print("bateau ajoute")

g.ajoute_bateau(b2)
g.ajoute_bateau(b3)
g.generer_grille()
print(b1.position)
g.affiche()

