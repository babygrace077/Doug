# Livrables Office — Architecture Zero Trust IA (ART Cameroun)

Fichiers prêts à ouvrir dans **Microsoft Word**, **PowerPoint** et **Excel**.

## Word (`.docx`)

| Fichier | Usage |
|---------|--------|
| `word/00_Synthese_projet.docx` | Vue d’ensemble du projet |
| `word/01_Note_defense_theme_encadreur.docx` | **Note d’1 page** à faire valider par l’encadreur |
| `word/02_Theme_reformule.docx` | Thème, concepts, périmètre IN/OUT |
| `word/03_Cahier_des_charges.docx` | Cahier des charges & livrables |
| `word/04_Structure_memoire.docx` | Plan détaillé du mémoire |
| `word/05_Plan_hebdomadaire.docx` | Plan des 8 semaines + points d’étape |

## PowerPoint (`.pptx`)

| Fichier | Usage |
|---------|--------|
| `powerpoint/01_Presentation_defense_theme_encadreur.pptx` | Présentation de défense du thème (encadreur) |
| `powerpoint/02_Presentation_plan_travail_8_semaines.pptx` | Présentation du plan de travail |
| `powerpoint/03_Modele_point_etape_bihebdomadaire.pptx` | Modèle réutilisable pour les points mardi/vendredi |

## Excel (`.xlsx`)

| Fichier | Feuilles / contenu |
|---------|---------------------|
| `excel/01_Diagramme_Gantt_8_semaines.xlsx` | Gantt S1–S8, jalons, charge hebdo + graphique |
| `excel/02_Suivi_livrables_et_exigences.xlsx` | Suivi livrables L1–L9 + exigences PoC |
| `excel/03_Planning_points_etape.xlsx` | 16 points d’étape datés + fiche type |
| `excel/04_Diagrammes_architecture_Zero_Trust.xlsx` | Composants, flux séquence, menaces, politiques, RACI |

## Archive

`TOUS_LES_LIVRABLES_OFFICE.zip` — tous les fichiers ci-dessus.

## Régénération

```bash
python3 scripts/generate_office_deliverables.py
```
