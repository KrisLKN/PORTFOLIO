/*******************************************************************************
   Script de comptage des données dans la base Magasin_LOKOUN_THYS
   Exécutez ce script APRÈS avoir créé la base avec 00_CREATE_MAGASIN_DB.sql
********************************************************************************/

USE [Magasin_LOKOUN_THYS];
GO

PRINT '============================================================';
PRINT 'COMPTAGE DES DONNEES - BASE MAGASIN_LOKOUN_THYS';
PRINT '============================================================';
PRINT '';

-- Compter les Invoices
PRINT '1. TABLE Invoice:';
PRINT '------------------------------------------------------------';
SELECT COUNT(*) AS NbInvoices FROM [dbo].[Invoice];
GO

-- Compter les InvoiceLines
PRINT '';
PRINT '2. TABLE InvoiceLine:';
PRINT '------------------------------------------------------------';
SELECT COUNT(*) AS NbInvoiceLines FROM [dbo].[InvoiceLine];
GO

-- Détails supplémentaires
PRINT '';
PRINT '3. DETAILS SUPPLEMENTAIRES:';
PRINT '------------------------------------------------------------';

-- Nombre d'Invoices avec NULL dans BillingState
SELECT COUNT(*) AS NbInvoicesAvecNULL_BillingState 
FROM [dbo].[Invoice] 
WHERE [BillingState] IS NULL;
GO

-- Nombre d'Invoices avec NULL dans BillingPostalCode
SELECT COUNT(*) AS NbInvoicesAvecNULL_BillingPostalCode 
FROM [dbo].[Invoice] 
WHERE [BillingPostalCode] IS NULL;
GO

-- Total des Invoices par pays
PRINT '';
PRINT '4. REPARTITION PAR PAYS (Top 10):';
PRINT '------------------------------------------------------------';
SELECT TOP 10 
    [BillingCountry] AS Pays,
    COUNT(*) AS NbInvoices
FROM [dbo].[Invoice]
GROUP BY [BillingCountry]
ORDER BY NbInvoices DESC;
GO

-- Total des InvoiceLines par Invoice
PRINT '';
PRINT '5. STATISTIQUES InvoiceLine:';
PRINT '------------------------------------------------------------';
SELECT 
    COUNT(*) AS TotalInvoiceLines,
    COUNT(DISTINCT [InvoiceId]) AS NbInvoicesAvecLignes,
    AVG(CAST([Quantity] AS FLOAT)) AS QuantiteMoyenne,
    SUM([UnitPrice] * [Quantity]) AS MontantTotal
FROM [dbo].[InvoiceLine];
GO

PRINT '';
PRINT '============================================================';
PRINT 'COMPTAGE TERMINE';
PRINT '============================================================';
GO
