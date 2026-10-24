from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.utils import ImageReader

ROOT = Path('/Users/cesaraugustovargas/Documents/Documentos Cesar/estefani')
OUT = ROOT / 'output/pdf/manual-usuario-importaciones-ebc.pdf'
ASSETS = ROOT / 'public'

NAVY = colors.HexColor('#071b3a')
BLUE = colors.HexColor('#173a69')
RED = colors.HexColor('#e74343')
GREEN = colors.HexColor('#1f9d63')
INK = colors.HexColor('#17233d')
MUTED = colors.HexColor('#66758e')
PALE = colors.HexColor('#f5f7fb')
LINE = colors.HexColor('#dfe5ee')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=30, leading=34, textColor=colors.white, alignment=TA_LEFT, spaceAfter=10))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['BodyText'], fontName='Helvetica', fontSize=13, leading=18, textColor=colors.HexColor('#dce8f8')))
styles.add(ParagraphStyle(name='H1EBC', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=23, leading=27, textColor=NAVY, spaceBefore=2, spaceAfter=8))
styles.add(ParagraphStyle(name='H2EBC', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=BLUE, spaceBefore=9, spaceAfter=5))
styles.add(ParagraphStyle(name='BodyEBC', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.7, leading=14, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name='SmallEBC', parent=styles['BodyText'], fontName='Helvetica', fontSize=8, leading=11, textColor=MUTED))
styles.add(ParagraphStyle(name='Callout', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=BLUE))
styles.add(ParagraphStyle(name='CenterSmall', parent=styles['SmallEBC'], alignment=TA_CENTER))

def P(text, style='BodyEBC'):
    return Paragraph(text, styles[style])

def bullet(text):
    return P(f'<font color="#e74343">●</font> &nbsp;{text}', 'BodyEBC')

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page > 1:
        canvas.setFillColor(NAVY); canvas.rect(0, h-12*mm, w, 12*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white); canvas.setFont('Helvetica-Bold', 8); canvas.drawString(16*mm, h-8*mm, 'IMPORTACIONES EBC  |  MANUAL DE USUARIO')
    canvas.setFillColor(MUTED); canvas.setFont('Helvetica', 7.5); canvas.drawString(16*mm, 9*mm, 'Uso interno del equipo de tienda  ·  importacionesebc.store')
    canvas.drawRightString(w-16*mm, 9*mm, f'{doc.page}')
    canvas.restoreState()

def panel_mock(title, items, width=175*mm, height=74*mm, highlight=None):
    data = [[P('<b>IMPORTACIONES<br/>EBC</b>', 'SmallEBC'), P(f'<b>{title}</b>', 'H2EBC')]]
    table = Table(data, colWidths=[38*mm, width-38*mm], rowHeights=[15*mm])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),NAVY),('BACKGROUND',(1,0),(1,0),colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('BOX',(0,0),(-1,-1),0.7,LINE)]))
    rows = []
    for label, detail, action in items:
        bg = colors.HexColor('#fff2f2') if action == 'Inactivar' else colors.white
        rows.append([P(f'<b>{label}</b><br/><font color="#66758e">{detail}</font>', 'SmallEBC'), P(f'<font color="#173a69"><b>{action}</b></font>', 'SmallEBC')])
    body = Table(rows, colWidths=[width-42*mm, 42*mm], rowHeights=[11*mm]*len(rows))
    body.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,colors.HexColor('#fbfcfe')]),('GRID',(0,0),(-1,-1),0.35,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7)]))
    return [table, body]

def field_table(rows):
    t = Table([[P(f'<b>{a}</b>', 'SmallEBC'), P(b, 'SmallEBC')] for a,b in rows], colWidths=[43*mm, 125*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#eef3fa')),('GRID',(0,0),(-1,-1),0.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def image(path, width, height=None):
    if not Path(path).exists(): return Spacer(width, 4)
    im = Image(str(path), width=width, height=height or width*0.62, kind='proportional')
    return im

story = []

# Cover
cover = Table([[P('MANUAL DE USUARIO', 'CoverSub')], [P('Administra tu tienda<br/>Importaciones EBC', 'CoverTitle')], [P('Guía práctica para parametrizar categorías, productos, imágenes, precios y configuración comercial.', 'CoverSub')]], colWidths=[174*mm])
cover.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),NAVY),('LEFTPADDING',(0,0),(-1,-1),15*mm),('RIGHTPADDING',(0,0),(-1,-1),15*mm),('TOPPADDING',(0,0),(-1,0),13*mm),('TOPPADDING',(0,1),(-1,1),5*mm),('TOPPADDING',(0,2),(-1,2),3*mm),('BOTTOMPADDING',(0,-1),(-1,-1),15*mm)]))
story += [Spacer(1, 24*mm), image(ASSETS/'logo.webp', 48*mm, 28*mm), Spacer(1, 10*mm), cover, Spacer(1, 8*mm), image(ASSETS/'hero.webp', 174*mm, 78*mm), Spacer(1, 8*mm), P('<b>Panel administrativo:</b> https://importacionesebc.store/admin<br/><b>Tienda pública:</b> https://importacionesebc.store', 'CenterSmall'), PageBreak()]

# Access
story += [P('1. Antes de empezar', 'H1EBC'), P('Este manual está dirigido a la persona encargada de mantener el catálogo y la información comercial de Importaciones EBC.', 'BodyEBC'), P('Credenciales de acceso', 'H2EBC'), bullet('El administrador debe recibir por correo el correo autorizado y la contraseña temporal o definida para el panel.'), bullet('En el formulario, escribe el correo en <b>Correo</b> y la contraseña en <b>Contraseña</b>; luego selecciona <b>Ingresar</b>.'), bullet('No compartas la contraseña por WhatsApp ni la incluyas en documentos públicos. Si se pierde, solicita un reinicio al responsable de la tienda.'), Spacer(1, 5*mm)]
login = Table([[P('<font color="#e74343"><b>IMPORTACIONES EBC</b></font><br/><br/><font size="16"><b>Administrar tienda</b></font><br/><font color="#66758e">Ingresa para editar el catálogo y la configuración.</font><br/><br/><font color="#66758e">Correo</font><br/><font backColor="#fff8d6">correo autorizado</font><br/><br/><font color="#66758e">Contraseña</font><br/><font backColor="#fff8d6">••••••••••••</font><br/><br/><font color="#ffffff" backColor="#071b3a"><b>Ingresar</b></font>', 'BodyEBC')]], colWidths=[82*mm])
login.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.white),('BOX',(0,0),(-1,-1),0.8,LINE),('ROUNDEDCORNERS',[8,8,8,8]),('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12)]))
story += [login, Spacer(1, 5*mm), P('<b>Importante:</b> la tienda pública y el panel son enlaces distintos. El cliente visita la tienda; el equipo administra desde el panel.', 'Callout'), PageBreak()]

# Overview
story += [P('2. Conoce el panel', 'H1EBC'), P('Después de ingresar, verás un menú lateral. La cantidad junto a cada opción indica cuántas categorías o productos están registrados.', 'BodyEBC')]
overview = Table([[P('<b>MENÚ LATERAL</b>', 'SmallEBC'), P('<b>¿Para qué sirve?</b>', 'SmallEBC')], [P('Resumen', 'BodyEBC'), P('Revisa cantidades de categorías, productos y destacados.', 'BodyEBC')], [P('Categorías', 'BodyEBC'), P('Crea, edita, busca, ordena, activa o inactiva categorías.', 'BodyEBC')], [P('Productos', 'BodyEBC'), P('Crea, edita precios, imágenes, disponibilidad y productos destacados.', 'BodyEBC')], [P('Configuración', 'BodyEBC'), P('Actualiza textos, logo, imagen principal y datos de WhatsApp.', 'BodyEBC')]], colWidths=[42*mm,126*mm])
overview.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),0.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
story += [overview, Spacer(1, 6*mm), P('Regla general de guardado', 'H2EBC'), bullet('Completa los campos obligatorios.'), bullet('Revisa la imagen, el estado y el orden antes de guardar.'), bullet('Después de guardar, confirma que el registro aparece en el listado y revisa la tienda pública.'), Spacer(1, 4*mm), P('<b>Ruta rápida:</b> Categorías → crear o editar categoría → Productos → crear o editar productos → Configuración → guardar textos y WhatsApp.', 'Callout'), PageBreak()]

# Categories
story += [P('3. Gestionar categorías', 'H1EBC'), P('Las categorías organizan el catálogo y permiten que el cliente filtre los productos desde la tienda pública.', 'BodyEBC'), P('Crear una categoría', 'H2EBC'), bullet('Entra a <b>Categorías</b> y pulsa <b>+ Nueva categoría</b>.'), bullet('Escribe el nombre, una descripción corta, el orden y, si corresponde, una imagen.'), bullet('Pulsa <b>Guardar cambios</b> y verifica que aparece en el listado.'), Spacer(1, 3*mm)]
story += panel_mock('Categorías', [('Ariana Grande','Fragancias y body mist · 2 productos','Editar'),('Bath and Body Works','Cuidado corporal y fragancias · 8 productos','Inactivar'),('Vitaminas','Suplementos y bienestar · 21 productos','Editar')])
story += [Spacer(1, 5*mm), P('Activar o inactivar una categoría', 'H2EBC'), bullet('<b>Inactivar:</b> la categoría deja de mostrarse en la tienda y también se inactivan sus productos activos.'), bullet('<b>Activar:</b> vuelve a habilitar la categoría, pero no reactiva automáticamente todos sus productos.'), bullet('Si activas un producto de una categoría inactiva, el sistema habilita esa categoría y solamente el producto seleccionado.'), P('<b>Consejo:</b> usa la búsqueda y el contador de productos para comprobar que estás trabajando sobre la categoría correcta.', 'Callout'), PageBreak()]

# Products
story += [P('4. Gestionar productos', 'H1EBC'), P('Desde <b>Productos</b> puedes mantener la información que el cliente verá en el catálogo.', 'BodyEBC'), P('Campos del producto', 'H2EBC'), field_table([('Nombre','Nombre comercial visible en el catálogo.'),('Categoría','Define dónde aparecerá el producto.'),('Precio COP','Precio actual en pesos colombianos.'),('Precio anterior','Opcional. Debe ser mayor que el precio actual para mostrar una rebaja.'),('Etiqueta','Ejemplos: Nuevo, Oferta.'),('SKU','Código interno de referencia.'),('Stock opcional','Cantidad disponible, si la controlas.'),('Descripción','Texto corto para la tarjeta del producto.'),('Detalles','Ficha ampliada con formato y contenido adicional.'),('Orden','Posición relativa dentro del catálogo.')]), Spacer(1, 5*mm), P('Estados y destacados', 'H2EBC'), bullet('<b>Activo:</b> el producto puede aparecer en el catálogo.'), bullet('<b>Disponible:</b> controla si puede mostrarse como disponible para la tienda.'), bullet('<b>Destacado:</b> lo incluye en la sección de selección de la tienda.'), bullet('Para reactivar un producto de una categoría deshabilitada, pulsa <b>Activar</b> en ese producto. Se habilitarán solo la categoría y ese producto.'), PageBreak()]

# Images and prices
story += [P('5. Imágenes, precios y detalles', 'H1EBC'), P('Imágenes', 'H2EBC'), bullet('Usa JPG, PNG o WEBP. El panel optimiza la imagen antes de cargarla.'), bullet('Se recomienda una imagen nítida, con el producto centrado y fondo limpio.'), bullet('Para reemplazarla, entra a <b>Editar</b>, selecciona una nueva imagen y guarda.'), Spacer(1, 3*mm), Image(str(ASSETS/'category-belleza.webp'), width=38*mm, height=24*mm), Spacer(1, 4*mm), P('Regla de precios', 'H2EBC'), bullet('Si solo tienes un precio, llena <b>Precio COP</b> y deja vacío <b>Precio anterior</b>.'), bullet('Si muestras una promoción, el precio anterior debe ser numéricamente mayor. Ejemplo: anterior $150.000 y actual $120.000.'), bullet('No uses el precio anterior para guardar costos internos; es visible para el cliente.'), P('Detalles del producto', 'H2EBC'), bullet('Escribe beneficios, características y recomendaciones claras.'), bullet('Usa títulos, negrita, listas y enlaces solo cuando aporten información útil.'), bullet('Evita promesas no verificadas o información que no puedas confirmar.'), PageBreak()]

# Configuration/store
story += [P('6. Configuración y tienda pública', 'H1EBC'), P('En <b>Configuración</b> puedes actualizar la comunicación de la tienda.', 'BodyEBC'), field_table([('Nombre de la tienda','Nombre visible en encabezados y metadatos.'),('Texto superior','Aviso corto, por ejemplo envíos y atención por WhatsApp.'),('Título y descripción del hero','Mensaje principal de la portada.'),('Logo e imagen principal','Elementos visuales de marca.'),('Número de WhatsApp','Número con código de país, solo dígitos.'),('Mensaje base','Texto que acompaña el pedido enviado por WhatsApp.'),('Saludo inicial','Mensaje de bienvenida para consultas.'),('Aviso de precios','Nota sobre disponibilidad, envío y valor final.'),('Instrucciones de compra','Explica que la confirmación se realiza por WhatsApp.')]), Spacer(1, 5*mm), P('La tienda pública', 'H2EBC'), P('El cliente visita <b>https://importacionesebc.store</b>. Allí puede explorar categorías, buscar productos, ver detalles, agregar al carrito y enviar el pedido por WhatsApp. No se realizan pagos en línea desde este sitio.', 'BodyEBC'), image(ASSETS/'hero.webp', 168*mm, 74*mm), PageBreak()]

# Routine/troubleshooting
story += [P('7. Flujo recomendado y solución de problemas', 'H1EBC'), P('Flujo diario', 'H2EBC'), bullet('1. Ingresa al panel con las credenciales recibidas por correo.'), bullet('2. Revisa primero categorías activas y luego productos activos/disponibles.'), bullet('3. Crea o edita categorías antes de crear productos nuevos.'), bullet('4. Carga imágenes, revisa precios y define si el producto es destacado.'), bullet('5. Guarda y revisa la tienda pública en una pestaña nueva.'), bullet('6. Haz una prueba de búsqueda, carrito y enlace de WhatsApp.'), Spacer(1, 5*mm), P('Si algo no aparece', 'H2EBC'), bullet('Confirma que la categoría esté activa.'), bullet('Confirma que el producto esté activo y disponible.'), bullet('Revisa que el producto tenga la categoría correcta.'), bullet('Recarga la página con <b>Ctrl + Shift + R</b> o <b>Cmd + Shift + R</b> si acabas de recibir una actualización.'), bullet('Si el problema continúa, anota el nombre del producto/categoría y envía una captura al responsable técnico.'), Spacer(1, 7*mm), P('<b>Enlaces importantes</b>', 'H2EBC'), P('Panel administrativo: https://importacionesebc.store/admin<br/>Tienda pública: https://importacionesebc.store', 'BodyEBC'), Spacer(1, 10*mm), P('Última recomendación: cambia la contraseña si la cuenta es compartida o si sospechas que fue expuesta.', 'Callout')]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=19*mm, bottomMargin=17*mm, title='Manual de usuario - Importaciones EBC', author='Importaciones EBC')
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
