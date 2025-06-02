import streamlit as st

st.set_page_config(
    page_title="Test Deployment",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 Test Yield Management")
st.success("✅ L'application démarre correctement !")

# Test import des dépendances
try:
    import pandas as pd
    import plotly.graph_objects as go
    st.success("✅ Toutes les dépendances sont disponibles")
except ImportError as e:
    st.error(f"❌ Erreur d'import: {e}")
