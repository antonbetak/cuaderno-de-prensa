"""Generate Noticia 03 using the project's ReportLab/JSON workflow.

All text is measured before drawing; overflow fails generation. All four
pages are rendered for visual QA. Does not regenerate editions 01 or 02.
"""
from pathlib import Path
import importlib.util
import json
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
import pymupdf as fitz

ROOT = Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('pdf_editorial', ROOT/'scripts/pdf-editorial.py')
core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
A=json.loads((ROOT/'app/article-03.json').read_text())
OUT=ROOT/'output/pdf/noticia-03-wired-agentes-ia.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
p=core.EditorialPDF(OUT,A['title'],4)
M,CW=core.M,core.CW

p.base(1,'NOTICIA 03 / REVISTA / 30 SEP 2026')
p.text('AI AGENT WARS',80,'label')
t=p.text('La batalla por convertirse<br/>en tu agente personal.',108,'hero',html=True)
t=p.text(A['subtitle'],t+18)+18
p.text('Reece Rogers / WIRED · Business / 30 septiembre 2026',t,'small')
p.text('Análisis: Anton Betak / Ingeniería en Sistemas Computacionales',t+17,'small')
t+=51
# Original vector illustration; deliberately abstract rather than product mascots.
c=p.canvas
c.setFillColor(HexColor('#EEEAE3')); c.rect(M,core.H-t-138,CW,138,fill=1,stroke=0)
c.setFillColor(HexColor('#ED563C')); c.circle(190,core.H-t-66,43,fill=1,stroke=0)
c.setFillColor(HexColor(core.INK)); c.roundRect(330,core.H-t-104,80,80,7,fill=1,stroke=0)
for x in [201,220,341,360]:
    c.setFillColor(HexColor(core.PAPER)); c.roundRect(x,core.H-t-70,6,17,3,fill=1,stroke=0)
p.text('OPENAI DOTS',t+112,'label',x=150,width=130)
p.text('VS',t+61,'label',x=291,width=25)
p.text('META MUSE',t+112,'label',x=335,width=110)
t+=154
p.text('01 / EL CONTEXTO · INFORMACIÓN DE WIRED',t,'label');t+=24
t=p.paragraphs(A['summary'],t)
p.text('La competencia ya no termina en una respuesta: se extiende a las tareas que el usuario decide delegar.',t+3,'sub')
c.showPage()

p.base(2,'IMPORTANCIA / DOS ESTRATEGIAS DE ENTRADA')
t=p.heading('02 / ANÁLISIS PERSONAL','De preguntar a delegar.')
p.text('CHATBOT: Pregunta > Respuesta',t,'sub'); t+=30
p.text('AGENTE: Contexto > Plan > Acción > Seguimiento',t,'sub');t+=29
p.text('Esquema conceptual propio. Cada acción depende de permisos y límites.',t,'small');t+=30
t=p.paragraphs(A['importance'],t)
p.line(t);t+=18
p.text('DOS ESTRATEGIAS / DATOS DE WIRED [1] + MI INTERPRETACIÓN',t,'label');t+=24
ends=[]
for i,s in enumerate(A['strategies']):
    x=M+i*(CW/2+10); width=CW/2-20
    u=p.text(s['name'],t,'label',x,width)+10
    u=p.text(s['price'],u,'sub',x,width)+9
    u=p.text(s['detail'],u,'small',x,width)+12
    ends.append(p.text(s['analysis'],u,'body',x,width))
c.showPage()

p.base(3,'MERCADOTECNIA / ANÁLISIS PERSONAL')
t=p.heading('03 / DE LA NOTICIA A LA CLASE','El producto también<br/>es la confianza.')
# Heading supports markup intentionally through the core helper below.
for i,m in enumerate(A['marketing']):
    p.line(t-5)
    p.text(f'0{i+1}',t+7,'label',width=24)
    u=p.text(m['title'],t+5,'sub',x=M+35,width=CW-35)+10
    t=p.text(m['text'],u,'body',x=M+35,width=CW-35)+26
c.showPage()

p.base(4,'INGENIERÍA EN SISTEMAS / REFLEXIÓN / REFERENCIAS')
t=p.heading('04 / MI MIRADA PROFESIONAL','Detrás de un mensaje sencillo.')
t=p.paragraphs(A['profession'],t)
p.text('EJEMPLO HIPOTÉTICO / NO ES UNA ARQUITECTURA OFICIAL',t,'label');t+=19
p.text('Usuario: “Reserva una cena para mañana”',t,'sub');t+=27
p.text('Modelo de IA > Contexto > Permisos > API / servicio externo<br/>Validación > Acción > Confirmación',t,'small',html=True);t+=35
p.text('Se debe verificar disponibilidad, datos y autorización antes de confirmar.',t,'small');t+=26
p.text('MI REFLEXIÓN',t,'label');t+=18
t=p.text(A['reflection'],t)+18
p.line(t-4)
p.text('REFERENCIA [1]',t+5,'label');t+=23
s=A['sources'][0]
t=p.text('Rogers, R. (2026, September 30). The Battle to Be Your Personal AI Agent Is Here. WIRED.',t,'small')+5
start=t
t=p.text(s['url'],t,'small')+7
c.linkURL(s['url'],(M,core.H-t,M+CW,core.H-start),relative=0)
p.text('Consulta: '+A['consulted']+'. '+A['sourceNote'],t,'small')
c.save()
reader=PdfReader(OUT)
assert len(reader.pages)==4
text='\n'.join(page.extract_text() for page in reader.pages)
for expected in ['Dos','confianza','Ingeniería','Rogers','REFLEXIÓN']:
    assert expected.lower() in text.lower(),expected
(ROOT/'public'/OUT.name).write_bytes(OUT.read_bytes())
preview=ROOT/'tmp/pdfs/noticia-03';preview.mkdir(parents=True,exist_ok=True)
doc=fitz.open(OUT)
for i,page in enumerate(doc):
    for block in page.get_text('blocks'):
        assert block[0]>=M-1 and block[2]<=core.W-M+1, f'Horizontal overflow on page {i+1}: {block}'
    page.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False).save(preview/f'page-{i+1}.png')
print(f'{OUT}\nPages: {len(reader.pages)}\nAll pages rendered: {preview}')
