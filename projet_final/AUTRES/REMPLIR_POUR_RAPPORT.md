# 📝 FORMULAIRE À REMPLIR POUR LE RAPPORT FINAL SAE 4

*Cochez les cases en remplaçant `[ ]` par `[x]` quand c'est fait.*
*Tapez vos réponses directement sous les questions à la place de `Votre réponse ici...`.*
*Prenez les captures d'écran demandées et placez-les toutes dans un dossier (ex: `images_rapport/`).*
*Une fois terminé, copiez-collez tout ce texte et envoyez-le moi !*

---

## 1. ORGANISATION ET TECHNOLOGIE
**Q1. Pourquoi être passé d'Oracle (S3) à SSIS/SQL Server (S4) ? (Problèmes d'installation, envie de voir Microsoft, etc.)**
> Votre réponse ici...

**Q2. Comment vous êtes-vous réparti le travail avec Abel et comment avez-vous collaboré ?**
> Votre réponse ici...

---

## 2. MODÉLISATION ET BASES DE DONNÉES
**Q3. Qu'est-ce qui différenciait la nouvelle base "Magasin" de la base "Chinook" (Online) initiale ?**
> Votre réponse ici...

**Q4. Pourquoi avoir fusionné les infos des Playlists directement dans `DIM_PISTE` au lieu de faire de multiples dimensions en flocon ?**
> Votre réponse ici...

---

## 3. LE PROCESSUS ETL (SSIS)
**Q5. Dans le flux ODS, comment avez-vous réussi à détecter et appliquer les changements de prix (le fameux Lookup avec Match/No Match) ? Racontez le blocage que vous avez eu.**
> Votre réponse ici...

**Q6. Comment avez-vous géré la fusion technique des deux sources (Magasin + Online) dans SSIS vers le DWH ?**
> Votre réponse ici...

**Q7. Avez-vous rencontré des erreurs de troncature (ex: NVARCHAR(4000) dans du 500) ou des galères de conversion de types de dates ? Comment les avez-vous réglées ?**
> Votre réponse ici...

**Q8. Pourquoi et comment avez-vous mis une valeur par défaut `GETDATE()` dans SQL Server pour la colonne `DATE_DEBUT` ?**
> Votre réponse ici...

---

## 4. REPORTING (POWER BI)
**Q9. Quels sont les 3 principaux indicateurs (KPI) que vous mettez en avant sur l'onglet Synthèse ?**
> Votre réponse ici...

**Q10. Avez-vous utilisé du code DAX dans Power BI ? Si oui, à quoi a-t-il servi ?**
> Votre réponse ici...

---

## 5. PERSPECTIVES ET CONCLUSION
**Q11. Si vous aviez 10 heures de plus, que rajouteriez-vous à ce projet ?**
> Votre réponse ici...

---
---

## 📸 LISTE DES CAPTURES D'ÉCRAN À FAIRE

### A. Modélisation et BDD
- [ ] `capture_mpd_chinook.png` (Le schéma de départ de Chinook)
- [ ] `capture_etoile_dwh.png` (Votre schéma en étoile du DWH)
- [ ] `capture_ssms_arborescence.png` (Explorateur SSMS montrant vos 7 bases de données)
- [ ] `capture_ssms_scd2_preuve.png` (Une requête SELECT dans `DIM_PISTE` montrant une piste avec 2 prix différents : ACTIF=0 et ACTIF=1)

### B. SSIS (Très important)
- [ ] `capture_ssis_master.png` (Le Control Flow d'un super-package qui lance les autres, tout en vert)
- [ ] `capture_ssis_dsa_dataflow.png` (Data Flow d'un DSA basique : Source -> Derived Column -> Dst)
- [ ] `capture_ssis_ods_lookup.png` (Data Flow d'un ODS montrant le composant Lookup avec ses sorties Match/No Match)
- [ ] `capture_ssis_fait_fusion.png` (Data Flow de `FAIT_VENTE` montrant le composant "Union All" et la cascade de Lookups)
- [ ] `capture_ssis_scd_wizard.png` (Le Data Flow compliqué généré par le SCD Wizard pour `DIM_PISTE`)

### C. Power BI (Reporting)
- [ ] `capture_pbi_synthese.png`
- [ ] `capture_pbi_ventes.png`
- [ ] `capture_pbi_catalogue.png`
- [ ] `capture_pbi_clients.png`
- [ ] `capture_pbi_employes.png`

---
*Fin du formulaire.*
