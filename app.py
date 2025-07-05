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