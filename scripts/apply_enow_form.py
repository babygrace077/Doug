#!/usr/bin/env python3
"""
Applique la FORME du mémoire Enow (PDF) au mémoire ART Word.
Ne copie aucun contenu Enow — uniquement styles / mise en page.
"""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Twips, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = Path("/workspace/livrables/memoire/Memoire_ART_Zero_Trust_mise_en_forme.docx")
OUT = Path("/workspace/livrables/memoire/Memoire_ART_Zero_Trust_forme_Enow.docx")
ART = Path("/opt/cursor/artifacts/memoire/Memoire_ART_Zero_Trust_forme_Enow.docx")

# Forme extraite du PDF Enow (mesures approx. / styles dominants)
BODY_FONT = "Times New Roman"
BODY_SIZE = 12
CHAPTER_SIZE = 16
SECTION_SIZE = 12
CAPTION_SIZE = 12
HEADER_FONT = "Calibri Light"
HEADER_SIZE = 11
TABLE_SIZE = 10

# En-tête : titre COURT du mémoire de l'étudiant (pas celui d'Enow)
HEADER_LINE1 = (
    "Refonte du modèle de confiance du SI et architecture Zero Trust multicouche. "
    "Étude de"
)
HEADER_LINE2 = "cas : Agence de Régulation des Télécommunications (ART)"


def set_run_font(run, name=BODY_FONT, size=BODY_SIZE, bold=None, italic=None):
    run.font.name = name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def rewrite_runs(p, text, name=BODY_FONT, size=BODY_SIZE, bold=False, italic=False):
    if p.runs:
        p.runs[0].text = text
        set_run_font(p.runs[0], name=name, size=size, bold=bold, italic=italic)
        for r in p.runs[1:]:
            r.text = ""
    else:
        r = p.add_run(text)
        set_run_font(r, name=name, size=size, bold=bold, italic=italic)


def para_has_image(p) -> bool:
    return bool(
        p._element.findall(
            ".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
        )
    )


def add_page_number(paragraph):
    """Insert PAGE field centered."""
    run = paragraph.add_run()
    set_run_font(run, name=BODY_FONT, size=10)
    fld_char_begin = OxmlElement("w:fldChar")
    fld_char_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_char_end = OxmlElement("w:fldChar")
    fld_char_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_char_begin)
    run._r.append(instr)
    run._r.append(fld_char_end)


def setup_header_footer(section):
    header = section.header
    header.is_linked_to_previous = False
    # clear existing
    for p in header.paragraphs:
        p.clear()
    hp = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = hp.add_run(HEADER_LINE1)
    set_run_font(r1, name=HEADER_FONT, size=HEADER_SIZE)
    hp2 = header.add_paragraph()
    hp2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = hp2.add_run(HEADER_LINE2)
    set_run_font(r2, name=HEADER_FONT, size=HEADER_SIZE)
    for p in (hp, hp2):
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    footer = section.footer
    footer.is_linked_to_previous = False
    for p in footer.paragraphs:
        p.clear()
    fp = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number(fp)
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)


def normalize_caption(text: str) -> str:
    """Figure 4. Xxx -> Figure 4 : Xxx (forme Enow)."""
    import re

    text = text.strip()
    text = re.sub(r"^(Figure\s+\d+)\.\s*", r"\1 : ", text)
    text = re.sub(r"^(Tableau\s+\d+)\.\s*", r"\1 : ", text)
    # collapse double spaces / colon artifacts
    text = text.replace(" : :", " :")
    return text


def classify(text: str):
    t = text.strip()
    if not t:
        return "empty"
    if t.startswith("CHAPITRE"):
        return "chapter"
    if t.startswith("Figure ") or t.startswith("Tableau "):
        return "caption"
    if t.startswith(("I.", "II.", "III.", "IV.")) and len(t) < 160:
        return "section"
    if t in ("Introduction", "Conclusion", "Conclusion du chapitre", "REFERENCES", "Références"):
        return "section"
    if t.startswith("Keyword:") or t.startswith("Mots"):
        return "meta"
    return "body"


def main():
    doc = Document(str(SRC))

    # --- Page setup (A4 + marges type Enow) ---
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        # Enow ~ left 25mm, right 21mm, top with header, bottom ~21mm
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.1)
        section.top_margin = Cm(2.2)
        section.bottom_margin = Cm(2.1)
        section.header_distance = Cm(1.0)
        section.footer_distance = Cm(1.2)
        setup_header_footer(section)

    # --- Paragraph styles ---
    for p in doc.paragraphs:
        t = p.text.strip()
        kind = classify(t)
        pf = p.paragraph_format
        pf.first_line_indent = Cm(0)  # Enow: pas d'alinéa visible (même x0)

        if para_has_image(p) and not t:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            pf.space_before = Pt(6)
            pf.space_after = Pt(6)
            continue

        if kind == "chapter":
            # CHAPITRE X : ...
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.space_before = Pt(18)
            pf.space_after = Pt(12)
            pf.line_spacing = 1.5
            # keep text, force bold 16
            for r in p.runs:
                if r.text:
                    set_run_font(r, name=BODY_FONT, size=CHAPTER_SIZE, bold=True)
            if not p.runs and t:
                rewrite_runs(p, t, size=CHAPTER_SIZE, bold=True)

        elif kind == "section":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)
            pf.line_spacing = 1.5
            for r in p.runs:
                if r.text:
                    set_run_font(r, name=BODY_FONT, size=SECTION_SIZE, bold=True)
            if not p.runs and t:
                rewrite_runs(p, t, size=SECTION_SIZE, bold=True)

        elif kind == "caption":
            new_t = normalize_caption(t)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.space_before = Pt(6)
            pf.space_after = Pt(8)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            rewrite_runs(p, new_t, size=CAPTION_SIZE, bold=False, italic=False)

        elif kind == "meta":
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.line_spacing = 1.5
            for r in p.runs:
                if r.text:
                    set_run_font(r, name=BODY_FONT, size=11, italic=True)

        else:  # body / empty
            if t:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            pf.line_spacing = 1.5  # dominant reading rhythm (~18-20pt)
            for r in p.runs:
                if r.text:
                    # preserve explicit bold/italic if already set for emphasis
                    bold = r.bold if r.bold else False
                    italic = r.italic if r.italic else False
                    set_run_font(r, name=BODY_FONT, size=BODY_SIZE, bold=bold, italic=italic)

    # --- Tables : Times 10 ---
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.space_before = Pt(1)
                    for r in p.runs:
                        if r.text:
                            set_run_font(
                                r,
                                name=BODY_FONT,
                                size=TABLE_SIZE,
                                bold=bool(r.bold),
                                italic=bool(r.italic),
                            )

    # --- Normal style baseline ---
    try:
        style = doc.styles["Normal"]
        style.font.name = BODY_FONT
        style.font.size = Pt(BODY_SIZE)
        style.paragraph_format.line_spacing = 1.5
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    except Exception:
        pass

    doc.save(str(OUT))
    doc.save(str(ART))
    print("Saved", OUT)
    print("Saved", ART)

    # quick verify
    d2 = Document(str(OUT))
    print("sections", len(d2.sections))
    h = d2.sections[0].header.paragraphs
    print("header:", " | ".join(p.text for p in h if p.text)[:160])
    caps = [p.text for p in d2.paragraphs if p.text.startswith("Figure ") or p.text.startswith("Tableau ")]
    print("sample captions:", caps[:4])


if __name__ == "__main__":
    main()
