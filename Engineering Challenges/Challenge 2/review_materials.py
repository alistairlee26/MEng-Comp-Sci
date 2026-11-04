from pathlib import Path
import sys
import zipfile
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / '.review-tools'))
import pymupdf

out = ROOT / 'material_review'
out.mkdir(exist_ok=True)
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
for source in sorted(ROOT.iterdir()):
    sections = []
    if source.suffix.lower() == '.pdf':
        doc = pymupdf.open(source)
        for i, page in enumerate(doc, 1):
            sections.append(f'--- PAGE {i} ---\n{page.get_text()}')
        print(f'{source.name}: {len(doc)} pages')
        if source.name == 'Engineering Challenges Presentation.pdf':
            for i, page in enumerate(doc, 1):
                page.get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2)).save(out / f'team_slide_{i:02}.png')
    elif source.suffix.lower() == '.pptx':
        with zipfile.ZipFile(source) as archive:
            slides = sorted([n for n in archive.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)], key=lambda n: int(re.search(r'slide(\d+)', n).group(1)))
            for i, name in enumerate(slides, 1):
                root = ET.fromstring(archive.read(name))
                lines = [''.join(p.itertext()) for p in root.findall('.//a:t', ns)]
                sections.append(f'--- SLIDE {i} ---\n' + '\n'.join(lines))
                notes = f'ppt/notesSlides/notesSlide{i}.xml'
                if notes in archive.namelist():
                    root = ET.fromstring(archive.read(notes))
                    sections.append('NOTES:\n' + '\n'.join(t.text or '' for t in root.findall('.//a:t', ns)))
        print(f'{source.name}: {len(slides)} slides')
    if sections:
        (out / (source.stem + '.txt')).write_text('\n\n'.join(sections), encoding='utf-8')
