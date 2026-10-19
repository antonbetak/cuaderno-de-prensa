/* oxlint-disable next/no-img-element -- This project uses Vite; the local SVG has explicit dimensions and alt text. */
import { ArrowDown, ArrowUp, ArrowUpRight, Download } from 'lucide-react';
import article from './article-03.json';

import type { EditionNumber } from './page';
const pdf = `${import.meta.env.BASE_URL}noticia-03-wired-agentes-ia.pdf`;
function Text({ text }: { text: string }) {
  return <>{text.split(/(\[1\])/).map((part, i) => part === '[1]' ? <a key={i} className="agent-citation" href="#fuente-1" aria-label="Ver referencia WIRED">[1]</a> : part)}</>;
}
export default function ArticleThree({ links, chooseEdition }: {
  links: { number: EditionNumber; href: string; label: string }[];
  chooseEdition: (event: React.MouseEvent<HTMLAnchorElement>, next: EditionNumber) => void;
}) {
  const nav = links.map(link => <a key={link.number} href={link.href} onClick={e => chooseEdition(e, link.number)} aria-current={link.number === '03' ? 'page' : undefined}>{link.label}</a>);
  return <div className="edition edition-03">
    <a href="#noticia" className="skip-link">Saltar al contenido</a>
    <header className="site-header">
      <a href="#inicio" className="brand"><span className="brand-symbol">m<span>.</span></span><span>CUADERNO<br />DE PRENSA</span></a>
      <nav aria-label="Navegación principal">{nav}<a href="#fuentes">Fuentes <ArrowUpRight size={14} /></a></nav>
      <a href={pdf} download className="download-link"><Download size={16} /><span>Descargar PDF</span></a>
    </header>
    <nav className="mobile-edition-nav" aria-label="Cambiar noticia">{nav}</nav>
    <main id="inicio">
      <section className="agent-cover" aria-labelledby="agent-title">
        <div className="agent-kicker"><span>NOTICIA 03 / REVISTA DIGITAL · WIRED</span><span>30 SEP 2026 · BUSINESS</span></div>
        <div className="agent-cover-grid">
          <div><p className="agent-label">AI AGENT WARS</p><h1 id="agent-title">La batalla por<br />convertirse en tu<br /><em>agente personal.</em></h1><p className="agent-deck">{article.subtitle}</p><p className="agent-byline">Artículo original: Reece Rogers<br />Análisis: Anton Betak · Mercadotecnia</p><a href="#noticia" className="agent-read">Leer el análisis <ArrowDown size={17} /></a></div>
          <figure className="agent-art"><img src={`${import.meta.env.BASE_URL}assets/agent-wars.svg`} width="600" height="520" alt="Composición propia de dos figuras abstractas enfrentadas entre símbolos de correo, tareas y documentos" /><figcaption>OPENAI DOTS <span>VS</span> META MUSE<br /><small>Ilustración conceptual propia; no representa interfaces de producto.</small></figcaption></figure>
        </div>
        <div className="agent-cover-bottom"><span>SISTEMAS × MERCADOTECNIA</span><span>03 / 06</span></div>
      </section>
      <div className="agent-reading">
        <aside className="agent-index"><p className="agent-label">EN ESTA ENTRADA</p><nav aria-label="Índice de la noticia">{[['noticia','La competencia'],['importancia','De preguntar a delegar'],['asignatura','El mercado'],['profesion','Detrás del mensaje'],['reflexion','Mi reflexión'],['fuentes','Referencias']].map(([id,title],i)=><a key={id} href={`#${id}`}><span>0{i+1}</span>{title}</a>)}</nav><p className="agent-index-note">Tercera entrada de seis.<br />Fuente: revista digital.<br />Publicada después de agosto de 2026.</p></aside>
        <article className="agent-story">
          <section id="noticia"><p className="agent-label">01 / EL CONTEXTO · INFORMACIÓN DE WIRED</p><h2>Dos agentes.<br />Una misma competencia.</h2>{article.summary.map(p=><p key={p}><Text text={p}/></p>)}
            <div className="agent-comparison">{article.strategies.map(s=><div key={s.name}><h3>{s.name}</h3><strong>{s.price}</strong><p className="agent-detail">{s.detail} [1]</p><p>{s.analysis}</p></div>)}</div>
          </section>
          <section id="importancia"><p className="agent-label">02 / LO QUE CAMBIA · ANÁLISIS PERSONAL</p><h2>De preguntar<br />a delegar.</h2><div className="agent-paradigm"><div><span>CHATBOT</span><p>Pregunta → Respuesta</p></div><div><span>AGENTE</span><p>Contexto → Plan → Acción → Seguimiento</p></div><small>Esquema conceptual propio: las acciones dependen de permisos y límites.</small></div>{article.importance.map(p=><p key={p}><Text text={p}/></p>)}</section>
          <section id="asignatura"><p className="agent-label">03 / MERCADOTECNIA · ANÁLISIS PERSONAL</p><h2>El producto también<br />es la confianza.</h2>{article.marketing.map((m,i)=><div className="agent-market" key={m.title}><span>0{i+1}</span><div><h3>{m.title}</h3><p><Text text={m.text}/></p></div></div>)}</section>
          <section id="profesion"><p className="agent-label">04 / INGENIERÍA EN SISTEMAS COMPUTACIONALES</p><h2>Detrás de<br />un mensaje sencillo.</h2>{article.profession.map(p=><p key={p}>{p}</p>)}<div className="agent-stack"><p className="agent-label">EJEMPLO HIPOTÉTICO · ARQUITECTURA CONCEPTUAL</p><h3>Lo que ve el usuario</h3><p className="agent-request">“Reserva una cena para mañana”</p><h3>Lo que ocurre detrás</h3><ol>{article.flow.map(f=><li key={f}>{f}</li>)}</ol><p>Antes de confirmar una reserva: verificar disponibilidad, datos y autorización. Este esquema no afirma que los productos probados ejecuten esta tarea.</p></div></section>
          <section id="reflexion"><p className="agent-label">05 / REFLEXIÓN PERSONAL</p><h2>Probar es fácil.<br />Confiar lleva tiempo.</h2><p>{article.reflection}</p></section>
        </article>
      </div>
      <section id="fuentes" className="agent-sources"><p className="agent-label">LECTURAS Y REFERENCIAS</p><h2>La fuente, a la vista.</h2>{article.sources.map(s=><a id={`fuente-${s.id}`} key={s.id} href={s.url} target="_blank" rel="noreferrer"><span>[{s.id}] Rogers, R. (2026, September 30).<br /><strong>{s.title}.</strong> WIRED. <ArrowUpRight size={17}/><br /><small>{s.url}</small></span></a>)}<p>Consulta: {article.consulted}. {article.sourceNote}</p></section>
      <section className="pdf-strip"><div><span className="eyebrow">REVISTA DIGITAL / NOTICIA 03</span><h2>Una entrada lista para entregar.</h2></div><a className="pdf-button" href={pdf} download>Descargar noticia 03 <Download size={18}/></a></section>
    </main><footer><a href="#inicio" className="footer-brand">m.</a><p>Ingeniería en Sistemas Computacionales<br /><span>Actividad individual / Noticia 03 de 06</span></p><a href="#inicio" className="back-top">Volver arriba <ArrowUp size={16}/></a></footer>
  </div>;
}
