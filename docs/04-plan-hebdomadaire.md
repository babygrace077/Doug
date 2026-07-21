# 4. Plan détaillé — 8 semaines + points d’étape (2× / semaine)

**Calendrier de référence :** Semaine 1 = démarrage immédiat ; **Soutenance = dernier jour de la Semaine 8 (J60).**  
**Rythme de reporting :** **2 points d’étape par semaine** (idéalement **mardi** et **vendredi**), 10–15 min + 1 fiche d’1 page.

Légende des attendus :
- **Faire** = travail de production  
- **Livrer** = artefact à montrer  
- **Présenter** = contenu du point d’étape  

---

## Vue d’ensemble des 8 semaines

| Semaine | Focus principal | Livrable clé |
|--------:|-----------------|--------------|
| S1 | Cadrage & validation du thème | Note de cadrage |
| S2 | État de l’art + cas d’usage ART | Synthèse bibliographique v1 |
| S3 | Analyse des risques & exigences | Spec besoins + menaces |
| S4 | Architecture Zero Trust | Dossier conception v1 |
| S5 | Développement PoC (cœur) | PoC alpha |
| S6 | Scénarios d’attaque & durcissement | PoC beta + tests |
| S7 | Mémoire (corps) + recommandations | Draft mémoire 80 % |
| S8 | Finalisation, diapo, répétition, soutenance | Mémoire + soutenance |

---

## SEMAINE 1 — Cadrage (fondations)

### Objectif
Obtenir la **validation écrite/orale** du thème reformulé et figer le cas d’usage.

### Travaux à faire
1. Relire missions ART et identifier 2–3 processus candidats.  
2. Choisir **1 seul** cas d’usage (recommandé : assistance documentaire réglementaire).  
3. Rédiger la note de cadrage (problématique, objectifs, périmètre IN/OUT, planning).  
4. Lister 15–20 références prioritaires (NIST, OWASP LLM, articles agents).  
5. Installer l’environnement de travail (Python, Git, éditeur).

### Ce qu’on attend de vous
- Un thème **défendable** et **borné**.  
- Une compréhension claire de Zero Trust vs « antivirus / firewall ».  
- Un engagement sur le PoC (pas seulement théorique).

### Point d’étape 1A — Mardi S1
**Présenter :**
- Thème reformulé (1 slide)  
- 2–3 cas d’usage possibles + choix provisoire  
- Risques projet  

**Livrable joint :** brouillon de note de cadrage (1–2 pages).

### Point d’étape 1B — Vendredi S1
**Présenter :**
- Thème validé / ajusté après retours  
- Cas d’usage définitif  
- Planning 8 semaines  

**Livrable joint :** `Note de cadrage v1` + liste de références.

---

## SEMAINE 2 — État de l’art & immersion ART

### Objectif
Maîtriser le socle théorique et ancrer le sujet dans le réel de l’ART.

### Travaux à faire
1. Rédiger Ch.1 (sections 1.1 à 1.3) en draft.  
2. Fiches de lecture (minimum 8 sources).  
3. Entretiens / observations (même courts) au service d’accueil.  
4. Décrire le processus métier « as-is » du cas d’usage.  
5. Cartographier données / acteurs / outils.

### Ce qu’on attend de vous
- Synthèse **critique** (avantages/limites des approches).  
- Preuve que vous comprenez les menaces agentiques.  
- Première description crédible du cas ART.

### Point d’étape 2A — Mardi S2
**Présenter :**
- Schéma « agent IA » et principaux risques  
- Principes Zero Trust (5 piliers max)  

**Livrable :** 5–8 slides + 2 fiches de lecture.

### Point d’étape 2B — Vendredi S2
**Présenter :**
- Processus ART retenu (as-is)  
- Première liste d’exigences de sécurité  

**Livrable :** draft Ch.1 (partiel) + fiche processus (1–2 pages).

---

## SEMAINE 3 — Analyse des risques & exigences

### Objectif
Transformer le besoin ART en **exigences de sécurité testables**.

### Travaux à faire
1. Matrice des actifs (documents, APIs, identités).  
2. Analyse de menaces (STRIDE simplifié ou liste structurée).  
3. Exigences EF/ENF du cahier des charges affinées.  
4. Rédiger Ch.2 (draft).  
5. Définir les indicateurs de succès du PoC.

### Ce qu’on attend de vous
- Une analyse qui justifie **pourquoi** Zero Trust.  
- Des exigences traçables (ID → test).  
- Pas de solution technique trop tôt sans exigences.

### Point d’étape 3A — Mardi S3
**Présenter :**
- Top 5 menaces du cas d’usage  
- Impacts pour l’ART  

**Livrable :** tableau menaces (Excel/Markdown).

### Point d’étape 3B — Vendredi S3
**Présenter :**
- Exigences Must/Should  
- Périmètre PoC figé  

**Livrable :** `Spécification besoins & risques v1` + draft Ch.2.

---

## SEMAINE 4 — Conception architecture Zero Trust

### Objectif
Livrer une architecture **claire, diagrammable et implémentable**.

### Travaux à faire
1. Diagramme de contexte + diagramme de composants.  
2. Diagramme de séquence (appel d’outil sous contrôle).  
3. Modèle d’identité agent + scopes.  
4. Rédiger **≥ 5 politiques** de fidélité (YAML/JSON).  
5. Choisir et justifier la stack technique.  
6. Rédiger Ch.3 (draft 70 %).

### Ce qu’on attend de vous
- Des diagrammes lisibles (pas décoratifs).  
- Une définition opérationnelle de la **fidélité**.  
- Une architecture alignée NIST Zero Trust (même simplifiée).

### Point d’étape 4A — Mardi S4
**Présenter :**
- Architecture logique (1 schéma)  
- Rôle de chaque composant (PEP, PDP, Audit…)  

**Livrable :** schémas v1 (draw.io / diagrams.net / Mermaid).

### Point d’étape 4B — Vendredi S4
**Présenter :**
- Séquence d’autorisation d’une action  
- 5 politiques exemples  
- Plan d’implémentation S5–S6  

**Livrable :** `Dossier conception v1` + draft Ch.3.

---

## SEMAINE 5 — Prototype alpha (cœur Zero Trust)

### Objectif
Avoir un **chemin heureux** : agent authentifié → outil autorisé → audit.

### Travaux à faire
1. Implémenter Identity + émission de jeton agent.  
2. Implémenter Tool Gateway / PEP.  
3. Implémenter Policy Engine minimal.  
4. Brancher 2–3 outils fictifs (lire doc, résumer, exporter).  
5. Journal JSON des décisions.  
6. README d’installation.  
7. Commencer Ch.4 (environnement + premiers composants).

### Ce qu’on attend de vous
- Un PoC qui **tourne** (même rustique).  
- Preuve d’interception **avant** l’outil.  
- Logs consultables.

### Point d’étape 5A — Mardi S5
**Présenter :**
- Démo partielle : authentification + 1 outil autorisé  
- Structure du code  

**Livrable :** repo Git + README draft.

### Point d’étape 5B — Vendredi S5
**Présenter :**
- Démo alpha complète du chemin heureux  
- Exemple de log d’audit  

**Livrable :** `PoC alpha` + captures d’écran.

---

## SEMAINE 6 — Tests d’attaque, durcissement, PoC beta

### Objectif
Montrer que l’architecture **augmente** la sécurité (fidélité) de façon démontrable.

### Travaux à faire
1. Implémenter refus d’outil non autorisé.  
2. Scénario exfiltration / export hors politique.  
3. (Bonus) Tentative de prompt injection.  
4. Tableau de résultats (autorisé/refusé).  
5. Corriger les failles évidentes du PoC.  
6. Rédiger Ch.5 (protocole + résultats partiels).  
7. Mini dashboard d’audit (Should).

### Ce qu’on attend de vous
- ≥ 3 scénarios documentés avec preuves.  
- Comparaison qualitative « sans ZT » vs « avec ZT ».  
- Limites assumées.

### Point d’étape 6A — Mardi S6
**Présenter :**
- Scénario d’attaque #1 et #2 en live  
- Matrice résultats provisoire  

**Livrable :** scripts de test + logs.

### Point d’étape 6B — Vendredi S6
**Présenter :**
- PoC beta + 3 scénarios  
- Première interprétation des résultats  

**Livrable :** `Rapport de tests v1` + PoC beta.

---

## SEMAINE 7 — Rédaction lourde & recommandations ART

### Objectif
Disposer d’un **draft mémoire à ~80 %** et d’une note utile pour l’Agence.

### Travaux à faire
1. Consolider Intro + Ch.1 à Ch.5.  
2. Harmoniser figures, numérotation, glossaire.  
3. Rédiger la **Note de recommandations ART** (2–4 pages).  
4. Compléter bibliographie.  
5. Préparer plan du diaporama de soutenance.  
6. Relire avec checklist qualité (orthographe, citations, cohérence).

### Ce qu’on attend de vous
- Un mémoire déjà « soutenable » même s’il manque la polish.  
- Des recommandations réalistes (pas « déployer ChatGPT partout »).  
- Traçabilité exigences → conception → tests.

### Point d’étape 7A — Mardi S7
**Présenter :**
- Table des matières définitive + avancement % par chapitre  
- Points bloquants rédactionnels  

**Livrable :** draft mémoire (PDF) partiel.

### Point d’étape 7B — Vendredi S7
**Présenter :**
- Recommandations ART (lecture commentée)  
- Plan de soutenance (structure diapo)  

**Livrable :** `Draft mémoire ~80 %` + note recommandations v1.

---

## SEMAINE 8 — Finalisation, répétition, soutenance (J60)

### Objectif
Livrer un pack soutenance professionnel et convaincant.

### Travaux à faire (jour par jour suggéré)

| Jour | Activité |
|-----:|----------|
| Lun | Finaliser figures, annexes, résumé/abstract |
| Mar | Mémoire version quasi-finale + relecture encadreur |
| Mer | Diaporama complet + script oral (12–15 min) |
| Jeu | Répétition soutenance + démo chronométrée |
| Ven | Corrections de dernière minute |
| **Dernier jour** | **Soutenance officielle** |

### Ce qu’on attend de vous
- Maîtrise orale du discours (problème → architecture → preuve).  
- Démo stable (prévoir plan B vidéo).  
- Réponses préparées sur limites et perspectives.

### Point d’étape 8A — Mardi S8
**Présenter :**
- Diapo v1 + timing  
- Checklist des livrables  

**Livrable :** slides v1 + mémoire quasi-final.

### Point d’étape 8B — Vendredi S8 (avant-dernier jour utile)
**Présenter :**
- Répétition générale devant encadreur  
- Démo finale  

**Livrable :** pack soutenance (mémoire PDF, slides, PoC, note ART).

### Jour J — Soutenance
**Ordre oral recommandé (15 min) :**
1. Contexte ART & problématique (2 min)  
2. État de l’art express (2 min)  
3. Architecture Zero Trust proposée (4 min)  
4. Démo PoC (3 min)  
5. Résultats & recommandations (2 min)  
6. Conclusion / perspectives (2 min)  

---

## Modèle de fiche de point d’étape (à dupliquer 16 fois)

```text
FICHE POINT D’ÉTAPE — Semaine __ / Session A|B — Date __/__/__
1. Objectif de la période :
2. Travaux réalisés (faits) :
3. Livrables produits :
4. Écarts vs planning :
5. Blocages / besoins d’arbitrage :
6. Plan jusqu’au prochain point :
7. Indicateurs (ex. % mémoire, % PoC, nb scénarios) :
```

---

## Charge de travail indicative (par semaine)

| Activité | Heures / semaine (indicatif) |
|----------|-------------------------------:|
| Recherche / rédaction | 12–16 h |
| Conception / PoC | 10–14 h |
| Points d’étape + corrections | 3–4 h |
| Coordination ART | 2–3 h |
| **Total** | **~30–35 h** |

> Si votre stage impose une présence bureau, réservez les créneaux « deep work » (PoC + rédaction) en blocs de 2–3 h non fragmentés.
