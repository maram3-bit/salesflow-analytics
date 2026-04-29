# ============================================================
#  app.py — Dashboard SalesFlow Analytics (Streamlit)
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from data_generator import DataGenerator
from sales_analyzer import SalesAnalyzer
from config import INPUT_CSV, OUTPUT_CSV, TVA_RATE

# ── Configuration de la page ─────────────────────────────────
st.set_page_config(
    page_title="SalesFlow Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS personnalisé ─────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0d0d0d; }
    .stApp { background-color: #0d0d0d; }
    
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #00E5FF33;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,229,255,0.1);
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00E5FF;
        margin: 8px 0;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-gold .kpi-value { color: #FFD93D; }
    .kpi-red  .kpi-value { color: #FF6B6B; }
    .kpi-green .kpi-value { color: #6BCB77; }

    .title-main {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00E5FF, #7B2FBE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .section-title {
        color: #00E5FF;
        font-size: 1.3rem;
        font-weight: 700;
        border-left: 4px solid #00E5FF;
        padding-left: 12px;
        margin: 2rem 0 1rem;
    }
    .badge-gold   { background:#FFD93D22; color:#FFD93D;
                    padding:4px 12px; border-radius:20px; font-size:0.8rem; }
    .badge-silver { background:#C0C0C022; color:#C0C0C0;
                    padding:4px 12px; border-radius:20px; font-size:0.8rem; }
    .badge-bronze { background:#CD7F3222; color:#CD7F32;
                    padding:4px 12px; border-radius:20px; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)


# ── Fonctions utilitaires ────────────────────────────────────
def classifier_produit(ca_net, q1, q3):
    if ca_net >= q3:
        return "🥇 Gold"
    elif ca_net >= q1:
        return "🥈 Silver"
    else:
        return "🥉 Bronze"

def detecter_anomalies(df):
    anomalies = []
    mean = df['CA_Net'].mean()
    std  = df['CA_Net'].std()
    for _, row in df.iterrows():
        if row['Remise'] >= 25:
            anomalies.append(f"⚠️ Produit {int(row['ID'])} : remise élevée ({row['Remise']}%)")
        if row['CA_Net'] > mean + 2 * std:
            anomalies.append(f"🚀 Produit {int(row['ID'])} : CA exceptionnel ({row['CA_Net']:,.0f} DT)")
        if row['CA_Net'] < mean - 2 * std:
            anomalies.append(f"🔴 Produit {int(row['ID'])} : CA très faible ({row['CA_Net']:,.0f} DT)")
    return anomalies

def charger_donnees(filepath):
    try:
        
        analyzer = SalesAnalyzer(filepath)
        
        
        if analyzer.df.empty:
            st.warning("⚠️ Le fichier CSV est vide.")
            return analyzer.df, {
                'ca_total': 0, 'tva_totale': 0, 'top_id': "N/A", 
                'top_ca': 0, 'nb_produits': 0
            }
            
        
        analyzer.run_all()
        df = analyzer.df
        
        
        q1 = df['CA_Net'].quantile(0.33) if not df.empty else 0
        q3 = df['CA_Net'].quantile(0.66) if not df.empty else 0
        
        df['Categorie'] = df['CA_Net'].apply(lambda x: classifier_produit(x, q1, q3))
        return df, analyzer.get_summary()

    except Exception as e:
        # Cas 3 : Le fichier est totalement illisible (ex: un JPG renommé en CSV)
        st.error(f"❌ Erreur de lecture : Le fichier est mal formé ou vide.")
        return pd.DataFrame(), None


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ SalesFlow")
    st.markdown("---")
    st.markdown("### 📁 Source des données")

    source = st.radio("", ["Générer automatiquement", "Uploader un CSV"])

    if source == "Générer automatiquement":
        nb = st.slider("Nombre de produits", 10, 200, 50)
        if st.button("🔄 Générer", use_container_width=True):
            gen = DataGenerator(nb_produits=nb)
            gen.generer_csv()
            st.success(f"✅ {nb} produits générés !")
            st.rerun()

    else:
        uploaded = st.file_uploader("Choisir un fichier CSV", type="csv")
        if uploaded:
            with open(INPUT_CSV, 'wb') as f:
                f.write(uploaded.read())
            st.success("✅ Fichier uploadé !")
            st.rerun()

    st.markdown("---")
    st.markdown("### 🎨 Affichage")
    show_table    = st.checkbox("Tableau détaillé", value=True)
    show_anomalies = st.checkbox("Anomalies", value=True)
    st.markdown("---")
    st.markdown("### 📤 Export")
    if st.button("💾 Exporter CSV", use_container_width=True):
        if os.path.exists(OUTPUT_CSV):
            with open(OUTPUT_CSV, 'rb') as f:
                st.download_button("⬇️ Télécharger", f,
                                   file_name="resultats_final.csv",
                                   mime="text/csv",
                                   use_container_width=True)


# ── Contenu principal ────────────────────────────────────────
st.markdown('<h1 class="title-main">⚡ SalesFlow Analytics</h1>',
            unsafe_allow_html=True)
st.markdown('<p class="subtitle">Dashboard professionnel d\'analyse des ventes</p>',
            unsafe_allow_html=True)

if not os.path.exists(INPUT_CSV):
    st.info("👈 Commence par générer un fichier depuis la sidebar !")
    st.stop()

# Chargement
df, summary = charger_donnees(INPUT_CSV)

# ── KPI Cards ────────────────────────────────────────────────
st.markdown('<p class="section-title">📊 Indicateurs Clés</p>',
            unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Produits analysés</div>
        <div class="kpi-value">{summary['nb_produits']}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">CA Total Net</div>
        <div class="kpi-value">{summary['ca_total']:,.0f} DT</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""<div class="kpi-card kpi-red">
        <div class="kpi-label">TVA Totale (20%)</div>
        <div class="kpi-value">{summary['tva_totale']:,.0f} DT</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""<div class="kpi-card kpi-gold">
        <div class="kpi-label">Meilleur Produit</div>
        <div class="kpi-value">ID {summary['top_id']}</div>
        <div class="kpi-label">{summary['top_ca']:,.0f} DT</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Graphiques Row 1 ─────────────────────────────────────────
st.markdown('<p class="section-title">📈 Analyse Visuelle</p>',
            unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    color_map = {"🥇 Gold": "#FFD93D",
                 "🥈 Silver": "#C0C0C0",
                 "🥉 Bronze": "#CD7F32"}
    fig1 = px.bar(
        df, x='ID', y='CA_Net', color='Categorie',
        color_discrete_map=color_map,
        title="CA Net par Produit",
        template="plotly_dark",
        labels={'CA_Net': 'CA Net (DT)', 'ID': 'ID Produit'}
    )
    fig1.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16,
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    ca_net  = df['CA_Net'].sum()
    tva     = df['TVA'].sum()
    remises = (df['CA_Brut'] - df['CA_Net']).sum()
    fig2 = go.Figure(go.Pie(
        labels=['CA Net', 'TVA', 'Remises accordées'],
        values=[ca_net, tva, remises],
        hole=0.55,
        marker=dict(colors=['#00E5FF', '#FFD93D', '#FF6B6B'],
                    line=dict(color='#111', width=2)),
    ))
    fig2.update_layout(
        title="Répartition Financière",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16,
        annotations=[dict(text=f"{ca_net:,.0f}<br>DT",
                          x=0.5, y=0.5, font_size=14,
                          font_color='#00E5FF', showarrow=False)]
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Graphiques Row 2 ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    top10 = df.nlargest(10, 'CA_Net').sort_values('CA_Net')
    fig3  = px.bar(
        top10, x='CA_Net', y=top10['ID'].astype(str),
        orientation='h',
        title="🏆 Top 10 Produits",
        template="plotly_dark",
        color='CA_Net',
        color_continuous_scale=['#FF6B6B', '#FFD93D', '#00E5FF'],
        labels={'CA_Net': 'CA Net (DT)', 'y': 'ID Produit'}
    )
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=df['ID'], y=df['CA_Net'],
        fill='tozeroy',
        fillcolor='rgba(0,229,255,0.1)',
        line=dict(color='#00E5FF', width=2),
        mode='lines+markers',
        marker=dict(size=5, color='#FFD93D'),
        name='CA Net'
    ))
    fig4.add_trace(go.Scatter(
        x=df['ID'], y=df['CA_Brut'],
        line=dict(color='#FF6B6B', width=1.5, dash='dot'),
        mode='lines',
        name='CA Brut'
    ))
    fig4.update_layout(
        title="Évolution CA Brut vs Net",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_size=16
    )
    st.plotly_chart(fig4, use_container_width=True)

# ── Anomalies ────────────────────────────────────────────────
if show_anomalies:
    st.markdown('<p class="section-title">🔍 Détection d\'Anomalies</p>',
                unsafe_allow_html=True)
    anomalies = detecter_anomalies(df)
    if anomalies:
        cols = st.columns(2)
        for i, a in enumerate(anomalies):
            cols[i % 2].info(a)
    else:
        st.success("✅ Aucune anomalie détectée !")

# ── Tableau ──────────────────────────────────────────────────
if show_table:
    st.markdown('<p class="section-title">📋 Tableau Détaillé</p>',
                unsafe_allow_html=True)
    search = st.text_input("🔍 Rechercher un produit par ID")
    df_show = df[df['ID'].astype(str).str.contains(search)] if search else df
    st.dataframe(
        df_show[['ID','Prix','Quantite','Remise',
                 'CA_Brut','CA_Net','TVA','CA_TTC','Categorie']],
        use_container_width=True,
        height=400
    )

st.markdown("---")
st.markdown("<center><small>⚡ SalesFlow Analytics — Projet PFA 2026</small></center>",
            unsafe_allow_html=True)