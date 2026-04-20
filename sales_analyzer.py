# ============================================================
#  sales_analyzer.py — Analyse des ventes (POO)
# ============================================================

import pandas as pd
from config import INPUT_CSV, OUTPUT_CSV, TVA_RATE

class SalesAnalyzer:

    def __init__(self, filepath=INPUT_CSV):
        self.filepath = filepath
        self.df = pd.read_csv(filepath)
        print(f"✅ Fichier '{filepath}' chargé — {len(self.df)} produits.")

    def calculate_ca_brut(self):
        self.df['CA_Brut'] = self.df['Prix'] * self.df['Quantite']

    def apply_remises(self):
        self.df['CA_Net'] = self.df['CA_Brut'] * (1 - self.df['Remise'] / 100)

    def calculate_tva(self):
        self.df['TVA'] = self.df['CA_Net'] * TVA_RATE

    def calculate_ca_ttc(self):
        self.df['CA_TTC'] = self.df['CA_Net'] + self.df['TVA']

    def get_ca_total(self):
        return round(self.df['CA_Net'].sum(), 2)

    def get_tva_totale(self):
        return round(self.df['TVA'].sum(), 2)

    def get_top_product(self):
        idx = self.df['CA_Net'].idxmax()
        return self.df.loc[idx, 'ID'], round(self.df.loc[idx, 'CA_Net'], 2)

    def get_summary(self):
        top_id, top_ca = self.get_top_product()
        return {
            'ca_total'    : self.get_ca_total(),
            'tva_totale'  : self.get_tva_totale(),
            'top_id'      : top_id,
            'top_ca'      : top_ca,
            'nb_produits' : len(self.df),
        }

    def run_all(self):
        self.calculate_ca_brut()
        self.apply_remises()
        self.calculate_tva()
        self.calculate_ca_ttc()

    def export_results(self):
        self.df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print(f"✅ Résultats exportés dans '{OUTPUT_CSV}'.")

    def afficher_resultats(self):
        s = self.get_summary()
        print("\n" + "="*45)
        print("       📊 SALESFLOW — RÉSULTATS FINAUX")
        print("="*45)
        print(f"  Nombre de produits   : {s['nb_produits']}")
        print(f"  CA Total (Net)       : {s['ca_total']} DT")
        print(f"  TVA Totale (20%)     : {s['tva_totale']} DT")
        print(f"  Meilleur produit     : ID {s['top_id']} → {s['top_ca']} DT")
        print("="*45)


# ── Test direct ─────────────────────────────────────────────
if __name__ == "__main__":
    analyzer = SalesAnalyzer()
    analyzer.run_all()
    analyzer.afficher_resultats()
    analyzer.export_results()