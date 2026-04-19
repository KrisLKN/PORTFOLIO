/*******************************************************************************
   CHARGEMENT DU DWH FLOCON DEPUIS LES ODS
   Base    : DWH_COMMON_LOKOUN_THYS
   Auteurs : LOKOUN / THYS

   Prérequis : Avoir exécuté 04_CREATE_DWH_COMMON.sql

   ORDRE DE CHARGEMENT (respecter les dépendances FK) :
   ─────────────────────────────────────────────────────
   1. DIM_ARTISTE     ← ODS_ONLINE : Artist
   2. DIM_GENRE       ← ODS_ONLINE : Genre
   3. DIM_TYPE_MEDIA  ← ODS_ONLINE : MediaType
   4. DIM_EMPLOYE     ← ODS_ONLINE : Employee
   5. DIM_ALBUM       ← ODS_ONLINE : Album       (dépend de DIM_ARTISTE)
   6. DIM_CLIENT      ← ODS_ONLINE : Customer    (dépend de DIM_EMPLOYE)
   7. DIM_PISTE       ← ODS_ONLINE : Track       (dépend de DIM_ALBUM, DIM_GENRE, DIM_TYPE_MEDIA) + SCD2
   8. DIM_PLAYLIST    ← ODS_ONLINE : Playlist
   9. PONT_PLAYLIST_PISTE ← ODS_ONLINE : PlaylistTrack (dépend de DIM_PLAYLIST, DIM_PISTE)
  10. FAIT_VENTE      ← ODS_ONLINE : Invoice + InvoiceLine (canal 1)
                      ← ODS_STORE  : Invoice + InvoiceLine (canal 2)
********************************************************************************/

USE [DWH_COMMON_LOKOUN_THYS];
GO

PRINT '================================================================';
PRINT ' Chargement DWH FLOCON depuis ODS';
PRINT '================================================================';
PRINT '';


-- ============================================================
-- ÉTAPE 1 : DIM_ARTISTE
-- ============================================================
PRINT 'Étape 1/10 : Chargement DIM_ARTISTE...';

DELETE FROM [dbo].[DIM_ARTISTE];

INSERT INTO [dbo].[DIM_ARTISTE] ([NK_ID_ARTISTE], [NOM_ARTISTE])
SELECT [ArtistId], [Name]
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Artist];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' artistes.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 2 : DIM_GENRE
-- ============================================================
PRINT 'Étape 2/10 : Chargement DIM_GENRE...';

DELETE FROM [dbo].[DIM_GENRE];

INSERT INTO [dbo].[DIM_GENRE] ([NK_ID_GENRE], [NOM_GENRE])
SELECT [GenreId], [Name]
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Genre];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' genres.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 3 : DIM_TYPE_MEDIA
-- ============================================================
PRINT 'Étape 3/10 : Chargement DIM_TYPE_MEDIA...';

DELETE FROM [dbo].[DIM_TYPE_MEDIA];

INSERT INTO [dbo].[DIM_TYPE_MEDIA] ([NK_ID_TYPE_MEDIA], [NOM_TYPE_MEDIA])
SELECT [MediaTypeId], [Name]
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[MediaType];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' types de média.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 4 : DIM_EMPLOYE
-- ============================================================
PRINT 'Étape 4/10 : Chargement DIM_EMPLOYE...';

DELETE FROM [dbo].[DIM_EMPLOYE];

INSERT INTO [dbo].[DIM_EMPLOYE]
    ([NK_ID_EMPLOYE], [NOM], [PRENOM], [FONCTION], [VILLE], [PAYS])
SELECT
    [EmployeeId], [LastName], [FirstName], [Title], [City], [Country]
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Employee];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' employés.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 5 : DIM_ALBUM (dépend de DIM_ARTISTE)
-- ============================================================
PRINT 'Étape 5/10 : Chargement DIM_ALBUM...';

DELETE FROM [dbo].[DIM_ALBUM];

INSERT INTO [dbo].[DIM_ALBUM] ([NK_ID_ALBUM], [TITRE_ALBUM], [TK_ARTISTE])
SELECT
    a.[AlbumId],
    a.[Title],
    art.[TK_ARTISTE]       -- Résolution NK → TK
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Album] a
LEFT JOIN [dbo].[DIM_ARTISTE] art ON a.[ArtistId] = art.[NK_ID_ARTISTE];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' albums.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 6 : DIM_CLIENT (dépend de DIM_EMPLOYE)
-- SCD2 : chargement initial — tous actifs
-- ============================================================
PRINT 'Étape 6/10 : Chargement DIM_CLIENT (SCD2)...';

DELETE FROM [dbo].[DIM_CLIENT];

INSERT INTO [dbo].[DIM_CLIENT]
    ([NK_ID_CLIENT], [PRENOM], [NOM], [VILLE], [PAYS],
     [TK_EMPLOYE], [DATE_DEBUT], [DATE_FIN], [ACTIF])
SELECT
    c.[CustomerId],
    c.[FirstName],
    c.[LastName],
    c.[City],
    c.[Country],
    emp.[TK_EMPLOYE],
    CAST(ISNULL(c.[CustomerDate], '2009-01-01') AS DATE),
    NULL,
    1
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Customer] c
LEFT JOIN [dbo].[DIM_EMPLOYE] emp ON c.[SupportRepId] = emp.[NK_ID_EMPLOYE];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' clients (version initiale active).';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 7 : DIM_PISTE (dépend de DIM_ALBUM, DIM_GENRE, DIM_TYPE_MEDIA)
-- SCD2 sur PRIX_UNITAIRE
-- ============================================================
PRINT 'Étape 7/10 : Chargement DIM_PISTE (SCD2)...';

-- Source complète avec résolution des TK
SELECT
    t.[TrackId]                                              AS NK_ID_PISTE,
    t.[Name]                                                 AS NOM_PISTE,
    t.[Composer]                                             AS COMPOSITEUR,
    t.[Milliseconds]                                         AS DUREE_MS,
    t.[Bytes]                                                AS TAILLE_OCTETS,
    alb.[TK_ALBUM],
    g.[TK_GENRE],
    mt.[TK_TYPE_MEDIA],
    t.[UnitPrice]                                            AS PRIX_UNITAIRE,
    CAST(ISNULL(t.[TrackDate], '2009-01-01') AS DATE)        AS DATE_DEBUT
INTO #SRC_PISTE
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Track] t
LEFT JOIN [dbo].[DIM_ALBUM]      alb ON t.[AlbumId]     = alb.[NK_ID_ALBUM]
LEFT JOIN [dbo].[DIM_GENRE]      g   ON t.[GenreId]     = g.[NK_ID_GENRE]
LEFT JOIN [dbo].[DIM_TYPE_MEDIA] mt  ON t.[MediaTypeId] = mt.[NK_ID_TYPE_MEDIA];
GO

-- 7a : Nouvelles pistes → INSERT initial
INSERT INTO [dbo].[DIM_PISTE]
    ([NK_ID_PISTE],[NOM_PISTE],[COMPOSITEUR],[DUREE_MS],[TAILLE_OCTETS],
     [TK_ALBUM],[TK_GENRE],[TK_TYPE_MEDIA],
     [PRIX_UNITAIRE],[DATE_DEBUT],[DATE_FIN],[ACTIF])
SELECT
    s.[NK_ID_PISTE],s.[NOM_PISTE],s.[COMPOSITEUR],s.[DUREE_MS],s.[TAILLE_OCTETS],
    s.[TK_ALBUM],s.[TK_GENRE],s.[TK_TYPE_MEDIA],
    s.[PRIX_UNITAIRE],s.[DATE_DEBUT],NULL,1
FROM #SRC_PISTE s
WHERE s.[NK_ID_PISTE] NOT IN (SELECT [NK_ID_PISTE] FROM [dbo].[DIM_PISTE]);
GO

DECLARE @nb_piste_new INT = @@ROWCOUNT;
PRINT '  → ' + CAST(@nb_piste_new AS NVARCHAR) + ' nouvelles pistes insérées.';
GO

-- 7b : Prix modifiés → SCD2 (fermer ancienne version)
UPDATE p
SET [DATE_FIN] = CAST(GETDATE() AS DATE), [ACTIF] = 0
FROM [dbo].[DIM_PISTE] p
INNER JOIN #SRC_PISTE s ON p.[NK_ID_PISTE] = s.[NK_ID_PISTE]
WHERE p.[ACTIF] = 1
  AND ABS(CAST(p.[PRIX_UNITAIRE] AS FLOAT) - CAST(s.[PRIX_UNITAIRE] AS FLOAT)) > 0.001;
GO

DECLARE @nb_piste_hist INT = @@ROWCOUNT;
PRINT '  → ' + CAST(@nb_piste_hist AS NVARCHAR) + ' pistes historisées (prix modifié).';
GO

-- 7c : Insérer nouvelle version active pour les pistes historisées
INSERT INTO [dbo].[DIM_PISTE]
    ([NK_ID_PISTE],[NOM_PISTE],[COMPOSITEUR],[DUREE_MS],[TAILLE_OCTETS],
     [TK_ALBUM],[TK_GENRE],[TK_TYPE_MEDIA],
     [PRIX_UNITAIRE],[DATE_DEBUT],[DATE_FIN],[ACTIF])
SELECT
    s.[NK_ID_PISTE],s.[NOM_PISTE],s.[COMPOSITEUR],s.[DUREE_MS],s.[TAILLE_OCTETS],
    s.[TK_ALBUM],s.[TK_GENRE],s.[TK_TYPE_MEDIA],
    s.[PRIX_UNITAIRE],CAST(GETDATE() AS DATE),NULL,1
FROM #SRC_PISTE s
WHERE s.[NK_ID_PISTE] NOT IN (SELECT [NK_ID_PISTE] FROM [dbo].[DIM_PISTE] WHERE [ACTIF]=1);
GO

DECLARE @nb_piste_v2 INT = @@ROWCOUNT;
PRINT '  → ' + CAST(@nb_piste_v2 AS NVARCHAR) + ' nouvelles versions SCD2.';

DROP TABLE IF EXISTS #SRC_PISTE;
GO

PRINT '';
GO


-- ============================================================
-- ÉTAPE 8 : DIM_PLAYLIST
-- ============================================================
PRINT 'Étape 8/10 : Chargement DIM_PLAYLIST...';

DELETE FROM [dbo].[DIM_PLAYLIST];

INSERT INTO [dbo].[DIM_PLAYLIST] ([NK_ID_PLAYLIST], [NOM_PLAYLIST])
SELECT [PlaylistId], [Name]
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[Playlist];
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' playlists.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 9 : PONT_PLAYLIST_PISTE (bridge many-to-many)
-- Source : ODS_ONLINE.PlaylistTrack
-- ============================================================
PRINT 'Étape 9/10 : Chargement PONT_PLAYLIST_PISTE (bridge)...';

DELETE FROM [dbo].[PONT_PLAYLIST_PISTE];

INSERT INTO [dbo].[PONT_PLAYLIST_PISTE]
    ([TK_PLAYLIST], [TK_PISTE], [NK_PLAYLIST], [NK_PISTE], [DATE_CHARGEMENT])
SELECT
    pl.[TK_PLAYLIST],
    p.[TK_PISTE],
    pt.[PlaylistId],
    pt.[TrackId],
    GETDATE()
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[PlaylistTrack] pt
INNER JOIN [dbo].[DIM_PLAYLIST] pl ON pt.[PlaylistId] = pl.[NK_ID_PLAYLIST]
INNER JOIN [dbo].[DIM_PISTE]    p  ON pt.[TrackId]    = p.[NK_ID_PISTE] AND p.[ACTIF] = 1;
GO

PRINT '  → ' + CAST(@@ROWCOUNT AS NVARCHAR) + ' associations playlist-piste.';
PRINT '';
GO


-- ============================================================
-- ÉTAPE 10 : FAIT_VENTE
-- Canal 1 (En ligne)  → ODS_ONLINE
-- Canal 2 (Magasin)   → ODS_STORE
-- ============================================================
PRINT 'Étape 10/10 : Chargement FAIT_VENTE...';

DELETE FROM [dbo].[FAIT_VENTE];
GO

-- ── Canal 1 : En ligne (ODS_ONLINE) ──────────────────────────
INSERT INTO [dbo].[FAIT_VENTE]
    ([TK_DATE],[TK_PISTE],[TK_CLIENT],[TK_EMPLOYE],[TK_CANAL],
     [NK_FACTURE],[NK_LIGNE_FACTURE],
     [QUANTITE],[PRIX_UNITAIRE],[TOTAL_LIGNE],[MONTANT_FACTURE],[DATE_CHARGEMENT])
SELECT
    YEAR(inv.[InvoiceDate])*10000+MONTH(inv.[InvoiceDate])*100+DAY(inv.[InvoiceDate]),
    p.[TK_PISTE],
    c.[TK_CLIENT],
    c.[TK_EMPLOYE],
    can.[TK_CANAL],
    inv.[InvoiceId],
    il.[InvoiceLineId],
    il.[Quantity],
    il.[UnitPrice],
    CAST(il.[Quantity] AS NUMERIC(10,2)) * il.[UnitPrice],
    inv.[Total],
    GETDATE()
FROM [ODS_ONLINE_LOKOUN_THYS].[dbo].[InvoiceLine] il
INNER JOIN [ODS_ONLINE_LOKOUN_THYS].[dbo].[Invoice]  inv ON il.[InvoiceId]  = inv.[InvoiceId]
INNER JOIN [dbo].[DIM_PISTE]   p   ON il.[TrackId]    = p.[NK_ID_PISTE]  AND p.[ACTIF]  = 1
INNER JOIN [dbo].[DIM_CLIENT]  c   ON inv.[CustomerId] = c.[NK_ID_CLIENT] AND c.[ACTIF]  = 1
INNER JOIN [dbo].[DIM_CANAL]   can ON can.[CODE_CANAL] = 1
INNER JOIN [dbo].[DIM_DATE]    d   ON d.[TK_DATE] = YEAR(inv.[InvoiceDate])*10000
                                                  + MONTH(inv.[InvoiceDate])*100
                                                  + DAY(inv.[InvoiceDate]);
GO

DECLARE @n1 INT = @@ROWCOUNT;
PRINT '  → ' + CAST(@n1 AS NVARCHAR) + ' lignes (Canal En ligne).';
GO

-- ── Canal 2 : Magasin (ODS_STORE) ────────────────────────────
INSERT INTO [dbo].[FAIT_VENTE]
    ([TK_DATE],[TK_PISTE],[TK_CLIENT],[TK_EMPLOYE],[TK_CANAL],
     [NK_FACTURE],[NK_LIGNE_FACTURE],
     [QUANTITE],[PRIX_UNITAIRE],[TOTAL_LIGNE],[MONTANT_FACTURE],[DATE_CHARGEMENT])
SELECT
    YEAR(inv.[InvoiceDate])*10000+MONTH(inv.[InvoiceDate])*100+DAY(inv.[InvoiceDate]),
    p.[TK_PISTE],
    c.[TK_CLIENT],
    c.[TK_EMPLOYE],
    can.[TK_CANAL],
    inv.[InvoiceId],
    il.[InvoiceLineId],
    il.[Quantity],
    il.[UnitPrice],
    CAST(il.[Quantity] AS NUMERIC(10,2)) * il.[UnitPrice],
    inv.[Total],
    GETDATE()
FROM [ODS_STORE_LOKOUN_THYS].[dbo].[InvoiceLine] il
INNER JOIN [ODS_STORE_LOKOUN_THYS].[dbo].[Invoice]  inv ON il.[InvoiceId]  = inv.[InvoiceId]
INNER JOIN [dbo].[DIM_PISTE]   p   ON il.[TrackId]    = p.[NK_ID_PISTE]  AND p.[ACTIF]  = 1
LEFT  JOIN [dbo].[DIM_CLIENT]  c   ON inv.[CustomerId] = c.[NK_ID_CLIENT] AND c.[ACTIF]  = 1
INNER JOIN [dbo].[DIM_CANAL]   can ON can.[CODE_CANAL] = 2
INNER JOIN [dbo].[DIM_DATE]    d   ON d.[TK_DATE] = YEAR(inv.[InvoiceDate])*10000
                                                  + MONTH(inv.[InvoiceDate])*100
                                                  + DAY(inv.[InvoiceDate]);
GO

DECLARE @n2 INT = @@ROWCOUNT;
PRINT '  → ' + CAST(@n2 AS NVARCHAR) + ' lignes (Canal Magasin).';
PRINT '';
GO


-- ============================================================
-- VÉRIFICATION FINALE
-- ============================================================
PRINT '================================================================';
PRINT ' VÉRIFICATION FINALE';
PRINT '================================================================';

SELECT 'DIM_DATE'              AS [Table], COUNT(*) AS [Lignes] FROM [dbo].[DIM_DATE]
UNION ALL SELECT 'DIM_CANAL',    COUNT(*) FROM [dbo].[DIM_CANAL]
UNION ALL SELECT 'DIM_EMPLOYE',  COUNT(*) FROM [dbo].[DIM_EMPLOYE]
UNION ALL SELECT 'DIM_ARTISTE',  COUNT(*) FROM [dbo].[DIM_ARTISTE]
UNION ALL SELECT 'DIM_GENRE',    COUNT(*) FROM [dbo].[DIM_GENRE]
UNION ALL SELECT 'DIM_TYPE_MEDIA', COUNT(*) FROM [dbo].[DIM_TYPE_MEDIA]
UNION ALL SELECT 'DIM_ALBUM',    COUNT(*) FROM [dbo].[DIM_ALBUM]
UNION ALL SELECT 'DIM_CLIENT (actifs)',      COUNT(*) FROM [dbo].[DIM_CLIENT] WHERE [ACTIF]=1
UNION ALL SELECT 'DIM_CLIENT (historiques)', COUNT(*) FROM [dbo].[DIM_CLIENT] WHERE [ACTIF]=0
UNION ALL SELECT 'DIM_PISTE (actives)',      COUNT(*) FROM [dbo].[DIM_PISTE]  WHERE [ACTIF]=1
UNION ALL SELECT 'DIM_PISTE (historiques)',  COUNT(*) FROM [dbo].[DIM_PISTE]  WHERE [ACTIF]=0
UNION ALL SELECT 'DIM_PLAYLIST', COUNT(*) FROM [dbo].[DIM_PLAYLIST]
UNION ALL SELECT 'PONT_PLAYLIST_PISTE', COUNT(*) FROM [dbo].[PONT_PLAYLIST_PISTE]
UNION ALL SELECT 'FAIT_VENTE (En ligne)',  COUNT(*) FROM [dbo].[FAIT_VENTE] WHERE [TK_CANAL]=1
UNION ALL SELECT 'FAIT_VENTE (Magasin)',   COUNT(*) FROM [dbo].[FAIT_VENTE] WHERE [TK_CANAL]=2;
GO

PRINT '';
SELECT can.[LIBELLE] AS Canal,
       COUNT(*)                        AS NbLignes,
       COUNT(DISTINCT fv.[NK_FACTURE]) AS NbFactures,
       COUNT(DISTINCT fv.[TK_CLIENT])  AS NbClients,
       CAST(SUM(fv.[TOTAL_LIGNE]) AS NUMERIC(12,2)) AS CA_Total
FROM [dbo].[FAIT_VENTE] fv
INNER JOIN [dbo].[DIM_CANAL] can ON fv.[TK_CANAL]=can.[TK_CANAL]
GROUP BY can.[LIBELLE] ORDER BY can.[LIBELLE];
GO

PRINT '';
PRINT '================================================================';
PRINT ' CHARGEMENT TERMINÉ — DWH FLOCON PRÊT';
PRINT '================================================================';
GO
