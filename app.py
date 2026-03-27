import streamlit as st
import matplotlib.pyplot as plt
from fruit_manager import *
import matplotlib.dates as mdates
import pandas as pd

st.title("🍇​ Dashboard de la Plantation")

if "inventaire" not in st.session_state:
    st.session_state.inventaire = ouvrir_inventaire()

if "tresorerie" not in st.session_state:
    st.session_state.tresorerie = ouvrir_tresorerie()

if "prix" not in st.session_state:
    st.session_state.prix = ouvrir_prix()

inventaire = st.session_state.inventaire
prix = st.session_state.prix
tresorerie = st.session_state.tresorerie

st.header("💰​ Trésorerie")
st.metric(label="Montant disponible", value=f"{tresorerie:.2f} $")

st.header("Évolution de la trésorerie")
historique = lire_tresorerie_historique()
if historique:

    df = pd.DataFrame(historique).tail(20)  # Dernier 20 points
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    fig, ax = plt.subplots()
    ax.plot(df["timestamp"], df["tresorerie"], marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("Trésorerie (en $)")
    ax.set_title("Évolution de la trésorerie")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M"))
    fig.autofmt_xdate()
    _, mid_col, _ = st.columns([1, 2, 1])
    mid_col.pyplot(fig)
else:
    st.info("Aucune donnée d'historique de trésorerie pour le moment.")

st.header("📦​ Inventaire")
# Inventaire sous forme de tableau
st.table(inventaire)
# Inventaire sous forme de graphique
fig, ax = plt.subplots()
# Trier l'inventaire par quantité croissante
inventaire = dict(sorted(inventaire.items(), key=lambda item: item[1], reverse=True))
ax.bar(inventaire.keys(), inventaire.values(), color="salmon", edgecolor="k")
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
        inventaire, tresorerie, message = vendre(
            inventaire, fruit_vendre, quantite_vendre, tresorerie, prix
        )
        # Mise à jour de la session
        st.session_state.inventaire = inventaire
        st.session_state.tresorerie = tresorerie

        # Sauvegarde fichier
        ecrire_inventaire(inventaire)
        ecrire_tresorerie(tresorerie)

        if message["status"] == "success":
            st.success(message["text"])
            st.toast(
                f"Vous avez vendu {quantite_vendre} unité(s) de {fruit_vendre}​ ☑️​"
            )
        else:
            st.error(message["text"])

    st.header("​🌱​ Récolter des fruits")
    fruit_recolter = st.selectbox(
        "Choisir un fruit à récolter", list(inventaire.keys()), key="recolter"
    )
    quantite_recolter = st.number_input(
        "Quantité à récolter", min_value=1, step=1, key="quantite"
    )

    if st.button("Récolter"):
        inventaire = recolter(inventaire, fruit_recolter, quantite_recolter)
        st.session_state.inventaire = inventaire
        ecrire_inventaire(inventaire)
        st.toast(
            f"Vous avez récolté {quantite_recolter} unité(s) de {fruit_recolter}​ ☑️​"
        )
