#!/usr/bin/env python3
"""Génère schémas vectoriels (matplotlib) et placeholders pour le mémoire ART ZT."""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.patheffects as pe

OUT = Path("/workspace/livrables/memoire/figures")
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    path = OUT / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)
    return path


def placeholder(title, filename, size=(10, 4.5)):
    fig, ax = plt.subplots(figsize=size)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.add_patch(Rectangle((0, 0), 10, 4.5, facecolor="black", edgecolor="black"))
    ax.text(
        5,
        2.25,
        title,
        ha="center",
        va="center",
        color="white",
        fontsize=14,
        fontweight="bold",
        wrap=True,
    )
    ax.axis("off")
    return save(fig, filename)


def fig4_topologie_maquette():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Figure 4. Topologie logique de la maquette", fontsize=12, pad=8)

    # Pare-feu box
    fw = FancyBboxPatch((3.5, 4.6), 4, 0.9, boxstyle="round,pad=0.02,rounding_size=0.08",
                        facecolor="#1f4e79", edgecolor="#0b2e4a", linewidth=1.5)
    ax.add_patch(fw)
    ax.text(5.5, 5.05, "Pare-feu / USG", ha="center", va="center", color="white", fontsize=11, fontweight="bold")

    zones = [
        (0.3, "Utilisateurs\n(postes)", "#d6eaf8"),
        (2.5, "Serveurs\n(DC, membre)", "#d5f5e3"),
        (4.7, "Critique\n(serveur fictif)", "#fadbd8"),
        (6.9, "Invité\n(Wi-Fi)", "#fcf3cf"),
        (9.1, "Administration\n(KSC, Wazuh,\nprivacyIDEA)", "#e8daef"),
    ]
    for x, label, color in zones:
        box = FancyBboxPatch((x, 2.0), 1.9, 1.8, boxstyle="round,pad=0.02,rounding_size=0.06",
                             facecolor=color, edgecolor="#333333", linewidth=1.2)
        ax.add_patch(box)
        ax.text(x + 0.95, 2.9, label, ha="center", va="center", fontsize=8.5)
        # vertical line from firewall
        ax.plot([x + 0.95, x + 0.95], [4.6, 3.8], color="#333333", lw=1.2)
        ax.plot([x + 0.95, 5.5], [3.8, 3.8], color="#333333", lw=1.0)

    # attacker note
    atk = FancyBboxPatch((0.3, 0.35), 10.4, 1.1, boxstyle="round,pad=0.02,rounding_size=0.05",
                         facecolor="#f5f5f5", edgecolor="#666666", linewidth=1)
    ax.add_patch(atk)
    ax.text(
        5.5,
        0.9,
        "Poste attaquant (KALI) : placé tour à tour dans Utilisateurs et dans Invité",
        ha="center",
        va="center",
        fontsize=9.5,
    )
    return save(fig, "figure4_topologie_maquette.png")


def fig6_maturite():
    """Barres de maturité initiale (4 piliers du périmètre)."""
    fig, ax = plt.subplots(figsize=(9, 4.8))
    pillars = ["Identité", "Terminaux", "Réseaux", "Données"]
    # Ordinal: Non évalué=0, Traditionnel=1, Traditionnel+éléments=1.5, Initial=2
    values = [1.0, 1.5, 1.0, 0.0]
    labels = ["Traditionnel", "Traditionnel\n(+ éléments initiaux)", "Traditionnel", "Non évalué"]
    colors = ["#c0392b", "#e67e22", "#c0392b", "#7f8c8d"]
    bars = ax.barh(pillars[::-1], values[::-1], color=colors[::-1], edgecolor="#222222", height=0.55)
    ax.set_xlim(0, 3)
    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["Non évalué", "Traditionnel", "Initial", "Avancé"])
    ax.set_title("Figure 6. Synthèse de maturité Zero Trust initiale", fontsize=12)
    for bar, lab in zip(bars, labels[::-1]):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, lab,
                va="center", fontsize=8)
    ax.set_xlabel("Palier (échelle ordinale)")
    ax.grid(axis="x", linestyle=":", alpha=0.5)
    fig.tight_layout()
    return save(fig, "figure6_maturite_initiale.png")


def fig7_pe_pa_pep():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("Figure 7. Architecture cible PE / PA / PEP", fontsize=12, pad=6)

    def box(x, y, w, h, title, body, fc, ec="#1a1a1a"):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                           facecolor=fc, edgecolor=ec, linewidth=1.4)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h - 0.35, title, ha="center", va="center",
                fontsize=10, fontweight="bold", color="#111111")
        ax.text(x + w / 2, y + h / 2 - 0.15, body, ha="center", va="center", fontsize=8)

    # Subject / Agent side
    box(0.3, 5.2, 2.4, 1.3, "Sujet", "Utilisateur /\nAgent de poste", "#d6eaf8")
    box(0.3, 3.4, 2.4, 1.3, "Ressource", "Docs / APIs /\nServices métier", "#d5f5e3")

    # Control plane
    box(3.5, 5.0, 3.2, 1.6, "PE — Policy Engine", "AD ; MFA (privacyIDEA)\nPolitiques KSC\nDécision", "#fdebd0")
    box(3.5, 3.0, 3.2, 1.6, "PA — Policy Administrator", "USG ; KSC ; RADIUS\nMise en œuvre session", "#fad7a0")

    # Enforcement
    box(7.5, 3.5, 3.2, 2.6, "PEP — Enforcement", "USG ; passerelle ; UniFi\nKES ; GPO\nFiltrage / VLAN / USB", "#f5b7b1")

    # Sources
    box(3.5, 0.6, 7.2, 1.5, "Sources de preuves",
        "Wazuh (cible) ; inventaire ; journaux  |  Preuves (T12, I9)", "#e8daef")

    # Arrows
    ax.annotate("", xy=(3.5, 5.7), xytext=(2.7, 5.7),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.3))
    ax.annotate("", xy=(7.5, 5.0), xytext=(6.7, 5.0),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.3))
    ax.annotate("", xy=(7.5, 4.0), xytext=(6.7, 3.8),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.3))
    ax.annotate("", xy=(5.1, 2.1), xytext=(5.1, 3.0),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.3))

    ax.text(5.5, 6.85,
            "SO3→PE (T2,T5)   |   SO1→PEP réseau (T9,T7)   |   SO5→KSC/KES+USG (T3,T6)",
            ha="center", fontsize=8, color="#333333")
    return save(fig, "figure7_architecture_pe_pa_pep.png")


def fig8_topologie_logique():
    # Variant focused on EVE-NG lab nodes mentioned in text
    fig, ax = plt.subplots(figsize=(11, 5.8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("Figure 8. Topologie logique maquette (lab EVE-NG)", fontsize=12)

    nodes = [
        (5.0, 5.0, 2.6, 0.8, "AR / USG (HA)", "#1f4e79", "white"),
        (1.0, 3.2, 2.2, 0.9, "SW Utilisateurs", "#5dade2", "black"),
        (4.0, 3.2, 2.2, 0.9, "SW Serveurs", "#58d68d", "black"),
        (7.0, 3.2, 2.2, 0.9, "SW Admin", "#af7ac5", "black"),
        (1.0, 1.4, 2.2, 0.9, "VPCS / Postes", "#aed6f1", "black"),
        (4.0, 1.4, 2.2, 0.9, "DC-AD / SRV-FIC", "#abebc6", "black"),
        (7.0, 1.4, 2.2, 0.9, "KSC / KALI", "#d7bde2", "black"),
    ]
    for x, y, w, h, label, fc, tc in nodes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    facecolor=fc, edgecolor="#222", lw=1.2))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", color=tc, fontsize=9, fontweight="bold")

    # links
    for x in [2.1, 5.1, 8.1]:
        ax.plot([5.0 + 1.3, x], [5.0, 4.1], color="#444", lw=1.1)
        ax.plot([x, x], [3.2, 2.3], color="#444", lw=1.1)

    ax.text(5.5, 0.35, "Écarts assumés : AD en Server 2016 ; postes clients Windows absents ; privacyIDEA/Wazuh/KSC de test spécifiés",
            ha="center", fontsize=8, color="#444")
    return save(fig, "figure8_topologie_logique_maquette.png")


def fig_arch_reseau_placeholder():
    return placeholder(
        "Schéma / image attendu(e) :\nArchitecture du réseau de l'ART\n(section I.1.1)",
        "placeholder_architecture_reseau_art.png",
        size=(10, 4.2),
    )


def fig_dispositif_placeholder():
    return placeholder(
        "Schéma / image attendu(e) :\nSynthèse du dispositif sécuritaire actuel de l'Agence\n(section I.1.2)",
        "placeholder_dispositif_securitaire.png",
        size=(10, 4.0),
    )


if __name__ == "__main__":
    fig4_topologie_maquette()
    fig6_maturite()
    fig7_pe_pa_pep()
    fig8_topologie_logique()
    fig_arch_reseau_placeholder()
    fig_dispositif_placeholder()
    print("OK", OUT)
