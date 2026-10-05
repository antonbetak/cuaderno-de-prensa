"""Shared ReportLab primitives for new editorial editions.

Uses the top-based coordinates, Paragraph wrapping and A4 margins of the
existing create-pdf.py/create-pdf-02.py scripts, with explicit overflow guards.
The previous editions remain byte-for-byte unchanged.
"""
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

W, H, M = 595.28, 841.89, 42
CW = W - 2 * M
INK, MUTED, CORAL, PAPER, LINE = '#242528', '#514D47', '#B93622', '#FAF7F0', '#D5CFC5'

class EditorialPDF:
    def __init__(self, path, title, pages):
        self.canvas = canvas.Canvas(str(path), pagesize=(W, H))
        self.canvas.setTitle(title)
        self.canvas.setAuthor('Anton Betak')
        self.canvas.setSubject('Cuaderno de prensa / Mercadotecnia / Revista digital')
        self.pages = pages
        self.styles = {name: ParagraphStyle(name, fontName=font, fontSize=size,
                      leading=leading, textColor=HexColor(color))
                       for name, font, size, leading, color in [
            ('body', 'Helvetica', 10.5, 15.7, MUTED),
            ('small', 'Helvetica', 8.5, 12.5, MUTED),
            ('title', 'Helvetica-Bold', 30, 33, INK),
            ('hero', 'Helvetica-Bold', 36, 38, INK),
            ('sub', 'Helvetica-Bold', 15, 19, INK),
            ('label', 'Helvetica-Bold', 8, 11, CORAL),
        ]}

    def text(self, value, top, style='body', x=M, width=CW, html=False, limit=773):
        p = Paragraph(value if html else escape(value), self.styles[style])
        _, height = p.wrap(width, H)
        if top + height > limit:
            raise ValueError(f'Overflow: {value[:60]} ends at {top+height:.1f} > {limit}')
        p.drawOn(self.canvas, x, H-top-height)
        return top+height

    def line(self, top, x=M, width=CW):
        self.canvas.setStrokeColor(HexColor(LINE))
        self.canvas.line(x, H-top, x+width, H-top)

    def base(self, page, tag):
        c=self.canvas
        c.setFillColor(HexColor(PAPER)); c.rect(0,0,W,H,fill=1,stroke=0)
        self.text('N/03  ·  CUADERNO DE PRENSA', 31, 'label')
        self.text('REVISTA DIGITAL / WIRED', 31, 'label', x=350, width=203)
        self.line(55); self.line(792)
        self.text(tag, 803, 'small',width=450,limit=828)
        self.text(f'{page:02d} / {self.pages:02d}',803,'small',x=510,width=43,limit=828)

    def heading(self, label, title):
        self.text(label, 79, 'label')
        return self.text(title, 103, 'title', html=True)+22

    def paragraphs(self, values, top):
        for value in values: top=self.text(value,top)+12
        return top
