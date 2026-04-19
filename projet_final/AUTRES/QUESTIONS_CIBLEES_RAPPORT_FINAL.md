# 🎯 QUESTIONS CIBLÉES POUR FINALISER LE RAPPORT

J'ai bien analysé ton brouillon actuel ! Il est déjà excellent sur l'architecture et les flux globaux. Pour que le rapport final généré par le script Python décroche la note maximale, il manque juste quelques "vrais" retours d'expérience sur la technique.

Remplis ces questions rapides (mets des `[x]` et tape sous les questions), puis on génère le rapport !

---

## 1. INTÉGRATION DU MAGASIN PHYSIQUE
Ton brouillon dit que vous avez utilisé un `Union All`.
**Q1. Quelles ont été les difficultés liées à la base Oracle "Magasin" ?**
> Les types de données étaient-ils différents (ex: NUMBER vs INT) ? Les noms de colonnes correspondaient-ils directement ou as-tu dû tout renommer dans SSIS (Derived Column) avant le Union All ? Raconte une difficulté d'intégration précise.
> *Ta réponse :* 

---

## 2. L'ENFER DU SCD TYPE 2 (Historisation des prix)
Ton brouillon dit que le "SCD2 ne se déclenchait pas" au début et que c'était le plus dur de la SAE.
**Q2. Comment as-tu implémenté le SCD2 dans la dimension DIM_PISTE ?**
> As-tu utilisé le composant tout fait "SCD Wizard" (Dimension à variation lente) de SSIS, ou as-tu tout fait à la main (Lookup, Conditional Split, OLE DB Command) ?
> *Ta réponse :* 

**Q3. L'erreur `DATE_DEBUT` NULL**
> Raconte le bug final que nous venons de corriger ensemble ce soir dans SSIS. (L'erreur où la destination d'insertion plantait car SSIS n'envoyait pas de date, et comment la contrainte `DEFAULT GETDATE()` dans SQL Server a sauvé le composant). C'est le genre de détail "vécu" que les profs adorent lire !
> *Ta réponse :* 

---

## 3. REPORTING (LE DASHBOARD)
Cette partie est absente de ton brouillon PDF.
**Q4. Explique-moi concrètement le dashboard PowerBI (ou autre outil) que vous avez rendu.**
> 1. Quel outil as-tu utilisé ?
> 2. Quels sont les 3 gros indicateurs de la vue "Synthèse" ?
> 3. As-tu fait un visuel comparant les ventes "Magasin" vs "En ligne" ?
> *Ta réponse :* 

---

## 📸 LES SEULES CAPTURES D'ÉCRAN DONT J'AI ENCORE BESOIN
Mets-les dans un dossier. C'est indispensable pour aérer le rapport.

- [ ] `capture_ssis_fait_fusion.png` : Un screen clair de ton flux SSIS où on voit le composant `Union All` qui mélange les ventes magasin et en ligne.
- [ ] `capture_ssis_scd2.png` : Le flux SSIS du chargement de `DIM_PISTE` (soit le wizard de SSIS, soit ton flux manuel).
- [ ] `capture_ssms_scd2_preuve.png` : Dans SQL Server (SSMS), affiche la table DIM_PISTE et montre-moi une piste musicale qui apparaît en **double** (une ligne avec l'ancien prix et ACTIF à 0, et la nouvelle ligne avec le nouveau prix et ACTIF à 1).
- [ ] 5 captures de tes 5 onglets du Dashboard (`dashboard_synthese.png`, `dashboard_ventes.png`, etc.).

Dès que tu as répondu et pris ces 8 captures, c'est parti pour la version finale !
