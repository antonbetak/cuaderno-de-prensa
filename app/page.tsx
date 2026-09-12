import { useEffect, useMemo, useState } from 'react';
import {
  ArrowDown,
  ArrowUp,
  ArrowUpRight,
  ChartNoAxesCombined,
  Database,
  Download,
  Fingerprint,
  MessageCircle,
  Minus,
  Plus,
  ScanLine,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Target,
} from 'lucide-react';
import articleOne from './article.json';
import articleTwo from './article-02.json';

const sections = [
  { id: 'noticia', name: 'La noticia' },
  { id: 'importancia', name: 'Su importancia' },
  { id: 'asignatura', name: 'En la asignatura' },
  { id: 'profesion', name: 'Mi profesión' },
];

const editions = {
  '01': {
    number: '01',
    data: articleOne,
    month: 'SEPTIEMBRE 2026',
    publisher: 'OPENAI',
    newsMeta: '03 SEP 2026 · LANZAMIENTO',
    headline: 'GPT-6 Astra: de responder preguntas a ejecutar tareas.',
    heroTitle: (
      <>
        Sistemas que<br />
        conectan con<br />
        <span>el mercado.</span>
      </>
    ),
    bottomTags: ['INTELIGENCIA ARTIFICIAL', 'INGENIERÍA EN SISTEMAS', 'REFLEXIÓN PROFESIONAL'],
    pdf: '01_Anton%20Betak.pdf?v=20260912',
    visual: 'image' as const,
    sourceDate: '6 de septiembre de 2026',
    keyNoteTitle: 'La conexión con mercadotecnia',
    keyNoteText: 'El análisis de esta entrada explora aplicaciones posibles; no atribuye al lanzamiento resultados de ventas o campañas.',
    sectionLead: 'El lanzamiento permite conectar la innovación tecnológica con cuatro temas de mercadotecnia.',
    importance: [articleOne.importance],
    topicIcons: [ScanLine, Target, Fingerprint, ChartNoAxesCombined],
    closingLine: 'INGENIERÍA CON PROPÓSITO. TECNOLOGÍA CON VALOR.',
  },
  '02': {
    number: '02',
    data: articleTwo,
    month: 'SEPTIEMBRE 2026',
    publisher: 'SHOPIFY',
    newsMeta: '10 SEP 2026 · ACTUALIZACIÓN',
    headline: 'Shopify lleva el consentimiento de WhatsApp al checkout.',
    heroTitle: (
      <>
        El permiso<br />
        también<br />
        <span>convierte.</span>
      </>
    ),
    bottomTags: ['MERCADOTECNIA DIGITAL', 'DATOS DEL CLIENTE', 'PRIVACIDAD Y CONFIANZA'],
    pdf: '02_Anton%20Betak.pdf?v=20260912',
    visual: 'product' as const,
    sourceDate: '12 de septiembre de 2026',
    keyNoteTitle: 'El dato necesita contexto',
    keyNoteText: 'Registrar un número telefónico no equivale a tener permiso ilimitado. La tienda debe conservar la preferencia y respetar la decisión del cliente.',
    sectionLead: 'La actualización conecta una decisión dentro del checkout con cuatro temas centrales de mercadotecnia.',
    importance: articleTwo.importance,
    topicIcons: [MessageCircle, Database, ShoppingBag, ShieldCheck],
    closingLine: 'UN PERMISO CLARO. UN SISTEMA CONFIABLE. UNA MEJOR RELACIÓN.',
  },
};

type EditionNumber = keyof typeof editions;

function getEditionFromUrl(): EditionNumber {
  if (typeof window === 'undefined') return '01';
  return new URLSearchParams(window.location.search).get('noticia') === '2' ? '02' : '01';
}

function CitedText({ text }: { text: string }) {
  return (
    <>
      {text.split(/(\[\d\])/).map((part, index) =>
        /\[\d\]/.test(part) ? (
          <a key={`${part}-${index}`} className="citation" href={`#fuente-${part[1]}`} aria-label={`Ver fuente ${part[1]}`}>
            {part}
          </a>
        ) : (
          part
        ),
      )}
    </>
  );
}

export default function Home() {
  const [editionNumber, setEditionNumber] = useState<EditionNumber>(getEditionFromUrl);
  const [active, setActive] = useState('noticia');
  const [progress, setProgress] = useState(0);
  const [open, setOpen] = useState<string[]>(['01']);
  const edition = editions[editionNumber];
  const article = edition.data;

  const editionLinks = useMemo(
    () =>
      (Object.keys(editions) as EditionNumber[]).map((number) => ({
        number,
        href: `?noticia=${Number(number)}`,
        label: `Noticia ${number}`,
      })),
    [],
  );

  useEffect(() => {
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      setProgress(max > 0 ? (window.scrollY / max) * 100 : 0);
      const current = sections
        .filter((section) => (document.getElementById(section.id)?.getBoundingClientRect().top ?? 10000) < 180)
        .at(-1);
      setActive(current?.id ?? 'noticia');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener('scroll', onScroll);
  }, [editionNumber]);

  useEffect(() => {
    const onPopState = () => setEditionNumber(getEditionFromUrl());
    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  useEffect(() => {
    document.title = `${article.title} | Cuaderno de prensa`;
    const meta = document.querySelector<HTMLMetaElement>('meta[name="description"]');
    if (meta) meta.content = article.subtitle;
  }, [article]);

  const chooseEdition = (event: React.MouseEvent<HTMLAnchorElement>, next: EditionNumber) => {
    event.preventDefault();
    if (next === editionNumber) return;
    const url = new URL(window.location.href);
    url.searchParams.set('noticia', String(Number(next)));
    url.hash = '';
    window.history.pushState({}, '', url);
    setEditionNumber(next);
    setActive('noticia');
    setOpen(['01']);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className={`edition edition-${editionNumber}`}>
      <a href="#noticia" className="skip-link">Saltar al contenido</a>
      <div className="reading-progress" style={{ width: `${progress}%` }} aria-hidden="true" />
      <header className="site-header">
        <a href="#inicio" className="brand" aria-label="Cuaderno de prensa, inicio">
          <span className="brand-symbol">m<span>.</span></span>
          <span>CUADERNO<br />DE PRENSA</span>
        </a>
        <nav aria-label="Navegación principal">
          {editionLinks.map((link) => (
            <a
              href={link.href}
              key={link.number}
              onClick={(event) => chooseEdition(event, link.number)}
              className={editionNumber === link.number ? 'current-edition' : ''}
              aria-current={editionNumber === link.number ? 'page' : undefined}
            >
              {link.label}
              {editionNumber === link.number && <span className="nav-dot" />}
            </a>
          ))}
          <a href="#fuentes">Fuentes <ArrowUpRight size={14} /></a>
        </nav>
        <a href={`${import.meta.env.BASE_URL}${edition.pdf}`} download className="download-link">
          <Download size={16} /><span>Descargar PDF</span>
        </a>
      </header>

      <nav className="mobile-edition-nav" aria-label="Cambiar noticia">
        {editionLinks.map((link) => (
          <a
            href={link.href}
            key={link.number}
            onClick={(event) => chooseEdition(event, link.number)}
            aria-current={editionNumber === link.number ? 'page' : undefined}
          >
            {link.label}
          </a>
        ))}
      </nav>

      <main id="inicio">
        <section className="hero" aria-labelledby="hero-title">
          <div className="hero-topline">
            <span><span className="small-star">✳</span> SISTEMAS × MERCADOTECNIA</span>
            <span>VOL. {edition.number} <i /> {edition.month}</span>
          </div>
          <div className="hero-grid">
            <div className="hero-copy">
              <div className="eyebrow"><span className="lime-dot" /> NOTICIA {edition.number} / INTERNET</div>
              <h1 id="hero-title">{edition.heroTitle}</h1>
              <p>{article.subtitle}</p>
              <a className="hero-cta" href="#noticia">Explorar la noticia <ArrowDown size={18} /></a>
            </div>
            {edition.visual === 'image' ? (
              <figure className="hero-visual">
                <img src={`${import.meta.env.BASE_URL}assets/astra.png`} alt="Ilustración editorial de GPT-6 Astra: esfera luminosa azul y violeta con el emblema de OpenAI" width="1672" height="941" />
                <div className="image-index"><span>EN EL RADAR</span><b>GPT-6<br />Astra<span>↗</span></b></div>
                <figcaption>Ilustración: Future / ChatGPT, vía Tom's Guide</figcaption>
              </figure>
            ) : (
              <figure className="hero-visual shopify-visual">
                <img src={`${import.meta.env.BASE_URL}assets/shopify-whatsapp.png`} alt="Interfaz oficial de Shopify para crear una campaña de WhatsApp y seleccionar un segmento de clientes" width="800" height="600" />
                <div className="image-index"><span>DEL CHECKOUT AL CRM</span><b>Permiso<br />que conecta<span>↗</span></b></div>
                <figcaption>Imagen de producto: Shopify Editions, Spring '26</figcaption>
              </figure>
            )}
          </div>
          <div className="hero-bottom">
            {edition.bottomTags.map((tag) => <span key={tag}>{tag}</span>)}
            <span className="edition-number">{edition.number} — 06</span>
          </div>
        </section>

        <div className="article-shell">
          <aside className="article-nav">
            <div className="sticky-index">
              <p className="eyebrow">EN ESTA ENTRADA</p>
              <nav aria-label="Índice de la noticia">
                {sections.map((section, index) => (
                  <a href={`#${section.id}`} key={section.id} className={active === section.id ? 'active' : ''} aria-current={active === section.id ? 'location' : undefined}>
                    <span>0{index + 1}</span>{section.name}<ArrowUpRight size={15} />
                  </a>
                ))}
              </nav>
              <div className="edition-card">
                <span className="edition-big">{edition.number}<span>/06</span></span>
                <p>{edition.number === '01' ? 'Primera' : 'Segunda'} entrada<br />Cuaderno de prensa</p>
                <div className="edition-track" aria-hidden="true">
                  {[1, 2, 3, 4, 5, 6].map((item) => <i key={item} className={item <= Number(edition.number) ? 'complete' : ''} />)}
                </div>
                <span className="tiny">FUENTE DE INTERNET</span>
              </div>
            </div>
          </aside>

          <div className="article-content">
            <section id="noticia" className="article-section">
              <div className="section-label"><span>01</span> EL CONTEXTO</div>
              <h2>¿De qué trata<br />la noticia?</h2>
              <div className="news-meta"><span>{edition.publisher}</span><span>{edition.newsMeta}</span></div>
              <h3 className="news-headline">{edition.headline}</h3>
              {article.summary.map((paragraph) => <p key={paragraph}><CitedText text={paragraph} /></p>)}
              <a href={article.sources[0].url} target="_blank" rel="noreferrer" className="text-link">Leer la noticia original <ArrowUpRight size={17} /></a>
              <div className="key-note">
                <Sparkles size={22} />
                <p><strong>{edition.keyNoteTitle}</strong>{edition.keyNoteText}</p>
              </div>
            </section>

            <section id="importancia" className="article-section">
              <div className="section-label"><span>02</span> LO QUE ESTÁ EN JUEGO</div>
              <h2>¿Qué importancia<br />tiene?</h2>
              {edition.importance.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
              <div className="balance-grid">
                <div className="balance opportunity">
                  <span className="eyebrow">LA OPORTUNIDAD <ArrowUpRight size={18} /></span>
                  <h3>{edition.number === '01' ? <>Más espacio<br />para la estrategia.</> : <>Una relación<br />más directa.</>}</h3>
                  <p>{article.opportunity}</p>
                </div>
                <div className="balance responsibility">
                  <span className="eyebrow">LA RESPONSABILIDAD <ScanLine size={18} /></span>
                  <h3>{edition.number === '01' ? <>Más criterio<br />en cada decisión.</> : <>El permiso<br />tiene límites.</>}</h3>
                  <p>{article.risk}</p>
                </div>
              </div>
            </section>

            <section id="asignatura" className="article-section">
              <div className="section-label"><span>03</span> DE LA NOTICIA A LA CLASE</div>
              <h2>¿Cómo y con qué temas<br />de la asignatura se relaciona?</h2>
              <p>{edition.sectionLead}</p>
              <div className="topic-list">
                {article.topics.map((topic, index) => {
                  const Icon = edition.topicIcons[index];
                  const expanded = open.includes(topic.number);
                  return (
                    <div className={`topic ${expanded ? 'expanded' : ''}`} key={topic.number}>
                      <h3>
                        <button aria-expanded={expanded} aria-controls={`topic-${topic.number}`} onClick={() => setOpen((previous) => expanded ? previous.filter((number) => number !== topic.number) : [...previous, topic.number])}>
                          <Icon size={22} /><span>{topic.title}</span>{expanded ? <Minus size={19} /> : <Plus size={19} />}
                        </button>
                      </h3>
                      <div id={`topic-${topic.number}`} className="topic-text" hidden={!expanded}><p>{topic.text}</p></div>
                    </div>
                  );
                })}
              </div>
              <div className="case-study">
                <span className="eyebrow">LLEVÉMOSLO A UN EJEMPLO</span>
                <h3>{article.example.title}</h3>
                {'intro' in article.example && article.example.intro && <p className="case-intro">{article.example.intro}</p>}
                <div className="case-steps">
                  {article.example.steps.map((step, index) => (
                    <div key={step.title}><span className="step-number">0{index + 1}</span><h4>{step.title}</h4><p>{step.text}</p></div>
                  ))}
                </div>
                <p className="case-decision">{article.example.decision}</p>
              </div>
            </section>

            <section id="profesion" className="article-section profession">
              <div className="section-label"><span>04</span> MI MIRADA PROFESIONAL</div>
              <h2>¿Cómo se relaciona<br />con mi profesión?</h2>
              {article.profession.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
              <blockquote><span aria-hidden="true">“</span>{article.conclusion}</blockquote>
              <div className="closing-line"><span className="lime-dot" /> {edition.closingLine}</div>
            </section>
          </div>
        </div>

        <section id="fuentes" className="sources-section">
          <div className="sources-heading">
            <div className="section-label">LECTURAS Y REFERENCIAS</div>
            <h2>Detrás del análisis.</h2>
            <p>Una noticia de Internet y su fuente primaria.<br />Consultadas el {edition.sourceDate}.</p>
          </div>
          <div className="sources-list">
            {article.sources.map((source) => (
              <a id={`fuente-${source.id}`} href={source.url} key={source.id} target="_blank" rel="noreferrer">
                <div><span className="eyebrow">[{source.id}] {source.type}</span><h3>{source.title}</h3><p>{source.author} · {source.publisher} · {source.date}</p></div>
                <ArrowUpRight size={23} />
              </a>
            ))}
          </div>
        </section>

        <section className="pdf-strip">
          <div><span className="eyebrow">DEL PORTAFOLIO A LA ENTREGA</span><h2>El análisis completo, en PDF.</h2></div>
          <a className="pdf-button" href={`${import.meta.env.BASE_URL}${edition.pdf}`} download>Descargar noticia {edition.number} <Download size={18} /></a>
        </section>
      </main>

      <footer>
        <a href="#inicio" className="footer-brand">m.</a>
        <p>Ingeniería en Sistemas Computacionales<br /><span>Actividad individual / Noticia {edition.number} de 06</span></p>
        <a href="#inicio" className="back-top">Volver arriba <ArrowUp size={16} /></a>
      </footer>
    </div>
  );
}
