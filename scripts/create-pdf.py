"""Generate a cleaner, premium/tech 4-page submission PDF.

Drop-in replacement for the original ReportLab generator.
Requires: reportlab, pypdf
Optional preview rendering: pymupdf
"""

from pathlib import Path
from xml.sax.saxutils import escape
import json

from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent.parent
A = json.loads((ROOT / "app/article.json").read_text(encoding="utf-8"))

ARTICLE_NUMBER = "01"
AUTHOR_NAME = "Anton Betak"
OUTPUT_NAME = f"{ARTICLE_NUMBER}_{AUTHOR_NAME}.pdf"

OUT = ROOT / "output/pdf" / OUTPUT_NAME
PUBLIC_OUT = ROOT / "public" / OUTPUT_NAME
LEGACY_OUT = ROOT / "output/pdf/noticia-01-astra.pdf"
LEGACY_PUBLIC_OUT = ROOT / "public/noticia-01-astra.pdf"

OUT.parent.mkdir(parents=True, exist_ok=True)

# ============================================================
# TAMAÑO DE PÁGINA
# ============================================================

W, H = 595.28, 841.89

# ============================================================
# SISTEMA VISUAL
# ============================================================

BG = "#F7F8FC"
PAPER = "#FFFFFF"

INK = "#101424"
MUTED = "#646D7C"

NAVY = "#0A1020"
NAVY_2 = "#111A31"

PURPLE = "#6D5DFB"
PURPLE_SOFT = "#EEEAFE"

CYAN = "#22D3EE"
CYAN_SOFT = "#E7FAFE"

LINE = "#E5E8EF"
SOFT = "#F0F2F7"
WHITE = "#FFFFFF"

MARGIN = 38
CONTENT_W = W - 2 * MARGIN
FOOTER_TOP = 790

# ============================================================
# PDF
# ============================================================

c = canvas.Canvas(str(OUT), pagesize=(W, H))

c.setTitle(
    f"Noticia {ARTICLE_NUMBER} - GPT-6 Astra, sistemas y mercadotecnia"
)

c.setAuthor(
    f"Cuaderno de prensa - {AUTHOR_NAME}"
)

# ============================================================
# ESTILOS DE TEXTO
# ============================================================

styles = {

    "hero": ParagraphStyle(
        "hero",
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=28,
        textColor=HexColor(WHITE),
        spaceAfter=0,
    ),

    "page_title": ParagraphStyle(
        "page_title",
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=24,
        textColor=HexColor(INK),
        spaceAfter=0,
    ),

    "body": ParagraphStyle(
        "body",
        fontName="Helvetica",
        fontSize=9.35,
        leading=14.2,
        textColor=HexColor(MUTED),
        spaceAfter=0,
    ),

    "body_dark": ParagraphStyle(
        "body_dark",
        fontName="Helvetica",
        fontSize=9.1,
        leading=13.7,
        textColor=HexColor("#D7DEEC"),
        spaceAfter=0,
    ),

    "small": ParagraphStyle(
        "small",
        fontName="Helvetica",
        fontSize=7.8,
        leading=11,
        textColor=HexColor(MUTED),
        spaceAfter=0,
    ),

    "small_light": ParagraphStyle(
        "small_light",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10.5,
        textColor=HexColor("#BCC7DB"),
        spaceAfter=0,
    ),

    "sub": ParagraphStyle(
        "sub",
        fontName="Helvetica-Bold",
        fontSize=11.2,
        leading=14,
        textColor=HexColor(INK),
        spaceAfter=0,
    ),

    "card_title": ParagraphStyle(
        "card_title",
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=15,
        textColor=HexColor(INK),
        spaceAfter=0,
    ),

    "source": ParagraphStyle(
        "source",
        fontName="Helvetica",
        fontSize=7.4,
        leading=10.3,
        textColor=HexColor(MUTED),
        spaceAfter=0,
        splitLongWords=True,
    ),
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def C(hex_value):
    return HexColor(hex_value)


def y_from_top(top):
    return H - top


def rounded_box(
    x,
    top,
    width,
    height,
    fill,
    radius=12,
    stroke=None,
    stroke_width=1,
):

    c.setFillColor(C(fill))

    if stroke:
        c.setStrokeColor(C(stroke))
        c.setLineWidth(stroke_width)
        stroke_flag = 1
    else:
        stroke_flag = 0

    c.roundRect(
        x,
        H - top - height,
        width,
        height,
        radius,
        fill=1,
        stroke=stroke_flag,
    )


def hline(
    top,
    x=MARGIN,
    width=CONTENT_W,
    color=LINE,
    thickness=0.7,
):

    c.setStrokeColor(C(color))
    c.setLineWidth(thickness)

    c.line(
        x,
        y_from_top(top),
        x + width,
        y_from_top(top),
    )


def paragraph(
    html,
    x,
    top,
    width,
    style="body",
    color=None,
):

    st = styles[style]

    if color:
        st = ParagraphStyle(
            f"{style}_temp",
            parent=st,
            textColor=C(color),
        )

    p = Paragraph(html, st)

    _, ph = p.wrap(
        width,
        2000,
    )

    p.drawOn(
        c,
        x,
        H - top - ph,
    )

    return top + ph


def plain(s):
    return escape(str(s))


def draw_label(
    text,
    x,
    top,
    color=MUTED,
    size=7.2,
    right=None,
):

    c.setFillColor(C(color))
    c.setFont(
        "Helvetica-Bold",
        size,
    )

    if right is None:

        c.drawString(
            x,
            H - top - size,
            text,
        )

    else:

        c.drawRightString(
            right,
            H - top - size,
            text,
        )


# ============================================================
# BASE DE TODAS LAS PÁGINAS
# ============================================================

def page_base(
    page,
    footer_tag,
):

    # fondo general
    c.setFillColor(C(BG))

    c.rect(
        0,
        0,
        W,
        H,
        fill=1,
        stroke=0,
    )

    # hoja blanca interior
    c.setFillColor(C(PAPER))

    c.rect(
        18,
        18,
        W - 36,
        H - 36,
        fill=1,
        stroke=0,
    )

    # etiqueta superior izquierda
    rounded_box(
        MARGIN,
        31,
        44,
        20,
        NAVY,
        radius=6,
    )

    c.setFillColor(C(WHITE))

    c.setFont(
        "Helvetica-Bold",
        7.2,
    )

    c.drawCentredString(
        MARGIN + 22,
        H - 44,
        f"N/{ARTICLE_NUMBER}",
    )

    # encabezados
    draw_label(
        "CUADERNO DE PRENSA",
        MARGIN + 56,
        37,
        color=MUTED,
    )

    draw_label(
        "SISTEMAS COMPUTACIONALES  /  MERCADOTECNIA",
        MARGIN,
        37,
        color=MUTED,
        right=W - MARGIN,
    )

    hline(
        61,
        color=LINE,
    )

    # footer
    hline(
        777,
        color=LINE,
    )

    draw_label(
        footer_tag,
        MARGIN,
        793,
        color=MUTED,
        size=6.8,
    )

    draw_label(
        f"{page:02d} / 04",
        MARGIN,
        793,
        color=INK,
        size=6.8,
        right=W - MARGIN,
    )


# ============================================================
# ENCABEZADO DE CADA SECCIÓN
# ============================================================

def section_header(
    number,
    eyebrow,
    title,
    top=84,
):

    # caja de número
    rounded_box(
        MARGIN,
        top,
        42,
        42,
        PURPLE,
        radius=10,
    )

    c.setFillColor(C(WHITE))

    c.setFont(
        "Helvetica-Bold",
        14,
    )

    c.drawCentredString(
        MARGIN + 21,
        H - top - 27,
        f"{int(number):02d}",
    )

    # etiqueta
    draw_label(
        eyebrow.upper(),
        MARGIN + 56,
        top + 2,
        color=PURPLE,
        size=7.0,
    )

    # título
    bottom = paragraph(
        title,
        MARGIN + 56,
        top + 14,
        CONTENT_W - 56,
        "page_title",
    )

    return max(
        top + 42,
        bottom,
    ) + 21


# ============================================================
# DECORACIÓN TIPO CIRCUITO
# ============================================================

def draw_circuit_accent(
    x,
    top,
    w,
    h,
):

    c.saveState()

    c.setStrokeColor(
        C("#33415D")
    )

    c.setFillColor(
        C(CYAN)
    )

    c.setLineWidth(0.9)

    lines = [

        (
            x,
            top + 22,
            x + 48,
            top + 22,
        ),

        (
            x + 48,
            top + 22,
            x + 48,
            top + 44,
        ),

        (
            x + 48,
            top + 44,
            x + 92,
            top + 44,
        ),

        (
            x + 20,
            top + 75,
            x + 66,
            top + 75,
        ),

        (
            x + 66,
            top + 75,
            x + 66,
            top + 100,
        ),

        (
            x + 66,
            top + 100,
            x + 126,
            top + 100,
        ),

    ]

    for x1, t1, x2, t2 in lines:

        c.line(
            x1,
            H - t1,
            x2,
            H - t2,
        )

    for dx, dt in [

        (0, 22),
        (92, 44),
        (20, 75),
        (126, 100),

    ]:

        c.circle(
            x + dx,
            H - (top + dt),
            2.2,
            fill=1,
            stroke=0,
        )

    c.restoreState()


# ============================================================
# PÁGINA 1
# PORTADA + RESUMEN
# ============================================================

page_base(
    1,
    "INTERNET  /  NOTICIA PUBLICADA EL 4 DE SEPTIEMBRE DE 2026",
)

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------

HERO_TOP = 82
HERO_H = 206

rounded_box(
    MARGIN,
    HERO_TOP,
    CONTENT_W,
    HERO_H,
    NAVY,
    radius=18,
)

# etiqueta
rounded_box(
    MARGIN + 18,
    HERO_TOP + 18,
    112,
    20,
    NAVY_2,
    radius=7,
    stroke="#26304A",
)

draw_label(
    "GPT-6 ASTRA / OPENAI",
    MARGIN + 29,
    HERO_TOP + 24,
    color=CYAN,
    size=6.6,
)

# ------------------------------------------------------------
# TÍTULO IZQUIERDO
# ------------------------------------------------------------

t = paragraph(
    "Sistemas que<br/>"
    "conectan con<br/>"
    "el mercado.",
    MARGIN + 20,
    HERO_TOP + 54,
    270,
    "hero",
)

paragraph(
    "Ingeniería en Sistemas Computacionales<br/>"
    "Asignatura: Mercadotecnia",
    MARGIN + 20,
    max(
        t + 11,
        HERO_TOP + 148,
    ),
    270,
    "small_light",
)

# ------------------------------------------------------------
# MÓDULO VISUAL DERECHO
# ------------------------------------------------------------

VIS_X = 365
VIS_TOP = HERO_TOP + 24
VIS_W = 172
VIS_H = 126

rounded_box(
    VIS_X,
    VIS_TOP,
    VIS_W,
    VIS_H,
    NAVY_2,
    radius=15,
    stroke="#273452",
)

draw_circuit_accent(
    VIS_X + 18,
    VIS_TOP + 10,
    VIS_W - 36,
    VIS_H - 20,
)

# órbitas
cx = VIS_X + VIS_W / 2
cy = H - (VIS_TOP + 63)

c.setStrokeColor(
    C(CYAN)
)

c.setLineWidth(1.0)

for radius in (
    34,
    46,
    57,
):

    c.circle(
        cx,
        cy,
        radius,
        fill=0,
        stroke=1,
    )

# esfera central
c.setFillColor(
    C(PURPLE)
)

c.circle(
    cx,
    cy,
    25,
    fill=1,
    stroke=0,
)

c.setFillColor(
    C(NAVY)
)

c.circle(
    cx,
    cy,
    15,
    fill=1,
    stroke=0,
)

c.setFillColor(
    C(WHITE)
)

c.setFont(
    "Helvetica-Bold",
    8.5,
)

c.drawCentredString(
    cx,
    cy - 3,
    "ASTRA",
)

# ------------------------------------------------------------
# IMAGEN ASTRA
# ------------------------------------------------------------

img_path = ROOT / "public/assets/astra.png"

if img_path.exists():

    rounded_box(
        VIS_X + 10,
        VIS_TOP + 137,
        VIS_W - 20,
        42,
        "#0D1529",
        radius=8,
        stroke="#26304A",
    )

    c.drawImage(
        str(img_path),
        VIS_X + 14,
        H - (VIS_TOP + 174),
        width=62,
        height=35,
        preserveAspectRatio=True,
        mask="auto",
    )

    paragraph(
        "Ilustración de apoyo<br/>"
        "Tom's Guide",
        VIS_X + 84,
        VIS_TOP + 147,
        70,
        "small_light",
    )


# ------------------------------------------------------------
# METADATOS
# ------------------------------------------------------------

META_TOP = 301

rounded_box(
    MARGIN,
    META_TOP,
    CONTENT_W,
    35,
    SOFT,
    radius=10,
)

draw_label(
    "LANZAMIENTO",
    MARGIN + 14,
    META_TOP + 9,
    color=PURPLE,
    size=6.4,
)

draw_label(
    "03 SEP 2026",
    MARGIN + 14,
    META_TOP + 20,
    color=INK,
    size=7.0,
)

draw_label(
    "CONSULTA",
    MARGIN + 150,
    META_TOP + 9,
    color=PURPLE,
    size=6.4,
)

draw_label(
    "06 SEP 2026",
    MARGIN + 150,
    META_TOP + 20,
    color=INK,
    size=7.0,
)

draw_label(
    "FUENTE",
    MARGIN + 275,
    META_TOP + 9,
    color=PURPLE,
    size=6.4,
)

draw_label(
    "TOM'S GUIDE + OPENAI",
    MARGIN + 275,
    META_TOP + 20,
    color=INK,
    size=7.0,
)

# ------------------------------------------------------------
# RESUMEN
# ------------------------------------------------------------

Y = section_header(
    1,
    "ANÁLISIS",
    "¿De qué trata la noticia?",
    top=357,
)

for p in (
    A["summary"]
    + A["pdf_extra"]["context"]
):

    Y = paragraph(
        plain(p),
        MARGIN,
        Y,
        CONTENT_W,
        "body",
    ) + 9


assert Y < FOOTER_TOP - 12, (
    "page1 overflow",
    Y,
)

c.showPage()


# ============================================================
# PÁGINA 2
# IMPORTANCIA
# ============================================================

page_base(
    2,
    "IMPORTANCIA  /  TECNOLOGÍA Y VALOR PARA EL CLIENTE",
)

Y = section_header(
    2,
    "LECTURA CRÍTICA",
    "¿Qué importancia tiene?",
    top=86,
)

for p in (
    [A["importance"]]
    + A["pdf_extra"]["importance"]
):

    Y = paragraph(
        plain(p),
        MARGIN,
        Y,
        CONTENT_W,
        "body",
    ) + 9

Y += 8

hline(Y)

Y += 20

# ------------------------------------------------------------
# TARJETAS
# ------------------------------------------------------------

GAP = 14

CARD_W = (
    CONTENT_W - GAP
) / 2

CARD_TOP = Y

CARD_H = 196

# tarjeta izquierda
rounded_box(
    MARGIN,
    CARD_TOP,
    CARD_W,
    CARD_H,
    PURPLE_SOFT,
    radius=14,
)

# tarjeta derecha
rounded_box(
    MARGIN + CARD_W + GAP,
    CARD_TOP,
    CARD_W,
    CARD_H,
    CYAN_SOFT,
    radius=14,
)

# ------------------------------------------------------------
# OPORTUNIDAD
# ------------------------------------------------------------

rounded_box(
    MARGIN + 14,
    CARD_TOP + 14,
    32,
    32,
    PURPLE,
    radius=8,
)

c.setFillColor(
    C(WHITE)
)

c.setFont(
    "Helvetica-Bold",
    9,
)

c.drawCentredString(
    MARGIN + 30,
    H - CARD_TOP - 34,
    "01",
)

paragraph(
    "La oportunidad",
    MARGIN + 56,
    CARD_TOP + 17,
    CARD_W - 70,
    "card_title",
)

paragraph(
    plain(
        A["opportunity"]
    ),
    MARGIN + 14,
    CARD_TOP + 60,
    CARD_W - 28,
    "body",
)

# ------------------------------------------------------------
# RESPONSABILIDAD
# ------------------------------------------------------------

RX = (
    MARGIN
    + CARD_W
    + GAP
)

rounded_box(
    RX + 14,
    CARD_TOP + 14,
    32,
    32,
    NAVY,
    radius=8,
)

c.setFillColor(
    C(WHITE)
)

c.setFont(
    "Helvetica-Bold",
    9,
)

c.drawCentredString(
    RX + 30,
    H - CARD_TOP - 34,
    "02",
)

paragraph(
    "La responsabilidad",
    RX + 56,
    CARD_TOP + 17,
    CARD_W - 70,
    "card_title",
)

paragraph(
    plain(
        A["risk"]
    ),
    RX + 14,
    CARD_TOP + 60,
    CARD_W - 28,
    "body",
)

# ------------------------------------------------------------
# IDEA CLAVE
# ------------------------------------------------------------

Y = (
    CARD_TOP
    + CARD_H
    + 22
)

rounded_box(
    MARGIN,
    Y,
    CONTENT_W,
    84,
    NAVY,
    radius=14,
)

paragraph(
    "<b>Idea clave.</b> "
    "El punto de encuentro entre ambas áreas es evaluar si la solución "
    "funciona y si aporta valor. Una buena implementación técnica debe "
    "acompañarse de objetivos comerciales claros y de una experiencia "
    "útil para las personas.",
    MARGIN + 18,
    Y + 19,
    CONTENT_W - 36,
    "body_dark",
)

assert (
    Y + 84
    < FOOTER_TOP - 12
), (
    "page2 overflow",
    Y,
)

c.showPage()


# ============================================================
# PÁGINA 3
# TEMAS DE LA ASIGNATURA
# ============================================================

page_base(
    3,
    "ASIGNATURA: MERCADOTECNIA  /  APLICACIÓN",
)

Y = section_header(
    3,
    "CONEXIONES",
    "¿Cómo y con qué temas de la asignatura se relaciona?",
    top=86,
)

# ------------------------------------------------------------
# TARJETAS DE TEMAS
# ------------------------------------------------------------

for i, topic in enumerate(
    A["topics"],
    start=1,
):

    p_title = Paragraph(
        plain(
            topic["title"]
        ),
        styles["sub"],
    )

    _, ht = p_title.wrap(
        CONTENT_W - 80,
        500,
    )

    p_body = Paragraph(
        plain(
            topic["text"]
        ),
        styles["body"],
    )

    _, hb = p_body.wrap(
        CONTENT_W - 80,
        1000,
    )

    card_h = max(
        68,
        ht + hb + 25,
    )

    rounded_box(
        MARGIN,
        Y,
        CONTENT_W,
        card_h,
        PAPER,
        radius=12,
        stroke=LINE,
    )

    rounded_box(
        MARGIN + 12,
        Y + 14,
        38,
        38,
        SOFT,
        radius=9,
    )

    c.setFillColor(
        C(PURPLE)
    )

    c.setFont(
        "Helvetica-Bold",
        9,
    )

    c.drawCentredString(
        MARGIN + 31,
        H - Y - 38,
        str(
            topic.get(
                "number",
                f"0{i}",
            )
        ),
    )

    yy = paragraph(
        plain(
            topic["title"]
        ),
        MARGIN + 64,
        Y + 14,
        CONTENT_W - 78,
        "sub",
    ) + 5

    paragraph(
        plain(
            topic["text"]
        ),
        MARGIN + 64,
        yy,
        CONTENT_W - 78,
        "body",
    )

    Y += (
        card_h
        + 6
    )


# ------------------------------------------------------------
# EJEMPLO
# ------------------------------------------------------------

Y += 6

hline(Y)

Y += 18

draw_label(
    "EJEMPLO HIPOTÉTICO",
    MARGIN,
    Y,
    color=PURPLE,
    size=7.0,
)

Y = paragraph(
    plain(
        A["example"]["title"]
    ),
    MARGIN,
    Y + 15,
    CONTENT_W,
    "sub",
) + 14

steps = A["example"]["steps"]

STEP_GAP = 10

STEP_W = (
    CONTENT_W
    - STEP_GAP
    * (
        len(steps) - 1
    )
) / len(steps)

for i, step in enumerate(
    steps
):

    x = (
        MARGIN
        + i
        * (
            STEP_W
            + STEP_GAP
        )
    )

    rounded_box(
        x,
        Y,
        STEP_W,
        118,
        NAVY
        if i == 0
        else SOFT,
        radius=12,
    )

    accent = (
        CYAN
        if i == 0
        else PURPLE
    )

    draw_label(
        f"0{i + 1}",
        x + 13,
        Y + 12,
        color=accent,
        size=7.0,
    )

    title_style = (
        "small_light"
        if i == 0
        else "small"
    )

    body_style = (
        "small_light"
        if i == 0
        else "small"
    )

    title_color = (
        WHITE
        if i == 0
        else INK
    )

    yy = paragraph(
        f"<b>{plain(step['title'])}</b>",
        x + 13,
        Y + 29,
        STEP_W - 26,
        title_style,
        title_color,
    ) + 6

    paragraph(
        plain(
            step["text"]
        ),
        x + 13,
        yy,
        STEP_W - 26,
        body_style,
    )

Y += 124

# decisión
rounded_box(
    MARGIN,
    Y,
    CONTENT_W,
    50,
    PURPLE_SOFT,
    radius=12,
)

paragraph(
    f"<b>Decisión:</b> "
    f"{plain(A['example']['decision'])}",
    MARGIN + 15,
    Y + 15,
    CONTENT_W - 30,
    "small",
)

assert (
    Y + 56
    < FOOTER_TOP - 12
), (
    "page3 overflow",
    Y,
)

c.showPage()


# ============================================================
# PÁGINA 4
# PROFESIÓN + FUENTES
# ============================================================

page_base(
    4,
    "INGENIERÍA EN SISTEMAS COMPUTACIONALES  /  REFLEXIÓN",
)

Y = section_header(
    4,
    "PROFESIÓN",
    "¿Cómo se relaciona con mi profesión?",
    top=86,
)

profession_paragraphs = (
    A["profession"]
    + [
        A[
            "pdf_extra"
        ][
            "profession"
        ][
            1
        ]
    ]
)

for p in profession_paragraphs:

    Y = paragraph(
        plain(p),
        MARGIN,
        Y,
        CONTENT_W,
        "body",
    ) + 9


# ------------------------------------------------------------
# CONCLUSIÓN
# ------------------------------------------------------------

Y += 6

rounded_box(
    MARGIN,
    Y,
    CONTENT_W,
    94,
    NAVY,
    radius=15,
)

draw_label(
    "CONCLUSIÓN",
    MARGIN + 18,
    Y + 16,
    color=CYAN,
    size=6.8,
)

paragraph(
    f"<b>{plain(A['conclusion'])}</b>",
    MARGIN + 18,
    Y + 34,
    CONTENT_W - 36,
    "body_dark",
)

Y += 114

hline(Y)

Y += 17

draw_label(
    "FUENTES Y REFERENCIAS",
    MARGIN,
    Y,
    color=PURPLE,
    size=7.0,
)

Y += 17


# ------------------------------------------------------------
# FUENTES
# ------------------------------------------------------------

for source in A["sources"]:

    rounded_box(
        MARGIN,
        Y,
        CONTENT_W,
        51,
        PAPER,
        radius=9,
        stroke=LINE,
    )

    rounded_box(
        MARGIN + 10,
        Y + 10,
        30,
        30,
        SOFT,
        radius=8,
    )

    c.setFillColor(
        C(PURPLE)
    )

    c.setFont(
        "Helvetica-Bold",
        8,
    )

    c.drawCentredString(
        MARGIN + 25,
        H - Y - 29,
        f"[{source['id']}]",
    )

    paragraph(
        f"<b>{plain(source['author'])}</b> "
        f"· {plain(source['date'])}",
        MARGIN + 50,
        Y + 9,
        CONTENT_W - 62,
        "source",
    )

    paragraph(
        f"<link href='{source['url']}' "
        f"color='{PURPLE}'>"
        f"<b>{plain(source['title'])}</b>"
        f"</link>",
        MARGIN + 50,
        Y + 25,
        CONTENT_W - 62,
        "source",
    )

    Y += 59


# ------------------------------------------------------------
# NOTA FINAL
# ------------------------------------------------------------

Y += 5

paragraph(
    "Consulta: 6 de septiembre de 2026. "
    "Fuente de Internet: Tom's Guide. "
    "Contraste: anuncio oficial de OpenAI. "
    "Las aplicaciones propuestas y el ejemplo de la cafetería "
    "son una reflexión sobre usos posibles, no resultados "
    "documentados de una campaña.",
    MARGIN,
    Y,
    CONTENT_W,
    "source",
)

assert Y < FOOTER_TOP - 12, (
    "page4 overflow",
    Y,
)

c.save()


# ============================================================
# COPIAR PDF A LAS DIFERENTES CARPETAS
# ============================================================

PDF_BYTES = OUT.read_bytes()

PUBLIC_OUT.write_bytes(
    PDF_BYTES
)

LEGACY_OUT.write_bytes(
    PDF_BYTES
)

LEGACY_PUBLIC_OUT.write_bytes(
    PDF_BYTES
)

print(OUT)


# ============================================================
# VALIDACIÓN DEL PDF
# ============================================================

from pypdf import PdfReader

r = PdfReader(OUT)

assert len(r.pages) == 4

whole = " ".join(
    p.extract_text() or ""
    for p in r.pages
)

for q in [

    "¿De qué trata la noticia?",

    "¿Qué importancia tiene?",

    "con mi profesión?",

    "Ingeniería en Sistemas Computacionales",

]:

    assert q in whole, q


assert (
    "Como estudiante de mercadotecnia"
    not in whole
)

for i, p in enumerate(
    r.pages
):

    print(
        "Page",
        i + 1,
        "characters:",
        len(
            p.extract_text()
            or ""
        ),
    )

print(
    "Total words:",
    len(
        whole.split()
    ),
)


# ============================================================
# GENERAR PREVIEWS PNG OPCIONALES
# ============================================================

try:

    import pymupdf as fitz

    preview_dir = (
        ROOT
        / "tmp/pdfs"
    )

    preview_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    d = fitz.open(OUT)

    for i, p in enumerate(d):

        p.get_pixmap(
            matrix=fitz.Matrix(
                1.4,
                1.4,
            ),
            alpha=False,
        ).save(
            str(
                preview_dir
                / f"premium-page-{i + 1}.png"
            )
        )

except ImportError:

    pass