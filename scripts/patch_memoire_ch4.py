#!/usr/bin/env python3
"""Corrections de cohérence et mise à jour du chapitre IV du mémoire ART ZT."""

from copy import deepcopy
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.text.paragraph import Paragraph
from docx.table import Table

SRC = "/workspace/livrables/memoire/memoire_ART_ZT_travail.docx"
OUT = "/workspace/livrables/memoire/Memoire_ART_Zero_Trust_corrige.docx"
ART = "/opt/cursor/artifacts/memoire/Memoire_ART_Zero_Trust_corrige.docx"

# Mercuriale 2026 (Lefisk / BOND) — prestations intellectuelles
REF_ING = "32-003-220002"
TX_ING = 250_000  # FCFA / homme-jour — Ingénieur < 9 ans d'expérience
REF_CHEF = "32-003-220001"
TX_CHEF = 350_000  # FCFA / homme-jour — Chef de mission ingénieur > 9 ans

# Effort j-p (min, max) par lot
LOTS_JP = {
    "0": (3, 5),
    "1": (26, 39),
    "2": (24, 36),
    "3": (8, 12),
    "4": (8, 12),
    "Gouvernance": (5, 8),
}

# Estimation équipements (FCFA) — reprise de l'existant privilégiée ; montants indicatifs mercuriale rub. 01/35
# Lot 0: config publications — pas d'achat lourd
# Lot 1: MFA / serveur de test / jetons — serveur entrée de gamme + licences/tokens
# Lot 2: segmentation sur USG existant — câblage/switch de management éventuel
# Lot 3: extension couverture endpoint (licences)
# Lot 4: sauvegarde/doc données (hors SIEM si Visibilité hors périmètre)
EQUIP = {
    "0": (0, 250_000),
    "1": (1_500_000, 4_500_000),
    "2": (500_000, 2_500_000),
    "3": (800_000, 3_000_000),
    "4": (500_000, 2_000_000),
    "Gouvernance": (0, 150_000),
}


def insert_paragraph_after(paragraph, text="", style=None):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        new_para.add_run(text)
    if style is not None:
        new_para.style = style
    return new_para


def insert_table_after(paragraph, rows, cols):
    tbl = OxmlElement("w:tbl")
    tblPr = OxmlElement("w:tblPr")
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), "5000")
    tblW.set(qn("w:type"), "pct")
    tblPr.append(tblW)
    # style Table Grid if possible via tblStyle
    tblStyle = OxmlElement("w:tblStyle")
    tblStyle.set(qn("w:val"), "TableGrid")
    tblPr.append(tblStyle)
    tbl.append(tblPr)
    tblGrid = OxmlElement("w:tblGrid")
    for _ in range(cols):
        gc = OxmlElement("w:gridCol")
        tblGrid.append(gc)
    tbl.append(tblGrid)
    for _ in range(rows):
        tr = OxmlElement("w:tr")
        for _c in range(cols):
            tc = OxmlElement("w:tc")
            tcPr = OxmlElement("w:tcPr")
            tcW = OxmlElement("w:tcW")
            tcW.set(qn("w:w"), str(5000 // cols))
            tcW.set(qn("w:type"), "pct")
            tcPr.append(tcW)
            tc.append(tcPr)
            p = OxmlElement("w:p")
            tc.append(p)
            tr.append(tc)
        tbl.append(tr)
    paragraph._p.addnext(tbl)
    # return a Table wrapper — need the document body parent
    return tbl


def set_cell_text(cell, text):
    cell.text = ""
    p = cell.paragraphs[0]
    run = p.add_run(text)
    return run


def replace_in_paragraph(p, mapping):
    """Replace full-paragraph texts or substrings when unique."""
    t = p.text
    if not t:
        return False
    new = t
    for a, b in mapping:
        if a in new:
            new = new.replace(a, b)
    if new != t:
        # preserve roughly by clearing and rewriting
        if p.runs:
            p.runs[0].text = new
            for r in p.runs[1:]:
                r.text = ""
        else:
            p.add_run(new)
        return True
    return False


def delete_paragraph(paragraph):
    el = paragraph._element
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)


def delete_table(table):
    el = table._element
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)


def main():
    doc = Document(SRC)

    # ------------------------------------------------------------------
    # 1) Global text replacements (pillars, hypotheses, promises soft, typos)
    # ------------------------------------------------------------------
    para_repls = [
        (
            "sur les piliers Identité, Terminaux, Réseaux et Données.",
            "sur les quatre piliers retenus pour cette étude : Identité, Terminaux, Réseaux et Données. Le pilier Visibilité (ZTMM) est rappelé dans le cadre théorique mais n’est pas évalué ni dimensionné dans le périmètre de ce mémoire.",
        ),
        (
            "pilier par pilier (Identité, Terminaux, Réseaux, Données) selon le ZTMM v2.0.",
            "pilier par pilier sur les quatre piliers du périmètre (Identité, Terminaux, Réseaux, Données) selon le ZTMM v2.0.",
        ),
        (
            "Une amélioration de maturité chiffrée, d’au moins un palier sur chacun des piliers du périmètre, démontrée par des indicateurs mesurés avant et après la mise en œuvre.",
            "Une grille de maturité « avant » attestée et une grille de maturité « après » (même format), destinée à constater le passage éventuel d’un palier sur les piliers du périmètre une fois les lots exécutés et les tests du tableau des tests rejoués.",
        ),
        (
            "Un pilote fonctionnel, déployé en environnement contrôlé et validant les mesures retenues.",
            "Une maquette brownfield en environnement contrôlé, servant à préparer et, progressivement, à valider les mesures retenues.",
        ),
        (
            "Mettre en œuvre un pilote en environnement contrôlé pour valider les mesures retenues sur les piliers du périmètre.",
            "Mettre en œuvre une maquette en environnement contrôlé pour préparer la validation des mesures retenues sur les quatre piliers du périmètre.",
        ),
        (
            "IV.5. Indicateurs et hypothèses",
            "IV.5. Indicateurs avant / après",
        ),
        (
            "Configurations C0–C3 (H2) et mesure T12 (H4) : spécifiées, non exécutées au gel rédactionnel. Câblage / IP / politiques : en cours.",
            "Configurations C0–C3 et mesure T12 : spécifiées, non exécutées au gel rédactionnel. Câblage / IP / politiques : en cours.",
        ),
        (
            "Limites principales : exports pare-feu courts ; AD sans expansion complète des groupes imbriqués ; maquette 2016 / VPCS ; Données et Visibilité non évaluées ; H2 et H4 non encore mesurées ; notes EBIOS à valider en atelier.",
            "Limites principales : exports pare-feu courts ; AD sans expansion complète des groupes imbriqués ; maquette 2016 / VPCS ; pilier Données encore peu documenté ; notes EBIOS à consolider en atelier ; valeurs « après » de maturité à renseigner après exécution des lots.",
        ),
        (
            "Palier visé : Initial sur Identité, Terminaux et Réseaux (tests du tableau 7 à rendre OK), puis Données et Visibilité dès que les pièces existent.",
            "Palier visé sur le périmètre de l’étude : Initial sur Identité, Terminaux et Réseaux (tests de validation à rendre OK), puis Données dès que les pièces existent. La Visibilité ZTMM reste hors périmètre de notation de ce mémoire.",
        ),
        (
            "Identité et Réseaux : traditionnel ; Terminaux : traditionnel avec éléments initiaux ; Données et Visibilité : non évalués. L’architecture cible et la feuille de route (74–112 j-p) indiquent comment gagner un palier sans remplacer l’existant. La démonstration chiffrée « après » reste à compléter en maquette et en pilote.",
            "Sur les quatre piliers du périmètre : Identité et Réseaux au palier traditionnel ; Terminaux au palier traditionnel avec éléments initiaux ; Données non évaluée faute de pièces suffisantes. L’architecture cible et la feuille de route (74–112 j-p, plus estimation FCFA) indiquent comment viser un palier supérieur sans remplacer l’existant. Le tableau de maturité « après » et les indicateurs « après » sont le support de la démonstration chiffrée une fois les lots exécutés.",
        ),
        (
            "Tableau 5. Phases de la démarche et livrables",
            "Tableau 6. Phases de la démarche et livrables",
        ),
        (
            "Tableau 6. Règle de notation de la maturité",
            "Tableau 7. Règle de notation de la maturité",
        ),
        (
            "Tableau 7. Batterie de tests commune à l’audit et à la validation",
            "Tableau 8. Batterie de tests commune à l’audit et à la validation",
        ),
        (
            "Tableau 8. Indicateurs avant / après",
            "Tableau 9. Indicateurs avant / après",
        ),
        (
            "Tableau 9. Composition de la maquette",
            "Tableau 10. Composition de la maquette",
        ),
        (
            "Tableau 10. Score de maturité initial",
            "Tableau 11. Score de maturité initial",
        ),
        (
            "Tableau 11. Scénarios opérationnels",
            "Tableau 12. Scénarios opérationnels",
        ),
        (
            "Tableau 12. PE / PA / PEP (NIST SP 800-207)",
            "Tableau 13. PE / PA / PEP (NIST SP 800-207)",
        ),
        (
            "Tableau 13. Indicateurs disponibles",
            "Tableau 14. Indicateurs disponibles",
        ),
        (
            "Tableau 14. Lots (jours-personne)",
            "Tableau 16. Lots, effort et estimation des coûts (FCFA)",
        ),
        (
            "La notation suit le tableau 6 : sans pièce, on écrit « non évalué », pas « traditionnel ».",
            "La notation suit le tableau 7 : sans pièce, on écrit « non évalué », pas « traditionnel ».",
        ),
        (
            "Écarts vs tableau 9 :",
            "Écarts vs tableau 10 :",
        ),
        (
            "L’audit s’appuie sur les exports de production",
            "L’audit initial s’appuie sur les exports de production",
        ),
        # soften leftover hypothesis words if any short forms remain in other paras
        ("(H2)", ""),
        ("(H4)", ""),
    ]

    # Fix duplicate problematic paragraph (keep first, clear second if identical)
    seen_prob = None
    for p in doc.paragraphs:
        t = p.text.strip()
        if t.startswith("L'Agence de Régulations des Télécommunications, gendarme du secteur"):
            if seen_prob is None:
                seen_prob = t
            elif t == seen_prob or t.startswith("L'Agence de Régulations des Télécommunications, gendarme"):
                # blank duplicate
                for r in p.runs:
                    r.text = ""
                if not p.runs:
                    pass

    for p in doc.paragraphs:
        replace_in_paragraph(p, para_repls)

    # Remove "Décision distribuée..." paragraph entirely
    for p in list(doc.paragraphs):
        if "Décision distribuée" in p.text or "couplage natif KSC" in p.text:
            delete_paragraph(p)

    # ------------------------------------------------------------------
    # 2) Enrich IV.2 before scenarios table + bridge to Fig 7
    # ------------------------------------------------------------------
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("EBIOS sert ici à ordonner les écarts"):
            # expand this paragraph
            new_text = (
                "EBIOS sert ici à ordonner les écarts, non à produire une étude complète. "
                "V et G vont de 1 à 4 ; la priorité est le produit V×G.\n\n"
                "Lecture des colonnes du tableau des scénarios : "
                "le numéro (SO) identifie le chemin d’attaque ; "
                "le scénario le décrit ; "
                "les écarts sont les constats d’audit (tests Ti en échec) qui rendent ce chemin crédible aujourd’hui ; "
                "V×G fixe la priorité ; "
                "les tests sont les contrôles de la batterie commune qui seront rejoués après remédiation.\n\n"
                "Exemple — SO3 (hameçonnage → privilèges AD) : "
                "l’écart T2 signifie qu’un compte privilégié peut encore se connecter sans second facteur ; "
                "on arrange la mesure (MFA sur les comptes à privilèges) ; "
                "on vérifie en rejouant le test T2 (connexion refusée sans MFA) et le test T5 (chemins vers le niveau 0 de l’annuaire)."
            )
            if p.runs:
                p.runs[0].text = new_text
                for r in p.runs[1:]:
                    r.text = ""
            break

    for i, p in enumerate(doc.paragraphs):
        if "SO1, SO3 et SO5" in p.text and "orientent la feuille de route" in p.text:
            extra = (
                " SO1, SO3 et SO5 (score 12) orientent donc la feuille de route : publications, identité, segmentation. "
                "Ces priorités pilotent aussi la lecture de la Figure 7 (architecture PE / PA / PEP) : "
                "SO3 se joue surtout dans le moteur de décision (PE : AD, MFA) ; "
                "SO1 dans les points d’application réseau (PEP : USG, passerelle, publications) ; "
                "SO5 à cheval entre contrôles terminaux (KSC/KES, GPO) et filtrage réseau. "
                "Les écarts diagnostiquent ; l’architecture arrange ; les tests de la batterie commune valident."
            )
            # replace paragraph with clearer version
            if p.runs:
                p.runs[0].text = extra.strip()
                for r in p.runs[1:]:
                    r.text = ""
            break

    # Figure 7 caption / following note
    for p in doc.paragraphs:
        if p.text.strip().startswith("Figure 7. Architecture cible"):
            # add legend in same para or next — append to caption
            if p.runs:
                base = p.text.strip()
                p.runs[0].text = (
                    base
                    + " — Lecture : SO3 → PE (AD/MFA) → tests T2, T5 ; "
                    "SO1 → PEP réseau (USG/passerelle) → tests T9, T7 ; "
                    "SO5 → KSC/KES + USG → tests T3, T6 ; "
                    "SO2 → UniFi/RADIUS → T8 ; SO4 → AD → T1."
                )
                for r in p.runs[1:]:
                    r.text = ""
            break

    # ------------------------------------------------------------------
    # 3) Update Tableau 11 (maturity initial) - remove Visibilité or mark hors périmètre
    #    tables index: T9 is maturity initial
    # ------------------------------------------------------------------
    mat = doc.tables[9]
    # last row Visibilité -> hors périmètre
    for row in mat.rows[1:]:
        pilier = row.cells[0].text.strip()
        if pilier.startswith("Visibilité"):
            set_cell_text(row.cells[1], "Hors périmètre de notation de cette étude (ZTMM rappelé au chapitre II uniquement)")
            set_cell_text(row.cells[2], "Hors périmètre")
            set_cell_text(row.cells[3], "Non applicable")

    # ------------------------------------------------------------------
    # 4) Delete hypotheses table (index 13)
    # ------------------------------------------------------------------
    # After potential deletions, find by header
    for t in list(doc.tables):
        header = " | ".join(c.text.strip() for c in t.rows[0].cells)
        if header.startswith("Hypothèse"):
            delete_table(t)

    # ------------------------------------------------------------------
    # 5) Expand lots table with costs (find by header Lot | Contenu)
    # ------------------------------------------------------------------
    lots_table = None
    for t in doc.tables:
        h0 = t.rows[0].cells[0].text.strip()
        if h0 == "Lot" and "Contenu" in t.rows[0].cells[1].text:
            lots_table = t
            break

    if lots_table is not None:
        # Add columns by rewriting table content into a new wider table after caption
        # Easier: modify existing 4-col table cells and append 3 columns via XML
        # python-docx doesn't add columns easily — rebuild after the caption paragraph.

        # Find caption paragraph
        caption = None
        for p in doc.paragraphs:
            if "Tableau 16. Lots" in p.text or "Lots, effort" in p.text or p.text.strip().startswith("Tableau 14. Lots"):
                caption = p
                break
        if caption is None:
            for p in doc.paragraphs:
                if "feuille de route" in p.text.lower() and p.text.strip().startswith("IV.6"):
                    caption = p
                    break

        # Build data rows from existing
        data_rows = []
        for row in lots_table.rows[1:]:
            lot = row.cells[0].text.strip()
            contenu = row.cells[1].text.strip()
            priorite = row.cells[2].text.strip()
            jp = row.cells[3].text.strip()
            data_rows.append((lot, contenu, priorite, jp))

        # Delete old lots table
        delete_table(lots_table)

        # Prepare new values
        def prest(lo, hi):
            return f"{lo * TX_ING:,} – {hi * TX_ING:,}".replace(",", " ")

        new_rows = [
            ["Lot", "Contenu", "Priorité", "j-p", "Prestation intellectuelle (FCFA HT)", "Équipements (FCFA HT, estim.)", "Total lot (FCFA HT, estim.)"],
        ]
        tot_p_lo = tot_p_hi = tot_e_lo = tot_e_hi = 0
        mapping_contenu = {
            "0": "Publications, gestion, SNMPv3",
            "1": "Identité (T1, T2, puis T3–T5)",
            "2": "Réseaux / segmentation (T7–T9)",
            "3": "Terminaux (T10, T11, I8)",
            "4": "Données (pilier du périmètre)",
            "Gouvernance": "Charte, incidents, sensibilisation",
            "Total": "",
        }
        # Prefer existing contenu when present
        for lot, contenu, priorite, jp in data_rows:
            key = lot if lot in LOTS_JP or lot == "Total" or lot == "Gouvernance" else lot
            if lot == "Total":
                continue
            if "Données + Visibilité" in contenu or contenu.startswith("Données"):
                contenu = "Données (pilier du périmètre ; Visibilité hors notation)"
            if lot not in LOTS_JP and lot != "Gouvernance":
                # try first token
                pass
            jp_key = "Gouvernance" if "Gouvernance" in lot or lot == "Gouvernance" else lot
            if jp_key not in LOTS_JP:
                # parse from jp text
                lo, hi = 0, 0
            else:
                lo, hi = LOTS_JP[jp_key]
            e_lo, e_hi = EQUIP.get(jp_key, (0, 0))
            p_lo, p_hi = lo * TX_ING, hi * TX_ING
            tot_p_lo += p_lo
            tot_p_hi += p_hi
            tot_e_lo += e_lo
            tot_e_hi += e_hi
            new_rows.append([
                lot,
                contenu,
                priorite,
                jp if jp else f"{lo}–{hi}",
                f"{p_lo:,} – {p_hi:,}".replace(",", " "),
                f"{e_lo:,} – {e_hi:,}".replace(",", " "),
                f"{p_lo + e_lo:,} – {p_hi + e_hi:,}".replace(",", " "),
            ])

        new_rows.append([
            "Total",
            "",
            "",
            "74–112",
            f"{tot_p_lo:,} – {tot_p_hi:,}".replace(",", " "),
            f"{tot_e_lo:,} – {tot_e_hi:,}".replace(",", " "),
            f"{tot_p_lo + tot_e_lo:,} – {tot_p_hi + tot_e_hi:,}".replace(",", " "),
        ])

        # Insert note + table after IV.6 / caption area
        anchor = None
        for p in doc.paragraphs:
            if p.text.strip().startswith("IV.6. Feuille de route") or "Tableau 16. Lots" in p.text:
                anchor = p
                break
        if anchor is None:
            for p in doc.paragraphs:
                if p.text.strip().startswith("IV.7. Discussion"):
                    anchor = p
                    break

        note = (
            "Bases de chiffrage : prestations intellectuelles informatiques a 250 000 FCFA HT / homme-jour "
            "(Mercuriale des prix de l'Etat du Cameroun, exercice 2026, ref. 32-003-220002 — "
            "Honoraire d'un ingenieur ayant moins de 9 ans d'experience, unite homme par jour). "
            "A titre de comparaison, le chef de mission ingenieur (> 9 ans) est a 350 000 FCFA HT / homme-jour "
            "(ref. 32-003-220001). Les fourchettes d'equipements sont indicatives "
            "(rubriques informatique / reseaux de la mercuriale) et privilegient la reutilisation "
            "de l'existant (USG, AD, KSC) ; elles ne constituent pas un devis d'achat."
        )
        # accents
        note = (
            "Bases de chiffrage : prestations intellectuelles informatiques à 250 000 FCFA HT / homme-jour "
            "(Mercuriale des prix de l'État du Cameroun, exercice 2026, réf. 32-003-220002 — "
            "Honoraire d'un ingénieur ayant moins de 9 ans d'expérience, unité homme par jour). "
            "À titre de comparaison, le chef de mission ingénieur (> 9 ans) est à 350 000 FCFA HT / homme-jour "
            "(réf. 32-003-220001). Les fourchettes d'équipements sont indicatives "
            "(rubriques informatique / réseaux de la mercuriale) et privilégient la réutilisation "
            "de l'existant (USG, AD, KSC) ; elles ne constituent pas un devis d'achat."
        )

        if anchor is not None:
            # ensure caption
            if not anchor.text.strip().startswith("Tableau"):
                # add caption after IV.6 heading
                cap = insert_paragraph_after(anchor, "Tableau 16. Lots, effort et estimation des coûts (FCFA)")
                npara = insert_paragraph_after(cap, note)
                # insert table after note by creating via body
                # Use document.add_table then move — simpler approach: add at end then move XML
                tbl = doc.add_table(rows=len(new_rows), cols=7)
                tbl.style = "Table Grid"
                for ri, rowvals in enumerate(new_rows):
                    for ci, val in enumerate(rowvals):
                        set_cell_text(tbl.rows[ri].cells[ci], val)
                # move table after npara
                npara._p.addnext(tbl._tbl)
            else:
                npara = insert_paragraph_after(anchor, note)
                tbl = doc.add_table(rows=len(new_rows), cols=7)
                tbl.style = "Table Grid"
                for ri, rowvals in enumerate(new_rows):
                    for ci, val in enumerate(rowvals):
                        set_cell_text(tbl.rows[ri].cells[ci], val)
                npara._p.addnext(tbl._tbl)

    # ------------------------------------------------------------------
    # 6) Insert maturité après BEFORE feuille de route (IV.6 becomes maturité après, shift)
    # ------------------------------------------------------------------
    # Renumber sections in chapter IV
    section_repls = [
        ("IV.5. Indicateurs avant / après", "IV.5. Indicateurs avant / après"),
        ("IV.6. Feuille de route", "IV.7. Feuille de route"),
        ("IV.7. Discussion et limites", "IV.8. Discussion et limites"),
    ]
    for p in doc.paragraphs:
        replace_in_paragraph(p, section_repls)

    # Insert IV.6 maturité finale before IV.7 Feuille de route
    for p in doc.paragraphs:
        if p.text.strip().startswith("IV.7. Feuille de route"):
            # insert block before this heading by adding previous siblings in reverse
            # We'll insert after previous paragraph instead: find previous and append after indicators section
            break

    # Find IV.5 end — paragraph Tableau 14 or after indicators table area
    insert_after = None
    for p in doc.paragraphs:
        if "Tableau 14. Indicateurs" in p.text or p.text.strip() == "IV.5. Indicateurs avant / après":
            insert_after = p
    # Better: insert immediately before IV.7
    before = None
    for p in doc.paragraphs:
        if p.text.strip().startswith("IV.7. Feuille de route"):
            before = p
            break

    if before is not None:
        # Create heading and content BEFORE `before` using previous paragraph
        prev = before._p.getprevious()
        # Walk to a paragraph element
        from docx.oxml.ns import qn as _qn

        # Insert sequence before `before`: heading, text, caption, table, note
        def prepend_para(text):
            new_p = OxmlElement("w:p")
            before._p.addprevious(new_p)
            para = Paragraph(new_p, before._parent)
            para.add_run(text)
            return para

        # addprevious stacks in reverse order if we call multiple times — so add in reverse
        note2 = prepend_para(
            "Les cases « Palier » et « Statut » sont à renseigner après exécution des lots et rejeu des tests de validation. "
            "Le format est identique au tableau de maturité initial afin de permettre une comparaison opposable."
        )
        # table
        tbl = doc.add_table(rows=5, cols=4)
        tbl.style = "Table Grid"
        headers = ["Pilier", "Constats / preuves après travaux", "Palier", "Statut"]
        for ci, h in enumerate(headers):
            set_cell_text(tbl.rows[0].cells[ci], h)
        pillars = [
            ("Identité", "[À renseigner]", "[À renseigner]", "[À renseigner]"),
            ("Terminaux", "[À renseigner]", "[À renseigner]", "[À renseigner]"),
            ("Réseaux", "[À renseigner]", "[À renseigner]", "[À renseigner]"),
            ("Données", "[À renseigner]", "[À renseigner]", "[À renseigner]"),
        ]
        for ri, vals in enumerate(pillars, start=1):
            for ci, v in enumerate(vals):
                set_cell_text(tbl.rows[ri].cells[ci], v)
        before._p.addprevious(tbl._tbl)

        prepend_para("Tableau 15. Score de maturité après travaux (même grille que le tableau initial)")
        prepend_para(
            "Ce tableau reprend le même format que le score de maturité initial. "
            "Il constitue le résultat « après » attendu sur les quatre piliers du périmètre "
            "(Identité, Terminaux, Réseaux, Données). Les valeurs sont à compléter par l’auteur "
            "lorsque les lots prioritaires auront été exécutés et les tests rejoués."
        )
        prepend_para("IV.6. Maturité Zero Trust après travaux")

    # Remove leftover placeholder cost line
    for p in list(doc.paragraphs):
        if "À compléter : coût journalier ART" in p.text:
            delete_paragraph(p)

    # Clean any remaining "hypothèse" mentions lightly
    for p in doc.paragraphs:
        t = p.text
        if not t:
            continue
        if "hypothèse" in t.lower() or "Hypothèse" in t:
            # specific cleanups
            nt = t
            nt = nt.replace("et des plans d’expérience liés aux hypothèses", "et des plans d’expérience de validation")
            nt = nt.replace("et hypothèses", "")
            nt = nt.replace("Hypothèses de chiffrage", "Bases de chiffrage")  # keep cost basis wording clear
            if "Bases de chiffrage" in nt or "Hypothèses de chiffrage" in t:
                # For the cost paragraph we intentionally had "Hypothèses de chiffrage" — change to Bases
                pass
            if nt != t and p.runs:
                p.runs[0].text = nt.replace("Hypothèses de chiffrage", "Bases de chiffrage")
                for r in p.runs[1:]:
                    r.text = ""

    # Figure numbering note for maturity figure
    for p in doc.paragraphs:
        if p.text.strip().startswith("Figure — Synthèse de maturité"):
            if p.runs:
                p.runs[0].text = "Figure 6. Synthèse de maturité initiale"
                for r in p.runs[1:]:
                    r.text = ""

    # Intro chapter plan: ensure 4 chapters mention remains
    # Fix "tests du tableau 7" references that now shifted — already handled some

    # References in methodology conclusion "onze indicateurs" ok

    doc.save(OUT)
    doc.save(ART)
    print("Saved", OUT)
    print("Saved", ART)

    # Verification pass
    doc2 = Document(OUT)
    print("\n--- VERIFY ---")
    for i, p in enumerate(doc2.paragraphs):
        t = p.text.strip()
        if any(k in t for k in ["IV.", "Tableau 1", "Figure 7", "hypothèse", "Hypothèse", "H2", "H4", "Décision distribuée", "Visibilité", "SO1, SO3", "Bases de chiffrage", "Mercuriale", "quatre piliers", "Maturité Zero Trust après"]):
            if t:
                print(f"{i}: {t[:220]}")
    print("tables", len(doc2.tables))
    for ti, t in enumerate(doc2.tables):
        print(ti, " | ".join(c.text.strip()[:30] for c in t.rows[0].cells))


if __name__ == "__main__":
    main()
