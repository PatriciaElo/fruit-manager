import json
import os
from datetime import datetime

DATA_DIR = "data"
PRIX_PATH = os.path.join(DATA_DIR, "prix.json")
INVENTAIRE_PATH = os.path.join(DATA_DIR, "inventaire.json")
TRESORERIE_PATH = os.path.join(DATA_DIR, "tresorerie.txt")


def enregistrer_tresorerie_historique(
    tresorerie, fichier="data/tresorerie_history.json"
):
    historique = []
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            try:
                historique = json.load(f)
            except:
                historique = []
    historique.append(
        {"timestamp": datetime.now().isoformat(), "tresorerie": tresorerie}
    )
    with open(fichier, "w") as f:
        json.dump(historique, f)


def lire_tresorerie_historique(fichier="data/tresorerie_history.json"):
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def ouvrir_prix(path=PRIX_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        prix_defaut = {
            "bananes": 2,
            "mangues": 7,
            "ananas": 5,
            "noix de coco": 4,
            "papayes": 3,
        }
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(prix_defaut, fichier, ensure_ascii=False, indent=4)
    with open(path, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def ouvrir_inventaire(path=INVENTAIRE_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        inventaire_defaut = {
            "bananes": 120,
            "mangues": 85,
            "ananas": 45,
            "noix de coco": 60,
            "papayes": 30,
        }
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(inventaire_defaut, fichier, ensure_ascii=False, indent=4)
    with open(path, "r", encoding="utf-8") as fichier:
        inventaire = json.load(fichier)
    return inventaire


def ecrire_inventaire(inventaire, path="data/inventaire.json"):
    with open(path, "w", encoding="utf-8") as fichier:
        json.dump(inventaire, fichier, ensure_ascii=False, indent=4)


def ouvrir_tresorerie(path=TRESORERIE_PATH):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fichier:
            json.dump(1000.0, fichier)
    with open(path, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def ecrire_tresorerie(tresorerie, path="data/tresorerie.txt"):
    with open(path, "w", encoding="utf-8") as fichier:
        json.dump(tresorerie, fichier, ensure_ascii=False, indent=4)


def afficher_tresorerie(tresorerie):
    print(f"\n Trésorerie actuelle : {tresorerie: .2f} $")


def afficher_inventaire(inventaire):
    print("Inventaire actuel de la plantation :")
    for fruit, quantite in inventaire.items():
        print(f"- {fruit.capitalize()} : {quantite} unités.")


def recolter(inventaire, fruit, quantite):
    inventaire[fruit] = inventaire.get(fruit, 0) + quantite
    print(f"\n OK - Récolté {quantite} {fruit} supplémentaires !")
    return inventaire


def vendre(inventaire, fruit, quantite, tresorerie, prix):
    if (
        inventaire.get(fruit, 0) >= quantite
    ):  # get ici retourne juste la valeur associée à la clé.
        inventaire[fruit] -= quantite
        tresorerie += prix.get(fruit, 0) * quantite
        enregistrer_tresorerie_historique(tresorerie)
        print(f"\n Vendu {quantite} {fruit} !")
        return (inventaire, tresorerie)
    else:
        print(f"\n Pas assez de {fruit} pour vendre {quantite} unités.")


def vendre_tout(inventaire, tresorerie, prix):
    print("\n🛒​ Vente de tout l'inventaire :")
    for fruit, quantite in list(inventaire.items()):
        if quantite > 0:
            revenu = prix.get(fruit, 0) * quantite
            tresorerie += revenu
            print(
                f"- {fruit.capitalize()} : vendu {quantite} unités pour {revenu:.2f} $"
            )
            inventaire[fruit] = 0
    return inventaire, tresorerie


def dollar_to_euro(tresorerie):
    taux_de_change = 0.86
    tresorerie_euro = tresorerie * taux_de_change
    return tresorerie_euro


def valeur_stock(inventaire, prix):
    valeur = {}
    for fruit in inventaire:
        quantite = inventaire[fruit]
        prix_unitaire = prix.get(fruit, 0)
        valeur[fruit] = quantite * prix_unitaire
    return valeur


if __name__ == "__main__":
    inventaire = ouvrir_inventaire()
    tresorerie = ouvrir_tresorerie()
    prix = ouvrir_prix()
    afficher_tresorerie(tresorerie)
    afficher_inventaire(inventaire)

    recolter(inventaire, "bananes", 10)
    # notre opération vendre va nous retourner un inventaire et une tresorerie
    inventaire, tresorerie = vendre(inventaire, "bananes", 5, tresorerie, prix)

    ecrire_inventaire(inventaire)
    ecrire_tresorerie(tresorerie)
