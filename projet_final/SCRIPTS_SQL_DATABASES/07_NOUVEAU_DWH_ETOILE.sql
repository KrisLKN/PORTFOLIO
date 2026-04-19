/*******************************************************************************
 NOUVEAU DATAWAREHOUSE - SCHÉMA EN ÉTOILE CORRIGÉ
 DWH_COMMON_LOKOUN_THYS
 
 STRUCTURE : 1 TABLE DE FAITS + 5 DIMENSIONS
 ─────────────────────────────────────────────
 FAIT_VENTE       → Table de faits centrale (ligne de vente)
 DIM_DATE         → Dimension temporelle (avec hiérarchie complète)
 DIM_PISTE        → Dimension produit (Genre + Album + Artiste + Média intégrés) + SCD2
 DIM_CLIENT       → Dimension client (avec lien vers employé)
 DIM_EMPLOYE      → Dimension employé (conseiller de vente)
 DIM_CANAL        → Dimension canal de vente (En ligne / Magasin physique)
 
 AVANT           → APRÈS
 ─────────────────────────────────────────────
 11 tables        → 6 tables
 2 tables de faits → 1 table de faits
 Flocon (snowflake) → Étoile (star schema)
 Relation Fait→Fait → Éliminée
 DIM_ALBUM séparée  → Intégrée dans DIM_PISTE
 DIM_ARTIST séparée → Intégrée dans DIM_PISTE
 DIM_GENRE séparée  → Intégrée dans DIM_PISTE
 DIM_MEDIATYPE sep. → Intégrée dans DIM_PISTE
 
 ORDRE D'EXÉCUTION :
 Ce script doit être exécuté AVANT 08_CHARGER_DWH_DEPUIS_ODS.sql
 ********************************************************************************/
USE [DWH_COMMON_LOKOUN_THYS];
GO PRINT '================================================';
PRINT ' ÉTAPE 1 : Suppression des anciens objets';
PRINT '================================================';
-- Supprimer les vues si elles existent
DROP VIEW IF EXISTS [dbo].[V_FAIT_VENTE];
DROP VIEW IF EXISTS [dbo].[V_DIM_TRACK_ETOILE];
DROP VIEW IF EXISTS [dbo].[V_DIM_TRACK_COMPLET];
GO -- Supprimer les contraintes FK (pour pouvoir supprimer les tables)
    IF EXISTS (
        SELECT 1
        FROM sys.foreign_keys
        WHERE name = 'FK_FACT_INVOICE_LINE_FACT_INVOICE'
    )
ALTER TABLE [dbo].[FACT_INVOICE_LINE] DROP CONSTRAINT [FK_FACT_INVOICE_LINE_FACT_INVOICE];
IF EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FACT_INVOICE_LINE_DIM_TRACK'
)
ALTER TABLE [dbo].[FACT_INVOICE_LINE] DROP CONSTRAINT [FK_FACT_INVOICE_LINE_DIM_TRACK];
IF EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FACT_INVOICE_LINE_DIM_DATE'
)
ALTER TABLE [dbo].[FACT_INVOICE_LINE] DROP CONSTRAINT [FK_FACT_INVOICE_LINE_DIM_DATE];
IF EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FACT_INVOICE_DIM_CUSTOMER'
)
ALTER TABLE [dbo].[FACT_INVOICE] DROP CONSTRAINT [FK_FACT_INVOICE_DIM_CUSTOMER];
IF EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FACT_INVOICE_DIM_DATE'
)
ALTER TABLE [dbo].[FACT_INVOICE] DROP CONSTRAINT [FK_FACT_INVOICE_DIM_DATE];
IF EXISTS (
    SELECT 1
    FROM sys.foreign_keys
    WHERE name = 'FK_FACT_INVOICE_DIM_CHANNEL'
)
ALTER TABLE [dbo].[FACT_INVOICE] DROP CONSTRAINT [FK_FACT_INVOICE_DIM_CHANNEL];
GO -- Supprimer les anciennes tables de faits
    DROP TABLE IF EXISTS [dbo].[FACT_INVOICE_LINE];
DROP TABLE IF EXISTS [dbo].[FACT_INVOICE];
GO -- Supprimer les anciennes dimensions
    DROP TABLE IF EXISTS [dbo].[DIM_TRACK];
DROP TABLE IF EXISTS [dbo].[DIM_CUSTOMER];
DROP TABLE IF EXISTS [dbo].[DIM_EMPLOYEE];
DROP TABLE IF EXISTS [dbo].[DIM_ALBUM];
DROP TABLE IF EXISTS [dbo].[DIM_ARTIST];
DROP TABLE IF EXISTS [dbo].[DIM_GENRE];
DROP TABLE IF EXISTS [dbo].[DIM_MEDIATYPE];
DROP TABLE IF EXISTS [dbo].[DIM_CHANNEL];
DROP TABLE IF EXISTS [dbo].[DIM_DATE];
GO -- Supprimer nouvelle table de faits si déjà créée
    DROP TABLE IF EXISTS [dbo].[FAIT_VENTE];
DROP TABLE IF EXISTS [dbo].[DIM_PISTE];
DROP TABLE IF EXISTS [dbo].[DIM_CLIENT];
DROP TABLE IF EXISTS [dbo].[DIM_EMPLOYE];
DROP TABLE IF EXISTS [dbo].[DIM_CANAL];
GO PRINT 'Anciens objets supprimés avec succès.';
PRINT '';
GO PRINT '================================================';
PRINT ' ÉTAPE 2 : Création des dimensions';
PRINT '================================================';
-- ─────────────────────────────────────────────────────────────
-- DIM_DATE : Dimension temporelle (hiérarchie complète pour Power BI)
-- ─────────────────────────────────────────────────────────────
CREATE TABLE [dbo].[DIM_DATE] (
    [TK_DATE] INT NOT NULL,
    -- Format YYYYMMDD (ex: 20090101)
    [DATE_COMPLETE] DATE NOT NULL,
    [NUMERO_JOUR] INT NOT NULL,
    [NUMERO_MOIS] INT NOT NULL,
    [NOM_MOIS] NVARCHAR(20) NOT NULL,
    -- "Janvier", "Février"...
    [MOIS_COURT] NVARCHAR(5) NOT NULL,
    -- "Jan", "Fév"...
    [NUMERO_TRIMESTRE] INT NOT NULL,
    [LIBELLE_TRIMESTRE] NVARCHAR(5) NOT NULL,
    -- "T1", "T2", "T3", "T4"
    [NUMERO_ANNEE] INT NOT NULL,
    [ANNEE_MOIS] NVARCHAR(7) NOT NULL,
    -- "2009-01" (pour tri chronologique)
    [NUMERO_SEMAINE] INT NOT NULL,
    [NOM_JOUR] NVARCHAR(15) NOT NULL,
    -- "Lundi", "Mardi"...
    [NUMERO_JOUR_SEMAINE] INT NOT NULL,
    -- 1=Lundi ... 7=Dimanche
    CONSTRAINT [PK_DIM_DATE] PRIMARY KEY CLUSTERED ([TK_DATE])
);
GO -- ─────────────────────────────────────────────────────────────
    -- DIM_CANAL : Dimension canal de vente
    -- ─────────────────────────────────────────────────────────────
    CREATE TABLE [dbo].[DIM_CANAL] (
        [TK_CANAL] INT IDENTITY(1, 1) NOT NULL,
        [CODE_CANAL] INT NOT NULL,
        [LIBELLE] NVARCHAR(50) NOT NULL,
        -- "En ligne" / "Magasin physique"
        [SOURCE_DONNEES] NVARCHAR(100) NOT NULL,
        -- "Chinook" / "Magasin"
        CONSTRAINT [PK_DIM_CANAL] PRIMARY KEY CLUSTERED ([TK_CANAL])
    );
GO -- Insérer les 2 canaux fixes
INSERT INTO [dbo].[DIM_CANAL] ([CODE_CANAL], [LIBELLE], [SOURCE_DONNEES])
VALUES (1, N'En ligne', N'Chinook');
INSERT INTO [dbo].[DIM_CANAL] ([CODE_CANAL], [LIBELLE], [SOURCE_DONNEES])
VALUES (2, N'Magasin physique', N'Magasin');
GO -- ─────────────────────────────────────────────────────────────
    -- DIM_EMPLOYE : Dimension employé (conseiller commercial)
    -- ─────────────────────────────────────────────────────────────
    CREATE TABLE [dbo].[DIM_EMPLOYE] (
        [TK_EMPLOYE] INT IDENTITY(1, 1) NOT NULL,
        [NK_ID_EMPLOYE] INT NOT NULL,
        [NOM] NVARCHAR(20),
        [PRENOM] NVARCHAR(20),
        [FONCTION] NVARCHAR(30),
        [VILLE] NVARCHAR(40),
        [PAYS] NVARCHAR(40),
        CONSTRAINT [PK_DIM_EMPLOYE] PRIMARY KEY CLUSTERED ([TK_EMPLOYE])
    );
GO -- ─────────────────────────────────────────────────────────────
    -- DIM_CLIENT : Dimension client (avec référence à l'employé conseiller)
    -- SCD2 : on historise les changements d'adresse/pays
    -- ─────────────────────────────────────────────────────────────
    CREATE TABLE [dbo].[DIM_CLIENT] (
        [TK_CLIENT] INT IDENTITY(1, 1) NOT NULL,
        [NK_ID_CLIENT] INT NOT NULL,
        [PRENOM] NVARCHAR(40),
        [NOM] NVARCHAR(20),
        [VILLE] NVARCHAR(40),
        [PAYS] NVARCHAR(40),
        [TK_EMPLOYE] INT NULL,
        -- FK vers DIM_EMPLOYE (conseiller)
        [DATE_DEBUT] DATE NOT NULL,
        [DATE_FIN] DATE NULL,
        -- NULL = enregistrement actif
        [ACTIF] BIT NOT NULL DEFAULT 1,
        CONSTRAINT [PK_DIM_CLIENT] PRIMARY KEY CLUSTERED ([TK_CLIENT])
    );
GO CREATE INDEX [IX_DIM_CLIENT_NK_ACTIF] ON [dbo].[DIM_CLIENT] ([NK_ID_CLIENT], [ACTIF]);
GO -- ─────────────────────────────────────────────────────────────
    -- DIM_PISTE : Dimension produit DÉNORMALISÉE (Étoile pure)
    --   Contient : Genre + Album + Artiste + Type Média directement
    --   SCD2 sur PRIX_UNITAIRE (l'attribut qui change)
    -- ─────────────────────────────────────────────────────────────
    CREATE TABLE [dbo].[DIM_PISTE] (
        [TK_PISTE] INT IDENTITY(1, 1) NOT NULL,
        [NK_ID_PISTE] INT NOT NULL,
        -- Attributs de la piste
        [NOM_PISTE] NVARCHAR(200),
        [COMPOSITEUR] NVARCHAR(220),
        [DUREE_MS] INT,
        [TAILLE_OCTETS] INT,
        -- Attributs dénormalisés (Genre, Album, Artiste, Média)
        [NOM_GENRE] NVARCHAR(120),
        [NOM_ALBUM] NVARCHAR(160),
        [NOM_ARTISTE] NVARCHAR(120),
        [NOM_TYPE_MEDIA] NVARCHAR(120),
        -- ✅ NOUVEAU : Playlist dénormalisée (pas de flocon)
        [NB_PLAYLISTS] INT NULL,
        -- Nb de playlists contenant la piste
        [NOM_PLAYLISTS] NVARCHAR(500) NULL,
        -- ex: "Music | Rock | Top 50"
        -- SCD2 : attribut suivi
        [PRIX_UNITAIRE] NUMERIC(10, 2) NOT NULL,
        -- Colonnes SCD2 obligatoires
        [DATE_DEBUT] DATE NOT NULL,
        [DATE_FIN] DATE NULL,
        [ACTIF] BIT NOT NULL DEFAULT 1,
        CONSTRAINT [PK_DIM_PISTE] PRIMARY KEY CLUSTERED ([TK_PISTE])
    );
GO CREATE INDEX [IX_DIM_PISTE_NK_ACTIF] ON [dbo].[DIM_PISTE] ([NK_ID_PISTE], [ACTIF]);
GO PRINT '================================================';
PRINT ' ÉTAPE 3 : Création de la table de faits unique';
PRINT '================================================';
-- ─────────────────────────────────────────────────────────────
-- FAIT_VENTE : Table de faits centrale (une ligne = une ligne de vente)
--   Toutes les clés étrangères pointent DIRECTEMENT vers les dimensions
--   Pas de relation Fait→Fait
-- ─────────────────────────────────────────────────────────────
CREATE TABLE [dbo].[FAIT_VENTE] (
    [TK_VENTE] INT IDENTITY(1, 1) NOT NULL,
    -- Clés étrangères vers les 5 dimensions
    [TK_DATE] INT NOT NULL,
    -- → DIM_DATE
    [TK_PISTE] INT NOT NULL,
    -- → DIM_PISTE (version active au moment de la vente)
    [TK_CLIENT] INT NOT NULL,
    -- → DIM_CLIENT
    [TK_EMPLOYE] INT NULL,
    -- → DIM_EMPLOYE (peut être NULL pour magasin)
    [TK_CANAL] INT NOT NULL,
    -- → DIM_CANAL
    -- Clés naturelles (traçabilité vers ODS)
    [NK_FACTURE] INT NOT NULL,
    -- InvoiceId original
    [NK_LIGNE_FACTURE] INT NOT NULL,
    -- InvoiceLineId original
    -- Mesures
    [QUANTITE] INT NOT NULL,
    [PRIX_UNITAIRE] NUMERIC(10, 2) NOT NULL,
    [TOTAL_LIGNE] NUMERIC(10, 2) NOT NULL,
    [MONTANT_FACTURE] NUMERIC(10, 2) NOT NULL,
    -- Total de la facture (répété par ligne)
    -- Traçabilité
    [DATE_CHARGEMENT] DATETIME2 NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_FAIT_VENTE] PRIMARY KEY CLUSTERED ([TK_VENTE])
);
GO PRINT '================================================';
PRINT ' ÉTAPE 4 : Création des clés étrangères';
PRINT '================================================';
ALTER TABLE [dbo].[FAIT_VENTE]
ADD CONSTRAINT [FK_FAIT_VENTE_DIM_DATE] FOREIGN KEY ([TK_DATE]) REFERENCES [dbo].[DIM_DATE] ([TK_DATE]);
GO
ALTER TABLE [dbo].[FAIT_VENTE]
ADD CONSTRAINT [FK_FAIT_VENTE_DIM_PISTE] FOREIGN KEY ([TK_PISTE]) REFERENCES [dbo].[DIM_PISTE] ([TK_PISTE]);
GO
ALTER TABLE [dbo].[FAIT_VENTE]
ADD CONSTRAINT [FK_FAIT_VENTE_DIM_CLIENT] FOREIGN KEY ([TK_CLIENT]) REFERENCES [dbo].[DIM_CLIENT] ([TK_CLIENT]);
GO
ALTER TABLE [dbo].[FAIT_VENTE]
ADD CONSTRAINT [FK_FAIT_VENTE_DIM_EMPLOYE] FOREIGN KEY ([TK_EMPLOYE]) REFERENCES [dbo].[DIM_EMPLOYE] ([TK_EMPLOYE]);
GO
ALTER TABLE [dbo].[FAIT_VENTE]
ADD CONSTRAINT [FK_FAIT_VENTE_DIM_CANAL] FOREIGN KEY ([TK_CANAL]) REFERENCES [dbo].[DIM_CANAL] ([TK_CANAL]);
GO
ALTER TABLE [dbo].[DIM_CLIENT]
ADD CONSTRAINT [FK_DIM_CLIENT_DIM_EMPLOYE] FOREIGN KEY ([TK_EMPLOYE]) REFERENCES [dbo].[DIM_EMPLOYE] ([TK_EMPLOYE]);
GO PRINT 'Clés étrangères créées.';
PRINT '';
GO PRINT '================================================';
PRINT ' ÉTAPE 5 : Remplissage de DIM_DATE (2009-2025)';
PRINT '================================================';
DECLARE @Date DATE = '2009-01-01';
DECLARE @DateFin DATE = '2025-12-31';
WHILE @Date <= @DateFin BEGIN
INSERT INTO [dbo].[DIM_DATE] (
        [TK_DATE],
        [DATE_COMPLETE],
        [NUMERO_JOUR],
        [NUMERO_MOIS],
        [NOM_MOIS],
        [MOIS_COURT],
        [NUMERO_TRIMESTRE],
        [LIBELLE_TRIMESTRE],
        [NUMERO_ANNEE],
        [ANNEE_MOIS],
        [NUMERO_SEMAINE],
        [NOM_JOUR],
        [NUMERO_JOUR_SEMAINE]
    )
VALUES (
        YEAR(@Date) * 10000 + MONTH(@Date) * 100 + DAY(@Date),
        @Date,
        DAY(@Date),
        MONTH(@Date),
        DATENAME(MONTH, @Date),
        LEFT(DATENAME(MONTH, @Date), 3),
        DATEPART(QUARTER, @Date),
        'T' + CAST(DATEPART(QUARTER, @Date) AS NVARCHAR(1)),
        YEAR(@Date),
        FORMAT(@Date, 'yyyy-MM'),
        DATEPART(WEEK, @Date),
        DATENAME(WEEKDAY, @Date),
        DATEPART(WEEKDAY, @Date)
    );
SET @Date = DATEADD(DAY, 1, @Date);
END;
GO PRINT 'DIM_DATE remplie.';
PRINT '';
GO PRINT '================================================';
PRINT ' VÉRIFICATION FINALE';
PRINT '================================================';
SELECT 'DIM_DATE' AS [Table],
    COUNT(*) AS [Lignes]
FROM [dbo].[DIM_DATE]
UNION ALL
SELECT 'DIM_CANAL',
    COUNT(*)
FROM [dbo].[DIM_CANAL]
UNION ALL
SELECT 'DIM_EMPLOYE',
    COUNT(*)
FROM [dbo].[DIM_EMPLOYE]
UNION ALL
SELECT 'DIM_CLIENT',
    COUNT(*)
FROM [dbo].[DIM_CLIENT]
UNION ALL
SELECT 'DIM_PISTE',
    COUNT(*)
FROM [dbo].[DIM_PISTE]
UNION ALL
SELECT 'FAIT_VENTE',
    COUNT(*)
FROM [dbo].[FAIT_VENTE];
GO PRINT '';
PRINT '================================================';
PRINT ' NOUVEAU SCHÉMA EN ÉTOILE CRÉÉ AVEC SUCCÈS';
PRINT '';
PRINT '  FAIT_VENTE (centre)';
PRINT '    ├── DIM_DATE    (TK_DATE)';
PRINT '    ├── DIM_PISTE   (TK_PISTE) - SCD2 sur PRIX_UNITAIRE';
PRINT '    ├── DIM_CLIENT  (TK_CLIENT) → DIM_EMPLOYE';
PRINT '    ├── DIM_EMPLOYE (TK_EMPLOYE)';
PRINT '    └── DIM_CANAL   (TK_CANAL)';
PRINT '';
PRINT '  Prochaine étape : exécuter 08_CHARGER_DWH_DEPUIS_ODS.sql';
PRINT '================================================';
GO