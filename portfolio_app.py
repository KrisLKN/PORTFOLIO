import streamlit as st
import os
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Portfolio Professionnel | Kris LOKOUN",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé pour un rendu professionnel (sans emojis, épuré)
st.markdown("""
<style>
    /* Masquer le menu Streamlit par défaut et le footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typographie et couleurs de base */
    html, body, [class*="css"]  {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A; /* Bleu marine pro */
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sub-title {
        font-size: 1.25rem;
        color: #4B5563; /* Gris ardoise */
        margin-bottom: 2rem;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 1rem;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #111827;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E3A8A;
        padding-left: 10px;
    }
    
    .text-body {
        font-size: 1rem;
        color: #374151;
        line-height: 1.6;
        text-align: justify;
    }
    
    .tech-tag {
        display: inline-block;
        background-color: #F3F4F6;
        color: #1F2937;
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid #D1D5DB;
    }
</style>
""", unsafe_allow_html=True)

# Définition des chemins absolus (basés sur votre environnement)
BASE_PATH = r"c:\Users\LOKOUN Kris\Desktop\projects\Prtfolio STREAMLIT"
PROJET_FINAL_PATH = os.path.join(BASE_PATH, "projet_final")
IMAGES_RAPPORT_PATH = os.path.join(PROJET_FINAL_PATH, "IMAGES_RAPPORT")
PBI_PATH = os.path.join(PROJET_FINAL_PATH, "PBI")

# Fonction sécurisée pour charger les images
def load_image(folder, filename):
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

# Sidebar pour la navigation des projets
with st.sidebar:
    st.markdown("<h2 style='color: #1E3A8A; font-weight: 700;'>Mes Projets</h2>", unsafe_allow_html=True)
    st.markdown("---")
    projet_selectionne = st.radio(
        "Sélectionnez un projet à visualiser :",
        ["Composant Décisionnel (SAE 4)"]
        # D'autres projets pourront être ajoutés ici plus tard
    )
    
    st.markdown("---")
    st.markdown("<p style='font-size: 0.8rem; color: #6B7280;'>Portfolio Professionnel<br>Développement Data & BI</p>", unsafe_allow_html=True)


# Contenu principal
if projet_selectionne == "Composant Décisionnel (SAE 4)":
    
    st.markdown("<div class='main-title'>Développement d'une Solution Décisionnelle Complète</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>ETL, Data Warehousing & Visualisation Power BI</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='section-title'>Résumé Exécutif (FR)</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='text-body'>
        Ce projet illustre la conception et la mise en œuvre d'une <b>architecture décisionnelle complète (Business Intelligence)</b> utilisant la suite Microsoft SQL Server Integration Services (SSIS). L'objectif est d'intégrer et de consolider des données issues de sources hétérogènes (ventes multicanales : en ligne et en magasin) pour fournir aux décideurs des indicateurs de performance robustes.<br><br>
        <b>Points clés techniques :</b>
        <ul>
            <li><b>Architecture 3-Tiers :</b> Déploiement d'un pipeline étanche : <b>DSA</b> (Data Staging Area) pour l'extraction brute, <b>ODS</b> (Operational Data Store) pour la consolidation et le nettoyage, et <b>DWH</b> (Data Warehouse) pour la modélisation en étoile.</li>
            <li><b>Modélisation Avancée :</b> Création d'un schéma en étoile pur en évitant les problèmes de flocons. Les dimensions complexes, comme les pistes musicales (albums, artistes, genres) et la résolution des relations Many-to-Many (via une table Bridge pour les Playlists) ont été dénormalisées au sein du DWH.</li>
            <li><b>Gestion de l'historique (SCD Type 2) :</b> Implémentation du Slowly Changing Dimension de Type 2 via SSIS sur le prix des pistes (DIM_PISTE) pour figer et tracer chaque modification de tarif dans le temps.</li>
            <li><b>Analyse Omnicanale Omnisciente :</b> Les ventes 'Online' et 'Store' ont été fusionnées au sein d'une table de fait consolidée (FAIT_VENTE) pour un pilotage centralisé sous Power BI.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-title'>Executive Summary (EN)</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='text-body'>
        This project demonstrates the end-to-end design and implementation of a <b>Business Intelligence architecture</b> using Microsoft SQL Server Integration Services (SSIS). The goal is to integrate and consolidate data from heterogeneous sources (omnichannel sales: online and in-store) to deliver robust performance metrics to decision-makers.<br><br>
        <b>Technical Highlights:</b>
        <ul>
            <li><b>3-Tier Architecture:</b> Deployment of a strict data pipeline: <b>DSA</b> (Data Staging Area) for raw extraction, <b>ODS</b> (Operational Data Store) for consolidation/cleansing, and <b>DWH</b> (Data Warehouse) for final star-schema modeling.</li>
            <li><b>Advanced Modeling:</b> Development of a pure star schema to avoid snowflake limitations. Complex structures (e.g., musical tracks, albums, artists, genres) and Many-to-Many relationships (using a Bridge table for Playlists) were heavily denormalized within the DWH.</li>
            <li><b>Historical Tracking (SCD Type 2):</b> Implementation of Slowly Changing Dimension Type 2 workflows via SSIS on unit prices (DIM_PISTE), tracking pricing evolution dynamically and enabling historically accurate profitability analysis.</li>
            <li><b>Omnichannel Unification:</b> Both 'Online' and 'Store' sales records were successfully merged inside a consolidated Fact Table (FAIT_VENTE) for holistic, centralized reporting using Power BI.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='section-title'>Technologies</div>", unsafe_allow_html=True)
        st.markdown("""
        <span class='tech-tag'>SQL Server</span>
        <span class='tech-tag'>SSIS</span>
        <span class='tech-tag'>Power BI</span>
        <span class='tech-tag'>Python</span>
        <span class='tech-tag'>DAX</span>
        <span class='tech-tag'>Star Schema</span>
        <span class='tech-tag'>SCD Type 2</span>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Section 1: Modélisation et Base de données
    st.markdown("<div class='section-title'>1. Modélisation Data Warehouse</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='text-body'>
    Conception d'un modèle en étoile strict. Afin d'éviter les modèles en flocons (Snowflake), la dénormalisation a été privilégiée (par exemple, l'intégration des playlists directement dans la dimension Piste).
    </div>
    """, unsafe_allow_html=True)
    
    img_modele = load_image(IMAGES_RAPPORT_PATH, "MODELE EN ETOILE.png")
    if img_modele:
        st.image(img_modele, caption="Modèle en étoile du Data Warehouse", use_container_width=True)

    # Section 2: Processus ETL
    st.markdown("<div class='section-title'>2. Processus ETL (SSIS) & Historisation</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='text-body'>
    Développement des flux d'intégration de données avec SQL Server Integration Services. Le flux de données traverse trois couches :
    <ul>
        <li><b>DSA (Staging)</b> : Extraction brute des sources de données.</li>
        <li><b>ODS (Operational Data Store)</b> : Nettoyage, typage et préparation.</li>
        <li><b>DWH (Data Warehouse)</b> : Chargement final avec gestion des Slowly Changing Dimensions (SCD Type 2) pour tracer l'évolution des prix unitaires.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        img_etl = load_image(IMAGES_RAPPORT_PATH, "RUN_ALL_ETL.png")
        if img_etl:
            st.image(img_etl, caption="Orchestration via le Master Package SSIS", use_container_width=True)
            
        img_ods = load_image(IMAGES_RAPPORT_PATH, "LOAD_ODS_TRACK.png")
        if img_ods:
            st.image(img_ods, caption="Data Flow d'alimentation (Derived Column, Lookup)", use_container_width=True)

    with col_img2:
        img_scd = load_image(IMAGES_RAPPORT_PATH, "RESULTAT_SCD2_SSMS_SIMPLE.png")
        if img_scd:
            st.image(img_scd, caption="Validation SQL Server du Slowly Changing Dimension", use_container_width=True)
            
        img_fait = load_image(IMAGES_RAPPORT_PATH, "DESTINATION_INVOICELINE.png")
        if img_fait:
            st.image(img_fait, caption="Consolidation Omnicanale de la Table de Fait", use_container_width=True)

    # Section 3: Visualisation & Reporting
    st.markdown("<div class='section-title'>3. Analyse Métier (Power BI)</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='text-body'>
    Restitution des données traduite par un rapport interactif Power BI articulé autour de plusieurs axes analytiques.
    Utilisation de DAX pour générer des métriques fiables et actionnables pour le management.
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    col_pbi1, col_pbi2 = st.columns(2)
    with col_pbi1:
        img_synthese = load_image(PBI_PATH, "SYNTHESE.jpg")
        if img_synthese:
            st.image(img_synthese, caption="Vue de Synthèse Principale", use_container_width=True)
            
        img_client = load_image(PBI_PATH, "Analyse Client.png")
        if img_client:
            st.image(img_client, caption="Dashboard Analyse Client", use_container_width=True)

    with col_pbi2:
        img_ventes = load_image(PBI_PATH, "VENTES.png")
        if img_ventes:
            st.image(img_ventes, caption="Analyse des Ventes & CA", use_container_width=True)

        img_cata = load_image(PBI_PATH, "Catalogue.png")
        if img_cata:
            st.image(img_cata, caption="Analyse du Catalogue", use_container_width=True)

    # Conclusion
    st.markdown("---")
    st.markdown("""
    <div class='text-body' style='text-align: center; font-style: italic; color: #6B7280;'>
    Projet finalisé incluant la génération automatisée d'un rapport de synthèse via scripts Python.
    </div>
    """, unsafe_allow_html=True)
