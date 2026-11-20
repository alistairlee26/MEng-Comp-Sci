from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

destination = ROOT / 'Circuit_Diagram_Examples'
context = destination / 'Context'
context.mkdir(parents=True, exist_ok=True)

with pymupdf.open(ROOT / 'Introduction_to_Transistors.pdf') as doc:
    page = doc[5]
    # Bounds of the embedded circuit figure, with a small margin.
    clip = pymupdf.Rect(363, 164, 698, 429)
    page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip).save(
        destination / '01_MOSFET_Switch_Heating_Reference_Transistors_Slide_06.png'
    )
    page.get_pixmap(matrix=pymupdf.Matrix(2, 2)).save(
        context / 'Transistors_Slide_06_Full.png'
    )

shutil.copyfile(
    ROOT / 'material_review' / 'motor_original_circuit.jpeg',
    destination / '02_Stirring_Circuit_MotorHallSensorInstructions_Slide_03.jpeg',
)

for path in sorted(destination.rglob('*')):
    if path.is_file():
        print(f'{path.relative_to(destination)} ({path.stat().st_size:,} bytes)')
