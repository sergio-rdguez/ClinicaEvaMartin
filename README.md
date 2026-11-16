# Clínica Dental Dra. Eva Martín Molina

Web de la clínica dental en Leganés, publicada con GitHub Pages en
https://www.dentalevamartinmolina.com

Es una web estática (HTML, CSS y JavaScript, sin dependencias). Las páginas
interiores se generan con un pequeño script de Python.

## Estructura

```
index.html              Portada (se edita a mano)
<tratamiento>/          Una página por tratamiento (generadas)
tratamientos/           Índice de tratamientos (generado)
aviso-legal.html, privacidad.html, cookies.html, 404.html   (generadas)
contacto/, blog-1/      Redirecciones de URLs antiguas de Wix (generadas)
sitemap.xml, site.webmanifest                               (generados)
tools/contenido.py      Textos de los tratamientos
tools/legal.py          Textos legales
tools/generar.py        Plantillas y generador
css/styles.css          Estilos (paleta y tipografía en las variables de :root)
js/main.js              Menú móvil, estado "abierto/cerrado", mapa bajo demanda
assets/img/             Fotos (JPG + WebP en varios tamaños), logo e iconos
assets/fonts/           Tipografías alojadas en la propia web
CNAME                   Dominio propio para GitHub Pages
```

## Editar contenidos

- **Tratamientos**: edita `tools/contenido.py` y ejecuta `python tools/generar.py`.
  Para añadir un tratamiento nuevo, añade un bloque a la lista y enlázalo también
  desde la portada (`index.html`, sección `#tratamientos`).
- **Textos legales**: `tools/legal.py` y vuelve a generar.
- **Cabecera y pie**: en `tools/generar.py` (funciones `header` y `footer`).
  El pie de `index.html` es una copia: si cambias el pie, cópialo también allí.
- **Horario**: tabla de `index.html`, función `aside` de `tools/generar.py` y el
  objeto `schedule` de `js/main.js`. Actualiza también `openingHoursSpecification`
  en el JSON-LD de `index.html`.

## Ver en local

```bash
python -m http.server 8080
```

Y abrir http://localhost:8080

## SEO incluido

- Título, descripción, canonical y Open Graph únicos en cada página.
- Datos estructurados (JSON-LD): `Dentist` con dirección, horario y servicios en la
  portada; `MedicalWebPage`, `BreadcrumbList` y `FAQPage` en cada tratamiento.
- Una página por tratamiento con URL propia, manteniendo las URLs antiguas de Wix
  (`/implantes`, `/ortodoncia`, `/ortodoncia-invisible`, `/estetica-dental`,
  `/tratamientos`, `/contacto`).
- `sitemap.xml` y `robots.txt`.
- Imágenes WebP con `srcset`, carga diferida y textos alternativos.
- Sin cookies ni recursos externos al cargar.

## Dominio y DNS

- **DNS**: Cloudflare (plan gratuito). Registros en modo *Solo DNS* (nube gris):
  - `A` `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
  - `CNAME` `www` → sergio-rdguez.github.io
- **Registrador**: Wix hasta completar la transferencia a Cloudflare Registrar
  (posible a partir del 23/12/2026).
- **GitHub Pages**: Settings → Pages, rama `main` / `(root)`, dominio
  `www.dentalevamartinmolina.com`, *Enforce HTTPS* activado cuando haya certificado.
