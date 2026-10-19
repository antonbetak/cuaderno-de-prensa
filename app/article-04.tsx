/* oxlint-disable next/no-img-element, next/no-html-link-for-pages -- Vite serves the original local vector illustration. */
import { ArrowDown, Download } from 'lucide-react';
import article from './article-04.json';
import type { EditionNumber } from './page';
const pdf = `${import.meta.env.BASE_URL}noticia-04-forbes-gemelos-digitales.pdf`;
export default function ArticleFour({ links, chooseEdition }: {
  links: { number: EditionNumber; href: string; label: string }[];
  chooseEdition: (event: React.MouseEvent<HTMLAnchorElement>, next: EditionNumber) => void;
}) {
  const nav = links.map(l => <a key={l.number} href={l.href} onClick={e => chooseEdition(e,l.number)} aria-current={l.number === '04' ? 'page' : undefined}>{l.label}</a>);
  return <div className="edition edition-04">
    <a href="#noticia" className="skip-link">Saltar al contenido</a>
    <header className="site-header"><a href="?noticia=1" onClick={e=>chooseEdition(e,'01')} className="brand"><span className="brand-symbol">m<span>.</span></span><span>CUADERNO<br/>DE PRENSA</span></a><nav aria-label="Navegación principal">{nav}</nav><a className="download-link" href={pdf} download><Download size={16}/><span>Descargar PDF</span></a></header>
    <nav className="mobile-edition-nav" aria-label="Cambiar noticia">{nav}</nav>
    <main id="inicio">
      <section className="twins-cover"><div className="twins-kicker"><span>NOTICIA 04 · REVISTA 02/02 · FORBES</span><span>14 OCT 2026 / CMO</span></div><div className="twins-grid"><div><p className="eyebrow">INVESTIGACIÓN / INTELIGENCIA ARTIFICIAL</p><h1>Cómo los gemelos digitales están reinventando la <em>investigación de clientes.</em></h1><p className="twins-deck">{article.subtitle}</p><p className="twins-byline">Análisis: Anton Betak Licea<br/>Ingeniería en Sistemas Computacionales · Mercadotecnia Básica<br/>19 de octubre de 2026</p><a className="hero-cta" href="#noticia">Explorar el análisis <ArrowDown size={17}/></a></div><figure><img src={`${import.meta.env.BASE_URL}assets/digital-twins.svg`} width="900" height="720" alt="Una persona y su representación en una malla digital conectadas por datos"/><figcaption>Ilustración vectorial original del cuaderno. No representa una interfaz de Outset.</figcaption></figure></div></section>
      <div className="agent-reading"><aside className="agent-index"><p className="eyebrow">EN ESTA ENTRADA</p><nav aria-label="Índice de la noticia">{[['noticia','La noticia'],['importancia','Su importancia'],['asignatura','Mercadotecnia'],['profesion','Ingeniería en sistemas'],['ejemplo','Aplicación hipotética'],['reflexion','Reflexión'],['fuentes','Referencias']].map(([id,t],i)=><a key={id} href={`#${id}`}><span>0{i+1}</span>{t}</a>)}</nav><p className="agent-index-note">Cuarta entrada de seis.<br/>Revista 02/02.<br/>Publicación posterior a agosto de 2026.</p></aside><article className="agent-story">
      <section id="noticia"><p className="eyebrow">01 / CONTEXTO</p><h2>¿De qué trata la noticia?</h2>{article.summary.map(t=><p key={t}>{t}</p>)}<a className="text-link" href={article.sources[0].url} target="_blank" rel="noreferrer">Leer la noticia original de Forbes ↗</a></section>
      <section id="importancia"><p className="eyebrow">02 / ANÁLISIS PROPIO</p><h2>Preguntar más rápido.<br/>Decidir con evidencia.</h2>{article.importance.map(t=><p key={t}>{t}</p>)}<div className="twins-flow" aria-label="Ciclo conceptual de investigación">{['Escuchar','Modelar','Explorar','Validar'].map((s,i)=><div key={s}><span>0{i+1}</span><strong>{s}</strong></div>)}</div><p className="twins-note">Esquema propio: una simulación orienta la siguiente prueba; no confirma una conducta real.</p></section>
      <section id="asignatura"><p className="eyebrow">03 / MERCADOTECNIA BÁSICA</p><h2>Del dato a la decisión.</h2>{article.marketing.map((m,i)=><div key={m.title} className="agent-market"><span>0{i+1}</span><div><h3>{m.title}</h3><p>{m.text}</p></div></div>)}</section>
      <section id="profesion"><p className="eyebrow">04 / INGENIERÍA EN SISTEMAS COMPUTACIONALES</p><h2>Construir también<br/>implica evaluar.</h2>{article.profession.map(t=><p key={t}>{t}</p>)}</section>
      <section id="ejemplo"><p className="eyebrow">05 / PROPUESTA ILUSTRATIVA</p><h2>Una tienda, dos promociones.</h2><p>{article.example}</p></section>
      <section id="reflexion"><p className="eyebrow">06 / REFLEXIÓN PERSONAL</p><h2>Simular para<br/>preguntar mejor.</h2><p>{article.reflection}</p><ul>{article.learnings.map(t=><li key={t}>{t}</li>)}</ul></section>
      </article></div>
      <section id="fuentes" className="agent-sources"><p className="eyebrow">REFERENCIAS / FUENTE ORIGINAL</p><h2>La evidencia, a la vista.</h2>{article.sources.map(s=><a id={`fuente-${s.id}`} key={s.id} href={s.url} target="_blank" rel="noreferrer">[{s.id}] {s.author}. ({s.date}). <strong>{s.title}.</strong> {s.publisher}.<br/><small>{s.url}</small></a>)}<p>Consulta: {article.consulted}. {article.sourceNote}</p></section>
      <section className="pdf-strip"><div><span className="eyebrow">REVISTA 02/02 · CUATRO PÁGINAS</span><h2>El análisis completo, en PDF.</h2></div><a className="pdf-button" href={pdf} download>Descargar noticia 04 <Download size={18}/></a></section>
    </main>
  </div>;
}
