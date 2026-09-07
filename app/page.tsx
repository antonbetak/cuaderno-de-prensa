import { useEffect, useState } from 'react';
import { ArrowUpRight, ArrowDown, Download, ArrowUp, Sparkles, ScanLine, Target, Fingerprint, ChartNoAxesCombined, Plus, Minus } from 'lucide-react';
import article from './article.json';

const sections = [{id:'noticia',name:'La noticia'},{id:'importancia',name:'Su importancia'},{id:'asignatura',name:'En la asignatura'},{id:'profesion',name:'Mi profesión'}];
const icons = [ScanLine,Target,Fingerprint,ChartNoAxesCombined];
function CitedText({text}:{text:string}) {
  return <>{text.split(/(\[\d\])/).map((part,i)=> /\[\d\]/.test(part) ? <a key={i} className="citation" href={`#fuente-${part[1]}`} aria-label={`Ver fuente ${part[1]}`}>{part}</a> : part)}</>;
}
export default function Home() {
  const [active,setActive] = useState('noticia');
  const [progress,setProgress] = useState(0);
  const [open,setOpen] = useState<string[]>(['01']);
  useEffect(()=>{
    const onScroll=()=>{
      const max=document.documentElement.scrollHeight-window.innerHeight;
      setProgress(max>0 ? window.scrollY/max*100 : 0);
      const current=sections.filter(s=>(document.getElementById(s.id)?.getBoundingClientRect().top ?? 10000)<180).at(-1);
      setActive(current?.id ?? 'noticia');
    };
    window.addEventListener('scroll',onScroll,{passive:true});onScroll();
    return ()=>window.removeEventListener('scroll',onScroll);
  },[]);
  return <>
    <a href="#noticia" className="skip-link">Saltar al contenido</a>
    <div className="reading-progress" style={{width:`${progress}%`}} aria-hidden="true"/>
    <header className="site-header">
      <a href="#inicio" className="brand" aria-label="Cuaderno de prensa, inicio"><span className="brand-symbol">m<span>.</span></span><span>CUADERNO<br/>DE PRENSA</span></a>
      <nav aria-label="Navegación principal"><a href="#noticia">Noticia 01 <span className="nav-dot"/></a><a href="#fuentes">Fuentes <ArrowUpRight size={14}/></a></nav>
      <a href={`${import.meta.env.BASE_URL}noticia-01-astra.pdf`} download className="download-link"><Download size={16}/><span>Descargar PDF</span></a>
    </header>
    <main id="inicio">
      <section className="hero" aria-labelledby="hero-title">
        <div className="hero-topline"><span><span className="small-star">✳</span> SISTEMAS × MERCADOTECNIA</span><span>VOL. 01 <i/> SEPTIEMBRE 2026</span></div>
        <div className="hero-grid">
          <div className="hero-copy"><div className="eyebrow"><span className="lime-dot"/> NOTICIA 01 / INTERNET</div><h1 id="hero-title">Sistemas que<br/>conectan con<br/><span>el mercado.</span></h1><p>{article.subtitle}</p><a className="hero-cta" href="#noticia">Explorar la noticia <ArrowDown size={18}/></a></div>
          <figure className="hero-visual"><img src={`${import.meta.env.BASE_URL}assets/astra.png`} alt="Ilustración editorial de GPT-6 Astra: esfera luminosa azul y violeta con el emblema de OpenAI" width="1672" height="941"/><div className="image-index"><span>EN EL RADAR</span><b>GPT-6<br/>Astra<span>↗</span></b></div><figcaption>Ilustración: Future / ChatGPT, vía Tom’s Guide</figcaption></figure>
        </div>
        <div className="hero-bottom"><span>INTELIGENCIA ARTIFICIAL</span><span>INGENIERÍA EN SISTEMAS</span><span>REFLEXIÓN PROFESIONAL</span><span className="edition-number">01 — 06</span></div>
      </section>
      <div className="article-shell">
        <aside className="article-nav"><div className="sticky-index"><p className="eyebrow">EN ESTA ENTRADA</p><nav aria-label="Índice de la noticia">{sections.map((s,i)=><a href={`#${s.id}`} key={s.id} className={active===s.id?'active':''} aria-current={active===s.id?'location':undefined}><span>0{i+1}</span>{s.name}<ArrowUpRight size={15}/></a>)}</nav><div className="edition-card"><span className="edition-big">01<span>/06</span></span><p>Primera entrada<br/>Cuaderno de prensa</p><div className="edition-track" aria-hidden="true"><i/><i/><i/><i/><i/><i/></div><span className="tiny">FUENTE DE INTERNET</span></div></div></aside>
        <div className="article-content">
          <section id="noticia" className="article-section"><div className="section-label"><span>01</span> EL CONTEXTO</div><h2>¿De qué trata<br/>la noticia?</h2><div className="news-meta"><span>OPENAI</span><span>03 SEP 2026 · LANZAMIENTO</span></div><h3 className="news-headline">GPT-6 Astra: de responder preguntas a ejecutar tareas.</h3>{article.summary.map((p,i)=><p key={i}><CitedText text={p}/></p>)}<a href={article.sources[0].url} target="_blank" rel="noreferrer" className="text-link">Leer la noticia original <ArrowUpRight size={17}/></a><div className="key-note"><Sparkles size={22}/><p><strong>La conexión con mercadotecnia</strong>El análisis de esta entrada explora aplicaciones posibles; no atribuye al lanzamiento resultados de ventas o campañas.</p></div></section>
          <section id="importancia" className="article-section"><div className="section-label"><span>02</span> LO QUE ESTÁ EN JUEGO</div><h2>¿Qué importancia<br/>tiene?</h2><p>{article.importance}</p><div className="balance-grid"><div className="balance opportunity"><span className="eyebrow">LA OPORTUNIDAD <ArrowUpRight size={18}/></span><h3>Más espacio<br/>para la estrategia.</h3><p>{article.opportunity}</p></div><div className="balance responsibility"><span className="eyebrow">LA RESPONSABILIDAD <ScanLine size={18}/></span><h3>Más criterio<br/>en cada decisión.</h3><p>{article.risk}</p></div></div></section>
          <section id="asignatura" className="article-section"><div className="section-label"><span>03</span> DE LA NOTICIA A LA CLASE</div><h2>¿Cómo y con qué temas<br/>de la asignatura se relaciona?</h2><p>El lanzamiento permite conectar la innovación tecnológica con cuatro temas de mercadotecnia.</p><div className="topic-list">{article.topics.map((topic,i)=>{const Icon=icons[i];const expanded=open.includes(topic.number);return <div className={`topic ${expanded?'expanded':''}`} key={topic.number}><h3><button aria-expanded={expanded} aria-controls={`topic-${topic.number}`} onClick={()=>setOpen(prev=>expanded?prev.filter(x=>x!==topic.number):[...prev,topic.number])}><Icon size={22}/><span>{topic.title}</span>{expanded?<Minus size={19}/>:<Plus size={19}/>}</button></h3><div id={`topic-${topic.number}`} className="topic-text" hidden={!expanded}><p>{topic.text}</p></div></div>})}</div><div className="case-study"><span className="eyebrow">LLEVÉMOSLO A UN EJEMPLO</span><h3>{article.example.title}</h3><p className="case-intro">{article.example.intro}</p><div className="case-steps">{article.example.steps.map((step,i)=><div key={step.title}><span className="step-number">0{i+1}</span><h4>{step.title}</h4><p>{step.text}</p></div>)}</div><p className="case-decision">{article.example.decision}</p></div></section>
          <section id="profesion" className="article-section profession"><div className="section-label"><span>04</span> MI MIRADA PROFESIONAL</div><h2>¿Cómo se relaciona<br/>con mi profesión?</h2>{article.profession.map(p=><p key={p}>{p}</p>)}<blockquote><span aria-hidden="true">“</span>{article.conclusion}</blockquote><div className="closing-line"><span className="lime-dot"/> INGENIERÍA CON PROPÓSITO. TECNOLOGÍA CON VALOR.</div></section>
        </div>
      </div>
      <section id="fuentes" className="sources-section"><div className="sources-heading"><div className="section-label">LECTURAS Y REFERENCIAS</div><h2>Detrás del análisis.</h2><p>Una noticia de Internet y su fuente primaria.<br/>Consultadas el 6 de septiembre de 2026.</p></div><div className="sources-list">{article.sources.map(s=><a id={`fuente-${s.id}`} href={s.url} key={s.id} target="_blank" rel="noreferrer"><div><span className="eyebrow">[{s.id}] {s.type}</span><h3>{s.title}</h3><p>{s.author} · {s.publisher} · {s.date}</p></div><ArrowUpRight size={23}/></a>)}</div></section>
      <section className="pdf-strip"><div><span className="eyebrow">DEL PORTAFOLIO A LA ENTREGA</span><h2>El análisis completo, en PDF.</h2></div><a className="pdf-button" href={`${import.meta.env.BASE_URL}noticia-01-astra.pdf`} download>Descargar noticia 01 <Download size={18}/></a></section>
    </main>
    <footer><a href="#inicio" className="footer-brand">m.</a><p>Ingeniería en Sistemas Computacionales<br/><span>Actividad individual / Noticia 01 de 06</span></p><a href="#inicio" className="back-top">Volver arriba <ArrowUp size={16}/></a></footer>
  </>;
}
