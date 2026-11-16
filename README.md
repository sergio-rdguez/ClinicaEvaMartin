# Clínica Dental Dra. Eva Martín Molina

Web de la clínica dental en Leganés, publicada con GitHub Pages en
https://www.dentalevamartinmolina.com

Es una web estática (HTML, CSS y JavaScript sin dependencias ni proceso de build).

## Estructura

```
index.html        Página principal
404.html          Página de error (también recoge enlaces de la web antigua de Wix)
css/styles.css    Estilos (paleta y tipografía en las variables de :root)
js/main.js        Menú móvil, estado "abierto/cerrado", mapa bajo demanda
assets/img/       Logo y fotos de la clínica
CNAME             Dominio propio para GitHub Pages
robots.txt, sitemap.xml
```

## Ver en local

```bash
python -m http.server 8080
```

Y abrir http://localhost:8080

## Cambios habituales

- **Horario**: se cambia en dos sitios: la tabla de `index.html` (sección `#contacto`)
  y el objeto `schedule` de `js/main.js` (minutos desde las 00:00).
- **Teléfono / email / dirección**: buscar `916806724`, `draevamartin@gmail.com` o
  `Reina Sofía` en `index.html` (incluye el bloque JSON-LD de la cabecera, que usa Google).
- **Tratamientos**: cada uno es un `<li class="treat">` dentro de `#tratamientos`.

## Publicar en GitHub Pages

1. En el repositorio: **Settings → Pages → Build and deployment**
   - Source: *Deploy from a branch*
   - Branch: `main` / `(root)`
2. En **Custom domain** escribir `www.dentalevamartinmolina.com` y guardar.
3. Cuando el certificado esté listo, marcar **Enforce HTTPS**.

## DNS del dominio

En el panel donde esté gestionado el dominio (si se compró con Wix, en
Wix → Dominios → Registros DNS), quitar los registros que apuntan a Wix y crear:

| Tipo  | Nombre | Valor                    |
|-------|--------|--------------------------|
| CNAME | www    | sergio-rdguez.github.io  |
| A     | @      | 185.199.108.153          |
| A     | @      | 185.199.109.153          |
| A     | @      | 185.199.110.153          |
| A     | @      | 185.199.111.153          |
| AAAA  | @      | 2606:50c0:8000::153      |
| AAAA  | @      | 2606:50c0:8001::153      |
| AAAA  | @      | 2606:50c0:8002::153      |
| AAAA  | @      | 2606:50c0:8003::153      |

Los cambios de DNS pueden tardar desde minutos hasta 24–48 h en propagarse.
