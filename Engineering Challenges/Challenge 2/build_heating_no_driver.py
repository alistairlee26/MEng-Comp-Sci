from pathlib import Path
from html import escape
import sys
import re
import json

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

OUT = ROOT / 'Circuit_Diagram_Examples' / 'Heating_Breadboard_No_Driver'
OUT.mkdir(parents=True, exist_ok=True)
W,H = 2000,1250
INK,GRAY,RED,BLUE,GREEN,ORANGE = '#203442','#546976','#be4035','#196f9e','#168169','#b3761d'


class Drawing:
    def __init__(self,title,subtitle,page):
        self.parts=[]
        self.rect(0,0,W,H,'white','white')
        self.text(55,67,title,38,bold=True)
        self.text(55,109,subtitle,23,GRAY)
        self.line([(55,138),(1945,138)],'#d4dfe5',2)
        self.text(1940,1218,f'{page} / 2',20,GRAY,anchor='end')
    def text(self,x,y,s,size=22,col=INK,bold=False,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{col}" text-anchor="{anchor}">{escape(s)}</text>')
    def rect(self,x,y,w,h,fill='white',stroke=INK,r=0):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>')
    def circle(self,x,y,r,fill,stroke=None):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or fill}" stroke-width="2"/>')
    def line(self,pts,col=INK,width=4,halo=False):
        p=' '.join(f'{x},{y}' for x,y in pts)
        if halo:
            self.parts.append(f'<polyline points="{p}" fill="none" stroke="white" stroke-width="{width+6}" stroke-linejoin="round"/>')
        self.parts.append(f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="{width}" stroke-linejoin="round"/>')
    def svg(self):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+''.join(self.parts)+'</svg>'


def xy(h):
    m=re.fullmatch(r'([A-J])(\d+)',h)
    c,r=m[1],int(m[2])
    y=460+'ABCDE'.index(c)*26 if c in 'ABCDE' else 654+'FGHIJ'.index(c)*26
    return 500+(r-1)*38,y


# Actual lead endpoints, also used to generate the wiring table.
WIRES=[
    ('Nano.3V3','B3'),('Nano.A0','B9'),('Nano.GND','A6'),('Nano.D5','B16'),
    ('B6','G26'),('TH1.1','D9'),('TH1.2','D6'),('STAR.GND','H26'),('Q1.G','B22'),
    ('Q1.S','STAR.GND'),
]
PASSIVES=[('R1','E3','E9','10 kΩ, 1%'),('R2','C16','C22','1 kΩ')]
parent={}; occupied={}
def net(h):
    m=re.fullmatch(r'([A-J])(\d+)',h)
    return ('AE' if m[1]<='E' else 'FJ')+m[2] if m else h
def find(h):
    h=net(h); parent.setdefault(h,h)
    if parent[h]!=h: parent[h]=find(parent[h])
    return parent[h]
for a,b in WIRES:
    parent[find(a)]=find(b)
    for h in [a,b]:
        if re.fullmatch(r'[A-J]\d+',h):
            assert h not in occupied,h
            occupied[h]='wire'
for ref,a,b,v in PASSIVES:
    for h in [a,b]:
        assert h not in occupied,h
        occupied[h]=ref
for a,b in [('Nano.3V3','E3'),('Nano.A0','E9'),('TH1.1','Nano.A0'),('TH1.2','Nano.GND'),('Q1.S','Nano.GND'),('Nano.D5','C16'),('Q1.G','C22')]:
    assert find(a)==find(b),(a,b)
assert len({find(h) for h in ['Nano.3V3','Nano.A0','Nano.GND','Nano.D5','Q1.G']})==5
(OUT/'Connectivity_Check.json').write_text(json.dumps({'result':'PASS','checks':['no shared endpoint holes','sensor divider nets separate','gate resistor not bypassed','common source/controller ground','no heater positive connection on breadboard'],'occupied_holes':occupied},indent=2),encoding='utf-8')

# PAGE 1: breadboard.
d=Drawing('Heating breadboard · no driver IC','Nano ESP32 + your IRLB8748  |  regulated 6 V heater supply  |  direct 3.3 V drive requires the load check on page 2',1)
d.text(55,174,'Updated version: no TC4420. Only the sensor and low-current control connections use the breadboard.',23,GRAY)
d.rect(460,320,1210,550,'#f5f3ed','#c7c7bf',22)
d.rect(480,590,1170,45,'#dedbd1','#dedbd1',8)
d.text(520,620,'CENTRE GAP',17,'#99968d')
for yy in [360,385,825,850]:
    for r in range(1,31): d.circle(xy('A'+str(r))[0],yy,4,'#d0cec5')
for c in 'ABCDEFGHIJ':
    yy=xy(c+'1')[1]
    d.text(482,yy+5,c,19,GRAY,True,'end')
    d.text(1630,yy+5,c,19,GRAY,True)
    for r in range(1,31): d.circle(*xy(c+str(r)),5,'#aaa89e')
for r in range(1,31):
    for yy in [438,795]: d.text(xy('A'+str(r))[0],yy,str(r),17,GRAY,anchor='middle')
d.text(1640,305,'RAILS UNUSED',18,GRAY,anchor='end')

# Nano top view with verified board-label positions; it sits beside the breadboard.
d.rect(90,300,190,460,'#18786b','#135b50',12)
d.rect(150,266,70,46,'#d3dbe1','#778a97',5)
d.text(185,247,'USB-C power',21,GRAY,anchor='middle')
left=['D13','3V3','B0','A0','A1','A2','A3','A4','A5','A6','A7','VBUS','B1','GND','VIN']
right=['D12','D11','D10','D9','D8','D7','D6','D5','D4','D3','D2','GND','RESET','D0/RX','D1/TX']
pins={}
for names,side in [(left,'L'),(right,'R')]:
    for i,name in enumerate(names):
        x=70 if side=='L' else 300; y=340+27*i
        d.line([(x,y),(90 if side=='L' else 280,y)],'#a5b5ad',3)
        d.rect(x-4,y-4,8,8,'#d4b45f','#947f49')
        d.text(102 if side=='L' else 268,y+5,name,15,'white',name in ['3V3','A0','D5','GND'],'start' if side=='L' else 'end')
        pins[side+name]=(x,y)
d.text(185,797,'NANO ESP32',23,bold=True,anchor='middle')
d.text(185,830,'Top view · USB at top',19,GRAY,anchor='middle')
routes=[
    ([pins['L3V3'],(35,367),(35,210),(576,210),xy('B3')],RED),
    ([pins['LA0'],(15,421),(15,190),(804,190),xy('B9')],BLUE),
    ([pins['RGND'],(420,637),(420,245),(690,245),xy('A6')],INK),
    ([pins['RD5'],(390,529),(390,280),(1070,280),xy('B16')],ORANGE),
    ([xy('B6'),(690,925),(1450,925),xy('G26')],INK),
]
for pts,col in routes:
    d.line(pts,col,5,True); d.circle(*pts[-1],5,col)

# Three external, low-current connections: probe, gate and source-reference ground.
d.rect(1720,365,230,480,'#f2f7f9','#c5d6df',12)
d.text(1835,408,'TO PAGE 2',23,bold=True,anchor='middle')
d.line([xy('B22'),(1298,260),(1790,260),(1790,465)],GREEN,5,True)
d.text(1740,507,'GATE · B22',22,GREEN,True)
d.text(1740,539,'To Q1 leg 1',21,GRAY)
d.line([xy('H26'),(1695,706),(1695,725),(1750,725)],INK,5,True)
d.text(1740,772,'GND · H26',22,INK,True)
d.text(1740,805,'To supply negative',19,GRAY)
for h in ['B22','H26']: d.circle(*xy(h),5,GREEN if h=='B22' else INK)

def resistor(a,b,label):
    x1,y=xy(a); x2,_=xy(b); m=(x1+x2)/2
    d.line([(x1,y),(m-40,y)],'#7e7e70',3)
    d.rect(m-40,y-12,80,24,'#e5d0a9','#a48c62',4)
    d.text(m,y+5,label,17,bold=True,anchor='middle')
    d.line([(m+40,y),(x2,y)],'#7e7e70',3)
    for h in [a,b]: d.circle(*xy(h),4,'#7e7e70')
resistor('E3','E9','10k')
resistor('C16','C22','1k')
d.line([xy('D6'),(690,546),(850,546),(850,1005)],INK,4,True)
d.line([xy('D9'),(804,526),(885,526),(885,1005)],BLUE,4,True)
d.rect(817,1005,100,43,'#f1f6f8','#8ba2af',10)
d.text(867,1034,'TH1',22,BLUE,True,'middle')
d.text(867,1080,'10 kΩ NTC probe · leads to D6 and D9',22,GRAY,anchor='middle')
d.line([(55,1110),(1945,1110)],'#d4dfe5',2)
for x,t,s1,s2 in [
    (55,'Breadboard parts','R1: E3–E9 = 10 kΩ, 1%','R2: C16–C22 = 1 kΩ'),
    (700,'Jumper and gate lead','B6 ↔ G26: ground jumper','B22 → MOSFET G (leg 1)'),
    (1350,'External pull-down','R3: 100 kΩ from G to S at Q1','No +6 V connection on this board')]:
    d.text(x,1148,t,24,bold=True)
    d.text(x,1182,s1,22,GRAY)
    d.text(x,1214,s2,22,GRAY)
p1=d.svg()

# PAGE 2: heater circuit, physical MOSFET connections and practical drive check.
d=Drawing('Heating wiring · direct GPIO to MOSFET','Set the heater supply to 6 V  |  about 2 A and 12 W when ON  |  use slow switching, around a one-second control period',2)
d.text(55,180,'IRLB8748: printed face toward you, metal tab behind, legs down → left G, middle D, right S.',25,bold=True)
d.rect(90,280,300,150,'#f2f7fa','#9eb2c0',12)
d.text(240,323,'REGULATED SUPPLY',24,bold=True,anchor='middle')
d.text(240,366,'6.0 V · ≥3 A',29,RED,True,'middle')
d.text(130,414,'+',25,RED,True); d.text(350,414,'−',25,INK,True)
d.line([(130,430),(130,520),(350,520)],RED,9)
d.rect(350,499,150,42,'#fff4f1',RED,6)
d.text(425,527,'F1 · 3 A',23,RED,True,'middle')
d.line([(500,520),(575,520)],RED,9)
d.circle(575,520,5,RED); d.circle(660,520,5,RED)
d.line([(575,520),(640,480)],RED,7)
d.text(620,448,'SW1',24,bold=True,anchor='middle')
d.text(620,572,'DC-rated ≥5 A',21,GRAY,anchor='middle')
d.line([(660,520),(780,520)],RED,9)
d.rect(780,460,310,120,'#fff6ee','#b57540',12)
d.text(935,505,'HEATER',27,bold=True,anchor='middle')
d.text(935,546,'3 Ω · 30 W rated',24,anchor='middle')
d.text(935,625,'Keep the element immersed.',22,GRAY,anchor='middle')
d.line([(1090,520),(1200,520),(1200,930),(1540,930),(1540,800)],RED,9)

d.rect(1405,230,270,110,'#b9c3ca','#748590',10)
d.circle(1540,275,22,'white','#748590')
d.rect(1385,320,310,270,'#27353e','#1b2a34',12)
d.text(1540,384,'IRLB8748',31,'white',True,'middle')
d.text(1540,432,'Front view',24,'#d8e1e6',anchor='middle')
d.text(1540,472,'TAB = DRAIN',23,'#d8e1e6',True,'middle')
for x,l in [(1460,'G'),(1540,'D'),(1620,'S')]:
    d.text(x,557,l,25,'white',True,'middle')
    d.line([(x,590),(x,800)],'#8a969f',12)

d.line([(350,430),(350,1040),(1840,1040),(1840,800),(1620,800)],INK,9,True)
d.circle(350,1040,9,INK)
d.text(350,1080,'STAR = supply negative terminal',22,INK,True)
d.rect(490,720,480,185,'#f2f8fa','#b2c7d4',10)
d.text(515,761,'BREADBOARD CONNECTIONS',23,bold=True)
d.text(515,811,'B22 → GATE (left leg 1)',24,GREEN,True)
d.text(515,859,'H26 → supply-negative STAR',24,INK,True)
d.line([(970,810),(1130,810),(1130,800),(1460,800)],GREEN,5,True)
d.line([(350,1040),(430,1040),(430,850),(490,850)],INK,5,True)
d.line([(1460,800),(1460,1000),(1390,1000)],GREEN,4,True)
d.rect(1240,980,150,40,'#e5d0a9','#a48c62',5)
d.text(1315,1008,'R3 · 100k',22,bold=True,anchor='middle')
d.line([(1240,1000),(1160,1000),(1160,1020),(1840,1020)],INK,4,True)
d.circle(1840,1020,6,INK)
d.text(1640,895,'SOURCE return',22,INK,True)
d.text(1640,928,'direct to supply −',21,GRAY)
for x,n,col in [(1460,'1',GREEN),(1540,'2',RED),(1620,'3',INK)]:
    d.circle(x,780,17,col)
    d.text(x,786,n,18,'white',True,'middle')

d.line([(55,1110),(1945,1110)],'#d4dfe5',2)
d.text(55,1148,'Required check at 6 V: with Q1 fully ON, measure D–S voltage (red probe leg 2, black leg 3). Aim for <0.1 V at about 2 A.',23,bold=True)
d.text(55,1181,'Start with a brief supervised test. Stop if the voltage drop is high or increases. See the instructions for the complete check.',22,GRAY)
d.text(55,1215,'Heater current stays off the breadboard. Secure power leads and MOSFET legs using an insulated terminal adapter.',22,GRAY)
p2=d.svg()

pdf=pymupdf.open()
for name,svg in [('01_Breadboard_No_Driver',p1),('02_Heater_Wiring_No_Driver',p2)]:
    (OUT/f'{name}.svg').write_text(svg,encoding='utf-8')
    with pymupdf.open(stream=svg.encode(),filetype='svg') as doc:
        with pymupdf.open('pdf',doc.convert_to_pdf()) as source:
            source[0].get_pixmap(matrix=pymupdf.Matrix(1.2,1.2),alpha=False).save(OUT/f'{name}.png')
            dest=pdf.new_page(width=1190.55,height=841.89)
            dest.show_pdf_page(dest.rect,source,0)
pdf.save(OUT/'Heating_No_Driver_Guide.pdf')
pdf.close()

notes='''# Heating breadboard without a driver IC

This replaces the earlier TC4420 version for your available IRLB8748. Use the two-page **Heating_No_Driver_Guide.pdf** and this connection list together.

## What the TC4420 was doing

It is a gate driver: it takes the Nano's 3.3 V PWM signal and drives the MOSFET gate at a higher voltage. It does not measure temperature or supply the heater current. It was an added design precaution, not a part shown on the lecturer's whiteboard.

The IRLB8748 data sheet gives guaranteed on-resistance at gate voltages of 4.5 V and 10 V. Its typical curves show operation at lower gate voltages, but typical curves do not guarantee every individual part. Direct 3.3 V drive is therefore a **bench-verified option for this 6 V, approximately 2 A load**, not a guaranteed replacement for the driver across arbitrary loads, devices or temperatures.

## Parts and operating conditions

- Nano ESP32, USB powered; confirmed IRLB8748 TO-220.
- R1: 10 kΩ, 1%, ≥0.25 W (selected for this design because the whiteboard value was unclear).
- R2: 1 kΩ, ≥0.25 W, in series between D5 and the gate. This limits the initial GPIO charging current to about 3.3 mA. Slow thermal switching avoids a need for fast gate edges.
- R3: 100 kΩ, ≥0.25 W, gate-to-source pull-down **at the MOSFET connector**. This holds the device off if the controller or gate lead is disconnected.
- Kit 10 kΩ NTC and 3 Ω, 30 W-rated heater.
- Regulated **6 V**, ≥3 A continuous supply capability. The heater operates at approximately 2 A and 12 W when fully on. Do not select 12 V for this layout.
- Manual heater enable switch rated ≥5 A DC, 3 A DC fuse/holder near supply positive, and insulated heater wiring/terminals rated ≥5 A. Check the actual fuse characteristics and supply fault behaviour when assembling.
- Standard 400-point breadboard, or numbered strips 1–30 of an 830-point board. Rails unused. All +6 V heater-power wiring remains off the breadboard.

## Exact connections

On the board, holes A–E of one number connect together, and F–J of that number connect together separately. The two groups do not join across the centre gap. Wire crossings in the picture do not connect.

| Connection / part | From | To |
|---|---|---|
| Nano 3V3 | Nano 3V3 | B3 |
| R1, 10 kΩ | E3 | E9 |
| NTC probe | D9 | D6 (either probe lead orientation) |
| Nano analogue input | Nano A0 | B9 |
| Nano ground | Nano GND | A6 |
| Ground jumper | B6 | G26 |
| PWM control | Nano D5 | B16 |
| R2, 1 kΩ | C16 | C22 |
| Gate lead | B22 | MOSFET G, left leg 1 |
| Common reference | H26 | Supply-negative star terminal |
| R3, 100 kΩ | MOSFET G | MOSFET S, physically at Q1 connector |

The Nano is placed beside the breadboard and connected by female-to-male jumpers; the drawing's board labels refer specifically to the Nano ESP32. Use `D5` and `A0` constants in code. D5 replaces the whiteboard's D1 so TX remains available for UART. Do not map these names directly to numeric ESP32 GPIO numbers.

## Heater power wiring — outside the breadboard

Printed MOSFET face towards you, metal tab behind, legs down: **left gate (1), middle drain (2), right source (3)**. The metal tab is drain. Use secured, insulated terminals or a soldered adapter; do not simply twist bare leads together.

1. Regulated +6 V → 3 A fuse → manual enable switch → heater positive.
2. Heater negative → MOSFET drain, middle leg 2.
3. MOSFET source, right leg 3 → supply negative with a separate power lead. This wire carries heater current; it does not go through the Nano, USB or breadboard.
4. H26 → that same supply-negative terminal via a separate low-current ground lead.
5. B22 → gate, left leg 1. R3 bridges G to S at the MOSFET connector. Keep the gate/control-return wiring short, preferably about 10 cm or less, and away from heater-current wiring.

## Checks before sustained heating

1. Disconnect all power while wiring. Keep the heater-enable switch open. Check that the 3.3 V sensor circuit has no connection to heater positive.
2. Load code that sets D5 LOW immediately at startup. Leave the switch open; power the Nano over USB and verify the sensor. At 25°C with a 10 kΩ thermistor, A0 should be approximately 1.65 V. Warming an NTC should lower that voltage.
3. Set the regulated supply to 6.0 V and verify it with a meter. With the heater isolated, verify gate-to-source voltage is near zero when D5 is LOW and approximately 3.3 V when D5 is HIGH (slightly lower due to R2/R3). Return LOW. **Never connect the gate directly to 6 V while it is also connected to the Nano.**
4. Switch off before connecting the heater. Immerse it correctly, secure the connections and attach voltmeter probes across MOSFET drain and source (red to leg 2, black to leg 3) while power is off. Do not allow a probe to bridge adjacent legs. Use the meter's DC-voltage mode, not its current mode across these pins.
5. With the element immersed, perform a brief supervised full-on test at 6 V. The circuit should draw close to 2 A. **Use less than 0.1 V D–S drop at approximately 2 A as an initial design criterion**, giving less than about 0.2 W MOSFET conduction loss. This is a practical screening target, not a manufacturer specification or a complete thermal certification. Measure real current using the supply display or a properly connected current measurement.
6. If the drop is high, or increases as the device warms, switch off rather than continuing. Recheck pinout and gate voltage. If direct 3.3 V drive is inadequate, use a MOSFET with on-resistance specified at 2.5/3.3 V or add a suitable driver. Do not solve it by connecting Nano GPIO to a higher supply.
7. After the initial check passes, extend the test gradually under supervision and monitor MOSFET temperature using an appropriate instrument and D–S drop, including at the warmest intended operating conditions. Do not rely on touching the MOSFET to judge temperature. Keep a manual heater disconnect available.

Use slow thermal control, for example a one-second on/off control period (time proportioning), rather than an unexamined high-frequency PWM setting. This is a circuit/drive check, not a complete feedback controller: sensor-fault detection and overtemperature handling remain required in the control code. No physical build or temperature-control performance test has been carried out here.

## References

- [Infineon IRLB8748 data sheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irlb8748-datasheet-en.pdf): pinout and specified/typical gate-drive behaviour.
- [Arduino Nano ESP32 pinout](https://docs.arduino.cc/resources/pinouts/ABX00083-full-pinout.pdf): board-label positions.

The generator checked hole occupancy, row connectivity, separate sensor and gate nets, the gate series resistor, and shared controller/source ground. A physical load and thermal check is still necessary for this direct-drive arrangement.
'''
(OUT/'Wiring_Instructions_No_Driver.md').write_text(notes,encoding='utf-8')
print('PASS: hole occupancy and electrical row connections checked.')
for f in sorted(OUT.iterdir()): print(f.relative_to(ROOT))
