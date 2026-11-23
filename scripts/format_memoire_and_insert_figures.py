#!/usr/bin/env python3
"""Mise en forme propre + insertion contrôlée des figures (sans doublons)."""

from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph

SRC = Path("/workspace/livrables/memoire/Memoire_ART_Zero_Trust_corrige.docx")
OUT = Path("/workspace/livrables/memoire/Memoire_ART_Zero_Trust_mise_en_forme.docx")
ART = Path("/opt/cursor/artifacts/memoire/Memoire_ART_Zero_Trust_mise_en_forme.docx")
FIG = Path("/workspace/livrables/memoire/figures")


def set_run_font(run, name="Times New Roman", size=12, bold=None, italic=None):
    run.font.name = name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn("w:ascii"), name)
    rFonts.set(qn("w:hAnsi"), name)
    rFonts.set(qn("w:cs"), name)
    run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def replace_dashes(text: str) -> str:
    text = text.replace("—", " : ")
    text = text.replace("–", "-")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.replace(" : :", " :")
    return text


def para_has_image(p) -> bool:
    return bool(p._element.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))


def clear_images_in_paragraph(p):
    """Remove drawing elements from a paragraph, keep text runs if any."""
    for drawing in p._element.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}drawing"):
        parent = drawing.getparent()
        if parent is not None:
            parent.remove(drawing)


def insert_picture_after(paragraph, image_path, width_inches=5.8):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    para = Paragraph(new_p, paragraph._parent)
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run()
    run.add_picture(str(image_path), width=Inches(width_inches))
    return para


def insert_caption_after_element(element, text, parent):
    cap = OxmlElement("w:p")
    element.addnext(cap)
    cpara = Paragraph(cap, parent)
    cpara.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cpara.add_run(text)
    set_run_font(run, size=10, italic=True)
    return cpara


def rewrite_para_text(p, new_text):
    if p.runs:
        p.runs[0].text = new_text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(new_text)


def main():
    doc = Document(str(SRC))

    # 1) Dashes
    for p in doc.paragraphs:
        if "—" in p.text or "–" in p.text:
            rewrite_para_text(p, replace_dashes(p.text))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    if "—" in p.text or "–" in p.text:
                        rewrite_para_text(p, replace_dashes(p.text))

    # 2) Clear ASCII diagram under Figure 4
    for i, p in enumerate(doc.paragraphs):
        if "[Pare-feu]" in p.text or ("----" in p.text and "Utilisateurs" in p.text):
            rewrite_para_text(p, "")
            clear_images_in_paragraph(p)
        if "Poste attaquant : placé" in p.text and "Utilisateurs" in p.text:
            rewrite_para_text(p, "")

    # 3) Remove empty/orphan image-only paragraphs that sit just BEFORE figure captions
    #    (legacy blanks at fig6/fig7) — keep images that accompany NIST/ZTMM body if intentional.
    paras = list(doc.paragraphs)
    for i, p in enumerate(paras):
        t = p.text.strip()
        if t.startswith("Figure 6.") or t.startswith("Figure 7.") or t.startswith("Figure 8.") or t.startswith("Figure 4."):
            # if previous is image-only empty, clear its image (will reinsert ours after caption)
            if i > 0 and paras[i - 1].text.strip() == "" and para_has_image(paras[i - 1]):
                clear_images_in_paragraph(paras[i - 1])

    # 4) Insert our figures AFTER captions (once)
    wanted = {
        "Figure 4. Topologie": FIG / "figure4_topologie_maquette.png",
        "Figure 6. Synthèse de maturité": FIG / "figure6_maturite_initiale.png",
        "Figure 7. Architecture cible": FIG / "figure7_architecture_pe_pa_pep.png",
        "Figure 8. Topologie logique": FIG / "figure8_topologie_logique_maquette.png",
    }
    for p in list(doc.paragraphs):
        t = p.text.strip()
        for prefix, path in wanted.items():
            if t.startswith(prefix):
                # skip if next sibling already has our fresh image (has drawing)
                nxt = p._p.getnext()
                already = False
                if nxt is not None and nxt.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
                    already = True
                if not already:
                    insert_picture_after(p, path, 5.8)
                break

    # 5) Placeholders for I.1.1 and I.1.2 if no dedicated figure caption yet
    # If an empty image already follows the heading, replace by clearing and inserting ours + caption
    for p in list(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("I.1.1.") and "Architecture du réseau" in t:
            nxt = p._p.getnext()
            # clear following empty image para if any
            # find paragraph object for next
            for q in doc.paragraphs:
                if q._p is nxt and para_has_image(q) and not q.text.strip():
                    clear_images_in_paragraph(q)
                    break
            img_p = insert_picture_after(p, FIG / "placeholder_architecture_reseau_art.png", 5.7)
            insert_caption_after_element(img_p._p, "Figure 1. Architecture du réseau de l'ART (emplacement réservé)", p._parent)
        if t.startswith("I.1.2.") and "dispositif sécuritaire" in t:
            img_p = insert_picture_after(p, FIG / "placeholder_dispositif_securitaire.png", 5.7)
            insert_caption_after_element(img_p._p, "Figure 2. Synthèse du dispositif sécuritaire actuel (emplacement réservé)", p._parent)

    # 6) Page setup + typography (forme mémoire type ; Enow non fourni sur la VM)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)

    for p in doc.paragraphs:
        t = p.text.strip()
        pf = p.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
        pf.space_after = Pt(6)
        pf.space_before = Pt(0)

        if para_has_image(p) and not t:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            continue

        if t.startswith("CHAPITRE"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.space_before = Pt(18)
            pf.space_after = Pt(12)
            for r in p.runs:
                set_run_font(r, size=14, bold=True)
        elif t.startswith("Figure ") or t.startswith("Tableau "):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            for r in p.runs:
                set_run_font(r, size=10, italic=True)
        elif t.startswith(("I.", "II.", "III.", "IV.")) and len(t) < 140:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.space_before = Pt(12)
            for r in p.runs:
                set_run_font(r, size=12, bold=True)
        else:
            if t:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            for r in p.runs:
                if r.text:
                    set_run_font(r, size=12)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        if r.text:
                            set_run_font(r, size=10)

    doc.save(str(OUT))
    doc.save(str(ART))
    print("Saved", OUT)

    # verify
    doc2 = Document(str(OUT))
    print("em dashes", sum(p.text.count("—") for p in doc2.paragraphs))
    print("ascii", sum(1 for p in doc2.paragraphs if "[Pare-feu]" in p.text))
    imgs = 0
    for i, p in enumerate(doc2.paragraphs):
        if para_has_image(p):
            imgs += 1
            prev = doc2.paragraphs[i - 1].text.strip()[:70] if i else ""
            print(f"img@{i} after={prev!r}")
    print("images", imgs)


if __name__ == "__main__":
    main()
