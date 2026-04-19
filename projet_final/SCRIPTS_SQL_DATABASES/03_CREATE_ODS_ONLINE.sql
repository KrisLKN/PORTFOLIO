/*******************************************************************************
   Création des tables ODS_ONLINE
   Structure identique à DSA_ONLINE + colonne LOAD_DATE
********************************************************************************/

USE [ODS_ONLINE_LOKOUN_THYS];
GO

-- Table Genre
CREATE TABLE [dbo].[Genre]
(
    [GenreId] INT NOT NULL,
    [Name] NVARCHAR(120),
    [GenreDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Genre] PRIMARY KEY CLUSTERED ([GenreId])
);
GO

-- Table MediaType
CREATE TABLE [dbo].[MediaType]
(
    [MediaTypeId] INT NOT NULL,
    [Name] NVARCHAR(120),
    [MediaTypeDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_MediaType] PRIMARY KEY CLUSTERED ([MediaTypeId])
);
GO

-- Table Artist
CREATE TABLE [dbo].[Artist]
(
    [ArtistId] INT NOT NULL,
    [Name] NVARCHAR(120),
    [ArtistDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Artist] PRIMARY KEY CLUSTERED ([ArtistId])
);
GO

-- Table Employee
CREATE TABLE [dbo].[Employee]
(
    [EmployeeId] INT NOT NULL,
    [LastName] NVARCHAR(20) NOT NULL,
    [FirstName] NVARCHAR(20) NOT NULL,
    [Title] NVARCHAR(30),
    [ReportsTo] INT,
    [BirthDate] DATETIME,
    [HireDate] DATETIME,
    [Address] NVARCHAR(70),
    [City] NVARCHAR(40),
    [State] NVARCHAR(40),
    [Country] NVARCHAR(40),
    [PostalCode] NVARCHAR(10),
    [Phone] NVARCHAR(24),
    [Fax] NVARCHAR(24),
    [Email] NVARCHAR(60),
    [EmployeeDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Employee] PRIMARY KEY CLUSTERED ([EmployeeId])
);
GO

-- Table Album
CREATE TABLE [dbo].[Album]
(
    [AlbumId] INT NOT NULL,
    [Title] NVARCHAR(160) NOT NULL,
    [ArtistId] INT NOT NULL,
    [AlbumDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Album] PRIMARY KEY CLUSTERED ([AlbumId])
);
GO

-- Table Customer
CREATE TABLE [dbo].[Customer]
(
    [CustomerId] INT NOT NULL,
    [FirstName] NVARCHAR(40) NOT NULL,
    [LastName] NVARCHAR(20) NOT NULL,
    [Company] NVARCHAR(80),
    [Address] NVARCHAR(70),
    [City] NVARCHAR(40),
    [State] NVARCHAR(40),
    [Country] NVARCHAR(40),
    [PostalCode] NVARCHAR(10),
    [Phone] NVARCHAR(24),
    [Fax] NVARCHAR(24),
    [Email] NVARCHAR(60) NOT NULL,
    [SupportRepId] INT,
    [CustomerDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Customer] PRIMARY KEY CLUSTERED ([CustomerId])
);
GO

-- Table Track
CREATE TABLE [dbo].[Track]
(
    [TrackId] INT NOT NULL,
    [Name] NVARCHAR(200) NOT NULL,
    [AlbumId] INT,
    [MediaTypeId] INT NOT NULL,
    [GenreId] INT,
    [Composer] NVARCHAR(220),
    [Milliseconds] INT NOT NULL,
    [Bytes] INT,
    [UnitPrice] NUMERIC(10,2) NOT NULL,
    [TrackDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Track] PRIMARY KEY CLUSTERED ([TrackId])
);
GO

-- Table Playlist
CREATE TABLE [dbo].[Playlist]
(
    [PlaylistId] INT NOT NULL,
    [Name] NVARCHAR(120),
    [PlaylistDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_Playlist] PRIMARY KEY CLUSTERED ([PlaylistId])
);
GO

-- Table Invoice
-- NOTE: CHANNEL_ID = 1 pour identifier que ces données viennent de la source "Chinook" (ventes en ligne)
--       LOAD_DATE permet de tracer quand les données ont été chargées dans l'ODS
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
    [CHANNEL_ID] INT NOT NULL DEFAULT 1,  -- 1 = Source Chinook (En ligne)
    [LOAD_DATE] DATETIME2,                 -- Date de chargement dans l'ODS
    CONSTRAINT [PK_Invoice] PRIMARY KEY CLUSTERED ([InvoiceId]),
    CONSTRAINT [CK_Invoice_Channel_Online_ODS] CHECK ([CHANNEL_ID] = 1)  -- Vérification que CHANNEL_ID = 1 pour ODS_ONLINE
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
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_InvoiceLine] PRIMARY KEY CLUSTERED ([InvoiceLineId])
);
GO

-- Table PlaylistTrack
CREATE TABLE [dbo].[PlaylistTrack]
(
    [PlaylistId] INT NOT NULL,
    [TrackId] INT NOT NULL,
    [PlaylistTrackDate] DATETIME2,
    [LOAD_DATE] DATETIME2,
    CONSTRAINT [PK_PlaylistTrack] PRIMARY KEY CLUSTERED ([PlaylistId], [TrackId])
);
GO

PRINT 'Tables ODS_ONLINE créées avec succès';
PRINT 'NOTE: Toutes les factures dans ODS_ONLINE ont CHANNEL_ID = 1 (Source: Chinook - En ligne)';
PRINT '      La colonne LOAD_DATE permet de tracer la date de chargement dans l''ODS';
GO
