# Expose SSIS - Projet ETL Chinook + Magasin
## LOKOUN Kris & THYS - BUT SD Semestre 4

---

# PLAN DE L'EXPOSE (5 minutes)

- **1 min** : Contexte + Jeu de donnees
- **2 min** : Composants utilises (role + parametres)
- **2 min** : Demo SSIS

---

# 1. CONTEXTE ET JEU DE DONNEES (1 min)

## 1.1 Le projet

Construction d'une chaine ETL complete a partir de **deux sources de donnees heterogenes** :

- **Chinook** (`Chinook_LOKOUN_THYS`) : base de ventes de musique en ligne (11 tables)
- **Magasin** (`Magasin_LOKOUN_THYS`) : base de ventes en magasin physique (2 tables, convertie d'Oracle vers SQL Server)

## 1.2 Architecture en 3 couches

```
SOURCES  -->  DSA (Data Staging Area)  -->  ODS (Operational Data Store)  -->  DWH (Data Warehouse)
```

- **DSA** : zone tampon technique (chargement brut, fiable, sans transformation metier)
- **ODS** : donnees propres + tracabilite (ajout de LOAD_DATE)
- **DWH** : modele en etoile pour l'analyse (dimensions + faits)

## 1.3 Le jeu de donnees

Le Data Warehouse final contient :

| Table | Description | Lignes |
|-------|-------------|--------|
| `DIM_DATE` | Dimension temporelle (toutes dates min/max) | ~1884 |
| `DIM_TRACK` | Dimension pistes musicales (**SCD Type 2**) | ~3503+ |
| `DIM_CUSTOMER` | Dimension clients | ~59 |
| `DIM_CHANNEL` | Dimension canal (Online=1, Store=2) | 2 |
| `DIM_GENRE` | Dimension genres musicaux | ~25 |
| `DIM_ARTIST` | Dimension artistes | ~275 |
| `DIM_ALBUM` | Dimension albums | ~347 |
| `DIM_EMPLOYEE` | Dimension employes | ~8 |
| `DIM_MEDIATYPE` | Dimension types de media | ~5 |
| `FACT_INVOICE` | Faits factures (Online + Store) | ~1412 |
| `FACT_INVOICE_LINE` | Faits lignes de facture | ~4757 |

Ce jeu de donnees est **non trivial** : il implique la fusion de 2 sources, la gestion de cles de substitution (TK), la tracabilite par canal, et la gestion de l'historique des prix (SCD2).

## 1.4 Pourquoi ce jeu de donnees est adapte

- **Deux sources heterogenes** a fusionner (Online + Store) -> justifie Union All
- **Changements de prix** sur les pistes -> justifie le SCD Type 2 sur DIM_TRACK
- **Dates a generer dynamiquement** -> justifie Execute SQL Task avec CTE recursive
- **Volumes suffisants** pour montrer l'interet des composants (3503 pistes, 4757 lignes de facture)
- **Dependances entre tables** (FK) -> justifie l'orchestration et Execute Package Task

---

# 2. COMPOSANTS SSIS UTILISES (2 min)

## ========================================
## INVENTAIRE COMPLET PAR NIVEAU
## ========================================

---

## 2.1 COMPOSANTS NIVEAU 1 (integration obligatoire)

### 2.1.1 Execute SQL Task (Tache Executer SQL)

**Ou ?** Dans le package `03_LOAD_DIM_DATE.dtsx`

**Role :**
L'Execute SQL Task permet d'executer une requete SQL directement dans le Control Flow (flux de controle), sans passer par un Data Flow Task. C'est utile pour des operations DDL (CREATE, ALTER, TRUNCATE) ou des insertions/mises a jour complexes qui ne necessitent pas de transformation ligne par ligne.

**Comment on l'a utilise :**
Le chargement de `DIM_DATE` ne necessite pas de flux de donnees classique (Source -> Transformation -> Destination). Au lieu de cela, une seule requete SQL genere toutes les dates entre la date minimum et la date maximum trouvees dans les ODS, puis les insere dans DIM_DATE avec un MERGE.

**Parametres cles configures :**

| Parametre | Valeur | Explication |
|-----------|--------|-------------|
| Connection | `LocalHost.DWH_COMMON_LOKOUN_THYS` | Connexion OLE DB vers le Data Warehouse |
| SQLStatement | Script SQL complet (MERGE + CTE) | Requete executee a chaque run |
| ResultSet | None | Pas de jeu de resultats retourne |

**Contenu du script SQL execute :**

```sql
-- 1) Trouver la date MIN et MAX dans les 4 tables ODS
DECLARE @DateMin DATE;
DECLARE @DateMax DATE;

SELECT @DateMin = MIN(DATE_COMPLETE), @DateMax = MAX(DATE_COMPLETE)
FROM (
    SELECT CAST(InvoiceDate AS DATE) AS DATE_COMPLETE
    FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Invoice]
    UNION
    SELECT CAST(InvoiceLineDate AS DATE) AS DATE_COMPLETE
    FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[InvoiceLine]
    UNION
    SELECT CAST(InvoiceDate AS DATE) AS DATE_COMPLETE
    FROM [ODS_STORE_LOKOUN_THYS].[dbo].[Invoice]
    UNION
    SELECT CAST(InvoiceLineDate AS DATE) AS DATE_COMPLETE
    FROM [ODS_STORE_LOKOUN_THYS].[dbo].[InvoiceLine]
) AS ToutesDates;

-- 2) Generer toutes les dates entre MIN et MAX avec une CTE recursive
WITH Dates AS (
    SELECT @DateMin AS DATE_COMPLETE
    UNION ALL
    SELECT DATEADD(DAY, 1, DATE_COMPLETE) FROM Dates
    WHERE DATE_COMPLETE < @DateMax
)
-- 3) MERGE : inserer seulement les dates qui n'existent pas deja
MERGE [dbo].[DIM_DATE] AS target
USING (
    SELECT DATE_COMPLETE,
           YEAR(DATE_COMPLETE)*10000 + MONTH(DATE_COMPLETE)*100 + DAY(DATE_COMPLETE) AS TK_DATE,
           DAY(DATE_COMPLETE) AS NUMERO_JOUR,
           MONTH(DATE_COMPLETE) AS NUMERO_MOIS,
           DATENAME(MONTH, DATE_COMPLETE) AS NOM_MOIS,
           (MONTH(DATE_COMPLETE)-1)/3 + 1 AS NUMERO_TRIMESTRE,
           YEAR(DATE_COMPLETE) AS NUMERO_ANNEE
    FROM Dates
) AS source
ON target.DATE_COMPLETE = source.DATE_COMPLETE
WHEN NOT MATCHED THEN INSERT (...) VALUES (...)
OPTION (MAXRECURSION 10000);
```

**Pourquoi c'est pertinent :**
- Evite un Data Flow Task inutilement complexe pour une operation purement SQL
- Le MERGE garantit l'idempotence (pas de doublons si on relance)
- La CTE recursive genere automatiquement toutes les dates sans intervention manuelle
- Le parametre `OPTION (MAXRECURSION 10000)` est necessaire car SQL Server limite par defaut la recursion a 100

**Parametre dynamique :**
Les noms des bases ODS (`ODS_ONLINE_LOKOUN_THYS`, `ODS_STORE_LOKOUN_THYS`) sont references dans la requete SQL. On pourrait les parametrer via des variables SSIS pour rendre le package reutilisable sur d'autres environnements.

---

### 2.1.2 Row Count (Nombre de Lignes)

**Ou ?** Dans **TOUS** les packages DSA (13 packages) :
- `01_LOAD_DSA_TRACK_ONLINE.dtsx` (variable : `User::RowCount_Track`)
- `01_LOAD_DSA_ALBUM_ONLINE.dtsx` (variable : `User::RowCount_Album`)
- `01_LOAD_DSA_ARTIST_ONLINE.dtsx` (variable : `User::RowCount_Artist`)
- `01_LOAD_DSA_CUSTOMER_ONLINE.dtsx` (variable : `User::RowCount_Customer`)
- `01_LOAD_DSA_EMPLOYEE_ONLINE.dtsx` (variable : `User::RowCount_Employee`)
- `01_LOAD_DSA_GENRE_ONLINE.dtsx` (variable : `User::RowCount_Genre`)
- `01_LOAD_DSA_INVOICE_ONLINE.dtsx` (variable : `User::RowCount_Invoice`)
- `01_LOAD_DSA_INVOICELINE_ONLINE.dtsx` (variable : `User::RowCount_InvoiceLine`)
- `01_LOAD_DSA_MEDIATYPE_ONLINE.dtsx` (variable : `User::RowCount_MediaType`)
- `01_LOAD_DSA_PLAYLIST_ONLINE.dtsx` (variable : `User::RowCount_Playlist`)
- `01_LOAD_DSA_PLAYLISTTRACK_ONLINE.dtsx` (variable : `User::RowCount_PlaylistTrack`)
- `01_LOAD_DSA_INVOICE_STORE.dtsx` (variable : `User::RowCount_INVOICE_STORE`)
- `01_LOAD_DSA_INVOICELINE_STORE.dtsx` (variable : `User::RowCount_INVOICELINE_STORE`)

**Role :**
Le composant Row Count compte le nombre de lignes qui traversent un point du flux de donnees et stocke ce nombre dans une variable SSIS. Il ne modifie pas les donnees.

**Comment on l'a utilise :**
Place entre la transformation (Derived Column) et la destination (OLE DB Destination) dans chaque package DSA, il permet de verifier combien de lignes ont ete effectivement chargees.

**Parametres cles :**

| Parametre | Valeur (exemple Track) | Explication |
|-----------|----------------------|-------------|
| VariableName | `User::RowCount_Track` | Variable SSIS qui recoit le nombre de lignes |

**Pourquoi c'est pertinent :**
- **Controle de qualite** : on verifie que le nombre de lignes chargees correspond a ce qu'on attend (ex : 3503 Track, 347 Album, 275 Artist)
- **Audit** : en cas de probleme, on sait exactement combien de lignes sont passees
- **Debugging** : si la variable vaut 0, on sait que la source est vide ou que le mapping est incorrect

---

## 2.2 COMPOSANTS NIVEAU 2 (intermediaire)

### 2.2.1 Derived Column (Colonne Derivee) -- COMPOSANT LE PLUS UTILISE

**Ou ?** Dans **TOUS** les packages du projet (DSA, ODS, DWH) - plus de 30 occurrences

**Role :**
Le composant Derived Column cree de nouvelles colonnes ou remplace des colonnes existantes en appliquant des expressions SSIS. C'est le "couteau suisse" du Data Flow.

**Utilisations concretes dans le projet :**

#### a) En couche DSA (ajout de dates de tracabilite)
Dans chaque package DSA, une Derived Column ajoute une colonne de date :
- Expression : `GETDATE()`
- Nom : `TrackDate`, `AlbumDate`, `GenreDate`, etc.
- Type : `DT_DBTIMESTAMP`

#### b) En couche DSA (ajout du CHANNEL_ID)
Pour les tables Invoice, ajout d'une constante identifiant le canal :
- ONLINE : Expression = `1` (INT) -> `CHANNEL_ID = 1`
- STORE : Expression = `2` (INT) -> `CHANNEL_ID = 2`

#### c) En couche ODS (ajout de LOAD_DATE)
Dans chaque package ODS, une Derived Column ajoute :
- Expression : `GETDATE()`
- Nom : `LOAD_DATE`
- Type : `DT_DBTIMESTAMP`

#### d) En couche DWH - DIM_TRACK (3 Derived Columns differentes !)

**CD_DIM_TRACK** : Prepare les colonnes pour l'insertion initiale

| Colonne derivee | Expression | Type | But |
|----------------|------------|------|-----|
| DURATION_MS | `Milliseconds` | INT | Renommage de la colonne source |
| FILESIZE_BYTES | `Bytes` | INT | Renommage de la colonne source |
| UNIT_PRICE | `UnitPrice` | NUMERIC(10,2) | Colonne surveillee par le SCD2 |
| DATE_DEBUT | `GETDATE()` | DT_DBTIMESTAMP | Date de debut de validite SCD2 |
| ACTIF | `1` | INT | Flag actif pour la nouvelle ligne |

**CD_FERMER_ANCIENNE** : Prepare les valeurs pour fermer l'ancienne ligne (SCD2)

| Colonne derivee | Expression | Type | But |
|----------------|------------|------|-----|
| DATE_FIN | `DATEADD("day", -1, GETDATE())` | DT_DBTIMESTAMP | Ferme la ligne a la veille |
| ACTIF | `0` | INT | Marque la ligne comme inactive |

**CD_NOUVELLE_LIGNE** : Prepare les valeurs pour la nouvelle version (SCD2)

| Colonne derivee | Expression | Type | But |
|----------------|------------|------|-----|
| DATE_DEBUT | `GETDATE()` | DT_DBTIMESTAMP | Debut de validite de la nouvelle version |
| ACTIF | `1` | INT | La nouvelle ligne est active |

#### e) En couche DWH - FACT_INVOICE et FACT_INVOICE_LINE
- Cast de dates : `(DT_DBDATE)InvoiceLineDate` pour assurer la correspondance avec DIM_DATE
- Calcul de colonnes derivees pour le mapping

**Parametre dynamique :**
Les expressions des Derived Column pourraient etre parametrees via des variables SSIS (ex : coefficient de calcul, taux TVA, date de reference).

---

### 2.2.2 Conditional Split (Separation Conditionnelle)

**Ou ?** Dans le package `03_LOAD_DIM_TRACK.dtsx`

**Role :**
Le Conditional Split permet de router les lignes vers differentes sorties en fonction de conditions (expressions SSIS). C'est l'equivalent d'un `IF/ELSE` ou d'un `SWITCH/CASE` dans le flux de donnees.

**Comment on l'a utilise :**
Le composant `CS_PRIX_CHANGE` dans le flux SCD2 de DIM_TRACK compare le prix unitaire actuel de chaque piste avec le prix existant en base :

**Condition configuree :**
```
UNIT_PRICE != UNIT_PRICE_EXISTANT
```

**Sorties :**

| Sortie | Condition | Destination |
|--------|-----------|-------------|
| `PRIX_CHANGE` | `UNIT_PRICE != UNIT_PRICE_EXISTANT` | Flux SCD2 (fermeture ancienne + insertion nouvelle) |
| `Sortie par defaut` | Aucun changement | Lignes ignorees (pas de modification) |

**Parametres cles :**

| Parametre | Valeur | Explication |
|-----------|--------|-------------|
| Expression (Sortie 1) | `UNIT_PRICE != UNIT_PRICE_EXISTANT` | Detecte les pistes dont le prix a change |
| Order | 1 | Priorite de la condition |
| Default Output Name | Sortie par defaut | Les lignes sans changement |

**Pourquoi c'est pertinent :**
- C'est le coeur de la logique SCD2 : seules les pistes dont le prix a **reellement change** declenchent la creation d'une nouvelle version
- Sans cette separation, on recreerait inutilement des lignes pour toutes les pistes a chaque execution
- La condition est non triviale : elle compare deux valeurs NUMERIC(10,2) venant de sources differentes (ODS vs DWH existant)

---

### 2.2.3 Union All (Unir Tout)

**Ou ?** Dans les packages :
- `03_LOAD_FACT_INVOICE.dtsx`
- `03_LOAD_FACT_INVOICE_LINE.dtsx`

**Role :**
Le composant Union All combine les lignes de plusieurs entrees en une seule sortie. Contrairement a Merge, il ne necessite PAS que les donnees soient triees.

**Comment on l'a utilise :**
Dans chaque package de chargement des tables de faits, un Union All fusionne les donnees venant des deux ODS :

```
SRC_INVOICE_ODS_ONLINE ----\
                             >--- UNION_ALL_INVOICE ---> (Lookup + Destination)
SRC_INVOICE_ODS_STORE -----/
```

**Pourquoi c'est pertinent :**
- Les deux sources (Online et Store) ont la meme structure de colonnes
- Les donnees NE SONT PAS triees -> Union All est le bon choix (pas besoin de Merge)
- Cela permet de charger les faits des deux sources en un seul flux, sans dupliquer la logique de Lookup et d'insertion

**Parametres cles :**
- Mapping des colonnes : chaque entree doit avoir les memes colonnes (ou compatibles) mappees vers la sortie

---

## 2.3 COMPOSANT NIVEAU 3 (avance) -- COMPOSANT PRINCIPAL

### 2.3.1 Slowly Changing Dimension Type 2 (SCD2) -- Implementation manuelle

**Ou ?** Dans le package `03_LOAD_DIM_TRACK.dtsx`

**Role :**
Le SCD Type 2 (Slowly Changing Dimension Type 2) est une strategie de gestion de l'historique des changements dans une dimension. Au lieu de simplement mettre a jour une ligne existante (SCD Type 1), le SCD Type 2 **conserve l'historique** en :
1. **Fermant** l'ancienne version de la ligne (DATE_FIN = hier, ACTIF = 0)
2. **Inserant** une nouvelle version avec les nouvelles valeurs (DATE_DEBUT = aujourd'hui, ACTIF = 1)

**IMPORTANT :** Dans notre projet, nous avons implemente le SCD2 **manuellement** (sans utiliser le composant SCD Wizard de SSIS), en combinant plusieurs composants :

### Architecture du flux SCD2 dans DIM_TRACK :

```
SRC_TRACK_ODS_ONLINE (OLE DB Source)
    |
    v
CD_DIM_TRACK (Derived Column)
    --> Ajoute : DURATION_MS, FILESIZE_BYTES, UNIT_PRICE, DATE_DEBUT, ACTIF=1
    |
    v
LKP_DIM_TRACK_ACTIF (Lookup)
    --> Cherche dans DIM_TRACK WHERE ACTIF = 1
    --> Recupere : TK_PISTE_EXISTANT, UNIT_PRICE_EXISTANT
    |
    |--- Match Output (piste existante) --------\
    |                                             |
    |--- No Match Output (nouvelle piste) ----> DST_DIM_TRACK_NOUVELLE
    |                                           (OLE DB Destination : insertion directe)
    |
    v (Match Output)
CS_PRIX_CHANGE (Conditional Split)
    |
    |--- PRIX_CHANGE (UNIT_PRICE != UNIT_PRICE_EXISTANT)
    |       |
    |       v
    |   CD_FERMER_ANCIENNE (Derived Column)
    |       --> DATE_FIN = DATEADD("day",-1,GETDATE())
    |       --> ACTIF = 0
    |       |
    |       v
    |   CMD_FERMER_ANCIENNE (OLE DB Command)
    |       --> UPDATE DIM_TRACK SET DATE_FIN=?, ACTIF=? WHERE TK_PISTE=?
    |       |
    |       v
    |   CD_NOUVELLE_LIGNE (Derived Column)
    |       --> DATE_DEBUT = GETDATE()
    |       --> ACTIF = 1
    |       |
    |       v
    |   DST_DIM_TRACK_CHANGEE (OLE DB Destination)
    |       --> INSERT nouvelle version de la piste
    |
    |--- Sortie par defaut (pas de changement) --> [rien, ignore]
```

### Composants utilises dans le flux SCD2 :

| Composant | Type SSIS | Role dans le SCD2 |
|-----------|-----------|-------------------|
| SRC_TRACK_ODS_ONLINE | OLE DB Source | Lit les pistes depuis l'ODS |
| CD_DIM_TRACK | Derived Column | Prepare les colonnes (renommage, GETDATE(), ACTIF=1) |
| LKP_DIM_TRACK_ACTIF | Lookup | Cherche si la piste existe deja (ACTIF=1) |
| CS_PRIX_CHANGE | Conditional Split | Detecte si le prix a change |
| CD_FERMER_ANCIENNE | Derived Column | Prepare DATE_FIN et ACTIF=0 |
| CMD_FERMER_ANCIENNE | OLE DB Command | UPDATE sur l'ancienne ligne |
| CD_NOUVELLE_LIGNE | Derived Column | Prepare DATE_DEBUT et ACTIF=1 |
| DST_DIM_TRACK_CHANGEE | OLE DB Destination | INSERT la nouvelle version |
| DST_DIM_TRACK_NOUVELLE | OLE DB Destination | INSERT les pistes totalement nouvelles |

### Parametres cles du Lookup (LKP_DIM_TRACK_ACTIF) :

**Requete SQL :**
```sql
SELECT TK_PISTE AS TK_PISTE_EXISTANT,
       NK_ID_PISTE,
       UNIT_PRICE AS UNIT_PRICE_EXISTANT
FROM DIM_TRACK
WHERE ACTIF = 1
```

| Parametre | Valeur | Explication |
|-----------|--------|-------------|
| Cache Mode | Full Cache | Charge toute la table de reference en memoire |
| Connection | DWH_COMMON_LOKOUN_THYS | Base du Data Warehouse |
| No Match Behavior | Redirect to No Match Output | Les nouvelles pistes vont vers l'insertion directe |
| Mapping | NK_ID_PISTE (input) -> NK_ID_PISTE (lookup) | Cle naturelle de correspondance |

### Parametres cles du OLE DB Command (CMD_FERMER_ANCIENNE) :

**Commande SQL :**
```sql
UPDATE [dbo].[DIM_TRACK]
SET DATE_FIN = ?,
    ACTIF = ?
WHERE TK_PISTE = ?
```

| Parametre | Mapping | Explication |
|-----------|---------|-------------|
| Param_0 | DATE_FIN (de CD_FERMER_ANCIENNE) | La date de fin de validite |
| Param_1 | ACTIF (de CD_FERMER_ANCIENNE) = 0 | Marque comme inactif |
| Param_2 | TK_PISTE_EXISTANT (de LKP) | Identifie la ligne a fermer |

### Test du SCD2 :

Un script de test (`05_TEST_SCD2_TRACK.sql`) a ete cree pour valider le fonctionnement :

```sql
USE [Chinook_LOKOUN_THYS];
UPDATE Track SET UnitPrice = 0.49
WHERE TrackId BETWEEN 2358 AND 2405;
-- 48 pistes modifiees de 0.99 a 0.49
```

Apres re-execution de l'ETL complet, dans DIM_TRACK on doit voir :
- Les anciennes lignes avec ACTIF=0, DATE_FIN = veille
- Les nouvelles lignes avec ACTIF=1, UNIT_PRICE=0.49, DATE_DEBUT = aujourd'hui

**Parametre dynamique :**
Le nom de la table de dimension ou la colonne de cle d'entreprise (NK_ID_PISTE) pourrait etre parametre via des variables SSIS pour rendre le package reutilisable pour d'autres dimensions SCD2.

---

## 2.4 AUTRES COMPOSANTS UTILISES (hors niveaux)

### 2.4.1 Lookup (Recherche)

Utilise dans **tous** les packages ODS et DWH :
- **ODS** : verifie si la ligne existe deja (anti-doublon)
- **DWH FACT** : recupere les cles de substitution (TK_DATE, TK_CLIENT, TK_CANAL, TK_PISTE, TK_FACTURE)
- **DWH DIM_TRACK** : verifie l'existence de la piste active (SCD2)

### 2.4.2 OLE DB Command (Commande OLE DB)

Utilise dans `03_LOAD_DIM_TRACK.dtsx` pour executer un UPDATE ligne par ligne sur les anciennes versions des pistes (fermeture SCD2).

### 2.4.3 Execute Package Task (Tache Executer le Package)

Utilise dans les packages d'orchestration :
- `00_RUN_ALL.dtsx` : execute RUN_DSA -> RUN_ODS -> RUN_DWH
- `00_RUN_ALL_DSA_LOADS.dtsx` : execute les 13 packages DSA
- `00_RUN_ALL_ODS_LOADS.dtsx` : execute les packages ODS
- `00_RUN_ALL_DWH_lOADS.dtsx` : execute les 10 packages DWH

Ordre d'orchestration dans `00_RUN_ALL.dtsx` :
```
RUN_DSA  --(Success)-->  RUN_ODS  --(Success)-->  RUN_DWH
```

---

# 3. DEMO SSIS (2 min)

## 3.1 Ce qu'on montre

### Demo 1 : Package DSA (couche 1)
- Ouvrir `01_LOAD_DSA_TRACK_ONLINE.dtsx`
- Montrer le flux : **OLE DB Source** -> **Derived Column** (TrackDate + CHANNEL_ID) -> **Row Count** -> **OLE DB Destination**
- Executer et montrer la variable `RowCount_Track` = 3503

### Demo 2 : Package DIM_DATE (Execute SQL Task)
- Ouvrir `03_LOAD_DIM_DATE.dtsx`
- Montrer le Control Flow avec l'**Execute SQL Task** seul
- Montrer la requete SQL (MERGE + CTE recursive)
- Executer et verifier dans SSMS : `SELECT COUNT(*) FROM DIM_DATE`

### Demo 3 : Package DIM_TRACK (SCD2 - composant principal)
- Ouvrir `03_LOAD_DIM_TRACK.dtsx`
- Montrer le flux complet :
  - **Source** -> **Derived Column** -> **Lookup** (match/no match)
  - **Conditional Split** (prix change ?)
  - Branche "change" : **Derived Column** (fermer) -> **OLE DB Command** (UPDATE) -> **Derived Column** (nouvelle) -> **Destination** (INSERT)
  - Branche "no match" : **Destination** (INSERT directe)
- Executer le script de test SCD2 dans SSMS (`05_TEST_SCD2_TRACK.sql`)
- Re-executer le package DIM_TRACK
- Verifier dans SSMS :
```sql
SELECT TK_PISTE, NK_ID_PISTE, NOM_PISTE, UNIT_PRICE, DATE_DEBUT, DATE_FIN, ACTIF
FROM DIM_TRACK
WHERE NK_ID_PISTE BETWEEN 2358 AND 2405
ORDER BY NK_ID_PISTE, DATE_DEBUT;
```

### Demo 4 : Package FACT_INVOICE_LINE (Union All)
- Ouvrir `03_LOAD_FACT_INVOICE_LINE.dtsx`
- Montrer le flux : 2 Sources ODS (Online + Store) -> **Union All** -> Lookups (TK_DATE, TK_PISTE, TK_FACTURE) -> Destination

### Demo 5 : Package global (orchestration)
- Ouvrir `00_RUN_ALL.dtsx`
- Montrer l'enchainement : RUN_DSA -> RUN_ODS -> RUN_DWH
- Executer et montrer que tout passe au vert

---

# 4. RECAPITULATIF DES COMPOSANTS

## Tableau recapitulatif par niveau

| Niveau | Composant | Packages ou il est utilise | Nombre d'occurrences |
|--------|-----------|---------------------------|---------------------|
| **Niveau 1** | Execute SQL Task | `03_LOAD_DIM_DATE.dtsx` | 1 |
| **Niveau 1** | Row Count | Tous les packages DSA (`01_LOAD_DSA_*.dtsx`) | 13 |
| **Niveau 2** | Derived Column | TOUS les packages (DSA, ODS, DWH) | 30+ |
| **Niveau 2** | Conditional Split | `03_LOAD_DIM_TRACK.dtsx` | 1 |
| **Niveau 2** | Union All | `03_LOAD_FACT_INVOICE.dtsx`, `03_LOAD_FACT_INVOICE_LINE.dtsx` | 2 |
| **Niveau 3** | SCD Type 2 (manuel) | `03_LOAD_DIM_TRACK.dtsx` | 1 |
| Autre | Lookup | Tous les packages ODS et DWH | 20+ |
| Autre | OLE DB Command | `03_LOAD_DIM_TRACK.dtsx` | 1 |
| Autre | Execute Package Task | `00_RUN_ALL*.dtsx` | 4 packages |

## Schema du flux principal (DIM_TRACK avec SCD2)

```
Source (ODS)
    |
    v
[Niveau 2] Derived Column  (prepare colonnes)
    |
    v
[Lookup] Recherche piste existante (ACTIF=1)
    |
    +-- No Match --> [Destination] Insert nouvelle piste
    |
    +-- Match --> [Niveau 2] Conditional Split (prix change ?)
                    |
                    +-- OUI --> [Niveau 2] Derived Column (fermer ancienne)
                    |               |
                    |               v
                    |           [OLE DB Command] UPDATE (DATE_FIN, ACTIF=0)
                    |               |
                    |               v
                    |           [Niveau 2] Derived Column (nouvelle ligne)
                    |               |
                    |               v
                    |           [Destination] Insert nouvelle version
                    |
                    +-- NON --> (rien, la piste est inchangee)
```

---

# 5. CONCLUSION

Ce projet ETL illustre une utilisation **reelle et non triviale** des composants SSIS :
- Les composants de **Niveau 1** (Execute SQL Task, Row Count) sont integres de maniere utile (pas decoratifs)
- Les composants de **Niveau 2** (Derived Column, Conditional Split, Union All) sont au coeur de chaque transformation
- Le composant de **Niveau 3** (SCD Type 2) est l'element le plus complexe, implemente manuellement avec une combinaison de Lookup, Conditional Split, Derived Column et OLE DB Command
- L'**orchestration** (Execute Package Task) garantit un chargement automatise dans le bon ordre
- Les **parametres dynamiques** (variables SSIS, noms de bases, expressions) rendent les packages reutilisables

---

# CAPTURES D'ECRAN NECESSAIRES

1. [EXISTANTE] `IMAGES_RAPPORT/LOAD_DIM_TRACK_NON_EXECUTER.png` - Flux DIM_TRACK avant execution
2. [EXISTANTE] `IMAGES_RAPPORT/LOAD_DIM_TRACK_EXUTOION COMPLETE ET FONCTIONNELLE.png` - Flux DIM_TRACK apres execution
3. [EXISTANTE] `IMAGES_RAPPORT/LOAD_INVOICELINE.png` - Flux FACT_INVOICE_LINE
4. [EXISTANTE] `IMAGES_RAPPORT/RUN_ALL_ETL.png` - Package global 00_RUN_ALL
5. [EXISTANTE] `IMAGES_RAPPORT/RUN_ALL_DSA.png` - Package DSA global
6. [EXISTANTE] `IMAGES_RAPPORT/RUN_ALL_ODS.png` - Package ODS global
7. [EXISTANTE] `IMAGES_RAPPORT/LOAD_DSA_TRACK.png` - Package DSA Track
8. [A FAIRE] Capture de l'Execute SQL Task (03_LOAD_DIM_DATE) - editeur de proprietes
9. [A FAIRE] Capture du Conditional Split (CS_PRIX_CHANGE) - editeur de conditions
10. [A FAIRE] Capture du Lookup (LKP_DIM_TRACK_ACTIF) - onglet Connection + Columns
11. [A FAIRE] Capture du OLE DB Command (CMD_FERMER_ANCIENNE) - onglet Column Mappings
12. [A FAIRE] Capture du resultat SCD2 dans SSMS (SELECT sur DIM_TRACK avec ACTIF=0 et ACTIF=1)
13. [A FAIRE] Capture du Union All (UNION_ALL_INVOICELINE) - editeur de mappings
14. [A FAIRE] Capture du Row Count - proprietes avec le nom de la variable
