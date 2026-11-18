"""Noticia 06: PDF editorial de Mercado Ads."""
from pathlib import Path
import importlib.util, json
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
import pymupdf as fitz
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('editorial',ROOT/'scripts/pdf-editorial.py'); core=importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
A=json.loads((ROOT/'app/article-06.json').read_text()); OUT=ROOT/'output/pdf/noticia-06-mercado-ads.pdf'; OUT.parent.mkdir(parents=True,exist_ok=True)
p=core.EditorialPDF(OUT,A['title'],6); c=p.canvas; c.setAuthor('Anton Betak Licea'); c.setSubject('Mercadotecnia Básica / Periódico 02/02 / El Economista')
for name in p.styles: p.styles[name].textColor=HexColor('#D49D00' if name=='label' else '#102B46' if name in ['hero','title','sub'] else '#43515A')
p.styles['body'].fontSize=9.8; p.styles['body'].leading=14; p.styles['small'].fontSize=8.5; p.styles['small'].leading=12; M,CW,H=core.M,core.CW,core.H
def base(tag):
    c.setFillColor(HexColor('#FBF8F0')); c.rect(0,0,core.W,H,fill=1,stroke=0); p.text('N/06 · CUADERNO DE PRENSA',31,'label'); p.text('EL ECONOMISTA / PERIÓDICO 02/02',31,'label',x=365,width=188); p.line(55); p.line(792); p.text(tag,803,'small',width=440,limit=828)
def section(label,title): p.text(label,79,'label'); return p.text(title,103,'title')+20
base('ANTON BETAK LICEA / MERCADOTECNIA BÁSICA'); p.text('06 / RETAIL MEDIA / DATOS',81,'label'); t=p.text(A['title'],112,'hero')+20; t=p.text(A['subtitle'],t)+20; p.text('EL ECONOMISTA · Patricia Ortega · 2 octubre 2026',t,'small'); t+=21; p.text('Anton Betak Licea / Ingeniería en Sistemas Computacionales · Grupo C',t,'small'); t+=35; c.setFillColor(HexColor('#102B46')); c.roundRect(M,H-t-240,CW,240,14,fill=1,stroke=0); c.setFillColor(HexColor('#FFCB05')); c.circle(M+CW-100,H-t-90,70,fill=1,stroke=0); p.text('PUBLICIDAD → DATOS → VENTA',t+270,'sub'); c.showPage()
base('ANÁLISIS / MEDIR EL RECORRIDO'); t=section('01 / LA NOTICIA','¿De qué trata?'); t=p.paragraphs(A['summary'],t); p.text('LECTURA DEL MODELO',t+8,'label'); t+=28; p.text('BÚSQUEDA   ·   NAVEGACIÓN   ·   COMPRA',t,'sub'); t+=30; p.text('El diagrama es una interpretación didáctica, no una representación de la arquitectura interna de Mercado Ads.',t,'small'); p.text('02 / SU IMPORTANCIA',t+35,'label'); t+=58; t=p.paragraphs(A['importance'],t); c.showPage()
base('MERCADOTECNIA BÁSICA / RELACIÓN CON LA CLASE'); p.styles['body'].fontSize=8.9; p.styles['body'].leading=12.3; t=section('03 / RELACIÓN ACADÉMICA','Medir para comprender.'); gap=22; col=(CW-gap)/2; left=t
for m in A['topics'][:3]: left=p.text(m['title'],left,'sub',width=col)+5; left=p.text(m['text'],left,width=col)+9
right=p.text(A['topics'][3]['title'],t,'sub',x=M+col+gap,width=col)+5; right=p.text(A['topics'][3]['text'],right,x=M+col+gap,width=col)+12; right=p.text(A['topics'][4]['title'],right,'sub',x=M+col+gap,width=col)+5; right=p.text(A['topics'][4]['text'],right,x=M+col+gap,width=col)+12
t=max(left,right)+10; p.text('04 / MI PROFESIÓN',t,'label'); t+=20; t=p.paragraphs(A['profession'][:2],t); c.showPage()
base('INGENIERÍA EN SISTEMAS / REFERENCIAS'); t=section('04 / MI MIRADA PROFESIONAL','Sistemas que vuelven visible el resultado.'); t=p.paragraphs(A['profession'][2:],t)+20; p.text('CAPAS DE UNA SOLUCIÓN RESPONSABLE',t,'label'); t+=22; p.text('SOFTWARE   ·   BASES DE DATOS   ·   IA   ·   APIs   ·   DASHBOARDS   ·   SEGURIDAD',t,'sub'); t+=34; p.line(t); t+=20; p.text('REFERENCIA BIBLIOGRÁFICA · APA 7',t,'label'); t+=24
for s in A['sources']:
    start=t; t=p.text(f"[{s['id']}] {s['author']} ({s['date']}). {s['title']}. {s['publisher']}.",t,'small')+3; t=p.text(s['url'],t,'small')+10; c.linkURL(s['url'],(M,H-t,M+CW,H-start),relative=0)
p.text(A['sourceNote'],t+5,'small'); c.save(); r=PdfReader(OUT); assert len(r.pages)==4
text='\n'.join(page.extract_text() or '' for page in r.pages); assert all(term.lower() in text.lower() for term in ['Mercado Ads','importancia','mercadotecnia','profesión','referencia'])
preview=ROOT/'tmp/pdfs/noticia-06'; preview.mkdir(parents=True,exist_ok=True); doc=fitz.open(OUT)
for i,page in enumerate(doc): page.get_pixmap(matrix=fitz.Matrix(1.5,1.5),alpha=False).save(preview/f'page-{i+1}.png')
(ROOT/'public'/OUT.name).write_bytes(OUT.read_bytes()); print(f'{OUT}: 4 pages rendered and copied to public/.')
