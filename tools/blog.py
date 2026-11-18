"""Lectura de las entradas del blog.

Cada entrada es un archivo en tools/entradas/ con este formato:

    ---
    titulo: ¿Por qué me sangran las encías?
    descripcion: Texto para Google (entre 120 y 160 caracteres).
    fecha: 2026-11-20
    tratamiento: odontologia-general
    resumen: Una o dos frases para las tarjetas del blog.
    ---
    <p>Cuerpo de la entrada en HTML sencillo: p, h2, h3, ul, ol, li, strong, a.</p>

Campos opcionales: h1 (si es distinto del título) y titulo_seo (la etiqueta
<title> si es distinta de "titulo | Dra. Eva Martín Molina").

El nombre del archivo da la dirección de la entrada: 2026-11-20-sangrado-encias.html
se publica en /blog/sangrado-encias/. La fecha que manda es la del campo "fecha":
la entrada no aparece en la web hasta ese día (hora de Madrid).
"""
import datetime
import pathlib
import re

CARPETA = pathlib.Path(__file__).resolve().parent / "entradas"
OBLIGATORIOS = ("titulo", "descripcion", "fecha", "tratamiento", "resumen")
NOMBRE = re.compile(r"^\d{4}-\d{2}-\d{2}-([a-z0-9]+(?:-[a-z0-9]+)*)\.html$")


def hoy_madrid():
    """Fecha de hoy en Madrid (los servidores de GitHub van en UTC)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.datetime.now(ZoneInfo("Europe/Madrid")).date()
    except Exception:  # Windows sin base de datos de zonas horarias
        return datetime.date.today()


def leer(archivo):
    m = NOMBRE.match(archivo.name)
    if not m:
        raise ValueError(f"{archivo.name}: el nombre debe ser AAAA-MM-DD-slug.html (minúsculas, sin tildes)")
    texto = archivo.read_text(encoding="utf-8")
    partes = texto.split("---", 2)
    if len(partes) != 3 or partes[0].strip():
        raise ValueError(f"{archivo.name}: falta la cabecera entre líneas ---")
    datos = {}
    for linea in partes[1].strip().splitlines():
        if not linea.strip():
            continue
        clave, sep, valor = linea.partition(":")
        if not sep:
            raise ValueError(f"{archivo.name}: línea de cabecera sin ':' -> {linea!r}")
        datos[clave.strip()] = valor.strip()
    faltan = [c for c in OBLIGATORIOS if not datos.get(c)]
    if faltan:
        raise ValueError(f"{archivo.name}: faltan campos {', '.join(faltan)}")
    datos["slug"] = m.group(1)
    datos["fecha"] = datetime.date.fromisoformat(datos["fecha"])
    datos["cuerpo"] = partes[2].strip()
    datos.setdefault("h1", datos["titulo"])
    datos["archivo"] = archivo.name
    return datos


def entradas(hasta=None, tratamientos=()):
    """Entradas publicadas hasta la fecha indicada (por defecto, hoy), de la más nueva a la más antigua."""
    hasta = hasta or hoy_madrid()
    todas = [leer(a) for a in sorted(CARPETA.glob("*.html"))]
    slugs = {}
    for t in todas:
        if t["slug"] in slugs:
            raise ValueError(f"Slug repetido: {t['archivo']} y {slugs[t['slug']]}")
        slugs[t["slug"]] = t["archivo"]
        if tratamientos and t["tratamiento"] not in tratamientos:
            raise ValueError(f"{t['archivo']}: tratamiento desconocido {t['tratamiento']!r}")
    publicadas = [t for t in todas if t["fecha"] <= hasta]
    publicadas.sort(key=lambda t: (t["fecha"], t["archivo"]), reverse=True)
    return publicadas, todas
