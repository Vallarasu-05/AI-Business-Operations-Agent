import re
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def markdown_to_pdf(md: str, path: str) -> str:
    """Tiny markdown -> PDF renderer (headings, bullets, paragraphs). Built-in fonts lack the rupee glyph."""
    md = md.replace("₹", "Rs. ").replace("•", "-").replace("–", "-")
    styles = getSampleStyleSheet()
    flow = []
    for line in md.splitlines():
        if not line.strip():
            flow.append(Spacer(1, 6))
            continue
        txt = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escape(line))
        if line.startswith("# "):
            flow.append(Paragraph(txt[2:], styles["Heading1"]))
        elif line.startswith("## "):
            flow.append(Paragraph(txt[3:], styles["Heading2"]))
        elif line.lstrip().startswith(("- ", "* ")):
            flow.append(Paragraph("- " + txt.lstrip()[2:], styles["BodyText"]))
        else:
            flow.append(Paragraph(txt, styles["BodyText"]))
    SimpleDocTemplate(path, pagesize=A4).build(flow)
    return path
