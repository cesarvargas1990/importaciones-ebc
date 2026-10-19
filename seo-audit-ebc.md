# Auditoría SEO — Importaciones EBC

Fecha: 2026-10-18  
Alcance: storefront público del proyecto local, con revisión técnica y on-page. No se modificó código.

## Resumen ejecutivo

La tienda tiene una base correcta para continuar: idioma español declarado, título principal, jerarquía de encabezados razonable, imágenes WebP, textos de intención comercial y un build de producción exitoso. El mayor riesgo SEO está en la forma de publicación: el HTML inicial solo contiene el contenedor React y el catálogo se solicita después desde `/storeadmin/api/public/catalog`. Además, no se observan en el proyecto `robots.txt`, `sitemap.xml`, canonical, meta description, Open Graph ni JSON-LD.

Estado general: **base técnica parcial; requiere ajustes de indexación antes de escalar el catálogo**.

## Prioridades principales

1. **Alta — señales básicas de indexación incompletas.** `index.html` contiene `lang`, viewport, theme-color y title, pero no meta description, canonical, robots, Open Graph ni Twitter Cards. Evidencia: `index.html:1-13`.
2. **Alta — riesgo de contenido inicial delgado.** El documento inicial solo monta `<div id="root">` y carga `src/main.jsx`; los productos, categorías y configuración llegan después mediante `fetch` a `/public/catalog`. Evidencia: `index.html:9-11` y `src/Storefront.jsx:4-10`.
3. **Alta — no hay URLs indexables para producto/categoría.** La navegación del catálogo usa botones, filtros, paginación y un modal; no se generan enlaces permanentes individuales para productos o categorías. Evidencia: `src/Storefront.jsx:16` y `src/Storefront.jsx:21`.
4. **Media — datos estructurados no implementados en el código inspeccionado.** No se observa JSON-LD de `Organization`, `WebSite`, `Product`, `Offer` o `BreadcrumbList`. Esta conclusión es del código local; la skill advierte que el HTML estático o curl no basta para descartar schema inyectado por JavaScript.
5. **Media — rendimiento del bundle.** El build produce un JS minificado de aproximadamente 708 kB y Vite emite advertencia por superar 500 kB. Esto puede afectar JavaScript execution y carga interactiva en móvil.

## Hallazgos técnicos

### 1. Metadatos incompletos

**Impacto:** Alto.  
**Evidencia:** existe `<title>Importaciones EBC | De Estados Unidos para ti</title>`, pero no description, canonical, robots ni metadata social en `index.html:3-8`.  
**Corrección:** agregar description única, canonical absoluta de `https://importacionesebc.store/`, Open Graph, Twitter Card y, si aplica, `robots` explícito. Mantener el title actual o refinarlo con la intención principal.

### 2. Renderizado dependiente de JavaScript/API

**Impacto:** Alto.  
**Evidencia:** el HTML inicial monta únicamente React (`index.html:9-11`) y el storefront consulta el catálogo después del montaje (`src/Storefront.jsx:10`, `src/Storefront.jsx:21`).  
**Corrección:** preferir prerender/SSR para la home y páginas permanentes de categoría/producto. Si se conserva SPA, generar al menos HTML estático enriquecido para home, categorías y productos prioritarios.

### 3. Arquitectura de URLs e internal linking

**Impacto:** Alto.  
**Evidencia:** las categorías se representan como `<button>` y el detalle de producto se abre en un modal; la navegación visible usa anclas internas como `#productos` y `#categorias` (`src/Storefront.jsx:21`).  
**Corrección:** crear URLs descriptivas y estables, por ejemplo `/categoria/belleza` y `/producto/slug-del-producto`, con `<a>` rastreables, canonical propia, title/H1 únicos y enlaces entre categoría, producto y home.

### 4. Sitemap y robots

**Impacto:** Alto.  
**Evidencia:** no aparecen `robots.txt` ni `sitemap.xml` entre los archivos públicos/locales inspeccionados. La comprobación pública desde este entorno no pudo completarse porque el dominio no resolvió DNS, por lo que el estado desplegado queda pendiente de verificación externa.  
**Corrección:** publicar `robots.txt` con referencia a sitemap y generar sitemap XML con solo URLs canónicas, indexables y permanentes. Registrar el sitemap en Search Console.

### 5. Schema de comercio electrónico

**Impacto:** Medio/alto.  
**Evidencia:** no se observa JSON-LD en el código inspeccionado. La skill indica que schema generado en runtime debe comprobarse con navegador renderizado o Rich Results Test, no únicamente con curl.  
**Corrección:** añadir `Organization`/`WebSite` para home, `BreadcrumbList` para jerarquía y `Product` + `Offer` en páginas de producto. No inventar disponibilidad, precio final o condiciones que no estén confirmadas por el backend.

### 6. Contenido repetitivo de producto

**Impacto:** Medio.  
**Evidencia:** `generatedDetails` genera el mismo bloque de texto para productos sin detalles propios: “es una opción seleccionada…”, “Compra acompañada” y tres viñetas (`src/Storefront.jsx:15`).  
**Corrección:** exigir descripción y detalles únicos por producto; usar el texto generado solo como fallback no indexable o enriquecerlo con atributos reales: marca, presentación, uso, compatibilidad, entrega y condiciones.

### 7. Imágenes y rendimiento visual

**Impacto:** Medio.  
**Fortalezas:** el storefront remapea PNG a WebP (`src/Storefront.jsx:7-8`) y los assets WebP locales pesan aproximadamente 60–236 kB.  
**Oportunidades:** los `<img>` principales no declaran `width`/`height`, `srcset` ni `sizes`; las imágenes de tarjetas tampoco usan lazy loading explícito. La imagen hero se aplica como background CSS.  
**Corrección:** definir dimensiones intrínsecas, usar `srcset`/`sizes`, reservar espacio para evitar CLS y aplicar lazy loading a imágenes fuera del primer viewport. Priorizar la imagen hero y el logo como recursos críticos.

### 8. Encabezados y semántica

**Impacto:** Bajo/positivo.  
**Evidencia:** se observa un H1 para el hero y una jerarquía posterior de H2/H3 (`src/Storefront.jsx:16`, `src/Storefront.jsx:21`).  
**Recomendación:** conservar esta jerarquía y revisar en cada futura página que exista un solo H1 alineado con el title y la URL.

## Lo que está bien

- `html lang="es"` está definido.
- El title actual es descriptivo y está alineado con la propuesta “De Estados Unidos para ti”.
- Hay navegación interna clara hacia productos, categorías y cómo comprar.
- Los nombres de producto se usan como `alt` en las tarjetas y detalles.
- Las imágenes locales optimizadas WebP ya están integradas.
- La salida de producción compila correctamente con Vite.
- El sitio comunica intención comercial, Colombia, envíos y contacto por WhatsApp.

## Plan priorizado

### Crítico

1. Agregar metadata técnica completa y canonical.
2. Publicar y registrar robots/sitemap.
3. Definir estrategia de páginas indexables para categorías y productos.

### Alto impacto

4. Prerenderizar o servir HTML enriquecido para las páginas SEO.
5. Añadir JSON-LD validado con Rich Results Test.
6. Reemplazar textos repetitivos por contenido propio y verificable.

### Quick wins

7. Añadir Open Graph/Twitter Card.
8. Añadir `width`, `height`, `loading` y `decoding` donde corresponda.
9. Reducir el bundle mediante code splitting de administración/WYSIWYG, que no debería cargar en la tienda pública.

### Medición

10. Configurar Search Console y Analytics.
11. Medir indexación, consultas, CTR, LCP, INP y CLS.
12. Comparar las URLs indexadas frente al catálogo activo y productos destacados.

## Límites de esta auditoría

- No se tuvo acceso a Search Console, Analytics, PageSpeed histórico ni competidores.
- El dominio público no resolvió DNS desde el entorno de auditoría, por lo que robots, sitemap, headers, SSL/HSTS y HTML realmente desplegado deben confirmarse desde una red con acceso.
- La ausencia de schema se reporta como “no observado en código local”; debe confirmarse con navegador renderizado o Rich Results Test.

