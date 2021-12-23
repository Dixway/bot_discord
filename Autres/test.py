class Toto:
    def __init__(self, prenom):
        self.nom = prenom
        self.maListe = []

    def getPrenom(self):
        self.maListe.append("toto")
        return self.nom

    def setPrenom(self, prenom):
        self.nom = prenom

    def getListe(self):
        return self.maListe


toto = Toto("victor")

print(toto.getListe())

print(toto.getPrenom())

print(toto.getListe())

toto.setPrenom("sylvain")

print(toto.getPrenom())
