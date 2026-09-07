# Cuaderno de prensa · Noticia 01

Portafolio de Ingeniería en Sistemas Computacionales para la asignatura de Mercadotecnia, en español sobre GPT-6 Astra, Ingeniería en Sistemas Computacionales y mercadotecnia, desarrollado con **React 19, TypeScript y Vite 8**. Incluye solamente la primera noticia, de Internet; no simula las otras cinco entradas.

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
