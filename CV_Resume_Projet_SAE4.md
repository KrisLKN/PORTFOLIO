# PROJET : DÉVELOPPEMENT D'UNE SOLUTION DÉCISIONNELLE (BUSINESS INTELLIGENCE)
**Mots-clés :** Data Engineering, ETL, MS SQL Server, SSIS, Power BI, Python, Modélisation en étoile, SCD Type 2.

*Conception et implémentation complète d'une infrastructure Data (de la base transactionnelle jusqu'au tableau de bord de direction) pour l'analyse de données de ventes omnicanales.*

### 🛠️ Réalisations Techniques :
- **Architecture ETL & Pipelines Data :** Création d'un pipeline étanche en 3 couches (Staging Area, ODS, Data Warehouse) avec SQL Server Integration Services (SSIS) pour extraire, nettoyer et consolider des données hétérogènes (Magasin physique & Vente en ligne).
- **Modélisation Avancée (Data Warehouse) :** Modélisation d'un data warehouse en étoile pur. Dénormalisation de données complexes (pistes, albums, genres) et gestion des relations Many-to-Many via table Bridge (Playlists).
- **Gestion d'historique (Slowly Changing Dimensions) :** Paramétrage d'un flux SCD Type 2 garantissant la traçabilité temporelle des prix, évitant ainsi les distorsions analytiques sur le chiffre d'affaires.
- **Reporting & Data Visualisation (DAX / Power BI) :** Conception d’un tableau de bord de direction interactif structuré en 5 axes (Synthèse, Ventes, Catalogue, RH, Clients) permettant une fouille de données fine sur le CA et la performance omnicanale.
- **Automatisation & Qualité :** Orchestration via un Master Package, utilisation de Lookups pour l'intégrité référentielle, et génération programmatique de rapports PDF via Python.

### 🎯 Impact & Compétences Développées :
- Vision "End-to-End" du cycle de vie de la Data en entreprise.
- Rigueur dans la résolution d'anomalies de typage de données et l'optimisation des requêtes.
- Capacité avérée à traduire un besoin Métier (Direction/Management) en leviers techniques opérationnels (Modélisation, ETL, Dataviz).
