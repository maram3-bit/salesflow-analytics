# ⚡ SalesFlow Analytics

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3D4DB7?style=for-the-badge&logo=plotly)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> Dashboard professionnel d'analyse automatique des ventes — développé dans le cadre du Projet de Fin d'Année 2026.

---

## 🎯 Aperçu

SalesFlow Analytics est une application web interactive qui permet d'analyser automatiquement des données de ventes CSV et de générer des visualisations professionnelles en temps réel.

---

## ✨ Fonctionnalités

- 📊 **Dashboard interactif** avec graphiques Plotly animés
- 🏆 **Classement automatique** des produits en Gold / Silver / Bronze
- 🔍 **Détection d'anomalies** intelligente
- 📁 **Upload de fichiers CSV** directement depuis l'interface
- 🔎 **Recherche en temps réel** dans le tableau des produits
- 💾 **Export CSV** des résultats calculés
- 🎲 **Génération automatique** de données de test

---

## 📈 Graphiques inclus

| Graphique | Description |
|---|---|
| 📊 Bar Chart | CA Net par produit avec catégories Gold/Silver/Bronze |
| 🍩 Donut Chart | Répartition CA Net / TVA / Remises |
| 🏅 Top 10 | Meilleurs produits par CA Net |
| 📈 Area Chart | Évolution CA Brut vs CA Net |

---

## 🧮 Calculs automatiques

| Calcul | Formule |
|---|---|
| CA Brut | Prix × Quantité |
| CA Net | CA Brut × (1 - Remise / 100) |
| TVA | CA Net × 20% |
| CA TTC | CA Net + TVA |

---

## 🗂️ Structure du projet

    pfa_ventes/
    │
    ├── app.py                 # Dashboard Streamlit principal
    ├── config.py              # Configuration globale
    ├── data_generator.py      # Génération des données CSV
    ├── sales_analyzer.py      # Analyse et calculs (POO)
    ├── requirements.txt       # Librairies Python
    ├── .gitignore             # Fichiers ignorés par Git
    └── README.md              # Documentation

---

## 🚀 Installation et lancement

1. Cloner le projet

        git clone https://github.com/TON_USERNAME/salesflow-analytics.git
        cd salesflow-analytics

2. Créer l'environnement virtuel

        python -m venv venv
        venv\Scripts\activate

3. Installer les dépendances

        pip install -r requirements.txt

4. Lancer le dashboard

        streamlit run app.py

5. Ouvrir dans le navigateur

        http://localhost:8501

---

## 🛠️ Technologies utilisées

| Technologie | Utilisation |
|---|---|
| **Python 3.13** | Langage principal |
| **Streamlit** | Interface web interactive |
| **Plotly** | Graphiques interactifs |
| **Pandas** | Analyse et manipulation des données |
| **Matplotlib** | Graphiques additionnels |
| **Git / GitHub** | Versioning et déploiement |

---

## 👨‍💻 Auteur

**[Ton Nom]**
Étudiant en [Ta Filière] — [Ton École]
Projet de Fin d'Année 2026

---

<p align="center">Développé avec ❤️ et Python</p>