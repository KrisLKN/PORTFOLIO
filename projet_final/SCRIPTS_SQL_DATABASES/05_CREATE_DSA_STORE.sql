/*******************************************************************************
   Création des tables DSA_STORE
   Structure pour les ventes en magasin physique
********************************************************************************/

USE [DSA_STORE_LOKOUN_THYS];
GO

-- Table Invoice (ventes magasin)
-- NOTE: CHANNEL_ID = 2 pour identifier que ces données viennent de la source "Magasin" (ventes en magasin physique)
CREATE TABLE [dbo].[Invoice]
(
    [InvoiceId] INT NOT NULL,
    [CustomerId] INT NOT NULL,
    [InvoiceDate] DATETIME NOT NULL,
    [BillingAddress] NVARCHAR(70),
    [BillingCity] NVARCHAR(40),
    [BillingState] NVARCHAR(40),
    [BillingCountry] NVARCHAR(40),
    [BillingPostalCode] NVARCHAR(10),
    [Total] NUMERIC(10,2) NOT NULL,
    [InvoiceDateCre] DATETIME2,
    [CHANNEL_ID] INT NOT NULL DEFAULT 2,  -- 2 = Source Magasin (Magasin physique)
    CONSTRAINT [PK_Invoice] PRIMARY KEY CLUSTERED ([InvoiceId]),
    CONSTRAINT [CK_Invoice_Channel_Store] CHECK ([CHANNEL_ID] = 2)  -- Vérification que CHANNEL_ID = 2 pour DSA_STORE
);
GO

-- Table InvoiceLine
CREATE TABLE [dbo].[InvoiceLine]
(
    [InvoiceLineId] INT NOT NULL,
    [InvoiceId] INT NOT NULL,
    [TrackId] INT NOT NULL,
    [UnitPrice] NUMERIC(10,2) NOT NULL,
    [Quantity] INT NOT NULL,
    [InvoiceLineDate] DATETIME2,
    CONSTRAINT [PK_InvoiceLine] PRIMARY KEY CLUSTERED ([InvoiceLineId])
);
GO

PRINT 'Tables DSA_STORE créées avec succès';
PRINT 'NOTE: Toutes les factures dans DSA_STORE ont CHANNEL_ID = 2 (Source: Magasin - Magasin physique)';
GO
