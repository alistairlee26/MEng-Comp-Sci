from pathlib import Path
from html import escape
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

OUT = ROOT / 'Circuit_Diagram_Examples' / 'Heating_Whiteboard_Redrawn'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1800, 1120
INK, BLUE, RED, MUTED = '#152536', '#17618a', '#ac4036', '#526373'
parts = []

def line(x1, y1, x2, y2, colour=INK, width=3):
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}"/>')

def text(x, y, value, size=24, colour=INK, bold=False, anchor='start'):
    parts.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{colour}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

def rect(x, y, w, h, fill='white', stroke=INK, radius=0):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')

def dot(x, y):
    parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{INK}"/>')

def resistor(x, top, bottom, ref, value, thermistor=False):
    middle = (top + bottom) / 2
    line(x, top, x, middle - 43)
    rect(x-17, middle-43, 34, 86)
    line(x, middle+43, x, bottom)
    if thermistor:
        line(x-36, middle+39, x+34, middle-39)
        line(x-36, middle+39, x-51, middle+39)
    text(x+56, middle-8, ref, 25, bold=True)
    text(x+56, middle+27, value, 23)

def ground(x, y):
    line(x, y, x, y+20)
    for offset, half in [(20, 26), (30, 17), (40, 8)]:
        line(x-half, y+offset, x+half, y+offset)

rect(0, 0, W, H, 'white', 'white')
text(70, 78, 'Heating subsystem', 44, bold=True)
text(70, 120, "Lecturer's whiteboard circuit — clean schematic redraw", 25, MUTED)
line(70, 151, 1730, 151, '#d8e0e7', 2)
text(100, 205, 'INPUT · TEMPERATURE', 23, BLUE, True)
text(595, 205, 'PROCESSING · MCU', 23, BLUE, True)
text(1190, 205, 'OUTPUT · HEATER', 23, RED, True)

# Divider supplied by the MCU's 3.3 V rail, as drawn on the board.
line(230, 275, 740, 275, BLUE)
line(230, 275, 230, 320)
text(230, 253, '+3.3 V', 26, BLUE, True)
resistor(230, 320, 505, 'R1', 'Fixed resistor*')
dot(230, 505)
text(179, 515, 'A', 27, BLUE, True)
resistor(230, 505, 740, 'TH1', '10 kΩ thermistor', True)
line(230, 740, 230, 835)
line(230, 505, 575, 505, BLUE)
text(385, 482, 'V_SENSE', 21, BLUE, anchor='middle')

# MCU shown as a functional block because no board model is specified.
rect(575, 360, 345, 380, '#f2f7fb', BLUE, 10)
line(740, 275, 740, 360, BLUE)
text(755, 341, '3V3', 22, BLUE)
text(597, 494, 'A0', 25, BLUE, True)
text(748, 428, 'MICROCONTROLLER', 23, BLUE, True, 'middle')
text(748, 465, '3.3 V logic', 22, MUTED, anchor='middle')
text(748, 600, 'Read temperature', 23, anchor='middle')
text(748, 639, 'Set heater PWM', 23, anchor='middle')
text(897, 540, 'D1', 25, BLUE, True, 'end')
text(748, 716, 'GND', 23, anchor='middle')
line(748, 740, 748, 835)

# Whiteboard output: heater on positive supply, MOSFET switches its return.
text(1370, 265, '+12 V DC', 27, RED, True, 'middle')
line(1370, 282, 1370, 310, RED, 4)
resistor(1370, 310, 470, 'H1 · Heater', '3 Ω / 30 W rated')
line(1370, 470, 1370, 510, RED, 4)
text(1392, 507, 'D', 22, RED, True)

# Simplified N-channel enhancement MOSFET: gate is insulated from channel.
line(1260, 510, 1260, 620, BLUE, 4)
for start, end in [(510, 535), (549, 581), (595, 620)]:
    line(1290, start, 1290, end, INK, 4)
line(1290, 510, 1370, 510, INK, 4)
line(1290, 620, 1370, 620, INK, 4)
# Body connection tied to source, arrow points from P body into N channel.
line(1290, 565, 1335, 565)
line(1335, 565, 1335, 620)
parts.append(f'<polygon points="1293,565 1308,558 1308,572" fill="{INK}"/>')
line(1370, 620, 1370, 835, INK, 4)
text(1392, 649, 'S', 22, bold=True)
text(1236, 588, 'G', 22, BLUE, True, 'end')
text(1445, 556, 'Q1', 26, bold=True)
text(1445, 594, 'N-channel MOSFET', 23)
text(1445, 630, 'Part not specified', 21, MUTED)

line(920, 565, 1260, 565, BLUE)
text(1085, 484, 'PWM · 0–3.3 V', 24, BLUE, True, 'middle')
text(1085, 522, '62.5% duty cycle', 23, BLUE, anchor='middle')

# One explicit shared return removes ambiguity between the two ground symbols.
line(230, 835, 1370, 835)
dot(748, 835)
ground(748, 835)
text(850, 883, 'Common ground / 0 V', 23, MUTED)

line(70, 930, 1730, 930, '#d8e0e7', 2)
text(70, 977, 'Whiteboard power example', 25, RED, True)
text(70, 1017, '12 V across 3 Ω → 48 W when ON; 62.5% PWM → 30 W ideal average power.', 25)
text(70, 1061, '* R1 value is unclear in the photo. The MOSFET connection is reproduced as drawn;', 21, MUTED)
text(70, 1091, 'the diagram does not establish Q1 suitability for 3.3 V drive or validate the heater operating conditions.', 21, MUTED)

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(parts) + '</svg>'
stem = OUT / 'Heating_Whiteboard_Redrawn'
stem.with_suffix('.svg').write_text(svg, encoding='utf-8')
with pymupdf.open(stream=svg.encode('utf-8'), filetype='svg') as doc:
    with pymupdf.open('pdf', doc.convert_to_pdf()) as pdf:
        pdf.save(stem.with_suffix('.pdf'))
        pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False).save(stem.with_suffix('.png'))

notes = '''# Heating whiteboard redraw

Source: `WhatsApp Image 2026-11-18 at 11.37.47.jpeg` in the project root.

The SVG is editable; PDF and PNG are provided for documents and presentations.

## Transcription

- A fixed upper resistor and a lower 10 kΩ thermistor form a divider powered from the MCU 3.3 V rail. Node A feeds A0.
- D1 controls the gate of an unspecified N-channel MOSFET. The source returns to ground; the drain connects to the heater.
- The heater label reads 3 Ω, 30 W. The board annotates 12 V and 48 W, with a PWM duty annotation read as 62.5%.
- The fixed resistor value is blurry. It may read 1 kΩ, but the redraw deliberately leaves its value unspecified.
- MCU model, MOSFET part number and thermistor resistance reference temperature are not specified in the photograph.

## Drawing choices

- R1, TH1, H1 and Q1 are added reference designators for clarity.
- The separate ground indications are drawn as an explicit common return.
- The MOSFET is redrawn using a conventional symbol; no extra driver, protection components or filtering have been added.
- This reproduces the lecturer's concept; it is not an independently validated construction design. Whether Q1 operates properly at 3.3 V depends on the actual device. The arithmetic average of PWM power alone does not establish that a heater rated at 30 W may safely be pulsed at 48 W.
'''
(OUT / 'Source_and_Interpretation.md').write_text(notes, encoding='utf-8')
for file in sorted(OUT.iterdir()):
    print(file.relative_to(ROOT))
