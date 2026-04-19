# -*- coding: utf-8 -*-
"""
Generateur de PDF - RAPPORT SAE4 + EXPOSE SSIS
Projet ETL Chinook + Magasin
LOKOUN Kris & THYS Abel - BUT SD Semestre 4

V4 - Explications approfondies dans le rapport
"""

from fpdf import FPDF
import os

BASE = r'C:\Users\LOKOUN Kris\Desktop\BUT 2\SAE DATA\S4\projet_final'
IMG_DIR = os.path.join(BASE, 'IMAGES_RAPPORT')
LOGO_UNIV = os.path.join(IMG_DIR, 'Logotype_Universit\u00e9_de_Lille_2022.png')
LOGO_IUT = os.path.join(IMG_DIR, 'Recadrage-logos-site-web-IUT-ROUBAIX-768x456.png')

M_LEFT = 20
M_RIGHT = 20
M_TOP = 25
M_BOTTOM = 25
PAGE_W = 210
CONTENT_W = PAGE_W - M_LEFT - M_RIGHT

BLEU = (0, 51, 102)


def s(txt):
    reps = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u2022': '-',
        '\u2192': '->', '\u00b7': '.', '\u2019': "'",
    }
    for old, new in reps.items():
        txt = txt.replace(old, new)
    return txt


def img(nom):
    return os.path.join(IMG_DIR, nom)


# =============================================================================
class RapportPDF(FPDF):
    def __init__(self, titre_court=''):
        super().__init__()
        self.fig_num = 0
        self.titre_court = titre_court

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font('Times', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.set_xy(M_LEFT, 8)
        self.cell(CONTENT_W, 5, s(self.titre_court), 0, 0, 'L')
        self.set_draw_color(*BLEU)
        self.set_line_width(0.3)
        self.line(M_LEFT, M_TOP - 4, PAGE_W - M_RIGHT, M_TOP - 4)
        self.set_xy(M_LEFT, M_TOP)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-M_BOTTOM + 5)
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.2)
        self.line(M_LEFT, 297 - M_BOTTOM + 2, PAGE_W - M_RIGHT, 297 - M_BOTTOM + 2)
        self.set_font('Times', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W / 2, 8, 'LOKOUN Kris - THYS Abel - BUT SD S4', 0, 0, 'L')
        self.cell(CONTENT_W / 2, 8, str(self.page_no()), 0, 0, 'R')

    # ---- Titres ----
    def titre_I(self, num, titre):
        self.saut(20)
        self.set_font('Times', 'B', 16)
        self.set_text_color(*BLEU)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 10, s(num + '. ' + titre), 0, 1, 'L')
        y = self.get_y()
        self.set_draw_color(*BLEU)
        self.set_line_width(0.4)
        self.line(M_LEFT, y, M_LEFT + 60, y)
        self.set_text_color(0, 0, 0)
        self.ln(5)

    def titre_II(self, num, titre):
        self.saut(15)
        self.set_font('Times', 'B', 13)
        self.set_text_color(*BLEU)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 8, s(num + '. ' + titre), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def titre_III(self, lettre, titre):
        self.saut(12)
        self.set_font('Times', 'B', 11)
        self.set_text_color(30, 30, 30)
        self.set_x(M_LEFT + 5)
        self.cell(CONTENT_W - 5, 7, s(lettre + '. ' + titre), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def titre_libre(self, titre):
        self.saut(10)
        self.set_font('Times', 'B', 11)
        self.set_text_color(30, 30, 30)
        self.set_x(M_LEFT + 5)
        self.cell(CONTENT_W - 5, 7, s(titre), 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(1)

    # ---- Paragraphes ----
    def p(self, texte):
        self.set_font('Times', '', 11)
        self.set_text_color(0, 0, 0)
        self.set_x(M_LEFT)
        self.multi_cell(CONTENT_W, 6, s(texte), 0, 'J')
        self.ln(2)

    def p_italic(self, texte):
        self.set_font('Times', 'I', 11)
        self.set_text_color(80, 80, 80)
        self.set_x(M_LEFT)
        self.multi_cell(CONTENT_W, 6, s(texte), 0, 'J')
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def bullet(self, texte):
        self.set_font('Times', '', 11)
        self.set_text_color(0, 0, 0)
        self.set_x(M_LEFT + 8)
        self.multi_cell(CONTENT_W - 8, 6, s('- ' + texte), 0, 'J')
        self.ln(1)

    def bullet_gras(self, label, texte):
        self.set_font('Times', 'B', 11)
        self.set_x(M_LEFT + 8)
        lw = self.get_string_width(s(label + ' : ')) + 2
        self.cell(lw, 6, s(label + ' : '), 0, 0)
        self.set_font('Times', '', 11)
        self.multi_cell(CONTENT_W - 8 - lw, 6, s(texte), 0, 'J')
        self.ln(1)

    def code(self, texte):
        self.set_font('Courier', '', 8)
        self.set_fill_color(245, 245, 245)
        for line in texte.split('\n'):
            self.saut(5)
            self.set_x(M_LEFT + 5)
            self.cell(CONTENT_W - 10, 4.5, s('  ' + line), 0, 1, 'L', True)
        self.set_font('Times', '', 11)
        self.ln(3)

    def tableau(self, headers, rows, col_widths=None):
        if col_widths is None:
            w = CONTENT_W / len(headers)
            col_widths = [w] * len(headers)
        self.saut(12 + len(rows) * 8)
        self.set_font('Times', 'B', 9)
        self.set_fill_color(*BLEU)
        self.set_text_color(255, 255, 255)
        self.set_x(M_LEFT)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, s(h), 1, 0, 'C', True)
        self.ln()
        self.set_font('Times', '', 9)
        self.set_text_color(0, 0, 0)
        alt = False
        for row in rows:
            self.saut(8)
            if alt:
                self.set_fill_color(235, 240, 248)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_x(M_LEFT)
            for i, ct in enumerate(row):
                self.cell(col_widths[i], 7, s(str(ct)[:60]), 1, 0, 'L', True)
            self.ln()
            alt = not alt
        self.ln(3)

    def figure(self, chemin, legende, largeur=None):
        if largeur is None:
            largeur = 120
        self.fig_num += 1
        self.saut(50)
        if os.path.exists(chemin):
            try:
                x = M_LEFT + (CONTENT_W - largeur) / 2
                self.image(chemin, x=x, w=largeur)
                self.ln(2)
            except Exception:
                self.p('[Image non chargeable : ' + os.path.basename(chemin) + ']')
        else:
            self.p('[Image manquante : ' + os.path.basename(chemin) + ']')
        self.set_font('Times', 'I', 9)
        self.set_text_color(80, 80, 80)
        self.set_x(M_LEFT)
        self.multi_cell(CONTENT_W, 4,
                        s('Figure ' + str(self.fig_num) + ' : ' + legende), 0, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def saut(self, h=40):
        if self.get_y() > 297 - M_BOTTOM - h:
            self.add_page()

    def separateur(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        mid = PAGE_W / 2
        self.line(mid - 30, self.get_y(), mid + 30, self.get_y())
        self.ln(5)

    # ---- Page de garde ----
    def page_garde(self, titre_principal, sous_titre, sae_code, date_depot):
        self.add_page()
        if os.path.exists(LOGO_UNIV):
            try:
                self.image(LOGO_UNIV, x=30, y=25, w=55)
            except Exception:
                pass
        if os.path.exists(LOGO_IUT):
            try:
                self.image(LOGO_IUT, x=125, y=25, w=55)
            except Exception:
                pass
        self.set_y(70)
        self.set_font('Times', '', 12)
        self.set_text_color(100, 100, 100)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 7,
                  s('Universit\u00e9 de Lille - BUT SD - Semestre 4 - 2025/2026'),
                  0, 1, 'C')
        self.ln(10)
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.5)
        self.line(50, self.get_y(), 160, self.get_y())
        self.ln(10)
        self.set_font('Times', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 12, s(sae_code), 0, 1, 'C')
        self.ln(3)
        self.set_font('Times', 'B', 22)
        self.set_x(M_LEFT)
        self.multi_cell(CONTENT_W, 12, s(titre_principal), 0, 'C')
        self.ln(3)
        self.set_font('Times', 'I', 14)
        self.set_text_color(60, 60, 60)
        self.set_x(M_LEFT)
        self.multi_cell(CONTENT_W, 8, s(sous_titre), 0, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.line(50, self.get_y(), 160, self.get_y())
        self.ln(15)
        self.set_font('Times', '', 13)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 8, 'Par', 0, 1, 'C')
        self.set_font('Times', 'B', 14)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 10, 'Kris LOKOUN et Abel THYS', 0, 1, 'C')
        self.ln(8)
        self.set_font('Times', '', 12)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 7, 'Sous la direction de', 0, 1, 'C')
        self.set_font('Times', 'B', 12)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 7, s('M. Le V\u00e9ler'), 0, 1, 'C')
        self.ln(15)
        self.set_font('Times', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 7,
                  s('Date de d\u00e9p\u00f4t : ' + date_depot), 0, 1, 'C')
        self.set_text_color(0, 0, 0)

    # ---- Table des matieres avec numeros de pages ----
    def tdm(self, items, page_map=None):
        self.add_page()
        self.set_font('Times', 'B', 18)
        self.set_text_color(*BLEU)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 12, s('Table des mati\u00e8res'), 0, 1, 'C')
        y = self.get_y()
        self.set_draw_color(*BLEU)
        self.set_line_width(0.3)
        self.line(PAGE_W / 2 - 25, y, PAGE_W / 2 + 25, y)
        self.set_text_color(0, 0, 0)
        self.ln(10)
        for level, num, titre, key in items:
            if level == 1:
                self.set_font('Times', 'B', 12)
                indent = 0
            elif level == 2:
                self.set_font('Times', '', 11)
                indent = 10
            else:
                self.set_font('Times', '', 10)
                indent = 20
            label = s(num + ' ' + titre)
            label_w = self.get_string_width(label)
            page_str = ''
            if page_map and key in page_map:
                page_str = str(page_map[key])
            page_w = self.get_string_width(page_str) if page_str else 0
            avail = CONTENT_W - indent - label_w - page_w - 4
            dot_w = self.get_string_width('.')
            n_dots = max(3, int(avail / dot_w)) if dot_w > 0 else 3
            dots = ' ' + '.' * n_dots + ' '
            self.set_x(M_LEFT + indent)
            self.cell(label_w, 6, label, 0, 0, 'L')
            self.set_font('Times', '', 8)
            self.set_text_color(150, 150, 150)
            self.cell(avail + 2, 6, dots, 0, 0, 'R')
            if level == 1:
                self.set_font('Times', 'B', 12)
            else:
                self.set_font('Times', '', 11)
            self.set_text_color(0, 0, 0)
            self.cell(page_w + 2, 6, page_str, 0, 1, 'R')

    # ---- Logos outils ----
    def bloc_outil(self, chemin_logo, nom, description, x_start, y_start, w_col):
        logo_w = 22
        if os.path.exists(chemin_logo):
            try:
                logo_x = x_start + (w_col - logo_w) / 2
                self.image(chemin_logo, x=logo_x, y=y_start, w=logo_w)
            except Exception:
                pass
        self.set_xy(x_start, y_start + 24)
        self.set_font('Times', 'B', 10)
        self.set_text_color(*BLEU)
        self.cell(w_col, 5, s(nom), 0, 1, 'C')
        self.set_xy(x_start, y_start + 30)
        self.set_font('Times', '', 8)
        self.set_text_color(60, 60, 60)
        self.multi_cell(w_col, 4, s(description), 0, 'C')
        self.set_text_color(0, 0, 0)

    def section_outils(self):
        self.saut(80)
        y0 = self.get_y()
        w_col = CONTENT_W / 4
        self.bloc_outil(img('logo_sql_server.png'), 'SQL Server 2022',
                        'Moteur de BDD\n(7 bases)', M_LEFT, y0, w_col)
        self.bloc_outil(img('logo_ssis.png'), 'SSIS',
                        'Flux ETL\n(30+ packages)', M_LEFT + w_col, y0, w_col)
        self.bloc_outil(img('logo_visual_studio.png'), 'Visual Studio 2022',
                        'Conception\ndes packages', M_LEFT + 2 * w_col, y0, w_col)
        self.bloc_outil(img('logo_ssms.png'), 'SSMS',
                        'Administration\net tests SQL', M_LEFT + 3 * w_col, y0, w_col)
        self.set_y(y0 + 50)
        self.fig_num += 1
        self.set_font('Times', 'I', 9)
        self.set_text_color(80, 80, 80)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 4,
                  s('Figure ' + str(self.fig_num) +
                    ' : Outils et technologies utilis\u00e9s'), 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    # ---- MPD Chinook (dessine) ----
    def draw_chinook_mpd(self):
        self.add_page()
        self.set_font('Times', 'B', 12)
        self.set_text_color(*BLEU)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 8,
                  s('MPD de la base Chinook (11 tables)'), 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(3)

        def box(x, y, w, h, name, cols):
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.3)
            self.set_fill_color(200, 210, 225)
            self.rect(x, y, w, 6, 'FD')
            self.set_font('Helvetica', 'B', 5.5)
            self.set_text_color(0, 0, 0)
            self.set_xy(x, y)
            self.cell(w, 6, name, 0, 0, 'C')
            self.set_fill_color(255, 255, 255)
            body_h = h - 6
            self.rect(x, y + 6, w, body_h, 'FD')
            self.set_font('Helvetica', '', 4.5)
            for i, col in enumerate(cols):
                self.set_xy(x + 1, y + 7 + i * 3.5)
                pfx = 'PK ' if i == 0 else ('FK ' if 'FK' in col else '   ')
                self.cell(w - 2, 3.5, pfx + col.replace(' FK', ''), 0, 0, 'L')

        def trait(x1, y1, x2, y2):
            self.set_draw_color(100, 100, 100)
            self.set_line_width(0.25)
            self.line(x1, y1, x2, y2)

        box(20, 50, 28, 16, 'Artist', ['ArtistId', 'Name'])
        box(56, 46, 30, 24, 'Album', ['AlbumId', 'Title', 'ArtistId FK'])
        box(94, 42, 34, 42, 'Track',
            ['TrackId', 'Name', 'AlbumId FK', 'MediaTypeId FK',
             'GenreId FK', 'Composer', 'Milliseconds', 'UnitPrice'])
        box(140, 42, 28, 16, 'Genre', ['GenreId', 'Name'])
        box(140, 64, 28, 16, 'MediaType', ['MediaTypeId', 'Name'])
        box(140, 92, 28, 16, 'Playlist', ['PlaylistId', 'Name'])
        box(94, 92, 34, 16, 'PlaylistTrack', ['PlaylistId FK', 'TrackId FK'])
        box(20, 120, 34, 28, 'Customer',
            ['CustomerId', 'FirstName', 'LastName', 'Email', 'SupportRepId FK'])
        box(20, 162, 34, 24, 'Employee',
            ['EmployeeId', 'LastName', 'FirstName', 'ReportsTo FK'])
        box(68, 120, 32, 28, 'Invoice',
            ['InvoiceId', 'CustomerId FK', 'InvoiceDate', 'BillingCity', 'Total'])
        box(110, 120, 36, 28, 'InvoiceLine',
            ['InvoiceLineId', 'InvoiceId FK', 'TrackId FK', 'UnitPrice', 'Quantity'])
        trait(48, 58, 56, 58)
        trait(86, 58, 94, 58)
        trait(140, 52, 128, 52)
        trait(140, 72, 128, 72)
        trait(111, 84, 111, 92)
        trait(140, 100, 128, 100)
        trait(111, 84, 128, 120)
        trait(54, 134, 68, 134)
        trait(37, 162, 37, 148)
        trait(100, 134, 110, 134)
        self.set_y(195)
        self.set_font('Times', '', 7)
        self.set_text_color(100, 100, 100)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 4,
                  s('PK = Cl\u00e9 primaire  |  FK = Cl\u00e9 \u00e9trang\u00e8re  '
                    '|  Traits = Relations entre tables'), 0, 1, 'C')
        self.fig_num += 1
        self.set_font('Times', 'I', 9)
        self.set_text_color(80, 80, 80)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 5,
                  s('Figure ' + str(self.fig_num) +
                    ' : MPD de la base Chinook (11 tables, SQL Server)'),
                  0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    # ---- Schema en etoile DWH ----
    def draw_star_schema(self):
        self.add_page()
        self.set_font('Times', 'B', 12)
        self.set_text_color(*BLEU)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 8,
                  s('Mod\u00e8le en \u00e9toile du Data Warehouse'), 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

        def box(x, y, w, h, name, cols, is_fact=False):
            self.set_draw_color(0, 0, 0)
            self.set_line_width(0.4)
            if is_fact:
                self.set_fill_color(*BLEU)
            else:
                self.set_fill_color(200, 210, 225)
            self.rect(x, y, w, 7, 'FD')
            self.set_font('Helvetica', 'B', 6)
            if is_fact:
                self.set_text_color(255, 255, 255)
            else:
                self.set_text_color(0, 0, 0)
            self.set_xy(x, y)
            self.cell(w, 7, name, 0, 0, 'C')
            self.set_fill_color(255, 255, 255)
            self.rect(x, y + 7, w, h - 7, 'FD')
            self.set_font('Helvetica', '', 5)
            self.set_text_color(0, 0, 0)
            for i, col in enumerate(cols):
                self.set_xy(x + 1, y + 8 + i * 4)
                prefix = '(PK) ' if i == 0 else '     '
                self.cell(w - 2, 4, prefix + col, 0, 0, 'L')

        def trait(x1, y1, x2, y2):
            self.set_draw_color(100, 100, 100)
            self.set_line_width(0.3)
            self.line(x1, y1, x2, y2)

        fil_x, fil_y, fil_w, fil_h = 75, 115, 32, 35
        box(fil_x, fil_y, fil_w, fil_h, 'FACT_INVOICE_LINE',
            ['TK_LIGNE_FACTURE', 'TK_FACTURE (FK)', 'TK_PISTE (FK)',
             'TK_DATE (FK)', 'QUANTITE', 'PRIX_UNITAIRE'], True)
        fi_x, fi_y, fi_w, fi_h = 75, 170, 32, 28
        box(fi_x, fi_y, fi_w, fi_h, 'FACT_INVOICE',
            ['TK_FACTURE', 'TK_CLIENT (FK)', 'TK_DATE (FK)',
             'TK_CANAL (FK)', 'MONTANT_TOTAL'], True)
        trait(fil_x + fil_w / 2, fil_y + fil_h, fi_x + fi_w / 2, fi_y)
        box(20, 95, 32, 32, 'DIM_DATE',
            ['TK_DATE', 'DATE_COMPLETE', 'NUMERO_JOUR', 'NUMERO_MOIS',
             'NOM_MOIS', 'TRIMESTRE'])
        trait(52, 115, fil_x, fil_y + 18)
        trait(52, 118, fi_x, fi_y + 12)
        box(125, 80, 34, 50, 'DIM_TRACK (SCD2)',
            ['TK_PISTE', 'NK_ID_PISTE', 'NOM_PISTE', 'NK_ID_ALBUM',
             'NK_ID_GENRE', 'COMPOSER', 'UNIT_PRICE',
             'DATE_DEBUT', 'DATE_FIN', 'ACTIF'])
        trait(fil_x + fil_w, fil_y + 14, 125, 100)
        box(20, 170, 32, 28, 'DIM_CUSTOMER',
            ['TK_CLIENT', 'NK_ID_CLIENT', 'PRENOM', 'NOM', 'PAYS'])
        trait(fi_x, fi_y + 10, 52, 182)
        box(125, 170, 32, 24, 'DIM_CHANNEL',
            ['TK_CANAL', 'CODE_CANAL', 'LIBELLE', 'SOURCE'])
        trait(fi_x + fi_w, fi_y + 18, 125, 182)
        box(20, 50, 28, 20, 'DIM_GENRE',
            ['TK_GENRE', 'NK_ID_GENRE', 'NOM_GENRE'])
        trait(48, 65, 125, 102)
        box(165, 60, 28, 20, 'DIM_ALBUM',
            ['TK_ALBUM', 'NK_ID_ALBUM', 'TITRE'])
        trait(159, 100, 165, 70)
        box(165, 35, 28, 16, 'DIM_ARTIST',
            ['TK_ARTISTE', 'NK_ID_ARTISTE', 'NOM'])
        trait(179, 51, 179, 60)
        box(20, 210, 32, 24, 'DIM_EMPLOYEE',
            ['TK_EMPLOYE', 'NK_ID_EMPLOYE', 'NOM', 'PRENOM'])
        box(55, 50, 30, 20, 'DIM_MEDIATYPE',
            ['TK_TYPE_MEDIA', 'NK_ID_TYPE', 'NOM'])
        trait(85, 65, 125, 96)
        self.set_y(240)
        self.set_font('Times', '', 8)
        self.set_text_color(0, 0, 0)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 5,
                  s('Bleu = Tables de faits  |  Gris = Tables de dimensions  '
                    '|  SCD2 = Slowly Changing Dimension Type 2'), 0, 1, 'C')
        self.fig_num += 1
        self.set_font('Times', 'I', 9)
        self.set_text_color(80, 80, 80)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 5,
                  s('Figure ' + str(self.fig_num) +
                    ' : Mod\u00e8le en \u00e9toile DWH_COMMON_LOKOUN_THYS'),
                  0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(5)

    # ---- Bilan personnel en tableau ----
    def tableau_bilan(self, nom, items):
        self.saut(40)
        self.set_font('Times', 'B', 12)
        self.set_fill_color(*BLEU)
        self.set_text_color(255, 255, 255)
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 8, s(nom), 1, 1, 'C', True)
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.set_font('Times', '', 10)
        for item in items:
            self.saut(8)
            self.set_x(M_LEFT)
            self.cell(CONTENT_W, 7, s('  -> ' + item), 'LR', 1, 'L')
        self.set_x(M_LEFT)
        self.cell(CONTENT_W, 1, '', 'T', 1)
        self.ln(5)


# =============================================================================
# TABLE DES MATIERES
# =============================================================================
TDM_RAPPORT = [
    (1, 'I.', 'Introduction', 'I'),
    (1, 'II.', 'M\u00e9thodologie', 'II'),
    (2, '1.', 'Migration technologique', 'II.1'),
    (2, '2.', 'Construction des couches de donn\u00e9es', 'II.2'),
    (2, '3.', 'Cr\u00e9ation des flux ETL avec SSIS', 'II.3'),
    (2, '4.', 'Validation et optimisation', 'II.4'),
    (1, 'III.', 'D\u00e9tail du projet', 'III'),
    (2, '1.', 'Description du projet', 'III.1'),
    (3, 'A.', 'Contexte et continuit\u00e9 du S3', 'III.1.A'),
    (3, 'B.', 'Organisation du travail', 'III.1.B'),
    (3, 'C.', 'Outils et technologies utilis\u00e9s', 'III.1.C'),
    (2, '2.', 'Analyse initiale et mod\u00e9lisation', 'III.2'),
    (2, '3.', 'Architecture en 3 couches (DSA, ODS, DWH)', 'III.3'),
    (3, 'A.', 'Data Staging Area (DSA)', 'III.3.A'),
    (3, 'B.', 'Operational Data Store (ODS)', 'III.3.B'),
    (3, 'C.', 'Data Warehouse (DWH) et mod\u00e8le en \u00e9toile', 'III.3.C'),
    (2, '4.', 'Cr\u00e9ation des flux de donn\u00e9es avec SSIS', 'III.4'),
    (3, 'A.', 'Flux Sources vers DSA', 'III.4.A'),
    (3, 'B.', 'Flux DSA vers ODS', 'III.4.B'),
    (3, 'C.', 'Flux ODS vers DWH', 'III.4.C'),
    (2, '5.', 'Gestion du SCD Type 2 sur DIM_TRACK', 'III.5'),
    (2, '6.', 'Validation et v\u00e9rification des donn\u00e9es', 'III.6'),
    (1, 'IV.', 'Automatisation de l\'ETL', 'IV'),
    (1, 'V.', 'Difficult\u00e9s rencontr\u00e9es et solutions', 'V'),
    (1, 'VI.', 'Conclusion', 'VI'),
    (1, 'VII.', 'Bilan personnel', 'VII'),
    (1, 'VIII.', 'Remerciements', 'VIII'),
]


# =============================================================================
# CONSTRUCTION DU RAPPORT
# =============================================================================
def _build_rapport(save=True, toc_pages=None):
    pdf = RapportPDF(titre_court="SAE 4.VCOD01 - Syst\u00e8me d'Information D\u00e9cisionnel")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=M_BOTTOM)
    pdf.set_left_margin(M_LEFT)
    pdf.set_right_margin(M_RIGHT)
    pm = {}

    # PAGE DE GARDE
    pdf.page_garde(
        "Int\u00e9gration de donn\u00e9es dans un Data Warehouse",
        "Migration Oracle vers SQL Server, ajout d'une source Magasin\n"
        "et impl\u00e9mentation du SCD Type 2 avec SSIS",
        'SAE 4.VCOD01', 'Mars 2026')

    # TABLE DES MATIERES
    pdf.tdm(TDM_RAPPORT, toc_pages)

    # =================================================================
    # I. INTRODUCTION
    # =================================================================
    pdf.add_page()
    pm['I'] = pdf.page_no()
    pdf.titre_I('I', 'Introduction')

    pdf.p(
        "Dans le cadre de la SAE 4.VCOD01 (Syst\u00e8me d'Information "
        "D\u00e9cisionnel), nous poursuivons le travail initi\u00e9 au "
        "semestre 3 (SAE 3.02) en int\u00e9grant des donn\u00e9es dans un "
        "entrep\u00f4t de donn\u00e9es (Data Warehouse). Ce projet constitue "
        "la suite directe de notre travail pr\u00e9c\u00e9dent, avec des "
        "\u00e9volutions majeures tant sur le plan technologique que fonctionnel.")

    pdf.p(
        "Au semestre 3, nous avions construit une cha\u00eene ELT "
        "(Extraction, Loading, Transformation) \u00e0 partir de la seule "
        "base de donn\u00e9es Chinook, en utilisant Oracle Database et "
        "Oracle Data Integrator (ODI). Chinook est une base de donn\u00e9es "
        "transactionnelle mod\u00e9lisant un magasin de musique en ligne, "
        "comparable \u00e0 iTunes. Elle comporte 11 tables "
        "repr\u00e9sentant les diff\u00e9rentes entit\u00e9s du syst\u00e8me : "
        "les artistes (Artist), les albums (Album), les pistes musicales "
        "(Track), les genres (Genre), les types de m\u00e9dia (MediaType), "
        "les playlists (Playlist, PlaylistTrack), les clients (Customer), "
        "les employ\u00e9s (Employee), ainsi que les factures (Invoice) et "
        "leurs d\u00e9tails (InvoiceLine). Au total, la base contient "
        "environ 15 000 lignes de donn\u00e9es r\u00e9parties entre ces tables.")

    pdf.p(
        "L'architecture en trois couches (DSA, ODS, DWH) avait \u00e9t\u00e9 "
        "mise en place avec un mod\u00e8le d\u00e9cisionnel en \u00e9toile "
        "(star schema) dans le Data Warehouse. Cependant, certains aspects "
        "n'avaient pas pu \u00eatre finalis\u00e9s, notamment l'impl\u00e9mentation "
        "effective du SCD Type 2 (Slowly Changing Dimension) via l'IKM Oracle "
        "Slowly Changing Dimension, qui n'avait pas fonctionn\u00e9 comme attendu.")

    pdf.p("Au semestre 4, le projet \u00e9volue sur trois axes majeurs :")

    pdf.bullet(
        "Migration technologique : passage de l'\u00e9cosyst\u00e8me Oracle "
        "(Oracle Database + ODI) vers l'\u00e9cosyst\u00e8me Microsoft "
        "(SQL Server 2022 + SSIS). Ce changement nous permet de d\u00e9couvrir "
        "un autre ensemble d'outils largement utilis\u00e9 dans l'industrie de "
        "la Business Intelligence. SQL Server Integration Services (SSIS) est "
        "l'outil ETL int\u00e9gr\u00e9 \u00e0 la suite SQL Server, permettant "
        "de cr\u00e9er des packages de flux de donn\u00e9es visuellement dans "
        "Visual Studio.")

    pdf.bullet(
        "Ajout d'une seconde source de donn\u00e9es : la base Magasin, "
        "repr\u00e9sentant les ventes en magasin physique. Cette base, "
        "initialement fournie en syntaxe Oracle (PL/SQL), contient 2 tables "
        "(Invoice et InvoiceLine) repr\u00e9sentant environ 2 000 lignes de "
        "transactions. Le Data Warehouse doit d\u00e9sormais fusionner les "
        "deux canaux de vente (Online via Chinook et Store via Magasin) tout "
        "en maintenant la tra\u00e7abilit\u00e9 de l'origine des donn\u00e9es "
        "gr\u00e2ce \u00e0 un identifiant de canal (CHANNEL_ID).")

    pdf.bullet(
        "Impl\u00e9mentation du SCD Type 2 : gestion de l'historique des "
        "changements de prix dans la dimension DIM_TRACK. Contrairement au S3 "
        "o\u00f9 nous avions tent\u00e9 d'utiliser le m\u00e9canisme int\u00e9gr\u00e9 "
        "d'ODI, nous impl\u00e9mentons ici le SCD2 manuellement avec les composants "
        "natifs de SSIS (Lookup, Conditional Split, OLE DB Command, Derived Column). "
        "Cette approche manuelle nous donne un contr\u00f4le total sur le "
        "processus d'historisation.")

    pdf.p(
        "Ce rapport pr\u00e9sente en d\u00e9tail les \u00e9tapes de "
        "conception et de r\u00e9alisation : la m\u00e9thodologie adopt\u00e9e, "
        "l'analyse de la base source, la construction des couches de donn\u00e9es, "
        "la cr\u00e9ation des flux SSIS, l'impl\u00e9mentation du SCD Type 2, "
        "la validation des r\u00e9sultats, ainsi que les difficult\u00e9s "
        "rencontr\u00e9es et les solutions apport\u00e9es.")

    # =================================================================
    # II. METHODOLOGIE
    # =================================================================
    pdf.add_page()
    pm['II'] = pdf.page_no()
    pdf.titre_I('II', 'M\u00e9thodologie')
    pdf.p(
        "Le projet suit une m\u00e9thodologie structur\u00e9e en quatre "
        "\u00e9tapes principales, chacune correspondant \u00e0 une phase "
        "distincte du cycle de vie d'un projet d'int\u00e9gration de donn\u00e9es. "
        "Cette m\u00e9thodologie est identique \u00e0 celle du S3, avec des "
        "adaptations li\u00e9es au changement d'outils.")

    pm['II.1'] = pdf.page_no()
    pdf.titre_II('1', 'Migration technologique')
    pdf.p(
        "La premi\u00e8re \u00e9tape consiste \u00e0 migrer l'ensemble du "
        "projet de l'\u00e9cosyst\u00e8me Oracle vers l'\u00e9cosyst\u00e8me "
        "Microsoft. Cela implique plusieurs sous-\u00e9tapes :")
    pdf.bullet(
        "Installation et configuration de SQL Server 2022 sur les postes de travail, "
        "avec cr\u00e9ation des 7 bases de donn\u00e9es n\u00e9cessaires "
        "(Chinook, Magasin, DSA_ONLINE, DSA_STORE, ODS_ONLINE, ODS_STORE, DWH_COMMON).")
    pdf.bullet(
        "Conversion des scripts SQL Oracle (PL/SQL) vers T-SQL (Transact-SQL) : "
        "les types de donn\u00e9es diff\u00e8rent (NUMBER -> INT/DECIMAL, "
        "VARCHAR2 -> VARCHAR, DATE -> DATETIME), les fonctions \u00e9galement "
        "(TO_DATE -> CAST, NVL -> ISNULL, SYSDATE -> GETDATE()), et les "
        "s\u00e9quences Oracle sont remplac\u00e9es par des colonnes IDENTITY.")
    pdf.bullet(
        "Remplacement d'ODI par SSIS pour la cr\u00e9ation des flux ETL. "
        "Les interfaces et proc\u00e9dures ODI sont reconstitu\u00e9es sous "
        "forme de packages SSIS dans Visual Studio 2022, avec l'extension "
        "SQL Server Data Tools (SSDT).")

    pm['II.2'] = pdf.page_no()
    pdf.titre_II('2', 'Construction des couches de donn\u00e9es')
    pdf.p(
        "L'architecture est construite en trois couches, conform\u00e9ment "
        "aux bonnes pratiques de l'entreposage de donn\u00e9es. Par rapport au "
        "S3, la principale \u00e9volution est le d\u00e9doublement des couches "
        "DSA et ODS pour g\u00e9rer les deux sources s\u00e9par\u00e9ment "
        "avant la fusion dans le DWH :")
    pdf.bullet_gras("DSA (Data Staging Area)",
        "deux bases s\u00e9par\u00e9es (DSA_ONLINE et DSA_STORE). Zone de transit "
        "vid\u00e9e (TRUNCATE) \u00e0 chaque chargement. Ajout d'un CHANNEL_ID "
        "(1 = Online, 2 = Store) via un composant Derived Column pour identifier "
        "l'origine des donn\u00e9es d\u00e8s l'entr\u00e9e dans le syst\u00e8me.")
    pdf.bullet_gras("ODS (Operational Data Store)",
        "deux bases avec ajout d'une colonne LOAD_DATE pour la tra\u00e7abilit\u00e9 "
        "temporelle. L'ODS n'est PAS vid\u00e9 \u00e0 chaque chargement : un Lookup "
        "anti-doublon \u00e9vite les insertions en double, et un OLE DB Command "
        "met \u00e0 jour les lignes existantes si elles ont chang\u00e9.")
    pdf.bullet_gras("DWH (Data Warehouse)",
        "base unique (DWH_COMMON) fusionnant les deux sources via Union All. "
        "Mod\u00e8le en \u00e9toile avec 9 dimensions (dont DIM_TRACK en SCD2) "
        "et 2 tables de faits (FACT_INVOICE et FACT_INVOICE_LINE).")

    pm['II.3'] = pdf.page_no()
    pdf.titre_II('3', 'Cr\u00e9ation des flux ETL avec SSIS')
    pdf.p(
        "Les flux ETL sont impl\u00e9ment\u00e9s sous forme de packages SSIS "
        "(.dtsx) dans Visual Studio 2022. Chaque package contient un Control Flow "
        "(flux de contr\u00f4le) d\u00e9finissant l'ordre des t\u00e2ches, et un "
        "ou plusieurs Data Flow Tasks (flux de donn\u00e9es) d\u00e9finissant "
        "les transformations. Plus de 30 packages ont \u00e9t\u00e9 cr\u00e9\u00e9s, "
        "organis\u00e9s en trois niveaux d'orchestration :")
    pdf.bullet("00_RUN_ALL.dtsx : orchestrateur global qui ex\u00e9cute "
               "s\u00e9quentiellement DSA -> ODS -> DWH")
    pdf.bullet("00_RUN_ALL_DSA_LOADS.dtsx : regroupe les 13 packages DSA "
               "(11 tables Online + 2 tables Store)")
    pdf.bullet("00_RUN_ALL_ODS_LOADS.dtsx : regroupe les packages ODS correspondants")
    pdf.bullet("00_RUN_ALL_DWH_LOADS.dtsx : regroupe les 10 packages DWH "
               "(9 dimensions + chargement des faits)")
    pdf.p(
        "Cette structure hi\u00e9rarchique permet de r\u00e9ex\u00e9cuter "
        "l'ensemble de l'ETL en un seul clic, tout en conservant la "
        "possibilit\u00e9 de tester chaque package individuellement.")

    pm['II.4'] = pdf.page_no()
    pdf.titre_II('4', 'Validation et optimisation')
    pdf.p(
        "\u00c0 chaque \u00e9tape de l'int\u00e9gration, nous avons mis en "
        "place des contr\u00f4les rigoureux pour valider la qualit\u00e9 des "
        "donn\u00e9es :")
    pdf.bullet("Comptage des lignes par couche (Source -> DSA -> ODS -> DWH) pour "
               "v\u00e9rifier la coh\u00e9rence et d\u00e9tecter les pertes de donn\u00e9es.")
    pdf.bullet("Calcul du chiffre d'affaires (CA) \u00e0 chaque couche pour "
               "s'assurer de la pr\u00e9servation des valeurs mon\u00e9taires.")
    pdf.bullet("Test du SCD Type 2 : modification volontaire de 48 prix dans la "
               "source Chinook, puis v\u00e9rification de l'apparition de deux "
               "versions dans DIM_TRACK (ancienne ferm\u00e9e, nouvelle active).")
    pdf.bullet("Composant Row Count dans chaque package DSA pour compter les lignes "
               "transf\u00e9r\u00e9es et stocker le r\u00e9sultat dans une variable SSIS.")

    # =================================================================
    # III. DETAIL DU PROJET
    # =================================================================
    pdf.add_page()
    pm['III'] = pdf.page_no()
    pdf.titre_I('III', 'D\u00e9tail du projet')

    # --- III.1 Description ---
    pm['III.1'] = pdf.page_no()
    pdf.titre_II('1', 'Description du projet')

    pm['III.1.A'] = pdf.page_no()
    pdf.titre_III('A', 'Contexte et continuit\u00e9 du semestre 3')
    pdf.p(
        "Ce projet s'inscrit dans la continuit\u00e9 directe de la SAE 3.02 "
        "r\u00e9alis\u00e9e au semestre 3. Au S3, nous avions construit un "
        "Data Warehouse \u00e0 partir de la seule base Chinook en utilisant "
        "Oracle Database comme SGBD et Oracle Data Integrator (ODI) comme outil "
        "ETL. Le mod\u00e8le en \u00e9toile comprenait 8 dimensions et 2 tables "
        "de faits, aliment\u00e9es par des interfaces ODI.")
    pdf.p(
        "Cependant, le semestre 3 avait r\u00e9v\u00e9l\u00e9 certaines "
        "limitations : l'installation d'ODI \u00e9tait complexe et ne "
        "fonctionnait qu'\u00e0 l'IUT, nous emp\u00eachant de travailler \u00e0 "
        "domicile. De plus, le SCD Type 2 configur\u00e9 via l'IKM Oracle "
        "n'avait pas produit les r\u00e9sultats attendus. Ces difficult\u00e9s "
        "ont motiv\u00e9 le changement de technologie au S4.")
    pdf.p(
        "Au semestre 4, nous conservons la m\u00eame architecture logique "
        "(DSA -> ODS -> DWH) tout en apportant trois \u00e9volutions majeures : "
        "le changement de technologie (SQL Server + SSIS), l'ajout d'une seconde "
        "source de donn\u00e9es (Magasin), et l'impl\u00e9mentation effective du "
        "SCD Type 2 avec un contr\u00f4le total sur le processus.")

    pm['III.1.B'] = pdf.page_no()
    pdf.titre_III('B', 'Organisation du travail')
    pdf.p(
        "Le projet a \u00e9t\u00e9 r\u00e9alis\u00e9 en bin\u00f4me (Kris "
        "LOKOUN et Abel THYS) sur une p\u00e9riode de novembre 2025 \u00e0 mars "
        "2026, repr\u00e9sentant environ 80 heures de travail. Nous avons travaill\u00e9 "
        "\u00e0 la fois \u00e0 l'IUT et \u00e0 domicile, gr\u00e2ce \u00e0 la "
        "facilit\u00e9 d'installation de SQL Server et Visual Studio sur nos "
        "machines personnelles (contrairement \u00e0 ODI au S3).")
    pdf.p("La r\u00e9partition des t\u00e2ches a \u00e9t\u00e9 la suivante :")
    pdf.bullet_gras('Kris LOKOUN',
        "conception et cr\u00e9ation des packages SSIS (30+ packages), "
        "impl\u00e9mentation du SCD Type 2 (9 composants), "
        "d\u00e9bogage des flux, "
        "v\u00e9rification de la coh\u00e9rence des donn\u00e9es, "
        "r\u00e9daction du rapport et de l'expos\u00e9")
    pdf.bullet_gras('Abel THYS',
        "r\u00e9daction des scripts SQL de cr\u00e9ation des bases (7 scripts), "
        "conversion de la base Magasin d'Oracle vers SQL Server, "
        "tests d'int\u00e9gration et d\u00e9bogage, "
        "v\u00e9rification des requ\u00eates de validation")
    pdf.p(
        "Cette r\u00e9partition a permis d'avancer en parall\u00e8le sur les "
        "aspects techniques (scripts SQL) et visuels (packages SSIS), tout en "
        "maintenant une communication r\u00e9guli\u00e8re pour assurer la "
        "coh\u00e9rence globale du projet.")

    pm['III.1.C'] = pdf.page_no()
    pdf.titre_III('C', 'Outils et technologies utilis\u00e9s')
    pdf.p(
        "Le projet s'appuie enti\u00e8rement sur l'\u00e9cosyst\u00e8me Microsoft, "
        "contrairement au S3 qui utilisait l'\u00e9cosyst\u00e8me Oracle. Ce choix "
        "a \u00e9t\u00e9 impos\u00e9 par les consignes de la SAE, mais il nous "
        "permet de d\u00e9couvrir un autre ensemble d'outils majeur du march\u00e9 "
        "de la BI. Voici les outils utilis\u00e9s et leur r\u00f4le pr\u00e9cis :")
    pdf.section_outils()

    pdf.p(
        "SQL Server 2022 est le moteur de base de donn\u00e9es relationnelle "
        "qui h\u00e9berge nos 7 bases. Il g\u00e8re les connexions, les transactions "
        "et l'ex\u00e9cution des requ\u00eates T-SQL. L'avantage par rapport "
        "\u00e0 Oracle est la simplicit\u00e9 d'installation et la gratuit\u00e9 "
        "de la version Developer.")
    pdf.p(
        "SSIS (SQL Server Integration Services) est l'outil ETL qui remplace "
        "ODI. Il permet de cr\u00e9er des packages visuels dans Visual Studio, "
        "avec deux niveaux de conception : le Control Flow (flux de contr\u00f4le, "
        "qui d\u00e9finit l'ordre des t\u00e2ches) et le Data Flow (flux de "
        "donn\u00e9es, qui d\u00e9finit les transformations ligne par ligne). "
        "Chaque composant est configurable via un \u00e9diteur graphique.")
    pdf.p(
        "SSMS (SQL Server Management Studio) est l'outil d'administration qui "
        "permet d'\u00e9crire et tester les requ\u00eates SQL, de visualiser "
        "les donn\u00e9es et de v\u00e9rifier les r\u00e9sultats des chargements. "
        "C'est l'\u00e9quivalent d'Oracle SQL Developer utilis\u00e9 au S3.")

    pdf.tableau(
        ['Outil', 'Equivalent S3', 'R\u00f4le dans le projet'],
        [
            ['SQL Server 2022', 'Oracle Database', '7 bases de donn\u00e9es'],
            ['SSIS', 'ODI', '30+ packages ETL'],
            ['Visual Studio 2022', 'ODI Studio', 'Conception SSIS'],
            ['SSMS', 'SQL Developer', 'Administration + tests'],
            ['T-SQL', 'PL/SQL', 'MERGE, CTE, triggers'],
            ['SQL Server Agent', '-', 'Planification automatique'],
        ], [40, 40, 90])

    # --- III.2 Analyse initiale et modelisation ---
    pdf.add_page()
    pm['III.2'] = pdf.page_no()
    pdf.titre_II('2', 'Analyse initiale et mod\u00e9lisation')

    pdf.p(
        "Avant de construire les couches de donn\u00e9es, il est essentiel "
        "d'analyser les bases sources pour en comprendre la structure, les "
        "relations et les volumes. Cette analyse permet de d\u00e9terminer "
        "quelles tables et colonnes seront utiles dans le Data Warehouse, "
        "et comment les transformer en mod\u00e8le d\u00e9cisionnel.")

    pdf.titre_libre('Terminologie de la mod\u00e9lisation')
    pdf.p(
        "La mod\u00e9lisation des donn\u00e9es passe par trois niveaux "
        "d'abstraction, du plus conceptuel au plus technique :")
    pdf.bullet_gras('MCD (Mod\u00e8le Conceptuel)',
        "repr\u00e9sentation abstraite des entit\u00e9s et de leurs relations, "
        "ind\u00e9pendante de tout SGBD. Par exemple : un Artiste compose "
        "des Albums, un Album contient des Pistes.")
    pdf.bullet_gras('MLD (Mod\u00e8le Logique)',
        "traduction du MCD en tables avec des colonnes nomm\u00e9es, des "
        "cl\u00e9s primaires (PK) et des cl\u00e9s \u00e9trang\u00e8res (FK). "
        "Les relations N:M sont mat\u00e9rialis\u00e9es par des tables "
        "d'association (ex : PlaylistTrack).")
    pdf.bullet_gras('MPD (Mod\u00e8le Physique)',
        "le MLD avec les types de donn\u00e9es sp\u00e9cifiques au SGBD "
        "(INT, NVARCHAR, DECIMAL, DATETIME pour SQL Server). C'est le "
        "sch\u00e9ma directement impl\u00e9mentable.")

    pdf.titre_libre('Analyse de la base Chinook')
    pdf.p(
        "La base Chinook est un mod\u00e8le transactionnel (OLTP) classique "
        "comportant 11 tables organis\u00e9es en deux zones fonctionnelles :")
    pdf.bullet_gras('Zone Musique (7 tables)',
        "Artist (275 lignes), Album (347), Track (3503), Genre (25), "
        "MediaType (5), Playlist (18), PlaylistTrack (8715). "
        "La table Track est la table centrale : chaque piste est "
        "reli\u00e9e \u00e0 un Album (via AlbumId), un Genre (GenreId) "
        "et un MediaType (MediaTypeId). Le prix unitaire (UnitPrice) "
        "est stock\u00e9 dans Track, ce qui en fait la cible id\u00e9ale "
        "pour le SCD Type 2.")
    pdf.bullet_gras('Zone Ventes (4 tables)',
        "Customer (59), Employee (8), Invoice (412), InvoiceLine (2240). "
        "La table Employee a une auto-r\u00e9f\u00e9rence (ReportsTo) "
        "pour repr\u00e9senter la hi\u00e9rarchie. La table InvoiceLine "
        "fait le lien entre les factures et les pistes via TrackId et InvoiceId.")

    pdf.p(
        "Le Mod\u00e8le Physique de Donn\u00e9es (MPD) ci-dessous "
        "repr\u00e9sente les 11 tables avec leurs cl\u00e9s primaires (PK) "
        "et \u00e9trang\u00e8res (FK). Les traits repr\u00e9sentent les "
        "relations entre tables. Ce sch\u00e9ma est le point de d\u00e9part "
        "pour concevoir notre Data Warehouse.")

    pdf.draw_chinook_mpd()

    pdf.titre_libre('Dictionnaire de donn\u00e9es (tables principales)')
    pdf.tableau(
        ['Table', 'Colonnes principales', 'Lignes', 'R\u00f4le'],
        [
            ['Artist', 'ArtistId (PK), Name', '275', 'Artistes musicaux'],
            ['Album', 'AlbumId (PK), Title, ArtistId (FK)', '347', 'Albums'],
            ['Track', 'TrackId (PK), Name, UnitPrice, ...', '3503', 'Pistes (SCD2)'],
            ['Genre', 'GenreId (PK), Name', '25', 'Genres musicaux'],
            ['MediaType', 'MediaTypeId (PK), Name', '5', 'Types de support'],
            ['Customer', 'CustomerId (PK), FirstName, ...', '59', 'Clients'],
            ['Employee', 'EmployeeId (PK), ReportsTo (FK)', '8', 'Employ\u00e9s'],
            ['Invoice', 'InvoiceId (PK), CustomerId (FK), ...', '412', 'Factures'],
            ['InvoiceLine', 'InvoiceLineId (PK), InvoiceId, ...', '2240', 'D\u00e9tails'],
        ], [27, 68, 18, 57])

    pdf.titre_libre('Analyse de la base Magasin')
    pdf.p(
        "La base Magasin est beaucoup plus simple : elle ne contient que "
        "2 tables (Invoice et InvoiceLine) repr\u00e9sentant les ventes "
        "en magasin physique, pour environ 2 000 lignes. Les cl\u00e9s "
        "\u00e9trang\u00e8res vers Track (TrackId) permettent de croiser "
        "les donn\u00e9es avec Chinook dans le DWH. Cette base \u00e9tait "
        "initialement fournie en syntaxe Oracle (PL/SQL) avec des types "
        "comme NUMBER et VARCHAR2, n\u00e9cessitant une conversion manuelle "
        "vers T-SQL.")

    pdf.titre_libre('Du mod\u00e8le OLTP au mod\u00e8le OLAP')
    pdf.p(
        "Le passage du mod\u00e8le transactionnel (OLTP) au mod\u00e8le "
        "d\u00e9cisionnel (OLAP) n\u00e9cessite une transformation fondamentale : "
        "les tables normalis\u00e9es de Chinook sont d\u00e9normalis\u00e9es en "
        "dimensions et en faits. Les cl\u00e9s naturelles (NK : ArtistId, TrackId, ...) "
        "sont remplac\u00e9es par des cl\u00e9s techniques (TK : TK_ARTISTE, TK_PISTE, ...) "
        "g\u00e9n\u00e9r\u00e9es automatiquement via des colonnes IDENTITY. Cette "
        "transformation est la cl\u00e9 de vo\u00fbte du Data Warehouse.")

    # --- III.3 Architecture ---
    pdf.add_page()
    pm['III.3'] = pdf.page_no()
    pdf.titre_II('3', 'Architecture en 3 couches (DSA, ODS, DWH)')

    pdf.p(
        "L'architecture ETL repose sur trois couches de donn\u00e9es, chacune "
        "ayant un r\u00f4le pr\u00e9cis dans le processus d'int\u00e9gration. "
        "Cette architecture en couches est un standard de l'industrie car elle "
        "permet de s\u00e9parer les responsabilit\u00e9s : la DSA g\u00e8re "
        "l'extraction brute, l'ODS g\u00e8re la tra\u00e7abilit\u00e9, et le "
        "DWH g\u00e8re l'analyse. Par rapport au S3, la principale \u00e9volution "
        "est le d\u00e9doublement des couches DSA et ODS pour g\u00e9rer les "
        "deux sources s\u00e9par\u00e9ment :")
    pdf.code(
        'SOURCES                    DSA                          ODS                         DWH\n'
        '---------                  ----------                   ----------                  --------\n'
        'Chinook  -------->  DSA_ONLINE_LOKOUN_THYS  --->  ODS_ONLINE_LOKOUN_THYS  --->\n'
        '                                                                                DWH_COMMON\n'
        'Magasin  -------->  DSA_STORE_LOKOUN_THYS   --->  ODS_STORE_LOKOUN_THYS   --->')

    pm['III.3.A'] = pdf.page_no()
    pdf.titre_III('A', 'Data Staging Area (DSA)')
    pdf.p(
        "La DSA est la zone de transit entre les sources et le reste du syst\u00e8me. "
        "Son r\u00f4le est de copier les donn\u00e9es brutes des sources sans aucune "
        "transformation m\u00e9tier. Deux bases s\u00e9par\u00e9es ont \u00e9t\u00e9 "
        "cr\u00e9\u00e9es : DSA_ONLINE_LOKOUN_THYS (11 tables, miroir de Chinook) et "
        "DSA_STORE_LOKOUN_THYS (2 tables, miroir de Magasin).")
    pdf.p("Caract\u00e9ristiques techniques de la DSA :")
    pdf.bullet(
        "TRUNCATE \u00e0 chaque chargement : la DSA est vid\u00e9e int\u00e9gralement "
        "avant chaque transfert, via un Execute SQL Task au d\u00e9but de chaque package. "
        "Cela garantit que seules les donn\u00e9es les plus r\u00e9centes de la source "
        "sont pr\u00e9sentes. C'est une approche Full Load (rechargement complet).")
    pdf.bullet(
        "Ajout de colonnes techniques via Derived Column : une date de chargement "
        "(ex : TrackDate = GETDATE()) et un identifiant de canal (CHANNEL_ID = 1 pour "
        "Online, 2 pour Store). Ces colonnes n'existent pas dans les sources et sont "
        "calcul\u00e9es \u00e0 la vol\u00e9e lors du transfert.")
    pdf.bullet(
        "Aucune transformation m\u00e9tier : les donn\u00e9es sont copi\u00e9es "
        "telles quelles. Les noms de colonnes et les types restent identiques "
        "\u00e0 la source (sauf les ajouts techniques).")

    pm['III.3.B'] = pdf.page_no()
    pdf.titre_III('B', 'Operational Data Store (ODS)')
    pdf.p(
        "L'ODS est la couche interm\u00e9diaire entre la DSA et le DWH. Son r\u00f4le "
        "principal est d'assurer la tra\u00e7abilit\u00e9 temporelle des donn\u00e9es : "
        "contrairement \u00e0 la DSA, l'ODS n'est PAS vid\u00e9 \u00e0 chaque "
        "chargement. Il conserve l'historique des chargements gr\u00e2ce \u00e0 une "
        "colonne LOAD_DATE ajout\u00e9e \u00e0 chaque table.")
    pdf.p("Le m\u00e9canisme anti-doublon dans l'ODS fonctionne ainsi :")
    pdf.bullet(
        "Un composant Lookup compare chaque ligne entrante de la DSA avec "
        "les lignes existantes dans l'ODS, en se basant sur la cl\u00e9 primaire "
        "(ex : TrackId pour Track).")
    pdf.bullet(
        "Si la ligne n'existe pas dans l'ODS (sortie No Match du Lookup), "
        "elle est ins\u00e9r\u00e9e via un OLE DB Destination (INSERT).")
    pdf.bullet(
        "Si la ligne existe d\u00e9j\u00e0 (sortie Match du Lookup), un "
        "OLE DB Command ex\u00e9cute un UPDATE pour mettre \u00e0 jour les "
        "colonnes qui ont pu changer (notamment le prix UnitPrice). "
        "Cette \u00e9tape est cruciale pour que les changements de prix "
        "se propagent jusqu'au DWH et d\u00e9clenchent le SCD Type 2.")
    pdf.p(
        "Ce m\u00e9canisme est essentiel car il garantit que les modifications "
        "dans la source (comme un changement de prix) sont propag\u00e9es "
        "\u00e0 travers toutes les couches sans perdre la tra\u00e7abilit\u00e9.")

    pm['III.3.C'] = pdf.page_no()
    pdf.titre_III('C', 'Data Warehouse (DWH) et mod\u00e8le en \u00e9toile')
    pdf.p(
        "Le DWH est la couche finale, con\u00e7ue pour l'analyse d\u00e9cisionnelle. "
        "Il utilise un mod\u00e8le en \u00e9toile (star schema) o\u00f9 les tables de "
        "faits sont au centre, reli\u00e9es aux tables de dimensions par des "
        "cl\u00e9s techniques (TK). Ce mod\u00e8le est optimis\u00e9 pour les "
        "requ\u00eates analytiques (GROUP BY, SUM, COUNT) car il \u00e9vite les "
        "jointures complexes du mod\u00e8le transactionnel.")
    pdf.p(
        "Le DWH comprend 9 tables de dimensions et 2 tables de faits. Les dimensions "
        "d\u00e9crivent les axes d'analyse (Qui ? Quoi ? Quand ? O\u00f9 ?) tandis "
        "que les faits contiennent les mesures (quantit\u00e9, prix, montant total).")
    pdf.tableau(
        ['Table', 'Type', 'Description', 'Lignes'],
        [
            ['DIM_DATE', 'Dimension', 'Calendrier (CTE r\u00e9cursive)', '~1884'],
            ['DIM_TRACK', 'Dim. SCD2', 'Pistes + historique prix', '3503+'],
            ['DIM_CUSTOMER', 'Dimension', 'Clients (Online)', '~59'],
            ['DIM_CHANNEL', 'Dimension', 'Canal : Online / Store', '2'],
            ['DIM_GENRE', 'Dimension', 'Genres musicaux', '~25'],
            ['DIM_ARTIST', 'Dimension', 'Artistes', '~275'],
            ['DIM_ALBUM', 'Dimension', 'Albums', '~347'],
            ['DIM_EMPLOYEE', 'Dimension', 'Employ\u00e9s support', '~8'],
            ['DIM_MEDIATYPE', 'Dimension', 'Types de m\u00e9dia', '~5'],
            ['FACT_INVOICE', 'Fait', 'Factures (Online+Store)', '~1412'],
            ['FACT_INVOICE_LINE', 'Fait', 'Lignes de facture', '~4757'],
        ], [36, 22, 80, 32])

    pdf.p(
        "La particularit\u00e9 de DIM_DATE est qu'elle est g\u00e9n\u00e9r\u00e9e "
        "enti\u00e8rement par un script SQL utilisant une CTE r\u00e9cursive "
        "(Common Table Expression) et un MERGE. Ce script g\u00e9n\u00e8re "
        "automatiquement toutes les dates entre le 01/01/2009 et le 31/12/2013, "
        "avec pour chaque date : le num\u00e9ro du jour, le mois, le nom du mois, "
        "le trimestre et l'ann\u00e9e.")

    pdf.draw_star_schema()

    pdf.p(
        "Dans ce sch\u00e9ma en \u00e9toile, les tables de faits (en bleu) "
        "occupent le centre. FACT_INVOICE_LINE contient une ligne par piste "
        "vendue, avec les cl\u00e9s techniques vers les dimensions DATE, TRACK "
        "et FACTURE. FACT_INVOICE contient une ligne par facture, avec les "
        "cl\u00e9s vers CLIENT, DATE et CHANNEL. La dimension DIM_TRACK est "
        "la seule \u00e0 g\u00e9rer le SCD Type 2 : elle peut contenir "
        "plusieurs versions d'une m\u00eame piste si le prix a chang\u00e9.")

    # --- III.4 Flux SSIS ---
    pdf.add_page()
    pm['III.4'] = pdf.page_no()
    pdf.titre_II('4', 'Cr\u00e9ation des flux de donn\u00e9es avec SSIS')

    pdf.p(
        "Les flux de donn\u00e9es constituent le coeur technique du projet. "
        "Ils sont impl\u00e9ment\u00e9s sous forme de packages SSIS dans "
        "Visual Studio 2022. Chaque package (.dtsx) est un fichier XML qui "
        "d\u00e9crit visuellement les \u00e9tapes de transfert et de "
        "transformation. SSIS distingue deux niveaux de conception :")
    pdf.bullet_gras("Control Flow",
        "d\u00e9finit l'ordre des t\u00e2ches (s\u00e9quentiel ou parall\u00e8le). "
        "Les composants typiques sont : Execute SQL Task (ex\u00e9cuter une requ\u00eate), "
        "Data Flow Task (flux de donn\u00e9es), Execute Package Task (appeler un autre "
        "package). Les fl\u00e8ches vertes indiquent le succ\u00e8s, les rouges l'\u00e9chec.")
    pdf.bullet_gras("Data Flow",
        "d\u00e9finit les transformations ligne par ligne \u00e0 l'int\u00e9rieur "
        "d'un Data Flow Task. Les composants typiques sont : OLE DB Source (lecture), "
        "Derived Column (calcul de colonnes), Lookup (recherche), "
        "Conditional Split (routage conditionnel), OLE DB Destination (\u00e9criture), "
        "OLE DB Command (UPDATE/DELETE), Row Count (comptage), Union All (fusion).")

    pm['III.4.A'] = pdf.page_no()
    pdf.titre_III('A', 'Flux Sources vers DSA')
    pdf.p(
        "Chaque package DSA suit le m\u00eame pattern : dans le Control Flow, "
        "un Execute SQL Task ex\u00e9cute un TRUNCATE TABLE pour vider la table "
        "cible, suivi d'un Data Flow Task pour transf\u00e9rer les donn\u00e9es. "
        "13 packages ont \u00e9t\u00e9 cr\u00e9\u00e9s (11 pour Chinook Online + "
        "2 pour Magasin Store).")
    pdf.p(
        "Dans le Data Flow, les composants sont chain\u00e9s dans cet ordre : "
        "OLE DB Source (lecture de la table source) -> Derived Column (ajout des "
        "colonnes techniques TrackDate et CHANNEL_ID) -> Row Count (comptage des "
        "lignes dans une variable) -> OLE DB Destination (\u00e9criture dans la "
        "table DSA). Le composant Derived Column utilise des expressions SSIS : "
        "GETDATE() pour la date et un entier constant (1 ou 2) pour le CHANNEL_ID.")

    pdf.figure(img('RUN_ALL_DSA.png'),
               "Orchestration des 13 packages DSA via Execute Package Tasks "
               "(fl\u00e8ches vertes = succ\u00e8s)", 125)
    pdf.p(
        "La Figure ci-dessus montre l'orchestrateur 00_RUN_ALL_DSA_LOADS.dtsx "
        "apr\u00e8s une ex\u00e9cution r\u00e9ussie. Chaque bo\u00eete verte "
        "repr\u00e9sente un Execute Package Task qui appelle un package DSA "
        "sp\u00e9cifique. Les packages sont ex\u00e9cut\u00e9s s\u00e9quentiellement "
        "de haut en bas.")

    pdf.figure(img('LOAD_DSA_TRACK.png'),
               "Data Flow du package 01_LOAD_DSA_TRACK : OLE DB Source -> "
               "Derived Column -> Row Count -> OLE DB Destination", 115)
    pdf.p(
        "Ce Data Flow illustre le pattern standard de tous les packages DSA. "
        "Les chiffres sur les fl\u00e8ches indiquent le nombre de lignes "
        "transf\u00e9r\u00e9es (ici 3503 pistes).")

    pdf.figure(img('EDITEUR_DERIVED_COLUMN_DSA.png'),
               "\u00c9diteur du composant Derived Column : ajout des colonnes "
               "TrackDate (GETDATE()) et CHANNEL_ID (1)", 115)
    pdf.p(
        "L'\u00e9diteur Derived Column montre les expressions utilis\u00e9es "
        "pour calculer les nouvelles colonnes. GETDATE() retourne la date et "
        "l'heure actuelles, permettant de savoir quand le chargement a eu lieu. "
        "Le CHANNEL_ID est un entier constant : 1 pour Online (Chinook), "
        "2 pour Store (Magasin).")

    pm['III.4.B'] = pdf.page_no()
    pdf.titre_III('B', 'Flux DSA vers ODS')
    pdf.p(
        "Les flux DSA -> ODS sont plus complexes car ils doivent g\u00e9rer "
        "le m\u00e9canisme anti-doublon d\u00e9crit pr\u00e9c\u00e9demment. "
        "Le pattern est le suivant : OLE DB Source (lecture DSA) -> Derived Column "
        "(ajout LOAD_DATE) -> Lookup (recherche dans l'ODS par cl\u00e9 primaire) "
        "-> deux sorties :")
    pdf.bullet(
        "Sortie No Match (nouvelle ligne) : OLE DB Destination pour INSERT.")
    pdf.bullet(
        "Sortie Match (ligne existante) : OLE DB Command pour UPDATE des "
        "colonnes modifi\u00e9es (UnitPrice, etc.). C'est cette \u00e9tape qui "
        "permet la propagation des changements de prix vers le DWH.")

    pdf.figure(img('RUN_ALL_ODS.png'),
               "Orchestration des packages ODS (ex\u00e9cution r\u00e9ussie)", 125)
    pdf.figure(img('LOAD_ODS_TRACK.png'),
               "Data Flow de LOAD_ODS_TRACK : Lookup avec deux sorties "
               "(No Match = INSERT, Match = UPDATE via OLE DB Command)", 115)
    pdf.p(
        "L'image ci-dessus montre le flux ODS pour la table Track. "
        "La sortie Match du Lookup alimente un OLE DB Command qui ex\u00e9cute "
        "un UPDATE SET UnitPrice = ? WHERE TrackId = ? pour mettre \u00e0 jour "
        "le prix si celui-ci a chang\u00e9 dans la source. Sans cette \u00e9tape, "
        "les modifications de prix ne seraient jamais propag\u00e9es au DWH.")

    pm['III.4.C'] = pdf.page_no()
    pdf.titre_III('C', 'Flux ODS vers DWH')
    pdf.p(
        "Le chargement du DWH est le plus complexe car il implique la "
        "transformation du mod\u00e8le transactionnel (tables normalis\u00e9es) "
        "vers le mod\u00e8le d\u00e9cisionnel (tables en \u00e9toile). "
        "Plusieurs types de chargements coexistent :")
    pdf.bullet_gras("Dimensions simples",
        "Lookup anti-doublon par cl\u00e9 naturelle (NK). Si la dimension n'existe "
        "pas, INSERT avec g\u00e9n\u00e9ration automatique d'une cl\u00e9 technique "
        "(TK) via IDENTITY. Exemples : DIM_GENRE, DIM_ARTIST, DIM_ALBUM, DIM_CUSTOMER.")
    pdf.bullet_gras("DIM_DATE",
        "g\u00e9n\u00e9r\u00e9e par un Execute SQL Task contenant un script "
        "T-SQL avec une CTE r\u00e9cursive. Le MERGE ins\u00e8re les dates "
        "manquantes sans cr\u00e9er de doublons.")
    pdf.bullet_gras("DIM_TRACK (SCD Type 2)",
        "flux sp\u00e9cifique \u00e0 9 composants (d\u00e9taill\u00e9 dans la "
        "section suivante).")
    pdf.bullet_gras("Tables de faits",
        "TRUNCATE puis rechargement complet. Les donn\u00e9es des deux sources "
        "(Online + Store) sont fusionn\u00e9es via un composant Union All. "
        "Ensuite, des Lookups r\u00e9cup\u00e8rent les cl\u00e9s techniques (TK) "
        "des dimensions (DIM_DATE, DIM_TRACK, DIM_CUSTOMER, DIM_CHANNEL) "
        "avant l'insertion dans la table de faits.")

    pdf.figure(img('LOAD_ALL_DWH.png'),
               "Orchestration des 10 packages DWH : dimensions puis faits", 125)

    pdf.figure(img('EDITEUR_EXECUTE_SQL_TASK_DIM_DATE.png'),
               "Script SQL de DIM_DATE : CTE r\u00e9cursive g\u00e9n\u00e9rant "
               "les dates de 2009 \u00e0 2013 + MERGE anti-doublon", 115)
    pdf.p(
        "La CTE r\u00e9cursive commence au 01/01/2009 et ajoute un jour "
        "\u00e0 chaque it\u00e9ration jusqu'au 31/12/2013. Le MERGE "
        "compare avec les dates d\u00e9j\u00e0 pr\u00e9sentes (WHEN NOT MATCHED "
        "THEN INSERT) pour \u00e9viter les doublons lors des ex\u00e9cutions "
        "r\u00e9p\u00e9t\u00e9es. Chaque date est d\u00e9compos\u00e9e en "
        "num\u00e9ro de jour, mois, nom du mois, trimestre et ann\u00e9e.")

    pdf.figure(img('LOAD_DIM_DATE_EXCTION_CORRECTE.png'),
               "Ex\u00e9cution r\u00e9ussie du package DIM_DATE (1884 dates g\u00e9n\u00e9r\u00e9es)", 115)

    pdf.figure(img('LOAD_INVOICELINE.png'),
               "FACT_INVOICE_LINE : Union All fusionnant Online et Store, "
               "puis Lookups TK vers les dimensions", 125)
    pdf.p(
        "Dans ce Data Flow, le composant Union All fusionne les lignes "
        "provenant de ODS_ONLINE et ODS_STORE en un seul flux. Ensuite, "
        "trois Lookups r\u00e9cup\u00e8rent les cl\u00e9s techniques : "
        "TK_FACTURE (via InvoiceId), TK_PISTE (via TrackId, ACTIF=1) "
        "et TK_DATE (via InvoiceDate). Le r\u00e9sultat est ins\u00e9r\u00e9 "
        "dans FACT_INVOICE_LINE.")

    # --- III.5 SCD2 ---
    pdf.add_page()
    pm['III.5'] = pdf.page_no()
    pdf.titre_II('5', 'Gestion du SCD Type 2 sur DIM_TRACK')

    pdf.p(
        "Le SCD Type 2 (Slowly Changing Dimension Type 2) est la fonctionnalit\u00e9 "
        "la plus complexe du projet. Son objectif est de conserver l'historique "
        "complet des changements de valeurs dans une dimension. Dans notre cas, "
        "nous suivons les changements de prix (UnitPrice) des pistes musicales "
        "dans DIM_TRACK.")

    pdf.titre_libre('Pourquoi le SCD Type 2 ?')
    pdf.p(
        "Sans SCD2 (c'est-\u00e0-dire avec un simple UPDATE, appel\u00e9 SCD Type 1), "
        "si le prix d'une piste passe de 0.99 \u00e0 0.49, l'ancien prix est "
        "\u00e9cras\u00e9 et perdu d\u00e9finitivement. Impossible ensuite de "
        "savoir quel prix \u00e9tait en vigueur lors des ventes pass\u00e9es. "
        "Le SCD Type 2 r\u00e9sout ce probl\u00e8me en conservant les deux versions.")

    pdf.tableau(
        ['Crit\u00e8re', 'SCD Type 1 (UPDATE)', 'SCD Type 2 (notre choix)'],
        [
            ['Principe', '\u00c9crase l\'ancienne valeur', 'Conserve toutes les versions'],
            ['Historique', 'Perdu d\u00e9finitivement', 'Pr\u00e9serv\u00e9 int\u00e9gralement'],
            ['Colonnes suppl.', 'Aucune', 'DATE_DEBUT, DATE_FIN, ACTIF'],
            ['Nb de lignes', 'Constant', 'Augmente (+1 par changement)'],
            ['Analyse du CA', 'Anciens prix perdus', 'Comparaison ancien/nouveau CA'],
            ['Complexit\u00e9 SSIS', '1 simple UPDATE', 'Lookup + Split + Command (9 composants)'],
            ['Cas d\'usage', 'Corrections d\'erreurs', 'Changements m\u00e9tier (prix, statuts)'],
        ], [33, 56, 81])

    pdf.titre_libre('Fonctionnement pas \u00e0 pas')
    pdf.p("Prenons l'exemple concret d'une piste dont le prix passe de 0.99 \u00e0 0.49 :")
    pdf.bullet(
        "\u00c9tape 1 - Lecture ODS : le composant SRC_TRACK_ODS lit la table Track "
        "de l'ODS, qui contient le nouveau prix (0.49) suite \u00e0 l'UPDATE "
        "effectu\u00e9 dans le flux DSA -> ODS.")
    pdf.bullet(
        "\u00c9tape 2 - Pr\u00e9paration : un Derived Column (CD_DIM_TRACK) "
        "pr\u00e9pare les colonnes n\u00e9cessaires pour le SCD2.")
    pdf.bullet(
        "\u00c9tape 3 - Recherche version active : le Lookup (LKP_DIM_TRACK_ACTIF) "
        "cherche dans DIM_TRACK la ligne o\u00f9 NK_ID_PISTE = TrackId ET ACTIF = 1. "
        "Deux cas se pr\u00e9sentent :")
    pdf.bullet(
        "\u00c9tape 3a - No Match : la piste n'existe pas encore dans le DWH. "
        "Elle est ins\u00e9r\u00e9e comme nouvelle dimension (DST_NOUVELLE) avec "
        "DATE_DEBUT = aujourd'hui, DATE_FIN = NULL, ACTIF = 1.")
    pdf.bullet(
        "\u00c9tape 3b - Match : la piste existe. Le Conditional Split "
        "(CS_PRIX_CHANGE) compare le prix ODS avec le prix DWH : "
        "UNIT_PRICE != UNIT_PRICE_EXISTANT.")
    pdf.bullet(
        "\u00c9tape 4 - Prix identique : rien \u00e0 faire, la ligne est ignor\u00e9e "
        "(sortie par d\u00e9faut du Conditional Split).")
    pdf.bullet(
        "\u00c9tape 5 - Prix diff\u00e9rent : fermeture de l'ancienne version "
        "via OLE DB Command (CMD_FERMER) : UPDATE SET DATE_FIN = GETDATE(), "
        "ACTIF = 0 WHERE TK_PISTE = TK_existant.")
    pdf.bullet(
        "\u00c9tape 6 - Insertion de la nouvelle version (DST_CHANGEE) avec "
        "le nouveau prix, DATE_DEBUT = GETDATE(), DATE_FIN = NULL, ACTIF = 1.")

    pdf.titre_libre('Architecture du flux SCD2 (9 composants)')
    pdf.code(
        'SRC_TRACK_ODS  -->  CD_DIM_TRACK (Derived Column)\n'
        '                        |\n'
        '                  LKP_DIM_TRACK_ACTIF (Lookup ACTIF=1)\n'
        '                   /             \\\n'
        '              No Match           Match\n'
        '                 |                  |\n'
        '           DST_NOUVELLE     CS_PRIX_CHANGE (Conditional Split)\n'
        '           (INSERT)            /            \\\n'
        '                       Prix change       Inchange\n'
        '                           |                (ignore)\n'
        '                  CMD_FERMER_ANCIENNE (UPDATE ACTIF=0)\n'
        '                           |\n'
        '                  DST_CHANGEE (INSERT nouvelle version)')
    pdf.tableau(
        ['Composant', 'Type SSIS', 'R\u00f4le d\u00e9taill\u00e9'],
        [
            ['SRC_TRACK_ODS', 'OLE DB Source', 'Lecture des pistes depuis ODS_ONLINE'],
            ['CD_DIM_TRACK', 'Derived Column', 'Pr\u00e9paration des colonnes SCD2'],
            ['LKP_DIM_TRACK', 'Lookup', 'Cherche la version active (ACTIF=1)'],
            ['CS_PRIX_CHANGE', 'Cond. Split', 'Compare UNIT_PRICE ODS vs DWH'],
            ['CD_FERMER', 'Derived Column', 'Calcule DATE_FIN=GETDATE(), ACTIF=0'],
            ['CMD_FERMER', 'OLE DB Command', 'UPDATE ancienne version'],
            ['CD_NOUVELLE', 'Derived Column', 'Calcule DATE_DEBUT, ACTIF=1'],
            ['DST_CHANGEE', 'OLE DB Dest.', 'INSERT nouvelle version (prix change)'],
            ['DST_NOUVELLE', 'OLE DB Dest.', 'INSERT piste inconnue'],
        ], [33, 33, 104])

    pdf.figure(img('LOAD_DIM_TRACK_NON_EXECUTER.png'),
               "Flux SCD2 dans Visual Studio avant ex\u00e9cution : "
               "9 composants connect\u00e9s", 115)
    pdf.figure(img('LOAD_DIM_TRACK_EXUTOION COMPLETE ET FONCTIONNELLE.png'),
               "Flux SCD2 apr\u00e8s ex\u00e9cution r\u00e9ussie : fl\u00e8ches "
               "vertes et compteurs de lignes sur chaque fl\u00e8che", 115)
    pdf.p(
        "Apr\u00e8s ex\u00e9cution, les compteurs sur les fl\u00e8ches "
        "montrent le nombre de lignes \u00e0 chaque \u00e9tape. Lors de la "
        "premi\u00e8re ex\u00e9cution, toutes les lignes passent par No Match "
        "(3503 INSERT). Apr\u00e8s modification des prix et re-ex\u00e9cution, "
        "48 lignes passent par Match -> Prix change (48 CLOSE + 48 INSERT), "
        "le reste par Match -> Inchang\u00e9 (ignor\u00e9).")

    # --- III.6 Validation ---
    pdf.add_page()
    pm['III.6'] = pdf.page_no()
    pdf.titre_II('6', 'Validation et v\u00e9rification des donn\u00e9es')
    pdf.p(
        "La validation est une \u00e9tape essentielle de tout projet "
        "d'int\u00e9gration. Elle permet de v\u00e9rifier que les donn\u00e9es "
        "n'ont pas \u00e9t\u00e9 alt\u00e9r\u00e9es, perdues ou dupliqu\u00e9es "
        "au cours du processus ETL. Nous avons mis en place trois types de "
        "contr\u00f4les :")

    pdf.titre_III('A', 'Test du SCD Type 2')
    pdf.p(
        "Pour tester le SCD2, nous avons modifi\u00e9 volontairement le prix de "
        "48 pistes dans la base source Chinook (UnitPrice de 0.99 \u00e0 0.49) "
        "via un UPDATE cibl\u00e9. Puis nous avons re-ex\u00e9cut\u00e9 l'ETL "
        "complet (00_RUN_ALL). Le r\u00e9sultat attendu : dans DIM_TRACK, chaque "
        "piste modifi\u00e9e doit appara\u00eetre en deux versions.")
    pdf.p("La requ\u00eate de v\u00e9rification utilis\u00e9e :")
    pdf.code(
        "SELECT CASE WHEN ACTIF = 0 THEN 'AVANT (ferm\u00e9e)'\n"
        "            ELSE 'APRES (active)' END AS [VERSION],\n"
        "    NK_ID_PISTE, NOM_PISTE, UNIT_PRICE,\n"
        "    DATE_DEBUT, DATE_FIN, ACTIF\n"
        "FROM [DWH_COMMON_LOKOUN_THYS].[dbo].[DIM_TRACK]\n"
        "WHERE NK_ID_PISTE BETWEEN 2358 AND 2370\n"
        "ORDER BY NK_ID_PISTE, ACTIF;")
    pdf.figure(img('RESULTAT_SCD2_SSMS_SIMPLE.png'),
               "R\u00e9sultat SCD2 dans SSMS : chaque piste appara\u00eet "
               "deux fois (AVANT \u00e0 0.99, APRES \u00e0 0.49)", 130)
    pdf.p(
        "L'image confirme le bon fonctionnement : pour chaque piste modifi\u00e9e, "
        "la version AVANT (ACTIF=0) conserve le prix original 0.99 avec une DATE_FIN "
        "correspondant au moment du changement. La version APRES (ACTIF=1) porte le "
        "nouveau prix 0.49 avec une DATE_DEBUT correspondante et DATE_FIN = NULL.")

    pdf.titre_III('B', 'Comptage des lignes par couche')
    pdf.p(
        "Le nombre de lignes doit rester constant \u00e0 travers les couches "
        "(Source -> DSA -> ODS -> DWH) pour garantir qu'aucune donn\u00e9e n'est "
        "perdue. L'exception est DIM_TRACK qui augmente gr\u00e2ce au SCD2 : "
        "3503 lignes de base + 48 versions historis\u00e9es = 3551 lignes au total "
        "(dont 3503 actives et 48 ferm\u00e9es).")
    pdf.figure(img('SUIVI_EVOLUTION PAR_COUCHE.png'),
               "Suivi des lignes par couche : le nombre reste constant "
               "de la source au DWH (coh\u00e9rence v\u00e9rifi\u00e9e)", 130)
    pdf.p(
        "Ce tableau montre que les comptages sont identiques \u00e0 chaque couche "
        "pour toutes les tables (Track, Album, Artist, Customer, Genre, Invoice, "
        "InvoiceLine). Seule DIM_TRACK dans le DWH affiche un nombre "
        "sup\u00e9rieur, ce qui est le comportement attendu du SCD2.")

    pdf.titre_III('C', "\u00c9volution du chiffre d'affaires (CA)")
    pdf.p(
        "Le CA (Quantit\u00e9 x Prix Unitaire) est calcul\u00e9 \u00e0 chaque "
        "couche et pour chaque canal (Online et Store) s\u00e9par\u00e9ment. "
        "L'objectif est de v\u00e9rifier qu'il n'y a aucune perte de donn\u00e9es "
        "mon\u00e9taires au cours du processus ETL.")
    pdf.p(
        "Le CA doit rester identique de la source au DWH. Dans le DWH, "
        "deux valeurs de CA sont calcul\u00e9es : le CA avec les prix actuels "
        "(ACTIF=1) et le CA avec les prix d'origine (ACTIF=0). La diff\u00e9rence "
        "entre les deux s'explique exclusivement par le SCD2 : les 48 pistes "
        "dont le prix est pass\u00e9 de 0.99 \u00e0 0.49 g\u00e9n\u00e8rent un "
        "CA inf\u00e9rieur avec les prix actuels.")
    pdf.figure(img('EVOLUTION CA (STORE ET ONLINE ).png'),
               "\u00c9volution du CA par couche et par canal : "
               "z\u00e9ro perte de la source au DWH", 130)
    pdf.p(
        "L'image confirme : le CA Source = CA DSA = CA ODS = CA DWH (prix historiques). "
        "Le CA DWH avec prix actuels est l\u00e9g\u00e8rement inf\u00e9rieur, "
        "ce qui est coh\u00e9rent avec la baisse de prix de 48 pistes. Cette "
        "diff\u00e9rence constitue la preuve que le SCD2 fonctionne correctement "
        "et permet de comparer l'\u00e9volution du CA dans le temps.")

    # =================================================================
    # IV. AUTOMATISATION
    # =================================================================
    pdf.add_page()
    pm['IV'] = pdf.page_no()
    pdf.titre_I('IV', "Automatisation de l'ETL")
    pdf.p(
        "En production, un ETL ne peut pas \u00eatre ex\u00e9cut\u00e9 "
        "manuellement \u00e0 chaque fois. SQL Server propose deux m\u00e9canismes "
        "d'automatisation : SQL Server Agent pour la planification, et les "
        "triggers T-SQL pour la d\u00e9tection \u00e9v\u00e9nementielle.")

    pdf.titre_II('1', 'SQL Server Agent')
    pdf.p(
        "SQL Server Agent est un service int\u00e9gr\u00e9 \u00e0 SQL Server qui "
        "permet de planifier l'ex\u00e9cution automatique de t\u00e2ches. Un Job "
        "se compose de Steps (les \u00e9tapes \u00e0 ex\u00e9cuter) et de "
        "Schedules (les horaires d'ex\u00e9cution). Dans notre cas, le Job "
        "ex\u00e9cuterait le package 00_RUN_ALL.dtsx chaque nuit :")
    pdf.code(
        'USE msdb;\n'
        "EXEC sp_add_job @job_name = 'ETL_RUN_ALL_NIGHTLY';\n"
        "EXEC sp_add_jobstep @job_name = 'ETL_RUN_ALL_NIGHTLY',\n"
        "    @step_name = 'Executer 00_RUN_ALL',\n"
        "    @subsystem = 'SSIS',\n"
        "    @command = '\\SSISDB\\ETL_Chinook\\00_RUN_ALL.dtsx';\n"
        "EXEC sp_add_schedule @schedule_name = 'Nuit_2h',\n"
        '    @freq_type = 4, @active_start_time = 020000;')
    pdf.p(
        "Le param\u00e8tre freq_type = 4 signifie \"tous les jours\", et "
        "active_start_time = 020000 signifie \"02h00\". Ainsi, l'ETL complet "
        "serait ex\u00e9cut\u00e9 automatiquement chaque nuit \u00e0 2h du matin, "
        "moment o\u00f9 la charge sur le serveur est minimale.")

    pdf.titre_II('2', 'Triggers T-SQL')
    pdf.p(
        "En compl\u00e9ment de la planification r\u00e9guli\u00e8re, un trigger "
        "T-SQL peut d\u00e9tecter automatiquement les modifications de prix dans "
        "la source et lancer l'ETL imm\u00e9diatement. Cela permet une "
        "r\u00e9activit\u00e9 maximale : d\u00e8s qu'un prix change dans "
        "Chinook, le SCD2 est d\u00e9clench\u00e9.")
    pdf.code(
        'CREATE TRIGGER trg_Track_PriceChange\n'
        'ON [Chinook_LOKOUN_THYS].[dbo].[Track]\n'
        'AFTER UPDATE AS\n'
        'BEGIN\n'
        '    IF UPDATE(UnitPrice)\n'
        '        EXEC msdb.dbo.sp_start_job\n'
        "            @job_name = 'ETL_RUN_ALL_NIGHTLY';\n"
        'END;')
    pdf.p(
        "Le trigger AFTER UPDATE se d\u00e9clenche apr\u00e8s chaque UPDATE "
        "sur la table Track. La condition IF UPDATE(UnitPrice) v\u00e9rifie "
        "que c'est bien la colonne UnitPrice qui a \u00e9t\u00e9 modifi\u00e9e. "
        "Si oui, il lance le Job ETL via sp_start_job, ce qui d\u00e9clenche "
        "toute la cha\u00eene DSA -> ODS -> DWH et met \u00e0 jour le SCD2 "
        "dans DIM_TRACK.")

    # =================================================================
    # V. DIFFICULTES
    # =================================================================
    pdf.add_page()
    pm['V'] = pdf.page_no()
    pdf.titre_I('V', 'Difficult\u00e9s rencontr\u00e9es et solutions')
    pdf.p(
        "Tout au long du projet, nous avons rencontr\u00e9 plusieurs "
        "difficult\u00e9s techniques qui ont n\u00e9cessit\u00e9 des recherches "
        "et des adaptations. Ces difficult\u00e9s font partie int\u00e9grante "
        "de l'apprentissage et ont renforc\u00e9 notre compr\u00e9hension "
        "des m\u00e9canismes ETL.")

    pdf.titre_II('1', 'Conversion Oracle vers SQL Server')
    pdf.p(
        "La base Magasin \u00e9tait fournie en syntaxe Oracle (PL/SQL). La "
        "conversion vers T-SQL a n\u00e9cessit\u00e9 : le remplacement des "
        "types de donn\u00e9es (NUMBER -> INT/DECIMAL, VARCHAR2 -> VARCHAR, "
        "DATE -> DATETIME), la remplacement des fonctions (TO_DATE -> CAST, "
        "NVL -> ISNULL, SYSDATE -> GETDATE()), et la conversion des "
        "s\u00e9quences Oracle (CREATE SEQUENCE) en colonnes IDENTITY. "
        "Un script Python a \u00e9t\u00e9 utilis\u00e9 pour automatiser "
        "la conversion des INSERT en masse.")

    pdf.titre_II('2', 'SCD2 ne se d\u00e9clenchait pas')
    pdf.p(
        "Apr\u00e8s modification des prix dans Chinook et re-ex\u00e9cution "
        "de l'ETL, DIM_TRACK ne montrait aucune ligne historis\u00e9e. "
        "Le probl\u00e8me \u00e9tait dans le flux ODS : le Lookup n'ins\u00e9rait "
        "que les nouvelles lignes (No Match) mais ignorait les lignes existantes "
        "(Match). Le prix modifi\u00e9 dans la source ne se propageait donc "
        "jamais jusqu'\u00e0 l'ODS, et donc jamais jusqu'au DWH. "
        "Solution : ajout d'un OLE DB Command sur la sortie Match du Lookup "
        "ODS pour ex\u00e9cuter un UPDATE. Important : nous ne pouvions pas "
        "TRUNCATE l'ODS car cela aurait d\u00e9truit la tra\u00e7abilit\u00e9 "
        "historique (LOAD_DATE).")

    pdf.titre_II('3', 'Doublons dans les tables de faits')
    pdf.p(
        "Apr\u00e8s plusieurs ex\u00e9cutions de l'ETL, FACT_INVOICE_LINE "
        "contenait 5 fois trop de lignes. Cause : les faits \u00e9taient "
        "recharg\u00e9s sans vider la table, cr\u00e9ant des doublons "
        "\u00e0 chaque ex\u00e9cution. Solution : ajout d'un Execute SQL Task "
        "avec TRUNCATE TABLE au d\u00e9but des packages de chargement des faits. "
        "Contrairement aux dimensions (qui n\u00e9cessitent un Lookup anti-doublon), "
        "les faits sont recharg\u00e9s int\u00e9gralement (Full Reload).")

    pdf.titre_II('4', 'Noms de colonnes incoh\u00e9rents entre couches')
    pdf.p(
        "Les colonnes portent des noms diff\u00e9rents selon la couche : "
        "UnitPrice dans Chinook/DSA/ODS vs PRIX_UNITAIRE dans le DWH, "
        "TrackId vs NK_ID_PISTE, etc. Cette incoh\u00e9rence a caus\u00e9 "
        "des erreurs dans les requ\u00eates de v\u00e9rification du CA. "
        "Solution : utilisation syst\u00e9matique des noms DWH pour les "
        "requ\u00eates analytiques, et documentation pr\u00e9cise des "
        "correspondances entre colonnes.")

    pdf.titre_II('5', 'Erreur de connexion SQL Server')
    pdf.p(
        "L'erreur 15404 (\"Impossible d'obtenir des informations sur "
        "l'utilisateur Windows NT\") apparaissait lors de certaines "
        "op\u00e9rations. Cause : le propri\u00e9taire de la base \u00e9tait "
        "un compte Windows non reconnu. Solution : ALTER AUTHORIZATION ON "
        "DATABASE::[nom_base] TO [sa] pour transf\u00e9rer la propri\u00e9t\u00e9 "
        "au compte sa (System Administrator).")

    # =================================================================
    # VI. CONCLUSION
    # =================================================================
    pdf.add_page()
    pm['VI'] = pdf.page_no()
    pdf.titre_I('VI', 'Conclusion')

    pdf.p(
        "Ce projet nous a permis de construire une cha\u00eene ETL compl\u00e8te "
        "avec SQL Server et SSIS, en partant de deux sources h\u00e9t\u00e9rog\u00e8nes "
        "(Chinook et Magasin) pour aboutir \u00e0 un Data Warehouse unifi\u00e9. "
        "L'ensemble des objectifs fix\u00e9s ont \u00e9t\u00e9 atteints :")
    pdf.bullet("7 bases de donn\u00e9es cr\u00e9\u00e9es et aliment\u00e9es "
               "(2 sources + 2 DSA + 2 ODS + 1 DWH)")
    pdf.bullet("Plus de 30 packages SSIS orchestr\u00e9s hi\u00e9rarchiquement "
               "(RUN_ALL -> DSA/ODS/DWH -> packages individuels)")
    pdf.bullet("SCD Type 2 fonctionnel et v\u00e9rifi\u00e9 avec 48 changements "
               "de prix (2 versions par piste modifi\u00e9e)")
    pdf.bullet("Fusion r\u00e9ussie des canaux Online et Store dans le DWH "
               "avec tra\u00e7abilit\u00e9 via CHANNEL_ID")
    pdf.bullet("Z\u00e9ro perte de donn\u00e9es v\u00e9rifi\u00e9e par comptage "
               "de lignes et calcul du CA \u00e0 chaque couche")
    pdf.bullet("Automatisation possible via SQL Server Agent et triggers T-SQL")

    pdf.p(
        "Par rapport au semestre 3, ce projet repr\u00e9sente une \u00e9volution "
        "majeure sur trois plans : la ma\u00eetrise d'un second \u00e9cosyst\u00e8me "
        "ETL (Microsoft vs Oracle), la gestion de deux sources de donn\u00e9es "
        "h\u00e9t\u00e9rog\u00e8nes, et l'impl\u00e9mentation effective du SCD "
        "Type 2 que nous n'avions pas r\u00e9ussi \u00e0 finaliser au S3. "
        "La compr\u00e9hension des m\u00e9canismes ETL et de la mod\u00e9lisation "
        "d\u00e9cisionnelle est d\u00e9sormais solide.")

    pdf.p("Parmi les am\u00e9liorations envisageables :")
    pdf.bullet("Automatisation compl\u00e8te via SQL Server Agent avec alertes "
               "par email en cas d'\u00e9chec")
    pdf.bullet("Ajout de contr\u00f4les de qualit\u00e9 plus fins (Data Profiling, "
               "assertions sur les volumes)")
    pdf.bullet("Int\u00e9gration de nouvelles sources (API, fichiers CSV, bases NoSQL)")
    pdf.bullet("S\u00e9paration de Invoice en dimension d\u00e9di\u00e9e pour "
               "optimiser les performances des requ\u00eates SELECT")
    pdf.p(
        "Ces am\u00e9liorations repr\u00e9senteraient environ 10 \u00e0 15 heures "
        "de travail suppl\u00e9mentaires. Le syst\u00e8me actuel r\u00e9pond "
        "pleinement aux objectifs fix\u00e9s.")

    # =================================================================
    # VII. BILAN PERSONNEL (en tableau comme NGUYEN_LE)
    # =================================================================
    pdf.add_page()
    pm['VII'] = pdf.page_no()
    pdf.titre_I('VII', 'Bilan personnel')

    pdf.tableau_bilan('Kris LOKOUN', [
        "Comp\u00e9tences ETL approfondies : Oracle/ODI au S3, SQL Server/SSIS au S4",
        "Impl\u00e9mentation manuelle du SCD Type 2 : logique d'historisation compl\u00e8te",
        "D\u00e9bogage avanc\u00e9 : tra\u00e7age des donn\u00e9es couche par couche pour localiser les probl\u00e8mes",
        "Fusion de deux sources h\u00e9t\u00e9rog\u00e8nes : d\u00e9fis r\u00e9els de l'int\u00e9gration multi-sources",
        "Ma\u00eetrise des outils professionnels de la BI (VS, SSMS, SQL Server Agent)",
        "Cette exp\u00e9rience me pr\u00e9pare aux projets futurs de gestion de donn\u00e9es \u00e0 grande \u00e9chelle",
    ])
    pdf.tableau_bilan('Abel THYS', [
        "Comp\u00e9tences T-SQL am\u00e9lior\u00e9es : MERGE, CTE r\u00e9cursives, triggers, IDENTITY",
        "Conversion de syntaxe Oracle vers SQL Server : compr\u00e9hension des diff\u00e9rences entre SGBD",
        "Compr\u00e9hension des cl\u00e9s techniques (TK) et naturelles (NK) dans un DWH",
        "Travail en bin\u00f4me : collaboration efficace et r\u00e9partition \u00e9quilibr\u00e9e des t\u00e2ches",
        "Capacit\u00e9 \u00e0 d\u00e9boguer des probl\u00e8mes complexes en \u00e9quipe",
    ])

    pdf.titre_libre('Apprentissages communs')
    pdf.bullet("Ma\u00eetrise de deux \u00e9cosyst\u00e8mes ETL complets (Oracle+ODI et Microsoft+SSIS)")
    pdf.bullet("Architecture DSA -> ODS -> DWH ma\u00eetris\u00e9e de bout en bout")
    pdf.bullet("Gestion de l'historique avec le SCD Type 2 (th\u00e9orie et pratique)")
    pdf.bullet("Importance de la v\u00e9rification syst\u00e9matique \u00e0 chaque \u00e9tape de l'ETL")
    pdf.bullet("Autonomie accrue : installation et configuration des outils sans d\u00e9pendance \u00e0 l'IUT")

    # =================================================================
    # VIII. REMERCIEMENTS
    # =================================================================
    pdf.add_page()
    pm['VIII'] = pdf.page_no()
    pdf.titre_I('VIII', 'Remerciements')
    pdf.p(
        "Nous tenons \u00e0 remercier sinc\u00e8rement Monsieur Yannick Le V\u00e9ler "
        "pour son accompagnement tout au long de ce projet. Ses conseils techniques, "
        "sa p\u00e9dagogie et sa disponibilit\u00e9 nous ont permis de progresser "
        "efficacement et de mener ce projet \u00e0 bien. Gr\u00e2ce \u00e0 ses "
        "pr\u00e9cieux retours, nous avons pu surmonter les difficult\u00e9s "
        "rencontr\u00e9es et approfondir notre compr\u00e9hension de l'int\u00e9gration "
        "de donn\u00e9es.")
    pdf.p(
        "Nous remercions \u00e9galement l'Universit\u00e9 de Lille et l'IUT de "
        "Roubaix pour les ressources mat\u00e9rielles et logicielles mises \u00e0 "
        "notre disposition, qui ont rendu possible la r\u00e9alisation de ce projet "
        "dans de bonnes conditions.")

    # GENERER
    if save:
        out = os.path.join(BASE, 'RAPPORT_SAE4_LOKOUN_THYS.pdf')
        try:
            pdf.output(out)
        except PermissionError:
            out = os.path.join(BASE, 'RAPPORT_SAE4_LOKOUN_THYS_v2.pdf')
            pdf.output(out)
        print('RAPPORT : ' + out)
        print('  Pages : ' + str(pdf.page_no()) +
              ', Figures : ' + str(pdf.fig_num))
        return pdf.page_no(), pdf.fig_num
    else:
        return pm


def generer_rapport():
    page_map = _build_rapport(save=False)
    return _build_rapport(save=True, toc_pages=page_map)


# =============================================================================
# 2. EXPOSE SSIS (inchange)
# =============================================================================
TDM_EXPOSE = [
    (1, 'I.', 'Composants choisis', 'I'),
    (2, 'A.', 'Execute SQL Task', 'I.A'),
    (2, 'B.', 'Row Count', 'I.B'),
    (2, 'C.', 'Derived Column', 'I.C'),
    (2, 'D.', 'Conditional Split', 'I.D'),
    (2, 'E.', 'Union All', 'I.E'),
    (2, 'F.', 'SCD Type 2 (principal)', 'I.F'),
    (2, 'G.', 'Autres composants', 'I.G'),
    (1, 'II.', 'Comparaison SCD1 vs SCD2', 'II'),
    (1, 'III.', 'D\u00e9monstration', 'III'),
    (2, 'A.', 'Orchestration globale', 'III.A'),
    (2, 'B.', 'Flux SCD2', 'III.B'),
    (2, 'C.', 'V\u00e9rification SCD2', 'III.C'),
    (2, 'D.', 'Coh\u00e9rence des donn\u00e9es', 'III.D'),
    (1, 'IV.', 'Automatisation', 'IV'),
    (2, 'A.', 'SQL Server Agent', 'IV.A'),
    (2, 'B.', 'Triggers T-SQL', 'IV.B'),
    (1, 'V.', 'Glossaire', 'V'),
]


def _build_expose(save=True, toc_pages=None):
    pdf = RapportPDF(titre_court='Expos\u00e9 SSIS - Composants ETL')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=M_BOTTOM)
    pdf.set_left_margin(M_LEFT)
    pdf.set_right_margin(M_RIGHT)
    pm = {}

    pdf.page_garde(
        'Expos\u00e9 SSIS',
        'Composants SSIS dans un projet ETL\n'
        'Data Warehouse Chinook + Magasin',
        'R4.VCOD08 / R4.EMS09', 'Mars 2026')

    pdf.tdm(TDM_EXPOSE, toc_pages)

    pdf.add_page()
    pm['I'] = pdf.page_no()
    pdf.titre_I('I', 'Composants choisis')
    pdf.p(
        "Chaque composant SSIS utilis\u00e9 dans le projet, son "
        "r\u00f4le, ses param\u00e8tres et sa justification.")

    pm['I.A'] = pdf.page_no()
    pdf.titre_III('A', 'Niveau 1 : Execute SQL Task')
    pdf.p(
        "Ex\u00e9cute une requ\u00eate SQL dans le Control Flow. "
        "Utilis\u00e9 pour DIM_DATE (MERGE + CTE r\u00e9cursive) et "
        "pour les TRUNCATE avant chargement DSA.")
    pdf.tableau(
        ['Param\u00e8tre', 'Valeur'],
        [['Connection', 'DWH_COMMON_LOKOUN_THYS'],
         ['SQLStatement', 'MERGE + CTE r\u00e9cursive'],
         ['ResultSet', 'None']], [50, 120])
    pdf.figure(img('EDITEUR_EXECUTE_SQL_TASK_DIM_DATE.png'),
               "Execute SQL Task : MERGE g\u00e9n\u00e9rant les dates", 115)

    pm['I.B'] = pdf.page_no()
    pdf.titre_III('B', 'Niveau 1 : Row Count')
    pdf.p(
        "Compte les lignes et stocke dans une variable SSIS. "
        "Contr\u00f4le qualit\u00e9 dans les 13 packages DSA.")

    pm['I.C'] = pdf.page_no()
    pdf.titre_III('C', 'Niveau 2 : Derived Column')
    pdf.p("Composant le plus utilis\u00e9 (30+ occurrences) :")
    pdf.bullet_gras('DSA', 'GETDATE() + CHANNEL_ID')
    pdf.bullet_gras('ODS', 'LOAD_DATE')
    pdf.bullet_gras('DWH SCD2', '3 Derived Columns')

    pm['I.D'] = pdf.page_no()
    pdf.titre_III('D', 'Niveau 2 : Conditional Split')
    pdf.p(
        "Route les lignes selon des conditions. Dans le SCD2 : "
        "UNIT_PRICE != UNIT_PRICE_EXISTANT.")

    pm['I.E'] = pdf.page_no()
    pdf.titre_III('E', 'Niveau 2 : Union All')
    pdf.p(
        "Fusionne Online et Store avant les Lookups de cl\u00e9s TK "
        "dans FACT_INVOICE et FACT_INVOICE_LINE.")

    pm['I.F'] = pdf.page_no()
    pdf.titre_III('F', 'Niveau 3 : SCD Type 2 (composant principal)')
    pdf.p("9 composants SSIS pour le SCD2 manuel :")
    pdf.tableau(
        ['Composant', 'Type SSIS', 'R\u00f4le'],
        [
            ['SRC_TRACK_ODS', 'OLE DB Source', 'Lecture ODS'],
            ['CD_DIM_TRACK', 'Derived Column', 'Pr\u00e9paration'],
            ['LKP_DIM_TRACK', 'Lookup', 'Version active'],
            ['CS_PRIX_CHANGE', 'Cond. Split', 'D\u00e9tection prix'],
            ['CD_FERMER', 'Derived Column', 'ACTIF=0'],
            ['CMD_FERMER', 'OLE DB Command', 'UPDATE'],
            ['CD_NOUVELLE', 'Derived Column', 'ACTIF=1'],
            ['DST_CHANGEE', 'OLE DB Dest.', 'INSERT nouvelle'],
            ['DST_NOUVELLE', 'OLE DB Dest.', 'INSERT inconnue'],
        ], [38, 36, 96])

    pm['I.G'] = pdf.page_no()
    pdf.titre_III('G', 'Autres composants')
    pdf.bullet_gras('Lookup', '20+ occurrences')
    pdf.bullet_gras('OLE DB Command', 'UPDATE SCD2 et ODS')
    pdf.bullet_gras('Execute Package Task', 'Orchestration RUN_ALL')

    pdf.add_page()
    pm['II'] = pdf.page_no()
    pdf.titre_I('II', 'Comparaison SCD Type 1 vs Type 2')
    pdf.tableau(
        ['Crit\u00e8re', 'SCD Type 1', 'SCD Type 2 (notre choix)'],
        [
            ['Principe', '\u00c9crase', 'Conserve versions'],
            ['Historique', 'Perdu', 'Pr\u00e9serv\u00e9'],
            ['Colonnes', 'Aucune', 'DATE_DEBUT, DATE_FIN, ACTIF'],
            ['Lignes', 'Constant', '+1 par changement'],
            ['CA', 'Anciens prix perdus', 'Comparaison possible'],
            ['Complexit\u00e9', '1 UPDATE', 'Lookup+Split+Command'],
            ['Usage', 'Corrections', 'Changements m\u00e9tier'],
        ], [35, 60, 75])
    pdf.p(
        "Exemple : piste 0.99 -> 0.49. SCD1 perd le prix. "
        "SCD2 conserve les deux versions.")

    pdf.add_page()
    pm['III'] = pdf.page_no()
    pdf.titre_I('III', 'D\u00e9monstration')

    pm['III.A'] = pdf.page_no()
    pdf.titre_III('A', 'Orchestration globale')
    pdf.figure(img('RUN_ALL_ETL.png'), "00_RUN_ALL : DSA -> ODS -> DWH", 125)

    pm['III.B'] = pdf.page_no()
    pdf.titre_III('B', 'Flux SCD2 en d\u00e9tail')
    pdf.figure(img('LOAD_DIM_TRACK_NON_EXECUTER.png'),
               "SCD2 DIM_TRACK avant ex\u00e9cution", 115)
    pdf.figure(img('LOAD_DIM_TRACK_EXUTOION COMPLETE ET FONCTIONNELLE.png'),
               "SCD2 apr\u00e8s ex\u00e9cution r\u00e9ussie", 115)

    pm['III.C'] = pdf.page_no()
    pdf.titre_III('C', 'V\u00e9rification du SCD2')
    pdf.figure(img('RESULTAT_SCD2_SSMS_SIMPLE.png'),
               "AVANT (0.99) et APRES (0.49)", 130)
    pdf.figure(img('RESULTAT_SCD2_SSMS_AVECDETAILS_NOMBRE_DE_LIGNES '
                   'hISTORISEES.png'),
               "Lignes historis\u00e9es dans DIM_TRACK", 130)

    pm['III.D'] = pdf.page_no()
    pdf.titre_III('D', 'Coh\u00e9rence des donn\u00e9es')
    pdf.figure(img('SUIVI_EVOLUTION PAR_COUCHE.png'),
               "Lignes par couche", 130)
    pdf.figure(img('EVOLUTION CA (STORE ET ONLINE ).png'),
               "CA par couche", 130)

    pdf.add_page()
    pm['IV'] = pdf.page_no()
    pdf.titre_I('IV', 'Automatisation')

    pm['IV.A'] = pdf.page_no()
    pdf.titre_III('A', 'SQL Server Agent')
    pdf.p("Planification via Jobs, Steps, Schedule.")
    pdf.code(
        'USE msdb;\n'
        "EXEC sp_add_job @job_name = 'ETL_RUN_ALL_NIGHTLY';\n"
        "EXEC sp_add_jobstep @job_name = 'ETL_RUN_ALL_NIGHTLY',\n"
        "    @step_name = 'Executer 00_RUN_ALL',\n"
        "    @subsystem = 'SSIS',\n"
        "    @command = '\\SSISDB\\ETL_Chinook\\00_RUN_ALL.dtsx';\n"
        "EXEC sp_add_schedule @schedule_name = 'Nuit_2h',\n"
        '    @freq_type = 4, @active_start_time = 020000;')

    pm['IV.B'] = pdf.page_no()
    pdf.titre_III('B', 'Triggers T-SQL')
    pdf.p("D\u00e9tection automatique des changements de prix :")
    pdf.code(
        'CREATE TRIGGER trg_Track_PriceChange\n'
        'ON [Chinook_LOKOUN_THYS].[dbo].[Track]\n'
        'AFTER UPDATE AS\n'
        'BEGIN\n'
        '    IF UPDATE(UnitPrice)\n'
        '        EXEC msdb.dbo.sp_start_job\n'
        "            @job_name = 'ETL_RUN_ALL_NIGHTLY';\n"
        'END;')

    pdf.add_page()
    pm['V'] = pdf.page_no()
    pdf.titre_I('V', 'Glossaire')
    glossaire = [
        ('ETL', "Extract, Transform, Load. Processus d'int\u00e9gration."),
        ('SSIS', "SQL Server Integration Services. Outil ETL Microsoft."),
        ('DSA', "Data Staging Area. Zone de transit (TRUNCATE)."),
        ('ODS', "Operational Data Store. Couche avec LOAD_DATE."),
        ('DWH', "Data Warehouse. Mod\u00e8le en \u00e9toile."),
        ('SCD', "Slowly Changing Dimension. Type 1/Type 2."),
        ('TK', "Technical Key. Cl\u00e9 primaire artificielle."),
        ('NK', "Natural Key. Cl\u00e9 de la source."),
        ('MERGE', "INSERT/UPDATE/DELETE en une instruction."),
        ('CTE', "Common Table Expression (WITH ... AS)."),
        ('Lookup', "Recherche dans une table de r\u00e9f\u00e9rence."),
        ('TRUNCATE', "Vide une table rapidement."),
        ('Star Schema', "Faits au centre, dimensions autour."),
        ('SSDT', "SQL Server Data Tools (plugin VS)."),
    ]
    for terme, definition in glossaire:
        pdf.saut(12)
        pdf.set_font('Times', 'B', 10)
        pdf.set_text_color(*BLEU)
        pdf.set_x(M_LEFT)
        pdf.cell(25, 6, s(terme), 0, 0, 'L')
        pdf.set_font('Times', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(CONTENT_W - 25, 6, s(definition), 0, 'J')
        pdf.ln(1)

    if save:
        out = os.path.join(BASE, 'EXPOSE_SSIS_LOKOUN_THYS.pdf')
        try:
            pdf.output(out)
        except PermissionError:
            out = os.path.join(BASE, 'EXPOSE_SSIS_LOKOUN_THYS_v2.pdf')
            pdf.output(out)
        print('EXPOSE : ' + out)
        print('  Pages : ' + str(pdf.page_no()) +
              ', Figures : ' + str(pdf.fig_num))
        return pdf.page_no(), pdf.fig_num
    else:
        return pm


def generer_expose():
    page_map = _build_expose(save=False)
    return _build_expose(save=True, toc_pages=page_map)


# =============================================================================
if __name__ == '__main__':
    print('=' * 60)
    print('Generation des deux documents PDF')
    print('=' * 60)
    print()
    p1, f1 = generer_rapport()
    print()
    p2, f2 = generer_expose()
    print()
    print('=' * 60)
    print('RAPPORT SAE4 : ' + str(p1) + ' pages, ' + str(f1) + ' figures')
    print('EXPOSE SSIS  : ' + str(p2) + ' pages, ' + str(f2) + ' figures')
    print('=' * 60)
