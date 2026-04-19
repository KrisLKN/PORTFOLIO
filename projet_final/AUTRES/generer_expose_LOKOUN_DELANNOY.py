# -*- coding: utf-8 -*-
"""
Generateur PDF - EXPOSE SSIS - LOKOUN Kris & Romain DELANNOY
BUT SD Semestre 4 - Mars 2026
Composant principal : SCD Type 2 (Wizard SSIS natif)
"""
from fpdf import FPDF
import os

BASE = r'C:\Users\LOKOUN Kris\Desktop\BUT 2\SAE DATA\S4\projet_final'
IMG_DIR = os.path.join(BASE, 'IMAGES_RAPPORT')
SCD2_DIR = os.path.join(BASE, 'SCD2')
LOGO_UNIV = os.path.join(IMG_DIR, 'Logotype_Universit\u00e9_de_Lille_2022.png')
LOGO_IUT = os.path.join(IMG_DIR, 'Recadrage-logos-site-web-IUT-ROUBAIX-768x456.png')
M_LEFT, M_RIGHT, M_TOP, M_BOTTOM = 20, 20, 25, 25
PAGE_W = 210
CW = PAGE_W - M_LEFT - M_RIGHT
BLEU = (0, 51, 102)
BINOME = 'Kris LOKOUN et Romain DELANNOY'
PIED = 'LOKOUN Kris - DELANNOY Romain - BUT SD S4'

def s(t):
    for o, n in {'\u2013':'-','\u2014':'-','\u2018':"'",'\u2019':"'",'\u201c':'"','\u201d':'"','\u2026':'...','\u2022':'-','\u2192':'->','\u00b7':'.'}.items():
        t = t.replace(o, n)
    return t

def img(n): return os.path.join(IMG_DIR, n)
def scd(n): return os.path.join(SCD2_DIR, n)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.fig_num = 0
    def header(self):
        if self.page_no() == 1: return
        self.set_font('Times','I',8); self.set_text_color(100,100,100)
        self.set_xy(M_LEFT,8); self.cell(CW,5,s('Expos\u00e9 SSIS - SCD Type 2 (Wizard)'),0,0,'L')
        self.set_draw_color(*BLEU); self.set_line_width(0.3)
        self.line(M_LEFT,M_TOP-4,PAGE_W-M_RIGHT,M_TOP-4); self.set_xy(M_LEFT,M_TOP)
    def footer(self):
        if self.page_no() == 1: return
        self.set_y(-M_BOTTOM+5); self.set_draw_color(180,180,180); self.set_line_width(0.2)
        self.line(M_LEFT,297-M_BOTTOM+2,PAGE_W-M_RIGHT,297-M_BOTTOM+2)
        self.set_font('Times','I',8); self.set_text_color(120,120,120); self.set_x(M_LEFT)
        self.cell(CW/2,8,PIED,0,0,'L'); self.cell(CW/2,8,str(self.page_no()),0,0,'R')
    def saut(self, h=40):
        if self.get_y() > 297 - M_BOTTOM - h: self.add_page()
    def t1(self, num, titre):
        self.saut(20); self.set_font('Times','B',16); self.set_text_color(*BLEU)
        self.set_x(M_LEFT); self.cell(CW,10,s(num+'. '+titre),0,1,'L')
        y=self.get_y(); self.set_draw_color(*BLEU); self.set_line_width(0.4)
        self.line(M_LEFT,y,M_LEFT+60,y); self.set_text_color(0,0,0); self.ln(5)
    def t2(self, num, titre):
        self.saut(15); self.set_font('Times','B',13); self.set_text_color(*BLEU)
        self.set_x(M_LEFT); self.cell(CW,8,s(num+'. '+titre),0,1,'L')
        self.set_text_color(0,0,0); self.ln(2)
    def t3(self, l, titre):
        self.saut(12); self.set_font('Times','B',11); self.set_text_color(30,30,30)
        self.set_x(M_LEFT+5); self.cell(CW-5,7,s(l+'. '+titre),0,1,'L')
        self.set_text_color(0,0,0); self.ln(1)
    def tl(self, titre):
        self.saut(10); self.set_font('Times','B',11); self.set_text_color(30,30,30)
        self.set_x(M_LEFT+5); self.cell(CW-5,7,s(titre),0,1,'L')
        self.set_text_color(0,0,0); self.ln(1)
    def p(self, t):
        self.set_font('Times','',11); self.set_text_color(0,0,0)
        self.set_x(M_LEFT); self.multi_cell(CW,6,s(t),0,'J'); self.ln(2)
    def b(self, t):
        self.set_font('Times','',11); self.set_text_color(0,0,0)
        self.set_x(M_LEFT+8); self.multi_cell(CW-8,6,s('- '+t),0,'J'); self.ln(1)
    def bg(self, label, t):
        self.set_font('Times','B',11); self.set_x(M_LEFT+8)
        lw=self.get_string_width(s(label+' : '))+2
        self.cell(lw,6,s(label+' : '),0,0); self.set_font('Times','',11)
        self.multi_cell(CW-8-lw,6,s(t),0,'J'); self.ln(1)
    def code(self, t):
        self.set_font('Courier','',8); self.set_fill_color(245,245,245)
        for l in t.split('\n'):
            self.saut(5); self.set_x(M_LEFT+5); self.cell(CW-10,4.5,s('  '+l),0,1,'L',True)
        self.set_font('Times','',11); self.ln(3)
    def tab(self, hd, rows, cw=None):
        if cw is None: w=CW/len(hd); cw=[w]*len(hd)
        self.saut(12+len(rows)*8)
        self.set_font('Times','B',9); self.set_fill_color(*BLEU); self.set_text_color(255,255,255)
        self.set_x(M_LEFT)
        for i,h in enumerate(hd): self.cell(cw[i],7,s(h),1,0,'C',True)
        self.ln(); self.set_font('Times','',9); self.set_text_color(0,0,0); alt=False
        for row in rows:
            self.saut(8)
            self.set_fill_color(235,240,248) if alt else self.set_fill_color(255,255,255)
            self.set_x(M_LEFT)
            for i,c in enumerate(row): self.cell(cw[i],7,s(str(c)[:60]),1,0,'L',True)
            self.ln(); alt=not alt
        self.ln(3)
    def fig(self, path, leg, w=120):
        self.fig_num += 1; self.saut(50)
        if os.path.exists(path):
            try:
                x=M_LEFT+(CW-w)/2; self.image(path,x=x,w=w); self.ln(2)
            except: self.p('[Image non chargeable : '+os.path.basename(path)+']')
        else: self.p('[Image manquante : '+os.path.basename(path)+']')
        self.set_font('Times','I',9); self.set_text_color(80,80,80); self.set_x(M_LEFT)
        self.multi_cell(CW,4,s('Figure '+str(self.fig_num)+' : '+leg),0,'C')
        self.set_text_color(0,0,0); self.ln(4)
    def garde(self):
        self.add_page()
        for logo,x in [(LOGO_UNIV,30),(LOGO_IUT,125)]:
            if os.path.exists(logo):
                try: self.image(logo,x=x,y=25,w=55)
                except: pass
        self.set_y(70); self.set_font('Times','',12); self.set_text_color(100,100,100)
        self.set_x(M_LEFT); self.cell(CW,7,s('Universit\u00e9 de Lille - BUT SD - Semestre 4 - 2025/2026'),0,1,'C')
        self.ln(10); self.set_draw_color(0,0,0); self.set_line_width(0.5)
        self.line(50,self.get_y(),160,self.get_y()); self.ln(10)
        self.set_font('Times','B',18); self.set_text_color(0,0,0); self.set_x(M_LEFT)
        self.cell(CW,12,'R4.VCOD08 / R4.EMS09',0,1,'C'); self.ln(3)
        self.set_font('Times','B',22); self.set_x(M_LEFT)
        self.multi_cell(CW,12,s('Expos\u00e9 SSIS'),0,'C'); self.ln(3)
        self.set_font('Times','I',14); self.set_text_color(60,60,60); self.set_x(M_LEFT)
        self.multi_cell(CW,8,s('Slowly Changing Dimension Type 2\n(Composant natif SSIS)'),0,'C')
        self.set_text_color(0,0,0); self.ln(10)
        self.line(50,self.get_y(),160,self.get_y()); self.ln(15)
        self.set_font('Times','',13); self.set_x(M_LEFT); self.cell(CW,8,'Par',0,1,'C')
        self.set_font('Times','B',14); self.set_x(M_LEFT); self.cell(CW,10,BINOME,0,1,'C')
        self.ln(8); self.set_font('Times','',12); self.set_x(M_LEFT)
        self.cell(CW,7,'Sous la direction de',0,1,'C')
        self.set_font('Times','B',12); self.set_x(M_LEFT); self.cell(CW,7,s('M. Le V\u00e9ler'),0,1,'C')
        self.ln(15); self.set_font('Times','I',11); self.set_text_color(100,100,100)
        self.set_x(M_LEFT); self.cell(CW,7,s('Date de d\u00e9p\u00f4t : Mars 2026'),0,1,'C')
        self.set_text_color(0,0,0)
    def tdm(self, items, pm=None):
        self.add_page(); self.set_font('Times','B',18); self.set_text_color(*BLEU)
        self.set_x(M_LEFT); self.cell(CW,12,s('Table des mati\u00e8res'),0,1,'C')
        y=self.get_y(); self.set_draw_color(*BLEU); self.set_line_width(0.3)
        self.line(PAGE_W/2-25,y,PAGE_W/2+25,y); self.set_text_color(0,0,0); self.ln(10)
        for lv,num,titre,key in items:
            if lv==1: self.set_font('Times','B',12); ind=0
            elif lv==2: self.set_font('Times','',11); ind=10
            else: self.set_font('Times','',10); ind=20
            lab=s(num+' '+titre); lw2=self.get_string_width(lab)
            ps=str(pm[key]) if pm and key in pm else ''
            pw=self.get_string_width(ps) if ps else 0
            av=CW-ind-lw2-pw-4; dw=self.get_string_width('.')
            nd=max(3,int(av/dw)) if dw>0 else 3
            self.set_x(M_LEFT+ind); self.cell(lw2,6,lab,0,0,'L')
            self.set_font('Times','',8); self.set_text_color(150,150,150)
            self.cell(av+2,6,' '+'.'*nd+' ',0,0,'R')
            self.set_font('Times','B' if lv==1 else '',12 if lv==1 else 11)
            self.set_text_color(0,0,0); self.cell(pw+2,6,ps,0,1,'R')

TDM = [
    (1,'I.','Contexte et jeu de donn\u00e9es','I'),
    (1,'II.','Composant Niveau 1 : Execute SQL Task','II'),
    (1,'III.','Composant Niveau 1 : Row Count','III'),
    (1,'IV.','Composant Niveau 2 : Derived Column','IV'),
    (1,'V.','Composant Niveau 2 : Union All','V'),
    (1,'VI.','Composant Niveau 3 : SCD Type 2 (Wizard SSIS)','VI'),
    (2,'A.','Qu\'est-ce que le SCD Type 2 ?','VI.A'),
    (2,'B.','Pourquoi le Wizard SSIS ?','VI.B'),
    (2,'C.','Configuration pas \u00e0 pas','VI.C'),
    (2,'D.','Flux g\u00e9n\u00e9r\u00e9 et r\u00e9sultat','VI.D'),
    (1,'VII.','D\u00e9monstration SSIS','VII'),
    (2,'A.','Orchestration du projet','VII.A'),
    (2,'B.','Ex\u00e9cution et v\u00e9rification','VII.B'),
    (1,'VIII.','Param\u00e8tre dynamique','VIII'),
]

def build(save=True, toc=None):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=M_BOTTOM)
    pdf.set_left_margin(M_LEFT); pdf.set_right_margin(M_RIGHT)
    pm = {}

    # PAGE DE GARDE
    pdf.garde()
    pdf.tdm(TDM, toc)

    # =================================================================
    # I. CONTEXTE ET JEU DE DONNEES (1 min de l'expose)
    # =================================================================
    pdf.add_page()
    pm['I'] = pdf.page_no()
    pdf.t1('I', 'Contexte et jeu de donn\u00e9es')

    pdf.tl('Le probl\u00e8me \u00e0 r\u00e9soudre')
    pdf.p(
        "Une entreprise de musique vend ses produits via deux canaux : "
        "un site de vente en ligne (base Chinook, 11 tables) et un magasin physique "
        "(base Magasin, 2 tables, convertie d'Oracle vers SQL Server). "
        "Le probl\u00e8me : les donn\u00e9es sont dispers\u00e9es dans deux syst\u00e8mes "
        "diff\u00e9rents, ce qui rend impossible toute analyse globale des ventes. "
        "De plus, les prix des pistes musicales changent r\u00e9guli\u00e8rement, "
        "et l'entreprise veut pouvoir analyser l'impact de ces changements sur le chiffre d'affaires.")
    pdf.p(
        "Notre mission : construire une cha\u00eene ETL (Extract, Transform, Load) compl\u00e8te "
        "avec SSIS pour fusionner ces deux sources dans un Data Warehouse unique, "
        "tout en conservant l'historique des changements de prix.")

    pdf.tl('Architecture ETL en 3 couches')
    pdf.p(
        "Le projet suit une architecture en 3 couches, chacune ayant un r\u00f4le pr\u00e9cis :")
    pdf.bg('Couche 1 - DSA (Data Staging Area)',
           "zone tampon o\u00f9 les donn\u00e9es sont copi\u00e9es telles quelles depuis "
           "les sources. On vide la table (TRUNCATE) puis on ins\u00e8re tout. "
           "C'est ici qu'on ajoute une date de chargement et un identifiant de canal "
           "(1=Online, 2=Store). 13 packages SSIS chargent cette couche.")
    pdf.bg('Couche 2 - ODS (Operational Data Store)',
           "les donn\u00e9es sont nettoy\u00e9es et enrichies avec une colonne LOAD_DATE "
           "pour la tra\u00e7abilit\u00e9. Un m\u00e9canisme anti-doublon (Lookup) "
           "emp\u00eache de r\u00e9ins\u00e9rer une ligne d\u00e9j\u00e0 pr\u00e9sente.")
    pdf.bg('Couche 3 - DWH (Data Warehouse)',
           "les donn\u00e9es sont transform\u00e9es en mod\u00e8le en \u00e9toile "
           "(dimensions + faits) pour l'analyse d\u00e9cisionnelle. C'est ici que le "
           "SCD Type 2 g\u00e8re l'historique des prix dans DIM_TRACK.")
    pdf.code(
        'Chinook (11 tables)  ---->  DSA_ONLINE  --->  ODS_ONLINE  ---\\\n'
        '                                                              --> DWH (etoile)\n'
        'Magasin (2 tables)   ---->  DSA_STORE   --->  ODS_STORE   ---/')

    pdf.tl('Le jeu de donn\u00e9es final')
    pdf.tab(
        ['Table DWH', 'Contenu', 'Lignes'],
        [['DIM_TRACK','Pistes musicales (SCD2 : historique prix)','3503+'],
         ['DIM_CUSTOMER','Clients','59'],
         ['DIM_DATE','Calendrier g\u00e9n\u00e9r\u00e9 automatiquement','1884'],
         ['DIM_CHANNEL','Canaux (Online=1, Store=2)','2'],
         ['DIM_GENRE / ARTIST / ALBUM','R\u00e9f\u00e9rentiels musicaux','25/275/347'],
         ['FACT_INVOICE_LINE','Lignes de facture (Online+Store)','4757'],
        ],[55,80,35])
    pdf.p(
        "Ce jeu de donn\u00e9es n'est pas trivial : deux sources h\u00e9t\u00e9rog\u00e8nes "
        "\u00e0 fusionner, des changements de prix \u00e0 historiser, et des volumes "
        "suffisants pour illustrer chaque composant SSIS.")

    # =================================================================
    # II. EXECUTE SQL TASK (Niveau 1)
    # =================================================================
    pdf.add_page()
    pm['II'] = pdf.page_no()
    pdf.t1('II', 'Composant Niveau 1 : Execute SQL Task')

    pdf.tl('Qu\'est-ce que c\'est ?')
    pdf.p(
        "L'Execute SQL Task est un composant du Control Flow (flux de contr\u00f4le) "
        "qui permet d'ex\u00e9cuter une requ\u00eate SQL directement, sans passer par "
        "un Data Flow Task. Il est utile pour les op\u00e9rations qui ne n\u00e9cessitent "
        "pas de transformation ligne par ligne : cr\u00e9ation de tables, vidage "
        "(TRUNCATE), insertions en masse, ou ex\u00e9cution de scripts complexes.")

    pdf.tl('O\u00f9 et pourquoi on l\'a utilis\u00e9 dans le projet')
    pdf.p(
        "On l'utilise dans le package 03_LOAD_DIM_DATE.dtsx pour g\u00e9n\u00e9rer "
        "automatiquement toutes les dates du calendrier dans la dimension DIM_DATE. "
        "Pourquoi un Execute SQL Task et pas un Data Flow ? Parce que les dates ne "
        "viennent pas d'une source existante : elles sont calcul\u00e9es \u00e0 la vol\u00e9e "
        "par une CTE r\u00e9cursive (boucle en SQL). Un Data Flow serait inutilement "
        "complexe pour une op\u00e9ration purement SQL.")
    pdf.p(
        "Le script SQL fait 3 choses : (1) il cherche la date minimum et maximum "
        "dans les 4 tables ODS, (2) il g\u00e9n\u00e8re toutes les dates entre ces "
        "deux bornes avec une CTE r\u00e9cursive, (3) il utilise un MERGE pour "
        "n'ins\u00e9rer que les dates manquantes (pas de doublons si on relance).")

    pdf.tl('Param\u00e8tres configur\u00e9s')
    pdf.tab(
        ['Param\u00e8tre', 'Valeur', 'Pourquoi'],
        [['Connection', 'DWH_COMMON', 'Pointe vers le Data Warehouse'],
         ['SQLStatement', 'Script MERGE + CTE', 'G\u00e9n\u00e8re et ins\u00e8re les dates'],
         ['ResultSet', 'None', 'Pas besoin de retourner de r\u00e9sultat'],
         ['MAXRECURSION', '10000', 'SQL Server limite \u00e0 100 par d\u00e9faut'],
        ],[40,45,85])
    pdf.fig(img('EDITEUR_EXECUTE_SQL_TASK_DIM_DATE.png'),
            "\u00c9diteur de l'Execute SQL Task : script MERGE + CTE r\u00e9cursive", 115)

    # =================================================================
    # III. ROW COUNT (Niveau 1)
    # =================================================================
    pdf.add_page()
    pm['III'] = pdf.page_no()
    pdf.t1('III', 'Composant Niveau 1 : Row Count')

    pdf.tl('Qu\'est-ce que c\'est ?')
    pdf.p(
        "Le Row Count est un composant tr\u00e8s simple du Data Flow : il compte "
        "le nombre de lignes qui passent dans le flux et stocke ce nombre dans une "
        "variable SSIS. Il ne modifie pas les donn\u00e9es, il les laisse passer.")

    pdf.tl('O\u00f9 et pourquoi on l\'a utilis\u00e9 dans le projet')
    pdf.p(
        "On l'a plac\u00e9 dans chacun des 13 packages DSA, entre la transformation "
        "(Derived Column) et la destination (OLE DB Destination). Pourquoi ? "
        "Pour le contr\u00f4le qualit\u00e9. Apr\u00e8s chaque ex\u00e9cution, "
        "on peut v\u00e9rifier que le nombre de lignes charg\u00e9es correspond "
        "aux attentes. Par exemple : Track = 3503 lignes, Album = 347, Artist = 275. "
        "Si la variable vaut 0, on sait imm\u00e9diatement que quelque chose ne va pas "
        "(source vide, mapping incorrect, connexion \u00e9chou\u00e9e).")
    pdf.p("Le flux DSA typique est donc :")
    pdf.code(
        'OLE DB Source (table Chinook)\n'
        '    --> Derived Column (ajout TrackDate + CHANNEL_ID)\n'
        '        --> Row Count (stocke dans User::RowCount_Track)\n'
        '            --> OLE DB Destination (table DSA)')
    pdf.fig(img('LOAD_DSA_TRACK.png'),
            "Package DSA Track : le Row Count est plac\u00e9 avant la destination", 115)

    # =================================================================
    # IV. DERIVED COLUMN (Niveau 2)
    # =================================================================
    pdf.add_page()
    pm['IV'] = pdf.page_no()
    pdf.t1('IV', 'Composant Niveau 2 : Derived Column')

    pdf.tl('Qu\'est-ce que c\'est ?')
    pdf.p(
        "Le Derived Column (Colonne D\u00e9riv\u00e9e) est le couteau suisse du Data Flow. "
        "Il permet de cr\u00e9er de nouvelles colonnes ou de remplacer des colonnes "
        "existantes en utilisant des expressions SSIS (GETDATE(), constantes, calculs, "
        "conversions de types, concat\u00e9nations, etc.).")

    pdf.tl('O\u00f9 et pourquoi on l\'a utilis\u00e9 dans le projet')
    pdf.p(
        "C'est le composant le plus utilis\u00e9 de tout le projet : "
        "plus de 30 occurrences dans les 3 couches. Voici ses utilisations concr\u00e8tes :")

    pdf.bg('En couche DSA (13 packages)',
           "dans chaque package DSA, un Derived Column ajoute 2 colonnes : "
           "(1) une date de chargement via l'expression GETDATE(), "
           "et (2) un CHANNEL_ID constant (1 pour Online, 2 pour Store). "
           "Ces colonnes permettent de savoir QUAND et D'O\u00d9 vient chaque ligne.")
    pdf.bg('En couche ODS',
           "un Derived Column ajoute une colonne LOAD_DATE = GETDATE() "
           "pour la tra\u00e7abilit\u00e9 (savoir quand la donn\u00e9e a \u00e9t\u00e9 "
           "charg\u00e9e dans l'ODS).")
    pdf.bg('En couche DWH (SCD2)',
           "3 Derived Columns diff\u00e9rents dans le flux DIM_TRACK : "
           "(1) pr\u00e9paration des colonnes avec DATE_DEBUT=GETDATE() et ACTIF=True, "
           "(2) pr\u00e9paration pour fermer l'ancienne version (ACTIF=False), "
           "(3) pr\u00e9paration pour la nouvelle version.")
    pdf.fig(img('EDITEUR_DERIVED_COLUMN_DSA.png'),
            "\u00c9diteur Derived Column : expressions GETDATE() et CHANNEL_ID=1", 115)
    pdf.p(
        "Chaque param\u00e8tre est justifi\u00e9 : GETDATE() n'est pas choisi au hasard, "
        "c'est la date/heure exacte d'ex\u00e9cution du package, ce qui permet de tracer "
        "pr\u00e9cis\u00e9ment le moment du chargement. Le CHANNEL_ID permet de distinguer "
        "les donn\u00e9es Online des donn\u00e9es Store apr\u00e8s fusion dans le DWH.")

    # =================================================================
    # V. UNION ALL (Niveau 2)
    # =================================================================
    pdf.add_page()
    pm['V'] = pdf.page_no()
    pdf.t1('V', 'Composant Niveau 2 : Union All')

    pdf.tl('Qu\'est-ce que c\'est ?')
    pdf.p(
        "Le Union All combine les lignes venant de plusieurs entr\u00e9es en une seule "
        "sortie. Il concat\u00e8ne simplement les flux, sans tri, sans d\u00e9doublonnage. "
        "Chaque entr\u00e9e doit avoir les m\u00eames colonnes (ou des colonnes compatibles).")

    pdf.tl('O\u00f9 et pourquoi on l\'a utilis\u00e9 dans le projet')
    pdf.p(
        "On l'utilise dans les packages de chargement des tables de faits : "
        "03_LOAD_FACT_INVOICE.dtsx et 03_LOAD_FACT_INVOICE_LINE.dtsx. "
        "Le probl\u00e8me \u00e0 r\u00e9soudre : les ventes en ligne (ODS_ONLINE) et "
        "les ventes en magasin (ODS_STORE) sont dans deux bases diff\u00e9rentes, "
        "mais doivent \u00eatre fusionn\u00e9es dans une seule table de faits du DWH.")
    pdf.code(
        'SRC_INVOICE_ODS_ONLINE -----\\\n'
        '                             >--- UNION ALL ---> Lookups TK ---> FACT_INVOICE_LINE\n'
        'SRC_INVOICE_ODS_STORE  -----/')
    pdf.p(
        "Pourquoi Union All et pas Merge ? Parce que nos donn\u00e9es ne sont pas "
        "tri\u00e9es et n'ont pas besoin de l'\u00eatre. Union All est plus simple, "
        "plus rapide, et accepte un nombre illimit\u00e9 d'entr\u00e9es. "
        "Apr\u00e8s la fusion, des Lookups r\u00e9cup\u00e8rent les cl\u00e9s techniques "
        "(TK_DATE, TK_PISTE, TK_CLIENT) pour compl\u00e9ter la table de faits.")
    pdf.fig(img('UNION_ALL_INVOICELINE.png'),
            "Union All fusionnant Online et Store dans FACT_INVOICE_LINE", 115)
    pdf.fig(img('LOAD_INVOICELINE.png'),
            "Flux complet : Union All --> Lookups TK --> Destination", 125)

    # =================================================================
    # VI. SCD TYPE 2 (Niveau 3 - COMPOSANT PRINCIPAL)
    # =================================================================
    pdf.add_page()
    pm['VI'] = pdf.page_no()
    pdf.t1('VI', 'Composant Niveau 3 : SCD Type 2 (Wizard SSIS)')

    pm['VI.A'] = pdf.page_no()
    pdf.t2('A', 'Qu\'est-ce que le SCD Type 2 ?')
    pdf.p(
        "Dans un Data Warehouse, une dimension peut changer au fil du temps. "
        "Par exemple, le prix d'une piste musicale passe de 0.99 \u00e0 0.49. "
        "La question est : que fait-on de l'ancien prix ?")
    pdf.p(
        "Avec un SCD Type 1 (simple UPDATE), on \u00e9crase l'ancien prix avec le nouveau. "
        "R\u00e9sultat : l'historique est perdu d\u00e9finitivement, et il est impossible "
        "de savoir quel prix \u00e9tait en vigueur lors des ventes pass\u00e9es.")
    pdf.p(
        "Avec un SCD Type 2 (notre choix), on conserve les deux versions dans la table. "
        "L'ancienne ligne est marqu\u00e9e comme expir\u00e9e (ACTIF = False), "
        "et une nouvelle ligne est cr\u00e9\u00e9e avec le nouveau prix (ACTIF = True). "
        "R\u00e9sultat : on peut analyser le CA avec les prix d'origine ET les prix actuels.")
    pdf.tab(
        ['', 'SCD Type 1 (UPDATE)', 'SCD Type 2 (notre choix)'],
        [['Action','Ecrase l\'ancien','Conserve + cr\u00e9e nouveau'],
         ['Historique','Perdu','Pr\u00e9serv\u00e9'],
         ['Colonnes','Aucune en plus','ACTIF (True/False)'],
         ['Nb lignes','Constant','Augmente (+1 par changement)'],
         ['Analyse CA','Impossible avant/apr\u00e8s','Comparaison possible'],
        ],[30,55,85])

    pm['VI.B'] = pdf.page_no()
    pdf.t2('B', 'Pourquoi le Wizard SSIS (et pas l\'impl\u00e9mentation manuelle) ?')
    pdf.p(
        "SSIS propose un composant natif appel\u00e9 Slowly Changing Dimension Wizard. "
        "C'est un assistant graphique qui, en quelques \u00e9tapes de configuration, "
        "g\u00e9n\u00e8re automatiquement tout le flux n\u00e9cessaire au SCD Type 2 : "
        "les Derived Columns, les OLE DB Commands, le Union All, et la Destination.")
    pdf.p(
        "L'avantage par rapport \u00e0 une impl\u00e9mentation manuelle "
        "(o\u00f9 il faut cha\u00eener soi-m\u00eame Lookup + Conditional Split + "
        "OLE DB Command + plusieurs Derived Columns) est la rapidit\u00e9 de mise en place "
        "et la fiabilit\u00e9 : le Wizard g\u00e9n\u00e8re un flux valid\u00e9 par Microsoft, "
        "sans risque d'erreur de c\u00e2blage entre composants.")

    pm['VI.C'] = pdf.page_no()
    pdf.t2('C', 'Configuration pas \u00e0 pas du Wizard')

    pdf.tl('\u00c9tape 1 : Connexion \u00e0 la source')
    pdf.p(
        "On configure l'OLE DB Source pour lire les pistes depuis l'ODS "
        "(LocalHost.ODS_ONLINE_LOKOUN_THYS). C'est la source de donn\u00e9es "
        "qui alimente le SCD.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 222547.png"),
            "OLE DB Source : connexion \u00e0 l'ODS", 105)

    pdf.tl('\u00c9tape 2 : S\u00e9lection de la table de dimension et des cl\u00e9s')
    pdf.p(
        "Le Wizard demande quelle table de dimension g\u00e9rer (DIM_TRACK dans le DWH) "
        "et quelle colonne est la Business Key (cl\u00e9 m\u00e9tier). "
        "La Business Key permet au Wizard d'identifier chaque enregistrement unique. "
        "Ici, c'est NK_ID_PISTE qui correspond au TrackId de la source.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 231819.png"),
            "S\u00e9lection de DIM_TRACK et mapping des colonnes", 105)

    pdf.tl('\u00c9tape 3 : Types de colonnes (le coeur du param\u00e9trage)')
    pdf.p(
        "C'est l'\u00e9tape la plus importante. Chaque colonne de la dimension "
        "re\u00e7oit un type qui dit au Wizard comment r\u00e9agir en cas de changement :")
    pdf.bg('Historical Attribute (Type 2)',
           "UNIT_PRICE. Si le prix change, le Wizard cr\u00e9e une nouvelle ligne "
           "et marque l'ancienne comme expir\u00e9e. C'est le SCD Type 2.")
    pdf.bg('Changing Attribute (Type 1)',
           "NOM_PISTE, NOM_ALBUM, NOM_ARTISTE, NOM_GENRE, NOM_TYPE_MEDIA, "
           "COMPOSER, DURATION_MS, FILESIZE_BYTES. Si ces valeurs changent, "
           "le Wizard les met \u00e0 jour directement (UPDATE simple).")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 232816.png"),
            "Configuration : UNIT_PRICE en Historical, les autres en Changing", 105)

    pdf.tl('\u00c9tape 4 : Options des attributs')
    pdf.p(
        "Pour les Changing Attributes, le Wizard propose de mettre \u00e0 jour "
        "tous les enregistrements correspondants (y compris les versions obsol\u00e8tes). "
        "On active cette option pour garantir la coh\u00e9rence des donn\u00e9es.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 232945.png"),
            "Options : mise \u00e0 jour de tous les enregistrements", 100)

    pdf.tl('\u00c9tape 5 : Options de l\'attribut Historical')
    pdf.p(
        "Le Wizard propose deux mani\u00e8res d'identifier la version courante d'un "
        "enregistrement : (1) une colonne unique (ACTIF = True/False), ou "
        "(2) des colonnes de dates (DATE_DEBUT / DATE_FIN). "
        "Nous utilisons la m\u00e9thode 1 avec la colonne ACTIF : "
        "True = version courante, False = version expir\u00e9e.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 233906.png"),
            "Colonne ACTIF : True = courant, False = expir\u00e9", 100)

    pdf.tl('\u00c9tape 6 : Membres inf\u00e9r\u00e9s')
    pdf.p(
        "Les Inferred Members g\u00e8rent le cas o\u00f9 une table de faits "
        "r\u00e9f\u00e9rence une dimension pas encore charg\u00e9e. "
        "Le Wizard ins\u00e8re une ligne temporaire (avec des NULL) qui sera "
        "compl\u00e9t\u00e9e automatiquement plus tard.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 234142.png"),
            "Inferred Dimension Members : support activ\u00e9", 100)

    pdf.tl('\u00c9tape 7 : R\u00e9sum\u00e9 et g\u00e9n\u00e9ration')
    pdf.p("Le Wizard affiche les 3 sorties qu'il va g\u00e9n\u00e9rer :")
    pdf.b('New Record Output : les pistes qui n\'existent pas encore -> INSERT')
    pdf.b('Changing Attributes Updates Output : les pistes dont le nom ou '
          'les m\u00e9tadonn\u00e9es ont chang\u00e9 -> UPDATE (Type 1)')
    pdf.b('Historical Attribute Output : les pistes dont le prix a chang\u00e9 '
          '-> FERMETURE ancienne version + INSERT nouvelle version (Type 2)')
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 234244.png"),
            "R\u00e9sum\u00e9 du Wizard : 3 sorties g\u00e9n\u00e9r\u00e9es automatiquement", 100)

    pm['VI.D'] = pdf.page_no()
    pdf.t2('D', 'Flux g\u00e9n\u00e9r\u00e9 et r\u00e9sultat')
    pdf.p(
        "Apr\u00e8s avoir cliqu\u00e9 sur Finish, le Wizard g\u00e9n\u00e8re automatiquement "
        "un flux complet dans le Data Flow. Ce flux contient : "
        "la transformation SCD (qui fait le Lookup + le routage), "
        "des Derived Columns (pour pr\u00e9parer les valeurs ACTIF), "
        "des OLE DB Commands (pour UPDATE les anciennes versions), "
        "un Union All (pour regrouper les sorties), et une Destination d'insertion.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 234424.png"),
            "Flux Data Flow g\u00e9n\u00e9r\u00e9 automatiquement par le Wizard SCD", 110)
    pdf.p(
        "Le mapping final dans la destination montre que chaque colonne d'entr\u00e9e "
        "est correctement associ\u00e9e \u00e0 sa colonne de destination dans DIM_TRACK. "
        "La cl\u00e9 technique TK_PISTE est g\u00e9n\u00e9r\u00e9e automatiquement "
        "par IDENTITY (auto-incr\u00e9ment) et n'a donc pas besoin d'\u00eatre mapp\u00e9e "
        "en entr\u00e9e.")
    pdf.fig(scd("Capture d'\u00e9cran 2026-03-03 235438.png"),
            "Mapping OLE DB Destination : colonnes vers DIM_TRACK", 110)

    # =================================================================
    # VII. DEMONSTRATION SSIS
    # =================================================================
    pdf.add_page()
    pm['VII'] = pdf.page_no()
    pdf.t1('VII', 'D\u00e9monstration SSIS')

    pm['VII.A'] = pdf.page_no()
    pdf.t2('A', 'Orchestration du projet')
    pdf.p(
        "Le package 00_RUN_ALL.dtsx orchestre l'ensemble de l'ETL. "
        "Il ex\u00e9cute les 3 sous-packages dans l'ordre : "
        "RUN_DSA (13 packages) -> RUN_ODS -> RUN_DWH (10 packages). "
        "Si une \u00e9tape \u00e9choue, les suivantes ne s'ex\u00e9cutent pas.")
    pdf.fig(img('RUN_ALL_ETL.png'),
            "Package 00_RUN_ALL : ex\u00e9cution s\u00e9quentielle DSA -> ODS -> DWH", 125)

    pm['VII.B'] = pdf.page_no()
    pdf.t2('B', 'Ex\u00e9cution et v\u00e9rification du SCD2')

    pdf.tl('Test : modification de 48 prix dans la source')
    pdf.p(
        "Pour prouver que le SCD2 fonctionne, nous avons modifi\u00e9 le prix "
        "de 48 pistes dans la base source Chinook (UnitPrice de 0.99 \u00e0 0.49) "
        "puis re-ex\u00e9cut\u00e9 l'ETL complet. R\u00e9sultat attendu : "
        "dans DIM_TRACK, chaque piste modifi\u00e9e doit appara\u00eetre en 2 versions.")
    pdf.fig(img('LOAD_DIM_TRACK_EXUTOION COMPLETE ET FONCTIONNELLE.png'),
            "Ex\u00e9cution r\u00e9ussie du flux SCD2 : compteurs sur les fl\u00e8ches", 115)
    pdf.fig(img('RESULTAT_SCD2_SSMS_SIMPLE.png'),
            "R\u00e9sultat dans SSMS : AVANT (0.99, ACTIF=False) et APRES (0.49, ACTIF=True)", 130)

    pdf.tl('Coh\u00e9rence des donn\u00e9es v\u00e9rifi\u00e9e')
    pdf.p(
        "Le nombre de lignes reste constant \u00e0 travers les couches "
        "(Source = DSA = ODS = DWH), sauf DIM_TRACK qui augmente de 48 lignes "
        "gr\u00e2ce au SCD2 (3503 actives + 48 historis\u00e9es = 3551).")
    pdf.fig(img('SUIVI_EVOLUTION PAR_COUCHE.png'),
            "Suivi par couche : z\u00e9ro perte de donn\u00e9es", 130)

    # =================================================================
    # VIII. PARAMETRE DYNAMIQUE
    # =================================================================
    pdf.add_page()
    pm['VIII'] = pdf.page_no()
    pdf.t1('VIII', 'Param\u00e8tre dynamique')
    pdf.p(
        "Conform\u00e9ment \u00e0 la consigne, chaque flux inclut au moins un "
        "param\u00e8tre dynamique. Dans notre projet, la variable SSIS "
        "User::NomTableDimension contr\u00f4le le nom de la table de dimension "
        "cibl\u00e9e par le Wizard SCD (par d\u00e9faut : DIM_TRACK).")
    pdf.p(
        "En modifiant cette variable, on peut r\u00e9utiliser le m\u00eame package "
        "pour g\u00e9rer le SCD Type 2 sur une autre dimension (par exemple DIM_CUSTOMER "
        "si on voulait historiser les changements d'adresse). De m\u00eame, la variable "
        "User::NomBaseODS permet de changer la base source sans modifier le code du package.")
    pdf.tab(
        ['Variable SSIS', 'Valeur par d\u00e9faut', 'Effet si modifi\u00e9e'],
        [['User::NomTableDimension','DIM_TRACK','Change la table cible du SCD'],
         ['User::NomBaseODS','ODS_ONLINE_LOKOUN_THYS','Change la source de donn\u00e9es'],
         ['User::RowCount_Track','(calcul\u00e9)','Stocke le nb de lignes charg\u00e9es'],
         ['User::ChannelID','1 ou 2','Identifie le canal (Online/Store)'],
        ],[45,55,70])
    pdf.p(
        "Ce param\u00e9trage rend le package r\u00e9utilisable : "
        "il suffit de modifier les variables pour l'adapter \u00e0 un autre environnement "
        "ou \u00e0 d'autres donn\u00e9es, sans toucher au flux SSIS lui-m\u00eame.")

    # ---- GENERER ----
    if save:
        out = os.path.join(BASE, 'EXPOSE_SSIS_LOKOUN_DELANNOY.pdf')
        try: pdf.output(out)
        except PermissionError:
            out = os.path.join(BASE, 'EXPOSE_SSIS_LOKOUN_DELANNOY_v2.pdf')
            pdf.output(out)
        print('EXPOSE : ' + out)
        print('  Pages : ' + str(pdf.page_no()) + ', Figures : ' + str(pdf.fig_num))
        return pdf.page_no(), pdf.fig_num
    else: return pm

def generer():
    pm = build(save=False)
    return build(save=True, toc=pm)

if __name__ == '__main__':
    print('='*60)
    print('EXPOSE SSIS - LOKOUN Kris & Romain DELANNOY')
    print('='*60)
    p, f = generer()
    print('='*60)
    print(f'RESULTAT : {p} pages, {f} figures')
    print('='*60)
