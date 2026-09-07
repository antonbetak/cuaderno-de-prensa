"""Generate the submission PDF from the same content used by the React site.
Requires: reportlab, pypdf; optional rendering: pymupdf.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent.parent
A=json.loads((ROOT/'app/article.json').read_text())
OUT=ROOT/'output/pdf/noticia-01-astra.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
W,H=595.28,841.89
INK='#141419'; MUTED='#60606c'; LIME='#cefc72'; PURPLE='#755394'
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('Noticia 01 - GPT-6 Astra, sistemas y mercadotecnia')
c.setAuthor('Cuaderno de prensa - Mercadotecnia')
styles={
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=10.5,leading=16,textColor=HexColor(MUTED),spaceAfter=0),
 'small':ParagraphStyle('small',fontName='Helvetica',fontSize=8.5,leading=12.5,textColor=HexColor(MUTED)),
 'heading':ParagraphStyle('heading',fontName='Helvetica',fontSize=25,leading=29,textColor=HexColor(INK)),
 'sub':ParagraphStyle('sub',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=HexColor(INK)),
 'quote':ParagraphStyle('quote',fontName='Times-Italic',fontSize=23,leading=29,textColor=HexColor('#4c355f')),
}
def text(s,x,top,width,style='body',color=None):
 st=styles[style]
 if color: st=ParagraphStyle('custom',parent=st,textColor=HexColor(color))
 p=Paragraph(s,st);pw,ph=p.wrap(width,1000);p.drawOn(c,x,H-top-ph)
 return top+ph

def label(s,x,top,color=PURPLE):
 c.setFillColor(HexColor(color));c.setFont('Helvetica-Bold',8);c.drawString(x,H-top-8,s)

def line(top,x=42,width=511):
 c.setStrokeColor(HexColor('#dcdce0'));c.setLineWidth(.6);c.line(x,H-top,x+width,H-top)

def base(page,tag):
 c.setFillColor(HexColor('#fafaf8'));c.rect(0,0,W,H,fill=1,stroke=0)
 label('m.   CUADERNO DE PRENSA',42,28,INK);label('MERCADOTECNIA / NOTICIA 01',365,28,MUTED)
 line(50);line(801)
 label(tag,42,813,MUTED);label(f'{page:02d} / 04',518,813,MUTED)

def section(n,title,top):
 label(n+' / ANÁLISIS',42,top);return text(title,42,top+20,511,'heading')+16

base(1,'INTERNET / NOTICIA PUBLICADA EL 4 DE SEPTIEMBRE DE 2026')
c.setFillColor(HexColor(INK));c.rect(0,H-265,W,199,fill=1,stroke=0)
label('GPT-6 ASTRA / OPENAI',42,83,LIME)
text('Sistemas que<br/>conectan con<br/>el mercado.',42,108,310,'heading','#ffffff')
text('Ingeniería en Sistemas Computacionales<br/>Asignatura: Mercadotecnia',42,211,310,'small','#bdbdc9')
c.drawImage(str(ROOT/'public/assets/astra.png'),350,H-246,width=205,height=115,preserveAspectRatio=True,mask='auto')
text('Ilustración: Future / ChatGPT, vía Tom’s Guide.',350,246,210,'small','#aaaab5')
y=section('01','¿De qué trata la noticia?',288)
for p in A['summary']+A['pdf_extra']['context']:
 y=text(escape(p),42,y,511)+12
line(y+6)
label('LANZAMIENTO: 03 SEP 2026 / CONSULTA: 06 SEP 2026',42,y+20)
assert y+35<790,('page1',y)
c.showPage()

base(2,'IMPORTANCIA / TECNOLOGÍA Y VALOR PARA EL CLIENTE')
y=section('02','¿Qué importancia tiene?',75)
for p in [A['importance']]+A['pdf_extra']['importance']:
 y=text(escape(p),42,y,511)+14
line(y);y+=20
for title,key in [('La oportunidad','opportunity'),('La responsabilidad','risk')]:
 y=text(title,42,y,511,'sub')+8
 y=text(escape(A[key]),42,y,511)+17
y=text('El punto de encuentro entre ambas áreas es evaluar si la solución funciona y si aporta valor. Una buena implementación técnica debe acompañarse de objetivos comerciales claros y de una experiencia útil para las personas.',42,y,511)
assert y<790,('page2',y)
c.showPage()

base(3,'ASIGNATURA: MERCADOTECNIA / APLICACIÓN')
y=section('03','¿Cómo y con qué temas de la<br/>asignatura se relaciona?',75)
for topic in A['topics']:
 label(topic['number'],42,y+3)
 y=text(escape(topic['title']),68,y,485,'sub')+7
 y=text(escape(topic['text']),68,y,485)+16
line(y-2);y+=15
label('EJEMPLO HIPOTÉTICO',42,y)
y=text(escape(A['example']['title']),42,y+19,511,'sub')+12
bottoms=[]
for i,step in enumerate(A['example']['steps']):
 x=42+i*175
 label(f'0{i+1}',x,y)
 z=text(escape(step['title']),x,y+18,155,'sub')+8
 bottoms.append(text(escape(step['text']),x,z,155,'small'))
y=max(bottoms)+15
y=text(escape(A['example']['decision']),42,y,511,'small')+10
assert y<790,('page3',y)
c.showPage()

base(4,'INGENIERÍA EN SISTEMAS COMPUTACIONALES / REFLEXIÓN')
y=section('04','¿Cómo se relaciona con mi profesión?',75)
for p in A['profession']+[A['pdf_extra']['profession'][1]]:
 y=text(escape(p),42,y,511)+11
y=text(escape(A['conclusion']),42,y+4,511,'sub')+20
line(y);y+=18
label('FUENTES Y REFERENCIAS',42,y);y+=20
for source in A['sources']:
 y=text(f"<b>[{source['id']}] {escape(source['author'])}</b> · {escape(source['date'])}",42,y,511,'small')+3
 y=text(f"<link href='{source['url']}' color='{PURPLE}'>{escape(source['title'])}</link>",42,y,511,'small')+3
 y=text(f"<link href='{source['url']}'>{escape(source['url'])}</link>",42,y,511,'small')+10
y=text('Consulta: 6 de septiembre de 2026. Fuente de Internet: Tom’s Guide. Contraste: anuncio oficial de OpenAI. Las aplicaciones propuestas y el ejemplo de la cafetería son una reflexión sobre usos posibles, no resultados documentados de una campaña.',42,y,511,'small')
assert y<790,('page4',y)
c.save()
(ROOT/'public/noticia-01-astra.pdf').write_bytes(OUT.read_bytes())
print(OUT)
from pypdf import PdfReader
r=PdfReader(OUT)
assert len(r.pages)==4
whole=' '.join(p.extract_text() for p in r.pages)
for q in ['¿De qué trata la noticia?', '¿Qué importancia tiene?', 'con mi profesión?', 'Ingeniería en Sistemas Computacionales', 'Investigación de mercados']:
 assert q in whole,q
assert 'Como estudiante de mercadotecnia' not in whole
for i,p in enumerate(r.pages): print('Page',i+1,'characters:',len(p.extract_text()))
print('Total words:',len(whole.split()))
try:
 import pymupdf as fitz
 d=fitz.open(OUT)
 for i,p in enumerate(d): p.get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(str(ROOT/f'tmp/pdfs/page-{i+1}.png'))
except ImportError: pass
