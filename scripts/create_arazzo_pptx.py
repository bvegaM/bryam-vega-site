from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Color palette ──────────────────────────────────────────────────────────────
C_BG        = RGBColor(0x0D, 0x1B, 0x2A)   # dark navy
C_SURFACE   = RGBColor(0x11, 0x28, 0x40)   # slightly lighter navy
C_ACCENT    = RGBColor(0x00, 0xC2, 0xFF)   # cyan accent
C_ACCENT2   = RGBColor(0x00, 0xFF, 0xC8)   # mint green
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_SOFT      = RGBColor(0xA0, 0xB8, 0xD0)   # muted blue-grey
C_CARD      = RGBColor(0x16, 0x32, 0x52)   # card bg
C_YELLOW    = RGBColor(0xFF, 0xD6, 0x00)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]   # completely blank


def add_slide():
    return prs.slides.add_slide(BLANK)


def bg(slide, color=C_BG):
    """Fill slide background."""
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def box(slide, l, t, w, h, color, radius=False):
    """Add a filled rectangle."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.RECTANGLE
        Inches(l), Inches(t), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def txt(slide, text, l, t, w, h,
        size=20, bold=False, color=C_WHITE,
        align=PP_ALIGN.LEFT, italic=False, wrap=True):
    """Add a text box."""
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb


def txt_multi(slide, lines, l, t, w, h, size=18, color=C_WHITE):
    """Add a text box with multiple paragraphs from a list of (text, bold, color) tuples."""
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        if isinstance(item, str):
            text, bold, col = item, False, color
        else:
            text, bold, col = item[0], item[1], item[2] if len(item) > 2 else color
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = col
    return txb


def accent_bar(slide, top=0.55, height=0.06, color=C_ACCENT):
    """Thin horizontal accent bar."""
    bar = slide.shapes.add_shape(1, Inches(0), Inches(top), Inches(13.33), Inches(height))
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()


def slide_number(slide, n, total=16):
    txt(slide, f"{n} / {total}", 12.0, 7.1, 1.2, 0.35,
        size=11, color=C_SOFT, align=PP_ALIGN.RIGHT)


def footer_logo(slide):
    txt(slide, "Bryam Vega · Thoughtworks", 0.3, 7.1, 4, 0.35,
        size=11, color=C_SOFT)


def card_box(slide, l, t, w, h, title, body_lines, title_color=C_ACCENT):
    """Render a card with title + bullet lines."""
    box(slide, l, t, w, h, C_CARD)
    # top accent strip
    strip = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(0.05))
    strip.fill.solid()
    strip.fill.fore_color.rgb = title_color
    strip.line.fill.background()
    txt(slide, title, l + 0.15, t + 0.1, w - 0.3, 0.4,
        size=15, bold=True, color=title_color)
    body_t = t + 0.55
    for line in body_lines:
        txt(slide, f"  {line}", l + 0.15, body_t, w - 0.3, 0.38,
            size=13, color=C_WHITE)
        body_t += 0.38


def code_box(slide, code_lines, l, t, w, h):
    """Monospaced code block."""
    box(slide, l, t, w, h, RGBColor(0x08, 0x12, 0x1E))
    border = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    border.fill.background()
    border.line.color.rgb = C_ACCENT
    border.line.width = Pt(0.75)
    txb = slide.shapes.add_textbox(Inches(l + 0.15), Inches(t + 0.15),
                                   Inches(w - 0.3), Inches(h - 0.3))
    txb.word_wrap = False
    tf = txb.text_frame
    tf.word_wrap = False
    first = True
    for line in code_lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.size = Pt(11)
        run.font.name = "Courier New"
        run.font.color.rgb = C_ACCENT2


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — PORTADA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)

# left gradient panel
grad = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(5.5), Inches(7.5))
grad.fill.solid()
grad.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
grad.line.fill.background()

# accent vertical bar
bar = s.shapes.add_shape(1, Inches(5.5), Inches(0), Inches(0.08), Inches(7.5))
bar.fill.solid()
bar.fill.fore_color.rgb = C_ACCENT
bar.line.fill.background()

txt(s, "De contratos aislados", 0.4, 1.2, 5.0, 1.0, size=30, bold=True, color=C_WHITE)
txt(s, "a flujos orquestados", 0.4, 2.1, 5.0, 0.9, size=30, bold=True, color=C_ACCENT)
txt(s, "Arazzo y el futuro de la gobernanza de APIs", 0.4, 3.1, 5.0, 0.8, size=17, color=C_SOFT)

# right side tags
for i, tag in enumerate(["#Arazzo", "#OpenAPI", "#APIGovernance", "#Workflows"]):
    txt(s, tag, 6.0, 1.5 + i * 0.6, 3.0, 0.5, size=16, color=C_ACCENT2)

txt(s, "Bryam David Vega Moreno", 6.0, 5.5, 5.5, 0.5, size=14, bold=True, color=C_WHITE)
txt(s, "Senior Consultant · Thoughtworks", 6.0, 5.95, 5.5, 0.4, size=13, color=C_SOFT)
txt(s, "Apidays New York 2026", 6.0, 6.4, 5.5, 0.4, size=12, color=C_YELLOW)

slide_number(s, 1)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — EL PROBLEMA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)

txt(s, "El problema que todos tenemos,", 0.5, 0.7, 12, 0.7, size=28, bold=True, color=C_WHITE)
txt(s, "pero pocos pueden nombrar", 0.5, 1.35, 12, 0.6, size=28, bold=True, color=C_ACCENT)

quote_box = s.shapes.add_shape(1, Inches(0.5), Inches(2.1), Inches(12.3), Inches(1.5))
quote_box.fill.solid()
quote_box.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
quote_box.line.color.rgb = C_ACCENT
quote_box.line.width = Pt(1.5)

txt(s, '"El problema no es que no tengamos buenos contratos de API;\n'
       'el problema es que los contratos no hablan entre sí."',
    0.8, 2.2, 11.8, 1.2, size=18, italic=True, color=C_WHITE)

txt(s, "— Frank Kilcommins · OpenAPI Initiative · Apidays New York 2026",
    0.8, 3.55, 12, 0.4, size=12, color=C_SOFT)

txt(s, "OpenAPI describe perfectamente cada endpoint.", 0.5, 4.15, 12, 0.45, size=15, color=C_WHITE)
txt(s, "Pero no dice nada de lo que ocurre  antes  ni  después.", 0.5, 4.55, 12, 0.45, size=15, color=C_SOFT)

footer_logo(s)
slide_number(s, 2)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — LOS 4 PATRONES DEL PROBLEMA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "A escala, el problema se manifiesta en 4 patrones", 0.5, 0.65, 12, 0.55, size=22, bold=True, color=C_WHITE)

cards = [
    ("01  Fragmentación", ["El flujo de negocio vive en Slack,", "wikis o en el código del consumidor."]),
    ("02  Testing frágil", ["Cada equipo construye su propio", "harness de prueba desde cero."]),
    ("03  Breaking changes invisibles", ["Un campo renombrado rompe el", "flujo en producción sin que nadie lo detecte."]),
    ("04  Duplicación por consumidor", ["10 consumidores = 10 versiones", "del mismo flujo, 10 interpretaciones."]),
]
colors = [C_ACCENT, C_ACCENT2, C_YELLOW, RGBColor(0xFF, 0x6B, 0x6B)]
positions = [(0.35, 1.4), (6.85, 1.4), (0.35, 4.2), (6.85, 4.2)]

for (title, lines), color, (l, t) in zip(cards, colors, positions):
    card_box(s, l, t, 6.2, 2.6, title, lines, title_color=color)

footer_logo(s)
slide_number(s, 3)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — QUÉ ES ARAZZO
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "¿Qué es Arazzo?", 0.5, 0.65, 12, 0.6, size=28, bold=True, color=C_WHITE)

# Big definition box
def_box = s.shapes.add_shape(1, Inches(0.5), Inches(1.5), Inches(12.3), Inches(1.4))
def_box.fill.solid()
def_box.fill.fore_color.rgb = C_SURFACE
def_box.line.color.rgb = C_ACCENT
def_box.line.width = Pt(1.5)

txt(s, "Especificación abierta del OpenAPI Initiative que describe workflows:", 0.75, 1.6, 12, 0.5, size=16, color=C_SOFT)
txt(s, "secuencias orquestadas de llamadas a APIs con sus dependencias,\n"
       "flujo de datos entre pasos y condiciones de éxito o falla.",
    0.75, 2.05, 11.8, 0.75, size=17, bold=True, color=C_WHITE)

txt(s, "La idea central:", 0.5, 3.15, 4, 0.45, size=15, color=C_SOFT)

box(s, 0.5, 3.6, 5.8, 0.85, RGBColor(0x00, 0x3A, 0x6B))
txt(s, "OpenAPI  →  el QUÉ de cada endpoint", 0.7, 3.68, 5.4, 0.6, size=17, bold=True, color=C_WHITE)

box(s, 7.0, 3.6, 5.8, 0.85, RGBColor(0x00, 0x3A, 0x6B))
txt(s, "Arazzo  →  el CÓMO de los flujos", 7.2, 3.68, 5.4, 0.6, size=17, bold=True, color=C_ACCENT)

arrow = s.shapes.add_shape(5, Inches(6.35), Inches(3.85), Inches(0.6), Inches(0.35))
arrow.fill.solid()
arrow.fill.fore_color.rgb = C_ACCENT2
arrow.line.fill.background()

for i, item in enumerate([
    ("Flujo de datos entre pasos", C_ACCENT),
    ("Condiciones de éxito explícitas", C_ACCENT2),
    ("Retry, salto, abort declarativos", C_WHITE),
    ("Orquestación multi-API", C_WHITE),
    ("Componentes reutilizables", C_WHITE),
]):
    col_offset = (i % 3) * 4.3
    row_offset = (i // 3) * 0.65
    txt(s, f"✓  {item[0]}", 0.5 + col_offset, 4.75 + row_offset, 4.1, 0.55,
        size=14, color=item[1])

footer_logo(s)
slide_number(s, 4)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — ESTRUCTURA DE ARAZZO
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "Anatomía de un archivo Arazzo", 0.5, 0.65, 12, 0.6, size=26, bold=True, color=C_WHITE)

components = [
    ("info", "Metadatos: título, versión, descripción.", C_SOFT),
    ("sourceDescriptions", "Lista de contratos OpenAPI/AsyncAPI que el workflow invoca.", C_ACCENT),
    ("workflows", "El corazón. Uno o varios flujos en el mismo archivo.", C_ACCENT2),
    ("  inputs", "Datos de entrada que el workflow recibe.", C_WHITE),
    ("  steps ( * )", "Cada llamada individual. Usa operationId o workflowId.", C_WHITE),
    ("  successCriteria", "Condición que valida el paso ($statusCode, JSONPath…).", C_WHITE),
    ("  outputs", "Valores que el workflow expone al exterior.", C_WHITE),
    ("components", "Parámetros, actions e inputs reutilizables.", C_YELLOW),
]

for i, (name, desc, color) in enumerate(components):
    row_t = 1.5 + i * 0.65
    indent = 0.5 if name.startswith("  ") else 0
    box(s, 0.4 + indent, row_t, 3.2 - indent, 0.52, C_CARD)
    txt(s, name.strip(), 0.6 + indent, row_t + 0.06, 3.0, 0.42, size=13, bold=True, color=color)
    txt(s, desc, 3.8, row_t + 0.06, 8.8, 0.42, size=13, color=C_WHITE)

footer_logo(s)
slide_number(s, 5)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — LO QUE HABILITA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "Lo que Arazzo hace posible", 0.5, 0.65, 12, 0.6, size=26, bold=True, color=C_WHITE)

items = [
    ("Documentación del flujo como artefacto de primera clase",
     "Versionado, revisable en un PR, con el mismo ciclo de vida que el contrato OpenAPI.",
     C_ACCENT),
    ("Testing de integración generado desde la especificación",
     "El archivo Arazzo define el flujo con suficiente precisión para ejecutarlo directamente. El flujo es el test.",
     C_ACCENT2),
    ("Detección de breaking changes en secuencias",
     "Si un campo referenciado en $steps.create-order.outputs cambia, la toolchain detecta que el flujo se rompe.",
     C_YELLOW),
    ("Reutilización canónica entre consumidores",
     "El equipo productor publica el Arazzo junto al OpenAPI. Un solo flujo, todos los consumidores.",
     RGBColor(0xFF, 0x6B, 0x6B)),
]

for i, (title, body, color) in enumerate(items):
    t = 1.5 + i * 1.45
    # number circle
    circ = s.shapes.add_shape(9, Inches(0.35), Inches(t + 0.2), Inches(0.55), Inches(0.55))
    circ.fill.solid()
    circ.fill.fore_color.rgb = color
    circ.line.fill.background()
    txt(s, str(i + 1), 0.35, t + 0.2, 0.55, 0.55, size=14, bold=True,
        color=C_BG, align=PP_ALIGN.CENTER)
    txt(s, title, 1.1, t + 0.1, 11.5, 0.45, size=15, bold=True, color=color)
    txt(s, body, 1.1, t + 0.55, 11.5, 0.65, size=13, color=C_SOFT)

footer_logo(s)
slide_number(s, 6)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — DEMO: ARQUITECTURA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "Demo: Sistema de tarjetas de crédito con Arazzo", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)
txt(s, "gitlab.com/api-labs1/api-arazzo/api-workflows", 0.5, 1.2, 12, 0.4, size=13, color=C_ACCENT)

# Architecture diagram
# FE box
box(s, 0.4, 2.0, 2.8, 1.2, RGBColor(0x00, 0x3A, 0x6B))
txt(s, "Frontend (FE)", 0.4, 2.1, 2.8, 0.4, size=14, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)
txt(s, "Consumer / Canal", 0.4, 2.5, 2.8, 0.5, size=12, color=C_SOFT, align=PP_ALIGN.CENTER)

# Arrow FE → BFF
txt(s, "→", 3.3, 2.4, 0.6, 0.4, size=22, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)

# BFF box
box(s, 4.0, 2.0, 2.8, 1.2, RGBColor(0x00, 0x3A, 0x6B))
txt(s, "BFF Loyalty", 4.0, 2.1, 2.8, 0.4, size=14, bold=True, color=C_ACCENT2, align=PP_ALIGN.CENTER)
txt(s, "bff-loyalty-financial\n-information.yaml", 4.0, 2.5, 2.8, 0.6, size=11, color=C_SOFT, align=PP_ALIGN.CENTER)

# Arrow BFF → BL
txt(s, "→", 6.9, 2.4, 0.6, 0.4, size=22, bold=True, color=C_ACCENT, align=PP_ALIGN.CENTER)

# BL box
box(s, 7.6, 2.0, 2.8, 1.2, RGBColor(0x00, 0x3A, 0x6B))
txt(s, "BL Loyalty", 7.6, 2.1, 2.8, 0.4, size=14, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
txt(s, "bl-loyalty-financial\n-information.yaml", 7.6, 2.5, 2.8, 0.6, size=11, color=C_SOFT, align=PP_ALIGN.CENTER)

# Arrow BFF → Arazzo
txt(s, "↕ Arazzo", 4.0, 3.3, 2.8, 0.4, size=12, color=C_ACCENT, align=PP_ALIGN.CENTER)

# 8 workflows table
txt(s, "8 Workflows organizados en 3 grupos:", 0.5, 3.85, 12, 0.45, size=15, bold=True, color=C_WHITE)

groups = [
    ("Consumer Journeys (FE)", "Tarjetas → beneficios  ·  Tarjetas → descuentos", C_ACCENT),
    ("Consumer Workflows (FE)", "Obtener tarjetas  ·  Obtener beneficios  ·  Obtener descuentos", C_ACCENT2),
    ("BFF Internal (BFF → BL)", "Delegar tarjetas  ·  Delegar beneficios  ·  Delegar descuentos", C_YELLOW),
]

for i, (group, workflows, color) in enumerate(groups):
    t = 4.45 + i * 0.9
    box(s, 0.4, t, 3.5, 0.75, C_CARD)
    txt(s, group, 0.6, t + 0.12, 3.2, 0.5, size=13, bold=True, color=color)
    txt(s, workflows, 4.1, t + 0.12, 8.8, 0.5, size=13, color=C_WHITE)

footer_logo(s)
slide_number(s, 7)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — DEMO: JOURNEY 1 (TARJETAS → BENEFICIOS)
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, C_ACCENT2)
txt(s, "Consumer Journey 1 — Tarjetas → Beneficios", 0.5, 0.65, 12.5, 0.6, size=22, bold=True, color=C_WHITE)
txt(s, "El card_id del paso 1 se propaga automáticamente al paso 2", 0.5, 1.2, 12, 0.4, size=14, color=C_SOFT)

code_box(s, [
    "- workflowId: consumer-browse-card-benefits",
    "  steps:",
    "    - stepId: get-credit-cards",
    "      operationId: bff-loyalty-financial-information.getCustomerCreditCards",
    "      successCriteria:",
    "        - condition: $statusCode == 200",
    "      onFailure:",
    "        - name: get-credit-cards-failed",
    "          type: end",
    "      outputs:",
    "        first_card_id: $response.body#/credit_cards/0/card_id   # ← extrae el ID",
    "",
    "    - stepId: get-benefits-for-selected-card",
    "      dependsOn: [get-credit-cards]",
    "      operationId: bff-loyalty-financial-information.getCardBenefits",
    "      parameters:",
    "        - name: card_id",
    "          in: path",
    "          value: $steps.get-credit-cards.outputs.first_card_id   # ← lo usa aquí",
    "      outputs:",
    "        benefits: $response.body#/benefits",
], 0.4, 1.7, 12.5, 5.6)

footer_logo(s)
slide_number(s, 8)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — DEMO: JOURNEY 2 (TARJETAS → DESCUENTOS)
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, C_YELLOW)
txt(s, "Consumer Journey 2 — Tarjetas → Descuentos", 0.5, 0.65, 12.5, 0.6, size=22, bold=True, color=C_WHITE)
txt(s, "Idéntico en el primer paso — solo cambia la operación del segundo step",
    0.5, 1.2, 12, 0.4, size=14, color=C_SOFT)

code_box(s, [
    "- workflowId: consumer-browse-card-discounts",
    "  steps:",
    "    - stepId: get-credit-cards",
    "      operationId: bff-loyalty-financial-information.getCustomerCreditCards",
    "      outputs:",
    "        first_card_id: $response.body#/credit_cards/0/card_id",
    "",
    "    - stepId: get-discounts-for-selected-card",
    "      dependsOn: [get-credit-cards]",
    "      operationId: bff-loyalty-financial-information.getCardDiscounts",
    "      parameters:",
    "        - name: card_id",
    "          in: path",
    "          value: $steps.get-credit-cards.outputs.first_card_id",
    "      outputs:",
    "        discounts: $response.body#/discounts",
], 0.4, 1.7, 12.5, 4.8)

insight_box = s.shapes.add_shape(1, Inches(0.4), Inches(6.6), Inches(12.5), Inches(0.72))
insight_box.fill.solid()
insight_box.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
insight_box.line.color.rgb = C_YELLOW
insight_box.line.width = Pt(1.2)
txt(s, "⚡  Esa repetición del primer paso existía implícitamente en cada consumidor por separado."
       " Arazzo la hace visible, nombrada y canónica.",
    0.65, 6.68, 12.1, 0.55, size=13, color=C_WHITE)

footer_logo(s)
slide_number(s, 9)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — DEMO: RETRY
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, RGBColor(0xFF, 0x6B, 0x6B))
txt(s, "Retry declarativo en la especificación", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)
txt(s, "Workflow: consumer-get-credit-cards — sin código de retry en el cliente",
    0.5, 1.2, 12, 0.4, size=14, color=C_SOFT)

code_box(s, [
    "onFailure:",
    "  - name: bff-credit-cards-retry",
    "    type: retry",
    "    retryAfter: 1        # segundos de espera",
    "    retryLimit: 3        # máximo de intentos",
    "    criteria:",
    "      - condition: $statusCode >= 400",
    "        type: simple",
    "  - name: bff-credit-cards-failed",
    "    type: end",
], 0.4, 1.75, 6.2, 4.0)

txt(s, "Lo que esto significa:", 7.0, 1.75, 5.8, 0.45, size=15, bold=True, color=C_WHITE)

points = [
    ("Retry = parte del contrato", "No del cliente, no del SDK.", C_ACCENT2),
    ("3 intentos con 1s de espera", "Cualquier runtime compatible lo respeta.", C_ACCENT),
    ("Si todos fallan → type: end", "El flujo termina limpiamente.", C_YELLOW),
    ("Visible en governance", "Aparece en el PR, en el diff, en el lint.", RGBColor(0xFF, 0x6B, 0x6B)),
]

for i, (title, body, color) in enumerate(points):
    t = 2.3 + i * 1.2
    box(s, 7.0, t, 5.8, 1.0, C_CARD)
    txt(s, title, 7.2, t + 0.08, 5.4, 0.42, size=14, bold=True, color=color)
    txt(s, body, 7.2, t + 0.5, 5.4, 0.38, size=12, color=C_SOFT)

footer_logo(s)
slide_number(s, 10)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — DEMO: BFF INTERNO
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, C_YELLOW)
txt(s, "Los workflows internos del BFF", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)
txt(s, "Cómo el BFF delega cada solicitud a la capa de negocio — documentado en Arazzo",
    0.5, 1.2, 12, 0.4, size=14, color=C_SOFT)

code_box(s, [
    "- workflowId: bff-get-credit-cards",
    "  steps:",
    "    - stepId: call-bl-credit-cards",
    "      operationId: bl-loyalty-financial-information.getCreditCardsFromDatabase",
    "      parameters:",
    "        - name: identification_number",
    "          in: query",
    "          value: $inputs.identification_number  # resuelto por el BFF desde el JWT",
    "      successCriteria:",
    "        - condition: $statusCode == 200",
    "      outputs:",
    "        credit_cards: $response.body#/credit_cards",
], 0.4, 1.75, 12.5, 4.0)

insight_box = s.shapes.add_shape(1, Inches(0.4), Inches(5.95), Inches(12.5), Inches(1.3))
insight_box.fill.solid()
insight_box.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
insight_box.line.color.rgb = C_YELLOW
insight_box.line.width = Pt(1.2)
txt(s, "Sin Arazzo: esa lógica vive solo en el código del BFF. Nadie más sabe que ocurre.\n"
       "Con Arazzo: es parte del contrato. Aparece en el diff, en el lint, en la documentación.",
    0.65, 6.05, 12.1, 1.1, size=14, color=C_WHITE)

footer_logo(s)
slide_number(s, 11)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — HERRAMIENTAS: ARAZZO UI
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "Herramienta 1 — Arazzo UI", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)
txt(s, "arazzo-ui.jentic.com", 0.5, 1.2, 12, 0.4, size=14, color=C_ACCENT)

box(s, 0.4, 1.75, 12.5, 2.2, C_CARD)
txt(s, "Renderiza tu archivo Arazzo como diagrama interactivo del flujo.", 0.65, 1.9, 12.0, 0.55, size=16, bold=True, color=C_ACCENT)
txt(s, "Puedes ver los steps, dependencias, inputs y outputs — sin instalar nada.\n"
       "Es el equivalente a Swagger UI, pero para workflows.",
    0.65, 2.45, 12.0, 0.9, size=14, color=C_WHITE)

txt(s, "Por qué importa:", 0.5, 4.2, 12, 0.45, size=15, bold=True, color=C_WHITE)

points = [
    "El archivo deja de ser YAML abstracto — se convierte en algo que cualquier persona del equipo puede leer.",
    "Ideal para presentar Arazzo a arquitectos, PO o equipos de negocio sin experiencia en la spec.",
    "Zero fricción: subís el archivo, ves el diagrama.",
]
for i, p in enumerate(points):
    txt(s, f"→  {p}", 0.6, 4.75 + i * 0.7, 12.1, 0.6, size=13, color=C_SOFT)

footer_logo(s)
slide_number(s, 12)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — HERRAMIENTAS: SPECTRAL + MI RULESET
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, C_ACCENT2)
txt(s, "Herramienta 2 — Spectral + mi ruleset público", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)

# Highlight box for the contribution
contrib = s.shapes.add_shape(1, Inches(0.4), Inches(1.3), Inches(12.5), Inches(1.1))
contrib.fill.solid()
contrib.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
contrib.line.color.rgb = C_ACCENT2
contrib.line.width = Pt(2.0)
txt(s, "🔖  Mientras investigaba, noté que no existía ningún ruleset de Spectral específico para Arazzo.\n"
       "     Así que lo creé y lo publiqué: gitlab.com/api-labs1/api-arazzo/spectral-rules",
    0.65, 1.38, 12.1, 0.92, size=14, color=C_WHITE)

txt(s, "116 reglas en 5 rulesets:", 0.5, 2.6, 5, 0.45, size=15, bold=True, color=C_ACCENT2)

rules = [
    ("General", "36", "Campos requeridos en todos los objetos"),
    ("Governance", "34", "Enums, exclusividad mutua, condiciones"),
    ("Naming", "17", "Patrones de identificadores y casing"),
    ("Expressions", "11", "Sintaxis de runtime ($steps.*, $inputs.*)"),
    ("Best Practices", "18", "Recomendaciones de calidad opinadas"),
]
for i, (name, count, desc) in enumerate(rules):
    t = 3.15 + i * 0.72
    box(s, 0.4, t, 1.2, 0.58, C_CARD)
    txt(s, count, 0.4, t + 0.06, 1.2, 0.46, size=18, bold=True, color=C_ACCENT2, align=PP_ALIGN.CENTER)
    txt(s, name, 1.75, t + 0.04, 2.5, 0.28, size=13, bold=True, color=C_WHITE)
    txt(s, desc, 1.75, t + 0.32, 10.5, 0.28, size=12, color=C_SOFT)

code_box(s, [
    "# .spectral.yaml",
    'extends:',
    '  - "https://gitlab.com/api-labs1/api-arazzo/spectral-rules/-/raw/main/spectral-arazzo.yaml"',
    "",
    "# Luego:",
    "spectral lint credit-card-workflow.arazzo.yaml --ruleset .spectral.yaml",
], 7.0, 2.55, 6.2, 2.8)

txt(s, "Incluye templates para GitHub Actions y GitLab CI listos para usar.",
    7.0, 5.5, 6.2, 0.5, size=13, color=C_SOFT)

footer_logo(s)
slide_number(s, 13)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — HERRAMIENTAS: ARAZZO CLI
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06, C_YELLOW)
txt(s, "Herramienta 3 — arazzo-cli", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)
txt(s, "strefethen.github.io/arazzo-cli  ·  Ejecuta y depura workflows Arazzo en local",
    0.5, 1.2, 12, 0.4, size=13, color=C_SOFT)

features = [
    ("Ejecución del flujo completo", "Resuelve expresiones, evalúa successCriteria, propaga outputs.", C_ACCENT),
    ("DAG-based scheduling", "Steps sin dependencias se ejecutan en paralelo automáticamente.", C_ACCENT2),
    ("Trazas detalladas", "trace.v1.json: cada request, response, criterio y decisión de routing.", C_YELLOW),
    ("Replay determinista", "Re-ejecuta una traza offline sin golpear la API de nuevo.", C_WHITE),
    ("VS Code extension", "Breakpoints, inspección de variables y watch expressions.", RGBColor(0xFF, 0x6B, 0x6B)),
]

for i, (title, body, color) in enumerate(features):
    t = 1.75 + i * 0.95
    circ = s.shapes.add_shape(9, Inches(0.35), Inches(t + 0.1), Inches(0.5), Inches(0.5))
    circ.fill.solid()
    circ.fill.fore_color.rgb = color
    circ.line.fill.background()
    txt(s, str(i + 1), 0.35, t + 0.1, 0.5, 0.5, size=13, bold=True,
        color=C_BG, align=PP_ALIGN.CENTER)
    txt(s, title, 1.0, t + 0.04, 5.0, 0.4, size=14, bold=True, color=color)
    txt(s, body, 1.0, t + 0.46, 5.5, 0.38, size=12, color=C_SOFT)

code_box(s, [
    "# Instalar (binarios disponibles para Linux, macOS, Windows)",
    "cargo install --git https://github.com/strefethen/arazzo-cli.git arazzo-cli --locked",
    "",
    "# Ejecutar el workflow de la demo",
    "arazzo-cli run credit-card-workflow.arazzo.yaml \\",
    "           --workflow consumer-browse-card-benefits",
    "",
    "# Output: JSON estructurado, listo para CI",
], 6.8, 1.75, 6.1, 3.5)

footer_logo(s)
slide_number(s, 14)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — POR QUÉ IMPORTA PARA GOBERNANZA
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)
accent_bar(s, 0.5, 0.06)
txt(s, "¿Por qué importa para la gobernanza de APIs?", 0.5, 0.65, 12.5, 0.6, size=24, bold=True, color=C_WHITE)

analogy = s.shapes.add_shape(1, Inches(0.4), Inches(1.4), Inches(12.5), Inches(1.0))
analogy.fill.solid()
analogy.fill.fore_color.rgb = C_SURFACE
analogy.line.color.rgb = C_ACCENT
analogy.line.width = Pt(1.2)
txt(s, "Documentar solo los contratos individuales es como escribir los ingredientes de una receta\n"
       "pero nunca los pasos de cocción.  Arazzo formaliza los pasos de cocción.",
    0.65, 1.5, 12.1, 0.82, size=14, italic=True, color=C_WHITE)

txt(s, "Cuando los flujos son artefactos de primera clase, pasan cuatro cosas:", 0.5, 2.65, 12.5, 0.5, size=15, bold=True, color=C_WHITE)

governance_items = [
    ("Breaking changes en flujos detectables antes de producción", C_ACCENT),
    ("Consumidores parten de una fuente canónica, no de su propia interpretación", C_ACCENT2),
    ("Testing de integración derivado de la especificación, no artesanal", C_YELLOW),
    ("La gobernanza cubre la secuencia, no solo el endpoint", RGBColor(0xFF, 0x6B, 0x6B)),
]

for i, (text, color) in enumerate(governance_items):
    t = 3.3 + i * 0.9
    bar_shape = s.shapes.add_shape(1, Inches(0.4), Inches(t + 0.15), Inches(0.12), Inches(0.55))
    bar_shape.fill.solid()
    bar_shape.fill.fore_color.rgb = color
    bar_shape.line.fill.background()
    txt(s, text, 0.7, t + 0.1, 12.1, 0.6, size=15, color=C_WHITE)

footer_logo(s)
slide_number(s, 15)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — CIERRE
# ══════════════════════════════════════════════════════════════════════════════
s = add_slide()
bg(s)

# Full-width top bar
top = s.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(0.12))
top.fill.solid()
top.fill.fore_color.rgb = C_ACCENT
top.line.fill.background()

txt(s, "El conjunto completo:", 0.6, 0.35, 12, 0.5, size=16, color=C_SOFT)

# Three pillars
pillars = [
    ("OpenAPI", "Los contratos", C_ACCENT),
    ("Arazzo", "Los flujos", C_ACCENT2),
    ("Gates en CI", "La gobernanza ejecutable", C_YELLOW),
]
for i, (title, sub, color) in enumerate(pillars):
    l = 0.5 + i * 4.25
    box(s, l, 1.0, 3.8, 2.0, C_CARD)
    strip = s.shapes.add_shape(1, Inches(l), Inches(1.0), Inches(3.8), Inches(0.1))
    strip.fill.solid()
    strip.fill.fore_color.rgb = color
    strip.line.fill.background()
    txt(s, title, l, 1.2, 3.8, 0.7, size=26, bold=True, color=color, align=PP_ALIGN.CENTER)
    txt(s, sub, l, 1.9, 3.8, 0.6, size=14, color=C_WHITE, align=PP_ALIGN.CENTER)

plus1 = s.shapes.add_shape(9, Inches(4.35), Inches(1.65), Inches(0.55), Inches(0.55))
plus1.fill.solid(); plus1.fill.fore_color.rgb = C_SOFT; plus1.line.fill.background()
txt(s, "+", 4.35, 1.65, 0.55, 0.55, size=18, bold=True, color=C_BG, align=PP_ALIGN.CENTER)

plus2 = s.shapes.add_shape(9, Inches(8.6), Inches(1.65), Inches(0.55), Inches(0.55))
plus2.fill.solid(); plus2.fill.fore_color.rgb = C_SOFT; plus2.line.fill.background()
txt(s, "+", 8.6, 1.65, 0.55, 0.55, size=18, bold=True, color=C_BG, align=PP_ALIGN.CENTER)

# Big closing quote
quote = s.shapes.add_shape(1, Inches(0.5), Inches(3.3), Inches(12.3), Inches(2.0))
quote.fill.solid()
quote.fill.fore_color.rgb = RGBColor(0x00, 0x3A, 0x6B)
quote.line.color.rgb = C_ACCENT
quote.line.width = Pt(2.0)

txt(s, '"Los contratos aislados documentan lo que una API puede hacer.\n'
       ' Los flujos orquestados documentan cómo las APIs producen valor juntas.\n'
       ' Ambos necesitan gobernanza. Arazzo le da al segundo\n'
       ' su primera representación estándar."',
    0.75, 3.4, 11.8, 1.8, size=16, italic=True, color=C_WHITE)

txt(s, "Repos:", 0.5, 5.55, 2, 0.4, size=13, bold=True, color=C_SOFT)
txt(s, "gitlab.com/api-labs1/api-arazzo/api-workflows", 1.4, 5.55, 7, 0.4, size=13, color=C_ACCENT)
txt(s, "gitlab.com/api-labs1/api-arazzo/spectral-rules", 1.4, 5.95, 7, 0.4, size=13, color=C_ACCENT2)

txt(s, "Bryam David Vega Moreno · Senior Consultant · Thoughtworks",
    0.5, 6.7, 10, 0.45, size=13, color=C_SOFT)

slide_number(s, 16)


# ── Save ───────────────────────────────────────────────────────────────────────
out_path = "/Users/bvegam/Downloads/arazzo-presentacion-bryam-vega.pptx"
prs.save(out_path)
print(f"Saved: {out_path}")
