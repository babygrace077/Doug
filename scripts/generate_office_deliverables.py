#!/usr/bin/env python3
"""Génère les livrables Word, PowerPoint et Excel du dossier de cadrage ART."""

from pathlib import Path
from datetime import date, timedelta

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt, Emu
from pptx.dml.color import RGBColor as RgbColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference

ROOT = Path("/workspace/livrables")
WORD = ROOT / "word"
PPT = ROOT / "powerpoint"
XLS = ROOT / "excel"

THEME = (
    "Proposition d’une architecture Zero Trust pour le contrôle de "
    "fidélité des agents IA : cadre de sécurisation et prototype "
    "applicables aux processus métier de l’ART Cameroun."
)
STAGIAIRE = "Grace Divine Tchuenteu Ebe'ete"
ORG = "Agence de Régulation des Télécommunications (ART) — Cameroun"
START = date(2026, 7, 21)


# ---------------------------------------------------------------------------
# Helpers Word
# ---------------------------------------------------------------------------

def set_run_font(run, size=11, bold=False, color=None, name="Calibri"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_heading_custom(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        set_run_font(run, size=16 if level == 1 else 13, bold=True, color=(0x0B, 0x3D, 0x5C))
    return p


def add_para(doc, text, size=11, bold=False, italic=False, space_after=6):
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    run.italic = italic
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    return p


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(item, style="List Bullet")
        for run in p.runs:
            set_run_font(run, size=11)


def set_cell_shading(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        run = p.add_run(h)
        set_run_font(run, size=10, bold=True, color=(255, 255, 255))
        set_cell_shading(hdr[i], "0B3D5C")
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            set_run_font(run, size=10)
            if r_idx % 2 == 1:
                set_cell_shading(cell, "E8F1F8")
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph()
    return table


def setup_doc():
    doc = Document()
    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
    return doc


def add_cover_block(doc, title, subtitle=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("ART CAMEROUN — MÉMOIRE DE STAGE")
    set_run_font(run, size=12, bold=True, color=(0x0B, 0x3D, 0x5C))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(title)
    set_run_font(run, size=16, bold=True, color=(0x0B, 0x3D, 0x5C))

    if subtitle:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(subtitle)
        set_run_font(run, size=11)
        run.italic = True

    add_para(doc, f"Stagiaire : {STAGIAIRE}", size=11)
    add_para(doc, f"Structure : {ORG}", size=11)
    add_para(doc, f"Date de référence : {START.strftime('%d/%m/%Y')}", size=11)
    doc.add_paragraph()


# ---------------------------------------------------------------------------
# Word documents
# ---------------------------------------------------------------------------

def build_word_note_defense():
    doc = setup_doc()
    add_cover_block(doc, "Note de cadrage — Défense du thème", "Document d’1 page pour validation encadreur")

    add_heading_custom(doc, "1. Thème proposé", 1)
    add_para(doc, THEME, bold=True)

    add_heading_custom(doc, "2. Pourquoi ce thème ?", 1)
    add_para(
        doc,
        "L’ART manipule des informations et des processus sensibles. L’usage d’agents IA "
        "(systèmes capables d’agir via des outils : lecture de documents, appels d’API, rédaction) "
        "crée des risques nouveaux : manipulation (prompt injection), actions non autorisées, "
        "fuite de données et absence d’audit.",
    )
    add_para(
        doc,
        "Le Zero Trust (« ne jamais faire confiance par défaut, toujours vérifier ») offre un cadre "
        "adapté : chaque action de l’agent est authentifiée, autorisée, tracée. La fidélité désigne "
        "ici la conformité des actions de l’agent à sa mission et aux politiques de sécurité.",
    )

    add_heading_custom(doc, "3. Problématique", 1)
    add_para(
        doc,
        "Comment concevoir et démontrer une architecture Zero Trust capable de garantir la fidélité "
        "des actions d’un agent IA dans un cas d’usage réaliste de l’ART ?",
        italic=True,
    )

    add_heading_custom(doc, "4. Objectifs et livrables (2 mois)", 1)
    add_table(
        doc,
        ["Objectif", "Livrable"],
        [
            ["Cadre théorique ciblé", "État de l’art Zero Trust × sécurité des agents"],
            ["Ancrage ART", "1 cas d’usage (ex. assistance documentaire réglementaire)"],
            ["Conception", "Architecture (identité, politiques, PEP/PDP, audit)"],
            ["Preuve", "Prototype (PoC) + ≥ 3 scénarios d’attaque simulés"],
            ["Valorisation", "Mémoire + note de recommandations ART + soutenance"],
        ],
        [6, 11],
    )
    add_para(
        doc,
        "Hors périmètre assumé : déploiement production, entraînement de modèle, couverture de tous les métiers de l’Agence.",
        italic=True,
    )

    add_heading_custom(doc, "5. Méthode", 1)
    add_para(
        doc,
        "Analyse du besoin → conception d’architecture → prototypage → tests de sécurité → rédaction et soutenance. "
        "Reporting bihebdomadaire (mardi/vendredi) pendant 8 semaines.",
    )

    add_heading_custom(doc, "6. Intérêt pour l’ART", 1)
    add_bullets(
        doc,
        [
            "Anticiper l’encadrement sécurisé d’outils d’IA agentique.",
            "Disposer d’un cadre de contrôle (politique + audit) réutilisable.",
            "Recevoir des recommandations opérationnelles sobres et actionnables.",
        ],
    )

    add_heading_custom(doc, "7. Critères de succès à la soutenance", 1)
    add_para(
        doc,
        "Architecture documentée ; PoC démontrable ; actions d’outils journalisées ; "
        "au moins trois scénarios de sécurité ; mémoire structuré ; recommandations ART.",
    )

    add_heading_custom(doc, "8. Demande à l’encadreur", 1)
    add_para(
        doc,
        "Validation de : (i) l’intitulé, (ii) le cas d’usage unique, (iii) le périmètre PoC (hors production), "
        "(iv) le planning 8 semaines.",
    )
    add_table(
        doc,
        ["Décision", "Visa"],
        [["☐ Validé    ☐ Validé avec réserves    ☐ À retravailler", "Date / Signature : ____________________"]],
        [10, 7],
    )

    path = WORD / "01_Note_defense_theme_encadreur.docx"
    doc.save(path)
    return path


def build_word_theme():
    doc = setup_doc()
    add_cover_block(doc, "Thème reformulé du mémoire", "Périmètre réalisable en 2 mois")

    add_heading_custom(doc, "Thème initial")
    add_para(
        doc,
        "Architecture sécurisée basée sur le « Zero Trust Fidelity » pour augmenter le taux de sécurité des IA agentiques.",
    )

    add_heading_custom(doc, "Thème reformulé (recommandé)")
    add_para(doc, THEME, bold=True)

    add_heading_custom(doc, "Concepts clés")
    add_table(
        doc,
        ["Concept", "Définition opérationnelle"],
        [
            ["IA agentique", "Système IA capable d’enchaîner des actions (outils, APIs, fichiers)"],
            ["Zero Trust", "Never trust, always verify : aucune confiance par défaut"],
            ["Fidélité de l’agent", "Actions autorisées, traçables et conformes à la mission"],
            ["Contrôle de fidélité", "Validation avant chaque action : identité, politique, audit"],
        ],
        [4.5, 12.5],
    )

    add_heading_custom(doc, "Périmètre IN SCOPE")
    add_bullets(
        doc,
        [
            "État de l’art ciblé (Zero Trust NIST, menaces agents IA)",
            "Analyse d’un cas d’usage ART unique",
            "Conception d’architecture Zero Trust (PEP/PDP, identité, audit)",
            "Prototype PoC avec ≥ 3 scénarios d’attaque",
            "Évaluation comparative simple + mémoire + soutenance",
        ],
    )

    add_heading_custom(doc, "Périmètre OUT OF SCOPE")
    add_bullets(
        doc,
        [
            "Déploiement en production sur le SI de l’ART",
            "Entraînement d’un modèle de fondation",
            "Certification réglementaire formelle",
            "Couverture de tous les processus de l’Agence",
        ],
    )

    add_heading_custom(doc, "Cas d’usage recommandé")
    add_para(
        doc,
        "Agent d’assistance à l’analyse documentaire réglementaire : lecture/résumé/classement de documents "
        "autorisés ; interdiction d’écrire hors périmètre, d’appeler des APIs non listées, d’exporter hors journal.",
    )

    add_heading_custom(doc, "Critères de succès")
    add_table(
        doc,
        ["Indicateur", "Cible"],
        [
            ["Architecture documentée", "Diagrammes + composants Zero Trust"],
            ["PoC exécutable", "Démo ≤ 10 min"],
            ["Politiques", "≥ 5 règles d’autorisation"],
            ["Scénarios de sécurité", "≥ 3 attaques simulées"],
            ["Traçabilité", "100 % des actions d’outil journalisées"],
            ["Mémoire", "Structure complète + bibliographie"],
        ],
        [6, 11],
    )

    path = WORD / "02_Theme_reformule.docx"
    doc.save(path)
    return path


def build_word_cdc():
    doc = setup_doc()
    add_cover_block(doc, "Cahier des charges — Livrables du projet", "Stage ART Cameroun — 8 semaines")

    add_heading_custom(doc, "1. Identification")
    add_table(
        doc,
        ["Élément", "Contenu"],
        [
            ["Intitulé", THEME],
            ["Organisme", "ART Cameroun"],
            ["Durée", "8 semaines (soutenance J60)"],
            ["Nature", "Mémoire de stage + prototype de démonstration (PoC)"],
        ],
        [4, 13],
    )

    add_heading_custom(doc, "2. Problématique")
    add_para(
        doc,
        "Comment concevoir et démontrer une architecture Zero Trust capable de garantir la fidélité "
        "des actions d’un agent IA dans un contexte métier de l’ART ?",
        italic=True,
    )

    add_heading_custom(doc, "3. Objectifs spécifiques")
    add_bullets(
        doc,
        [
            "Synthétiser l’état de l’art Zero Trust et menaces des IA agentiques",
            "Analyser les besoins de sécurité d’un processus métier ART",
            "Concevoir une architecture Zero Trust (identités, politiques, PEP/PDP, audit)",
            "Réaliser un PoC démontrant le blocage d’actions non conformes",
            "Évaluer le gain de sécurité via des scénarios de test",
            "Formuler des recommandations pour l’ART",
        ],
    )

    add_heading_custom(doc, "4. Exigences fonctionnelles (PoC)")
    add_table(
        doc,
        ["ID", "Exigence", "Priorité"],
        [
            ["EF-01", "Authentifier l’agent via une identité / jeton", "Must"],
            ["EF-02", "Intercepter chaque demande d’outil avant exécution", "Must"],
            ["EF-03", "Décider autoriser / refuser selon une politique", "Must"],
            ["EF-04", "Journaliser toute décision et toute action", "Must"],
            ["EF-05", "Simuler au moins 3 scénarios d’attaque", "Must"],
            ["EF-06", "Tableau de bord simple d’audit", "Should"],
            ["EF-07", "Gérer plusieurs rôles d’agent", "Should"],
            ["EF-08", "Intégration SI réel ART", "Won’t"],
        ],
        [2.5, 11, 3],
    )

    add_heading_custom(doc, "5. Livrables")
    add_table(
        doc,
        ["Code", "Livrable", "Échéance"],
        [
            ["L1", "Note de cadrage", "Semaine 1"],
            ["L2", "État de l’art synthétique", "Semaines 1–2"],
            ["L3", "Analyse existant / besoins ART", "Semaines 2–3"],
            ["L4", "Architecture cible", "Semaines 3–4"],
            ["L5", "Prototype PoC", "Semaines 4–6"],
            ["L6", "Rapport de tests & résultats", "Semaines 6–7"],
            ["L7", "Mémoire complet", "Semaine 8"],
            ["L8", "Recommandations ART", "Semaine 7"],
            ["L9", "Soutenance (diapo + démo)", "J60"],
        ],
        [2.5, 9, 5],
    )

    add_heading_custom(doc, "6. Stack technique suggérée")
    add_bullets(
        doc,
        [
            "Langage : Python",
            "Orchestration agent : LangChain / script custom minimal",
            "Politiques : YAML/JSON (+ OPA/Rego si connu)",
            "Identité : JWT / API key signée",
            "Audit : logs JSON + UI simple (Streamlit ou FastAPI)",
            "LLM : API cloud, modèle local, ou mode mock si accès limité",
        ],
    )

    add_heading_custom(doc, "7. Risques et mitigation")
    add_table(
        doc,
        ["Risque", "Impact", "Mitigation"],
        [
            ["Accès limité aux données ART", "Moyen", "Données fictives réalistes"],
            ["Pas d’accès LLM", "Élevé", "Mode mock + focus contrôles"],
            ["Sujet trop large", "Élevé", "Cas d’usage unique + OUT OF SCOPE"],
            ["Retard mémoire", "Élevé", "Rédaction continue dès S2"],
        ],
        [6, 3, 8],
    )

    path = WORD / "03_Cahier_des_charges.docx"
    doc.save(path)
    return path


def build_word_structure_memoire():
    doc = setup_doc()
    add_cover_block(doc, "Structure détaillée du mémoire", "Canevas adapté Zero Trust / Agents IA / ART")

    add_heading_custom(doc, "Pages liminaires")
    add_bullets(
        doc,
        [
            "Page de garde, attestation, remerciements",
            "Résumé FR + Abstract EN",
            "Listes des figures, tableaux, sigles",
            "Table des matières",
        ],
    )

    chapters = [
        (
            "Introduction générale (4–6 p.)",
            [
                "Contexte digitalisation / IA / régulation télécoms",
                "Problématique, objectifs, hypothèses",
                "Intérêt pour l’ART, méthodologie, annonce du plan",
            ],
        ),
        (
            "Chapitre 1 — Cadre théorique et état de l’art (10–12 p.)",
            [
                "Agents IA : concepts et architectures",
                "Menaces et vulnérabilités agentiques",
                "Paradigme Zero Trust (NIST SP 800-207)",
                "Fidélité des agents et gouvernance",
                "Travaux connexes et positionnement",
            ],
        ),
        (
            "Chapitre 2 — ART et analyse du besoin (8–10 p.)",
            [
                "Présentation de l’ART et du service d’accueil",
                "Cas d’usage retenu (as-is)",
                "Analyse des risques liés à un agent IA",
                "Contraintes organisationnelles, techniques, juridiques",
            ],
        ),
        (
            "Chapitre 3 — Conception architecture Zero Trust (10–12 p.)",
            [
                "Principes de conception",
                "Architecture logique (Agent, PEP, PDP, Identity, Audit, LLM)",
                "Modèle d’identité et de politiques de fidélité",
                "Flux de contrôle d’une action (séquence)",
                "Modèle de menaces et choix techniques du PoC",
            ],
        ),
        (
            "Chapitre 4 — Réalisation du prototype (8–10 p.)",
            [
                "Environnement, composants, politiques, interfaces",
                "Difficultés rencontrées et solutions",
            ],
        ),
        (
            "Chapitre 5 — Tests, résultats et discussion (6–8 p.)",
            [
                "Protocole de test et scénarios (≥ 3)",
                "Résultats, interprétation, limites",
            ],
        ),
        (
            "Conclusion générale et perspectives (3–4 p.)",
            [
                "Apports, limites, perspectives ART",
            ],
        ),
    ]

    for title, items in chapters:
        add_heading_custom(doc, title, 1)
        add_bullets(doc, items)

    add_heading_custom(doc, "Bibliographie & annexes")
    add_bullets(
        doc,
        [
            "NIST SP 800-207, NIST AI RMF, OWASP LLM Top 10, ISO 27001…",
            "Annexes : CDC, diagrammes, politiques, guide PoC, fiches points d’étape, note ART",
        ],
    )

    add_heading_custom(doc, "Volume indicatif")
    add_table(
        doc,
        ["Partie", "Pages"],
        [
            ["Introduction", "5"],
            ["Chapitre 1", "11"],
            ["Chapitre 2", "9"],
            ["Chapitre 3", "11"],
            ["Chapitre 4", "9"],
            ["Chapitre 5", "7"],
            ["Conclusion", "3"],
            ["Total corps", "~55"],
        ],
        [10, 4],
    )

    path = WORD / "04_Structure_memoire.docx"
    doc.save(path)
    return path


def build_word_plan_hebdo():
    doc = setup_doc()
    add_cover_block(doc, "Plan hebdomadaire détaillé", "8 semaines — 2 points d’étape / semaine")

    weeks = [
        (
            "Semaine 1 — Cadrage",
            "Validation du thème et du cas d’usage",
            [
                "Relire missions ART, choisir 1 cas d’usage",
                "Rédiger note de cadrage",
                "Lister 15–20 références, installer l’environnement",
            ],
            "Note de cadrage v1 + liste de références",
            "Thème reformulé + cas d’usage possibles",
            "Thème validé + planning 8 semaines",
        ),
        (
            "Semaine 2 — État de l’art & immersion ART",
            "Socle théorique + ancrage réel",
            [
                "Draft Ch.1 (agents, menaces, Zero Trust)",
                "Fiches de lecture (≥ 8 sources)",
                "Décrire processus métier as-is",
            ],
            "Draft Ch.1 partiel + fiche processus",
            "Schéma agent IA + principes Zero Trust",
            "Processus ART + premières exigences",
        ),
        (
            "Semaine 3 — Risques & exigences",
            "Exigences de sécurité testables",
            [
                "Matrice des actifs",
                "Analyse de menaces (STRIDE simplifié)",
                "Draft Ch.2",
            ],
            "Spécification besoins & risques v1",
            "Top 5 menaces + impacts ART",
            "Exigences Must/Should + périmètre PoC",
        ),
        (
            "Semaine 4 — Conception architecture",
            "Architecture claire et implémentable",
            [
                "Diagrammes contexte / composants / séquence",
                "≥ 5 politiques de fidélité",
                "Draft Ch.3 (~70 %)",
            ],
            "Dossier conception v1",
            "Architecture logique + rôles composants",
            "Séquence d’autorisation + plan S5–S6",
        ),
        (
            "Semaine 5 — PoC alpha",
            "Chemin heureux démontrable",
            [
                "Identity + jeton agent",
                "PEP + Policy Engine + 2–3 outils fictifs",
                "Journal JSON + README",
            ],
            "PoC alpha + captures",
            "Démo partielle authentification + 1 outil",
            "Démo alpha complète + log d’audit",
        ),
        (
            "Semaine 6 — Tests & PoC beta",
            "Preuve du gain de sécurité",
            [
                "3 scénarios d’attaque documentés",
                "Comparaison sans ZT / avec ZT",
                "Draft Ch.5",
            ],
            "Rapport de tests v1 + PoC beta",
            "Attaques #1 et #2 en live",
            "3 scénarios + interprétation",
        ),
        (
            "Semaine 7 — Rédaction & recommandations",
            "Draft mémoire ~80 %",
            [
                "Consolider Intro + Ch.1 à Ch.5",
                "Note recommandations ART (2–4 p.)",
                "Plan du diaporama",
            ],
            "Draft mémoire ~80 % + note ART",
            "ToC définitive + % par chapitre",
            "Recommandations + plan soutenance",
        ),
        (
            "Semaine 8 — Finalisation & soutenance",
            "Pack soutenance prêt",
            [
                "Mémoire final + annexes",
                "Diaporama + répétitions",
                "Soutenance le dernier jour (J60)",
            ],
            "Mémoire PDF + slides + PoC + note ART",
            "Diapo v1 + checklist livrables",
            "Répétition générale + démo finale",
        ),
    ]

    for title, obj, works, livrable, pta, ptb in weeks:
        add_heading_custom(doc, title, 1)
        add_para(doc, f"Objectif : {obj}", bold=True)
        add_para(doc, "Travaux :", bold=True)
        add_bullets(doc, works)
        add_para(doc, f"Livrable clé : {livrable}")
        add_para(doc, f"Point mardi : {pta}")
        add_para(doc, f"Point vendredi : {ptb}")

    add_heading_custom(doc, "Modèle de fiche de point d’étape")
    add_bullets(
        doc,
        [
            "1. Objectif de la période",
            "2. Travaux réalisés",
            "3. Livrables produits",
            "4. Écarts vs planning",
            "5. Blocages / besoins d’arbitrage",
            "6. Plan jusqu’au prochain point",
            "7. Indicateurs (% mémoire, % PoC, nb scénarios)",
        ],
    )

    path = WORD / "05_Plan_hebdomadaire.docx"
    doc.save(path)
    return path


def build_word_synthese():
    doc = setup_doc()
    add_cover_block(doc, "Synthèse du projet de stage", "Vue d’ensemble — ART Cameroun")
    add_heading_custom(doc, "Thème")
    add_para(doc, THEME, bold=True)
    add_heading_custom(doc, "Objectif")
    add_para(
        doc,
        "Concevoir et prototyper une architecture Zero Trust qui vérifie en continu l’identité, "
        "les permissions et la fidélité d’un agent IA avant chaque accès à un outil ou une donnée sensible.",
    )
    add_heading_custom(doc, "Livrables à la soutenance")
    add_table(
        doc,
        ["#", "Livrable", "Forme"],
        [
            ["1", "Mémoire de stage structuré", "PDF / Word"],
            ["2", "Architecture Zero Trust documentée", "Chapitre + diagrammes"],
            ["3", "Prototype fonctionnel (PoC)", "Démo + code"],
            ["4", "Scénarios de test de sécurité", "Rapport de résultats"],
            ["5", "Recommandations ART", "Note opérationnelle"],
            ["6", "Soutenance orale", "Diaporama"],
        ],
        [1.5, 8, 7],
    )
    path = WORD / "00_Synthese_projet.docx"
    doc.save(path)
    return path


# ---------------------------------------------------------------------------
# PowerPoint helpers
# ---------------------------------------------------------------------------

NAVY = RgbColor(0x0B, 0x3D, 0x5C)
TEAL = RgbColor(0x1F, 0x7A, 0x8C)
LIGHT = RgbColor(0xE8, 0xF1, 0xF8)
DARK = RgbColor(0x1A, 0x1A, 0x1A)
WHITE = RgbColor(0xFF, 0xFF, 0xFF)
ACCENT = RgbColor(0xC4, 0x5C, 0x26)


def add_bg(slide, color=None):
    fill = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, PInches(13.333), PInches(7.5)
    )
    fill.fill.solid()
    fill.fill.fore_color.rgb = color or LIGHT
    fill.line.fill.background()
    # send to back
    spTree = slide.shapes._spTree
    sp = fill._element
    spTree.remove(sp)
    spTree.insert(2, sp)


def add_header_bar(slide, title):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, PInches(13.333), PInches(0.9)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = NAVY
    bar.line.fill.background()
    tf = bar.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = PPt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"
    tf.margin_left = PInches(0.4)
    tf.margin_top = PInches(0.22)


def add_footer(slide, page, total):
    box = slide.shapes.add_textbox(PInches(0.4), PInches(7.1), PInches(12.5), PInches(0.3))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = f"ART Cameroun — Stage {STAGIAIRE}  |  {page}/{total}"
    p.font.size = PPt(10)
    p.font.color.rgb = TEAL
    p.font.name = "Calibri"


def add_text_box(slide, left, top, width, height, text, size=16, bold=False, color=None, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(PInches(left), PInches(top), PInches(width), PInches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = PPt(size)
    p.font.bold = bold
    p.font.color.rgb = color or DARK
    p.font.name = "Calibri"
    p.alignment = align
    return box


def add_bullets_box(slide, left, top, width, height, items, size=16):
    box = slide.shapes.add_textbox(PInches(left), PInches(top), PInches(width), PInches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.size = PPt(size)
        p.font.color.rgb = DARK
        p.font.name = "Calibri"
        p.space_after = PPt(8)
    return box


def new_prs():
    prs = Presentation()
    prs.slide_width = PInches(13.333)
    prs.slide_height = PInches(7.5)
    return prs


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def build_pptx_defense_theme():
    prs = new_prs()
    slides_meta = []

    # 1 title
    s = blank_slide(prs)
    add_bg(s, NAVY)
    add_text_box(s, 0.8, 1.5, 11.5, 0.5, "VALIDATION DU THÈME DE MÉMOIRE", 18, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 2.2, 11.5, 1.8, THEME, 24, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 4.4, 11.5, 0.4, STAGIAIRE, 16, False, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 4.9, 11.5, 0.4, ORG, 14, False, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 5.5, 11.5, 0.4, "Durée restante : 2 mois  •  Soutenance le dernier jour du 2ᵉ mois", 14, False, WHITE, PP_ALIGN.CENTER)
    slides_meta.append(s)

    # 2 contexte
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "1. Contexte et enjeu")
    add_bullets_box(
        s,
        0.6,
        1.3,
        12,
        5,
        [
            "L’ART traite des données et processus sensibles (dossiers, plaintes, décisions).",
            "Les agents IA peuvent enchaîner des actions autonomes (outils, APIs, fichiers).",
            "Nouveaux risques : prompt injection, abus d’outils, fuite de données, non-traçabilité.",
            "Le Zero Trust impose : authentifier, autoriser, vérifier en continu, auditer.",
            "La fidélité = conformité des actions de l’agent à sa mission et aux politiques.",
        ],
        18,
    )
    slides_meta.append(s)

    # 3 problematique
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "2. Problématique")
    shape = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(1), PInches(2.5), PInches(11.3), PInches(2.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = TEAL
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = (
        "Comment concevoir et démontrer une architecture Zero Trust capable de garantir "
        "la fidélité des actions d’un agent IA dans un cas d’usage réaliste de l’ART ?"
    )
    p.font.size = PPt(22)
    p.font.color.rgb = NAVY
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER
    tf.margin_left = PInches(0.4)
    tf.margin_right = PInches(0.4)
    tf.margin_top = PInches(0.5)
    slides_meta.append(s)

    # 4 objectifs
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "3. Objectifs et livrables (réalistes en 2 mois)")
    items = [
        ("Cadre théorique", "État de l’art Zero Trust × sécurité agents"),
        ("Ancrage ART", "1 cas d’usage documentaire réglementaire"),
        ("Conception", "Architecture identité / politiques / audit"),
        ("Preuve", "PoC + ≥ 3 scénarios d’attaque"),
        ("Valorisation", "Mémoire + reco ART + soutenance"),
    ]
    for i, (t, d) in enumerate(items):
        left = 0.5 + (i % 3) * 4.2
        top = 1.4 + (i // 3) * 2.6
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(left), PInches(top), PInches(3.9), PInches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = TEAL
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = t
        p.font.bold = True
        p.font.size = PPt(16)
        p.font.color.rgb = NAVY
        p2 = tf.add_paragraph()
        p2.text = d
        p2.font.size = PPt(14)
        p2.font.color.rgb = DARK
        tf.margin_left = PInches(0.2)
        tf.margin_top = PInches(0.35)
    slides_meta.append(s)

    # 5 perimetre
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "4. Périmètre IN / OUT")
    add_text_box(s, 0.6, 1.2, 5.8, 0.4, "IN SCOPE", 18, True, TEAL)
    add_bullets_box(
        s,
        0.6,
        1.7,
        5.8,
        4.5,
        [
            "État de l’art ciblé",
            "1 cas d’usage ART",
            "Architecture Zero Trust",
            "PoC démontrable",
            "3 scénarios de sécurité",
            "Mémoire + soutenance",
        ],
        16,
    )
    add_text_box(s, 7.0, 1.2, 5.8, 0.4, "OUT OF SCOPE", 18, True, ACCENT)
    add_bullets_box(
        s,
        7.0,
        1.7,
        5.8,
        4.5,
        [
            "Déploiement production SI ART",
            "Entraînement de modèle",
            "Certification formelle",
            "Tous les métiers de l’Agence",
            "Benchmarks à grande échelle",
        ],
        16,
    )
    slides_meta.append(s)

    # 6 planning
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "5. Planning 8 semaines")
    rows = [
        "S1 Cadrage & validation thème",
        "S2 État de l’art + cas ART",
        "S3 Menaces & exigences",
        "S4 Architecture Zero Trust",
        "S5 PoC alpha",
        "S6 Tests d’attaque + PoC beta",
        "S7 Mémoire 80 % + reco ART",
        "S8 Finalisation & SOUTENANCE",
    ]
    for i, r in enumerate(rows):
        y = 1.2 + i * 0.7
        bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(0.6), PInches(y), PInches(12.1), PInches(0.55))
        bar.fill.solid()
        bar.fill.fore_color.rgb = NAVY if i == 7 else WHITE
        bar.line.color.rgb = TEAL
        tf = bar.text_frame
        p = tf.paragraphs[0]
        p.text = r
        p.font.size = PPt(16)
        p.font.bold = i == 7
        p.font.color.rgb = WHITE if i == 7 else NAVY
        p.font.name = "Calibri"
        tf.margin_left = PInches(0.25)
        tf.margin_top = PInches(0.08)
    slides_meta.append(s)

    # 7 interet ART
    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "6. Intérêt pour l’ART & demande de validation")
    add_bullets_box(
        s,
        0.6,
        1.3,
        12,
        3,
        [
            "Anticiper l’encadrement sécurisé des outils d’IA agentique",
            "Disposer d’un cadre de contrôle (politique + audit) réutilisable",
            "Recevoir des recommandations opérationnelles actionnables",
        ],
        18,
    )
    add_text_box(
        s,
        0.6,
        4.5,
        12,
        1.5,
        "Demande : valider (i) l’intitulé, (ii) le cas d’usage unique, "
        "(iii) le périmètre PoC hors production, (iv) le planning 8 semaines.",
        18,
        True,
        NAVY,
    )
    slides_meta.append(s)

    # 8 cloture
    s = blank_slide(prs)
    add_bg(s, NAVY)
    add_text_box(s, 0.8, 2.5, 11.5, 0.6, "Merci — Discussion & validation", 32, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 3.5, 11.5, 0.5, "☐ Validé    ☐ Validé avec réserves    ☐ À retravailler", 18, False, WHITE, PP_ALIGN.CENTER)
    slides_meta.append(s)

    total = len(slides_meta)
    for i, sl in enumerate(slides_meta[1:-1], start=2):
        add_footer(sl, i, total)

    path = PPT / "01_Presentation_defense_theme_encadreur.pptx"
    prs.save(path)
    return path


def build_pptx_plan_travail():
    prs = new_prs()
    slides = []

    s = blank_slide(prs)
    add_bg(s, NAVY)
    add_text_box(s, 0.8, 2.0, 11.5, 0.5, "PLAN DE TRAVAIL — 8 SEMAINES", 18, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 2.7, 11.5, 1.5, "Architecture Zero Trust pour le contrôle\nde fidélité des agents IA", 28, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 4.8, 11.5, 0.4, f"{STAGIAIRE}  •  ART Cameroun", 16, False, WHITE, PP_ALIGN.CENTER)
    slides.append(s)

    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "Vue d’ensemble du planning")
    overview = [
        ("S1", "Cadrage"),
        ("S2", "État de l’art"),
        ("S3", "Exigences"),
        ("S4", "Conception"),
        ("S5", "PoC alpha"),
        ("S6", "Tests"),
        ("S7", "Mémoire"),
        ("S8", "Soutenance"),
    ]
    for i, (k, v) in enumerate(overview):
        left = 0.4 + i * 1.6
        card = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, PInches(left), PInches(2.5), PInches(1.45), PInches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = NAVY if i in (0, 7) else TEAL
        card.line.fill.background()
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = k
        p.font.size = PPt(20)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        p2 = tf.add_paragraph()
        p2.text = v
        p2.font.size = PPt(12)
        p2.font.color.rgb = WHITE
        p2.alignment = PP_ALIGN.CENTER
        tf.margin_top = PInches(0.55)
    add_text_box(s, 0.6, 5.2, 12, 0.5, "2 points d’étape chaque semaine : mardi et vendredi (10–15 min + fiche 1 page)", 16, False, NAVY)
    slides.append(s)

    week_details = [
        ("Semaine 1 — Cadrage", ["Valider le thème reformulé", "Choisir 1 cas d’usage ART", "Note de cadrage + références", "Installer l’environnement"]),
        ("Semaine 2 — État de l’art", ["Rédiger Ch.1 (draft)", "≥ 8 fiches de lecture", "Processus ART as-is", "Cartographier acteurs/données"]),
        ("Semaine 3 — Risques", ["Matrice des actifs", "Analyse de menaces", "Exigences EF/ENF", "Draft chapitre 2"]),
        ("Semaine 4 — Conception", ["Diagrammes architecture", "≥ 5 politiques", "Séquence PEP/PDP", "Draft chapitre 3"]),
        ("Semaine 5 — PoC alpha", ["Identité + jeton agent", "PEP + policy engine", "Journal d’audit", "Chemin heureux démo"]),
        ("Semaine 6 — Tests", ["3 scénarios d’attaque", "PoC beta", "Rapport de tests", "Draft chapitre 5"]),
        ("Semaine 7 — Rédaction", ["Mémoire ~80 %", "Note recommandations ART", "Bibliographie", "Plan diaporama"]),
        ("Semaine 8 — Soutenance", ["Mémoire final", "Diapo + répétitions", "Vidéo plan B", "Soutenance J60"]),
    ]
    for title, items in week_details:
        s = blank_slide(prs)
        add_bg(s)
        add_header_bar(s, title)
        add_bullets_box(s, 0.8, 1.5, 11.5, 5, items, 20)
        slides.append(s)

    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "Ordre oral de soutenance (15 min)")
    add_bullets_box(
        s,
        0.8,
        1.4,
        11.5,
        5,
        [
            "Contexte ART & problématique (2 min)",
            "État de l’art express (2 min)",
            "Architecture Zero Trust proposée (4 min)",
            "Démo PoC (3 min)",
            "Résultats & recommandations (2 min)",
            "Conclusion / perspectives (2 min)",
        ],
        20,
    )
    slides.append(s)

    s = blank_slide(prs)
    add_bg(s, NAVY)
    add_text_box(s, 0.8, 3.0, 11.5, 0.6, "Prêt pour exécution — points d’étape mardi / vendredi", 26, True, WHITE, PP_ALIGN.CENTER)
    slides.append(s)

    total = len(slides)
    for i, sl in enumerate(slides[1:-1], start=2):
        add_footer(sl, i, total)

    path = PPT / "02_Presentation_plan_travail_8_semaines.pptx"
    prs.save(path)
    return path


def build_pptx_point_etape_modele():
    prs = new_prs()
    slides = []

    s = blank_slide(prs)
    add_bg(s, NAVY)
    add_text_box(s, 0.8, 2.2, 11.5, 0.5, "MODÈLE — POINT D’ÉTAPE BIHEBDOMADAIRE", 18, True, WHITE, PP_ALIGN.CENTER)
    add_text_box(s, 0.8, 3.0, 11.5, 1.0, "Semaine __  •  Session A (mardi) / B (vendredi)\nDate __/__/____", 24, True, WHITE, PP_ALIGN.CENTER)
    slides.append(s)

    sections = [
        ("1. Objectif de la période", "Rappeler l’objectif fixé au point précédent"),
        ("2. Travaux réalisés", "Lister concrètement ce qui a été fait"),
        ("3. Livrables produits", "Documents, code, diagrammes, captures"),
        ("4. Écarts vs planning", "Retards, avances, causes"),
        ("5. Blocages / arbitrages", "Décisions attendues de l’encadreur"),
        ("6. Plan jusqu’au prochain point", "Actions datées + indicateurs"),
    ]
    for title, hint in sections:
        s = blank_slide(prs)
        add_bg(s)
        add_header_bar(s, title)
        add_text_box(s, 0.8, 1.4, 11.5, 0.5, hint, 16, False, TEAL)
        # empty lines for filling
        for i in range(5):
            line = s.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                PInches(0.8),
                PInches(2.2 + i * 0.75),
                PInches(11.7),
                PInches(0.08),
            )
            line.fill.solid()
            line.fill.fore_color.rgb = RgbColor(0xC8, 0xD6, 0xE0)
            line.line.fill.background()
        slides.append(s)

    s = blank_slide(prs)
    add_bg(s)
    add_header_bar(s, "7. Indicateurs de suivi")
    add_bullets_box(
        s,
        0.8,
        1.5,
        11.5,
        5,
        [
            "% avancement mémoire : ____ %",
            "% avancement PoC : ____ %",
            "Nombre de scénarios de test prêts : ____ / 3",
            "Nombre de politiques rédigées : ____ / 5",
            "Prochaine échéance critique : ____________________",
        ],
        20,
    )
    slides.append(s)

    total = len(slides)
    for i, sl in enumerate(slides[1:], start=2):
        add_footer(sl, i, total)

    path = PPT / "03_Modele_point_etape_bihebdomadaire.pptx"
    prs.save(path)
    return path


# ---------------------------------------------------------------------------
# Excel
# ---------------------------------------------------------------------------

THIN = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
FILL_HEADER = PatternFill("solid", fgColor="0B3D5C")
FILL_ALT = PatternFill("solid", fgColor="E8F1F8")
FILL_DONE = PatternFill("solid", fgColor="C6EFCE")
FILL_CRIT = PatternFill("solid", fgColor="1F7A8C")
FILL_MILESTONE = PatternFill("solid", fgColor="C45C26")
FONT_WHITE = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
FONT_NORMAL = Font(name="Calibri", size=11)
FONT_BOLD = Font(name="Calibri", bold=True, size=11)


def style_header(ws, row, cols):
    for c in range(1, cols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = FILL_HEADER
        cell.font = FONT_WHITE
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = THIN


def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def build_excel_gantt():
    wb = Workbook()

    # --- Feuille Gantt ---
    ws = wb.active
    ws.title = "Gantt_8_semaines"

    headers = ["ID", "Tâche", "Phase", "Début (sem.)", "Fin (sem.)", "Durée (sem.)", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "% Avancement", "Statut"]
    for col, h in enumerate(headers, 1):
        ws.cell(1, col, h)
    style_header(ws, 1, len(headers))

    tasks = [
        (1, "Validation thème & cas d’usage", "Cadrage", 1, 1, 1, [1, 0, 0, 0, 0, 0, 0, 0]),
        (2, "Note de cadrage", "Cadrage", 1, 1, 1, [1, 0, 0, 0, 0, 0, 0, 0]),
        (3, "État de l’art Zero Trust & agents", "Recherche", 2, 3, 2, [0, 1, 1, 0, 0, 0, 0, 0]),
        (4, "Immersion ART / processus as-is", "Recherche", 2, 3, 2, [0, 1, 1, 0, 0, 0, 0, 0]),
        (5, "Analyse menaces & exigences", "Analyse", 3, 3, 1, [0, 0, 1, 0, 0, 0, 0, 0]),
        (6, "Architecture ZT + politiques", "Conception", 4, 4, 1, [0, 0, 0, 1, 0, 0, 0, 0]),
        (7, "PoC alpha (identité, PEP, audit)", "Prototype", 5, 5, 1, [0, 0, 0, 0, 1, 0, 0, 0]),
        (8, "PoC beta + scénarios d’attaque", "Prototype", 6, 6, 1, [0, 0, 0, 0, 0, 1, 0, 0]),
        (9, "Rapport de tests", "Prototype", 6, 7, 2, [0, 0, 0, 0, 0, 1, 1, 0]),
        (10, "Rédaction continue du mémoire", "Mémoire", 2, 8, 7, [0, 1, 1, 1, 1, 1, 1, 1]),
        (11, "Note recommandations ART", "Mémoire", 7, 7, 1, [0, 0, 0, 0, 0, 0, 1, 0]),
        (12, "Finalisation mémoire + annexes", "Soutenance", 8, 8, 1, [0, 0, 0, 0, 0, 0, 0, 1]),
        (13, "Diaporama & répétitions", "Soutenance", 8, 8, 1, [0, 0, 0, 0, 0, 0, 0, 1]),
        (14, "SOUTENANCE (J60)", "Soutenance", 8, 8, 1, [0, 0, 0, 0, 0, 0, 0, 1]),
    ]

    for r, (tid, name, phase, start, end, dur, bars) in enumerate(tasks, start=2):
        values = [tid, name, phase, start, end, dur] + bars + [0, "À faire"]
        for c, v in enumerate(values, 1):
            cell = ws.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if r % 2 == 0 and c <= 6:
                cell.fill = FILL_ALT
        # color gantt bars
        for i, b in enumerate(bars):
            cell = ws.cell(r, 7 + i)
            cell.alignment = Alignment(horizontal="center")
            if b:
                if tid == 14:
                    cell.fill = FILL_MILESTONE
                    cell.value = "◆"
                    cell.font = Font(name="Calibri", bold=True, color="FFFFFF")
                else:
                    cell.fill = FILL_CRIT
                    cell.value = "█"
                    cell.font = Font(name="Calibri", color="FFFFFF")
            else:
                cell.value = ""

    # Dates estimées
    ws.cell(17, 1, "Date de début (J0)")
    ws.cell(17, 2, START.strftime("%d/%m/%Y"))
    ws.cell(18, 1, "Date de soutenance (J60)")
    ws.cell(18, 2, (START + timedelta(days=59)).strftime("%d/%m/%Y"))
    ws.cell(19, 1, "Légende")
    ws.cell(19, 2, "█ = période d’exécution  |  ◆ = jalon soutenance  |  Mettre à jour la colonne % Avancement chaque point d’étape")

    autosize(ws, [5, 42, 14, 12, 12, 12, 5, 5, 5, 5, 5, 5, 5, 5, 14, 12])
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = "C2"

    # --- Feuille Jalons ---
    ws2 = wb.create_sheet("Jalons")
    headers2 = ["Jalon", "Semaine", "Date cible", "Critère de passage", "Statut", "Visa encadreur"]
    for c, h in enumerate(headers2, 1):
        ws2.cell(1, c, h)
    style_header(ws2, 1, len(headers2))
    milestones = [
        ("M0 — Thème validé", "Fin S1", START + timedelta(days=6), "Encadreur OK sur intitulé + périmètre"),
        ("M1 — Spec besoins", "Fin S3", START + timedelta(days=20), "Exigences Must listées et testables"),
        ("M2 — Conception gelée", "Fin S4", START + timedelta(days=27), "Diagrammes + ≥5 politiques"),
        ("M3 — PoC beta", "Fin S6", START + timedelta(days=41), "3 scénarios démontrables"),
        ("M4 — Draft 80 %", "Fin S7", START + timedelta(days=48), "Corps du mémoire relisible"),
        ("M5 — Soutenance", "J60 S8", START + timedelta(days=59), "Pack complet remis + oral"),
    ]
    for r, (name, sem, d, crit) in enumerate(milestones, start=2):
        row = [name, sem, d.strftime("%d/%m/%Y"), crit, "À faire", ""]
        for c, v in enumerate(row, 1):
            cell = ws2.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws2, [24, 12, 14, 45, 12, 16])

    # --- Feuille Charge ---
    ws3 = wb.create_sheet("Charge_hebdo")
    headers3 = ["Activité", "Heures / semaine (indicatif)"]
    for c, h in enumerate(headers3, 1):
        ws3.cell(1, c, h)
    style_header(ws3, 1, 2)
    charge = [
        ("Recherche / rédaction", 14),
        ("Conception / PoC", 12),
        ("Points d’étape + corrections", 4),
        ("Coordination ART", 3),
        ("TOTAL", 33),
    ]
    for r, (a, h) in enumerate(charge, start=2):
        ws3.cell(r, 1, a).font = FONT_BOLD if a == "TOTAL" else FONT_NORMAL
        ws3.cell(r, 2, h).font = FONT_BOLD if a == "TOTAL" else FONT_NORMAL
        for c in range(1, 3):
            ws3.cell(r, c).border = THIN
    autosize(ws3, [40, 28])

    chart = BarChart()
    chart.type = "col"
    chart.title = "Charge indicative (heures/semaine)"
    data = Reference(ws3, min_col=2, min_row=1, max_row=5)
    cats = Reference(ws3, min_col=1, min_row=2, max_row=5)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    chart.y_axis.title = "Heures"
    ws3.add_chart(chart, "D2")

    path = XLS / "01_Diagramme_Gantt_8_semaines.xlsx"
    wb.save(path)
    return path


def build_excel_livrables():
    wb = Workbook()
    ws = wb.active
    ws.title = "Suivi_livrables"

    headers = ["Code", "Livrable", "Description", "Échéance", "Priorité", "%", "Statut", "Lien / fichier", "Commentaire"]
    for c, h in enumerate(headers, 1):
        ws.cell(1, c, h)
    style_header(ws, 1, len(headers))

    rows = [
        ("L1", "Note de cadrage", "Thème, problématique, cas d’usage, planning", "S1", "Must", 0, "À faire"),
        ("L2", "État de l’art", "Zero Trust + menaces agents IA", "S2", "Must", 0, "À faire"),
        ("L3", "Analyse besoins ART", "Processus, menaces, exigences", "S3", "Must", 0, "À faire"),
        ("L4", "Architecture cible", "Diagrammes + politiques", "S4", "Must", 0, "À faire"),
        ("L5", "Prototype PoC", "Code + README + démo", "S6", "Must", 0, "À faire"),
        ("L6", "Rapport de tests", "≥ 3 scénarios + résultats", "S6-S7", "Must", 0, "À faire"),
        ("L7", "Mémoire complet", "Document structuré 40–60 p.", "S8", "Must", 0, "À faire"),
        ("L8", "Recommandations ART", "Note 2–4 pages", "S7", "Must", 0, "À faire"),
        ("L9", "Soutenance", "Diapo + démo orale", "J60", "Must", 0, "À faire"),
    ]
    for r, row in enumerate(rows, start=2):
        for c, v in enumerate(list(row) + ["", ""], 1):
            cell = ws.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws, [8, 22, 42, 10, 10, 6, 12, 20, 20])
    ws.freeze_panes = "A2"

    # Exigences
    ws2 = wb.create_sheet("Exigences_PoC")
    headers2 = ["ID", "Exigence", "Type", "Priorité", "Critère d’acceptation", "Statut test"]
    for c, h in enumerate(headers2, 1):
        ws2.cell(1, c, h)
    style_header(ws2, 1, len(headers2))
    reqs = [
        ("EF-01", "Authentifier l’agent via identité/jeton", "Fonctionnelle", "Must", "Jeton valide requis avant action", "Non testé"),
        ("EF-02", "Intercepter chaque demande d’outil", "Fonctionnelle", "Must", "Aucun outil sans passage PEP", "Non testé"),
        ("EF-03", "Autoriser/refuser selon politique", "Fonctionnelle", "Must", "Décision explicite allow/deny", "Non testé"),
        ("EF-04", "Journaliser décisions et actions", "Fonctionnelle", "Must", "Log JSON pour 100% des appels", "Non testé"),
        ("EF-05", "≥ 3 scénarios d’attaque", "Fonctionnelle", "Must", "3 scripts + preuves", "Non testé"),
        ("EF-06", "Dashboard audit simple", "Fonctionnelle", "Should", "Liste des événements visible", "Non testé"),
        ("ENF-01", "PoC reproductible localement", "Non fonctionnelle", "Must", "README + scripts OK", "Non testé"),
        ("ENF-05", "Données de démo anonymisées/fictives", "Non fonctionnelle", "Must", "Aucune donnée réelle sensible", "Non testé"),
    ]
    for r, row in enumerate(reqs, start=2):
        for c, v in enumerate(row, 1):
            cell = ws2.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws2, [8, 40, 16, 10, 35, 12])

    path = XLS / "02_Suivi_livrables_et_exigences.xlsx"
    wb.save(path)
    return path


def build_excel_points_etape():
    wb = Workbook()
    ws = wb.active
    ws.title = "Planning_points_etape"

    headers = [
        "Semaine",
        "Session",
        "Jour",
        "Date cible",
        "Objectif du point",
        "Livrable à présenter",
        "Fait (O/N)",
        "Note encadreur",
        "Actions suivantes",
    ]
    for c, h in enumerate(headers, 1):
        ws.cell(1, c, h)
    style_header(ws, 1, len(headers))

    plan = [
        (1, "A", "Mardi", "Thème reformulé + cas d’usage possibles", "Brouillon note de cadrage"),
        (1, "B", "Vendredi", "Thème validé + planning", "Note de cadrage v1"),
        (2, "A", "Mardi", "Schéma agent IA + Zero Trust", "5–8 slides + 2 fiches lecture"),
        (2, "B", "Vendredi", "Processus ART + exigences", "Draft Ch.1 + fiche processus"),
        (3, "A", "Mardi", "Top 5 menaces", "Tableau menaces"),
        (3, "B", "Vendredi", "Exigences Must/Should", "Spec besoins & risques v1"),
        (4, "A", "Mardi", "Architecture logique", "Schémas v1"),
        (4, "B", "Vendredi", "Séquence + 5 politiques", "Dossier conception v1"),
        (5, "A", "Mardi", "Démo partielle", "Repo + README draft"),
        (5, "B", "Vendredi", "Démo alpha + audit", "PoC alpha + captures"),
        (6, "A", "Mardi", "Attaques #1 et #2", "Scripts + logs"),
        (6, "B", "Vendredi", "3 scénarios + interprétation", "Rapport tests v1 + PoC beta"),
        (7, "A", "Mardi", "Avancement mémoire", "Draft PDF partiel"),
        (7, "B", "Vendredi", "Reco ART + plan diapo", "Draft 80 % + note ART"),
        (8, "A", "Mardi", "Diapo v1 + checklist", "Slides + mémoire quasi-final"),
        (8, "B", "Vendredi", "Répétition générale", "Pack soutenance complet"),
    ]

    for r, (sem, sess, jour, obj, liv) in enumerate(plan, start=2):
        # Approximate dates: week start + 1 for Tuesday, +4 for Friday
        week_start = START + timedelta(days=(sem - 1) * 7)
        day_offset = 1 if jour == "Mardi" else 4
        d = week_start + timedelta(days=day_offset)
        row = [sem, sess, jour, d.strftime("%d/%m/%Y"), obj, liv, "", "", ""]
        for c, v in enumerate(row, 1):
            cell = ws.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws, [10, 10, 10, 12, 40, 35, 10, 20, 25])
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 30

    # Fiche type
    ws2 = wb.create_sheet("Fiche_type")
    ws2["A1"] = "FICHE POINT D’ÉTAPE"
    ws2["A1"].font = Font(name="Calibri", bold=True, size=16, color="0B3D5C")
    fields = [
        "Semaine / Session / Date",
        "1. Objectif de la période",
        "2. Travaux réalisés",
        "3. Livrables produits",
        "4. Écarts vs planning",
        "5. Blocages / besoins d’arbitrage",
        "6. Plan jusqu’au prochain point",
        "7. Indicateurs (% mémoire, % PoC, nb scénarios)",
        "Visa encadreur",
    ]
    for i, f in enumerate(fields, start=3):
        ws2.cell(i, 1, f).font = FONT_BOLD
        ws2.cell(i, 2, "").border = THIN
        ws2.merge_cells(start_row=i, start_column=2, end_row=i, end_column=4)
        ws2.row_dimensions[i].height = 35
    autosize(ws2, [45, 30, 20, 20])

    path = XLS / "03_Planning_points_etape.xlsx"
    wb.save(path)
    return path


def build_excel_architecture():
    """Diagrammes / matrices d'architecture en Excel."""
    wb = Workbook()

    # Composants
    ws = wb.active
    ws.title = "Composants_architecture"
    headers = ["Composant", "Rôle Zero Trust", "Entrées", "Sorties", "Priorité PoC"]
    for c, h in enumerate(headers, 1):
        ws.cell(1, c, h)
    style_header(ws, 1, len(headers))
    comps = [
        ("Agent IA", "Sujet à contrôler (jamais de confiance implicite)", "Prompt / objectif utilisateur", "Demandes d’outils", "Must"),
        ("Identity Service", "Authentifier l’agent (jeton, scopes)", "Credentials agent", "JWT / API key", "Must"),
        ("Tool Gateway (PEP)", "Point d’application des politiques", "Demande d’outil + jeton", "Allow/Deny + exécution", "Must"),
        ("Policy Engine (PDP)", "Décision d’autorisation", "Requête + politiques", "Décision allow/deny", "Must"),
        ("Policy Store", "Stockage des règles de fidélité", "YAML/JSON règles", "Politiques versionnées", "Must"),
        ("Audit / Telemetry", "Traçabilité continue", "Événements décision/action", "Logs JSON / dashboard", "Must"),
        ("Tool Adapters", "Exécution contrôlée des outils", "Appel autorisé", "Résultat métier", "Must"),
        ("LLM Provider", "Raisonnement (non digne de confiance seul)", "Prompt enrichi", "Plan / texte", "Should"),
        ("Dashboard Audit", "Visibilité pour l’opérateur ART", "Logs", "Vue événements", "Should"),
    ]
    for r, row in enumerate(comps, start=2):
        for c, v in enumerate(row, 1):
            cell = ws.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws, [22, 40, 28, 28, 12])
    for r in range(2, 11):
        ws.row_dimensions[r].height = 35

    # Flux séquence
    ws2 = wb.create_sheet("Flux_sequence_action")
    headers2 = ["Étape", "Acteur", "Action", "Contrôle Zero Trust", "Résultat attendu"]
    for c, h in enumerate(headers2, 1):
        ws2.cell(1, c, h)
    style_header(ws2, 1, len(headers2))
    steps = [
        (1, "Utilisateur", "Soumet une demande", "Authentification utilisateur (contexte)", "Session ouverte"),
        (2, "Agent IA", "Planifie un appel d’outil", "Aucune exécution directe", "Demande outillée formulée"),
        (3, "Identity", "Vérifie / renouvelle jeton agent", "Identité + scopes valides", "Jeton accepté ou rejeté"),
        (4, "PEP (Gateway)", "Intercepte la demande d’outil", "Mandatory enforcement point", "Requête transmise au PDP"),
        (5, "PDP (Policy)", "Évalue les politiques de fidélité", "Least privilege + contexte", "Allow ou Deny"),
        (6, "Audit", "Journalise la décision", "Traçabilité complète", "Événement stocké"),
        ("7a", "Tool Adapter", "Si Allow : exécute l’outil", "Périmètre strict", "Résultat retourné"),
        ("7b", "PEP", "Si Deny : bloque", "Fail closed", "Erreur contrôlée + log"),
        (8, "Agent / UI", "Restitue le résultat", "Pas d’escalade silencieuse", "Réponse utilisateur"),
    ]
    for r, row in enumerate(steps, start=2):
        for c, v in enumerate(row, 1):
            cell = ws2.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            if "Deny" in str(row[2]) or row[0] == "7b":
                cell.fill = PatternFill("solid", fgColor="FCE4D6")
            elif r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws2, [8, 16, 32, 30, 28])

    # Matrice menaces
    ws3 = wb.create_sheet("Matrice_menaces_controles")
    headers3 = ["ID", "Menace", "Exemple agentique", "Impact ART", "Contrôle Zero Trust", "Couvert PoC"]
    for c, h in enumerate(headers3, 1):
        ws3.cell(1, c, h)
    style_header(ws3, 1, len(headers3))
    threats = [
        ("T1", "Prompt injection", "Consigne malveillante dans un document", "Élevé", "Politique d’outils + validation sortie", "Oui"),
        ("T2", "Abus d’outil", "Appel API non autorisée", "Élevé", "PEP + least privilege", "Oui"),
        ("T3", "Exfiltration", "Export hors périmètre", "Critique", "Deny export + audit", "Oui"),
        ("T4", "Usurpation d’identité agent", "Jeton volé / spoof", "Élevé", "AuthN forte + expiration jeton", "Partiel"),
        ("T5", "Non-traçabilité", "Action sans log", "Élevé", "Telemetry obligatoire", "Oui"),
        ("T6", "Escalade de privilèges", "Passage rôle lecture → écriture", "Élevé", "Scopes figés + PDP", "Oui"),
    ]
    for r, row in enumerate(threats, start=2):
        for c, v in enumerate(row, 1):
            cell = ws3.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            if r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws3, [6, 22, 32, 12, 32, 12])

    # Politiques exemples
    ws4 = wb.create_sheet("Politiques_fidelite")
    headers4 = ["ID règle", "Sujet", "Action", "Ressource", "Condition", "Effet", "Priorité"]
    for c, h in enumerate(headers4, 1):
        ws4.cell(1, c, h)
    style_header(ws4, 1, len(headers4))
    policies = [
        ("P1", "agent:doc-assistant", "read", "docs:reglementaires", "classification <= interne", "ALLOW", 10),
        ("P2", "agent:doc-assistant", "summarize", "docs:reglementaires", "jeton valide", "ALLOW", 10),
        ("P3", "agent:doc-assistant", "export", "docs:*", "destination != audit-store", "DENY", 100),
        ("P4", "agent:doc-assistant", "call", "api:externe", "toujours", "DENY", 100),
        ("P5", "agent:doc-assistant", "write", "docs:brouillons", "role == redacteur", "ALLOW", 20),
        ("P6", "agent:*", "*", "*", "jeton expiré", "DENY", 1000),
    ]
    for r, row in enumerate(policies, start=2):
        for c, v in enumerate(row, 1):
            cell = ws4.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            if row[5] == "DENY":
                cell.fill = PatternFill("solid", fgColor="FCE4D6")
            elif r % 2 == 0:
                cell.fill = FILL_ALT
    autosize(ws4, [10, 22, 12, 22, 28, 10, 10])

    # RACI simplifié
    ws5 = wb.create_sheet("RACI_projet")
    headers5 = ["Activité", "Stagiaire", "Encadreur ART", "Encadreur académique"]
    for c, h in enumerate(headers5, 1):
        ws5.cell(1, c, h)
    style_header(ws5, 1, len(headers5))
    raci = [
        ("Validation du thème", "R", "A", "C"),
        ("Choix cas d’usage", "R", "A", "C"),
        ("État de l’art", "R", "C", "A"),
        ("Conception architecture", "R", "C", "A"),
        ("Développement PoC", "R", "I", "C"),
        ("Tests de sécurité", "R", "C", "C"),
        ("Rédaction mémoire", "R", "C", "A"),
        ("Recommandations ART", "R", "A", "C"),
        ("Soutenance", "R", "C", "A"),
    ]
    for r, row in enumerate(raci, start=2):
        for c, v in enumerate(row, 1):
            cell = ws5.cell(r, c, v)
            cell.font = FONT_NORMAL
            cell.border = THIN
            cell.alignment = Alignment(horizontal="center" if c > 1 else "left")
            if r % 2 == 0:
                cell.fill = FILL_ALT
    ws5.cell(12, 1, "R = Responsible, A = Accountable, C = Consulted, I = Informed")
    autosize(ws5, [30, 14, 16, 20])

    path = XLS / "04_Diagrammes_architecture_Zero_Trust.xlsx"
    wb.save(path)
    return path


def main():
    outputs = []
    print("Génération Word...")
    outputs.append(build_word_synthese())
    outputs.append(build_word_note_defense())
    outputs.append(build_word_theme())
    outputs.append(build_word_cdc())
    outputs.append(build_word_structure_memoire())
    outputs.append(build_word_plan_hebdo())

    print("Génération PowerPoint...")
    outputs.append(build_pptx_defense_theme())
    outputs.append(build_pptx_plan_travail())
    outputs.append(build_pptx_point_etape_modele())

    print("Génération Excel...")
    outputs.append(build_excel_gantt())
    outputs.append(build_excel_livrables())
    outputs.append(build_excel_points_etape())
    outputs.append(build_excel_architecture())

    print("\nFichiers générés :")
    for p in outputs:
        print(f"  - {p} ({p.stat().st_size} octets)")
    return outputs


if __name__ == "__main__":
    main()
