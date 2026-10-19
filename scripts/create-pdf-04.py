"""Noticia 04: four measured editorial pages from the shared article JSON."""
from pathlib import Path
import importlib.util
import json
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
import pymupdf as fitz

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('editorial',ROOT/'scripts/pdf-editorial.py')
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
A=json.loads((ROOT/'app/article-04.json').read_text())
OUT=ROOT/'output/pdf/noticia-04-forbes-gemelos-digitales.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
p=core.EditorialPDF(OUT,A['title'],4)
c=p.canvas
c.setAuthor('Anton Betak Licea');c.setSubject('Mercadotecnia Básica / Revista 02/02 / Forbes')
for name in p.styles:
    p.styles[name].textColor=HexColor('#176D49' if name=='label' else '#09271E' if name in ['hero','title','sub'] else '#3D5549')
p.styles['body'].fontSize=10;p.styles['body'].leading=14.4
p.styles['small'].fontSize=8.5;p.styles['small'].leading=12
M,CW,H=core.M,core.CW,core.H

def base(n,tag):
    c.setFillColor(HexColor('#F6FAF6'));c.rect(0,0,core.W,H,fill=1,stroke=0)
    p.text('N/04 · CUADERNO DE PRENSA',31,'label');p.text('FORBES / REVISTA 02/02',31,'label',x=365,width=188)
    p.line(55);p.line(792)
    p.text(tag,803,'small',width=440,limit=828);p.text(f'{n:02d} / 04',803,'small',x=510,width=43,limit=828)

def section(label,title):
    p.text(label,79,'label');return p.text(title,103,'title')+20

def twins(top,height):
    # Original scalable artwork: human silhouette and its digital mesh.
    from reportlab.graphics import renderPDF
    from svglib.svglib import svg2rlg
    d=svg2rlg(str(ROOT/'public/assets/digital-twins.svg'))
    scale=height/d.height;d.scale(scale,scale)
    renderPDF.draw(d,c,M+(CW-d.width*scale)/2,H-top-height)

base(1,'ANTON BETAK LICEA / MERCADOTECNIA BÁSICA')
p.text('04 / INVESTIGACIÓN DE CLIENTES / INTELIGENCIA ARTIFICIAL',81,'label')
t=p.text(A['title'],112,'hero')+20
t=p.text(A['subtitle'],t)+20
p.text('FORBES · Megan Poinski y CMO · Publicación: 14 octubre 2026',t,'small');t+=21
p.text('Anton Betak Licea / Ingeniería en Sistemas Computacionales',t,'small');t+=17
p.text('Mercadotecnia Básica / Trabajo: 19 de octubre de 2026',t,'small');t+=25
twins(t,240);t+=254
p.text('Ilustración vectorial original del cuaderno; no es una interfaz de Outset.',t,'small');t+=30
p.text('Escuchar a una persona. Explorar con un modelo. Validar con personas.',t,'sub')
c.showPage()

base(2,'ANÁLISIS / BENEFICIOS, ALCANCES Y LÍMITES')
t=section('01 / LA NOTICIA','¿De qué trata?')
t=p.paragraphs(A['summary'],t)
p.text('02 / SU IMPORTANCIA',t+3,'label');t+=25
t=p.paragraphs(A['importance'],t)
# Compact conceptual graphic and editorial highlight.
p.line(t);t+=16
p.text('ESCUCHAR  >  MODELAR  >  EXPLORAR  >  VALIDAR',t,'sub');t+=29
p.text('Ciclo conceptual propio: la simulación genera hipótesis; la evidencia humana permite contrastarlas.',t,'small')
c.showPage()

base(3,'MERCADOTECNIA BÁSICA / INGENIERÍA EN SISTEMAS')
p.styles['body'].fontSize=9.5;p.styles['body'].leading=13
p.styles['sub'].fontSize=12.5;p.styles['sub'].leading=15
t=section('03 / RELACIÓN ACADÉMICA Y PROFESIONAL','Del dato a la decisión.')
# Parallel columns keep academic concepts and the engineering role equally legible.
gap=24;col=(CW-gap)/2
left=t
for m in A['marketing']:
    left=p.text(m['title'],left,'sub',width=col)+7
    left=p.text(m['text'],left,width=col)+12
right=p.text('Mi papel como ingeniero',t,'sub',x=M+col+gap,width=col)+10
for text in A['profession']:
    right=p.text(text,right,x=M+col+gap,width=col)+12
t=max(left,right)-8
p.line(t);t+=14
p.text('04 / APLICACIÓN PRÁCTICA · EJEMPLO HIPOTÉTICO',t,'label');t+=20
p.text(A['example'],t)
c.showPage()

p.styles['body'].fontSize=10;p.styles['body'].leading=14.4
p.styles['sub'].fontSize=15;p.styles['sub'].leading=19
base(4,'REFLEXIÓN / REFERENCIAS / 19 OCTUBRE 2026')
t=section('05 / CONCLUSIÓN PERSONAL','Simular para preguntar mejor.')
t=p.text(A['reflection'],t)+28
p.text('PRINCIPALES APRENDIZAJES',t,'label');t+=23
for i,text in enumerate(A['learnings']):
    t=p.text(f'0{i+1} / {text}',t,'sub')+14
t+=8;p.line(t);t+=20
p.text('REFERENCIAS BIBLIOGRÁFICAS',t,'label');t+=23
s=A['sources'][0]
t=p.text(f"[1] {s['author']}. (2026, 14 de octubre). {s['title']}. Forbes, CMO.",t)+10
start=t;t=p.text(s['url'],t,'small')+9
c.linkURL(s['url'],(M,H-t,M+CW,H-start),relative=0)
t=p.text('Consulta: '+A['consulted']+'. '+A['sourceNote'],t,'small')+23
p.text('Autor: Anton Betak Licea / Ingeniería en Sistemas Computacionales',t,'small');t+=17
p.text('Asignatura: Mercadotecnia Básica / Fecha: 19 de octubre de 2026',t,'small')
c.save()
r=PdfReader(OUT);assert len(r.pages)==4
assert r.pages[3].get('/Annots'), 'Missing reference hyperlink'
text='\n'.join(page.extract_text() for page in r.pages)
for term in ['primarios','Segmentación','hipotético','aprendizaje','consentimiento','REFLEXIÓN','Poinski']:
    assert term.lower() in text.lower(),term
preview=ROOT/'tmp/pdfs/noticia-04';preview.mkdir(parents=True,exist_ok=True)
doc=fitz.open(OUT)
for i,page in enumerate(doc):
    for b in page.get_text('blocks'):
        assert b[0]>=M-1 and b[2]<=core.W-M+1,(i,b)
    page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(preview/f'page-{i+1}.png')
(ROOT/'public'/OUT.name).write_bytes(OUT.read_bytes())
print(f'{OUT}: 4 pages, text bounds and hyperlink verified; all pages rendered.')
