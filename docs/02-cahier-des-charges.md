# 2. Cahier des charges — Livrables du projet

## 2.1 Identification du projet

| Élément | Contenu |
|---------|---------|
| Intitulé | Proposition d’une architecture Zero Trust pour le contrôle de fidélité des agents IA — cadre et prototype pour l’ART Cameroun |
| Organisme | Agence de Régulation des Télécommunications (ART) |
| Durée | 8 semaines (soutenance J60) |
| Nature | Mémoire de stage + prototype de démonstration (PoC) |

## 2.2 Contexte et problématique

Les agents IA peuvent enchaîner des actions autonomes (lecture de documents, appels d’API, rédaction). Sans contrôles adaptés, ils exposent l’organisation à des risques d’accès non autorisé, de manipulation et de non-traçabilité.

**Problématique centrale :**  
*Comment concevoir et démontrer une architecture Zero Trust capable de garantir la fidélité des actions d’un agent IA dans un contexte métier de l’ART ?*

## 2.3 Objectifs

### Objectif général

Proposer et prototyper une architecture de sécurisation Zero Trust pour le contrôle de fidélité des agents IA, illustrée sur un cas d’usage ART.

### Objectifs spécifiques

1. Synthétiser l’état de l’art Zero Trust et des menaces liées aux IA agentiques.  
2. Analyser les besoins de sécurité d’un processus métier ART choisi.  
3. Concevoir une architecture Zero Trust (identités, politiques, PEP/PDP, audit).  
4. Réaliser un PoC démontrant le blocage d’actions non conformes.  
5. Évaluer le gain de sécurité via des scénarios de test.  
6. Formuler des recommandations pour l’ART.

## 2.4 Exigences fonctionnelles (PoC)

| ID | Exigence | Priorité |
|----|----------|----------|
| EF-01 | Authentifier l’agent via une identité / jeton | Must |
| EF-02 | Intercepter chaque demande d’outil avant exécution | Must |
| EF-03 | Décider autoriser / refuser selon une politique | Must |
| EF-04 | Journaliser toute décision et toute action | Must |
| EF-05 | Simuler au moins 3 scénarios d’attaque | Must |
| EF-06 | Afficher un tableau de bord simple d’audit (liste des événements) | Should |
| EF-07 | Gérer plusieurs rôles d’agent (ex. lecture seule / rédaction) | Should |
| EF-08 | Intégration SI réel ART | Won’t (hors délai) |

## 2.5 Exigences non fonctionnelles

| ID | Exigence | Priorité |
|----|----------|----------|
| ENF-01 | PoC reproductible localement (README + scripts) | Must |
| ENF-02 | Temps de décision politique < 1 s dans le PoC | Should |
| ENF-03 | Code commenté et structuré | Must |
| ENF-04 | Documentation d’architecture à jour | Must |
| ENF-05 | Données de démo anonymisées / fictives | Must |

## 2.6 Stack technique suggérée (adaptable)

Choisir une stack **simple** et maîtrisable :

- **Langage :** Python  
- **Orchestration agent :** LangChain / LlamaIndex / script custom minimal  
- **Politiques :** règles YAML/JSON + moteur simple (ou OPA/Rego si déjà connu)  
- **Identité :** JWT / API key signée pour l’agent  
- **Audit :** logs JSON + petite UI (Streamlit ou FastAPI + page HTML)  
- **LLM :** API cloud ou modèle local selon accès réseau ART  

> Si l’accès à un LLM est limité à l’ART, prévoir un **mode mock** (réponses simulées) pour que la démo des contrôles Zero Trust reste possible.

## 2.7 Livrables détaillés

### L1 — Note de cadrage (Semaine 1)
- Thème validé, problématique, hypothèses, cas d’usage ART, planning.

### L2 — État de l’art synthétique (Semaines 1–2)
- 10–15 pages max dans le mémoire : Zero Trust (NIST SP 800-207), menaces agents IA, travaux connexes, positionnement.

### L3 — Analyse de l’existant / besoins ART (Semaine 2–3)
- Description du processus choisi, actifs, menaces, exigences de sécurité, contraintes organisationnelles.

### L4 — Architecture cible (Semaine 3–4)
- Diagrammes (contexte, composants, séquence d’une action d’outil).  
- Matrice de politiques.  
- Modèle de menaces (STRIDE ou équivalent simplifié).

### L5 — Prototype (Semaines 4–6)
- Code source + README.  
- Jeu de politiques.  
- Scripts de scénarios d’attaque.  
- Capture d’écran / vidéo courte de démo.

### L6 — Rapport de tests & résultats (Semaine 6–7)
- Protocole de test, résultats, limites, interprétation.

### L7 — Mémoire complet (Semaines 5–8, finalisation S8)
- Document structuré selon `03-structure-memoire.md`.

### L8 — Recommandations ART (Semaine 7)
- Note 2–4 pages : feuille de route d’adoption prudente des agents IA.

### L9 — Soutenance (J60)
- Diaporama 15–20 diapos, démo, réponses aux questions.

## 2.8 Critères d’acceptation (checklist soutenance)

- [ ] Thème et problématique clairement énoncés  
- [ ] Lien explicite avec la mission de l’ART  
- [ ] Architecture Zero Trust cohérente et argumentée  
- [ ] PoC démontrant au moins un refus d’action non autorisée  
- [ ] Journal d’audit visible  
- [ ] ≥ 3 scénarios de sécurité documentés  
- [ ] Limites et perspectives honnêtes  
- [ ] Mémoire remis dans les délais académiques  

## 2.9 Risques projet et mitigation

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Accès limité aux données ART | Moyen | Données fictives réalistes |
| Pas d’accès LLM | Élevé | Mode mock + focus contrôles |
| Sujet trop large | Élevé | Cas d’usage unique + OUT OF SCOPE |
| Retard mémoire | Élevé | Rédaction continue dès S2 |
| Changement d’orientation encadreur | Moyen | Validation écrite S1 |

## 2.10 Hypothèses

1. Un cas d’usage ART peut être validé en semaine 1.  
2. Le PoC peut tourner hors production.  
3. Les données utilisées pour la démo sont fictives ou anonymisées.  
4. L’évaluation est qualitative + indicateurs simples (pas une étude statistique lourde).
