"""Build the web checklist and its one-page printable PDF from one source.

    uv run --with reportlab python tools/build_pilot_checklist.py
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]


class ChecklistItem(Flowable):
    def __init__(self, text, style):
        super().__init__()
        self.paragraph = Paragraph(escape(text), style)

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        _, height = self.paragraph.wrap(avail_width - 15, avail_height)
        self.height = height + 4
        return self.width, self.height

    def draw(self):
        self.canv.setStrokeColor(colors.HexColor('#52606d'))
        self.canv.rect(0, self.height - 10, 6, 6, fill=0, stroke=1)
        self.paragraph.drawOn(self.canv, 15, 4)


def main():
    data = json.loads((ROOT / 'tools/pilot_checklist.json').read_text())
    web = ['# ' + data['title'], '', data['intro'], '',
           '<a class="vm-button" href="handouts/lecturer-pilot-checklist.pdf">Download the printable checklist (PDF)</a>', '',
           'Use the [lecturer guide](supervisors.md), [Getting started](getting-started.md),',
           '[A1](units/ode-ivp/index.md) or [A2](units/linear-systems/index.md)',
           'for the detailed instructions. GitHub is optional; the usual route is a ZIP download.', '']
    for section in data['sections']:
        web += ['## ' + section['title'], '']
        web += ['- ' + text for text in section['items']]
        web += ['']
    web += ['## Send feedback', '',
            f"Email [{data['contact']}](mailto:{data['contact']}) with the subject",
            '**verifiedmethods pilot feedback - A1** or **A2**.', '',
            'There is no upload form or account requirement. Keep completed checklists',
            'with your course records and send a short summary by email.', '',
            data['edition'] + '. ' + data['license'], '']
    (ROOT / 'docs/pilot-checklist.md').write_text('\n'.join(web), encoding='utf-8')

    output = ROOT / 'extra/handouts/lecturer-pilot-checklist.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    styles = {
        'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=21, leading=24,
                                textColor=colors.HexColor('#1d5c8f'), spaceAfter=3),
        'subtitle': ParagraphStyle('subtitle', fontName='Helvetica', fontSize=10, leading=13, spaceAfter=9),
        'intro': ParagraphStyle('intro', fontName='Helvetica', fontSize=9.2, leading=12, spaceAfter=7),
        'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=10.2, leading=13,
                                  textColor=colors.HexColor('#1d5c8f'), spaceBefore=6, spaceAfter=4),
        'item': ParagraphStyle('item', fontName='Helvetica', fontSize=9.6, leading=12.6, alignment=TA_LEFT),
        'footer': ParagraphStyle('footer', fontName='Helvetica', fontSize=8, leading=10,
                                 textColor=colors.HexColor('#52606d')),
    }
    story = [Paragraph(escape(data['title']), styles['title']),
             Paragraph(escape(data['subtitle']), styles['subtitle']),
             Paragraph(escape(data['intro']), styles['intro'])]
    for section in data['sections']:
        story.append(Paragraph(escape(section['title']), styles['heading']))
        story.extend(ChecklistItem(text, styles['item']) for text in section['items'])
    story += [Spacer(1, 7),
              Paragraph('Feedback: <link href="mailto:' + data['contact'] + '">' + data['contact'] + '</link>', styles['footer']),
              Paragraph('<link href="' + data['page_url'] + '">' + data['page_url'] + '</link>', styles['footer']),
              Paragraph(escape(data['edition'] + ' | ' + data['license']), styles['footer'])]
    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=38, rightMargin=38,
                            topMargin=32, bottomMargin=30, title=data['title'],
                            author='verifiedmethods', pageCompression=1)
    doc.build(story)
    print('Built docs/pilot-checklist.md and', output.relative_to(ROOT))


if __name__ == '__main__':
    main()
