# 3. Structure détaillée du mémoire

> Structure type d’un mémoire de stage d’ingénierie / master au Cameroun, **adaptée** au thème Zero Trust / IA agentique / ART.  
> Si votre école impose un canevas officiel différent, conservez les titres institutionnels et réinjectez le contenu ci-dessous dans les chapitres correspondants.

**Volume indicatif :** 40–60 pages (hors annexes), réaliste en 2 mois.

---

## Pages liminaires

1. Page de garde (école, titre, noms, logos ART + établissement, année)  
2. Attestation / page de validation (selon école)  
3. Dédicaces (optionnel)  
4. Remerciements  
5. Résumé (FR) — ½ page  
6. Abstract (EN) — ½ page  
7. Liste des figures / tableaux  
8. Liste des sigles et acronymes (ART, ZTA, PEP, PDP, IAM, LLM, etc.)  
9. Table des matières  

---

## Introduction générale (4–6 pages)

1. Contexte : digitalisation, IA, régulation des télécoms au Cameroun  
2. Constat : émergence des agents IA et nouveaux risques de sécurité  
3. Problématique  
4. Objectifs (général + spécifiques)  
5. Hypothèses de travail  
6. Intérêt du sujet pour l’ART  
7. Méthodologie (analyse → conception → prototypage → tests)  
8. Structure du mémoire (annonce des chapitres)  

**Attendus :** problématique claire, objectifs mesurables, lien ART explicite.

---

## Chapitre 1 — Cadre théorique et état de l’art (10–12 pages)

### 1.1 Les agents IA : concepts et architectures
- Agent, outils (tools), boucle perception–raisonnement–action  
- Différence chatbot vs agent  

### 1.2 Menaces et vulnérabilités des systèmes agentiques
- Prompt injection, tool abuse, data exfiltration, privilege escalation  
- Exemples issus de la littérature / rapports (OWASP LLM Top 10, NIST AI RMF, etc.)  

### 1.3 Le paradigme Zero Trust
- Principes (NIST SP 800-207)  
- Composants : PEP, PDP, identité, politiques, télémétrie  
- Zero Trust vs périmètre traditionnel  

### 1.4 Fidélité des agents et gouvernance
- Définition opérationnelle de la fidélité  
- Lien avec l’alignement, l’auditabilité et la responsabilité  

### 1.5 Travaux connexes et positionnement
- Tableau comparatif (3–6 références / approches)  
- Ce que votre contribution apporte (cadre ART + PoC)  

**Attendus :** synthèse critique (pas une paraphrase), positionnement clair.

---

## Chapitre 2 — Présentation de l’ART et analyse du besoin (8–10 pages)

### 2.1 Présentation de l’Agence (ART)
- Missions, organisation (vue utile au sujet), enjeux numériques  

### 2.2 Contexte du stage et service d’accueil
- Activités observées liées à la donnée / aux processus documentaires  

### 2.3 Cas d’usage retenu
- Description du processus « as-is »  
- Acteurs, données, outils  

### 2.4 Analyse des risques de sécurité liés à un agent IA
- Actifs, menaces, impacts (tableau)  
- Exigences de sécurité dérivées  

### 2.5 Contraintes (organisationnelles, techniques, juridiques)
- Confidentialité, responsabilité, absence de déploiement prod  

**Attendus :** montrer que le sujet n’est pas « hors-sol » ; le cas ART justifie l’architecture.

---

## Chapitre 3 — Conception de l’architecture Zero Trust (10–12 pages)

### 3.1 Objectifs de conception et principes retenus
- Never trust, least privilege, continuous verification, assume breach  

### 3.2 Architecture logique
- Diagramme de composants (Agent, Tool Gateway/PEP, Policy Engine/PDP, Identity, Audit Store, LLM)  

### 3.3 Modèle d’identité et d’authentification des agents
- Identité agent, scopes, durée de vie des jetons  

### 3.4 Modèle de politiques (fidélité)
- Exemples de règles : outils autorisés, volumes, destinations, horaires, classification des docs  

### 3.5 Flux de contrôle d’une action (séquence)
- Diagramme de séquence : requête outil → PEP → PDP → décision → exécution/refus → audit  

### 3.6 Modèle de menaces et contrôles associés
- Table menace → contrôle Zero Trust  

### 3.7 Choix techniques du PoC
- Justification de la stack  

**Attendus :** diagrammes propres, politiques explicites, traçabilité des décisions de conception.

---

## Chapitre 4 — Réalisation du prototype (8–10 pages)

### 4.1 Environnement de développement  
### 4.2 Implémentation des composants  
### 4.3 Jeu de politiques et jeux de données fictifs  
### 4.4 Interfaces (CLI / dashboard audit)  
### 4.5 Difficultés rencontrées et solutions  

**Attendus :** captures d’écran, extraits de code pertinents (pas tout le code dans le corps), README en annexe.

---

## Chapitre 5 — Tests, résultats et discussion (6–8 pages)

### 5.1 Protocole de test  
### 5.2 Scénarios
1. Action légitime autorisée  
2. Outil non autorisé (doit être refusé)  
3. Tentative d’exfiltration / export hors périmètre  
4. (Bonus) Prompt injection visant à contourner la politique  

### 5.3 Résultats (tableaux + captures)  
### 5.4 Interprétation : gain de fidélité / sécurité  
### 5.5 Limites du PoC et validité externe  

**Attendus :** résultats reproductibles ; discussion honnête des limites.

---

## Conclusion générale et perspectives (3–4 pages)

1. Rappel de la problématique et des résultats  
2. Apports (théorique, pratique, pour l’ART)  
3. Limites  
4. Perspectives : industrialisation, gouvernance IA à l’ART, extension multi-agents, conformité  

---

## Bibliographie

Normes et références utiles à citer (indicatif) :
- NIST SP 800-207 (Zero Trust Architecture)  
- NIST AI RMF  
- OWASP Top 10 for LLM Applications  
- ISO/IEC 27001 (principes)  
- Documents / rapports ART (si publics)  
- Articles récents sur la sécurité des agents IA  

Style de citation : celui imposé par l’école (APA, IEEE, etc.).

---

## Annexes

- A. Cahier des charges synthétique  
- B. Diagrammes complémentaires  
- C. Extraits de politiques (YAML/JSON)  
- D. Guide d’exécution du PoC  
- E. Fiches des points d’étape bihebdomadaires  
- F. Note de recommandations ART  

---

## Répartition indicative du volume

| Partie | Pages |
|--------|------:|
| Intro | 5 |
| Ch.1 État de l’art | 11 |
| Ch.2 ART & besoins | 9 |
| Ch.3 Conception | 11 |
| Ch.4 Réalisation | 9 |
| Ch.5 Tests | 7 |
| Conclusion | 3 |
| **Total corps** | **~55** |
