# Cuaderno de prensa · Noticias 01–03

Portafolio de Ingeniería en Sistemas Computacionales para la asignatura de Mercadotecnia, en español sobre GPT-6 Astra, Ingeniería en Sistemas Computacionales y mercadotecnia, desarrollado con **React 19, TypeScript y Vite 8**. Incluye las Noticias 01 y 02 de Internet y la Noticia 03 de revista digital. Las tres entradas comparten navegación; no se simulan las noticias pendientes.

## Abrir y editar

```sh
npm install
npm run dev
```

Vite muestra la dirección local. Para generar la versión de producción: `npm run build`. Para verla: `npm run start`.

- `app/article.json`: contenido y referencias de la noticia.
- `app/page.tsx`: presentación, índice de lectura y secciones desplegables.
- `app/globals.css`: diseño adaptable y estilos de impresión.
- `output/pdf/noticia-01-astra.pdf`: PDF de entrega, también disponible en `public/` para descargar desde la web.

## Regenerar el PDF después de editar

Crear un entorno de Python e instalar `reportlab` y `pypdf`; `pymupdf` es opcional para renderizar las páginas de revisión. Ejecutar `python scripts/create-pdf.py`. El PDF se crea desde `app/article.json`; después ejecutar `npm run build` para incluir la versión actualizada en la web.

## Contenido académico

Responde las cuatro preguntas de la actividad. La fuente de Internet es Tom’s Guide (Amanda Caswell, 4 de septiembre de 2026) y el anuncio de OpenAI sirve de contraste. El lanzamiento corresponde al 3 de septiembre; la fecha de la noticia es distinta. Las aplicaciones a mercadotecnia y el ejemplo de la cafetería son análisis e hipótesis, no resultados empresariales demostrados.

Revisar la reflexión en primera persona para que represente tu opinión. Los temas de la asignatura son temas generales de mercadotecnia: ajustar su nombre al temario de la clase si es necesario. No se inventaron nombre, matrícula, institución o grupo.

La ilustración del artículo se acredita a Future / ChatGPT, vía Tom’s Guide. Las fuentes y sus enlaces están dentro de la web y el PDF.

## Verificación

Se comprueba la compilación de producción y la respuesta HTTP local. El generador comprueba las cuatro páginas del PDF y la presencia de las respuestas; las páginas renderizadas se revisan visualmente. No se realizaron pruebas de interacción en navegador: esta sesión no tenía navegador conectado.

## Publicación

La aplicación utiliza rutas relativas para funcionar dentro de `cuaderno-prensa/` en GitHub Pages. El sitio compilado se guarda en esa carpeta del repositorio y el código editable en `cuaderno-prensa/fuente/`. Después de editar, ejecutar `npm run build` y copiar `dist/` a la carpeta publicada.


## Noticia 03 · Revista digital

Abrir `?noticia=3`. WIRED, Reece Rogers, “The Battle to Be Your Personal AI Agent Is Here”, 30 de septiembre de 2026; consulta del 4 de octubre de 2026. Los datos reportados se citan con [1]. Las interpretaciones de mercadotecnia y los requisitos técnicos se distinguen como análisis propio. No se utilizaron fuentes secundarias ni se afirma conocer la arquitectura interna de los productos.

- `app/article-03.json`: contenido compartido por web y PDF.
- `app/article-03.tsx`: composición editorial de la tercera entrada.
- `public/assets/agent-wars.svg`: ilustración abstracta propia.
- `scripts/pdf-editorial.py`: primitivas ReportLab con medición y límites de página.
- `scripts/create-pdf-03.py`: exportación, copia pública y renderizado de las cuatro páginas.

Se conserva el flujo JSON + ReportLab de las primeras entradas; sus generadores y PDFs no se modifican. Para regenerar la tercera noticia:

```sh
python3 -m pip install reportlab pypdf pymupdf
python3 scripts/create-pdf-03.py
npm run build
```

Entrega: `output/pdf/noticia-03-wired-agentes-ia.pdf`. Copia descargable: `public/noticia-03-wired-agentes-ia.pdf`. Imágenes de revisión: `tmp/pdfs/noticia-03/page-1.png` a `page-4.png`.

La pieza responde al contexto de la noticia en la portada, a su importancia en “De preguntar a delegar”, a su relación con Mercadotecnia en “El producto también es la confianza”, y a su relación con Ingeniería en Sistemas en “Detrás de un mensaje sencillo”. Incluye reflexión en primera persona y referencia enlazada. Identidad editorial: crema, grafito, coral, tipografía amplia y diagramas propios. La infraestructura y los ejemplos se presentan como requisitos y esquemas conceptuales, no como capacidades comprobadas.

### Validación de la tercera entrada

- Build de producción con Vite completado; navegación, metadatos, PDF y consola comprobados también en `vite preview`.
- Navegación 01/02/03, historial atrás/adelante, metadatos y descargas verificadas con Chrome/Playwright.
- Web revisada visualmente y sin desbordamiento horizontal en 1440, 768, 390 y 320 px. Las tres entradas también comprobadas en 768, 820, 1024 y 390 px.
- PDF de cuatro páginas: todas renderizadas y revisadas visualmente, con comprobación de límites de texto y copia pública idéntica.
- TypeScript (`tsc --noEmit`) aprobado. Lint de `app/article-03.tsx` aprobado. El lint global conserva errores previos en componentes UI auxiliares y `app/page.tsx` (reglas de accesibilidad, React, tipos y Next.js); no se alteraron esos componentes para esta entrega. Debido a lecturas lentas de dependencias locales, lint y TypeScript se verificaron también con una copia idéntica del código y dependencias instaladas desde el mismo lockfile en una carpeta temporal. No se cambiaron versiones ni el lockfile.
