from pathlib import Path
from html import escape
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

INK, BLUE, RED, GREY = '#172a3a', '#176492', '#b64136', '#526575'


class Drawing:
    def __init__(self, title, subtitle, height=1500):
        self.w, self.h, self.items = 2400, height, []
        self.rect(0, 0, self.w, height, '#ffffff', '#ffffff')
        self.text(65, 75, title, 43, bold=True)
        self.text(65, 118, subtitle, 25, GREY)
        self.line(65, 150, 2335, 150, '#dbe3e9', 2)

    def line(self, x1, y1, x2, y2, colour=INK, width=3, dash=None):
        dash = f' stroke-dasharray="{dash}"' if dash else ''
        self.items.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-width="{width}"{dash}/>')

    def text(self, x, y, value, size=23, colour=INK, bold=False, anchor='start'):
        self.items.append(f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{colour}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

    def rect(self, x, y, w, h, fill='white', stroke=INK, radius=0):
        self.items.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')

    def circle(self, x, y, r, fill='white', stroke=INK):
        self.items.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')

    def dot(self, x, y, colour=INK):
        self.circle(x, y, 4, colour, colour)

    def ground(self, x, y):
        self.line(x, y, x, y+14)
        for offset, half in [(14, 22), (22, 14), (30, 6)]:
            self.line(x-half, y+offset, x+half, y+offset)

    def rv(self, x, top, bottom, label='', value='', side=1, shift=0):
        mid = (top+bottom)/2
        self.line(x, top, x, mid-32)
        self.rect(x-13, mid-32, 26, 64)
        self.line(x, mid+32, x, bottom)
        if label:
            anchor = 'start' if side > 0 else 'end'
            self.text(x+35*side, mid-3+shift, label, 22, bold=True, anchor=anchor)
            self.text(x+35*side, mid+25+shift, value, 22, anchor=anchor)

    def rh(self, left, right, y, label='', value='', shift=0):
        mid = (left+right)/2
        self.line(left, y, mid-35, y)
        self.rect(mid-35, y-12, 70, 24)
        self.line(mid+35, y, right, y)
        if label:
            self.text(mid, y-51+shift, label, 22, bold=True, anchor='middle')
            self.text(mid, y-24+shift, value, 22, anchor='middle')

    def cap(self, x, top, bottom, label, value, side=1, polar=False):
        mid = (top+bottom)/2
        self.line(x, top, x, mid-7)
        self.line(x-23, mid-7, x+23, mid-7)
        self.line(x-23, mid+7, x+23, mid+7)
        self.line(x, mid+7, x, bottom)
        anchor = 'start' if side > 0 else 'end'
        self.text(x+35*side, mid-3, label, 22, bold=True, anchor=anchor)
        self.text(x+35*side, mid+25, value, 22, anchor=anchor)
        if polar:
            self.text(x-40, mid-14, '+', 23)

    def diode_up(self, x, top, bottom, label, value, side=1):
        mid = (top+bottom)/2
        self.line(x, top, x, mid-22)
        self.line(x-24, mid-22, x+24, mid-22, width=4)
        self.items.append(f'<polygon points="{x},{mid-18} {x-22},{mid+20} {x+22},{mid+20}" fill="white" stroke="{INK}" stroke-width="3"/>')
        self.line(x, mid+20, x, bottom)
        a = 'start' if side > 0 else 'end'
        self.text(x+35*side, mid-10, label, 22, bold=True, anchor=a)
        self.text(x+35*side, mid+22, value, 21, anchor=a)
        self.text(x-12, top+31, 'K', 19, GREY, anchor='end')
        self.text(x-12, bottom-15, 'A', 19, GREY, anchor='end')

    def mosfet(self, drain_x, gate_y, label):
        gx, cx = drain_x-70, drain_x-46
        self.line(gx, gate_y-40, gx, gate_y+40, BLUE, 4)
        for ya, yb in [(-40, -22), (-10, 10), (22, 40)]:
            self.line(cx, gate_y+ya, cx, gate_y+yb, width=4)
        self.line(cx, gate_y-40, drain_x, gate_y-40, RED, 4)
        self.line(cx, gate_y+40, drain_x, gate_y+40, width=4)
        self.text(gx-14, gate_y-20, 'G', 21, BLUE, anchor='end')
        self.text(drain_x+17, gate_y-60, 'D', 21, RED)
        self.text(drain_x+17, gate_y+65, 'S', 21)
        self.text(drain_x+65, gate_y-5, label, 24, bold=True)
        self.text(drain_x+65, gate_y+29, 'IRLB8748', 22, bold=True)
        self.text(drain_x+65, gate_y+60, 'N-MOSFET', 20)

    def note_box(self, x, y, w, title, lines, red=False, height=220):
        self.rect(x, y, w, height, '#fff7f4' if red else '#f4f8fb', '#dbe3e9', 12)
        self.text(x+25, y+40, title, 25, RED if red else BLUE, True)
        for i, t in enumerate(lines):
            self.text(x+25, y+82+i*35, t, 23)

    def save(self, name):
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">' + ''.join(self.items) + '</svg>'
        (ROOT / f'{name}.svg').write_text(svg, encoding='utf-8')
        source = pymupdf.open(stream=svg.encode('utf-8'), filetype='svg')
        pdf = pymupdf.open('pdf', source.convert_to_pdf())
        pdf.save(ROOT / f'{name}.pdf')
        pdf[0].get_pixmap(alpha=False).save(ROOT / f'{name}.png')
        print(f'Created {name}.svg, .pdf and .png')


def stirring():
    d = Drawing('Stirring subsystem | example electrical schematic',
                'CSEEE-21  /  5 V motor + Hall encoder  /  Nano ESP32  /  example parts and values, untested')
    for x, label in [(90, '1  HALL SPEED FEEDBACK'), (950, '2  LOCAL CONTROL'), (1400, '3  GATE DRIVE'), (1930, '4  MOTOR POWER')]:
        d.text(x, 200, label, 25, RED if x == 1930 else BLUE, True)

    # Hall output is referenced to the unswitched assembly ground.
    d.rect(100, 350, 400, 220, '#edf5fa', BLUE, 14)
    d.text(300, 396, 'H1  Hall encoder', 28, bold=True, anchor='middle')
    d.text(300, 441, '70 pulses / output revolution', 24, anchor='middle')
    d.text(300, 484, 'Same assembly as M1', 23, GREY, anchor='middle')
    d.text(300, 526, 'Hall ground stays connected', 23, BLUE, anchor='middle')
    d.line(300, 350, 300, 280, RED)
    d.text(300, 255, '+5 V from Nano VBUS', 23, RED, True, 'middle')
    d.line(300, 570, 300, 640)
    d.ground(300, 640)
    d.line(500, 420, 640, 420, BLUE)
    d.dot(555, 420, BLUE)
    d.rv(555, 265, 420, 'R1', '10 kohm*', side=1, shift=-25)
    d.text(555, 245, '+5 V', 21, RED, anchor='middle')
    d.text(100, 734, '* Fit pull-up only if Hall output needs it.', 22, GREY)
    d.text(100, 768, 'Buffer protects 3.3 V logic from a 5 V signal.', 22, GREY)
    d.text(100, 802, 'Keep motor / sensor cable short.', 22, GREY)
    d.rect(640, 370, 250, 110, '#f0f6f4', BLUE, 10)
    d.text(765, 404, 'U2  74LVC1G17', 23, BLUE, True, 'middle')
    d.text(655, 453, 'A (2)', 20)
    d.text(875, 453, 'Y (4)', 20, anchor='end')
    d.line(765, 370, 765, 295, BLUE)
    d.text(765, 272, '+3.3 V (5)', 23, BLUE, anchor='middle')
    d.line(765, 480, 765, 545)
    d.ground(765, 545)
    d.text(805, 528, 'GND (3)', 20, GREY)
    d.line(890, 420, 950, 420, BLUE)
    d.text(900, 389, '3.3 V', 21, BLUE)
    d.line(605, 885, 605, 850, BLUE)
    d.text(605, 827, '+3.3 V', 21, BLUE, anchor='middle')
    d.cap(605, 885, 1005, 'C4', '100 nF')
    d.ground(605, 1005)
    d.text(100, 1055, 'C4 next to U2. Pin numbers assume SOT-23-5 / DBV.', 21, GREY)
    d.text(100, 1090, 'U2 input accepts up to 5.5 V; output uses 3.3 V supply.', 21, GREY)

    d.rect(950, 350, 340, 470, '#edf5fa', BLUE, 14)
    d.text(965, 453, 'D2: interrupt input', 22, BLUE, True)
    d.text(1120, 520, 'U1', 27, BLUE, True, 'middle')
    d.text(1120, 564, 'Arduino', 29, bold=True, anchor='middle')
    d.text(1120, 606, 'Nano ESP32', 29, bold=True, anchor='middle')
    d.text(1120, 650, 'USB powered', 24, GREY, anchor='middle')
    d.text(1275, 707, 'D10: PWM', 22, BLUE, True, 'end')
    d.text(1120, 757, 'RPM measurement + PI', 23, anchor='middle')
    d.text(1120, 792, 'Soft-start / missing-pulse stop', 21, anchor='middle')
    d.line(1120, 820, 1120, 900)
    d.ground(1120, 900)
    d.text(950, 1000, 'D5 / A0 remain available for heating.', 22, GREY)
    d.text(950, 1036, 'D10 and D2 are board pin labels.', 22, GREY)

    d.rect(1400, 630, 260, 130, '#f0f6f4', BLUE, 10)
    d.text(1530, 665, 'U3  TC4420', 25, BLUE, True, 'middle')
    d.text(1413, 710, 'IN (2)', 20)
    d.text(1647, 710, 'OUT (6,7)', 20, anchor='end')
    d.text(1530, 745, 'non-inverting', 20, GREY, anchor='middle')
    d.line(1290, 680, 1400, 680, BLUE)
    d.dot(1345, 680, BLUE)
    d.rv(1345, 730, 850)
    d.line(1345, 680, 1345, 730)
    d.line(1345, 850, 1345, 900)
    d.ground(1345, 900)
    d.text(1380, 825, 'R2', 22, bold=True)
    d.text(1380, 852, '100 kohm', 22)
    d.line(1530, 630, 1530, 410, RED)
    d.text(1530, 350, '+5 V VBUS', 23, RED, True, 'middle')
    d.text(1530, 381, 'VDD pins 1,8', 20, GREY, anchor='middle')
    d.line(1530, 410, 1710, 410, RED)
    d.dot(1530, 410, RED)
    d.cap(1710, 410, 530, 'C3', '1 uF')
    d.ground(1710, 530)
    d.line(1530, 760, 1530, 900)
    d.ground(1530, 900)
    d.text(1570, 875, 'GND (4,5)', 20, GREY)
    d.rh(1660, 1900, 680, 'R3', '100 ohm')
    d.line(1900, 680, 2010, 680, BLUE)
    d.dot(1900, 680, BLUE)
    d.rv(1900, 730, 850, 'R4', '100 kohm', side=-1)
    d.line(1900, 680, 1900, 730)
    d.line(1900, 850, 1900, 900)
    d.ground(1900, 900)

    # +5 V supply is the same named net used by the Hall sensor and driver.
    d.text(2080, 257, '+5 V from Nano VBUS', 24, RED, True, 'middle')
    d.text(2080, 289, 'USB current budget must be checked', 21, GREY, anchor='middle')
    d.line(2080, 305, 2080, 340, RED, 4)
    d.line(1830, 340, 2270, 340, RED, 4)
    d.dot(2080, 340, RED)
    d.dot(1830, 340, RED)
    d.line(2080, 340, 2080, 405, RED, 4)
    d.circle(2080, 450, 45)
    d.text(2080, 462, 'M', 31, bold=True, anchor='middle')
    d.text(1995, 450, 'M1', 23, bold=True, anchor='end')
    d.text(1995, 527, '5 V DC motor', 23, anchor='end')
    d.line(2080, 495, 2080, 640, RED, 4)
    d.line(2080, 580, 2270, 580, RED, 3)
    d.dot(2080, 580, RED)
    d.diode_up(2270, 340, 580, 'D1', '1N5822', side=-1)
    d.cap(1830, 340, 520, '', '', side=-1, polar=True)
    d.text(1830, 285, 'C1', 22, bold=True, anchor='middle')
    d.text(1830, 315, '470 uF, 10 V', 22, anchor='middle')
    d.ground(1830, 520)
    d.text(2000, 1000, 'D1 band (K) to +5 V.', 23, RED, True)
    d.mosfet(2080, 680, 'Q1')
    d.line(2080, 720, 2080, 900, width=4)
    d.ground(2080, 900)
    d.text(1960, 1040, 'Switch only the motor return;', 23, GREY)
    d.text(1960, 1075, 'never switch Hall ground.', 23, GREY)

    d.line(65, 1130, 2335, 1130, '#dbe3e9', 2)
    d.note_box(65, 1160, 1110, 'Measure the geared output shaft directly', [
        'RPM = 60 x pulse_frequency / 70.  No further 10:1 correction.',
        'At 1,000 RPM: approximately 1,167 pulses/s; period 857 us.',
        'Measure pulse period; a 10 ms count has coarse 85.7 RPM steps.',
        'Trial target: 800 RPM. Control tuning must use measured response.'
    ])
    d.note_box(1205, 1160, 1130, 'Important differences from older slides', [
        'Motor handout: approximately 1,000 RPM max at 5 V.',
        'Confirm the older 1,500 RPM requirement with teaching staff.',
        'VBUS supplies 5 V only when USB powered; do not add 6/12 V.',
        'U2 / U3 are added interface parts; kit availability unconfirmed.'
    ], red=True)
    d.text(65, 1430, 'Example design. All grounds common; keep motor-current return separate from sensor wiring. C1 close to assembly supply.', 23, GREY)
    d.text(65, 1470, 'Gate driver pin 3 NC. Motor starting/stall current and USB/VBUS capacity are not supplied; verify before energising.', 22, GREY)
    d.save('Stirring_Subsystem_Schematic')


def ph():
    d = Drawing('pH subsystem | example electrical schematic',
                'CSEEE-21  /  SEN0161 conditioner  /  two 6 V dosing pumps  /  Nano ESP32  /  illustrative, untested', 1800)
    d.text(90, 200, '1  CONDITION AND SCALE THE SENSOR SIGNAL', 25, BLUE, True)
    d.text(1340, 200, '2  TWO INDEPENDENT PUMP POWER STAGES', 25, RED, True)
    # Probe and the existing high impedance conditioning board.
    d.rect(85, 380, 210, 190, '#edf5fa', BLUE, 12)
    d.text(190, 425, 'PH-100ATC', 24, bold=True, anchor='middle')
    d.text(190, 463, 'pH probe', 25, bold=True, anchor='middle')
    d.text(190, 510, 'in vessel', 23, GREY, anchor='middle')
    d.line(295, 470, 385, 470, BLUE)
    d.text(340, 445, 'BNC', 21, BLUE, anchor='middle')
    d.rect(385, 370, 300, 210, '#edf5fa', BLUE, 12)
    d.text(535, 420, 'U2  SEN0161', 27, bold=True, anchor='middle')
    d.text(535, 464, 'Existing pH', 25, anchor='middle')
    d.text(535, 499, 'conditioner board', 25, anchor='middle')
    d.text(670, 550, 'A: analog out', 20, BLUE, anchor='end')
    d.line(535, 370, 535, 290, RED)
    d.text(535, 263, '+5.00 V regulated', 23, RED, True, 'middle')
    d.line(535, 580, 535, 635)
    d.ground(535, 635)
    d.line(685, 520, 710, 520, BLUE)
    d.rh(710, 950, 520, 'R1', '10 kohm, 1%')
    d.dot(950, 520, BLUE)
    d.line(950, 520, 1040, 520, BLUE)
    d.rv(950, 575, 695, 'R2', '10 kohm, 1%', side=-1)
    d.line(950, 520, 950, 575)
    d.line(950, 695, 950, 740)
    d.ground(950, 740)
    d.cap(1040, 520, 690, 'C1', '100 nF')
    d.ground(1040, 690)
    d.line(1040, 520, 1170, 520, BLUE)
    d.dot(1040, 520, BLUE)
    d.text(770, 825, 'Divider: V_ADC = 0.5 x V_A', 25, BLUE, True)
    d.text(770, 862, '0-5 V input assumption -> 0-2.5 V ADC', 22, GREY)
    d.text(90, 735, 'Use the supplied conditioner; do not connect', 22, GREY)
    d.text(90, 770, 'the raw glass electrode directly to an ADC.', 22, GREY)
    # Sensor local bypass on named regulated 5 V net.
    d.text(230, 920, '+5.00 V', 22, RED, anchor='middle')
    d.line(230, 940, 430, 940, RED)
    d.cap(230, 940, 1060, 'C2', '100 nF', side=-1)
    d.cap(430, 940, 1060, 'C3', '10 uF, 10 V', polar=True)
    d.ground(230, 1060)
    d.ground(430, 1060)
    d.text(90, 1135, 'C2/C3 next to U2; keep pump noise out of its supply.', 21, GREY)

    # Same system controller as heating/stirring, not additional boards.
    d.rect(1170, 370, 330, 720, '#edf5fa', BLUE, 14)
    d.text(1185, 550, 'A1: pH input', 22, BLUE, True)
    d.text(1335, 640, 'U1', 27, BLUE, True, 'middle')
    d.text(1335, 680, 'Arduino', 29, bold=True, anchor='middle')
    d.text(1335, 720, 'Nano ESP32', 29, bold=True, anchor='middle')
    d.text(1335, 765, 'USB powered', 23, GREY, anchor='middle')
    d.text(1485, 487, 'D6: ACID', 22, RED, True, 'end')
    d.text(1485, 1047, 'D9: BASE', 22, BLUE, True, 'end')
    d.text(1335, 830, 'Dose one pump', 23, anchor='middle')
    d.text(1335, 866, 'Wait for mixing', 23, anchor='middle')
    d.text(1335, 902, 'Re-measure pH', 23, anchor='middle')
    d.line(1335, 1090, 1335, 1180)
    d.ground(1335, 1180)

    # Two identical TC4420-based channels. Each has its own gate and flyback diode.
    def pump_channel(y, name, gpio, qref, dref, uref, rstart, branch_colour):
        # y is the gate / MCU output level. Named +6 V is common to both channels.
        d.line(1500, y, 1610, y, branch_colour)
        d.dot(1550, y, branch_colour)
        d.rv(1550, y+45, y+155)
        d.line(1550, y, 1550, y+45)
        d.ground(1550, y+155)
        d.text(1600, y+185, f'R{rstart} 100 kohm to GND', 20, GREY)
        d.rect(1610, y-60, 240, 130, '#f0f6f4', BLUE, 10)
        d.text(1730, y-20, f'{uref}  TC4420', 24, BLUE, True, 'middle')
        d.text(1623, y+30, 'IN (2)', 19)
        d.text(1837, y+30, 'OUT (6,7)', 19, anchor='end')
        d.text(1730, y+59, 'non-inverting', 19, GREY, anchor='middle')
        d.line(1730, y-60, 1730, y-110, RED)
        d.text(1730, y-132, '+6 V (1,8)', 21, RED, anchor='middle')
        d.line(1730, y+70, 1730, y+130)
        d.ground(1730, y+130)
        d.text(1765, y+122, 'GND (4,5)', 19, GREY)
        d.rh(1850, 2030, y, f'R{rstart+1}', '100 ohm')
        d.line(2030, y, 2080, y, BLUE)
        d.dot(2030, y, BLUE)
        d.rv(2030, y+45, y+155, f'R{rstart+2}', '100 kohm', side=-1)
        d.line(2030, y, 2030, y+45)
        d.ground(2030, y+155)
        d.mosfet(2150, y, qref)
        d.line(2150, y+40, 2150, y+155, width=4)
        d.ground(2150, y+155)
        # Pump and flyback loop.
        top = y-290
        d.text(2150, top-45, '+6 V PUMP SUPPLY', 22, RED, True, 'middle')
        d.line(2150, top-26, 2150, top, RED, 4)
        d.line(2150, top, 2330, top, RED, 3)
        d.dot(2150, top, RED)
        d.line(2150, top, 2150, y-205, RED, 4)
        d.circle(2150, y-160, 45)
        d.text(2150, y-148, 'M', 31, bold=True, anchor='middle')
        d.text(2075, y-180, name, 23, branch_colour, True, 'end')
        d.text(2075, y-145, '6 V, 1 A', 22, anchor='end')
        d.line(2150, y-115, 2150, y-40, RED, 4)
        d.line(2150, y-78, 2330, y-78, RED)
        d.dot(2150, y-78, RED)
        d.diode_up(2330, top, y-78, dref, '1N5822', side=-1)

    pump_channel(520, 'ACID', 'D6', 'Q1', 'D1', 'U3', 3, RED)
    pump_channel(1080, 'ALKALI', 'D9', 'Q2', 'D2', 'U4', 6, BLUE)

    d.line(65, 1310, 2335, 1310, '#dbe3e9', 2)
    d.note_box(65, 1340, 1095, 'Supply decoupling: these are electrical connections', [
        'U3: C4 100 nF + C5 1 uF across +6 V and GND at the IC.',
        'U4: C6 100 nF + C7 1 uF across +6 V and GND at the IC.',
        'Pump rail: C8 470 uF / 16 V + C9 100 nF to GND.',
        'Shown explicitly on sheet 2 of the pH PDF.'
    ])
    d.note_box(1190, 1340, 1145, 'Example dosing logic: firmware interlock required', [
        'Target pH 5.0: below 4.9 -> ALKALI; above 5.1 -> ACID.',
        'Inside band: both OFF. Both OFF while mixing / settling.',
        'Ramp starts; calibrate dose volume and wait before re-dosing.',
        'This hardware does not independently block both pumps ON.'
    ], red=True)
    d.text(65, 1615, 'Pump supply: regulated 6 V, >=3 A example; actual start/stall currents must be checked. Pump current must not flow through the Nano.', 23, GREY)
    d.text(65, 1655, 'D1/D2 band (K) to +6 V. All GND symbols common. Keep pump returns separate from the pH analog return.', 23, GREY)
    d.text(65, 1695, 'Drivers are added example parts, not confirmed kit contents. TC4420 pin 3 NC. A1 / D6 / D9 are board labels, not raw GPIO numbers.', 22, GREY)
    d.text(65, 1735, 'For normal operation only one pump may run. Invalid pH, loss of stirring or dose/time limits -> stop both pumps.', 22, GREY)
    d.save('pH_Subsystem_Schematic')

    # A second sheet keeps the main schematic legible without omitting decoupling.
    p = Drawing('pH subsystem | supply wiring and local decoupling',
                'Sheet 2  /  same named nets as sheet 1  /  keep sensor supply and high-current pump paths separate', 1500)
    p.text(90, 210, 'CLEAN SENSOR SUPPLY', 28, BLUE, True)
    p.text(90, 270, 'Regulated +5.00 V -> SEN0161 + terminal', 27)
    p.text(90, 320, 'Supply negative -> common GND', 26)
    p.text(90, 370, 'C2 100 nF and C3 10 uF are shown on sheet 1.', 25, GREY)
    p.text(1300, 210, 'PUMP SUPPLY', 28, RED, True)
    p.text(1300, 270, 'Regulated +6 V, >=3 A capability (example)', 27)
    p.text(1300, 320, 'Feeds both pump + terminals and U3/U4 VDD.', 25)
    p.text(1300, 370, 'Separate heater demand is not included in this rating.', 25, GREY)

    # Each capacitor is shown on a named net rather than a layout wiring prescription.
    for start, uref, c1, c2 in [(220, 'U3', 'C4', 'C5'), (1050, 'U4', 'C6', 'C7')]:
        p.text(start, 480, f'{uref} DRIVER BYPASS', 26, BLUE, True)
        p.line(start+100, 550, start+430, 550, RED)
        p.text(start+100, 520, '+6 V', 24, RED, True)
        p.cap(start+100, 550, 750, c1, '100 nF', side=-1)
        p.cap(start+430, 550, 750, c2, '1 uF, >=16 V')
        p.ground(start+100, 750)
        p.ground(start+430, 750)
        p.text(start, 850, f'At {uref} pins 1,8 (+6 V) and 4,5 (GND).', 24)
    p.text(1900, 480, 'BULK BYPASS', 26, RED, True)
    p.line(1930, 550, 2220, 550, RED)
    p.text(1930, 520, '+6 V', 24, RED, True)
    p.cap(1930, 550, 750, 'C8', '470 uF, 16 V', side=-1, polar=True)
    p.cap(2220, 550, 750, 'C9', '100 nF', side=1)
    p.ground(1930, 750)
    p.ground(2220, 750)
    p.text(1860, 850, 'Near pump supply entry.', 24)
    p.note_box(90, 980, 2220, 'Grounding and power notes', [
        'Return Q1/Q2 source current directly to the pump supply negative. Route the pH conditioner return separately to the common point.',
        'The Nano is USB powered. Connect its GND to the common point. Never connect the 6 V pump rail to Nano VBUS or GPIO.',
        'Do not connect external +5 V to VBUS while USB power is present. Separate named rails are joined only at GND.',
        'Use lab-approved branch protection sized from measured startup/stall current, conductor ratings and supply fault current.'
    ], height=240)
    p.text(90, 1320, 'C8 positive terminal -> +6 V; negative -> GND. C3 positive -> +5 V; negative -> GND. C4-C7/C9 may be ceramic.', 24, GREY)
    p.text(90, 1370, 'Illustrative design: no physical measurements, calibration or pump-flow test has been performed.', 24, GREY)
    p.save('pH_Subsystem_Supply_Detail')

    first = pymupdf.open(ROOT / 'pH_Subsystem_Schematic.pdf')
    second = pymupdf.open(ROOT / 'pH_Subsystem_Supply_Detail.pdf')
    first.insert_pdf(second)
    temp = ROOT / 'pH_Subsystem_Schematic_two_sheets.pdf'
    first.save(temp)
    first.close()
    temp.replace(ROOT / 'pH_Subsystem_Schematic.pdf')


if __name__ == '__main__':
    stirring()
    ph()
    for rpm in (500, 800, 1000, 1500):
        f = rpm * 70 / 60
        print(f'{rpm} RPM -> {f:.3f} Hz, pulse period {1e6/f:.3f} us')
    print('pH divider: 5 V input -> 2.5 V ADC; effective RC = 5 kohm * 100 nF = 0.5 ms')
