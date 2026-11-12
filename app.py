"""
🏨 YIELD MANAGEMENT TOURISM - STREAMLIT APP
===========================================
Système professionnel de yield management pour l'industrie touristique
Basé sur 8+ années d'expérience terrain (2008-2010)
Gestion de €15M+ de contrats avec partenaires premium
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime
from datetime import timedelta

# Configuration de la page
st.set_page_config(
    page_title="🏨 Yield Management Tourism",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .experience-badge {
        background: linear-gradient(45deg, #gold, #ffd700);
        color: #2c3e50;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# Données d'exemple
@st.cache_data
def load_sample_data():
    weekly_perf = pd.DataFrame({
        'semaine': ['S22', 'S23', 'S24', 'S25', 'S26', 'S27'],
        'clics': [2847, 3156, 2734, 3892, 2189, 3245],
        'conversions': [98, 112, 87, 143, 67, 118],
        'taux_conversion': [3.4, 3.5, 3.2, 3.7, 3.1, 3.6],
        'ca_realise': [247500, 289600, 228900, 378200, 187400, 295800],
        'marge': [18.2, 19.1, 16.8, 21.3, 15.2, 18.9]
    })
    
    flight_data = pd.DataFrame({
        'vol': ['AF738', 'TG947', 'QR834', 'EK405', 'GA715'],
        'destination': ['Maldives', 'Thaïlande', 'Maldives', 'Dubai', 'Bali'],
        'places_allouees': [45, 35, 25, 30, 45],
        'places_vendues': [38, 31, 18, 29, 32],
        'places_restantes': [7, 4, 7, 1, 13],
        'prix_achat': [890, 675, 920, 540, 780],
        'prix_vente': [1245, 985, 1189, 789, 1098],
        'marge_pct': [39.8, 45.9, 29.2, 46.1, 40.8]
    })
    
    hotel_data = pd.DataFrame({
        'hotel': ['Oberoi Beach Resort', 'Mercure Koh Samui', 'TBH Luxury Maldives', 
                 'Hilton Dubai Creek', 'Novotel Bali Benoa', 'Shangri-La Bangkok',
                 'Conrad Maldives', 'Sofitel Dubai Palm', 'Four Seasons Bali'],
        'chaine': ['Oberoi Hotels', 'Mercure', 'TBH Hotels', 'Hilton', 'Accor', 
                  'Shangri-La', 'Hilton', 'Accor', 'Four Seasons'],
        'type_contrat': ['Ferme', 'Allotement', 'Ferme', 'Allotement', 'Ferme', 
                        'Allotement', 'Ferme', 'Allotement', 'Ferme'],
        'chambres_semaine': [25, 40, 20, 35, 30, 28, 15, 32, 18],
        'prix_achat': [320, 185, 450, 240, 165, 285, 680, 295, 520],
        'commission': [12, 15, 10, 18, 16, 14, 8, 17, 9],
        'taux_utilisation': [92, 87, 95, 78, 83, 91, 97, 89, 94],
        'performance': ['Excellent', 'Très Bon', 'Excellent', 'Bon', 'Bon', 
                       'Très Bon', 'Excellent', 'Très Bon', 'Excellent']
    })
    
    return weekly_perf, flight_data, hotel_data

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏨 Système de Yield Management Touristique</h1>
    <h3>Optimisation professionnelle des revenus hôteliers</h3>
    <div style="margin-top: 1rem;">
        <span class="experience-badge">8+ Années d'Expérience</span>
        <span class="experience-badge">€15M+ Contrats Gérés</span>
        <span class="experience-badge">9 Hôtels Premium</span>
        <span class="experience-badge">+23% CA</span>
    </div>
    <p style="margin-top: 1rem; font-style: italic;">
        Basé sur mon expérience terrain 2008-2010 en tant que Responsable de Production Touristique<br>
        Partenaires: Oberoi Hotels • Mercure • TBH Hotels • Hilton • Shangri-La
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🎛️ Contrôles Yield Management")

# Chargement des données
weekly_perf, flight_data, hotel_data = load_sample_data()

# Sélection de la vue
view_option = st.sidebar.selectbox(
    "📊 Sélectionner la vue:",
    ["Dashboard Exécutif", "Allocations Vols", "Contrats Hôteliers", "Analytics"]
)

# DASHBOARD EXÉCUTIF
if view_option == "Dashboard Exécutif":
    st.markdown("## 📊 Dashboard Exécutif")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Places Avion", "180", "Contrat Ferme")
    
    with col2:
        st.metric("Hôtels Partenaires", "9", "Premium")
    
    with col3:
        st.metric("CA Mensuel", "€2.3M", "Objectif")
    
    with col4:
        total_utilization = hotel_data['taux_utilisation'].mean()
        st.metric("Taux Remplissage", f"{total_utilization:.0f}%", "Global")
    
    # Graphique performance hebdomadaire
    st.markdown("### 📈 Performance Hebdomadaire")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weekly_perf['semaine'], 
        y=weekly_perf['ca_realise'],
        mode='lines+markers',
        name='Chiffre d\'Affaires (€)',
        line=dict(color='#3498db', width=3)
    ))
    
    fig.update_layout(
        title="Évolution du Chiffre d'Affaires",
        xaxis_title="Semaines",
        yaxis_title="CA (€)",
        height=400
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # Tableau performance
    st.markdown("### 📊 Détail Performance Hebdomadaire")
    st.dataframe(weekly_perf, width="stretch")

# ALLOCATIONS VOLS
elif view_option == "Allocations Vols":
    st.markdown("## ✈️ Gestion des Allocations Vols")
    
    # Métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Places", flight_data['places_allouees'].sum())
    with col2:
        st.metric("Places Vendues", flight_data['places_vendues'].sum())
    with col3:
        efficiency = (flight_data['places_vendues'].sum() / flight_data['places_allouees'].sum()) * 100
        st.metric("Efficacité", f"{efficiency:.1f}%")
    
    # Tableau des allocations
    st.markdown("### 📊 Détail des Allocations")
    st.dataframe(flight_data, width="stretch")
    
    # Graphique de remplissage
    flight_data['taux_remplissage'] = (flight_data['places_vendues'] / flight_data['places_allouees']) * 100
    
    fig_fill = px.bar(
        flight_data, 
        x='vol', 
        y='taux_remplissage', 
        color='taux_remplissage', 
        color_continuous_scale='RdYlGn',
        title="Taux de Remplissage par Vol"
    )
    st.plotly_chart(fig_fill, width="stretch")

# CONTRATS HÔTELIERS
elif view_option == "Contrats Hôteliers":
    st.markdown("## 🏨 Gestion des Contrats Hôteliers")
    
    # Métriques contrats
    col1, col2, col3 = st.columns(3)
    with col1:
        fermes = len(hotel_data[hotel_data['type_contrat'] == 'Ferme'])
        st.metric("Contrats Fermes", fermes)
    with col2:
        allotements = len(hotel_data[hotel_data['type_contrat'] == 'Allotement'])
        st.metric("Allotements", allotements)
    with col3:
        avg_utilization = hotel_data['taux_utilisation'].mean()
        st.metric("Utilisation Moyenne", f"{avg_utilization:.1f}%")
    
    # Tableau des hôtels
    st.markdown("### 🏨 Portfolio Hôteliers")
    st.dataframe(hotel_data, width="stretch")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        fig_util = px.bar(
            hotel_data, 
            x='taux_utilisation', 
            y='hotel', 
            orientation='h', 
            title="Taux d'Utilisation par Hôtel",
            color='taux_utilisation', 
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_util, width="stretch")
    
    with col2:
        contract_counts = hotel_data['type_contrat'].value_counts()
        fig_contracts = px.pie(
            values=contract_counts.values, 
            names=contract_counts.index,
            title="Répartition Types de Contrats"
        )
        st.plotly_chart(fig_contracts, width="stretch")

# ANALYTICS
elif view_option == "Analytics":
    st.markdown("## 📊 Analytics Avancées")
    
    # KPIs avancés
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = weekly_perf['ca_realise'].sum()
        st.metric("Revenus Totaux", f"€{total_revenue:,.0f}")
    
    with col2:
        avg_margin = weekly_perf['marge'].mean()
        st.metric("Marge Moyenne", f"{avg_margin:.1f}%")
    
    with col3:
        conversion_trend = weekly_perf['taux_conversion'].iloc[-1] - weekly_perf['taux_conversion'].iloc[0]
        st.metric("Évolution Conversion", f"{conversion_trend:+.1f}%")
    
    with col4:
        best_hotel = hotel_data.loc[hotel_data['taux_utilisation'].idxmax()]
        st.metric("Top Performer", best_hotel['hotel'][:15])
    
    #  tendances
    st.markdown("### 📈 Analyse des Tendances")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trend = px.scatter(
            weekly_perf, 
            x='conversions', 
            y='marge', 
            size='ca_realise',
            title="Corrélation Conversions vs Marge"
        )
        st.plotly_chart(fig_trend, width="stretch")
    
    with col2:
        dest_performance = flight_data.groupby('destination').agg({
            'marge_pct': 'mean',
            'places_vendues': 'sum'
        }).reset_index()
        
        fig_dest = px.bar(
            dest_performance, 
            x='destination', 
            y='marge_pct',
            title="Marge Moyenne par Destination"
        )
        st.plotly_chart(fig_dest, width="stretch")

# Sidebar - Contexte expérience
st.sidebar.markdown("---")
st.sidebar.markdown("### 💼 Contexte Professionnel")
st.sidebar.markdown("""
**Expérience Terrain 2008-2010:**
- Responsable Production Touristique
- €15M+ contrats annuels gérés
- 180 places avion/semaine
- 9 hôtels premium

**Résultats Démontrés:**
- **+23.8%** Augmentation CA
- **+€580K** Profit additionnel  
- **100%** Liquidation crises stock
- **+2.3%** Amélioration marge Oberoi
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem;">
    <p><strong>🚀 Système Yield Management Tourism</strong></p>
    <p>Développé par Fahima - Responsable Production Touristique (2008-2010)</p>
    <p>GitHub: <a href="https://github.com/Fahima94/yield-management-tourism" target="_blank">yield-management-tourism</a></p>
</div>
""", unsafe_allow_html=True)
