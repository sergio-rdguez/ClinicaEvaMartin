"""Genera las páginas interiores de la web a partir de plantillas.

Uso (desde la raíz del repositorio):
    python tools/generar.py

    python tools/generar.py --hasta 2027-01-31   (previsualizar entradas futuras)

Genera: blog (entradas publicadas, índice, RSS), páginas de tratamientos,
/tratamientos/, páginas legales, 404, redirecciones de URLs antiguas de Wix,
sitemap.xml y site.webmanifest.
La portada (index.html) se edita a mano, salvo el bloque "Del blog".
"""
import argparse
import datetime
import html
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contenido import TRATAMIENTOS  # noqa: E402
from legal import AVISO, COOKIES, PRIVACIDAD  # noqa: E402
import blog  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://www.dentalevamartinmolina.com"
HOY = blog.hoy_madrid().isoformat()
TEL = "+34916806724"
TEL_TXT = "91 680 67 24"
WA = "https://wa.me/34640184016?text=Hola%2C%20quer%C3%ADa%20pedir%20cita%20en%20la%20cl%C3%ADnica."
DOCTORA = {"@type": "Person", "name": "Eva María Martín Molina", "jobTitle": "Odontóloga"}
POR_SLUG = {t["slug"]: t for t in TRATAMIENTOS}
CLINICA_ID = {"@id": SITE + "/#clinica"}
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
POR_PAGINA = 12
# Entradas publicadas (de la más nueva a la más antigua). Se rellena en main().
PUBLICADAS = []


def fecha_larga(fecha):
    return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}"


def ultima_modificacion():
    """Fecha del último commit que cambió los textos o las plantillas.

    Así las páginas fijas no cambian de fecha en el sitemap cada vez que la
    publicación diaria vuelve a generar la web.
    """
    try:
        salida = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", "tools/contenido.py", "tools/legal.py",
             "tools/generar.py", "index.html"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        return salida or HOY
    except (OSError, subprocess.CalledProcessError):
        return HOY


ACTUALIZADO = ultima_modificacion()

ICONO_WA = '<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7.1.2 1.8 2.8 4.5 3.9 1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>'
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
        <a href="/blog/">Blog</a>
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
            <li><a href="/blog/">Blog</a></li>
            <li><a href="https://www.facebook.com/p/Cl%C3%ADnica-Dental-Dra-Eva-Mart%C3%ADn-Molina-100068460270961/" target="_blank" rel="noopener">Facebook</a></li>
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

  <div class="call-bar">
    <a href="tel:{TEL}">{ICONO_TEL} Llamar</a>
    <a class="call-wa" href="{WA}" target="_blank" rel="noopener">{ICONO_WA} WhatsApp</a>
  </div>

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
            <a class="btn btn-ghost btn-block" href="{WA}" target="_blank" rel="noopener">{ICONO_WA} Escribir por WhatsApp</a>
            <address>Avenida de la Reina Sofía, 10<br>28919 Leganés, Madrid</address>
            <a class="text-link" href="https://www.google.com/maps?cid=871696087336392580" target="_blank" rel="noopener">Cómo llegar</a>
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
                "lastReviewed": ACTUALIZADO,
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
          <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ICONO_WA} Escribir por WhatsApp</a>
        </div>
      </div>
    </section>

    <div class="wrap page-grid">
        <article class="prose">
{"".join(cuerpo)}        </article>
{aside()}    </div>

{bloque_articulos(t)}
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
          <a class="btn btn-ghost" href="{WA}" target="_blank" rel="noopener">{ICONO_WA} Escribir por WhatsApp</a>
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


# ---------------------------------------------------------------- Blog

RSS_LINK = f'  <link rel="alternate" type="application/rss+xml" title="Blog de la Clínica Dental Dra. Eva Martín Molina" href="{SITE}/blog/feed.xml">\n'


def tarjetas_entradas(lista, nivel="h3"):
    items = []
    for p in lista:
        items.append(
            f'          <li><a href="/blog/{p["slug"]}/">'
            f'<time class="post-card-date" datetime="{p["fecha"].isoformat()}">{fecha_larga(p["fecha"])}</time>'
            f'<{nivel} class="related-name">{e(p["titulo"])}</{nivel}>'
            f'<span class="related-short">{e(p["resumen"])}</span></a></li>')
    return "\n".join(items)


def bloque_articulos(t):
    """Últimos artículos del blog sobre un tratamiento, para su página."""
    lista = [p for p in PUBLICADAS if p["tratamiento"] == t["slug"]][:3]
    if not lista:
        return ""
    return f"""    <section class="section-blog" aria-labelledby="art-title">
      <div class="wrap">
        <h2 id="art-title">Artículos sobre {e(t["nombre"][0].lower() + t["nombre"][1:])}</h2>
        <ul class="related-list post-cards">
{tarjetas_entradas(lista)}
        </ul>
        <a class="text-link" href="/blog/">Ver todos los artículos</a>
      </div>
    </section>
"""


def relacionadas(p, n=3):
    """Entradas del mismo tratamiento primero; si no hay bastantes, las más recientes."""
    otras = [x for x in PUBLICADAS if x["slug"] != p["slug"]]
    mismas = [x for x in otras if x["tratamiento"] == p["tratamiento"]]
    resto = [x for x in otras if x["tratamiento"] != p["tratamiento"]]
    return (mismas + resto)[:n]


def pagina_entrada(p):
    ruta = f"/blog/{p['slug']}/"
    url = SITE + ruta
    t = POR_SLUG[p["tratamiento"]]
    titulo_seo = p.get("titulo_seo") or f"{p['titulo']} | Dra. Eva Martín Molina"
    revisado = p.get("revisado", "").lower() in ("si", "sí", "true")

    articulo = {
        "@type": "BlogPosting",
        "@id": url + "#articulo",
        "mainEntityOfPage": url,
        "url": url,
        "headline": p["titulo"],
        "description": p["descripcion"],
        "datePublished": p["fecha"].isoformat(),
        "dateModified": p.get("actualizado") or p["fecha"].isoformat(),
        "inLanguage": "es-ES",
        "image": SITE + "/assets/img/og-image.jpg",
        "author": {"@type": "Organization", "name": "Clínica Dental Dra. Eva Martín Molina", "url": SITE + "/"},
        "publisher": CLINICA_ID,
        "isPartOf": {"@id": SITE + "/blog/#blog"},
        "about": {"@type": "MedicalProcedure", "name": t["nombre"], "url": f"{SITE}/{t['slug']}/"},
    }
    if revisado:
        articulo["reviewedBy"] = DOCTORA
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            articulo,
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                    {"@type": "ListItem", "position": 3, "name": p["titulo"], "item": url},
                ],
            },
        ],
    }
    meta_revision = (
        '<span>Revisado por la Dra. Eva María Martín Molina, odontóloga colegiada nº 28006108</span>'
        if revisado else '<span>Clínica Dental Dra. Eva Martín Molina</span>')
    mas = relacionadas(p)
    bloque_mas = ""
    if mas:
        bloque_mas = f"""
    <section class="related" aria-labelledby="mas-title">
      <div class="wrap">
        <h2 id="mas-title">Sigue leyendo</h2>
        <ul class="related-list post-cards">
{tarjetas_entradas(mas)}
        </ul>
        <a class="text-link" href="/blog/">Ver todos los artículos</a>
      </div>
    </section>
"""
    extra = jsonld(graph) + RSS_LINK + f'  <meta property="article:published_time" content="{p["fecha"].isoformat()}">\n'
    return (
        head(titulo_seo, p["descripcion"], ruta, extra, og_tipo="article")
        + header()
        + f"""
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
{migas([("Inicio", "/"), ("Blog", "/blog/"), (p["titulo"], None)])}        <h1>{e(p["h1"])}</h1>
        <p class="post-meta"><time datetime="{p["fecha"].isoformat()}">{fecha_larga(p["fecha"])}</time>{meta_revision}</p>
      </div>
    </section>

    <div class="wrap page-grid">
        <article class="prose">
{p["cuerpo"]}
          <div class="post-cta">
            <p class="post-cta-title">¿Quieres que lo veamos en consulta?</p>
            <p>En la clínica de la Dra. Eva Martín Molina, en Leganés, te explicamos tu caso con calma y sin compromiso.</p>
            <p class="post-cta-links"><a href="/{t["slug"]}/">Más sobre {e(t["nombre"][0].lower() + t["nombre"][1:])}</a> · <a href="tel:{TEL}">Llamar al {TEL_TXT}</a></p>
          </div>
          <p class="prose-note">Este artículo es informativo y no sustituye una valoración en consulta. Si tienes dolor o una urgencia, llámanos.</p>
        </article>
{aside()}    </div>
{bloque_mas}  </main>
"""
        + footer()
    )


def pagina_blog(n, total, lista):
    ruta = "/blog/" if n == 1 else f"/blog/pagina/{n}/"
    titulo = "Blog de salud dental | Clínica Dental Dra. Eva Martín Molina, Leganés"
    if n > 1:
        titulo = f"Blog de salud dental (página {n}) | Dra. Eva Martín Molina"
    desc = ("Consejos de salud bucodental de la clínica de la Dra. Eva Martín Molina en Leganés: "
            "implantes, ortodoncia, encías, blanqueamiento, bruxismo y cuidado diario.")
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": SITE + "/blog/#blog",
                "url": SITE + "/blog/",
                "name": "Blog de la Clínica Dental Dra. Eva Martín Molina",
                "description": desc,
                "inLanguage": "es-ES",
                "publisher": CLINICA_ID,
                "isPartOf": {"@id": SITE + "/#web"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                ],
            },
        ],
    }
    enlaces = []
    if n > 1:
        anterior = "/blog/" if n == 2 else f"/blog/pagina/{n - 1}/"
        enlaces.append(f'<a class="btn btn-ghost" href="{anterior}" rel="prev">Artículos más recientes</a>')
    if n < total:
        enlaces.append(f'<a class="btn btn-ghost" href="/blog/pagina/{n + 1}/" rel="next">Artículos anteriores</a>')
    paginacion = ""
    if enlaces:
        paginacion = (f'        <nav class="pager" aria-label="Páginas del blog">{"".join(enlaces)}'
                      f'<span class="pager-info">Página {n} de {total}</span></nav>\n')
    if lista:
        contenido = f"""        <ul class="related-list post-cards">
{tarjetas_entradas(lista, "h2")}
        </ul>
"""
    else:
        contenido = "        <p>Muy pronto publicaremos aquí nuestros primeros artículos.</p>\n"
    return (
        head(titulo, desc, ruta, jsonld(graph) + RSS_LINK)
        + header()
        + f"""
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
{migas([("Inicio", "/"), ("Blog", None)])}        <h1>Blog de salud dental</h1>
        <p class="lead">Respuestas claras a las dudas que más nos preguntáis en la consulta: qué es normal, qué no, y cuándo conviene venir a vernos.</p>
      </div>
    </section>

    <section class="section blog-index">
      <div class="wrap">
{contenido}{paginacion}      </div>
    </section>
  </main>
"""
        + footer()
    )


def feed_rss(lista):
    def rfc822(fecha):
        dias = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{dias[fecha.weekday()]}, {fecha.day:02d} {meses[fecha.month - 1]} {fecha.year} 07:00:00 +0100"

    items = []
    for p in lista[:20]:
        url = f"{SITE}/blog/{p['slug']}/"
        items.append(f"""    <item>
      <title>{e(p["titulo"])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{rfc822(p["fecha"])}</pubDate>
      <description>{e(p["descripcion"])}</description>
    </item>""")
    ultima = rfc822(lista[0]["fecha"]) if lista else rfc822(blog.hoy_madrid())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Blog de la Clínica Dental Dra. Eva Martín Molina</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Consejos de salud bucodental desde nuestra clínica en Leganés.</description>
    <language>es-ES</language>
    <lastBuildDate>{ultima}</lastBuildDate>
{chr(10).join(items)}
  </channel>
</rss>
"""


INICIO_MARCA = "<!-- BLOG:INICIO (lo rellena tools/generar.py) -->"
FIN_MARCA = "<!-- BLOG:FIN -->"


def actualizar_portada():
    """Pone las tres últimas entradas en la portada, entre las marcas BLOG:INICIO y BLOG:FIN."""
    archivo = ROOT / "index.html"
    texto = archivo.read_text(encoding="utf-8")
    ini, fin = texto.find(INICIO_MARCA), texto.find(FIN_MARCA)
    if ini == -1 or fin == -1:
        print("   (index.html sin marcas BLOG: no se actualiza la portada)")
        return
    bloque = ""
    if PUBLICADAS:
        bloque = f"""
    <section class="section section-blog home-blog" id="blog" aria-labelledby="b-title">
      <div class="wrap">
        <h2 id="b-title">Del blog</h2>
        <ul class="related-list post-cards">
{tarjetas_entradas(PUBLICADAS[:3])}
        </ul>
        <a class="text-link" href="/blog/">Ver todos los artículos</a>
      </div>
    </section>
    """
    nuevo = texto[:ini + len(INICIO_MARCA)] + bloque + texto[fin:]
    if nuevo != texto:
        archivo.write_text(nuevo, encoding="utf-8", newline="\n")
        print("   index.html (últimas entradas)")


# (ruta antigua de Wix, destino, texto del enlace). Las rutas van sin codificar:
# Google pide /caracter%C3%ADsticas-... y GitHub Pages sirve la carpeta con tilde.
WIX_ANTIGUAS = [
    ("blog-1", "/blog/", "Ir al blog"),
    ("blog-1/tags/endodoncia", "/odontologia-general/", "Ver odontología general"),
    ("blog-1/tags/ortodoncia-invisible", "/ortodoncia-invisible/", "Ver ortodoncia invisible"),
    ("single-post/2017/06/22/características-de-los-implantes-dentales",
     "/implantes/", "Ver implantes dentales"),
    ("single-post/2019/01/21/cuidados-básicos-que-requieren-los-implantes-dentales",
     "/implantes/", "Ver implantes dentales"),
    ("single-post/2018/07/17/5-preguntas-frecuentes-sobre-el-blanqueamiento-dental",
     "/blanqueamiento-dental/", "Ver blanqueamiento dental"),
    ("single-post/2018/09/07/ventajas-de-la-ortodoncia-invisible",
     "/ortodoncia-invisible/", "Ver ortodoncia invisible"),
]


def redireccion(destino, texto):
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Esta página se ha movido | Clínica Dental Dra. Eva Martín Molina</title>
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
    parser = argparse.ArgumentParser(description="Genera las páginas interiores de la web.")
    parser.add_argument("--hasta", metavar="AAAA-MM-DD",
                        help="Publica las entradas del blog hasta esa fecha (para previsualizar en local). "
                             "No hagas commit del resultado: vuelve a generar sin esta opción.")
    args = parser.parse_args()
    hasta = datetime.date.fromisoformat(args.hasta) if args.hasta else None

    publicadas, todas = blog.entradas(hasta, tratamientos=POR_SLUG)
    PUBLICADAS[:] = publicadas
    pendientes = len(todas) - len(publicadas)
    print(f"Blog: {len(publicadas)} entradas publicadas, {pendientes} programadas.")
    if pendientes:
        proxima = min(t["fecha"] for t in todas if t not in publicadas)
        ultima = max(t["fecha"] for t in todas)
        print(f"      Próxima: {proxima}. Última programada: {ultima}.")

    print("Generando páginas:")
    # La carpeta /blog/ se genera entera cada vez (así desaparece lo que se quite o se reprograme)
    shutil.rmtree(ROOT / "blog", ignore_errors=True)
    for p in PUBLICADAS:
        escribir(f"blog/{p['slug']}/index.html", pagina_entrada(p))
    paginas = max(1, -(-len(PUBLICADAS) // POR_PAGINA))
    for n in range(1, paginas + 1):
        trozo = PUBLICADAS[(n - 1) * POR_PAGINA:n * POR_PAGINA]
        escribir("blog/index.html" if n == 1 else f"blog/pagina/{n}/index.html", pagina_blog(n, paginas, trozo))
    escribir("blog/feed.xml", feed_rss(PUBLICADAS))
    actualizar_portada()

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

    # URLs antiguas de la web de Wix que Google sigue rastreando. GitHub Pages no
    # permite redirecciones 301, así que cada una es una página con redirección
    # inmediata (meta refresh) y canonical al destino, que Google trata como un 301.
    # Sin "noindex": con él, Google la marca como "Excluida por noindex" en vez de
    # seguir la redirección.
    escribir("contacto/index.html", redireccion("/#contacto", "Ir a horario y contacto"))
    for antigua, destino, texto in WIX_ANTIGUAS:
        escribir(f"{antigua}/index.html", redireccion(destino, texto))

    ultima_entrada = PUBLICADAS[0]["fecha"].isoformat() if PUBLICADAS else ACTUALIZADO
    reciente = max(ACTUALIZADO, ultima_entrada)

    def ultima_de(slug):
        fechas = [p["fecha"].isoformat() for p in PUBLICADAS if p["tratamiento"] == slug]
        return max([ACTUALIZADO] + fechas)

    # (ruta, prioridad, frecuencia, última modificación)
    urls = [("/", "1.0", "weekly", reciente), ("/tratamientos/", "0.9", "monthly", ACTUALIZADO)]
    urls += [(f"/{t['slug']}/", "0.8", "monthly", ultima_de(t["slug"])) for t in TRATAMIENTOS]
    urls += [("/blog/", "0.7", "daily", reciente)]
    urls += [(f"/blog/{p['slug']}/", "0.6", "yearly", p.get("actualizado") or p["fecha"].isoformat())
             for p in PUBLICADAS]
    urls += [(p, "0.2", "yearly", ACTUALIZADO) for p in ("/aviso-legal.html", "/privacidad.html", "/cookies.html")]
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for ruta, prioridad, freq, lastmod in urls:
        sitemap.append(f"  <url><loc>{SITE}{ruta}</loc><lastmod>{lastmod}</lastmod>"
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
