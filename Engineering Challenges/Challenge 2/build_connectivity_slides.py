from pathlib import Path
import sys
import math
import re

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / '.slide-tools'), str(ROOT / '.review-tools')]
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.xmlchemy import OxmlElement
import pymupdf

if '--inspect-style' in sys.argv:
    sys.stdout.reconfigure(encoding='utf-8')
    from collections import Counter
    source = pymupdf.open(ROOT / 'Engineering Challenges Presentation.pdf')
    for i, page in enumerate(source):
        spans = [span for block in page.get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans']]
        print(f'PAGE {i+1} SIZE {page.rect}')
        print('STYLES', Counter((s['font'], round(s['size'],2), s['color']) for s in spans).most_common(8))
        print('FIRST TEXT', [(s['text'], s['font'], round(s['size'],2), tuple(round(v,2) for v in s['bbox'])) for s in spans[:5]])
        print('DRAW COLOURS', Counter((str(d.get('color')), str(d.get('fill')), round(d.get('width') or 0,2)) for d in page.get_drawings()).most_common(5))
    raise SystemExit(0)

W, H = 1280, 720
MINIMAL = '--minimal' in sys.argv
MATCH_TEAM = '--match-team-style' in sys.argv or MINIMAL
SUFFIX = '_Simple' if MINIMAL else ('_Matched' if MATCH_TEAM else '')
INK = '#000000' if MATCH_TEAM else '#17232E'
MUTED = '#595959' if MATCH_TEAM else '#52606B'
ACCENT = '#595959' if MATCH_TEAM else '#245A78'
EDGE = '#595959' if MATCH_TEAM else '#BBC4CB'
PALE = '#FFFFFF' if MINIMAL else ('#EEEEEE' if MATCH_TEAM else '#F1F5F7')
WHITE = '#FFFFFF'
scenes = []
source_title = None
if MATCH_TEAM:
    with pymupdf.open(ROOT / 'Engineering Challenges Presentation.pdf') as ref:
        source_title = next(span for block in ref[6].get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'])


class Scene:
    def __init__(self, title):
        self.title = title
        self.items = []
        self.notes = ''

    def rect(self, x, y, w, h, fill=WHITE, stroke=EDGE):
        self.items.append(('rect', x, y, w, h, fill, stroke))

    def text(self, x, y, value, size=20, color=INK, bold=False, width=None):
        self.items.append(('text', x, y, value, size, color, bold, width or (W-x-35)))

    def line(self, x1, y1, x2, y2, color=ACCENT, width=2):
        self.items.append(('line', x1, y1, x2, y2, color, width))

    def arrow(self, x1, y1, x2, y2, both=False, color=ACCENT):
        self.line(x1, y1, x2, y2, color)
        def head(a, b, c, d):
            theta = math.atan2(d-b, c-a)
            for delta in (-.48, .48):
                self.line(c, d, c-9*math.cos(theta+delta), d-9*math.sin(theta+delta), color)
        head(x1, y1, x2, y2)
        if both:
            head(x2, y2, x1, y1)

    def box(self, x, y, w, title, lines):
        self.rect(x, y, w, 94, PALE)
        self.text(x+13, y+13, title, 21, bold=True, width=w-26)
        for i, line in enumerate(lines):
            self.text(x+13, y+46+i*21, line, 16, MUTED, width=w-26)


def base(title, subtitle):
    s = Scene(title)
    if MATCH_TEAM:
        if title.startswith('Backup:'):
            title = 'Command flow and software structure'
        s.text(source_title['bbox'][0]*W/720, source_title['bbox'][1]*W/720,
               title, source_title['size']*W/720, bold=False)
    else:
        s.text(40, 26, title, 38, bold=False)
        s.text(40, 79, subtitle, 20, MUTED)
        s.line(40, 117, 1240, 117, EDGE, 1)
    return s


def wireframe(s):
    s.text(40, 340, 'PROPOSED SCREEN  /  example values', 17, MUTED, True)
    cards = [
        ('Temperature', '29.8 °C', 'Confirmed: 30.0 °C', '25–35 °C', [27,23,17,6,10,8,9]),
        ('Stirring speed', '998 RPM', 'Confirmed: 1000 RPM', '500–1500 RPM', [25,7,13,10,12,9,11]),
        ('pH', '5.02', 'Confirmed: 5.00', 'pH 3–7', [2,8,15,17,14,16,15]),
    ]
    for i, (label, value, target, limit, series) in enumerate(cards):
        x = 40 + i*240
        s.rect(x, 374, 220, 210)
        s.text(x+14, 386, label, 19, bold=True, width=194)
        s.text(x+14, 417, value, 31, ACCENT, True, width=194)
        s.text(x+14, 458, target, 17, width=194)
        s.rect(x+14, 487, 117, 27, WHITE, EDGE)
        s.text(x+22, 491, 'New target', 15, MUTED, width=104)
        s.rect(x+141, 487, 65, 27, PALE, EDGE)
        s.text(x+153, 491, 'Apply', 15, ACCENT, width=48)
        s.line(x+15, 566, x+205, 566, EDGE, 1)
        s.line(x+15, 530, x+15, 566, EDGE, 1)
        s.line(x+15, 544, x+205, 544, '#8B959E', 1)
        for j in range(len(series)-1):
            s.line(x+16+j*31, 533+series[j], x+16+(j+1)*31, 533+series[j+1], ACCENT, 2)
        s.text(x+14, 591, limit, 16, MUTED, width=194)
    s.text(810, 340, 'OPERATOR ACTIONS', 17, MUTED, True)
    for i, t in enumerate(['Monitor values and trends.', 'Apply validated setpoints.', 'Wait for controller confirmation.', 'Export timestamped records.']):
        s.text(810, 379+i*35, t, 21, width=425)
    s.text(810, 534, 'On link loss: mark readings stale.', 20, ACCENT, True, width=425)
    s.text(810, 563, 'Local loops follow the agreed policy.', 19, MUTED, width=425)


def footer(s, caveat):
    s.rect(40, 632, 1200, 40, PALE, PALE)
    s.text(55, 642, 'PROPOSED TESTS   1 Hz reporting  |  95% of confirmations ≤2 s  |  stale warning after 5 s', 18, ACCENT, width=1160)
    s.text(40, 685, caveat, 13, MUTED, width=1200)


mqtt = base('Connectivity and User Interface', 'Shared monitoring, target adjustment and experiment logging')
mqtt.text(40, 134, 'AT THE REACTOR', 16, MUTED, True)
mqtt.text(560, 134, 'NETWORK SERVICE', 16, MUTED, True)
mqtt.text(810, 134, 'ON THE OPERATOR LAPTOP', 16, MUTED, True)
mqtt.box(40, 183, 190, 'Control board', ['Sensors + actuators', 'Local feedback loops'])
mqtt.box(300, 183, 190, 'ESP32 gateway', ['Forwards readings', 'and target requests'])
mqtt.box(560, 183, 180, 'MQTT broker', ['Routes messages', 'between clients'])
mqtt.box(810, 183, 200, 'Laptop backend', ['Hosts UI + CSV logs', 'Feeds data analysis'])
mqtt.box(1080, 183, 160, 'Browser', ['Dashboard', 'Operator inputs'])
for x1,x2,label,small in [(230,300,'UART',''),(490,560,'Wi-Fi','MQTT'),(740,810,'MQTT',''),(1010,1080,'Local','web')]:
    mqtt.arrow(x1+6, 233, x2-6, 233, both=True)
    mqtt.text(x1+7, 185, label, 15, ACCENT, width=x2-x1-10)
    if small:
        mqtt.text(x1+7, 204, small, 14, ACCENT, width=x2-x1-10)
mqtt.text(40, 296, 'Readings + controller confirmations →     ← Target requests', 18, MUTED)
wireframe(mqtt)
footer(mqtt, 'Proposed architecture. Verify board models and course-broker access. Brief: Design Specification pp. 4, 13, 17–18; Connectivity pp. 18–19.')

http = base('Connectivity and User Interface', 'Alternative proposal: direct HTTP over a local Wi-Fi connection')
http.text(40, 134, 'AT THE REACTOR', 16, MUTED, True)
http.text(790, 134, 'ON THE OPERATOR LAPTOP', 16, MUTED, True)
http.box(40, 183, 210, 'Control board', ['Sensors + actuators', 'Local feedback loops'])
http.box(350, 183, 250, 'ESP32 gateway', ['Wi-Fi access point', 'HTTP API + UART bridge'])
http.box(790, 183, 220, 'Laptop backend', ['Polls state + sends targets', 'Hosts UI + CSV logs'])
http.box(1080, 183, 160, 'Browser', ['Dashboard', 'Operator inputs'])
http.arrow(258, 233, 342, 233, both=True)
http.text(274, 198, 'UART', 17, ACCENT, width=70)
http.arrow(608, 233, 782, 233, both=True)
http.text(629, 184, 'Wi-Fi / HTTP', 19, ACCENT, width=158)
http.text(636, 209, 'JSON requests', 17, MUTED, width=145)
http.arrow(1018, 233, 1072, 233, both=True)
http.text(1019, 185, 'Local', 15, ACCENT, width=58)
http.text(1019, 204, 'web', 14, ACCENT, width=58)
http.text(40, 296, 'Laptop joins the ESP32 network. Backend polls readings and sends target requests.', 18, MUTED)
wireframe(http)
footer(http, 'Local access only: confirm this scope and access-point use with staff. Internet access is not provided by this arrangement.')

backup = base('Backup: command flow and software structure', 'How a user request becomes a confirmed controller target')
backup.text(40, 137, 'COMMAND FLOW', 17, MUTED, True)
for x,title,lines in [
    (40,'User request',['Edit target + Apply']),
    (285,'Validate request',['Range + message ID']),
    (530,'Send to controller',['Network, then UART']),
    (775,'Controller checks',['Accept or reject']),
    (1020,'Return result',['Update UI + event log'])
]:
    backup.box(x, 185, 220, title, lines)
for x in [260,505,750,995]:
    backup.arrow(x+3, 232, x+20, 232)
backup.text(285, 290, 'Invalid → show error; do not send.', 17, MUTED, width=400)
backup.text(775, 290, 'No result → show timeout / unconfirmed.', 17, MUTED, width=465)
backup.text(40, 334, 'An applied target is confirmed by the control board. Reaching that target takes longer.', 21, ACCENT)
backup.text(40, 390, 'SOFTWARE STRUCTURE', 17, MUTED, True)
backup.rect(110, 435, 410, 48, PALE)
backup.text(130, 446, 'Gateway firmware', 22, bold=True, width=370)
backup.rect(760, 435, 410, 48, PALE)
backup.text(780, 446, 'Laptop application', 22, bold=True, width=370)
for parent, xs, labels in [
    (315, [40,230,420], ['UART messages','Network transport','Link status']),
    (965, [690,880,1070], ['UI + commands','Logging + analysis','Device connection'])
]:
    for x,label in zip(xs,labels):
        backup.line(parent,483,parent,507,EDGE,1)
        backup.line(parent,507,x+85,507,EDGE,1)
        backup.line(x+85,507,x+85,531,EDGE,1)
        backup.rect(x,531,170,52)
        backup.text(x+10,547,label,16,bold=False,width=150)
backup.rect(40, 623, 1200, 48, PALE, PALE)
backup.text(57, 637, 'First integration test: one simulated reading → dashboard, then one target request → controller confirmation.', 19, ACCENT)
backup.text(40, 686, 'Supporting models for Design Specification p. 18. Proposed responsibilities and logic; not measured implementation results.', 14, MUTED)

notes = (ROOT / 'Connectivity_Presentation_Notes.md').read_text(encoding='utf-8')
def extract(start, end):
    return notes.split(start, 1)[1].split(end, 1)[0].strip()
mqtt.notes = 'MAIN SLIDE — recommended if using eduroam and the course broker. Present either this slide or the HTTP alternative, not both.\n\n' + extract('**What to say for the MQTT slide — approximately 70 seconds**', '**What to say for the HTTP slide') + '\n\nSources: Design Specification pp. 4, 13, 17–18; Connectivity pp. 18–19. Timing figures are proposed targets, not results.'
http.notes = 'ALTERNATIVE MAIN SLIDE — local-only HTTP, subject to staff confirming scope and access-point use.\n\n' + extract('**What to say for the HTTP slide — approximately 75 seconds**', '**Optional backup slide**') + '\n\nThe ESP32 hosts the API; the laptop hosts the UI and logger. The laptop initiates API requests. HTTP receipt alone is not controller confirmation. A single Wi-Fi adapter may lose campus/internet access when joining the ESP32 network. The teaching anomaly simulator separately uses MQTT. Source: https://docs.espressif.com/projects/arduino-esp32/en/latest/api/wifi.html'
backup.notes = extract('**Optional backup slide**', '**Questions and concise answers**') + '\n\nValidation failures stay on the laptop; controller-side validation also remains mandatory. Controller rejection and missing confirmation must be visible. Neither network transport runs the physical feedback algorithms.'
scenes = [mqtt, http, backup]

if MATCH_TEAM:
    label_changes = {
        'AT THE REACTOR': 'At the reactor',
        'NETWORK SERVICE': 'Network service',
        'ON THE OPERATOR LAPTOP': 'On the operator laptop',
        'PROPOSED SCREEN  /  example values': 'Proposed screen (example values)',
        'OPERATOR ACTIONS': 'Operator actions',
        'COMMAND FLOW': 'Command flow',
        'SOFTWARE STRUCTURE': 'Software structure',
    }
    for scene in scenes:
        updated = []
        for item in scene.items:
            if item[0] == 'text':
                v = list(item)
                v[3] = label_changes.get(v[3], v[3])
                if v[3].startswith('PROPOSED TESTS'):
                    v[3] = v[3].replace('PROPOSED TESTS', 'Tests (proposed)')
                if v[2] in (134,137):
                    v[2] = 150
                # Keep labels and explanatory prose in the deck's regular Arial style.
                if v[4] <= 22:
                    v[6] = False
                updated.append(tuple(v))
            else:
                updated.append(item)
        scene.items = updated

if MINIMAL:
    remove_labels = {
        'At the reactor', 'Network service', 'On the operator laptop',
        'Operator actions', 'Monitor values and trends.',
        'Apply validated setpoints.', 'Wait for controller confirmation.',
        'Export timestamped records.',
        'On link loss: mark readings stale.',
        'Local loops follow the agreed policy.',
        'Readings + controller confirmations →     ← Target requests',
        'Laptop joins the ESP32 network. Backend polls readings and sends target requests.',
    }
    for scene in scenes:
        simplified = []
        for item in scene.items:
            if item[0] in ('text', 'rect') and item[2] >= 623:
                continue
            if item[0] == 'text':
                if item[3] in remove_labels:
                    continue
                v = list(item)
                if v[3] == 'Proposed screen (example values)':
                    v[3] = 'Example interface'
                if v[3] == 'Link status':
                    v[3] = 'Message parsing'
                v[6] = False
                item = tuple(v)
            simplified.append(item)
        scene.items = simplified
    for scene in (mqtt, http):
        for i, text in enumerate([
            'Monitor readings and trends.',
            'Adjust temperature, speed and pH.',
            'Log data and export CSV.',
        ]):
            scene.text(810, 400+i*55, text, 24, MUTED, width=425)
    mqtt.notes = '''Our subsystem connects the reactor to the operator. The control board exchanges measurements and target requests with the ESP32 over UART. The ESP32 and laptop application connect to an MQTT broker, which forwards their messages.

The web application and logger run on the laptop. The interface displays temperature, stirring speed and pH, with their current targets and trends. The operator can request new targets, which we validate and confirm with the control board. We also save timestamped readings for data analysis and export them as CSV.

The interface values shown are examples. Confirm the actual board models and course broker access with the team. Sources: Design Specification pp. 4, 13, 17–18; Connectivity pp. 18–19.'''
    http.notes = '''This alternative uses a direct local Wi-Fi connection. The control board exchanges measurements and target requests with the ESP32 over UART. The ESP32 creates a Wi-Fi network and exposes an HTTP API. The laptop joins that network, requests readings and sends target requests.

The web application and logger run on the laptop. The operator can monitor temperature, stirring speed and pH, adjust their targets, and export timestamped measurements as CSV. A change is confirmed by the control board before the interface reports it as applied.

The interface values shown are examples. This is local wireless access, not internet-wide access. Confirm the local scope and access-point use with staff. The separate teaching simulator still uses MQTT. Reference: Connectivity_Presentation_Notes.md.'''


def rgb(value):
    return tuple(int(value[i:i+2],16)/255 for i in (1,3,5))


prs = Presentation()
UNITS_PER_INCH = 128 if MATCH_TEAM else 96
POINT_SCALE = 72 / UNITS_PER_INCH
prs.slide_width = Inches(W/UNITS_PER_INCH)
prs.slide_height = Inches(H/UNITS_PER_INCH)
prs.core_properties.title = 'Connectivity and User Interface — CSEEE-21'
prs.core_properties.subject = 'Two alternative proposal slides and an optional implementation backup'
pdf = pymupdf.open()

for idx, scene in enumerate(scenes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.notes_slide.notes_text_frame.text = scene.notes
    page = pdf.new_page(width=W, height=H)
    for item_index, item in enumerate(scene.items):
        kind, *v = item
        if kind == 'rect':
            x,y,w,h,fill,stroke = v
            shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x/UNITS_PER_INCH), Inches(y/UNITS_PER_INCH), Inches(w/UNITS_PER_INCH), Inches(h/UNITS_PER_INCH))
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor.from_string(fill[1:])
            shape.line.color.rgb = RGBColor.from_string(stroke[1:])
            shape.line.width = Pt(.8)
            page.draw_rect(pymupdf.Rect(x,y,x+w,y+h), color=rgb(stroke), fill=rgb(fill), width=1)
        elif kind == 'line':
            x1,y1,x2,y2,color,width = v
            conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1/UNITS_PER_INCH), Inches(y1/UNITS_PER_INCH), Inches(x2/UNITS_PER_INCH), Inches(y2/UNITS_PER_INCH))
            conn.line.color.rgb = RGBColor.from_string(color[1:])
            conn.line.width = Pt(width*POINT_SCALE)
            page.draw_line((x1,y1),(x2,y2),color=rgb(color),width=width)
        elif kind == 'text':
            x,y,value,size,color,bold,width = v
            font = 'hebo' if bold else 'helv'
            # Enforce fit in both outputs before writing any deliverables.
            measured = pymupdf.get_text_length(value, fontname=font, fontsize=size)
            if measured > width:
                raise ValueError(f'Text exceeds box: {value!r} ({measured:.1f} > {width})')
            tb = slide.shapes.add_textbox(Inches(x/UNITS_PER_INCH), Inches(y/UNITS_PER_INCH), Inches(width/UNITS_PER_INCH), Inches((size*1.6)/UNITS_PER_INCH))
            tf = tb.text_frame
            tf.word_wrap = False
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.space_before = p.space_after = Pt(0)
            p.text = value
            p.font.name = 'Arial'
            p.font.size = Pt(size*POINT_SCALE)
            p.font.bold = bold
            p.font.color.rgb = RGBColor.from_string(color[1:])
            # Use embedded Windows Arial to preserve Greek and inequality symbols.
            font_path = Path('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf')
            pdf_font = 'ArialBold' if bold else 'Arial'
            page.insert_font(fontname=pdf_font, fontfile=str(font_path))
            baseline = source_title['origin'][1]*W/720 if MATCH_TEAM and item_index == 0 else y+size
            page.insert_text((x,baseline),value,fontname=pdf_font,fontsize=size,color=rgb(color))
    page.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(ROOT / f'Connectivity_Slide_{idx+1}{SUFFIX}.png')

prs.save(ROOT / f'Connectivity_Proposal_Slides{SUFFIX}.pptx')
if MATCH_TEAM:
    scaled = pymupdf.open()
    for i in range(len(pdf)):
        page = scaled.new_page(width=720, height=405)
        page.show_pdf_page(page.rect, pdf, i)
    pdf.close()
    pdf = scaled
pdf.save(ROOT / f'Connectivity_Proposal_Slides{SUFFIX}.pdf', garbage=4, deflate=True)

# Preserve the original team PDF; replace only the empty page in two new variants.
source = pymupdf.open(ROOT / 'Engineering Challenges Presentation.pdf')
for index, suffix in [(0, 'MQTT'), (1, 'HTTP_Alternative')]:
    revised = pymupdf.open()
    revised.insert_pdf(source, from_page=0, to_page=5)
    page = revised.new_page(width=source[6].rect.width, height=source[6].rect.height)
    page.show_pdf_page(page.rect, pdf, index)
    revised.insert_pdf(source, from_page=7, to_page=7)
    revised.save(ROOT / f'Team_Presentation_With_Connectivity_{suffix}{SUFFIX}.pdf', garbage=4, deflate=True)

check = Presentation(ROOT / f'Connectivity_Proposal_Slides{SUFFIX}.pptx')
assert len(check.slides) == 3
assert all(s.notes_slide.notes_text_frame.text.strip() for s in check.slides)
if MINIMAL:
    visible = '\n'.join(shape.text for slide in check.slides for shape in slide.shapes if shape.has_text_frame)
    assert not any(t in visible.lower() for t in ['proposed architecture', 'link loss', 'stale', 'tests (proposed)'])
    (ROOT / 'Connectivity_Simple_Speaker_Notes.md').write_text(
        '\n\n'.join(f'**Slide {i+1}: {scene.title}**\n\n{scene.notes}' for i, scene in enumerate(scenes)), encoding='utf-8')
for name in ['MQTT', 'HTTP_Alternative']:
    assert len(pymupdf.open(ROOT / f'Team_Presentation_With_Connectivity_{name}{SUFFIX}.pdf')) == 8
if MATCH_TEAM:
    assert check.slide_width == Inches(10)
    assert check.slide_height == Inches(5.625)
    for slide in check.slides:
        title_shape = next(shape for shape in slide.shapes if shape.has_text_frame)
        assert abs(title_shape.text_frame.paragraphs[0].font.size.pt - 25.2) < .02
        for shape in slide.shapes:
            if shape.has_text_frame and shape.text.strip():
                for paragraph in shape.text_frame.paragraphs:
                    assert paragraph.font.name == 'Arial'
print('Created editable 3-slide PowerPoint with notes, PDF previews, 3 PNGs and two revised team PDFs.')
print('Validated text fit, slide count, notes and original team page count.')
