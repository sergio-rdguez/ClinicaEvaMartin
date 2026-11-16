"""Genera las páginas interiores de la web a partir de plantillas.

Uso (desde la raíz del repositorio):
    python tools/generar.py

Genera: páginas de tratamientos, /tratamientos/, páginas legales, 404,
redirecciones de URLs antiguas de Wix, sitemap.xml y site.webmanifest.
La portada (index.html) se edita a mano.
"""
import datetime
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contenido import TRATAMIENTOS  # noqa: E402
from legal import AVISO, COOKIES, PRIVACIDAD  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.dentalevamartinmolina.com"
HOY = datetime.date.today().isoformat()
TEL = "+34916806724"
TEL_TXT = "91 680 67 24"
DOCTORA = {"@type": "Person", "name": "Eva María Martín Molina", "jobTitle": "Odontóloga"}
POR_SLUG = {t["slug"]: t for t in TRATAMIENTOS}

ICONO_TEL = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>'


def e(texto):
    return html.escape(texto, quote=True)


def jsonld(data):
    return '  <script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n  </script>\n"


def head(titulo, descripcion, ruta, extra="", robots=None, og_tipo="website"):
    url = SITE + ruta
    # Una página noindex (como la 404) no lleva canonical
    if robots:
        meta_indexacion = f'  <meta name="robots" content="{robots}">'
    else:
        meta_indexacion = f'  <link rel="canonical" href="{url}">'
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titulo)}</title>
  <meta name="description" content="{e(descripcion)}">
{meta_indexacion}
  <meta name="theme-color" content="#12386a">

  <meta property="og:type" content="{og_tipo}">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Clínica Dental Dra. Eva Martín Molina">
  <meta property="og:title" content="{e(titulo)}">
  <meta property="og:description" content="{e(descripcion)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">

  <link rel="preload" href="/assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/css/styles.css">
{extra}</head>
"""


def header():
    return f"""<body>
  <a class="skip" href="#main">Saltar al contenido</a>

  <header class="site-header" id="top">
    <div class="wrap header-inner">
      <a class="brand" href="/" aria-label="Clínica Dental Dra. Eva Martín Molina, inicio">
        <img src="/assets/img/logo.png" alt="" width="317" height="187">
        <span class="brand-text">
          <span class="brand-name">Dra. Eva Martín Molina</span>
          <span class="brand-sub">Clínica dental en Leganés</span>
        </span>
      </a>

      <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">
        <span class="nav-toggle-bars" aria-hidden="true"></span>
        <span class="sr-only">Menú</span>
      </button>

      <nav class="site-nav" id="site-nav" aria-label="Principal">
        <a href="/tratamientos/">Tratamientos</a>
        <a href="/#doctora">La doctora</a>
        <a href="/#clinica">La clínica</a>
        <a href="/#contacto">Contacto</a>
        <a class="btn btn-small" href="tel:{TEL}">{TEL_TXT}</a>
      </nav>
    </div>
  </header>
"""


def footer():
    tratamientos = "\n".join(
        f'            <li><a href="/{t["slug"]}/">{e(t["nombre"])}</a></li>' for t in TRATAMIENTOS)
    return f"""
  <footer class="site-footer">
    <div class="wrap footer-inner">
      <div class="footer-brand">
        <img src="/assets/img/logo.png" alt="" width="317" height="187" loading="lazy">
        <p>Clínica Dental Dra. Eva Martín Molina<br>Av. de la Reina Sofía, 10, 28919 Leganés<br><a href="tel:{TEL}">{TEL_TXT}</a></p>
      </div>
      <nav class="footer-cols" aria-label="Pie de página">
        <div>
          <p class="footer-h">Tratamientos</p>
          <ul>
{tratamientos}
          </ul>
        </div>
        <div>
          <p class="footer-h">Clínica</p>
          <ul>
            <li><a href="/#doctora">La doctora</a></li>
            <li><a href="/#clinica">La clínica</a></li>
            <li><a href="/#contacto">Horario y contacto</a></li>
            <li><a href="https://www.facebook.com/Cl%C3%ADnica-Dental-Dra-Eva-Mart%C3%ADn-Molina-311185449074099/" target="_blank" rel="noopener">Facebook</a></li>
          </ul>
        </div>
      </nav>
      <div class="footer-legal">
        <p class="footer-reg">Centro sanitario autorizado por la Comunidad de Madrid, nº de registro CS11178. Dra. Eva María Martín Molina, colegiada nº 28006108.</p>
        <p>© <span data-year>{datetime.date.today().year}</span> Clínica Dental Dra. Eva Martín Molina</p>
        <nav aria-label="Información legal">
          <a href="/aviso-legal.html">Aviso legal</a>
          <a href="/privacidad.html">Privacidad</a>
          <a href="/cookies.html">Cookies</a>
        </nav>
      </div>
    </div>
  </footer>

  <a class="call-bar" href="tel:{TEL}">
    {ICONO_TEL}
    Llamar para pedir cita
  </a>

  <script src="/js/main.js" defer></script>
</body>
</html>
"""


def migas(items):
    """items: lista de (nombre, ruta o None para la página actual)."""
    lis = []
    for nombre, ruta in items:
        if ruta:
            lis.append(f'<li><a href="{ruta}">{e(nombre)}</a></li>')
        else:
            lis.append(f'<li aria-current="page">{e(nombre)}</li>')
    return '        <nav class="crumbs" aria-label="Estás en"><ol>' + "".join(lis) + "</ol></nav>\n"


def aside():
    filas = []
    dias = [("1", "Lunes"), ("2", "Martes"), ("3", "Miércoles"), ("4", "Jueves"), ("5", "Viernes")]
    for num, dia in dias:
        filas.append(f'<tr data-day="{num}"><th scope="row">{dia}</th><td>10:00–13:30<br>16:00–20:30</td></tr>')
    filas.append('<tr data-day="6" class="closed"><th scope="row">Sábado</th><td>Cerrado</td></tr>')
    filas.append('<tr data-day="0" class="closed"><th scope="row">Domingo</th><td>Cerrado</td></tr>')
    filas_html = "\n              ".join(filas)
    return f"""
        <aside class="page-aside" id="visita" aria-label="Pide cita">
          <div class="aside-card">
            <p class="aside-title">Pide cita</p>
            <div class="status status-inline" data-status aria-live="polite">
              <span class="status-dot" aria-hidden="true"></span>
              <span class="status-text">
                <strong data-status-title>Horario</strong>
                <span data-status-detail>Lunes a viernes: 10:00–13:30 y 16:00–20:30</span>
              </span>
            </div>
            <a class="btn btn-block" href="tel:{TEL}">{ICONO_TEL} {TEL_TXT}</a>
            <address>Avenida de la Reina Sofía, 10<br>28919 Leganés, Madrid</address>
            <a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query=Avenida+de+la+Reina+Sof%C3%ADa+10%2C+28919+Legan%C3%A9s" target="_blank" rel="noopener">Cómo llegar</a>
            <table class="aside-hours">
              <tbody data-hours>
              {filas_html}
              </tbody>
            </table>
            <p class="aside-doc">Te atiende la Dra. Eva María Martín Molina, odontóloga colegiada nº 28006108.</p>
          </div>
        </aside>
"""


def pagina_tratamiento(t):
    ruta = f"/{t['slug']}/"
    url = SITE + ruta
    crumbs = [("Inicio", "/"), ("Tratamientos", "/tratamientos/"), (t["nombre"], None)]

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "@id": url + "#pagina",
                "url": url,
                "name": t["titulo"],
                "description": t["descripcion"],
                "inLanguage": "es-ES",
                "isPartOf": {"@id": SITE + "/#web"},
                "publisher": {"@id": SITE + "/#clinica"},
                "lastReviewed": HOY,
                "reviewedBy": DOCTORA,
                "about": {"@type": "MedicalProcedure", "name": t["nombre"], "description": t["intro"]},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Tratamientos", "item": SITE + "/tratamientos/"},
                    {"@type": "ListItem", "position": 3, "name": t["nombre"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                    for q, a in t["faqs"]
                ],
            },
        ],
    }

    cuerpo = []
    secciones = list(t["secciones"])
    if secciones:
        h2, contenido = secciones.pop(0)
        cuerpo.append(f"          <h2>{e(h2)}</h2>\n{contenido.strip()}\n")
    if t["pasos"]:
        pasos = "\n".join(
            f'            <li><h3>{e(titulo)}</h3><p>{e(texto)}</p></li>' for titulo, texto in t["pasos"])
        cuerpo.append(f'          <h2>Cómo es el tratamiento</h2>\n          <ol class="steps">\n{pasos}\n          </ol>\n')
    for h2, contenido in secciones:
        cuerpo.append(f"          <h2>{e(h2)}</h2>\n{contenido.strip()}\n")
    faqs = "\n".join(
        f'            <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t["faqs"])
    cuerpo.append(f'          <h2>Preguntas frecuentes</h2>\n          <div class="faq">\n{faqs}\n          </div>\n')
    cuerpo.append('          <p class="prose-note">La información de esta página es orientativa. Cada caso necesita una valoración personal en consulta.</p>\n')

    relacionados = "\n".join(
        f'          <li><a href="/{r}/"><span class="related-name">{e(POR_SLUG[r]["nombre"])}</span>'
        f'<span class="related-short">{e(POR_SLUG[r]["resumen"])}</span></a></li>'
        for r in t["relacionados"])

    return (
        head(t["titulo"], t["descripcion"], ruta, jsonld(graph), og_tipo="article")
        + header()
        + f"""
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
{migas(crumbs)}        <h1>{e(t["h1"])}</h1>
        <p class="lead">{e(t["intro"])}</p>
        <div class="hero-actions">
          <a class="btn" href="tel:{TEL}">{ICONO_TEL} Pedir cita: {TEL_TXT}</a>
          <a class="btn btn-ghost" href="#visita">Horario y dirección</a>
        </div>
      </div>
    </section>

    <div class="wrap page-grid">
        <article class="prose">
{"".join(cuerpo)}        </article>
{aside()}    </div>

    <section class="related" aria-labelledby="rel-title">
      <div class="wrap">
        <h2 id="rel-title">Otros tratamientos</h2>
        <ul class="related-list">
{relacionados}
        </ul>
        <a class="text-link" href="/tratamientos/">Ver todos los tratamientos</a>
      </div>
    </section>
  </main>
"""
        + footer()
    )


def pagina_tratamientos():
    ruta = "/tratamientos/"
    titulo = "Tratamientos dentales en Leganés | Dra. Eva Martín Molina"
    desc = "Implantes, ortodoncia, ortodoncia invisible, estética dental, blanqueamiento, férulas para el bruxismo y odontología general en Leganés."
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": SITE + ruta + "#pagina",
                "url": SITE + ruta,
                "name": titulo,
                "description": desc,
                "inLanguage": "es-ES",
                "isPartOf": {"@id": SITE + "/#web"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Tratamientos", "item": SITE + ruta},
                ],
            },
        ],
    }
    tarjetas = "\n".join(
        f"""          <li>
            <a class="treat-card" href="/{t['slug']}/">
              <span class="treat-card-name">{e(t['nombre'])}</span>
              <span class="treat-card-short">{e(t['resumen'])}</span>
              <span class="treat-card-more">Ver tratamiento</span>
            </a>
          </li>""" for t in TRATAMIENTOS)
    return (
        head(titulo, desc, ruta, jsonld(graph))
        + header()
        + f"""
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
{migas([("Inicio", "/"), ("Tratamientos", None)])}        <h1>Tratamientos dentales en Leganés</h1>
        <p class="lead">Cada tratamiento empieza con un diagnóstico hecho por la Dra. Eva Martín Molina y un plan explicado con calma, para que sepas en todo momento qué vamos a hacer y por qué.</p>
        <div class="hero-actions">
          <a class="btn" href="tel:{TEL}">{ICONO_TEL} Pedir cita: {TEL_TXT}</a>
        </div>
      </div>
    </section>

    <section class="section treat-index">
      <div class="wrap">
        <ul class="treat-cards">
{tarjetas}
        </ul>
      </div>
    </section>
  </main>
"""
        + footer()
    )


def pagina_legal(archivo, titulo, desc, cuerpo):
    return (
        head(f"{titulo} | Clínica Dental Dra. Eva Martín Molina", desc, "/" + archivo)
        + header()
        + f"""
  <main id="main" class="legal">
    <div class="wrap">
{cuerpo}
    </div>
  </main>
"""
        + footer()
    )


def pagina_404():
    enlaces = "\n".join(
        f'          <li><a href="/{t["slug"]}/">{e(t["nombre"])}</a></li>' for t in TRATAMIENTOS)
    return (
        head("Página no encontrada | Clínica Dental Dra. Eva Martín Molina",
             "La página que buscas no existe. Vuelve al inicio o llámanos para pedir cita.",
             "/404.html", robots="noindex")
        + header()
        + f"""
  <main id="main" class="legal">
    <div class="wrap">
      <h1>Esta página ya no existe</h1>
      <p class="legal-updated">Hemos renovado nuestra web y algunas direcciones han cambiado.</p>
      <p class="hero-actions">
        <a class="btn" href="/">Ir al inicio</a>
        <a class="btn btn-ghost" href="tel:{TEL}">Llamar al {TEL_TXT}</a>
      </p>
      <h2>Quizá buscabas</h2>
      <ul>
{enlaces}
      </ul>
    </div>
  </main>
"""
        + footer()
    )


def redireccion(destino, texto):
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Esta página se ha movido | Clínica Dental Dra. Eva Martín Molina</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}{destino.split('#')[0]}">
  <meta http-equiv="refresh" content="0; url={destino}">
  <script>location.replace("{destino}");</script>
</head>
<body>
  <p>Esta página se ha movido. <a href="{destino}">{texto}</a>.</p>
</body>
</html>
"""


def escribir(ruta_rel, contenido):
    destino = ROOT / ruta_rel
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8", newline="\n")
    print("  ", ruta_rel)


def main():
    print("Generando páginas:")
    for t in TRATAMIENTOS:
        escribir(f"{t['slug']}/index.html", pagina_tratamiento(t))
    escribir("tratamientos/index.html", pagina_tratamientos())

    escribir("aviso-legal.html", pagina_legal(
        "aviso-legal.html", "Aviso legal",
        "Aviso legal de la web de la Clínica Dental Dra. Eva Martín Molina, en Leganés.", AVISO))
    escribir("privacidad.html", pagina_legal(
        "privacidad.html", "Política de privacidad",
        "Cómo trata los datos personales la Clínica Dental Dra. Eva Martín Molina.", PRIVACIDAD))
    escribir("cookies.html", pagina_legal(
        "cookies.html", "Política de cookies",
        "Esta web no usa cookies. Información sobre el mapa de Google que se carga bajo demanda.", COOKIES))
    escribir("404.html", pagina_404())

    # URLs antiguas de la web de Wix que no tienen equivalente directo
    escribir("contacto/index.html", redireccion("/#contacto", "Ir a horario y contacto"))
    escribir("blog-1/index.html", redireccion("/", "Ir al inicio"))

    urls = [("/", "1.0", "monthly"), ("/tratamientos/", "0.9", "monthly")]
    urls += [(f"/{t['slug']}/", "0.8", "monthly") for t in TRATAMIENTOS]
    urls += [(p, "0.2", "yearly") for p in ("/aviso-legal.html", "/privacidad.html", "/cookies.html")]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for ruta, prioridad, freq in urls:
        sitemap.append(f"  <url><loc>{SITE}{ruta}</loc><lastmod>{HOY}</lastmod>"
                       f"<changefreq>{freq}</changefreq><priority>{prioridad}</priority></url>")
    sitemap.append("</urlset>\n")
    escribir("sitemap.xml", "\n".join(sitemap))

    manifest = {
        "name": "Clínica Dental Dra. Eva Martín Molina",
        "short_name": "Dra. Eva Martín",
        "lang": "es",
        "start_url": "/",
        "display": "browser",
        "background_color": "#ffffff",
        "theme_color": "#12386a",
        "icons": [
            {"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    escribir("site.webmanifest", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print("Listo.")


if __name__ == "__main__":
    main()
