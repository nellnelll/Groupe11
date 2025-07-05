# app.py – Étape 1 : Importation via DuckDB avec 1 fichier
import streamlit as st
import duckdb

st.set_page_config(page_title="Analyse Achats", layout="wide")
st.title("Étape 1️⃣ – Importation des données")

# Connexion à DuckDB (en mémoire)
@st.cache_resource
def init_db():
    con = duckdb.connect(database=':memory:')
    con.execute("""
        CREATE TABLE shopping AS
        SELECT * FROM read_csv_auto('data/shopping_behavior_updated.csv', header=True)
    """)
    return con

con = init_db()

# Aperçu des données
st.subheader("📄 Données : Comportement d’achat")
df = con.execute("SELECT * FROM shopping LIMIT 10").df()
st.dataframe(df, use_container_width=True)

# Colonnes disponibles
st.markdown("### 🧾 Colonnes disponibles")
columns = con.execute("PRAGMA table_info('shopping')").fetchall()
st.write([col[1] for col in columns])

# app.py – Étape 2 : Nettoyage
import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="Nettoyage des données", layout="wide")
st.title("Étape 2️⃣ – Nettoyage des colonnes et formatage")

# Connexion DuckDB
@st.cache_resource
def init_db():
    con = duckdb.connect(database=':memory:')
    con.execute("""
        CREATE TABLE shopping AS
        SELECT * FROM read_csv_auto('data/shopping_behavior_updated.csv', header=True)
    """)
    return con

con = init_db()

# Charger les données dans pandas pour traitement
df = con.execute("SELECT * FROM shopping").df()

# Étape 1 : Renommage des colonnes (uniformisation)
renaming = {
    "Customer ID": "Customer_ID",
    "Item Purchased": "Item_Purchased",
    "Purchase Amount (USD)": "Purchase_Amount_USD",
    "Review Rating": "Review_Rating",
    "Subscription Status": "Subscription_Status",
    "Payment Method": "Payment_Method",
    "Shipping Type": "Shipping_Type",
    "Discount Applied": "Discount_Applied",
    "Promo Code Used": "Promo_Code_Used",
    "Previous Purchases": "Previous_Purchases",
    "Preferred Payment Method": "Preferred_Payment_Method",
    "Frequency of Purchases": "Frequency_of_Purchases"
}

df.rename(columns=renaming, inplace=True)

# Étape 2 : Suppression des doublons
before = df.shape[0]
df.drop_duplicates(inplace=True)
after = df.shape[0]
nb_doublons = before - after

st.subheader("📁 Types de données")
st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "Colonne", 0: "Type"}))

# Étape 3

