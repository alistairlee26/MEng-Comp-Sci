from pathlib import Path
import sys
import math
from html import escape

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

W, H = 2200, 1400
INK, BLUE, RED, GREY = '#172a3a', '#176492', '#b64136', '#526575'
items = []

def line(x1, y1, x2, y2, colour=INK, width=3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}"{d}/>')

def text(x, y, value, size=23, colour=INK, bold=False, anchor='start'):
    items.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{colour}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

def rect(x, y, w, h, fill='white', stroke=INK, radius=0):
    items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')

def dot(x, y, colour=INK):
    items.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{colour}"/>')

def ground(x, y):
    line(x, y, x, y+14)
    for offset, half in [(14, 22), (22, 14), (30, 6)]:
        line(x-half, y+offset, x+half, y+offset)

def rv(x, top, bottom, label, value, thermistor=False):
    mid=(top+bottom)/2
    line(x, top, x, mid-32)
    rect(x-13, mid-32, 26, 64)
    line(x, mid+32, x, bottom)
    if label:
        text(x+35, mid-3, label, 23, bold=True)
        text(x+35, mid+25, value, 22)
    if thermistor:
        line(x-31, mid+35, x+26, mid-36)
        line(x-31, mid+35, x-44, mid+35)

def rh(left, right, y, label, value, label_shift=0):
    mid=(left+right)/2
    line(left, y, mid-35, y)
    rect(mid-35, y-12, 70, 24)
    line(mid+35, y, right, y)
    text(mid, y-51+label_shift, label, 22, bold=True, anchor='middle')
    text(mid, y-24+label_shift, value, 22, anchor='middle')

def cap(x, top, bottom, label, value, label_left=False):
    mid=(top+bottom)/2
    line(x, top, x, mid-7)
    line(x-23, mid-7, x+23, mid-7)
    line(x-23, mid+7, x+23, mid+7)
    line(x, mid+7, x, bottom)
    tx=x-36 if label_left else x+35
    a='end' if label_left else 'start'
    text(tx, mid-3, label, 21, bold=True, anchor=a)
    text(tx, mid+24, value, 21, anchor=a)

rect(0, 0, W, H, '#ffffff', '#ffffff')
text(65, 75, 'Heating subsystem | example electrical schematic', 43, bold=True)
text(65, 117, 'CSEEE-21  /  Nano ESP32 controller  /  illustrative values, not a calibrated or tested build', 25, GREY)
line(65, 150, 2135, 150, '#dbe3e9', 2)
text(90, 200, '1  TEMPERATURE MEASUREMENT', 25, BLUE, True)
text(760, 200, '2  LOCAL CONTROL', 25, BLUE, True)
text(1200, 200, '3  GATE DRIVE', 25, BLUE, True)
text(1740, 200, '4  HEATER POWER', 25, RED, True)

# Thermistor divider: fixed resistor at the top, NTC to ground.
text(230, 260, '+3.3 V', 25, BLUE, True, 'middle')
text(230, 289, 'from Nano 3V3', 20, GREY, anchor='middle')
line(230, 300, 230, 310)
rv(230, 310, 420, 'R1', '10 kohm, 1%')
dot(230, 420)
rv(230, 420, 640, 'TH1', '10 kohm NTC at 25 C', True)
ground(230, 640)
text(95, 717, 'Thermistor immersed in liquid;', 22, GREY)
text(95, 749, 'electrically insulated probe.', 22, GREY)
rh(230, 620, 420, 'R2', '1 kohm', -65)
line(620, 420, 750, 420)
dot(620, 420)
cap(620, 420, 570, 'C1', '100 nF', True)
ground(620, 570)
text(465, 648, 'ADC filter', 21, GREY)
text(390, 464, 'V_SENSE', 20, BLUE, True)

# Controller: board supply and named 3V3 net.
rect(750, 390, 340, 400, '#edf5fa', BLUE, 14)
text(920, 482, 'U1', 26, BLUE, True, 'middle')
text(920, 523, 'Arduino', 29, bold=True, anchor='middle')
text(920, 563, 'Nano ESP32', 29, bold=True, anchor='middle')
text(920, 610, 'USB powered', 24, GREY, anchor='middle')
text(765, 450, 'A0', 23, BLUE, True)
text(1072, 659, 'D5', 23, BLUE, True, 'end')
text(920, 711, 'Read temperature', 23, anchor='middle')
text(920, 744, 'Compute heater duty', 23, anchor='middle')
line(920, 390, 920, 325, BLUE)
text(920, 308, '+3.3 V divider supply', 22, BLUE, anchor='middle')
line(920, 790, 920, 880)
ground(920, 880)
text(770, 947, 'UART to gateway omitted;', 22, GREY)
text(770, 979, 'feedback stays on U1.', 22, GREY)

# Non-inverting driver, including both duplicate pins for PDIP-8.
rect(1200, 620, 270, 140, '#f0f6f4', BLUE, 10)
text(1335, 655, 'U2  TC4420', 25, BLUE, True, 'middle')
text(1213, 706, 'IN (2)', 20)
text(1457, 706, 'OUT (6,7)', 20, anchor='end')
text(1335, 741, 'non-inverting', 20, GREY, anchor='middle')
line(1090, 680, 1200, 680, BLUE)
dot(1140, 680, BLUE)
rv(1140, 715, 825, '', '')
text(1175, 822, 'R3', 23, bold=True)
text(1175, 850, '100 kohm', 22)
line(1140, 680, 1140, 715)
line(1140, 825, 1140, 880)
ground(1140, 880)
text(1105, 520, '0 / 3.3 V PWM', 21, BLUE)
line(1335, 620, 1335, 600, RED)
line(1335, 600, 1250, 600, RED)
line(1250, 600, 1250, 400, RED)
line(1250, 400, 1555, 400, RED)
dot(1250, 400, RED)
text(1320, 352, '+6 V', 25, RED, True)
text(1320, 381, 'VDD pins 1,8', 20, GREY)
dot(1435, 400, RED)
cap(1435, 400, 520, 'C2', '100 nF', True)
ground(1435, 520)
cap(1555, 400, 520, 'C3', '1 uF')
ground(1555, 520)
text(1300, 585, 'C2/C3 close to U2 supply pins', 20, GREY)
line(1335, 760, 1335, 880)
ground(1335, 880)
text(1373, 850, 'GND pins 4,5', 20, GREY)
rh(1470, 1740, 680, 'R4', '100 ohm')
line(1740, 680, 1830, 680, BLUE)
dot(1740, 680, BLUE)
rv(1740, 715, 825, 'R5', '100 kohm')
line(1740, 680, 1740, 715)
line(1740, 825, 1740, 880)
ground(1740, 880)
text(1548, 604, '0 / 6 V gate drive', 21, BLUE)

# Heater branch: supply -> fuse -> switch -> heater -> drain -> source -> return.
text(1900, 260, '+6 V DC', 27, RED, True, 'middle')
text(1900, 291, 'example regulated supply: >=3 A', 20, GREY, anchor='middle')
line(1900, 303, 1900, 330, RED, 4)
rect(1884, 330, 32, 50, '#fff6f4', RED)
line(1900, 330, 1900, 380, RED, 2)
text(1940, 352, 'F1  3 A', 23, RED, True)
line(1900, 380, 1900, 402, RED, 4)
dot(1900, 402, RED)
line(1900, 402, 1922, 430, RED, 4)
dot(1900, 442, RED)
line(1900, 442, 1900, 470, RED, 4)
text(1940, 418, 'SW1', 23, bold=True)
text(1940, 446, 'heater enable', 21)
rv(1900, 470, 590, 'H1', '3 ohm, 30 W rated')
line(1900, 590, 1900, 640, RED, 4)

# Simplified N-channel enhancement MOSFET symbol: insulated gate, broken channel.
line(1830, 640, 1830, 720, BLUE, 4)
for ya, yb in [(640, 658), (670, 690), (702, 720)]:
    line(1854, ya, 1854, yb, INK, 4)
line(1854, 640, 1900, 640, RED, 4)
line(1854, 720, 1900, 720, INK, 4)
line(1900, 720, 1900, 880, INK, 4)
text(1815, 655, 'G', 21, BLUE, anchor='end')
text(1920, 622, 'D', 21, RED)
text(1920, 745, 'S', 21)
text(1950, 675, 'Q1', 25, bold=True)
text(1950, 710, 'IRLB8748', 24, bold=True)
text(1950, 742, 'N-MOSFET', 21)
ground(1900, 880)
text(1770, 947, 'ON: I approximately 2 A', 24, RED, True)
text(1770, 984, 'ON: P approximately 12 W', 24, RED, True)

# Notes below the drawing are part of the export.
line(65, 1025, 2135, 1025, '#dbe3e9', 2)
rect(65, 1055, 1005, 225, '#f4f8fb', '#dbe3e9', 12)
text(90, 1094, 'Sensor model and control', 25, BLUE, True)
text(90, 1134, 'V_SENSE = 3.3 x R_NTC / (10,000 + R_NTC)', 24)
text(90, 1170, 'At 25 C: R_NTC = 10 kohm, V_SENSE = 1.65 V.', 23)
text(90, 1206, 'As temperature rises, R_NTC and V_SENSE fall.', 23)
text(90, 1242, 'Example: 30 C target; start with slow PWM / time proportioning.', 22)
rect(1100, 1055, 1035, 225, '#fff7f4', '#eadad5', 12)
text(1125, 1094, 'Power and wiring assumptions', 25, RED, True)
text(1125, 1134, 'P_ON = V^2 / R = 6^2 / 3 = 12 W; P_AVG approximately duty x 12 W.', 23)
text(1125, 1170, '12 V directly across 3 ohm would produce 48 W, not 30 W.', 23)
text(1125, 1206, 'All GND symbols share a return. Route heater current separately', 23)
text(1125, 1242, 'from sensor/USB grounds to a common supply-return point.', 23)
text(65, 1324, 'Design example: verify actual pinouts, supply limits, thermistor calibration and available heating power before assembly.', 23, GREY)
text(65, 1364, 'U2 is an added driver, not confirmed in the supplied kit. NC pin 3 unconnected. SW1 shown open. All resistor values illustrative.', 21, GREY)

svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(items) + '</svg>'
(ROOT / 'Heating_Subsystem_Schematic.svg').write_text(svg, encoding='utf-8')
doc = pymupdf.open(stream=svg.encode('utf-8'), filetype='svg')
pdf_bytes = doc.convert_to_pdf()
pdf = pymupdf.open('pdf', pdf_bytes)
pdf.save(ROOT / 'Heating_Subsystem_Schematic.pdf')
pdf[0].get_pixmap(matrix=pymupdf.Matrix(1, 1), alpha=False).save(ROOT / 'Heating_Subsystem_Schematic.png')

print('Created Heating_Subsystem_Schematic.svg, .pdf and .png')
for c in (25, 30, 35):
    r=10000*math.exp(3950*(1/(c+273.15)-1/298.15))
    v=3.3*r/(10000+r)
    print(f'Illustrative beta=3950 K: {c} C -> {r:.0f} ohm -> {v:.3f} V')
for v in (6, 9, 12):
    print(f'{v} V across 3 ohm -> {v/3:.1f} A, {v*v/3:.1f} W')
