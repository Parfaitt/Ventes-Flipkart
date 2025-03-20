import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from itertools import combinations
from collections import Counter
import zipfile
import io
import os
import csv
from streamlit_extras.stylable_container import stylable_container
import plotly.figure_factory as ff

# --- Configuration de la page ---
st.set_page_config(
    page_title="Reporting ventes",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- Injection CSS améliorée ----
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .main { background: #f4f6f8; color: #333; }
        
        /* Sidebar avec un nouveau dégradé (violet et rose) */
        .stSidebar { 
            background: linear-gradient(135deg, #780000, #c1121f); 
            color: white; 
            padding: 1rem; 
        }
        
        /* Header avec un nouveau dégradé (orange et rouge) */
        .banking-header {
            background: linear-gradient(135deg, #FF6F61 0%, #FF3B3F 100%);
            padding: 2.5rem; 
            border-radius: 15px; /* Coins plus arrondis */
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Ombre plus prononcée */
        }
        
        /* Style pour les graphiques Plotly */
        .stPlotlyChart { 
            border: none; 
            border-radius: 15px; /* Coins arrondis pour les graphiques */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        }
        
        /* Style pour les DataFrames */
        .dataframe { 
            border-radius: 15px !important; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
        }
        
        /* Style pour les boutons et autres éléments interactifs */
        .stButton>button {
            border-radius: 8px;
            background-color: #FF6F61;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .stButton>button:hover {
            background-color: #FF3B3F;
        }
    </style>
""", unsafe_allow_html=True)

# --- En-tête personnalisé ---
st.markdown("""
    <div class='banking-header'>
        <h1 style='margin:0; font-weight:700;'>📊 Reporting des Ventes Flipkart</h1>
        <p style='opacity:0.9; font-weight:300;'>Analyse interactive et dynamique des ventes</p>
    </div>
""", unsafe_allow_html=True)

# --- Fonction utilitaire pour créer des "metric cards" compactes ---
def metric_card(title, value, bg_color):
    html = f"""
    <div style="
        background-color: {bg_color};
        padding: 15px;
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 3px 5px rgba(0,0,0,0.1);
        ">
        <h4 style="margin: 0; font-weight: 600; font-size: 1rem;">{title}</h4>
        <p style="font-size: 1.5rem; margin: 5px 0 0; font-weight: bold;">{value}</p>
    </div>
    """
    return html

# Chargement du fichier
#os.chdir(r"D:\PROJECT DASHBORD\Sales")
data = pd.read_csv("flipkart_sales.csv", encoding="ISO-8859-1")

# --- Nettoyage & transformation ---
data = data.rename(columns={'Customer Rating': 'Customer_Rating'})
def avis_client(Customer_Rating):
    if Customer_Rating < 3:
        return 'Mauvais'
    elif Customer_Rating <= 3.9:
        return 'Moyen'
    elif Customer_Rating >= 4:
        return 'Bon'
    else:
        return 'inconu'
data['avis']=data['Customer_Rating'].apply(avis_client)

def etatusa(avis):
    if avis == 'Mauvais':
        return 'Floride'
    elif avis =='Moyen':
        return 'Californie'
    elif avis =='Bon':
        return 'Texas'
    else:
        return 'inconu'
COGS=400000
Ca=75213112.74
Dépenses=8000000
Taxes=1500000
Autres=2000000
salaire=10000000
facture=10000000
data['etat']=data['avis'].apply(etatusa)
data['prix_unitaire']= data['Total Sales (INR)'] / data['Quantity Sold']
data['benef']=Ca-Dépenses-Taxes-Autres-salaire-facture
data['profit']= (data['Total Sales (INR)'] - (data['Quantity Sold'] * data['prix_unitaire']))

# --- Filtres dans la barre latérale ---
st.sidebar.header("🔎 Flipark")



# --- Création des onglets ---
tabs = st.tabs(["📊 Vue Globale des ventes", "🔄 Details des ventes"])

# =====================================================
    # Onglet 1 : Vue Globale des ventes
# ======================================================

# Calcul des KPI
with tabs[0]:
    st.subheader("Vue Globale des ventes")
    # -----Date debut date fin --------------------------------------
    col1, col2 = st.columns(2)
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    
    startDate = pd.to_datetime(data["Order Date"]).min()
    endDate = pd.to_datetime(data["Order Date"]).max()
    
    with col1:
        date1 = pd.to_datetime(st.date_input("Date Debut", startDate))
    
    with col2:
        date2 = pd.to_datetime(st.date_input("Date fin", endDate))
    
    data = data[(data["Order Date"] >= date1) & (data["Order Date"] <= date2)].copy()
# fin--------------------------------------------------------------------------
    Total_commande = data["Order ID"].count()
    Chiffre_affaire=data["Total Sales (INR)"].sum()
    Commande_moyenne=data["Total Sales (INR)"].mean().astype(int)
    Total_article_cmde=data["Quantity Sold"].sum()
    


# Affichage dans des metric cards
    col1, col2= st.columns(2)
    col1.markdown(metric_card("Total Commandes", Total_commande, "#780000"), unsafe_allow_html=True)
    col2.markdown(metric_card("Chiffre affaire", f"{Chiffre_affaire:,.2f} USD", "#003049"), unsafe_allow_html=True)

# Ajouter un espace vertical entre les lignes de métriques
    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    col1, col2= st.columns(2)
    col1.markdown(metric_card("Panier moyen", f"{Commande_moyenne:,.2f} USD", "#003049"), unsafe_allow_html=True)
    col2.markdown(metric_card("Total Article Commandés", Total_article_cmde, "#003049"), unsafe_allow_html=True)

    category_df = data.groupby(by=["Category"], as_index=False)["Total Sales (INR)"].sum()
    
    #graphique en bande et secteur
    with col1:
        st.subheader("Ventes par Catégorie")
        fig = px.bar(category_df, x="Category", y="Total Sales (INR)", template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=200)

    with col2:
        st.subheader("Ventes par Etat")
        fig = px.pie(data, values="Total Sales (INR)", names="etat", hole=0.5)
        fig.update_traces(text=data["etat"].astype(str), textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    #Line chart
    data["month_year"] = data["Order Date"].dt.to_period("M")
    st.subheader('Analyse des ventes par mois')
    linechart = pd.DataFrame(data.groupby(data["month_year"].dt.strftime("%Y : %b"))["Total Sales (INR)"].sum()).reset_index()
    fig2 = px.line(linechart, x="month_year", y="Total Sales (INR)", labels={"Total Sales (INR)": "Montant"}, height=500, width=1000, template="gridon")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Evololutions des transactions Moyen de paiement")
    monthly_sales = data.groupby("Payment Method")["Total Sales (INR)"].sum().reset_index()
    fig_month = px.bar(monthly_sales, x="Payment Method", y="Total Sales (INR)",
        text_auto=True,
        color="Total Sales (INR)",
        color_continuous_scale=["#1E90FF", "#4682B4"],
        template="plotly_white")
    fig_month.update_layout(height=330, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_month, use_container_width=True, config={"displayModeBar": False})


    #Create a treem based on region, category, sub-category
    st.subheader("Vue hiérarchique des ventes")
    fig3=px.treemap(data, path=["etat","Category","Product Name"],values="Total Sales (INR)",hover_data=["Total Sales (INR)"],color="Category")
    fig3.update_layout(width=800, height=650)
    st.plotly_chart(fig3,use_container_width=True)
        
# =====================================================
    # Onglet 2 : Details des ventes
# ======================================================
category_df = data.groupby(by=["Category"], as_index=False)["Total Sales (INR)"].sum()
with tabs[1]:
    
# -----Date debut date fin --------------------------------------

# fin--------------------------------------------------------------------------
    Total_profit = data["benef"].sum()
    Chiffre_affaire=data["Total Sales (INR)"].sum()


    # Affichage dans des metric cards
    col3, col4= st.columns(2)
    col3.markdown(metric_card("Chiffre affaire", f"{Chiffre_affaire:,.2f} USD", "#780000"), unsafe_allow_html=True)
    col4.markdown(metric_card("Benefice Net", f"{Total_profit:,.2f} USD", "#003049"), unsafe_allow_html=True)

    
    st.subheader(":point_right: Résumé des ventes")
    cl1, cl2 = st.columns(2)
    with cl1:
        with st.expander("Données par Catégorie"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger les données par Catégorie", data=csv, file_name="Category.csv", mime="text/csv", help='Cliquez ici pour télécharger les données au format CSV')
    
    with cl2:
        with st.expander("Données par Etat"):
            region = data.groupby(by="etat", as_index=False)["Total Sales (INR)"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger les données par Etat", data=csv, file_name="Region.csv", mime="text/csv", help='Cliquez ici pour télécharger les données au format CSV')


    import plotly.figure_factory as ff
    with st.expander("Tableau de résumé"):
        df_sample = data[0:10][["etat", "Category", "Total Sales (INR)", "Quantity Sold"]]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)


    product_df = data.groupby(by=["Product Name"], as_index=False)["Total Sales (INR)"].sum()
    with tabs[1]:
        cl1, cl2= st.columns(2)
        with cl1:
            with st.expander("Données par Produit"):
                st.write(product_df.style.background_gradient(cmap="Blues"))
                csv = product_df.to_csv(index=False).encode('utf-8')
                st.download_button("Télécharger les données produit", data=csv, file_name="Category.csv", mime="text/csv", help='Cliquez ici pour télécharger les données au format CSV')

    with cl2:
        with st.expander("Données par Payment Method"):
            region = data.groupby(by="Payment Method", as_index=False)["Total Sales (INR)"].sum()
            st.write(region.style.background_gradient(cmap="Oranges"))
            csv = region.to_csv(index=False).encode('utf-8')
            st.download_button("Télécharger les données", data=csv, file_name="Region.csv", mime="text/csv", help='Cliquez ici pour télécharger les données au format CSV')




# --- Footer personnalisé ---
st.markdown("""
    <div class="footer">
      <p>
        Développé par <strong>NG0RAN TANOH PARFAIT</strong> – Data Analyst • 
        Retrouvez-moi sur <a href="https://www.linkedin.com/in/tanoh-parfait-n-goran-10410a184/" target="_blank">LinkedIn</a> • 
        Pour suggestions et questions : <a href="mailto:ngorantanohparfait@gmail.com">ngorantanohparfait@gmail.com</a>
      </p>
    </div>
""", unsafe_allow_html=True)



