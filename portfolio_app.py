import streamlit as st
import os
from PIL import Image

# ----------------- CONFIGURATION -----------------
st.set_page_config(
    page_title="Data Portfolio | Kris LOKOUN",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CSS PROFESSIONNEL -----------------
st.markdown("""
<style>
    /* Masquer le menu Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typographie */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #475569;
        font-weight: 400;
        margin-bottom: 2rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 1rem;
    }

    .section-header {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1E293B;
        margin-top: 2rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .text-body {
        font-size: 1.05rem;
        color: #334155;
        line-height: 1.7;
        text-align: justify;
    }
    
    .card-tech {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: transform 0.2s;
    }
    .card-tech:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #1D4ED8, #3B82F6);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CHEMINS & FONCTIONS -----------------
BASE_PATH = r"c:\Users\LOKOUN Kris\Desktop\projects\Prtfolio STREAMLIT"
PROJET_FINAL_PATH = os.path.join(BASE_PATH, "projet_final")
IMAGES_RAPPORT_PATH = os.path.join(PROJET_FINAL_PATH, "IMAGES_RAPPORT")
PBI_PATH = os.path.join(PROJET_FINAL_PATH, "PBI")

@st.cache_data
def load_image(folder, filename):
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        try:
            return Image.open(path)
        except:
            return None
    return None

# ----------------- CONTENUS MULTILINGUES ET PROFILS -----------------
# Structure : content[lang][expertise]['section']
content = {
    'FR': {
        'Expert': {
            'role': 'Data & BI Engineer',
            'intro_title': '🚀 Ingénierie Décisionnelle & Architecture BI Complète',
            'intro_sub': 'Modélisation en Étoile, ETL 3-Tiers (SSIS) et Dataviz DAX',
            'context': """Ce projet démontre ma capacité à concevoir une architecture décisionnelle robuste de bout en bout. 
            L'objectif : unifier des sources hétérogènes (Bases Online et Magasins) pour alimenter un Data Warehouse en étoile. 
            Le défi technique principal résidait dans le traitement des SCD (Slowly Changing Dimensions) de Type 2 sur les prix et la dénormalisation complexe des hiérarchies musicales (Genres/Artistes/Albums) pour éviter les requêtes Snowflake coûteuses.""",
            
            'archi_title': '⚙️ Pipeline ETL Structuré & Modélisation Data Warehouse',
            'archi_text': """Le flux est orchestré via Microsoft SSIS avec une rigueur absolue :
            <br>• <b>DSA (Data Staging Area)</b> : Extraction brute "iso-source" via OLE DB, limitant les verrous sur la base de production.
            <br>• <b>ODS (Operational Data Store)</b> : Nettoyage, typage strict (conversion <code>DT_I4</code> vers <code>NVARCHAR</code>), et résolution des contraintes d'intégrité avec transformation <i>Lookup</i>.
            <br>• <b>DWH (Data Warehouse)</b> : Insertion/Update massif. Le tracking historique des prix est assuré par un flux SCD Type 2 implémenté nativement, garantissant une absence de distorsion sur les KPIs de Chiffre d'Affaires passés. L'omnicanal (Store + Web) est aggloméré via une opération <i>Union All</i> optimisée dans la table de faits <code>FAIT_VENTES</code>.""",
            
            'viz_title': '📈 Intelligence d\'Affaires : DAX & Power BI',
            'viz_text': """Le reporting n'est pas qu'esthétique, il est analytique. 
            La restitution s'appuie sur un requêtage DAX poussé pour des mesures de Time Intelligence et d'analyse de cohorte. Les relations Many-to-Many formées par les Playlists ont été gérées via une table Bridge directement dans le modèle vertipaq de Power BI, consolidant 5 axes exploratoires : Synthèse CA, Performances Ventes, Analyse Catalogue, Rétention Client, et Efficacité RH.""",
            
            'impact_title': '🎯 Impact Formation & R.O.I Technique',
            'impact_text': """La prise en charge autonome de cet écosystème valide l'acquisition d'un profil <b>Full-Stack BI Engineer</b>.
            De la création des scripts DDL SQL Server (`CREATE TABLE`, relations de clés étrangères) jusqu'à la sécurisation RLS (Row-Level Security) pressentie sur Power BI. L'automatisation du reporting via un script Python confirme ma capacité à fusionner l'ingénierie de données classique avec l'écosystème analytique moderne."""
        },
        'Business': {
            'role': 'Analyste BI & Consultant Data',
            'intro_title': '🚀 Transformer les Données en Décisions Stratégiques',
            'intro_sub': 'Centralisation des Ventes, Fiabilité des indicateurs et Tableaux de Bord Dynamiques',
            'context': """Ce projet illustre ma capacité à centraliser les informations d'une entreprise pour aider la direction à prendre de meilleures décisions. L'objectif était de rassembler les ventes issues des magasins physiques et du site e-commerce dans un entrepôt unique, offrant ainsi une "Vue 360°" infaillible de l'activité.""",
            
            'archi_title': '⚙️ Fiabilisation et Centralisation des Données',
            'archi_text': """Avant de pouvoir analyser les données, il fallait les préparer. J'ai construit un "pipeline" automatisé qui :
            <br>• <b>Extrait</b> les données des logiciels de vente chaque nuit sans les ralentir.
            <br>• <b>Nettoie</b> les erreurs, uniformise les formats et vérifie l'intégrité (par ex: s'assurer qu'une vente est bien reliée à un client existant).
            <br>• <b>Sécurise l'historique</b> : J'ai mis en place un système mémorisant l'évolution des prix de vente dans le temps. Ainsi, si une musique coûtait 0.99€ en 2023 et 1.49€ en 2024, le calcul du chiffre d'affaires reste strictement exact pour chaque période.""",
            
            'viz_title': '📈 Tableaux de Bord pour la Direction (Power BI)',
            'viz_text': """Les données nettoyées alimentent un outil de visualisation interactif. 
            J'ai conçu 5 écrans stratégiques (Synthèse globale, Ventes, Catalogue produit, Fidélité client, Performance des employés). Le Management peut ainsi filtrer dynamiquement les indicateurs pour comprendre d'où vient la croissance, quels sont les produits phares, et comment optimiser les efforts commerciaux.""",
            
            'impact_title': '🎯 Valeur Ajoutée & Compétences',
            'impact_text': """Ce projet m'a permis d'acquérir une double compétence rare :
            Je comprends le besoin métier d'un manager (suivi du CA, rentabilité), et je possède les compétences de développement nécessaires pour aller extraire et nettoyer cette donnée informatiquement. Je suis capable d'industrialiser ces processus pour garantir que l'entreprise dispose d'indicateurs justes, tous les matins, à 100% automatisés."""
        }
    },
    'EN': {
        'Expert': {
            'role': 'Data & BI Engineer',
            'intro_title': '🚀 End-to-End Decision Support System & BI Architecture',
            'intro_sub': 'Star Schema Data Warehousing, 3-Tier ETL (SSIS), and Advanced DAX',
            'context': """This project demonstrates my ability to architect a robust, end-to-end Business Intelligence solution. 
            The objective: consolidate heterogeneous sources (Online and Retail databases) to feed a pristine Star Schema Data Warehouse. 
            The primary technical challenge involved managing Type 2 Slowly Changing Dimensions (SCD) for dynamic pricing and heavily denormalizing musical hierarchies (Genres/Artists/Albums) to prevent expensive snowflake queries.""",
            
            'archi_title': '⚙️ Structured ETL Pipeline & DWH Modeling',
            'archi_text': """The data pipeline is fully orchestrated via Microsoft SSIS following strict industry standards:
            <br>• <b>DSA (Data Staging Area)</b>: Raw, 1:1 extraction using OLE DB, minimizing locks on production servers.
            <br>• <b>ODS (Operational Data Store)</b>: Cleansing, strict data typing (e.g., handling <code>DT_I4</code> to <code>NVARCHAR</code> conversions), and enforcing referential integrity using <i>Lookup</i> transformations.
            <br>• <b>DWH (Data Warehouse)</b>: Bulk Insert/Update. Historical pricing is tracked via a natively implemented SCD Type 2 flow, ensuring zero distortion on historical Revenue KPIs. Omnichannel data (Store + Web) is merged using an optimized <i>Union All</i> within the <code>FAIT_VENTES</code> Fact Table.""",
            
            'viz_title': '📈 Business Intelligence: DAX & Power BI',
            'viz_text': """The reporting layer focuses strictly on analytics. 
            Data delivery relies on advanced DAX querying for Time Intelligence and cohort analysis. The Many-to-Many relationships stemming from Playlists were resolved using a Bridge Table natively inside Power BI's Vertipaq model, driving 5 exploratory axes: Revenue Summary, Sales Performance, Catalog Analytics, Customer Retention, and HR Efficiency.""",
            
            'impact_title': '🎯 Training Impact & Technical R.O.I',
            'impact_text': """Achieving autonomous delivery of this ecosystem validates my profile as a <b>Full-Stack BI Engineer</b>.
            From crafting SQL Server DDL scripts to potential RLS (Row-Level Security) integration in Power BI. Furthermore, automating the final PDF reporting via a targeted Python script proves my capability to seamlessly bridge traditional data engineering with the modern open-source analytical stack."""
        },
        'Business': {
            'role': 'BI Analyst & Data Consultant',
            'intro_title': '🚀 Transforming Raw Data into Strategic Decisions',
            'intro_sub': 'Sales Centralization, Reliable KPIs, and Dynamic Dashboards',
            'context': """This project showcases my ability to centralize corporate data to empower executive decision-making. The goal was to unify sales records from both physical storefronts and e-commerce platforms into a Single Source of Truth, offering a flawless "360° View" of the business operations.""",
            
            'archi_title': '⚙️ Data Centralization & Reliability',
            'archi_text': """Before data could be analyzed, it had to be prepared. I built an automated "pipeline" that:
            <br>• <b>Extracts</b> data from sales software overnight without slowing down the actual stores.
            <br>• <b>Cleanses</b> errors, standardizes formats, and checks structural integrity (e.g., ensuring every sale is linked to a valid customer).
            <br>• <b>Secures Historical Data</b>: I engineered a system that remembers how retail prices evolve over time. If a song cost $0.99 in 2023 and $1.49 in 2024, the revenue calculations remain perfectly accurate for every respective period.""",
            
            'viz_title': '📈 Executive Dashboards (Power BI)',
            'viz_text': """The cleansed data feeds into an interactive visualization engine. 
            I designed 5 strategic screens (Global Summary, Sales, Product Catalog, Customer Loyalty, Employee Performance). Leadership can dynamically filter KPIs to understand growth drivers, identify top-selling products, and optimize sales efforts at a glance.""",
            
            'impact_title': '🎯 Added Value & Acquired Skills',
            'impact_text': """This journey allowed me to develop a rare dual-competency:
            I deeply understand the business needs of a manager (revenue tracking, profitability margins), and I possess the technical development skills to extract and refine that data programmatically. I can industrialize these processes to guarantee the company wakes up to 100% accurate, fully automated KPI reports every single morning."""
        }
    }
}

# ----------------- SIDEBAR INTERACTIVE -----------------
with st.sidebar:
    # Photo de profil
    st.markdown("<br>", unsafe_allow_html=True)
    col_pic1, col_pic2, col_pic3 = st.columns([1, 2, 1])
    with col_pic2:
        img_profile = load_image(BASE_PATH, "Photo de profil.jpeg")
        if img_profile:
            st.image(img_profile, use_container_width=True, format="JPEG", output_format="JPEG")
    
    st.markdown("<h2 style='text-align: center; color: #1E3A8A; font-weight:800; margin-bottom: 0;'>Kris LOKOUN</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Langage Toggle
    lang = st.radio("🌐 Language / Langue :", ["Français (FR)", "English (EN)"])
    L = 'FR' if 'FR' in lang else 'EN'
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Expertise Toggle
    st.markdown(f"**{'🎯 Profil du Visiteur' if L=='FR' else '🎯 Viewer Profile'}**")
    expertise_label = "Expert Data (Technique)" if L == 'FR' else "Data Expert (Technical)"
    business_label = "Décisionnel (Métier)" if L == 'FR' else "Executive (Business)"
    exp_choice = st.radio("Sélection / Selection :", [expertise_label, business_label], label_visibility="collapsed")
    EXP = 'Expert' if 'Expert' in exp_choice else 'Business'
    
    st.markdown(f"<p style='text-align: center; color: #6B7280; font-weight: 600; margin-top:20px;'>{content[L][EXP]['role']}</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    if L == 'FR':
        st.info("💡 **Astuce** : Changez le mode Profil de Visiteur pour voir le discours s'adapter de la technique pure aux enjeux stratégiques !")
    else:
        st.info("💡 **Tip**: Switch the Viewer Profile to see the pitch adapt from pure engineering to executive strategy!")


# ----------------- CONTENU PRINCIPAL -----------------
# Hero Section
st.markdown(f"<div class='hero-title'>{content[L][EXP]['intro_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='hero-subtitle'>{content[L][EXP]['intro_sub']}</div>", unsafe_allow_html=True)

# Tags technos
st.markdown("""
<span class='badge'>Microsoft SQL Server</span>
<span class='badge'>SSIS / ETL</span>
<span class='badge'>Power BI</span>
<span class='badge'>DAX</span>
<span class='badge'>Python</span>
""", unsafe_allow_html=True)

st.markdown(f"<div class='text-body' style='margin-top:20px;'>{content[L][EXP]['context']}</div>", unsafe_allow_html=True)

st.markdown("---")

# Section 1: Pipeline
st.markdown(f"<div class='section-header'>{content[L][EXP]['archi_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body'>{content[L][EXP]['archi_text']}</div>", unsafe_allow_html=True)

# Images pour Pipeline
col_img1, col_img2 = st.columns(2)
with col_img1:
    img_etl = load_image(IMAGES_RAPPORT_PATH, "RUN_ALL_ETL.png")
    if img_etl:
        caption1 = "Orchestration Master Package SSIS" if EXP == 'Expert' else "Pipeline de données automatisé"
        st.image(img_etl, caption=caption1, use_container_width=True)
        
    img_archi = load_image(IMAGES_RAPPORT_PATH, "SUIVI_EVOLUTION PAR_COUCHE.png")
    if img_archi:
        caption2 = "Audit d'Intégration (DSA -> ODS -> DWH)" if EXP == 'Expert' else "Suivi Qualité et Centralisation"
        st.image(img_archi, caption=caption2, use_container_width=True)

with col_img2:
    img_scd = load_image(IMAGES_RAPPORT_PATH, "RESULTAT_SCD2_SSMS_SIMPLE.png")
    if img_scd:
        caption3 = "Slowly Changing Dimension Type 2 (Validé via SQL)" if EXP == 'Expert' else "Sécurisation de l'historique des prix"
        st.image(img_scd, caption=caption3, use_container_width=True)
        
    # Logos Outils
    st.markdown("<br><b>Outils / Tools :</b>", unsafe_allow_html=True)
    col_logo1, col_logo2, col_logo3 = st.columns(3)
    
    logo_sql = load_image(IMAGES_RAPPORT_PATH, "logo_sql_server.png")
    if logo_sql: col_logo1.image(logo_sql, width=60)
    
    logo_ssis = load_image(IMAGES_RAPPORT_PATH, "logo_ssis.png")
    if logo_ssis: col_logo2.image(logo_ssis, width=60)
    
    logo_ssms = load_image(IMAGES_RAPPORT_PATH, "logo_ssms.png")
    if logo_ssms: col_logo3.image(logo_ssms, width=60)


st.markdown("---")

# Section 2: Dataviz
st.markdown(f"<div class='section-header'>{content[L][EXP]['viz_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body'>{content[L][EXP]['viz_text']}</div><br>", unsafe_allow_html=True)

# Affichage optimal des dashboards
col_dash1, col_dash2 = st.columns(2)
with col_dash1:
    img_syn = load_image(PBI_PATH, "SYNTHESE.jpg")
    if img_syn:
        st.image(img_syn, caption="Executive Dashboard - Synthèse", use_container_width=True)
        
    img_cli = load_image(PBI_PATH, "Analyse Client.png")
    if img_cli:
        st.image(img_cli, caption="Insights Client (Fidélisation)", use_container_width=True)

with col_dash2:
    img_ven = load_image(PBI_PATH, "VENTES.png")
    if img_ven:
        st.image(img_ven, caption="Analyse des Ventes", use_container_width=True)

    img_cat = load_image(PBI_PATH, "Catalogue.png")
    if img_cat:
        st.image(img_cat, caption="Analyse du Catalogue Produit", use_container_width=True)

st.markdown("---")

# Section 3: Impact
st.markdown(f"<div class='section-header'>{content[L][EXP]['impact_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body'>{content[L][EXP]['impact_text']}</div>", unsafe_allow_html=True)

st.markdown("<br><br><p style='text-align:center; color:#94A3B8; font-size: 0.9rem;'>Portfolio développé avec Streamlit Python.</p>", unsafe_allow_html=True)
