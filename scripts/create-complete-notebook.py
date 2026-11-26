#!/usr/bin/env python3
"""Create the vector cover and assemble the original six PDFs without altering them."""
from pathlib import Path
from shutil import copyfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output/pdf'
COVER = OUT / 'portada-cuaderno-de-prensa.pdf'
NAME = 'Cuaderno-de-Prensa-Anton-Betak-Licea-Otono-2026.pdf'
SOURCES = ['01_Anton Betak.pdf', '02_Anton Betak.pdf', 'noticia-03-wired-agentes-ia.pdf', 'noticia-04-forbes-gemelos-digitales.pdf', 'noticia-05-economista-consumidor-ia.pdf', 'noticia-06-mercado-ads.pdf']
W, H = map(float, (PdfReader(OUT / SOURCES[0]).pages[0].mediabox.width, PdfReader(OUT / SOURCES[0]).pages[0].mediabox.height))
c = canvas.Canvas(str(COVER), pagesize=(W,H))
c.setTitle('Portada — Cuaderno de prensa'); c.setAuthor('Anton Betak Licea')
def color(v): c.setFillColor(HexColor(v))
def text(x,y,s,font='Helvetica',size=10,fill='#f6f5ed'):
    color(fill); c.setFont(font,size); c.drawString(x,y,s)
def line(x1,y1,x2,y2,stroke='#737d73',width=.6):
    c.setStrokeColor(HexColor(stroke)); c.setLineWidth(width); c.line(x1,y1,x2,y2)
color('#15191a'); c.rect(0,0,W,H,fill=1,stroke=0)
text(42,H-52,'m.', 'Helvetica-Bold',27,'#cefc72')
text(93,H-39,'INGENIERÍA EN SISTEMAS', 'Helvetica-Bold',7)
text(93,H-51,'× MERCADOTECNIA', 'Helvetica-Bold',7)
text(432,H-39,'EDICIÓN ACADÉMICA', 'Helvetica-Bold',7)
text(432,H-51,'OTOÑO 2026', 'Helvetica-Bold',7)
line(42,H-67,W-42,H-67)
text(42,H-91,'UNA MIRADA AL PRESENTE', 'Courier',8,'#b9c4ba')
text(414,H-91,'01 — 06 / COMPLETO', 'Courier',8,'#b9c4ba')
text(42,H-142,'TECNOLOGÍA · MERCADO · PERSONAS','Courier-Bold',8,'#cefc72')
text(38,H-217,'Cuaderno','Helvetica-Bold',69)
text(38,H-284,'de prensa.','Times-Italic',70,'#cefc72')
text(42,H-317,'Ideas que conectan la innovación tecnológica con',size=11,fill='#c1c9c1')
text(42,H-333,'las decisiones, las marcas y las personas.',size=11,fill='#c1c9c1')
# Vector diagram: concentric networks and crossing market signals.
cx,cy=352,307
for radius in (135,99,62):
    c.setStrokeColor(HexColor('#737d73')); c.setLineWidth(.6); c.circle(cx,cy,radius,stroke=1,fill=0)
for dx,dy in ((155,0),(0,155),(110,110),(110,-110)): line(cx-dx,cy-dy,cx+dx,cy+dy)
c.setStrokeColor(HexColor('#cefc72')); c.setLineWidth(2.2)
p=c.beginPath(); p.moveTo(cx-135,cy); p.curveTo(cx-90,cy+90,cx-40,cy+110,cx,cy+99); p.curveTo(cx+40,cy+80,cx+85,cy-60,cx+135,cy); c.drawPath(p)
c.setStrokeColor(HexColor('#f48972')); p=c.beginPath(); p.moveTo(cx-110,cy-88); p.curveTo(cx-50,cy-75,cx-45,cy+40,cx,cy+38); p.curveTo(cx+50,cy+36,cx+75,cy+100,cx+110,cy+85); c.drawPath(p)
color('#cefc72'); c.circle(cx,cy,20,stroke=0,fill=1); color('#15191a'); c.circle(cx,cy,6,stroke=0,fill=1)
for x,y,col in ((cx-99,cy,'#f48972'),(cx+70,cy+70,'#cefc72'),(cx+110,cy+85,'#f48972'),(cx-50,cy-50,'#cefc72')):
    color(col); c.circle(x,y,4,stroke=0,fill=1)
text(42,389,'FIG. 01 / CONEXIONES','Courier',8,'#aeb8af')
text(42,371,'SISTEMAS EN', 'Helvetica-Bold',11)
text(42,356,'MOVIMIENTO', 'Helvetica-Bold',11)
text(42,329,'ANÁLISIS / REFLEXIÓN','Courier',8,'#aeb8af')
text(42,315,'6 NOTICIAS','Courier',8,'#aeb8af')
line(42,137,W-42,137)
text(42,120,'AUTOR','Courier',7,'#aeb8af'); text(42,103,'Anton Betak Licea','Helvetica-Bold',10)
text(280,120,'CARRERA','Courier',7,'#aeb8af'); text(280,103,'Ingeniería en Sistemas Computacionales','Helvetica-Bold',9)
text(42,76,'MATERIA','Courier',7,'#aeb8af'); text(42,59,'Mercadotecnia','Helvetica-Bold',10)
text(280,76,'PERIODO','Courier',7,'#aeb8af'); text(280,59,'Otoño 2026','Helvetica-Bold',10)
c.showPage(); c.save()
writer=PdfWriter(); count=0
for title,path in [('Portada',COVER)]+[(f'Noticia {i:02d}', OUT/name) for i,name in enumerate(SOURCES,1)]:
    reader=PdfReader(path); writer.append(reader, import_outline=False); writer.add_outline_item(title,count); count += len(reader.pages)
writer.add_metadata({'/Title':'Cuaderno de prensa — Mercadotecnia','/Author':'Anton Betak Licea','/Subject':'Ingeniería en Sistemas Computacionales — Otoño 2026'})
with (OUT/NAME).open('wb') as f: writer.write(f)
copyfile(OUT/NAME,ROOT/'public'/NAME)
print('Páginas por documento:', [len(PdfReader(p).pages) for p in [COVER]+[OUT/n for n in SOURCES]])
print('Total:',count)
