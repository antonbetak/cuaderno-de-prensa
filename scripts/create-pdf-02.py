"""Genera la Noticia 02 del Cuaderno de Prensa en un PDF de cuatro paginas."""

from pathlib import Path
from xml.sax.saxutils import escape
import json

from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "app/article-02.json").read_text(encoding="utf-8"))
OUT = ROOT / "output/pdf/02_Anton Betak.pdf"
PUBLIC_OUT = ROOT / "public/02_Anton Betak.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 595.28, 841.89
M = 38
CW = W - 2 * M

BG = "#F2F5F3"
PAPER = "#FFFFFF"
INK = "#10251D"
MUTED = "#607068"
DARK = "#09261D"
DARK_2 = "#11392D"
GREEN = "#12A56A"
GREEN_2 = "#25D366"
MINT = "#DFF7EA"
MINT_2 = "#EFFAF4"
LINE = "#DCE7E1"
WHITE = "#FFFFFF"


def col(value):
    return HexColor(value)


def safe(value):
    return escape(str(value))


styles = {
    "hero": ParagraphStyle("hero", fontName="Helvetica-Bold", fontSize=27, leading=29.5, textColor=col(WHITE)),
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20.5, leading=23.5, textColor=col(INK)),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.2, leading=13.6, textColor=col(MUTED)),
    "body_dark": ParagraphStyle("body_dark", fontName="Helvetica", fontSize=8.8, leading=12.6, textColor=col("#D2E3DB")),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=7.4, leading=10.3, textColor=col(MUTED)),
    "small_light": ParagraphStyle("small_light", fontName="Helvetica", fontSize=7.4, leading=10.2, textColor=col("#B7CEC4")),
    "card": ParagraphStyle("card", fontName="Helvetica", fontSize=8.35, leading=11.8, textColor=col(MUTED)),
    "card_title": ParagraphStyle("card_title", fontName="Helvetica-Bold", fontSize=10.8, leading=13, textColor=col(INK)),
    "quote": ParagraphStyle("quote", fontName="Helvetica-Bold", fontSize=12, leading=16.2, textColor=col(DARK)),
    "source": ParagraphStyle("source", fontName="Helvetica", fontSize=7.2, leading=9.6, textColor=col(MUTED), splitLongWords=True),
}

c = canvas.Canvas(str(OUT), pagesize=(W, H))
c.setTitle("Noticia 02 - El permiso también convierte")
c.setAuthor("Anton Betak")
c.setSubject("Cuaderno de prensa - Mercadotecnia e Ingeniería en Sistemas Computacionales")


def y(top):
    return H - top


def box(x, top, width, height, fill, radius=10, stroke=None, line_width=0.8):
    c.setFillColor(col(fill))
    if stroke:
        c.setStrokeColor(col(stroke))
        c.setLineWidth(line_width)
        do_stroke = 1
    else:
        do_stroke = 0
    c.roundRect(x, H - top - height, width, height, radius, fill=1, stroke=do_stroke)


def line(top, x=M, width=CW, color=LINE, thickness=0.7):
    c.setStrokeColor(col(color))
    c.setLineWidth(thickness)
    c.line(x, y(top), x + width, y(top))


def text(html, x, top, width, style="body", color=None):
    st = styles[style]
    if color:
        st = ParagraphStyle(style + "_temp", parent=st, textColor=col(color))
    p = Paragraph(html, st)
    _, ph = p.wrap(width, 2000)
    p.drawOn(c, x, H - top - ph)
    return top + ph


def label(value, x, top, color=MUTED, size=7.0, right=None):
    c.setFillColor(col(color))
    c.setFont("Helvetica-Bold", size)
    if right is None:
        c.drawString(x, H - top - size, value)
    else:
        c.drawRightString(right, H - top - size, value)


def base(page, footer):
    c.setFillColor(col(BG))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(col(PAPER))
    c.rect(18, 18, W - 36, H - 36, fill=1, stroke=0)
    box(M, 31, 44, 20, DARK, radius=6)
    c.setFillColor(col(WHITE))
    c.setFont("Helvetica-Bold", 7.2)
    c.drawCentredString(M + 22, H - 44, "N/02")
    label("CUADERNO DE PRENSA", M + 56, 37)
    label("SISTEMAS COMPUTACIONALES  /  MERCADOTECNIA", M, 37, right=W - M)
    line(61)
    line(777)
    label(footer, M, 793, size=6.55)
    label(f"{page:02d} / 04", M, 793, color=INK, size=6.8, right=W - M)


def heading(number, eyebrow, title, top=84):
    box(M, top, 42, 42, GREEN, radius=10)
    c.setFillColor(col(WHITE))
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(M + 21, H - top - 27, number)
    label(eyebrow.upper(), M + 56, top + 2, color=GREEN, size=7)
    bottom = text(title, M + 56, top + 14, CW - 56, "title")
    return max(top + 42, bottom) + 20


def phone_visual(x, top, width, height):
    box(x, top, width, height, DARK_2, radius=16, stroke="#2C5D4C")
    px = x + 30
    ptop = top + 15
    pw = width - 60
    ph = height - 30
    box(px, ptop, pw, ph, "#F8FBF9", radius=15)
    c.setFillColor(col(DARK))
    c.roundRect(px + pw / 2 - 16, H - ptop - 7, 32, 3, 1.5, fill=1, stroke=0)
    c.setFillColor(col(GREEN_2))
    c.circle(px + 18, H - (ptop + 35), 9, fill=1, stroke=0)
    c.setFillColor(col(WHITE))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(px + 18, H - (ptop + 38), "W")
    label("RECIBE NOVEDADES", px + 34, ptop + 29, color=INK, size=6.2)
    line(ptop + 51, px + 12, pw - 24, color="#D9E7E0", thickness=0.6)
    c.setFillColor(col(WHITE))
    c.setStrokeColor(col(GREEN))
    c.setLineWidth(1.3)
    c.roundRect(px + 14, H - (ptop + 77), 12, 12, 2, fill=1, stroke=1)
    c.setStrokeColor(col(GREEN))
    c.setLineWidth(1.8)
    c.line(px + 17, H - (ptop + 71), px + 20, H - (ptop + 74))
    c.line(px + 20, H - (ptop + 74), px + 25, H - (ptop + 67))
    text("Acepto recibir promociones<br/>por WhatsApp", px + 34, ptop + 61, pw - 48, "small")
    box(px + 14, ptop + 101, pw - 28, 23, GREEN, radius=6)
    c.setFillColor(col(WHITE))
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(px + pw / 2, H - (ptop + 116), "COMPLETAR COMPRA")


# PAGINA 1
base(1, "INTERNET  /  NOTICIA PUBLICADA EL 11 DE SEPTIEMBRE DE 2026")
box(M, 82, CW, 210, DARK, radius=18)
box(M + 18, 100, 148, 20, DARK_2, radius=6, stroke="#315849")
label("SHOPIFY / WHATSAPP / CHECKOUT", M + 29, 106, color=GREEN_2, size=6.25)
hero_bottom = text("El permiso<br/>también<br/>convierte.", M + 20, 138, 275, "hero")
text("Ingeniería en Sistemas Computacionales<br/>Asignatura: Mercadotecnia", M + 20, hero_bottom + 12, 260, "small_light")
phone_visual(361, 100, 174, 174)

top = heading("01", "La noticia", "¿De qué trata la noticia?", top=315)
for paragraph in DATA["summary"]:
    top = text(safe(paragraph), M, top, CW, "body") + 10
box(M, top + 3, CW, 54, MINT_2, radius=10, stroke=LINE)
label("IDEA CENTRAL", M + 15, top + 15, color=GREEN, size=6.7)
text("La tecnología incorpora el permiso de contacto dentro de la experiencia de compra; la estrategia comienza cuando la empresa decide cómo usarlo con relevancia y respeto.", M + 112, top + 12, CW - 128, "small")
c.showPage()


# PAGINA 2
base(2, "IMPORTANCIA  /  DATOS, CONFIANZA Y RELACION CON EL CLIENTE")
top = heading("02", "Lo que está en juego", "¿Qué importancia tiene?")
for paragraph in DATA["importance"]:
    top = text(safe(paragraph), M, top, CW, "body") + 10

gap = 12
card_w = (CW - gap) / 2
card_top = top + 2
for idx, (title_value, headline, body, fill, accent) in enumerate([
    ("LA OPORTUNIDAD", "Conversar despues de la compra.", DATA["opportunity"], MINT_2, GREEN),
    ("LA RESPONSABILIDAD", "El permiso tiene limites.", DATA["risk"], "#F7F4EE", "#D69038"),
]):
    x = M + idx * (card_w + gap)
    box(x, card_top, card_w, 123, fill, radius=12, stroke=LINE)
    label(title_value, x + 14, card_top + 15, color=accent, size=6.4)
    t = text(safe(headline), x + 14, card_top + 32, card_w - 28, "card_title")
    text(safe(body), x + 14, t + 9, card_w - 28, "card")

box(M, card_top + 139, CW, 72, DARK, radius=12)
label("REFLEXIÓN", M + 16, card_top + 154, color=GREEN_2, size=6.6)
text("La confianza también es un resultado de mercadotecnia. Si el sistema conserva el consentimiento correctamente y la marca cumple lo prometido, la tecnología fortalece la relación. Si falla cualquiera de las dos partes, el cliente percibe una sola mala experiencia.", M + 105, card_top + 151, CW - 123, "body_dark")
c.showPage()


# PAGINA 3
base(3, "ASIGNATURA: MERCADOTECNIA  /  APLICACION")
top = heading("03", "De la noticia a la clase", "¿Cómo y con qué temas de la<br/>asignatura se relaciona?")

for item in DATA["topics"]:
    box(M, top, CW, 70, MINT_2 if int(item["number"]) % 2 else PAPER, radius=10, stroke=LINE)
    box(M + 11, top + 12, 34, 34, GREEN if int(item["number"]) % 2 else DARK, radius=8)
    c.setFillColor(col(WHITE))
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(M + 28, H - top - 33, item["number"])
    text(safe(item["title"]), M + 57, top + 10, 172, "card_title")
    text(safe(item["text"]), M + 242, top + 10, CW - 255, "card")
    top += 78

box(M, top + 1, CW, 157, DARK, radius=14)
label("EJEMPLO HIPOTETICO", M + 17, top + 16, color=GREEN_2, size=6.7)
text(safe(DATA["example"]["title"]), M + 17, top + 34, CW - 34, "card_title", color=WHITE)
step_top = top + 63
step_w = (CW - 34) / 3
for i, step in enumerate(DATA["example"]["steps"]):
    x = M + 17 + i * step_w
    label(f"0{i+1}", x, step_top, color=GREEN_2, size=7)
    text(safe(step["title"]), x + 22, step_top - 3, step_w - 28, "card_title", color=WHITE)
    text(safe(step["text"]), x, step_top + 21, step_w - 14, "small_light")
text(safe(DATA["example"]["decision"]), M + 17, top + 124, CW - 34, "small_light")
c.showPage()


# PAGINA 4
base(4, "INGENIERIA EN SISTEMAS COMPUTACIONALES  /  REFLEXION")
top = heading("04", "Mi mirada profesional", "¿Cómo se relaciona con mi profesión?")
for paragraph in DATA["profession"]:
    top = text(safe(paragraph), M, top, CW, "body") + 9

box(M, top + 1, CW, 70, MINT, radius=12)
text(safe(DATA["conclusion"]), M + 18, top + 15, CW - 36, "quote")
source_top = top + 88
label("FUENTES Y REFERENCIAS", M, source_top, color=GREEN, size=7)
source_top += 16
for source in DATA["sources"]:
    box(M, source_top, CW, 58, PAPER, radius=8, stroke=LINE)
    label(f"[{source['id']}]  {source['type']}", M + 12, source_top + 10, color=GREEN, size=6.15)
    text(f"<b>{safe(source['title'])}</b><br/>{safe(source['author'])} - {safe(source['publisher'])} - {safe(source['date'])}<br/><font color='#3B705B'>{safe(source['url'])}</font>", M + 12, source_top + 22, CW - 24, "source")
    c.linkURL(source["url"], (M, H - source_top - 58, M + CW, H - source_top), relative=0)
    source_top += 66

text(f"Consulta: {safe(DATA['consulted'])}. La noticia fue contrastada con la documentación oficial de Shopify. El ejemplo y las aplicaciones profesionales son una reflexión propia.", M, source_top + 2, CW, "small")
c.save()

PUBLIC_OUT.write_bytes(OUT.read_bytes())
print(OUT)
