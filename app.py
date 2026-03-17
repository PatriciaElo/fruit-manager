import streamlit as st
from fruit_manager import *

st.title("🍇​ Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

st.header("💰​ Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📦​ Inventaire")
st.table(inventaire)

# Barre latérale

with st.sidebar:
    st.header("🛒​ Vendre des fruits")
    fruit_vendre = st.selectbox("Choisir un fruit", list(inventaire.keys()))
    quantite_vendre = st.number_input("Quantité à vendre", min_value=1, step=1)

    if st.button("Vendre"):
        inventaire, tresorerie = vendre(
            inventaire, fruit_vendre, quantite_vendre, tresorerie, prix
        )
        st.toast(f"Vous avez vendu {quantite_vendre} unité(s) de {fruit_vendre}​ ☑️​")


# st.sidebar.title("🛒​ Vendre des fruits")
#
# st.sidebar.selectbox("Choisir un fruit", inventaire)
# st.sidebar.number_input(
#    "Quantité à vendre", value=0, min_value=0, max_value=100, step=1
# )
#
## Bouton Vendre
# start_vendre = st.sidebar.button("Vendre")
#
# if start_vendre:
#    st.toast(f"Vous avez vendu {inventaire.value} unités de {inventaire}")
