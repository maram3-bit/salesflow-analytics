# ============================================================
#  config.py — Configuration globale du projet SalesFlow
# ============================================================

# ── Fichiers
INPUT_CSV   = "ventes.csv"
OUTPUT_CSV  = "resultats_final.csv"
REPORT_HTML = "rapport.html"
GRAPHS_DIR  = "graphs/"

# ── Paramètres financiers
TVA_RATE    = 0.20      # Taux TVA : 20%

# ── Génération des données
NB_PRODUITS = 50
PRIX_MIN    = 5.0
PRIX_MAX    = 500.0
QTE_MIN     = 1
QTE_MAX     = 100
REMISE_MAX  = 30

# ── Style des graphiques
GRAPH_STYLE           = "dark_background"
GRAPH_COLOR_PRIMARY   = "#00E5FF"
GRAPH_COLOR_SECONDARY = "#FF6B6B"
GRAPH_COLOR_ACCENT    = "#FFD93D"
GRAPH_DPI             = 150