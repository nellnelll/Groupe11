# app.py

import streamlit as st
import duckdb
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Configuration Streamlit
st.set_page_config(page_title="Analyse Achat - Groupe11", layout="wide")
st.title("🛍️ Analyse du Comportement d’Achat avec DuckDB")

# Charger les données avec DuckDB
@st.cache_data
def load_data():
    con = duckdb.connect(database=':memory:')
    con.execute("""
        CREATE TABLE shopping AS
        SELECT * FROM read_csv_auto('data/shopping_behavior_updated.csv', header=True)
    """)
    con.execute("""
        CREATE TABLE states AS
        SELECT "US State" AS US_State, "Population 2024" AS Population_2024
        FROM read_csv_auto('data/US_States_Ranked_by_Population_2024.csv', header=True)
    """)
    return con

# Connexion DuckDB
con = load_data()

# Nettoyage des noms de colonnes (DuckDB ne supporte pas rename dans-place)
df = con.execute("SELECT * FROM shopping").df()
rename_map = {
    "Customer ID": "Customer_ID",
    "Purchase Amount (USD)": "Purchase_Amount_USD",
    "Review Rating": "Review_Rating",
    "Subscription Status": "Subscription_Status",
    "Promo Code Used": "Promo_Code_Used",
    "Item Purchased": "Item_Purchased",
    "Shipping Type": "Shipping_Type",
    "Previous Purchases": "Previous_Purchases",
    "Payment Method": "Payment_Method",
    "Frequency of Purchases": "Frequency_of_Purchases"
}
df.rename(columns=rename_map, inplace=True)

# Réaffectation table nettoyée
con.execute("DROP TABLE IF EXISTS shopping_cleaned")
con.register("shopping_cleaned", df)

# Aperçu des données
st.subheader("📄 Aperçu des données")
st.dataframe(df.head(), use_container_width=True)

# Visualisation 1 : Répartition par genre
st.subheader("1️⃣ Répartition des clients par genre")
gender_df = con.execute("""
    SELECT Gender, COUNT(*) AS total
    FROM shopping_cleaned
    GROUP BY Gender
""").df()

fig1, ax1 = plt.subplots()
sns.barplot(data=gender_df, x="Gender", y="total", ax=ax1)
ax1.set_title("Distribution Genre")
st.pyplot(fig1)

# Visualisation 2 : Montant moyen par genre
st.subheader("2️⃣ Montant moyen des achats par genre")
mean_purchase_df = con.execute("""
    SELECT Gender, AVG(Purchase_Amount_USD) AS Mean_Purchase
    FROM shopping_cleaned
    GROUP BY Gender
""").df()

fig2, ax2 = plt.subplots()
sns.barplot(data=mean_purchase_df, x="Gender", y="Mean_Purchase", ax=ax2)
ax2.set_title("Montant moyen par genre")
st.pyplot(fig2)

# Visualisation 3 : Répartition par catégorie
st.subheader("3️⃣ Répartition des catégories par genre")
cat_df = con.execute("""
    SELECT Category, Gender, COUNT(*) AS Count
    FROM shopping_cleaned
    GROUP BY Category, Gender
""").df()

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(data=cat_df, x="Category", y="Count", hue="Gender", ax=ax3)
ax3.set_title("Catégories d’achats par genre")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Visualisation 4 : Distribution de l’âge
st.subheader("4️⃣ Distribution de l'âge")
age_df = con.execute("SELECT Age FROM shopping_cleaned").df()

fig4, ax4 = plt.subplots()
sns.kdeplot(data=age_df, x="Age",_
