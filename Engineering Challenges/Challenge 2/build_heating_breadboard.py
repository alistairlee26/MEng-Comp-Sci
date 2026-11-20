from pathlib import Path
from html import escape
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

OUT = ROOT / 'Circuit_Diagram_Examples' / 'Heating_Breadboard_6V'
OUT.mkdir(parents=True, exist_ok=True)
W, H = 2300, 1500
INK, MUTED = '#1c2d3b', '#526676'
RED, BLACK, BLUE, ORANGE, GREEN = '#c44138', '#263b47', '#1672b1', '#b86a13', '#188466'


class Drawing:
    def __init__(self, title, subtitle, number):
        self.parts = []
        self.rect(0, 0, W, H, '#ffffff', '#ffffff')
        self.text(70, 78, title, 43, bold=True)
        self.text(70, 124, subtitle, 25, MUTED)
        self.line([(70, 155), (2230, 155)], '#d7e1e7', 2)
        self.text(2230, 1460, f'{number} / 3', 22, MUTED, anchor='end')

    def text(self, x, y, value, size=23, colour=INK, bold=False, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{colour}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(value)}</text>')

    def rect(self, x, y, w, h, fill='white', stroke=INK, radius=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')

    def circle(self, x, y, r, fill, stroke=None):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or fill}" stroke-width="2"/>')

    def line(self, pts, colour=INK, width=4, halo=False):
        p = ' '.join(f'{x},{y}' for x, y in pts)
        if halo:
            self.parts.append(f'<polyline points="{p}" fill="none" stroke="white" stroke-width="{width+6}" stroke-linejoin="round" stroke-linecap="round"/>')
        self.parts.append(f'<polyline points="{p}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>')

    def tag(self, x, y, label, colour):
        self.circle(x, y, 17, colour)
        self.text(x, y+6, label, 18, 'white', True, 'middle')

    def svg(self):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + ''.join(self.parts) + '</svg>'


YS = {c: 500 + i*30 for i, c in enumerate('ABCDE')}
YS.update({c: 740 + i*30 for i, c in enumerate('FGHIJ')})


def xy(hole):
    match = re.fullmatch(r'([A-J])(\d+)', hole)
    assert match, hole
    c, r = match[1], int(match[2])
    assert 1 <= r <= 30
    return 550 + (r-1)*46, YS[c]


# Each endpoint gets its own physical hole. Five holes in one numbered strip
# connect internally; the two sides of the centre gap remain separate.
JUMPERS = [
    ('J1', 'B6', 'B18', BLACK, 'Ground: sensor section to driver'),
    ('J2', 'C6', 'G22', BLACK, 'Ground for input pull-down'),
    ('J3', 'C12', 'C15', RED, '+6 V to driver pin 8'),
    ('J4', 'D15', 'G15', RED, 'Join driver VDD pins 1 and 8'),
    ('J5', 'D18', 'G18', BLACK, 'Join driver GND pins 4 and 5'),
    ('J6', 'D16', 'D17', GREEN, 'Join driver output pins 7 and 6'),
    ('J7', 'J18', 'J29', BLACK, 'Driver ground to external ground lead'),
]
EXTERNAL = [
    ('N1', 'Nano.3V3', 'B3', RED, 'Nano 3V3'),
    ('N2', 'Nano.A0', 'B9', BLUE, 'Nano A0'),
    ('N3', 'Nano.GND', 'A6', BLACK, 'Nano GND'),
    ('N4', 'Nano.D5', 'I16', ORANGE, 'Nano D5'),
    ('P1', 'F2.OUT', 'A12', RED, 'Fused +6 V driver branch (page 2)'),
    ('P2', 'STAR.GND', 'H29', BLACK, 'Supply-negative star point (page 2)'),
    ('P3', 'Q1.G', 'B23', GREEN, 'MOSFET gate (page 2)'),
    ('T1', 'TH1.1', 'D9', BLUE, 'One thermistor lead'),
    ('T2', 'TH1.2', 'D6', BLACK, 'Other thermistor lead'),
]
PASSIVES = [
    ('R1', 'E3', 'E9', '10 kΩ, 1%', 'Divider resistor; selected for this design'),
    ('R2', 'H16', 'H22', '100 kΩ', 'Driver-input pull-down'),
    ('R3', 'C17', 'C23', '100 Ω', 'MOSFET gate series resistor'),
    ('C1', 'A15', 'A18', '1 µF ceramic, ≥16 V', 'Driver supply bypass; non-polar'),
]
PINS = {1:'F15', 2:'F16', 3:'F17', 4:'F18', 5:'E18', 6:'E17', 7:'E16', 8:'E15'}


def validate():
    # Check row connectivity independently of the graphics, including supply
    # isolation, duplicate driver pins, signal path, and occupied-hole conflicts.
    parent = {}
    used = {}
    polygon = [xy(PINS[n]) for n in range(1,9)]
    area = sum(polygon[i][0]*polygon[(i+1)%8][1] - polygon[(i+1)%8][0]*polygon[i][1] for i in range(8))
    assert area < 0, 'PDIP numbers must run counterclockwise in top view'
    assert PINS[1] == 'F15' and PINS[8] == 'E15', 'Notch-left top-view orientation'
    def node(s):
        m = re.fullmatch(r'([A-J])(\d+)', s)
        return f'{"AE" if m[1] <= "E" else "FJ"}{m[2]}' if m else s
    def find(n):
        parent.setdefault(n, n)
        if parent[n] != n:
            parent[n] = find(parent[n])
        return parent[n]
    def join(a, b):
        a, b = find(node(a)), find(node(b))
        parent[a] = b
    def occupy(h, ref):
        if re.fullmatch(r'[A-J]\d+', h):
            assert h not in used, f'Hole {h} shared by {used.get(h)} and {ref}'
            used[h] = ref
    for ref, a, b, *_ in JUMPERS + EXTERNAL:
        occupy(a, ref); occupy(b, ref); join(a, b)
    for ref, a, b, *_ in PASSIVES:
        occupy(a, ref); occupy(b, ref)
    for pin, h in PINS.items():
        occupy(h, f'U2.{pin}')
    def same(a, b):
        assert find(node(a)) == find(node(b)), f'Unconnected: {a}, {b}'
    for a, b in [('Nano.3V3','E3'), ('Nano.A0','E9'), ('Nano.A0','TH1.1'),
                 ('Nano.GND','TH1.2'), ('Nano.GND','STAR.GND'),
                 ('Nano.D5','F16'), ('Nano.D5','H16'), ('F2.OUT','F15'),
                 ('F2.OUT','E15'), ('STAR.GND','F18'), ('STAR.GND','E18'),
                 ('STAR.GND','H22'), ('E16','E17'), ('E17','C17'), ('Q1.G','C23')]:
        same(a,b)
    isolated = ['Nano.3V3', 'Nano.A0', 'Nano.GND', 'Nano.D5', 'F2.OUT', 'E17', 'Q1.G', 'F17']
    assert len({find(node(n)) for n in isolated}) == len(isolated), 'Short between distinct nets'
    assert find(node('E3')) != find(node('E9'))
    assert find(node('C17')) != find(node('C23'))
    return {'occupied_holes': len(used), 'checks': 'PASS: no occupied-hole conflicts; supply and signal nets distinct; duplicate driver pins connected; NC isolated', 'holes':used}


report = validate()
(OUT/'Connectivity_Check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

# PAGE 1: top-down physical placement.
d = Drawing('Heating subsystem · breadboard placement', 'Nano ESP32 + IRLB8748 + TC4420 PDIP-8  |  regulated 6 V heater supply  |  USB-powered Nano', 1)
d.text(70, 198, 'Follow hole labels, not physical scale. Colour crossings are insulated wires; connection points are their ends.', 25, MUTED)
d.rect(495, 360, 1460, 650, '#f6f4ee', '#c7c6bd', 25)
d.rect(525, 650, 1400, 60, '#dedbd2', '#dedbd2', 10)
d.text(565, 686, 'CENTRE GAP', 19, '#a09c91')
for yy in [400,430,930,960]:
    for r in range(1,31):
        xx = xy(f'A{r}')[0]
        d.circle(xx, yy, 5, '#d0cec6')
d.text(1880, 345, 'POWER RAILS UNUSED', 19, MUTED, anchor='end')
for letter in 'ABCDEFGHIJ':
    yy = YS[letter]
    d.text(520, yy+6, letter, 22, MUTED, True, 'end')
    d.text(1915, yy+6, letter, 22, MUTED, True)
    for r in range(1,31):
        xx = xy(f'{letter}{r}')[0]
        d.circle(xx, yy, 6, '#a5a49c')
for r in range(1,31):
    xx = xy(f'A{r}')[0]
    for yy in [477,903]:
        d.text(xx, yy, str(r), 19, MUTED, anchor='middle')

# On-board insulated jumpers: route the supply/ground bridges around the IC.
routes = {
    'J1': [xy('B6'), (780,1038), (1332,1038), xy('B18')],
    'J2': [xy('C6'), (780,1070), (1495,1070), (1495,770), xy('G22')],
    'J3': [xy('C12'), xy('C15')],
    'J4': [xy('D15'), (1166,590), (1166,770), xy('G15')],
    'J5': [xy('D18'), (1370,590), (1370,770), xy('G18')],
    'J6': [xy('D16'), xy('D17')],
    'J7': [xy('J18'), xy('J29')],
}
for ref,a,b,col,_ in JUMPERS:
    d.line(routes[ref], col, 6, halo=True)
    for h in [a,b]:
        d.circle(*xy(h), 6, col)

# Nano is connected by jumper leads, not inserted into this breadboard.
d.rect(125, 365, 200, 470, '#17796d', '#10564e', 13)
d.rect(190, 328, 70, 48, '#d3dbe1', '#73818a', 7)
d.text(225, 313, 'USB-C to computer', 21, MUTED, anchor='middle')
d.text(225, 865, 'NANO ESP32', 25, bold=True, anchor='middle')
d.text(225, 897, 'Top view · USB at top', 20, MUTED, anchor='middle')
left = ['D13','3V3','B0','A0','A1','A2','A3','A4','A5','A6','A7','VBUS','B1','GND','VIN']
right = ['D12','D11','D10','D9','D8','D7','D6','D5','D4','D3','D2','GND','RESET','D0/RX','D1/TX']
pins = {}
for names,side in [(left,'L'),(right,'R')]:
    for i,name in enumerate(names):
        yy = 405+i*28
        xx = 110 if side=='L' else 340
        d.rect(xx-5, yy-5, 10, 10, '#d7b55c', '#967d3f')
        d.line([(xx,yy), (125 if side=='L' else 325,yy)], '#a8b6b2', 3)
        d.text(140 if side=='L' else 310, yy+6, name, 16, 'white', name in ['3V3','A0','D5','GND'], 'start' if side=='L' else 'end')
        pins[side+name] = (xx,yy)

nano_routes = {
    'N1':[pins['L3V3'],(55,pins['L3V3'][1]),(55,250),(642,250),xy('B3')],
    'N2':[pins['LA0'],(30,pins['LA0'][1]),(30,225),(918,225),xy('B9')],
    'N3':[pins['RGND'],(430,pins['RGND'][1]),(430,275),(780,275),xy('A6')],
    'N4':[pins['RD5'],(390,pins['RD5'][1]),(390,1135),(1240,1135),xy('I16')],
}
for ref,_,h,col,_ in EXTERNAL[:4]:
    d.line(nano_routes[ref], col, 5, halo=True)
    d.circle(*xy(h),6,col)
    x,y = xy(h)
    d.tag(x-16,y-22,ref[-1],col)

# External driver supply, return and gate lead, kept separate from heater current.
d.rect(2000, 360, 250, 680, '#f4f8fa', '#d2dce3', 12)
d.text(2125, 404, 'TO PAGE 2', 24, bold=True, anchor='middle')
d.line([xy('A12'),(1056,300),(2070,300),(2070,465)],RED,5,True)
d.text(2030, 505, 'P1 · fused +6 V', 22, RED, True)
d.text(2030, 537, 'driver power only', 20, MUTED)
d.line([xy('B23'),(1590,530),(1590,1110),(1980,1110),(1980,745),(2030,745)],GREEN,5,True)
d.text(2030, 788, 'P3 · to Q1 gate', 22, GREEN, True)
d.line([xy('H29'),(1967,800),(1967,945),(2030,945)],BLACK,5,True)
d.text(2030, 989, 'P2 · star GND', 22, BLACK, True)
for h,col in [('A12',RED),('B23',GREEN),('H29',BLACK)]:
    d.circle(*xy(h),6,col)

# Driver with the package notch toward row 15 (left in this view).
x15,yE = xy('F15'); x18,_ = xy('F18')
d.rect(x15-15,650,x18-x15+30,60,'#283139','#182229',7)
d.circle(x15-15,680,11,'#f6f4ee')
d.text((x15+x18)/2,688,'TC4420',20,'white',True,'middle')
for pin,h in PINS.items():
    x,y = xy(h)
    d.line([(x,y),(x,650 if h[0]=='E' else 710)],'#9aa4ac',5)
    d.text(x,y+20 if h[0]=='E' else y-10,str(pin),16,MUTED,True,'middle')
d.text(x15-35,690,'◀',22,INK,True,'end')

def draw_resistor(a,b,label):
    x1,y = xy(a); x2,_ = xy(b); m=(x1+x2)/2
    d.line([(x1,y),(m-45,y)], '#72786e', 4)
    d.rect(m-45,y-14,90,28,'#e9d3ad','#a58c65',5)
    d.text(m,y+6,label,18,INK,True,'middle')
    d.line([(m+45,y),(x2,y)],'#72786e',4)
    for h in [a,b]: d.circle(*xy(h),5,'#72786e')

draw_resistor('E3','E9','10k')
draw_resistor('H16','H22','100k')
draw_resistor('C17','C23','100Ω')
# Non-polar ceramic bypass capacitor with two distinct leads.
x1,y = xy('A15'); x2,_ = xy('A18'); mid=(x1+x2)/2
d.line([(x1,y),(x1,465),(mid-16,465)],'#82715c',3)
d.line([(x2,y),(x2,465),(mid+16,465)],'#82715c',3)
d.circle(mid,465,22,'#dc9e40','#af7220')
d.text(mid,471,'1µ',16,'white',True,'middle')
for h in ['A15','A18']: d.circle(*xy(h),5,'#82715c')

# Thermistor is external: two interchangeable probe leads into D6 and D9.
d.line([xy('D6'),(780,600),(970,600),(970,1150)],BLACK,4,True)
d.line([xy('D9'),(918,585),(1005,585),(1005,1150)],BLUE,4,True)
d.rect(932,1150,110,45,'#f2f5f6','#869ba9',12)
d.text(987,1179,'TH1',23,BLUE,True,'middle')
d.text(987,1225,'10 kΩ NTC probe · either lead orientation',23,MUTED,anchor='middle')

d.line([(70,1260),(2230,1260)],'#d7e1e7',2)
for x,title,lines in [
    (70,'Place these parts',[ 'R1: E3–E9 · 10 kΩ, 1%', 'R2: H16–H22 · 100 kΩ', 'R3: C17–C23 · 100 Ω']),
    (805,'Driver orientation',[ 'TC4420 PDIP-8 · notch LEFT', 'Pins 1–4: F15, F16, F17, F18', 'Pins 8–5: E15, E16, E17, E18']),
    (1535,'Before applying power',[ 'C1: A15–A18 · 1 µF ceramic', 'Pin 3 / F17 stays unconnected', 'Heater and MOSFET stay off-board'])
]:
    d.text(x,1301,title,25,bold=True)
    for i,s in enumerate(lines): d.text(x,1340+i*34,s,23,MUTED)
page1=d.svg()

# PAGE 2: high-current circuit and MOSFET front-view wiring.
d = Drawing('Heating subsystem · external power wiring', 'Use regulated 6 V, rated ≥3 A  |  approximately 2 A / 12 W at full heater duty  |  heater current bypasses breadboard', 2)
d.text(70,205,'IRLB8748 front view: printed part number facing you, metal tab behind, legs downward.',27,bold=True)

# Physical MOSFET drawing on the right.
d.rect(1500,340,250,130,'#bec6cd','#6d7b85',12)
d.circle(1625,392,28,'white','#6d7b85')
d.rect(1475,450,300,300,'#25323a','#15232c',15)
d.text(1625,525,'IRLB8748',32,'white',True,'middle')
d.text(1625,571,'Q1 · front face',24,'#d6e0e5',anchor='middle')
d.text(1625,612,'TAB = DRAIN',22,'#d6e0e5',True,'middle')
for i,(x,l,col) in enumerate([(1520,'G',GREEN),(1625,'D',RED),(1730,'S',BLACK)],1):
    d.line([(x,750),(x,930)],'#8b969e',14)
    d.text(x,720,l,27,'white',True,'middle')

# Heater branch: positive -> F1 -> switch -> heater -> drain.
d.rect(95,300,340,180,'#f7fafc','#9bafbe',12)
d.text(265,350,'REGULATED SUPPLY',26,bold=True,anchor='middle')
d.text(265,392,'SET TO 6.0 V',30,RED,True,'middle')
d.text(265,432,'≥3 A continuous rating',23,MUTED,anchor='middle')
d.text(120,465,'+',25,RED,True)
d.text(410,465,'−',25,BLACK,True)
d.line([(135,480),(135,575),(435,575)],RED,10)
d.rect(435,552,160,46,'#fff4f0',RED,8)
d.text(515,584,'F1 · 3 A',23,RED,True,'middle')
d.line([(595,575),(690,575)],RED,10)
d.circle(690,575,6,RED); d.circle(790,575,6,RED)
d.line([(690,575),(765,530)],RED,8)
d.text(740,497,'SW1 · enable',24,bold=True,anchor='middle')
d.text(740,625,'DC-rated ≥5 A',22,MUTED,anchor='middle')
d.line([(790,575),(895,575)],RED,10)
d.rect(895,510,325,130,'#fff6ee','#b66b38',12)
d.text(1057,556,'HEATER H1',28,bold=True,anchor='middle')
d.text(1057,600,'3 Ω · 30 W rated',25,anchor='middle')
d.line([(1220,575),(1345,575),(1345,1090),(1625,1090),(1625,930)],RED,10)
d.text(1070,685,'6 V → about 2 A and 12 W',27,RED,True,anchor='middle')
d.text(1070,728,'Keep the heating element immersed.',23,MUTED,anchor='middle')

# Star ground at the PSU negative. Power-current path is a thick separate lead.
d.line([(410,480),(410,1195),(1900,1195),(1900,930),(1730,930)],BLACK,10,True)
d.circle(410,1195,11,BLACK)
d.text(420,1245,'STAR: supply negative terminal',25,BLACK,True)
d.text(1500,1245,'Thick direct return from SOURCE (leg 3)',24,BLACK,anchor='middle')

# Low-current driver branch: separate fuse protects thin jumper wiring.
d.circle(135,530,7,RED)
d.line([(135,530),(65,530),(65,900),(140,900)],RED,5)
d.rect(140,876,190,48,'#fff4f0',RED,8)
d.text(235,907,'F2 · 250 mA',23,RED,True,'middle')
d.line([(330,900),(540,900)],RED,5,True)
d.rect(540,840,520,180,'#f2f8fa','#b8cbd5',10)
d.text(565,880,'BREADBOARD CONNECTIONS',24,bold=True)
d.text(565,920,'P1: A12 ← fused +6 V (F2 output)',23,RED,True)
d.text(565,960,'P2: H29 ← STAR / supply negative',23,BLACK,True)
d.text(565,997,'P3: B23 → Q1 GATE (leg 1)',23,GREEN,True)
d.line([(410,1195),(470,1195),(470,955),(540,955)],BLACK,5,True)
d.line([(1060,990),(1180,990),(1180,930),(1520,930)],GREEN,5,True)

# Pull-down physically on the MOSFET side so loss of a gate lead leaves it off.
d.line([(1520,930),(1520,1105),(1450,1105)],GREEN,4,True)
d.rect(1300,1084,150,42,'#e9d3ad','#a58c65',5)
d.text(1375,1112,'R4 · 100k',22,bold=True,anchor='middle')
d.line([(1300,1105),(1265,1105),(1265,1160),(1900,1160)],BLACK,4,True)
d.line([(1900,1160),(1900,1195)],BLACK,4)
d.circle(1900,1160,6,BLACK)
d.text(2050,1090,'R4 connects G to S',24,bold=True,anchor='middle')
d.text(2050,1125,'at the MOSFET connector.',22,MUTED,anchor='middle')
for x,l,col,n in [(1520,'G',GREEN,'1'),(1625,'D',RED,'2'),(1730,'S',BLACK,'3')]:
    d.tag(x,962,n,col)
    d.text(x+25,1015,l,28,col,True)

d.line([(70,1300),(2230,1300)],'#d7e1e7',2)
d.text(70,1345,'Use insulated, secured screw terminals or a soldered adapter for Q1. The drawing shows electrical connections, not bare wire twists.',24,MUTED)
d.text(70,1383,'Heater leads, switch and terminals: rated ≥5 A DC. Fit F1 close to the supply. Driver leads use the separate F2 branch.',24,MUTED)
d.text(70,1421,'Do not select 12 V for this build, and do not connect +6 V to Nano 3V3, VBUS or any GPIO. Nano remains USB powered.',24,RED,True)
page2=d.svg()

# PAGE 3: printable connection list and first-power-up instructions.
d = Drawing('Heating subsystem · connection checklist', 'Coordinates match page 1 exactly  |  A–E share one numbered strip; F–J share another  |  no connection across the centre gap',3)

def table(x,y,width,head,rows,rowh=39):
    d.rect(x,y,width,44,'#eaf1f5','#d4dfe5',5)
    d.text(x+16,y+30,head,25,bold=True)
    for i,(a,b) in enumerate(rows):
        yy=y+44+i*rowh
        if i%2==0: d.rect(x,yy,width,rowh,'#f7f9fa','#f7f9fa')
        d.text(x+16,yy+27,a,22,bold=True)
        d.text(x+245,yy+27,b,22,MUTED)
    return y+44+len(rows)*rowh

table(70,200,1050,'COMPONENT LEADS',[(ref,f'{a} ↔ {b}  |  {val}') for ref,a,b,val,_ in PASSIVES]+[('Thermistor','D9 ↔ D6  |  10 kΩ NTC')])
table(1180,200,1050,'IC PINS · TC4420 PDIP-8',[(f'Pin {pin}',f'{h}  |  '+{1:'+6 V',2:'INPUT',3:'NC — leave empty',4:'GND',5:'GND',6:'OUTPUT',7:'OUTPUT',8:'+6 V'}[pin]) for pin,h in PINS.items()],35)
table(70,490,1050,'INSULATED JUMPER WIRES',[(ref,f'{a} ↔ {b}') for ref,a,b,_,_ in JUMPERS])
table(1180,580,1050,'EXTERNAL LEADS',[(ref,f'{label} → {h}') for ref,_,h,_,label in EXTERNAL[:7]],37)

table(70,850,1050,'MOSFET / POWER CONNECTIONS',[
    ('Gate · leg 1','B23; R4 100 kΩ to source'),
    ('Drain · leg 2','Heater return; tab is also drain'),
    ('Source · leg 3','Direct heavy lead to supply negative'),
    ('Heater +','Supply +6 V via F1 and SW1'),
    ('R4 · 100 kΩ','Across G and S at Q1 connector')],37)

d.text(1180,960,'FIRST POWER-UP',26,bold=True)
steps=[
    '1. Switch off and disconnect both power sources before wiring.',
    '2. Keep SW1 open; verify U2 notch and every hole in the tables.',
    '3. USB only: verify 3.3 V on B3 and about 1.65 V on B9 at 25°C.',
    '4. Set D5 LOW. Apply 6 V; G–S should be near 0 V.',
    '5. Heater disconnected: D5 HIGH should give about 6 V G–S.',
    '6. Return D5 LOW; power off, connect and immerse the heater.',
    '7. Reapply power, close SW1; check a short supervised test.'
]
for i,s in enumerate(steps): d.text(1180,1002+i*37,s,22,MUTED)
d.text(70,1183,'Design choices',25,bold=True)
d.text(70,1222,'R1 is 10 kΩ here; the whiteboard value was unclear.',23,MUTED)
d.text(70,1260,'D5 is used instead of D1, keeping TX available for UART.',23,MUTED)
d.text(70,1298,'TC4420 is an added part; do not omit it in this layout.',23,MUTED)
d.line([(70,1335),(2230,1335)],'#d7e1e7',2)
d.text(70,1377,'Use D5 / A0 board labels in code, not raw ESP32 GPIO numbers. At 6 V, PWM varies heater power from 0 to approximately 12 W.',24)
d.text(70,1415,'This is a checked drawing and connection plan; physical assembly and thermal performance have not been tested.',23,MUTED)
page3=d.svg()

pages = [('01_Breadboard_Placement',page1),('02_External_Heater_Wiring',page2),('03_Connection_Checklist',page3)]
combined = pymupdf.open()
for stem,svg in pages:
    (OUT/f'{stem}.svg').write_text(svg,encoding='utf-8')
    with pymupdf.open(stream=svg.encode('utf-8'),filetype='svg') as doc:
        with pymupdf.open('pdf',doc.convert_to_pdf()) as p:
            p[0].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(OUT/f'{stem}.png')
            dest=combined.new_page(width=1190.55,height=841.89)
            dest.show_pdf_page(dest.rect,p,0)
combined.save(OUT/'Heating_Breadboard_Guide.pdf')
combined.close()

guide = '''# Heating breadboard guide — Nano ESP32 and IRLB8748

Use **Heating_Breadboard_Guide.pdf** for all three illustrated sheets. PNG and editable SVG versions are also included.

## What this design assumes

- Controller: **Arduino Nano ESP32** from your course kit list. If your board is an Uno, an AVR Nano or a different ESP32 board, the drawn physical pin positions do not apply.
- Confirmed MOSFET: **IRLB8748**, TO-220. Printed face toward you, legs down: **G, D, S** from left to right; metal tab is drain.
- **Regulated 6.0 V**, at least **3 A continuous** supply capacity. At 3 Ω the heater takes about 2 A and produces 12 W at 100% duty. This layout deliberately uses the 6 V setting, not the whiteboard's 12 V / 48 W pulse example. Heating will be slower than a 30 W operating point; the temperature performance must be measured.
- Standard solderless breadboard with numbered strips and A–J holes: 400-point board or strips 1–30 of an 830-point board. The diagram is a placement guide, not to physical scale. Keep the driver, MOSFET and their short control leads close together.
- Nano stays beside the breadboard and is USB powered. Use female-to-male jumper wires on its headers. The power rails of the breadboard are unused, avoiding split-rail ambiguity.

## Parts to have before copying

| Part | Quantity / specification |
|---|---|
| Arduino Nano ESP32 | 1, with headers; USB powered |
| IRLB8748 | Your confirmed MOSFET |
| TC4420 | **1 additional non-inverting driver, PDIP-8 package** (e.g. TC4420CPA). Not TC4429 and not a TO-220/SOIC package |
| R1 | 10 kΩ, 1%, ≥0.25 W |
| R2 | 100 kΩ, ≥0.25 W, driver-input pull-down |
| R3 | 100 Ω, ≥0.25 W, gate series resistor |
| R4 | 100 kΩ, ≥0.25 W, gate-to-source pull-down at the MOSFET connector |
| C1 | 1 µF **ceramic/non-polar**, ≥16 V; use the shown A15/A18 positions with suitably formed leads |
| TH1 | Kit 10 kΩ NTC thermistor |
| H1 | Kit 3 Ω, 30 W-rated immersed heater |
| F1 / F2 | 3 A and 250 mA fast fuses, DC rated above the supply voltage, in insulated holders |
| SW1 | Manual heater-enable switch, ≥5 A DC at ≥6 V |
| Power connections | Secured, insulated terminals/adapter and cable rated ≥5 A DC for the heater loop |

TC4420 accepts the Nano's 3.3 V logic and supplies approximately 6 V gate drive. The IRLB8748 data sheet guarantees low on-resistance at 4.5 V and 10 V gate drive, not 3.3 V. R2 holds the driver input low if the Nano pin floats; R4 is physically at Q1 so an unplugged gate lead does not leave the gate floating. C1 provides the local driver supply bypass recommended by its data sheet. Do not remove the driver and connect D5 straight to the MOSFET in this layout.

## Breadboard connections

A–E of any one number are joined internally. F–J of that number are joined separately. A16 and F16 are **not** connected unless you add a jumper. Crossing insulated wires in the picture do not connect.

'''
guide += '| Component | First hole | Second hole | Value |\n|---|---|---|---|\n'
for ref,a,b,val,_ in PASSIVES:
    guide += f'| {ref} | {a} | {b} | {val} |\n'
guide += '| TH1 probe leads | D9 | D6 | 10 kΩ NTC; either way round |\n\n'
guide += 'Place U2 across the centre gap with its **notch to the left**, towards strip 15. The corner next to the notch on the F side is pin 1.\n\n| TC4420 pin | Hole | Function |\n|---|---|---|\n'
for pin,h in PINS.items():
    guide+=f'| {pin} | {h} | '+{1:'+6 V',2:'Input',3:'NC — leave unconnected',4:'Ground',5:'Ground',6:'Output',7:'Output',8:'+6 V'}[pin]+' |\n'
guide+='\n| Jumper | From | To | Purpose |\n|---|---|---|---|\n'
for ref,a,b,_,desc in JUMPERS: guide+=f'| {ref} | {a} | {b} | {desc} |\n'
guide+='\n| External lead | Connection | Breadboard hole |\n|---|---|---|\n'
for ref,_,h,_,desc in EXTERNAL: guide+=f'| {ref} | {desc} | {h} |\n'
guide+='''
## External heater wiring

1. Set the regulated output to **6 V** with the heater disconnected. Connect supply positive to two separate branches: heater branch through **F1 (3 A)** and **SW1** to heater positive; driver branch through **F2 (250 mA)** to **A12**. Fit the holders near the supply.
2. Heater negative → **IRLB8748 drain, middle leg (2)**. The tab is also drain: keep it insulated from ground and other wiring.
3. **IRLB8748 source, right leg (3)** → supply negative using a separate power lead. This is the approximately 2 A return; it never passes through breadboard contacts, Nano pins or the USB cable.
4. **H29** → the same supply-negative terminal with a separate low-current wire. This joins Nano, sensor and driver ground to the power circuit.
5. **B23** → IRLB8748 gate, left leg (1), keeping the connection short. Fit **R4 = 100 kΩ between gate and source at the MOSFET connector**, rather than at the far end of a detachable gate lead.
6. Use an insulated soldered adapter or suitably rated terminal arrangement for Q1. The drawing does not call for bare wires wrapped around its legs. Use individual secured connections; do not mount the high-current drain/source loop on the solderless board.

The two fuse values assume the listed cable/terminal ratings and regulated source. Verify the actual fuse time/current characteristics and supply fault behaviour when assembling. The small driver branch does not carry heater current. Keep all 6 V wiring away from Nano 3V3, VBUS, VIN and signal pins. Heater power is controlled by the external circuit, while the Nano is powered only by USB.

## Assembly and checks

1. Disconnect USB and the heater supply. Fit U2, R1–R3, C1 and every jumper using the tables. Verify the IC notch; inspect for adjacent shorts. R4 is at the external MOSFET connector.
2. With power disconnected, check continuity: upper strip 15 to lower strip 15; upper strip 18 to lower strip 18; upper 16 to upper 17; Nano GND to the supply-negative star. Confirm lower strip 17 (U2 NC) is not wired. Capacitors may briefly change an ohmmeter reading; a reading through a resistor is not the same as a short.
3. Leave the heater isolated with SW1 open. Connect USB only. Verify about 3.3 V at B3 and the divider voltage at B9. For a 10 kΩ thermistor at 25°C, the ideal divider gives about 1.65 V. Warming the NTC should lower the voltage. Do not assume the same ADC reading as an Uno.
4. Load code that makes **D5 LOW immediately at startup**. Check 6.0 V on the supply before connecting it. Apply the driver branch with heater still disconnected. Verify pins 1 and 8 of U2 are about +6 V relative to source; with D5 LOW, gate-to-source voltage should be near zero.
5. With the heater disconnected, briefly set D5 HIGH and verify about +6 V gate-to-source, then restore LOW. If either state is wrong, disconnect power and correct the wiring before connecting the heater.
6. Switch off and disconnect power. Connect the heater power loop, place the heater and thermistor correctly in the liquid, then repeat the LOW/off check before closing SW1. Start with a short, supervised heating test; monitor liquid temperature and power connections. Do not energise the heater dry.

## Changes from the lecturer's sketch

- Added the TC4420, local bypass capacitor, input pull-down, gate resistor and gate-to-source pull-down for the confirmed IRLB8748 and 3.3 V Nano.
- Chose a definite **10 kΩ** fixed divider resistor, because its whiteboard value was unclear. Calibrate using this actual resistor.
- Used **D5**, not D1/TX, to leave the UART transmit connection available. In code use `D5` and `A0` board-label constants; do not substitute the numeric GPIO pin names.
- Selected **6 V**, giving up to about 12 W. The whiteboard's 62.5% duty annotation is not this design's required operating duty. At 6 V, 62.5% would average about 7.5 W. Feedback must determine the required duty.

## Sources and verification

- [Arduino Nano ESP32 official pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf)
- [Arduino Nano ESP32 manual](https://docs.arduino.cc/resources/datasheets/ABX00083-datasheet.pdf)
- [Infineon IRLB8748 data sheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf)
- [Microchip TC4420/TC4429 data sheet](https://ww1.microchip.com/downloads/en/DeviceDoc/21419D.pdf)
- [BusBoard BB830 specification](https://www.busboard.com/BB830): an example quality solderless board is rated at 2 A. This design keeps heater current entirely off the board rather than relying on an unknown board's contact rating.

The generator checked occupied-hole conflicts, row-strip connectivity, separate 3.3 V / 6 V / ground / signal nets, the two connected driver supplies, both grounds, both outputs, and the unused NC pin. `Connectivity_Check.json` records the result. This is a drawing and connection check; no physical prototype, supply transient measurement, calibration or thermal performance test has been performed.
'''
(OUT/'Wiring_Instructions.md').write_text(guide,encoding='utf-8')
print(report['checks'])
for f in sorted(OUT.iterdir()): print(f.relative_to(ROOT))
