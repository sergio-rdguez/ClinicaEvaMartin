# Clínica Dental Dra. Eva Martín Molina

Web de la clínica dental en Leganés, publicada con GitHub Pages en
https://www.dentalevamartinmolina.com

Es una web estática (HTML, CSS y JavaScript, sin dependencias). Las páginas
interiores se generan con un pequeño script de Python.

## Estructura

```
index.html              Portada (se edita a mano, salvo el bloque "Del blog")
blog/                   Blog (generado entero en cada publicación: no editar)
<tratamiento>/          Una página por tratamiento (generadas)
tratamientos/           Índice de tratamientos (generado)
aviso-legal.html, privacidad.html, cookies.html, 404.html   (generadas)
contacto/, blog-1/      Redirecciones de URLs antiguas de Wix (generadas)
sitemap.xml, site.webmanifest                               (generados)
tools/contenido.py      Textos de los tratamientos
tools/legal.py          Textos legales
tools/generar.py        Plantillas y generador
tools/blog.py           Lectura de las entradas del blog
tools/entradas/         Una entrada del blog por archivo (AAAA-MM-DD-slug.html)
.github/workflows/      Publicación diaria en GitHub Pages
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

## Blog con entradas programadas

Cada entrada es un archivo en `tools/entradas/` con una cabecera y el texto en HTML
sencillo (el formato está explicado al principio de `tools/blog.py`). La fecha de la
cabecera es el día en que se publica: hasta entonces la entrada no aparece en la web,
ni en el sitemap, ni en el RSS.

- **Publicación automática**: la acción `.github/workflows/publicar.yml` genera y
  publica la web cada mañana (06:15 hora de Madrid en invierno) y con cada cambio que
  se sube a `main`. Para que funcione, en GitHub: Settings → Pages → Build and
  deployment → Source: **GitHub Actions**.
- **Añadir una entrada**: crea el archivo en `tools/entradas/` y súbelo. No hace falta
  generar nada a mano.
- **Cambiar la fecha**: edita `fecha:` en la cabecera (el nombre del archivo no
  manda, solo ordena).
- **Revisión de la doctora**: si la Dra. revisa una entrada, añade `revisado: si` a
  la cabecera. La entrada mostrará "Revisado por la Dra. Eva María Martín Molina" y lo
  indicará a Google en los datos estructurados.
- **Previsualizar entradas futuras** en local:
  `python tools/generar.py --hasta 2027-01-31`. Después vuelve a ejecutar
  `python tools/generar.py` antes de hacer commit.
- **Ojo**: GitHub desactiva las tareas programadas de un repositorio público si pasan
  60 días sin ningún commit (avisa antes por correo). Si se programan entradas a más de
  dos meses vista, basta con subir cualquier cambio de vez en cuando o reactivar la
  acción desde la pestaña Actions.

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
- Blog con `BlogPosting` y `BreadcrumbList`, RSS en `/blog/feed.xml` y enlaces
  cruzados entre entradas, tratamientos y portada.
- `sitemap.xml` (con la fecha real de cada página) y `robots.txt`.
- Imágenes WebP con `srcset`, carga diferida y textos alternativos.
- Sin cookies ni recursos externos al cargar.

## Dominio y DNS

- **DNS**: Cloudflare (plan gratuito). Registros en modo *Solo DNS* (nube gris):
  - `A` `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
  - `CNAME` `www` → sergio-rdguez.github.io
- **Registrador**: Wix hasta completar la transferencia a Cloudflare Registrar
  (posible a partir del 23/12/2026).
- **GitHub Pages**: Settings → Pages, origen *GitHub Actions*, dominio
  `www.dentalevamartinmolina.com`, *Enforce HTTPS* activado cuando haya certificado.
