#!/usr/bin/env python3
"""Build the PDF technical reference from its Markdown source."""
from pathlib import Path
import argparse
from html import escape
import re
import textwrap
from urllib.parse import urljoin

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle, XPreformatted,
)
from reportlab.platypus.tableofcontents import TableOfContents

ROOT = Path(__file__).resolve().parents[1]
BLUE = colors.HexColor('#153B5B')
INK = colors.HexColor('#243746')
MUTED = colors.HexColor('#526474')
PALE = colors.HexColor('#F0F4F7')
WIDTH, HEIGHT = A4
MARGIN = 20 * mm
CONTENT = WIDTH - 2 * MARGIN
GITHUB_DOCS = 'https://github.com/A-C-Simon/multi-roi-crop-navigation/blob/main/docs/'
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle('BodyTextMR', fontName='Helvetica', fontSize=9.5,
    leading=13.4, textColor=INK, spaceAfter=7))
STYLES.add(ParagraphStyle('SectionMR', fontName='Helvetica-Bold', fontSize=15,
    leading=19, textColor=BLUE, spaceBefore=14, spaceAfter=9, keepWithNext=True))
STYLES.add(ParagraphStyle('SubsectionMR', fontName='Helvetica-Bold', fontSize=11,
    leading=15, textColor=BLUE, spaceBefore=9, spaceAfter=6, keepWithNext=True))
STYLES.add(ParagraphStyle('CellMR', fontName='Helvetica', fontSize=8,
    leading=10.8, textColor=INK))
STYLES.add(ParagraphStyle('HeaderCellMR', parent=STYLES['CellMR'],
    fontName='Helvetica-Bold', textColor=colors.white))
STYLES.add(ParagraphStyle('CodeMR', fontName='Courier', fontSize=7.2,
    leading=9.6, textColor=INK, backColor=PALE, borderPadding=8,
    spaceBefore=5, spaceAfter=10))
STYLES.add(ParagraphStyle('CaptionMR', parent=STYLES['BodyTextMR'],
    fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5, textColor=MUTED))
STYLES.add(ParagraphStyle('TocMR', fontName='Helvetica', fontSize=10,
    leading=16, textColor=INK, spaceBefore=7))


def inline(text):
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*\*([^*]+)\*\*|\*([^*]+)\*')
    parts, start = [], 0
    for match in pattern.finditer(text):
        parts.append(escape(text[start:match.start()]))
        label, target, code, bold, italic = match.groups()
        if label is not None:
            url = target if '://' in target else urljoin(GITHUB_DOCS, target)
            parts.append(f'<link href="{escape(url, quote=True)}" color="#17639A">{escape(label)}</link>')
        elif code is not None:
            parts.append(f'<font name="Courier">{escape(code)}</font>')
        elif bold is not None:
            parts.append(f'<b>{escape(bold)}</b>')
        else:
            parts.append(f'<i>{escape(italic)}</i>')
        start = match.end()
    parts.append(escape(text[start:]))
    return ''.join(parts)


class TechnicalDocument(BaseDocTemplate):
    def __init__(self, path, metadata):
        super().__init__(str(path), pagesize=A4, leftMargin=MARGIN,
            rightMargin=MARGIN, topMargin=22*mm, bottomMargin=20*mm,
            title='Multi-ROI Crop Navigation: Technical Design and Integration Reference',
            author='A-C-Simon', subject=f"{metadata['Document ID']}, revision {metadata['Revision']}")
        self.metadata = metadata
        frame = Frame(MARGIN, 20*mm, CONTENT, HEIGHT-44*mm,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id='cover', frames=[frame], onPage=self.cover),
            PageTemplate(id='body', frames=[frame], onPage=self.header_footer),
        ])
        self.heading_number = 0

    def cover(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BLUE)
        canvas.rect(0, HEIGHT-94*mm, WIDTH, 94*mm, fill=1, stroke=0)
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica-Bold', 27)
        canvas.drawString(MARGIN, HEIGHT-37*mm, 'Multi-ROI Crop Navigation')
        canvas.setFont('Helvetica', 16)
        canvas.drawString(MARGIN, HEIGHT-52*mm, 'Technical Design and')
        canvas.drawString(MARGIN, HEIGHT-61*mm, 'Integration Reference')
        canvas.setFont('Helvetica', 10)
        canvas.drawString(MARGIN, HEIGHT-80*mm,
                          f"{self.metadata['Document ID']}  |  Revision {self.metadata['Revision']}")
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, 13*mm, f"Project documentation | {self.metadata['Issue date']}")
        canvas.restoreState()

    def header_footer(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#CED8E1'))
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, HEIGHT-15*mm, WIDTH-MARGIN, HEIGHT-15*mm)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(MARGIN, HEIGHT-12*mm, 'Multi-ROI Crop Navigation')
        canvas.drawRightString(WIDTH-MARGIN, HEIGHT-12*mm, f"{self.metadata['Document ID']} | Rev. {self.metadata['Revision']}")
        canvas.line(MARGIN, 15*mm, WIDTH-MARGIN, 15*mm)
        canvas.drawString(MARGIN, 10*mm, 'Technical Design and Integration Reference')
        canvas.drawRightString(WIDTH-MARGIN, 10*mm, str(doc.page))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'SectionMR':
            text = flowable.getPlainText()
            if text == 'Contents':
                return
            key = 'section-' + re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=0)
            self.notify('TOCEntry', (0, text, self.page, key))


def table(rows, widths=None):
    cells = []
    for index, row in enumerate(rows):
        style = STYLES['HeaderCellMR' if index == 0 else 'CellMR']
        cells.append([Paragraph(inline(cell), style) for cell in row])
    if widths is None:
        n = len(rows[0])
        fractions = {2:[.30,.70],3:[.25,.25,.50],5:[.23,.1925,.1925,.1925,.1925]}
        widths = [CONTENT*x for x in fractions.get(n, [1/n]*n)]
    result = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),BLUE),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),7),
        ('RIGHTPADDING',(0,0),(-1,-1),7),
        ('TOPPADDING',(0,0),(-1,-1),4),
        ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
        ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#CED8E1')),
    ]))
    result.spaceBefore = 5
    result.spaceAfter = 12
    return result


def render_body(lines, source):
    story = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith('```'):
            block = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith('```'):
                for wrapped in textwrap.wrap(lines[index], width=106,
                        subsequent_indent='    ', replace_whitespace=False,
                        drop_whitespace=False) or ['']:
                    block.append(wrapped)
                index += 1
            story.append(XPreformatted(escape('\n'.join(block)), STYLES['CodeMR']))
            index += 1
            continue
        if line.startswith('|'):
            rows = []
            while index < len(lines) and lines[index].strip().startswith('|'):
                cells = [cell.strip() for cell in lines[index].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', cell.replace(' ','')) for cell in cells):
                    rows.append(cells)
                index += 1
            story.append(table(rows))
            continue
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]), STYLES['SectionMR']))
            index += 1
            continue
        if line.startswith('### '):
            story.append(Paragraph(inline(line[4:]), STYLES['SubsectionMR']))
            index += 1
            continue
        image = re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
        if image:
            path = source.parent/image.group(2)
            picture = Image(str(path))
            picture.drawHeight *= CONTENT/picture.drawWidth
            picture.drawWidth = CONTENT
            story.extend([Spacer(1,5), picture, Spacer(1,6)])
            index += 1
            continue
        bullet = None
        match = re.match(r'^(\d+\.|-)\s+(.*)',line)
        if match:
            bullet = match.group(1)
            line = match.group(2)
        paragraph = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            nxt = lines[index].strip()
            if nxt.startswith(('#','|','```','![')) or re.match(r'^(\d+\.|-)\s+',nxt):
                break
            paragraph.append(nxt)
            index += 1
        style = STYLES['CaptionMR'] if paragraph[0].startswith('*Figure ') else STYLES['BodyTextMR']
        story.append(Paragraph(inline(' '.join(paragraph)),style,bulletText=bullet))
    return story


def build(source, output):
    lines = source.read_text(encoding='utf-8').splitlines()
    metadata = {}
    for line in lines:
        if line.startswith('| '):
            cells = [part.strip() for part in line.strip('|').split('|')]
            if len(cells) == 2 and cells[0] in (
                'Document ID','Revision','Issue date','Software version',
                'Implementation baseline','Project','Scope'):
                metadata[cells[0]] = cells[1]
        if line == '## Contents':
            break
    start = next(i for i,line in enumerate(lines) if line.startswith('## 1. '))
    story = [Spacer(1,88*mm)]
    rows = [['Document control','Value']]+[[key,value] for key,value in metadata.items()]
    story.extend([table(rows),Spacer(1,8*mm),Paragraph(
        'System architecture, processing algorithms, configuration, interfaces, '
        'execution procedures, and verification records.',STYLES['BodyTextMR']),
        NextPageTemplate('body'),PageBreak(),
        Paragraph('Contents',STYLES['SectionMR'])])
    toc = TableOfContents()
    toc.levelStyles = [STYLES['TocMR']]
    story.extend([toc,PageBreak()])
    story.extend(render_body(lines[start:],source))
    output.parent.mkdir(parents=True,exist_ok=True)
    document = TechnicalDocument(output,metadata)
    document.multiBuild(story)
    print(f'Built {output} ({document.page} pages)')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path,
        default=ROOT/'docs/technical-documentation.md')
    parser.add_argument('--output', type=Path,
        default=ROOT/'docs/technical-documentation.pdf')
    args = parser.parse_args()
    build(args.source.resolve(),args.output.resolve())


if __name__ == '__main__':
    main()
