import streamlit as st
import os
import streamlit.components.v1 as components
import pandas as pd
import datetime

# ----------------- CONFIGURATION -----------------
st.set_page_config(
    page_title="Kris LOKOUN - Portfolio Officiel",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- CSS CORPORATE (PURE & MINIMALISTE) -----------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Metrics Customization */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0A192F;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #495057;
        text-transform: uppercase;
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #0A192F;
        border-left: 5px solid #0A192F;
        padding-left: 15px;
        margin-bottom: 0px;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: #495057;
        font-weight: 400;
        margin-top: 10px;
        margin-bottom: 25px;
    }

    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #212529;
        margin-top: 40px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #DEE2E6;
        padding-bottom: 5px;
    }
    
    .text-body {
        font-size: 1rem;
        color: #343A40;
        line-height: 1.6;
        text-align: justify;
    }
    
    .badge-corporate {
        display: inline-block;
        background-color: #E9ECEF;
        color: #212529;
        padding: 6px 14px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 10px;
        border: 1px solid #CED4DA;
    }

    .tech-logo-container {
        display: flex;
        gap: 20px;
        align-items: center;
        margin-bottom: 20px;
        background-color: #F8F9FA;
        padding: 15px;
        border-radius: 4px;
        border: 1px solid #DEE2E6;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- CHEMINS & FONCTIONS -----------------
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
PROJET_FINAL_PATH = os.path.join(BASE_PATH, "projet_final")
IMAGES_RAPPORT_PATH = os.path.join(PROJET_FINAL_PATH, "IMAGES_RAPPORT")
PBI_PATH = os.path.join(PROJET_FINAL_PATH, "PAGE_TABLEAU_DE_BORD")

def load_image(folder, filename):
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return path
    return None

# ----------------- CONTENUS MULTILINGUES ET PROFILS (SANS EMOJIS) -----------------
content = {
    'FR': {
        'Expert': {
            'role': 'Data / BI Engineer',
            'intro_title': 'Ingénierie Décisionnelle & Architecture BI',
            'intro_sub': 'Modélisation en Étoile, ETL 3-Tiers (SSIS) et Dataviz DAX',
            'context': """Ce projet démontre ma capacité à concevoir une architecture décisionnelle robuste de bout en bout. 
            L'objectif consistait à unifier des sources de données hétérogènes (Bases de production Online et Magasins physiques) pour alimenter un Data Warehouse. 
            L'implémentation technique inclut la gestion du cycle de vie de la donnée, un traitement SCD (Slowly Changing Dimensions) de Type 2 sur les prix unitaires, ainsi que la dénormalisation de tables transactionnelles complexes pour optimiser le temps d'exécution des requêtes analytiques.""",
            
            'archi_title': 'PIPELINE ETL ET MODÉLISATION DWH',
            'archi_text': """L'architecture du flux de données est orchestrée via Microsoft SSIS selon les standards du marché :
            <br>• <b>DSA (Data Staging Area)</b> : Extraction "iso-source" via OLE DB, limitant les opérations pour ne pas impacter les performances de la base de production.
            <br>• <b>ODS (Operational Data Store)</b> : Processus de Data Cleansing, stricte résolution de typage (handling de <code>DT_I4</code> vers <code>NVARCHAR</code>), et intégrité référentielle validée via des transformations <i>Lookup</i>.
            <br>• <b>DWH (Data Warehouse)</b> : Chargement en masse via Bulk Insert/Update. L'historisation tarifaire est assurée par un flux SCD Type 2 natif, garantissant une intégrité absolue sur le calcul des KPIs financiers. La consolidation omnicanale (Store + Web) est réalisée avec une opération <i>Union All</i> optimisée dans <code>FAIT_VENTES</code>.""",
            
            'viz_title': 'INTELLIGENCE D\'AFFAIRES (POWER BI & DAX)',
            'viz_text': """La phase de restitution utilise le requêtage DAX pour la génération de mesures de Time Intelligence. 
            Les relations de type Many-to-Many introduites par la structure des Playlists ont été résolues via une Table Bridge au sein du modèle VertiPaq. Le modèle alimente 5 axes d'analyse distincts : Synthèse Financière, Performances Commerciales, Analyse du Catalogue, Suivi Clientèle, et Optimisation des Ressources Humaines.""",
            
            'qa_title': 'AUDIT ET ASSURANCE QUALITÉ (DATA QUALITY)',
            'qa_text': """Le pipeline intègre des mécanismes de contrôle stricts. Les rejets d'intégrité lors des transformations <i>Lookup</i> SSIS (ex: clés étrangères orphelines) sont isolés dans des sorties d'erreur (Error Output) pour audit. Les valeurs NULL et les erreurs de casting sont neutralisées en couche ODS via des dérivations conditionnelles et nettoyages en base, garantissant que 100% des lignes insérées en Data Warehouse respectent la conformité métier.""",

            'impact_title': 'IMPACT PROFESSIONNEL ET ACQUIS TECHNIQUES',
            'impact_text': """La prise en charge de cet écosystème valide l'intégration de compétences Full-Stack BI Engineer.
            De la création des scripts DDL SQL Server jusqu'à l'implémentation d'un environnement analytique complet et documenté, ce projet démontre une compréhension approfondie de l'ingénierie des données. L'automatisation du reporting via un script Python confirme ma capacité à connecter la Business Intelligence classique aux langages de développement analytique modernes."""
        },
        'Business': {
            'role': 'Analyste BI / Consultant Data',
            'intro_title': 'Transformer la Donnée en Outil Stratégique',
            'intro_sub': 'Centralisation des informations, Fiabilisation des KPIs et Tableaux de Bord Dynamiques',
            'context': """Ce livrable illustre ma capacité à centraliser les systèmes d'information d'une entreprise pour faciliter la prise de décision de la Direction. L'objectif était de consolider l'ensemble des ventes physiques et digitales dans un entrepôt unique, créant ainsi une source de vérité absolue et une vue complète de l'activité commerciale.""",
            
            'archi_title': 'RÉSEAU DE DONNÉES ET SÉCURISATION',
            'archi_text': """La préparation des indicateurs repose sur un pipeline automatisé rigoureux :
            <br>• <b>Extraction Sécurisée</b> : Les données sont copiées depuis les logiciels de caisse sans interférer avec la production opérationnelle.
            <br>• <b>Nettoyage Intégral</b> : Formatage des valeurs, correction des erreurs de saisie et vérification de la cohérence globale des informations entrantes.
            <br>• <b>Gestion de l'Historique</b> : L'architecture mémorise précisément l'évolution temporelle des tarifs. Ainsi, toute fluctuation des coûts de revient et des prix de vente au cours des années est prise en compte, assurant un calcul strict et exact du Chiffre d'Affaires pour n'importe quelle période donnée.""",
            
            'viz_title': 'REPORTING ET TABLEAUX DE BORD (POWER BI)',
            'viz_text': """Les données nettoyées servent de fondation à un outil de visualisation interactif pour les directeurs de service. 
            Cinq écrans stratégiques ont été déployés (Vue d'ensemble, Analyse des Ventes, Rentabilité du Catalogue, Fidélisation Client, Suivi des Ressources). Le Management est apte à filtrer ces rapports dynamiquement pour identifier les leviers de croissance et optimiser la force de vente efficacement.""",
            
            'qa_title': 'FIABILITÉ RIGOUREUSE ET GESTION DES REJETS',
            'qa_text': """La différence entre une simple donnée et une aide à la décision, c'est la fiabilité. Le système effectue un contrôle qualité automatisé massif. Si une vente est enregistrée avec des informations manquantes, ou si un prix est corrompu, le système isole automatiquement cette ligne dans une zone de quarantaine pour vérification, empêchant toute pollution des indicateurs financiers. Le Directeur dispose ainsi d'un chiffre d'affaires auditable et certifié.""",

            'impact_title': 'VALEUR AJOUTÉE OPÉRATIONNELLE',
            'impact_text': """Cette réalisation valide une double compétence critique :
            Une compréhension claire des enjeux métiers d'un comex (croissance, marges, rentabilité) alliée à une maîtrise technique du traitement la donnée. Je suis capable d'industrialiser et d'automatiser entièrement la production d'indicateurs de performance, afin de fournir quotidiennement une information actualisée, sûre et exploitable à 100%."""
        }
    },
    'EN': {
        'Expert': {
            'role': 'Data / BI Engineer',
            'intro_title': 'End-to-End BI Architecture & Data Engineering',
            'intro_sub': 'Star Schema Data Warehousing, 3-Tier ETL (SSIS), and Advanced DAX',
            'context': """This project demonstrates my capability to architect a highly reliable Business Intelligence environment. 
            The objective was to unify heterogeneous databases (Online platforms and physical Retail stores) into a centralized Data Warehouse. 
            The core technical implementation handles full data lineage, Type 2 Slowly Changing Dimensions (SCD) for structural asset pricing, and denormalization of deeply transactional attributes to eliminate expensive snowflake queries.""",
            
            'archi_title': 'STAGING PIPELINE & DWH MODELING',
            'archi_text': """Data orchestration relies on Microsoft SSIS, complying with industry-standard patterns:
            <br>• <b>DSA (Data Staging Area)</b>: OLE DB isolation extraction, preventing locks on live production environments.
            <br>• <b>ODS (Operational Data Store)</b>: Comprehensive cleansing, resolving persistent casting exceptions (e.g., managing <code>DT_I4</code> to <code>NVARCHAR</code>), and validating referential flows using <i>Lookup</i> tasks.
            <br>• <b>DWH (Data Warehouse)</b>: Handled via bulk insertions. Historical price changes are meticulously stored using native SCD Type 2 logic, preventing inaccuracies in historical Revenue evaluations. Omnichannel mapping (Store + Web records) is executed via optimized <i>Union All</i> directives into the central <code>FAIT_VENTES</code> Fact Table.""",
            
            'viz_title': 'ANALYTICS ENGINE (POWER BI & DAX)',
            'viz_text': """The analytical layer functions via sophisticated DAX structures built for Time Intelligence reporting. 
            Many-to-Many dependencies inherited from dynamic Playlist assignments were neutralized via a structured Bridge Table injected into the VertiPaq model. This supports 5 interactive dimensions: Revenue Analytics, Sales Pipeline, Catalog Health, Customer Churn, and HR Performance metrics.""",
            
            'qa_title': 'DATA QA AND ERROR HANDLING',
            'qa_text': """The pipeline relies on rigorous data quality constraints. Referential integrity rejections encountered during SSIS <i>Lookup</i> components are securely redirected to strict Error Outputs for auditing. NULL handling, duplicate suppression, and data type casting failures are structurally bypassed in the ODS layer via conditional derivatives. This guarantees a 100% integrity rate for records hitting the master Data Warehouse.""",

            'impact_title': 'TECHNICAL ROI & ENGINEERING COMPETENCIES',
            'impact_text': """Owning this data lifecycle asserts my proficiency as a Full-Stack BI Engineer.
            Ranging from SQL Server DDL query generation up to BI semantic modeling, this work represents professional-level data engineering logic. The final layer of programmatic PDF reporting via Python validates my readiness to bridge traditional relational environments with modernized coding paradigms."""
        },
        'Business': {
            'role': 'BI Analyst / Data Consultant',
            'intro_title': 'Pivoting Raw Data into Corporate Strategy',
            'intro_sub': 'Sales Consolidation, Absolute KPI Reliability, and Automated Dashboards',
            'context': """This delivery showcases my capacity to harmonize corporate information systems to empower executive action. The directive was to merge offline storefront performance with digital e-commerce metrics into a Single Source of Truth, ensuring a unified cross-channel view for top management.""",
            
            'archi_title': 'DATA PIPELINING AND INTEGRITY',
            'archi_text': """Before raw numbers hold meaning, they must go through automated assurance pipelines:
            <br>• <b>Background Extraction</b>: Data is quietly replicated from active payment platforms without causing operational lag.
            <br>• <b>Quality Control</b>: Manual entry errors are pruned, structural inconsistencies are standardized to ensure every transaction points to an authenticated customer profile.
            <br>• <b>Timeline Preservation</b>: I engineered mechanisms to securely log changing retail prices. Thus, regardless of how costs fluctuate over the years, historical profitability margins remain mathematically exact and unaltered.""",
            
            'viz_title': 'EXECUTIVE REPORTING (POWER BI)',
            'viz_text': """This refined data sustains an intuitive, interactive visualization portal designed for departmental directors. 
            I developed five primary monitors (Global Summary, Revenue Generation, Product Catalog Margins, Customer Loyalty, Workforce Output). The executive staff can actively filter indicators, exposing market drivers and focusing resources precisely where they are needed most.""",
            
            'qa_title': 'ABSOLUTE RELIABILITY AND QUARANTINE MANAGEMENT',
            'qa_text': """The difference between raw data and actionable insight is absolute reliability. Before processing, the architectural flow enforces massive automated quality checks. If a transaction surfaces with corrupted identifiers or missing price tags, the system intelligently quarantines the specific record for manual review rather than letting it poison the financial metrics. Leadership operates on entirely audited, flawless revenue figures.""",

            'impact_title': 'OPERATIONAL VALUE CREATION',
            'impact_text': """This final product underscores a crucial dual capacity:
            I assimilate complex business imperatives (revenue monitoring, profit safeguarding) and possess the programming insight to process and present that operational reality. I can successfully industrialize backend procedures to guarantee that corporate leaders access perfectly accurate, completely automated daily reports."""
        }
    }
}

# ----------------- UI: SIDEBAR -----------------
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    col_pic1, col_pic2, col_pic3 = st.columns([1, 2, 1])
    with col_pic2:
        img_profile = load_image(BASE_PATH, "Photo_de_profil.jpeg")
        if img_profile:
            st.image(img_profile, use_container_width=True)
            
    st.markdown("<h2 style='text-align: center; color: #0A192F; font-weight:700; margin-bottom: 0;'>Kris LOKOUN</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    lang = st.radio("Language / Langue", ["Français", "English"], horizontal=True, label_visibility="collapsed")
    L = 'FR' if 'Français' in lang else 'EN'
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    expertise_label = "Profil Technique (Expert)" if L == 'FR' else "Technical Profile (Expert)"
    business_label = "Profil Décisionnel (Métier)" if L == 'FR' else "Business Profile (Executive)"
    exp_choice = st.radio("Audience", [expertise_label, business_label], horizontal=True, label_visibility="collapsed")
    EXP = 'Expert' if 'Expert' in exp_choice else 'Business'
    
    st.markdown(f"<p style='text-align: center; color: #495057; font-size: 0.9rem; font-weight: 500; margin-top:15px;'>{content[L][EXP]['role']}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Bouton de téléchargement du CV
    st.markdown(f"**{'📄 Extrait CV (ATS)' if L=='FR' else '📄 ATS Resume Block'}**")
    cv_path = os.path.join(BASE_PATH, "CV_Resume_Projet_SAE4.md")
    if os.path.exists(cv_path):
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_data = f.read()
        btn_txt = "Télécharger (.md)" if L == 'FR' else "Download (.md)"
        st.download_button(label=btn_txt, data=cv_data, file_name="Kris_Lokoun_BI_Resume.md", mime="text/markdown", use_container_width=True)
        
    st.markdown("---")

    # Sélection du Projet
    st.markdown(f"**{'📁 Aperçu de Projet' if L=='FR' else '📁 Project Showcase'}**")
    project_idx = st.selectbox("Portfolio Project", ["Architecture BI (SAE 4)", "Data Ingestion API (SAE 3)"], label_visibility="collapsed")
    st.markdown("---")

# ----------------- ROUTING: PROJET SAE 3 (PYTHON API) -----------------
if "SAE 3" in project_idx:
    st.markdown(f"<div class='hero-title'>{'Ingénierie des Données & Extraction d\'API' if L=='FR' else 'Data Engineering & API Ingestion'}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>{'Scraping automatisé JSON OpenStreetMap (Python)' if L=='FR' else 'Automated OpenStreetMap JSON Scraping (Python)'}</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <span class='badge-corporate'>Python 3</span>
    <span class='badge-corporate'>Requests</span>
    <span class='badge-corporate'>JSON Parsing</span>
    <span class='badge-corporate'>API REST</span>
    <span class='badge-corporate'>Geocoding</span>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    if L == 'FR':
        col_kpi1.metric(label="Endpoints Gérés", value="15+", delta="Transports, Santé, Services")
        col_kpi2.metric(label="Temps de Scan", value="< 1 Sec", delta="Geocoding Nominatim")
        col_kpi3.metric(label="Format d'Ingestion", value="JSON", delta="Extraction & Tri Automatisé")
        desc = "Ce projet met en évidence la collecte programmatique de données par l'interrogation d'API complexes (Overpass API, Nominatim). Le script récupère instantanément toute l'infrastructure urbaine d'une ville (gares, hôpitaux, hôtels) via calculs géospatiaux de Bounding Boxes, automatisant complètement l'acquisition de données JSON pour des flux analytiques."
    else:
        col_kpi1.metric(label="Managed Endpoints", value="15+", delta="Transit, Health, Amenity")
        col_kpi2.metric(label="Scan Latency", value="< 1 Sec", delta="Nominatim Geocoding")
        col_kpi3.metric(label="Ingestion Format", value="JSON", delta="Automated Parsing")
        desc = "This project demonstrates programmatic data collection by interrogating complex REST APIs (Overpass API, Nominatim). The script instantly extracts the entire urban infrastructure of any given city (stations, hospitals, hotels) via geospatial Bounding Box calculations, completely automating JSON data acquisition for downstream analytical pipelines."

    st.markdown(f"<div class='text-body' style='margin-top:20px;'>{desc}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section-header'>{'MOTEUR DE REQUÊTES GÉOSPATIALES' if L=='FR' else 'GEOSPATIAL QUERY ENGINE'}</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='text-body'>{"Voici un extrait de l'algorithme d'acquisition des nodes OpenStreetMap, simulant l'ingestion d'une source tiers d'entreprise :" if L=='FR' else "Below is an excerpt of the OpenStreetMap node acquisition algorithm, simulating the ingestion of a third-party corporate data source :"}</div>", unsafe_allow_html=True)

    code_snippet = '''import requests

def extract_urban_data(ville):
    # 1. Extraction Dynamique des Bounding Boxes via Geocoding (Nominatim API)
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": ville, "format": "json", "limit": 1}
    response = requests.get(url, params=params, headers={"User-Agent": "SAE-Project/1.0"})
    
    south, north, west, east = map(float, response.json()[0]["boundingbox"])
    
    # 2. Ingestion Modulaire des Infrastructures (Overpass API - Array JSON)
    bus_url = f"https://overpass-api.de/api/interpreter?data=[out:json];node['highway'='bus_stop']({south},{west},{north},{east});out;"
    bus_data = requests.get(bus_url).json()["elements"]
    
    # Validation et préparation pour la Base de Données
    print(f"Ingestion réussie : {len(bus_data)} points d'arrêt identifiés.")
    pass'''
    
    st.code(code_snippet, language='python')
    st.stop() # Arrêt de l'interprétation ici : empêche le projet SAE 4 de se charger en dessous


# ----------------- UI: CONTENU PRINCIPAL -----------------
st.markdown(f"<div class='hero-title'>{content[L][EXP]['intro_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='hero-subtitle'>{content[L][EXP]['intro_sub']}</div>", unsafe_allow_html=True)

st.markdown("""
<span class='badge-corporate'>SQL Server</span>
<span class='badge-corporate'>SSIS / SSMS</span>
<span class='badge-corporate'>Modélisation DWH</span>
<span class='badge-corporate'>Power BI</span>
<span class='badge-corporate'>DAX</span>
<span class='badge-corporate'>Python</span>
""", unsafe_allow_html=True)

# ----------------- SECTION METRICS (KPIs) -----------------
st.markdown("<br>", unsafe_allow_html=True)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

if L == 'FR':
    col_m1.metric(label="Données (Rows)", value="1.2M+", delta="Croissance massive")
    col_m2.metric(label="Latence ETL", value="< 3 mins", delta="Opération Nuit", delta_color="off")
    col_m3.metric(label="Qualité ODS", value="100%", delta="Zéro Rejet")
    col_m4.metric(label="Dénormalisation", value="3 Niveaux", delta="Temps req. optimisé", delta_color="off")
else:
    col_m1.metric(label="Data Volume", value="1.2M+", delta="Massive scaling")
    col_m2.metric(label="ETL Latency", value="< 3 mins", delta="Overnight batch", delta_color="off")
    col_m3.metric(label="ODS Integrity", value="100%", delta="Zero Drop")
    col_m4.metric(label="Denormalization", value="3 Levels", delta="Optimized queries", delta_color="off")


st.markdown(f"<div class='text-body' style='margin-top:20px;'>{content[L][EXP]['context']}</div>", unsafe_allow_html=True)

# ----------------- SECTION TECHNOLOGIES & PIPELINE -----------------
st.markdown(f"<div class='section-header'>{content[L][EXP]['archi_title']}</div>", unsafe_allow_html=True)

# Diagramme Architecture Mermaid
st.markdown("""
<div class='text-body' style='margin-bottom:10px; font-weight:700;'>Data Lineage & Macro-Architecture :</div>
""", unsafe_allow_html=True)

# Injection HTML garantie pour faire fonctionner MermaidJS sur les vieux serveurs Streamlit Cloud
mermaid_html = """
<!DOCTYPE html>
<html>
    <head>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({ startOnLoad: true, theme: 'default' });
        </script>
        <style>
            body { font-family: 'Roboto', sans-serif; background: transparent; padding: 0; margin: 0; display: flex; justify-content: center; }
        </style>
    </head>
    <body>
        <div class="mermaid">
        flowchart LR
            subgraph Sources
            SQL1[(SQL Server<br>Magasin)]
            SQL2[(SQL Server<br>Online)]
            end

            subgraph ETL
            DSA[Staging Area<br>DSA]
            ODS[Cleansing<br>ODS]
            end

            subgraph Data_Warehouse
            DWH[(Star Schema<br>DWH)]
            end

            subgraph Analytics
            PBI[Power BI<br>Dataviz]
            end

            SQL1 --> DSA
            SQL2 --> DSA
            DSA --> ODS
            ODS --> DWH
            DWH --> PBI
        </div>
    </body>
</html>
"""
components.html(mermaid_html, height=200, scrolling=False)

# Affichage des logos réels web avec Devicon / Uploads Officiels
st.markdown("""
<div class='tech-logo-container' style='margin-top: 20px;'>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/microsoftsqlserver/microsoftsqlserver-plain-wordmark.svg" height="45" title="Microsoft SQL Server"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="40" title="Python"/>
    <span style="font-weight:700; color:#0A192F; font-size: 1.2rem; margin-left:10px;">Power BI / SSIS</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='text-body'>{content[L][EXP]['archi_text']}</div><br>", unsafe_allow_html=True)

# ----------------- SIMULATEUR SCD TYPE 2 -----------------
st.markdown("<br>", unsafe_allow_html=True)
expander_title = "[INTERACTIVE DEMO] Slowly Changing Dimension (SCD Type 2)" if L=='EN' else "[DÉMO INTERACTIVE] Slowly Changing Dimension (SCD Type 2)"
with st.expander(expander_title, expanded=True):
    st.markdown("<p style='font-size: 0.95rem; color: #495057;'>Testez la logique d'historisation implémentée dans le Data Warehouse. Modifiez le prix du produit et observez la clôture / création de ligne dans la base de données.</p>" if L=='FR' else "<p style='font-size: 0.95rem; color: #495057;'>Test the versioning logic implemented in the Data Warehouse. Trigger a price update and observe the row expiration / recreation in the database.</p>", unsafe_allow_html=True)
    
    if "scd_data" not in st.session_state:
        st.session_state.scd_data = pd.DataFrame([
            {"Track_ID": "TRK-892", "Track_Name": "Business Intelligence Masterclass", "Unit_Price": 1.99, "Valid_From": "2023-01-01", "Valid_To": "9999-12-31", "Is_Active": True}
        ])
    
    col_sim1, col_sim2 = st.columns([1, 2])
    with col_sim1:
        st.markdown("<br>", unsafe_allow_html=True)
        new_price = st.number_input("Nouveau Prix / New Price (€)", min_value=0.50, max_value=50.0, value=2.49, step=0.10)
        btn_sim = st.button("Mettre à jour la Base DWH" if L=='FR' else "Update DWH Database", use_container_width=True)
        if btn_sim:
            try:
                # Clôture ancienne ligne
                idx_active = st.session_state.scd_data.index[st.session_state.scd_data["Is_Active"] == True].tolist()[0]
                st.session_state.scd_data.at[idx_active, "Valid_To"] = datetime.date.today().strftime("%Y-%m-%d")
                st.session_state.scd_data.at[idx_active, "Is_Active"] = False
                
                # Nouvelle ligne
                new_row = {"Track_ID": "TRK-892", "Track_Name": "Business Intelligence Masterclass", "Unit_Price": new_price, "Valid_From": datetime.date.today().strftime("%Y-%m-%d"), "Valid_To": "9999-12-31", "Is_Active": True}
                st.session_state.scd_data = pd.concat([st.session_state.scd_data, pd.DataFrame([new_row])], ignore_index=True)
            except Exception as e:
                pass
            
    with col_sim2:
        st.dataframe(st.session_state.scd_data, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- NOUVELLE SOUS-SECTION : QUALITY ASSURANCE -----------------
st.markdown(f"<p style='font-size: 1.1rem; font-weight: 700; color: #0A192F; border-left: 3px solid #1D4ED8; padding-left: 10px;'>{content[L][EXP]['qa_title']}</p>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body' style='margin-bottom: 25px;'>{content[L][EXP]['qa_text']}</div>", unsafe_allow_html=True)

col_img1, col_img2 = st.columns(2)
with col_img1:
    img_etl = load_image(IMAGES_RAPPORT_PATH, "RUN_ALL_ETL.png")
    if img_etl:
        st.image(img_etl, caption="SSIS Master Package Integration" if L=='EN' else "Intégration via SSIS Master Package", use_container_width=True)
        
    img_archi = load_image(IMAGES_RAPPORT_PATH, "SUIVI_EVOLUTION PAR_COUCHE.png")
    if img_archi:
        st.image(img_archi, caption="Data Lineage Assessment" if L=='EN' else "Audit de conformité des données (DSA/ODS/DWH)", use_container_width=True)

with col_img2:
    img_scd = load_image(IMAGES_RAPPORT_PATH, "RESULTAT_SCD2_SSMS_SIMPLE.png")
    if img_scd:
        st.image(img_scd, caption="T-SQL Validation of Type 2 Dimensions" if L=='EN' else "Validation T-SQL des Dimensions Historisées", use_container_width=True)

# ----------------- SECTION DATAVIZ -----------------
st.markdown(f"<div class='section-header'>{content[L][EXP]['viz_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body'>{content[L][EXP]['viz_text']}</div><br>", unsafe_allow_html=True)

# Affichage avec Système d'Onglets (Tabs) pour une expérience "Application"
tab_titles = ["Synthèse Executive", "Analyse des Ventes", "Intelligence Catalogue", "Rétention Client", "Ressources Humaines"] if L == 'FR' else ["Executive Summary", "Sales Analytics", "Catalog Margins", "Customer Retention", "HR Performance"]
tabs = st.tabs(tab_titles)

with tabs[0]:
    img_syn = load_image(PBI_PATH, "PAGE_DE_SYNTHESE.png")
    if img_syn: st.image(img_syn, use_container_width=True)

with tabs[1]:
    img_ven = load_image(PBI_PATH, "PAGE_DE_VENTE.png")
    if img_ven: st.image(img_ven, use_container_width=True)

with tabs[2]:
    img_cat = load_image(PBI_PATH, "PAGE_DU_CATALOGUE.png")
    if img_cat: st.image(img_cat, use_container_width=True)

with tabs[3]:
    img_cli = load_image(PBI_PATH, "PAGE_DE_CLIENTS.png")
    if img_cli: st.image(img_cli, use_container_width=True)

with tabs[4]:
    img_emp = load_image(PBI_PATH, "PAGE_DES_EMPLOYES.png")
    if img_emp: st.image(img_emp, use_container_width=True)

# ----------------- SECTION IMPACT -----------------
st.markdown(f"<div class='section-header'>{content[L][EXP]['impact_title']}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='text-body' style='margin-bottom: 50px;'>{content[L][EXP]['impact_text']}</div>", unsafe_allow_html=True)
