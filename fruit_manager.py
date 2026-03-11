import json


def ouvrir_inventaire(path="inventaire.json"):
    with open(path, "r", encoding="utf-8") as fichier:
        inventaire = json.load(fichier)
    return inventaire


def ecrire_inventaire(inventaire, path="inventaire.json"):
    with open(path, "w", encoding="utf-8") as fichier:
        json.dump(inventaire, fichier, ensure_ascii=False, indent=4)


def afficher_inventaire(inventaire):
    print("Inventaire actuel de la plantation :")
    for fruit, quantite in inventaire.items():
        print(f"- {fruit.capitalize()} : {quantite} unités.")


def recolter(inventaire, fruit, quantite):
    inventaire[fruit] = inventaire.get(fruit, 0) + quantite
    print(f"\n OK - Récolté {quantite} {fruit} supplémentaires !")


def vendre(inventaire, fruit, quantite):
    if (
        inventaire.get(fruit, 0) >= quantite
    ):  # get ici retourne juste la valeur associée à la clé.
        inventaire[fruit] -= quantite
        print(f"\n Vendu {quantite} {fruit} !")
    else:
        print(f"\n Pas assez de {fruit} pour vendre {quantite} unités.")


if __name__ == "__main__":
    afficher_inventaire(inventaire)
    recolter(inventaire, "bananes", 10)
    vendre(inventaire, "bananes", 5)
    afficher_inventaire(inventaire)
