# Cuaderno de prensa · Mercadotecnia

Edición académica de Anton Betak Licea para Ingeniería en Sistemas Computacionales, Otoño 2026. El cuaderno reúne **seis noticias terminadas**, con análisis y reflexión sobre tecnología, innovación y mercados. La portada editorial abre la experiencia; las noticias mantienen sus enlaces directos `?noticia=1` a `?noticia=6` y sus PDF individuales.

Producción: https://cuaderno-de-prensa.vercel.app

## Desarrollo

Requiere Node.js 22.13 o posterior.

```sh
npm ci
npm run dev
npm run build
npm run start
npx tsc --noEmit
npm run lint
```

La aplicación utiliza React, TypeScript y Vite. Los contenidos están en `app/article*.json` y sus presentaciones en `app/page.tsx` y `app/article-0*.tsx`; los estilos están en `app/globals.css`.

## PDF de entrega

La portada individual está en `output/pdf/portada-cuaderno-de-prensa.pdf`. El cuaderno completo descargable está en `output/pdf/Cuaderno-de-Prensa-Anton-Betak-Licea-Otono-2026.pdf`, con una copia idéntica en `public/`. Contiene 25 páginas: portada y seis noticias originales de cuatro páginas cada una. Incluye marcadores para cada sección y conserva el contenido y los enlaces de los PDF originales.

Para regenerar la portada vectorial y ensamblar los seis PDF existentes, instalar ReportLab y pypdf en un entorno de Python y ejecutar:

```sh
python3 -m pip install reportlab pypdf
python3 scripts/create-complete-notebook.py
npm run build
```

El script no regenera ni modifica los PDF individuales. Los generadores anteriores de cada noticia permanecen en `scripts/`.

## Verificación

El ensamblado comprueba el número real de páginas y crea los marcadores y metadatos. Las noticias originales deben conservarse sin cambios; el documento combinado se puede inspeccionar con cualquier lector PDF compatible con marcadores. La prueba de navegador histórica `scripts/verify-notebook.cjs` requiere Playwright y un navegador Chromium disponibles.

Se verificaron la compilación de producción y TypeScript con una copia limpia instalada desde el lockfile. En Chromium se comprobaron portada y seis rutas directas a 320, 390, 768, 1024, 1440 y 1920 px, descargas, historial, acceso por teclado y ausencia de errores de consola. Se revisó la portada PDF renderizada y se comparó el renderizado de las 24 páginas de noticias con los originales. El lint global sigue señalando diagnósticos preexistentes en componentes auxiliares y en el contenido anterior de `app/page.tsx`.
