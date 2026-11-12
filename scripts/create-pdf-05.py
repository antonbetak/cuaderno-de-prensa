"""Noticia 05: cuatro paginas editoriales."""
from pathlib import Path
import importlib.util, json
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('editorial',ROOT/'scripts/pdf-editorial.py'); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
A=json.loads((ROOT/'app/article-05.json').read_text()); OUT=ROOT/'output/pdf/noticia-05-economista-consumidor-ia.pdf'; OUT.parent.mkdir(parents=True,exist_ok=True)
p=core.EditorialPDF(OUT,A['title'],5); c=p.canvas; c.setAuthor('Anton Betak Licea'); c.setSubject('Mercadotecnia Básica / Periódico 01/02 / El Economista')
for name in p.styles: p.styles[name].textColor=HexColor('#E86332' if name=='label' else '#102B46' if name in ['hero','title','sub'] else '#43515A')
p.styles['body'].fontSize=10; p.styles['body'].leading=14.4; p.styles['small'].fontSize=8.5; p.styles['small'].leading=12; M,CW,H=core.M,core.CW,core.H
def base(tag):
    c.setFillColor(HexColor('#FBF7EF')); c.rect(0,0,core.W,H,fill=1,stroke=0); p.text('N/05 · CUADERNO DE PRENSA',31,'label'); p.text('EL ECONOMISTA / PERIÓDICO 01/02',31,'label',x=365,width=188); p.line(55); p.line(792); p.text(tag,803,'small',width=440,limit=828)
def section(label,title): p.text(label,79,'label'); return p.text(title,103,'title')+20
base('ANTON BETAK LICEA / MERCADOTECNIA BÁSICA'); p.text('05 / CONSUMO / INTELIGENCIA ARTIFICIAL',81,'label'); t=p.text(A['title'],112,'hero')+20; t=p.text(A['subtitle'],t)+20; p.text('EL ECONOMISTA · Judith Santiago · 5 octubre 2026',t,'small'); t+=21; p.text('Anton Betak Licea / Ingeniería en Sistemas Computacionales',t,'small'); t+=35; c.setFillColor(HexColor('#102B46')); c.roundRect(M,H-t-260,CW,260,14,fill=1,stroke=0); c.setFillColor(HexColor('#F47B42')); c.circle(M+CW-100,H-t-90,70,fill=1,stroke=0); p.text('RECOMIENDA · EXPLICA · DEJA DECIDIR',t+285,'sub'); c.showPage()
base('ANÁLISIS / CONFIANZA, DATOS Y CONTROL'); t=section('01 / LA NOTICIA','¿De qué trata?'); t=p.paragraphs(A['summary'],t); p.text('DATOS DE LA FUENTE PRINCIPAL',t+8,'label'); t+=28; p.text('68%  recomendaciones     38%  no delega     90%+  usa smartphone',t,'sub'); t+=30; p.text('Son indicadores distintos, no partes complementarias de un mismo total.',t,'small'); p.text('02 / SU IMPORTANCIA',t+35,'label'); t+=58; t=p.paragraphs(A['importance'],t); c.showPage()
base('MERCADOTECNIA BÁSICA / INGENIERÍA EN SISTEMAS'); p.styles['body'].fontSize=9.3; p.styles['body'].leading=12.8; t=section('03 / RELACIÓN ACADÉMICA','Del comportamiento a la experiencia.'); gap=24; col=(CW-gap)/2; left=t
for m in A['marketing']: left=p.text(m['title'],left,'sub',width=col)+6; left=p.text(m['text'],left,width=col)+10
right=p.text('Mi papel como ingeniero',t,'sub',x=M+col+gap,width=col)+10
for tx in A['profession']: right=p.text(tx,right,x=M+col+gap,width=col)+10
t=max(left,right)+8; p.text('05 / EJEMPLO HIPOTÉTICO',t,'label'); t+=20; p.text(A['example'],t,width=CW); c.showPage()
base('REFLEXIÓN / REFERENCIAS / 12 NOVIEMBRE 2026'); t=section('06 / REFLEXIÓN PERSONAL','Diseñar con criterio humano.'); t=p.text(A['reflection'],t)+24; p.line(t); t+=18; p.text('REFERENCIAS BIBLIOGRÁFICAS · APA 7',t,'label'); t+=24
for s in A['sources']:
    start=t; t=p.text(f"[{s['id']}] {s['author']} ({s['date']}). {s['title']}. {s['publisher']}.",t,'small')+3; t=p.text(s['url'],t,'small')+10; c.linkURL(s['url'],(M,H-t,M+CW,H-start),relative=0)
p.text(A['sourceNote'],t+5,'small'); c.save(); r=PdfReader(OUT); assert len(r.pages)==4
text='\n'.join(page.extract_text() for page in r.pages); assert all(term.lower() in text.lower() for term in ['68%','38%','smartphone','hipotético','REFERENCIAS'])
preview=ROOT/'tmp/pdfs/noticia-05'; preview.mkdir(parents=True,exist_ok=True); doc=fitz.open(OUT)
for i,page in enumerate(doc): page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(preview/f'page-{i+1}.png')
(ROOT/'public'/OUT.name).write_bytes(OUT.read_bytes()); print(f'{OUT}: 4 pages rendered and copied to public/.')
