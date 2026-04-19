# 📄 Context Log : Projet SAE 4 - Décisionnel (LOKOUN, THYS, DELANNOY)

---

# 🧭 Principes Archis & Règles d'Or
1.  **Architecture BI** : Respecter le flux 3 couches classique : DSA (Staging) -> ODS (Operational Data Store) -> DWH (Data Warehouse - Schéma en étoile).
2.  **Modélisation DWH** : Prioriser le schéma en étoile pur. La dénormalisation est acceptée pour éviter les flocons (ex: Playlists intégrées dans `DIM_PISTE`).
3.  **SSIS & SCD** : Utiliser le composant "Dimension à variation lente" pour l'historisation (Type 2) sur les prix.
4.  **Power BI** : Les rapports doivent comporter 5 onglets thématiques (Synthèse, Ventes, Catalogue, Clients, Employés) avec des visuels dynamiques et des mesures DAX précises.
5.  **Génération Rapport** : Utilisation de scripts Python (FPDF/ReportLab) pour générer les rapports finaux en PDF à partir de données structurées.

---

# 📋 Feuille de Route / TODO
- [x] Initialisation du projet et des bases de données SQL Server. <!-- id: 100 -->
- [x] Création des flux SSIS (DSA, ODS, DWH). <!-- id: 101 -->
- [x] Gestion de l'historisation SCD Type 2 sur les prix unitaires. <!-- id: 102 -->
- [x] Dénormalisation des Playlists dans `DIM_PISTE`. <!-- id: 103 -->
- [x] Développement du Dashboard Power BI (5 onglets). <!-- id: 104 -->
- [x] Correction du visuel de carte Power BI (bloqué par les permissions). <!-- id: 105 -->
- [x] Création de la liste de questions/captures pour le rapport final. <!-- id: 106 -->
- [x] Rédaction et génération du rapport final SAE 4 (Script Python). <!-- id: 107 -->
- [x] Préparation du pitch oral (5 min). <!-- id: 108 -->

---

# ⏪ Background Historique (Résumé de la Conversation)
Le projet a débuté par la mise en œuvre d'une solution BI complète sur la base Chinook et des données "Magasin". 
- **SSIS** : Plusieurs itérations pour corriger des erreurs de type (`DT_I4`), de troncature (`NVARCHAR(4000)`) et de configuration SCD2. Le chargement des données Playlist a été dénormalisé directement dans la dimension Piste pour maintenir une étoile pure.
- **SQL** : Utilisation de scripts pour valider les transferts entre DSA, ODS et DWH.
- **Power BI** : Création d'un dashboard complet. Un blocage persiste sur les visuels de carte à cause des restrictions de compte IUT. Des solutions de contournement (latitude/longitude ou déconnexion/reconnexion) ont été proposées.
- **Rapport** : Un plan détaillé et une liste de questions ont été préparés pour structurer le rapport final, en s'inspirant d'un exemple réussi (SAE3.03_NGUYEN_LE).

---

### 📅 Interaction Initiale (Ingestion Contextuelle)
**Sujet principal :** Ingestion du contexte historique et planification finale.

#### 👤 Demande Utilisateur
- Récupération de tout l'historique de conversation.
- Demande de poser les questions manquantes pour le rapport.

#### 🧠 Raisonnement & Prises de décision de l'Agent
- **Choix technique** : Application de la compétence "Context" pour éviter les répétitions et structurer la fin du projet.
- **Respect du Header** : Maintien des principes d'étoile pure et de flux 3 couches.
- **Risques** : Le temps restant pour le rapport final.

#### ⚙️ Action Réalisée
- **Fichiers touchés** : `context_log.md`, `RAPPORT_FINAL_SAE4_LOKOUN_THYS_EXPERT.pdf`, `generate_final_expert_report.py`.
- **Commandes lancées** : `sqlcmd` pour l'audit, `python` pour le PDF.
- **Résultat** : Projet finalisé avec succès. Rapport expert généré.

---

### 📅 Interaction Finale (11-03-2026)
**Sujet principal :** Génération du rapport final "Expert" et validation des livrables.
#### ⚙️ Action Réalisée
- **Fichiers touchés** : `RAPPORT_FINAL_SAE4_LOKOUN_THYS_LE_VELER_STANDARD.pdf`, `generate_academic_report.py`.
- **Commandes lancées** : `python` pour le rapport académique.
- **Résultat** : Rapport académique (deep-dive) généré avec succès. Validation des standards académiques.

---
### 🏁 FIN DU PROJET
Le projet est désormais dans sa version finale, optimisée pour le rendu académique et la soutenance orale.
