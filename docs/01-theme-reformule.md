# 1. Reformulation du thème

## Thème initial (à reformuler)

Architecture sécurisée basée sur le « Zero Trust Fidelity » pour augmenter le taux de sécurité des IA agentiques.

## Problème de formulation

- « Zero Trust Fidelity » n’est pas un standard reconnu tel quel.
- « Augmenter le taux de sécurité » est trop vague pour être évalué en 2 mois.
- Sans cas d’usage ART, le sujet reste abstrait et difficile à soutenir.

## Thème reformulé (recommandé)

**Proposition d’une architecture Zero Trust pour le contrôle de fidélité des agents IA : cadre de sécurisation et prototype applicables aux processus métier de l’ART Cameroun.**

### Version anglaise (optionnelle, pour résumé)

*A Zero Trust Architecture for Agentic AI Fidelity Control: Security Framework and Prototype for Cameroon’s Telecommunications Regulatory Agency (ART).*

---

## Définition des concepts clés (à maîtriser pour la soutenance)

| Concept | Définition opérationnelle pour ce stage |
|---------|------------------------------------------|
| **IA agentique** | Système IA capable d’enchaîner des actions (outils, APIs, fichiers) pour atteindre un objectif |
| **Zero Trust** | Principe « never trust, always verify » : aucun agent, utilisateur ou service n’est digne de confiance par défaut |
| **Fidélité de l’agent** | Capacité de l’agent à n’exécuter que des actions **autorisées, traçables et conformes** à sa mission (pas de dérive, pas d’abus d’outils, pas d’exfiltration) |
| **Contrôle de fidélité** | Mécanismes qui valident *avant* chaque action : identité de l’agent, politique, contexte, journalisation |

En pratique : **Zero Trust** = le *cadre* ; **Fidélité** = la *propriété de sécurité* que l’on veut garantir pour l’agent.

---

## Pourquoi ce thème est pertinent pour l’ART

L’ART traite des données et processus sensibles (dossiers d’opérateurs, plaintes, décisions, documents réglementaires). L’introduction d’agents IA (assistance documentaire, tri de plaintes, synthèse de rapports) crée de nouveaux risques :

1. **Prompt injection** / manipulation de l’agent  
2. **Abus d’outils** (accès non autorisé à des fichiers ou APIs)  
3. **Fuite de données** réglementaires ou personnelles  
4. **Actions non traçables** (impossibilité d’audit)  
5. **Usurpation d’identité** d’un agent ou d’un service  

Une architecture Zero Trust répond directement à ces risques en imposant : authentification forte des agents, autorisation fine par action, vérification continue, et audit.

---

## Périmètre réalisable en 2 mois (IN SCOPE)

### Ce que vous ferez

1. **État de l’art** ciblé : Zero Trust (NIST), menaces des agents IA, contrôles existants.  
2. **Analyse des besoins ART** : 1 cas d’usage métier (recommandé : *assistant documentaire réglementaire* ou *tri assisté de plaintes*).  
3. **Conception d’architecture** Zero Trust pour agents (composants, flux, politiques).  
4. **Prototype (PoC)** minimal mais démontrable :
   - Identité / jeton d’agent  
   - Point d’application de politiques (PEP) avant chaque appel d’outil  
   - Journal d’audit des actions  
   - Au moins 3 scénarios d’attaque simulés (ex. : injection, outil non autorisé, exfiltration)  
5. **Évaluation** : comparaison « agent sans contrôle » vs « agent sous Zero Trust » sur des indicateurs simples.  
6. **Mémoire + soutenance**.

### Cas d’usage recommandé (simple et crédible pour l’ART)

> **Agent d’assistance à l’analyse documentaire réglementaire**  
> L’agent peut : lire des documents autorisés, résumer, classer, proposer un brouillon.  
> L’agent ne peut pas : écrire hors périmètre, appeler des APIs non listées, exporter des données hors journal.

Ce cas permet de montrer clairement les contrôles Zero Trust sans dépendre d’infrastructures lourdes de l’ART.

---

## Hors périmètre (OUT OF SCOPE) — à assumer clairement

- Déploiement en production sur le SI de l’ART  
- Entraînement d’un modèle de fondation  
- Certification réglementaire formelle  
- Couverture de tous les processus de l’Agence  
- Benchmarks à grande échelle  

Ces exclusions renforcent la crédibilité : le stage livre un **cadre + PoC**, pas un produit industrialisé.

---

## Critères de succès (mesurables)

| Indicateur | Cible à la soutenance |
|------------|------------------------|
| Architecture documentée | Diagrammes + description des composants Zero Trust |
| PoC exécutable | Démo live ou enregistrée ≤ 10 min |
| Politiques | ≥ 5 règles d’autorisation explicites |
| Scénarios de sécurité | ≥ 3 attaques simulées avec résultat (bloqué / non bloqué) |
| Traçabilité | 100 % des actions d’outil journalisées dans le PoC |
| Mémoire | Structure complète, bibliographie, annexes |
| Recommandations ART | Note de 2–4 pages actionnable |

---

## Formulation alternative (si l’encadreur préfère un angle plus « régulation »)

**Cadre Zero Trust pour la gouvernance de la fidélité des agents IA dans le secteur des télécommunications : étude et prototype pour l’ART Cameroun.**

À utiliser si l’encadreur insiste davantage sur la **gouvernance / régulation** que sur le prototype technique.
