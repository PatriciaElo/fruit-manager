import streamlit as st
import matplotlib.pyplot as plt
from fruit_manager import *

st.title("🍇​ Dashboard de la Plantation")

inventaire = ouvrir_inventaire()
prix = ouvrir_prix()
tresorerie = ouvrir_tresorerie()

st.header("💰​ Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("📦​ Inventaire")
# Inventaire sous forme de tableau
st.table(inventaire)
# Inventaire sous forme de graphique
fig, ax = plt.subplots()
# Trier l'inventaire par quantité croissante
inventaire = dict(sorted(inventaire.items(), key=lambda item: item[1], reverse=True))
ax.bar(inventaire.keys(), inventaire.values(), edgecolor="k")
ax.set_xlabel("Fruit")
ax.set_ylabel("Quantité")
ax.set_title("Inventaire")
st.pyplot(fig)


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

    st.header("​🌱​ Récolter des fruits")
    fruit_recolter = st.selectbox(
        "Choisir un fruit à récolter", list(inventaire.keys()), key="recolter"
    )
    quantite_recolter = st.number_input(
        "Quantité à récolter", min_value=1, step=1, key="quantite"
    )

    if st.button("Récolter"):
        inventaire = recolter(inventaire, fruit_recolter, quantite_recolter)
        st.toast(
            f"Vous avez récolté {quantite_recolter} unité(s) de {fruit_recolter}​ ☑️​"
        )
