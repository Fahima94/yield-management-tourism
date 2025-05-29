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
import json

# Configuration de la page
st.set_page_config(
    page_title="🏨 Yield Management Tourism",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un look professionnel
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
    .metric-card {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .success-metric {
        background: linear-gradient(135deg, #27ae60, #229954);
    }
    .warning-metric {
        background: linear-gradient(135deg, #f39c12, #d68910);
    }
    .info-metric {
        background: linear-gradient(135deg, #3498db, #2980b9);
    }
    .sidebar-content {
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .alert-critical {
        background: #e74c3c;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-warning {
        background: #f39c12;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .alert-success {
        background: #27ae60;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
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

# Classe pour les algorithmes de yield management
class YieldManagementEngine:
    def __init__(self):
        self.click_threshold = 3.5
        self.conversion_threshold = 2.8
        self.profit_margin_target = 18.0
        
    def calculate_yield_recommendation(self, data):
        """Calcul des recommandations de yield basé sur les données"""
        recommendations = []
        
        for _, row in data.iterrows():
            click_rate = row['taux_clics']
            stock = row['stock']
            current_price = row['prix_actuel']
            
            # Algorithme de recommandation
            if click_rate < self.click_threshold * 0.7 and stock > 20:
                action = "Réduction"
                new_price = current_price * 0.92  # -8%
                impact = "Stimuler la demande"
            elif click_rate > self.click_threshold * 1.3 and stock < 10:
                action = "Augmentation"
                new_price = current_price * 1.08  # +8%
                impact = "Optimiser les revenus"
            else:
                action = "Maintien"
                new_price = current_price
                impact = "Prix optimal"
            
            recommendations.append({
                'produit': row['produit'],
                'action': action,
                'prix_suggere': new_price,
                'impact': impact,
                'confiance': min(abs(click_rate - self.click_threshold) * 20, 95)
            })
        
        return pd.DataFrame(recommendations)

# Initialisation des données de démonstration
@st.cache_data
def load_sample_data():
    """Chargement des données d'exemple basées sur l'expérience terrain"""
    
    # Performance hebdomadaire
    weekly_perf = pd.DataFrame({
        'semaine': ['S22', 'S23', 'S24', 'S25', 'S26', 'S27'],
        'clics': [2847, 3156, 2734, 3892, 2189, 3245],
        'conversions': [98, 112, 87, 143, 67, 118],
        'taux_conversion': [3.4, 3.5, 3.2, 3.7, 3.1, 3.6],
        'ca_realise': [247500, 289600, 228900, 378200, 187400, 295800],
        'marge': [18.2, 19.1, 16.8, 21.3, 15.2, 18.9]
    })
    
    # Allocations de vol
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
    
    # Contrats hôteliers
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
    
    # Données yield management
    yield_data = pd.DataFrame({
        'produit': ['Maldives Premium', 'Thailand Beach', 'Dubai Luxury', 'Bali Culture'],
        'taux_clics': [2.8, 4.2, 3.1, 3.8],
        'stock': [12, 8, 15, 5],
        'prix_actuel': [1890, 1245, 985, 1156],
        'demande': ['Faible', 'Forte', 'Moyenne', 'Forte']
    })
    
    return weekly_perf, flight_data, hotel_data, yield_data

# Header principal avec expérience
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

# Sidebar pour les contrôles
st.sidebar.header("🎛️ Contrôles Yield Management")

# Chargement des données
weekly_perf, flight_data, hotel_data, yield_data = load_sample_data()

# Sélection de la vue
view_option = st.sidebar.selectbox(
    "📊 Sélectionner la vue:",
    ["Dashboard Exécutif", "Allocations Vols", "Contrats Hôteliers", "Yield Management", "Analytics Avancées"]
)

# Paramètres yield management
st.sidebar.markdown("### ⚙️ Paramètres Yield")
click_threshold = st.sidebar.slider("Seuil Taux de Clics (%)", 2.0, 5.0, 3.5, 0.1)
price_adjustment = st.sidebar.slider("Ajustement Prix (%)", 1, 15, 5)

# Filtres temporels
st.sidebar.markdown("### 📅 Filtres Temporels")
date_range = st.sidebar.date_input(
    "Période d'analyse:",
    value=(datetime.date.today() - timedelta(days=30), datetime.date.today()),
    max_value=datetime.date.today()
)

# Instance du moteur yield
yield_engine = YieldManagementEngine()
yield_engine.click_threshold = click_threshold

# DASHBOARD EXÉCUTIF
if view_option == "Dashboard Exécutif":
    st.markdown("## 📊 Dashboard Exécutif")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card info-metric">
            <h3>180</h3>
            <p>Places Avion<br>Contrat Ferme</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card success-metric">
            <h3>9</h3>
            <p>Hôtels<br>Partenaires</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card warning-metric">
            <h3>€2.3M</h3>
            <p>CA Mensuel<br>Objectif</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        total_utilization = hotel_data['taux_utilisation'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_utilization:.0f}%</h3>
            <p>Taux de<br>Remplissage</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique performance hebdomadaire
    st.markdown("### 📈 Performance Hebdomadaire")
    
    fig_weekly = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Chiffre d\'Affaires', 'Taux de Conversion', 'Marge (%)', 'Volume Clics'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # CA
    fig_weekly.add_trace(
        go.Scatter(x=weekly_perf['semaine'], y=weekly_perf['ca_realise'], 
                  mode='lines+markers', name='CA (€)', line=dict(color='#3498db', width=3)),
        row=1, col=1
    )
    
    # Taux de conversion
    fig_weekly.add_trace(
        go.Scatter(x=weekly_perf['semaine'], y=weekly_perf['taux_conversion'], 
                  mode='lines+markers', name='Conv. (%)', line=dict(color='#27ae60', width=3)),
        row=1, col=2
    )
    
    # Marge
    fig_weekly.add_trace(
        go.Scatter(x=weekly_perf['semaine'], y=weekly_perf['marge'], 
                  mode='lines+markers', name='Marge (%)', line=dict(color='#e74c3c', width=3)),
        row=2, col=1
    )
    
    # Clics
    fig_weekly.add_trace(
        go.Bar(x=weekly_perf['semaine'], y=weekly_perf['clics'], 
               name='Clics', marker_color='#f39c12'),
        row=2, col=2
    )
    
    fig_weekly.update_layout(height=600, showlegend=False, title_text="Évolution des KPIs")
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Alertes critiques
    st.markdown("### 🚨 Alertes & Actions Requises")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="alert-critical">
            <strong>🔴 STOCK CRITIQUE</strong><br>
            Conrad Maldives: 3 chambres restantes<br>
            <em>Action: Promotion immédiate recommandée</em>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="alert-warning">
            <strong>🟡 PERFORMANCE FAIBLE</strong><br>
            Novotel Bali: 67% utilisation vs 85% objectif<br>
            <em>Action: Réviser stratégie pricing</em>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="alert-success">
            <strong>🟢 OPPORTUNITÉ</strong><br>
            Oberoi: Négociation +2% commission possible<br>
            <em>Action: Planifier réunion direction</em>
        </div>
        """, unsafe_allow_html=True)

# ALLOCATIONS VOLS
elif view_option == "Allocations Vols":
    st.markdown("## ✈️ Gestion des Allocations Vols")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        destination_filter = st.selectbox("Destination:", ["Toutes"] + list(flight_data['destination'].unique()))
    with col2:
        st.metric("Total Places Allouées", flight_data['places_allouees'].sum())
    
    # Données filtrées
    if destination_filter != "Toutes":
        filtered_flights = flight_data[flight_data['destination'] == destination_filter]
    else:
        filtered_flights = flight_data
    
    # Tableau des allocations
    st.markdown("### 📊 Détail des Allocations")
    
    # Mise en forme du tableau
    display_flights = filtered_flights.copy()
    display_flights['Statut'] = display_flights.apply(lambda row: 
        '🔴 Critique' if row['places_restantes'] <= 3 else
        '🟡 Attention' if row['places_restantes'] <= 10 else
        '🟢 Normal', axis=1)
    
    st.dataframe(
        display_flights[['vol', 'destination', 'places_allouees', 'places_vendues', 
                        'places_restantes', 'prix_vente', 'marge_pct', 'Statut']].rename(columns={
            'vol': 'Vol',
            'destination': 'Destination', 
            'places_allouees': 'Allouées',
            'places_vendues': 'Vendues',
            'places_restantes': 'Restantes',
            'prix_vente': 'Prix Vente (€)',
            'marge_pct': 'Marge (%)'
        }),
        use_container_width=True
    )
    
    # Graphique de remplissage
    st.markdown("### 📈 Taux de Remplissage par Vol")
    
    flight_data['taux_remplissage'] = (flight_data['places_vendues'] / flight_data['places_allouees']) * 100
    
    fig_fill = go.Figure()
    colors = ['#e74c3c' if x < 70 else '#f39c12' if x < 85 else '#27ae60' 
              for x in flight_data['taux_remplissage']]
    
    fig_fill.add_trace(go.Bar(
        x=flight_data['vol'],
        y=flight_data['taux_remplissage'],
        marker_color=colors,
        text=[f"{x:.1f}%" for x in flight_data['taux_remplissage']],
        textposition='auto'
    ))
    
    fig_fill.update_layout(
        title="Taux de Remplissage par Vol",
        xaxis_title="Vol",
        yaxis_title="Taux de Remplissage (%)",
        height=400
    )
    
    st.plotly_chart(fig_fill, use_container_width=True)

# CONTRATS HÔTELIERS
elif view_option == "Contrats Hôteliers":
    st.markdown("## 🏨 Gestion des Contrats Hôteliers")
    
    # Métriques contrats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fermes = len(hotel_data[hotel_data['type_contrat'] == 'Ferme'])
        st.metric("Contrats Fermes", fermes)
    
    with col2:
        allotements = len(hotel_data[hotel_data['type_contrat'] == 'Allotement'])
        st.metric("Allotements", allotements)
    
    with col3:
        avg_utilization = hotel_data['taux_utilisation'].mean()
        st.metric("Taux Utilisation Moyen", f"{avg_utilization:.1f}%")
    
    with col4:
        total_rooms = hotel_data['chambres_semaine'].sum()
        st.metric("Total Chambres/Semaine", total_rooms)
    
    # Tableau des hôtels
    st.markdown("### 🏨 Portfolio Hôteliers")
    
    # Mise en forme avec couleurs
    display_hotels = hotel_data.copy()
    display_hotels['Performance Status'] = display_hotels['performance'].apply(lambda x:
        '🟢 ' + x if x == 'Excellent' else
        '🟡 ' + x if x == 'Très Bon' else
        '🟠 ' + x)
    
    st.dataframe(
        display_hotels[['hotel', 'chaine', 'type_contrat', 'chambres_semaine', 
                       'prix_achat', 'commission', 'taux_utilisation', 'Performance Status']].rename(columns={
            'hotel': 'Hôtel',
            'chaine': 'Chaîne',
            'type_contrat': 'Type Contrat',
            'chambres_semaine': 'Chambres/Sem',
            'prix_achat': 'Prix Achat (€)',
            'commission': 'Commission (%)',
            'taux_utilisation': 'Utilisation (%)'
        }),
        use_container_width=True
    )
    
    # Graphiques de performance
    col1, col2 = st.columns(2)
    
    with col1:
        # Utilisation par hôtel
        fig_util = px.bar(
            hotel_data, 
            x='taux_utilisation', 
            y='hotel', 
            orientation='h',
            title="Taux d'Utilisation par Hôtel",
            color='taux_utilisation',
            color_continuous_scale='RdYlGn'
        )
        fig_util.update_layout(height=400)
        st.plotly_chart(fig_util, use_container_width=True)
    
    with col2:
        # Répartition par type de contrat
        contract_counts = hotel_data['type_contrat'].value_counts()
        fig_contracts = px.pie(
            values=contract_counts.values,
            names=contract_counts.index,
            title="Répartition Types de Contrats"
        )
        fig_contracts.update_layout(height=400)
        st.plotly_chart(fig_contracts, use_container_width=True)

# YIELD MANAGEMENT
elif view_option == "Yield Management":
    st.markdown("## ⚡ Algorithmes de Yield Management")
    
    # Paramètres yield en colonnes
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Seuil Taux Clics", f"{click_threshold}%")
    with col2:
        st.metric("Ajustement Prix", f"±{price_adjustment}%")
    with col3:
        if st.button("🎯 Recalculer Recommandations"):
            st.success("Algorithmes mis à jour !")
    
    # Calcul des recommandations
    recommendations = yield_engine.calculate_yield_recommendation(yield_data)
    
    # Tableau des recommandations
    st.markdown("### 💡 Recommandations Pricing")
    
    # Création du tableau avec mise en forme
    display_reco = pd.merge(yield_data, recommendations, on='produit')
    display_reco['Évolution Prix'] = display_reco.apply(lambda row:
        f"€{row['prix_actuel']} → €{row['prix_suggere']:.0f}", axis=1)
    display_reco['Action Color'] = display_reco['action'].apply(lambda x:
        '🟢' if x == 'Augmentation' else '🔴' if x == 'Réduction' else '🟡')
    
    st.dataframe(
        display_reco[['produit', 'taux_clics', 'stock', 'Évolution Prix', 
                     'Action Color', 'action', 'impact', 'confiance']].rename(columns={
            'produit': 'Produit',
            'taux_clics': 'Taux Clics (%)',
            'stock': 'Stock',
            'Action Color': '🎯',
            'action': 'Action',
            'impact': 'Impact Attendu',
            'confiance': 'Confiance (%)'
        }),
        use_container_width=True
    )
    
    # Simulation d'impact
    st.markdown("### 📊 Simulation d'Impact")
    
    # Calcul impacts
    total_current_revenue = (yield_data['prix_actuel'] * yield_data['stock']).sum()
    total_new_revenue = (recommendations['prix_suggere'] * yield_data['stock']).sum()
    revenue_impact = ((total_new_revenue - total_current_revenue) / total_current_revenue) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CA Actuel", f"€{total_current_revenue:,.0f}")
    with col2:
        st.metric("CA Optimisé", f"€{total_new_revenue:,.0f}")
    with col3:
        st.metric("Impact", f"{revenue_impact:+.1f}%", delta=f"€{total_new_revenue-total_current_revenue:,.0f}")
    
    # Graphique de comparaison
    comparison_data = pd.DataFrame({
        'Produit': yield_data['produit'],
        'Prix Actuel': yield_data['prix_actuel'],
        'Prix Suggéré': recommendations['prix_suggere']
    })
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Prix Actuel',
        x=comparison_data['Produit'],
        y=comparison_data['Prix Actuel'],
        marker_color='lightblue'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Prix Suggéré',
        x=comparison_data['Produit'],
        y=comparison_data['Prix Suggéré'],
        marker_color='darkblue'
    ))
    
    fig_comparison.update_layout(
        title="Comparaison Prix Actuels vs Suggérés",
        xaxis_title="Produits",
        yaxis_title="Prix (€)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

# ANALYTICS AVANCÉES
elif view_option == "Analytics Avancées":
    st.markdown("## 📊 Analytics Avancées & Insights")
    
    # KPIs avancés
    st.markdown("### 🎯 KPIs Stratégiques")
    
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
        efficiency = (flight_data['places_vendues'].sum() / flight_data['places_allouees'].sum()) * 100
        st.metric("Efficacité Globale", f"{efficiency:.1f}%")
    
    # Analyse des tendances
    st.markdown("### 📈 Analyse des Tendances")
    
    # Corrélation performance vs prix
    fig_correlation = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Évolution Margin vs Volume', 'Performance par Destination')
    )
    
    # Scatter plot marge vs volume
    fig_correlation.add_trace(
        go.Scatter(
            x=weekly_perf['conversions'],
            y=weekly_perf['marge'],
            mode='markers+lines',
            name='Marge vs Conversions',
            marker=dict(size=weekly_perf['ca_realise']/10000, color='blue', opacity=0.7)
        ),
        row=1, col=1
    )
    
    # Performance par destination
    dest_performance = flight_data.groupby('destination').agg({
        'marge_pct': 'mean',
        'places_vendues': 'sum'
    }).reset_index()
    
    fig_correlation.add_trace(
        go.Bar(
            x=dest_performance['destination'],
            y=dest_performance['marge_pct'],
            name='Marge Moyenne (%)',
            marker_color='green'
        ),
        row=1, col=2
    )
    
    fig_correlation.update_layout(height=400)
    st.plotly_chart(fig_correlation, use_container_width=True)
    
    # Insights automatiques
    st.markdown("### 🧠 Insights Automatiques")
    
    # Calcul d'insights basés sur les données
    best_hotel = hotel_data.loc[hotel_data['taux_utilisation'].idxmax()]
    worst_performance = weekly_perf.loc[weekly_perf['marge'].idxmin()]
    best_flight = flight_data.loc[flight_data['marge_pct'].idxmax()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **🏆 Top Performer:**  
        {best_hotel['hotel']} ({best_hotel['chaine']})  
        Utilisation: {best_hotel['taux_utilisation']}%
        
        **⚡ Meilleur Vol:**  
        {best_flight['vol']} vers {best_flight['destination']}  
        Marge: {best_flight['m