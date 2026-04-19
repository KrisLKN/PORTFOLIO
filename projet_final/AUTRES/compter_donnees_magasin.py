#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour compter le nombre de données dans les fichiers Magasin
"""

import re

print("=" * 60)
print("COMPTAGE DES DONNEES - BASE MAGASIN")
print("=" * 60)

# Compter dans le fichier Oracle source
print("\n1. FICHIER ORACLE SOURCE (S4/Magasin.sql):")
print("-" * 60)
try:
    with open('../../S4/Magasin.sql', 'r', encoding='utf-8') as f:
        oracle_lines = f.readlines()
    
    oracle_invoice = sum(1 for l in oracle_lines if 'INSERT INTO Invoice' in l and 'InvoiceLine' not in l)
    oracle_invoiceline = sum(1 for l in oracle_lines if 'INSERT INTO InvoiceLine' in l)
    
    print(f"  - INSERT Invoice:     {oracle_invoice:>5}")
    print(f"  - INSERT InvoiceLine:  {oracle_invoiceline:>5}")
    print(f"  - TOTAL INSERT:       {oracle_invoice + oracle_invoiceline:>5}")
except FileNotFoundError:
    print("  ERREUR: Fichier Oracle non trouve")

# Compter dans le fichier SQL Server converti
print("\n2. FICHIER SQL SERVER (00_CREATE_MAGASIN_DB.sql):")
print("-" * 60)
try:
    with open('00_CREATE_MAGASIN_DB.sql', 'r', encoding='utf-8') as f:
        sqlserver_lines = f.readlines()
    
    sqlserver_invoice = sum(1 for l in sqlserver_lines if 'INSERT INTO [dbo].[Invoice]' in l and 'InvoiceLine' not in l)
    sqlserver_invoiceline = sum(1 for l in sqlserver_lines if 'INSERT INTO [dbo].[InvoiceLine]' in l)
    
    print(f"  - INSERT Invoice:     {sqlserver_invoice:>5}")
    print(f"  - INSERT InvoiceLine:  {sqlserver_invoiceline:>5}")
    print(f"  - TOTAL INSERT:       {sqlserver_invoice + sqlserver_invoiceline:>5}")
except FileNotFoundError:
    print("  ERREUR: Fichier SQL Server non trouve")

# Comparaison
print("\n3. COMPARAISON:")
print("-" * 60)
try:
    oracle_invoice
    sqlserver_invoice
    if oracle_invoice == sqlserver_invoice and oracle_invoiceline == sqlserver_invoiceline:
        print("  [OK] TOUTES LES DONNEES SONT PRESENTES")
        print(f"  [OK] Invoice: {oracle_invoice} = {sqlserver_invoice}")
        print(f"  [OK] InvoiceLine: {oracle_invoiceline} = {sqlserver_invoiceline}")
    else:
        print("  [ERREUR] DIFFERENCES TROUVEES:")
        if oracle_invoice != sqlserver_invoice:
            print(f"     Invoice: Oracle={oracle_invoice}, SQL Server={sqlserver_invoice}")
        if oracle_invoiceline != sqlserver_invoiceline:
            print(f"     InvoiceLine: Oracle={oracle_invoiceline}, SQL Server={sqlserver_invoiceline}")
except NameError:
    print("  Impossible de comparer (fichiers non trouves)")

# Détails supplémentaires
print("\n4. DETAILS SUPPLEMENTAIRES:")
print("-" * 60)
try:
    # Compter les lignes totales
    print(f"  - Lignes totales Oracle:     {len(oracle_lines):>5}")
    print(f"  - Lignes totales SQL Server: {len(sqlserver_lines):>5}")
    
    # Compter les valeurs NULL
    sqlserver_null = sum(1 for l in sqlserver_lines if 'INSERT INTO' in l and 'NULL' in l)
    print(f"  - INSERT avec NULL:         {sqlserver_null:>5}")
except:
    pass

print("\n" + "=" * 60)
print("COMPTAGE TERMINE")
print("=" * 60)
