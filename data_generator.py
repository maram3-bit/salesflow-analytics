# ============================================================
#  data_generator.py — Génération du fichier ventes.csv
# ============================================================

import csv
import random
import os
from config import (INPUT_CSV, NB_PRODUITS, PRIX_MIN, PRIX_MAX,
                    QTE_MIN, QTE_MAX, REMISE_MAX, GRAPHS_DIR)

class DataGenerator:

    def __init__(self, nb_produits=NB_PRODUITS):
        self.nb_produits = nb_produits
        self.filepath    = INPUT_CSV

    def generer_ligne(self, id_produit):
        prix    = round(random.uniform(PRIX_MIN, PRIX_MAX), 2)
        qte     = random.randint(QTE_MIN, QTE_MAX)
        remise  = random.choice([0, 0, 5, 10, 15, 20, REMISE_MAX])
        return [id_produit, prix, qte, remise]

    def generer_csv(self):
        # Crée le dossier graphs/ si il n'existe pas
        os.makedirs(GRAPHS_DIR, exist_ok=True)

        with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Prix', 'Quantite', 'Remise'])
            for i in range(101, 101 + self.nb_produits):
                writer.writerow(self.generer_ligne(i))

        print(f"✅ Fichier '{self.filepath}' généré avec {self.nb_produits} produits.")

    def afficher_apercu(self):
        print("\n📋 Aperçu des 5 premières lignes :")
        print(f"{'ID':<8} {'Prix':<10} {'Quantite':<12} {'Remise'}")
        print("-" * 40)
        with open(self.filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i == 5:
                    break
                print(f"{row['ID']:<8} {row['Prix']:<10} {row['Quantite']:<12} {row['Remise']}%")


# ── Test direct du fichier ──────────────────────────────────
if __name__ == "__main__":
    gen = DataGenerator()
    gen.generer_csv()
    gen.afficher_apercu()