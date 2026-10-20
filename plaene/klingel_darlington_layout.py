# Druckblatt Klingel-Platine NEU: 3 Kanaele mit je 2x BC547 als Darlington (A4 quer, 2 Seiten) — 16.10.2026
# Anlass: Gongs sind Batteriegongs mit Kontakteingang (Schleife Kl.1 <-> Kl.2, Taster schliesst kurz), Optokoppler
# ungeeignet (jede mA-Last = "gedrueckt"). EG nur ~2,7-3 V -> 2N7000 zu knapp, BC517 (reichelt) noch nicht da ->
# Darlington aus 2x BC547 (Amazon-Set). Notiz project_ha_klingel.
# 16.10.: zweite Variante fuer den BC517 (fertiger Darlington, reichelt): `python3 klingel_darlington_layout.py bc517`.
# Raster: Arbeitsfeld 13 x 13 Loecher (33 x 33 mm), mittig auf die 44 x 38,7-mm-Platine, Eckloecher frei.
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle, Circle, Wedge

KAN = [("Erdgeschoss", "#d4a800", "gelb", "D5", 1, "~2,7–3 V"),
       ("Etage 1", "#1a9850", "grün", "D6", 5, "~9,5 V"),
       ("Etage 2", "#2166ac", "blau", "D7", 9, "~4,5 V ?")]
GRAU, SCHW, ROT = "#8c8c8c", "#222222", "#c0392b"
N = 13
SPALTEN = "ABCDEFGHIJKLM"
BC517 = len(sys.argv) > 1 and sys.argv[1] == "bc517"
RWERT = "9,1 MΩ" if BC517 else "1 MΩ"

def netze():
    """Liste (Netzname, Farbe, [Pfad-Pads]) — Pads (spalte 1..13, zeile 1..13), Draufsicht Bestueckungsseite."""
    n = []
    for name, fc, farbe, pin, r, _ in KAN:
        n.append((f"{name}: Ader → R", fc, [(1, r + 1), (2, r + 1)]))
        if BC517:
            n.append((f"{name}: R → B", ROT, [(6, r + 1), (7, r + 1)]))
            n.append((f"{name}: C → {pin}", "#7b3294", [(7, r), (8, r), (9, r), (10, r), (11, r)]))
            n.append((f"{name}: E → GND", SCHW, [(7, r + 2), (8, r + 2), (9, r + 2), (10, r + 2), (11, r + 2), (12, r + 2), (13, r + 2)]))
            continue
        n.append((f"{name}: R → B1", ROT, [(6, r + 1), (7, r + 1)]))
        n.append((f"{name}: C1+C2 → {pin}", "#7b3294", [(7, r), (8, r), (9, r), (10, r), (11, r)]))
        n.append((f"{name}: E1 → B2", "#e66101", [(7, r + 2), (8, r + 2), (8, r + 1), (9, r + 1), (10, r + 1)]))
        n.append((f"{name}: E2 → GND", SCHW, [(10, r + 2), (11, r + 2), (12, r + 2), (13, r + 2)]))
    n.append(("GND-Schiene rechts", SCHW, [(13, z) for z in range(3, 14)]))
    n.append(("GND-Schiene unten", SCHW, [(s, 13) for s in range(1, 14)]))
    return n

def bauteile():
    b = []
    for name, fc, farbe, pin, r, _ in KAN:
        b.append(("R", (2, r + 1), (6, r + 1), RWERT))
        if BC517:
            b.append(("Q", 7, r, "BC517"))
            continue
        b.append(("Q", 7, r, "Q1"))
        b.append(("Q", 10, r, "Q2"))
    return b

def kabel():
    k = []
    for name, fc, farbe, pin, r, _ in KAN:
        k.append(((1, r + 1), fc, f"{farbe}: Kl.1 {name}", "links"))
        k.append(((11, r), fc, f"{farbe} → {pin}", "rechts"))
    k.append(((1, 13), GRAU, "grau: alle Kl.2", "links"))
    k.append(((13, 13), SCHW, "schwarz → G", "rechts"))
    return k

def raster(ax, gespiegelt):
    X = (lambda s: N + 1 - s) if gespiegelt else (lambda s: s)
    Y = lambda z: N + 1 - z          # Zeile 1 oben
    ax.set_xlim(-6.5, N + 7.5); ax.set_ylim(-1.2, N + 2.2); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0.3, 0.3), N + 0.4, N + 0.4, fc="#f3ead8", ec="#b59a6a", lw=1.2, zorder=0))
    for s in range(1, N + 1):
        ax.text(X(s), N + 1.1, SPALTEN[s - 1], ha="center", fontsize=7, color="#777")
        for z in range(1, N + 1):
            ax.add_patch(Circle((X(s), Y(z)), 0.30, fc="#d8b46a", ec="#a07a30", lw=0.6, zorder=1))
            ax.add_patch(Circle((X(s), Y(z)), 0.11, fc="white", ec="none", zorder=2))
    for z in range(1, N + 1):
        ax.text(X(0), Y(z), str(z), va="center", ha="center", fontsize=7, color="#555", zorder=9,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    return X, Y

def seite_bestueckung(ax):
    X, Y = raster(ax, False)
    ax.text(-6.3, N + 1.9, "Bestückungsseite (Draufsicht) — Arbeitsfeld 13 × 13 Löcher, mittig, Eckbohrungen frei",
            fontsize=10, fontweight="bold")
    # Verbindungen auf der Unterseite gestrichelt durchscheinen lassen
    for nm, fc, pfad in netze():
        ax.plot([X(s) for s, z in pfad], [Y(z) for s, z in pfad], color=fc, lw=2.2, alpha=0.35, ls="--", zorder=3)
    for b in bauteile():
        if b[0] == "R":
            (s1, z1), (s2, z2), wert = b[1], b[2], b[3]
            ax.plot([X(s1), X(s2)], [Y(z1), Y(z2)], color="#555", lw=1.4, zorder=4)
            ax.add_patch(Rectangle((X(s1) + 0.9, Y(z1) - 0.33), X(s2) - X(s1) - 1.8, 0.66, fc="#e9d7a5", ec="#555", zorder=5))
            for i, c in enumerate(("white", "#8b4513", "#2166ac") if BC517 else ("#8b4513", "black", "#2e8b57")):   # 1 MΩ br-sw-gn, 9,1 MΩ ws-br-bl
                ax.add_patch(Rectangle((X(s1) + 1.3 + i * 0.35, Y(z1) - 0.33), 0.18, 0.66, fc=c, ec="#999" if c == "white" else "none", lw=0.4, zorder=6))
            ax.text((X(s1) + X(s2)) / 2, Y(z1) - 0.62, wert, ha="center", va="top", fontsize=7.5, zorder=6)
        else:
            _, s, r, lab = b
            # TO-92 stehend, Beine senkrecht in einer Spalte: C oben, B Mitte, E unten -> flache Seite nach LINKS
            ax.add_patch(Wedge((X(s) + 0.05, Y(r + 1)), 1.45, -90, 90, fc="#333", ec="black", zorder=5, alpha=0.88))
            ax.add_patch(Rectangle((X(s) - 0.05, Y(r + 2) - 0.45), 0.10, 2.9, fc="#333", ec="none", zorder=5))
            for dz, p in ((0, "C"), (1, "B"), (2, "E")):
                ax.add_patch(Circle((X(s), Y(r + dz)), 0.17, fc="#ddd", ec="black", lw=0.5, zorder=6))
                ax.text(X(s) + 0.55, Y(r + dz), p, va="center", fontsize=6.5, color="white", fontweight="bold", zorder=7)
            ax.text(X(s) + 0.6, Y(r + 2) - 0.85, lab, fontsize=7, ha="center", zorder=7)
    for (s, z), fc, txt, seite in kabel():
        if seite == "links":
            ax.plot([X(s) - 0.35, X(s) - 2.2], [Y(z), Y(z)], color=fc, lw=4, solid_capstyle="round", zorder=4)
            ax.text(X(s) - 2.4, Y(z), txt, ha="right", va="center", fontsize=7.5)
        else:
            ax.plot([X(s) + 0.35, N + 2.3], [Y(z), Y(z)], color=fc, lw=4, solid_capstyle="round", zorder=4)
            ax.text(N + 2.5, Y(z), txt, ha="left", va="center", fontsize=7.5)
    for name, fc, farbe, pin, r, u in KAN:
        ax.text(4, Y(r) + 0.05, f"{name} ({u})", fontsize=7.5, color=fc, fontweight="bold", ha="center", va="center")
    ax.text(-6.3, -0.9, "Kabel aus der Dose links, D1 mini rechts (wie im Gehäuse). Gestrichelt = Verbindungen auf der Unterseite.",
            fontsize=7.5, style="italic")

def seite_loet(ax):
    X, Y = raster(ax, True)
    ax.text(-6.3, N + 1.9, "Lötseite (Platine umgedreht, SPIEGELVERKEHRT) — Brücken",
            fontsize=10, fontweight="bold")
    for nm, fc, pfad in netze():
        ax.plot([X(s) for s, z in pfad], [Y(z) for s, z in pfad], color=fc, lw=4.2, solid_capstyle="round", zorder=4)
    for name, fc, farbe, pin, r, _ in KAN:
        ax.text(X(4), Y(r) + 0.05, name, fontsize=7.5, color=fc, fontweight="bold", ha="center", va="center")
    ax.text(-6.3, -0.9, "Spalte A ist hier RECHTS. Brücken am besten mit abgeschnittenen Widerstandsbeinen legen, nicht mit Zinn ziehen.",
            fontsize=7.5, style="italic")

def schaltplan(ax):
    ax.set_xlim(0, 100); ax.set_ylim(0, 60); ax.axis("off")
    L = lambda *p, **kw: ax.plot([a for a, b in p], [b for a, b in p], color=kw.pop("c", "black"), lw=kw.pop("lw", 1.5), **kw)
    def npn(x, y, lab):
        ax.add_patch(Circle((x, y), 4.2, fill=False, lw=1.2)); L((x - 1.5, y - 2.8), (x - 1.5, y + 2.8), lw=2.2)
        L((x - 1.5, y + 1.2), (x + 2, y + 4.2)); L((x - 1.5, y - 1.2), (x + 2, y - 4.2))
        ax.annotate("", (x + 2, y - 4.2), (x - 0.2, y - 2.3), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="black"))
        ax.text(x + 4.8, y + 0.5, lab, fontsize=8)
        return (x - 1.5, y), (x + 2, y + 4.2), (x + 2, y - 4.2)    # B, C, E
    ax.text(0, 57, "Schaltplan je Etage", fontsize=10, fontweight="bold")
    L((2, 36), (16, 36), c="#d4a800", lw=3); ax.text(2, 31.5, "Kl.1 (+, Gong-Ader)", fontsize=7.5)
    ax.add_patch(Rectangle((16, 34.4), 12, 3.2, fill=False, lw=1.4)); ax.text(22, 39, RWERT, fontsize=8, ha="center")
    if BC517:
        b1, c1, e1 = npn(40, 36, "BC517\n(Darlington)")
        L((28, 36), b1)
        L(c1, (c1[0], 48), (80, 48), lw=2.2); ax.text(81, 47.3, "→ D5/D6/D7\n(Pull-up intern)", fontsize=7.5, va="center")
        L(e1, (e1[0], 8), lw=2.2); L((2, 8), (80, 8), lw=2.2)
        ax.text(81, 8, "→ G (D1 mini)", fontsize=7.5, va="center")
        L((2, 12), (10, 12), (10, 8), c=GRAU, lw=3); ax.text(2, 13.6, "Kl.2 (−, Rückkanal) = grau", fontsize=7.5)
        ax.text(0, 1, "Ruhe: Schleifenspannung → BC517 leitet → Pin LOW.\nTaster: Kl.1 = Kl.2 → sperrt → Pin HIGH.",
                fontsize=7.5)
        return
    b1, c1, e1 = npn(40, 36, "Q1 BC547")
    L((28, 36), b1)
    b2, c2, e2 = npn(54, 24, "Q2 BC547")
    L(e1, (e1[0], 24), b2)
    L(c1, (c1[0], 48), (c2[0], 48), c2)
    L((c2[0], 48), (80, 48), lw=2.2); ax.text(81, 47.3, "→ D5/D6/D7\n(Pull-up intern)", fontsize=7.5, va="center")
    L(e2, (e2[0], 8), lw=2.2); L((2, 8), (80, 8), lw=2.2)
    ax.text(81, 8, "→ G (D1 mini)", fontsize=7.5, va="center")
    L((2, 12), (10, 12), (10, 8), c=GRAU, lw=3); ax.text(2, 13.6, "Kl.2 (−, Rückkanal) = grau", fontsize=7.5)
    ax.text(0, 1, "Ruhe: Schleifenspannung → Q1/Q2 leiten → Pin LOW.\nTaster: Kl.1 = Kl.2 → sperrt → Pin HIGH.",
            fontsize=7.5)

T517 = (
        "Stückliste\n"
        "  3× BC517 (reichelt), 3× 9,1 MΩ (reichelt; 1 MΩ aus dem Sortiment geht auch)\n"
        "  Lochraster 44 × 38,7 (wie bisher), Litze: gelb/grün/blau/grau zur Dose,\n"
        "  gelb/grün/blau/schwarz zum D1 mini. Optokoppler, 1 kΩ, 1N4007 entfallen ganz.\n\n"
        "Vor dem Einlöten jeden BC517 prüfen (Diodentest)\n"
        "  rot am mittleren Bein (B): B→C ~0,6–0,75 V, B→E ~1,1–1,4 V (zwei Strecken\n"
        "  im Darlington; manche Multimeter zeigen dort OL). Umgekehrt OL.\n"
        "  Datenblatt CDIL: flache Seite zu dir, Beine unten = C B E (wie BC547).\n"
        "  Im Layout steht er gedreht: C oben, E unten → flache Seite zeigt nach LINKS.\n\n"
        "Nach dem Löten (ohne Anschluss)\n"
        "  Durchgang: kein Piepen zwischen Nachbar-Pads fremder Netze, v. a.\n"
        "  F2/G2 (R→B) gegen G1/G3 und die C-Brücke H1–K1 gegen die E-Brücke H3–M3.\n"
        "  Diodentest rot an G2/G6/G10 (B), schwarz an GND: ~1,1–1,4 V.\n"
        "  C-Pad K1/K5/K9 → GND: OL.\n\n"
        "Erst einen Kanal, dann den Rest\n"
        "  1. Nur EG bestücken, anklemmen (gelb Kl.1, grau Kl.2, schwarz G).\n"
        "  2. Gong EG muss STUMM bleiben, Spannung Kl.1↔Kl.2 ≈ wie vorher (2,7 V).\n"
        "  3. Klingeln EG → Gong läutet, Pin D5 geht HIGH (Firmware/Log).\n"
        "  4. Dann E1 + E2. Klingelt ein Gong dauernd → sofort abklemmen.\n\n"
        "Annahmen (ungeprüft)\n"
        "  Kl.1 = Plus je Etage, Minus-Seiten dürfen zusammen (grau). Falsch gepolt:\n"
        "  Pin dauerhaft HIGH, nichts geht kaputt (µA). Firmware wird umgestellt\n"
        "  (nicht invertiert, kurze Entprellung, Dauer-HIGH = Batterie leer)."
)

def text(ax):
    ax.axis("off")
    if BC517:
        ax.text(0, 1, T517, va="top", fontsize=7.8, family="DejaVu Sans", linespacing=1.3)
        return
    t = (
        "Stückliste\n"
        "  6× BC547 (Amazon-Set), 3× 1 MΩ (eigenes Sortiment; 10 MΩ geht auch)\n"
        "  Lochraster 44 × 38,7 (wie bisher), Litze: gelb/grün/blau/grau zur Dose,\n"
        "  gelb/grün/blau/schwarz zum D1 mini. Optokoppler, 1 kΩ, 1N4007 entfallen ganz.\n\n"
        "Vor dem Einlöten jeden BC547 prüfen (Diodentest)\n"
        "  rot am mittleren Bein (B): zu beiden Außenbeinen 0,6–0,75 V, umgekehrt OL.\n"
        "  B→E etwas höher als B→C. Typisch: flache Seite zu dir, Beine unten = C B E.\n"
        "  Im Layout steht er gedreht: C oben, E unten → flache Seite zeigt nach LINKS.\n\n"
        "Nach dem Löten (ohne Anschluss)\n"
        "  Durchgang: kein Piepen zwischen Nachbar-Pads fremder Netze, v. a.\n"
        "  H2/I2 (E1→B2) gegen H1/I1 (C-Brücke) und gegen G2 (B1).\n"
        "  Diodentest rot an G2/G6/G10 (B von Q1), schwarz an GND:\n"
        "  ~1,1–1,4 V (zwei B-E-Strecken in Reihe). C-Pad K1/K5/K9 → GND: OL.\n\n"
        "Erst einen Kanal, dann den Rest\n"
        "  1. Nur EG bestücken, anklemmen (gelb Kl.1, grau Kl.2, schwarz G).\n"
        "  2. Gong EG muss STUMM bleiben, Spannung Kl.1↔Kl.2 ≈ wie vorher (2,7 V).\n"
        "  3. Klingeln EG → Gong läutet, Pin D5 geht HIGH (Firmware/Log).\n"
        "  4. Dann E1 + E2. Klingelt ein Gong dauernd → sofort abklemmen.\n\n"
        "Annahmen (ungeprüft)\n"
        "  Kl.1 = Plus je Etage, Minus-Seiten dürfen zusammen (grau). Falsch gepolt:\n"
        "  Pin dauerhaft HIGH, nichts geht kaputt (µA). Firmware wird umgestellt\n"
        "  (nicht invertiert, kurze Entprellung, Dauer-HIGH = Batterie leer)."
    )
    ax.text(0, 1, t, va="top", fontsize=7.8, family="DejaVu Sans", linespacing=1.3)

DATEI = "klingel-platine-bc517" if BC517 else "klingel-platine-darlington"
with PdfPages(f"{DATEI}.pdf") as pdf:
    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Klingel-Platine neu: 3× BC517 statt Optokoppler — Stand 20.10.2026 (9,1 MΩ)" if BC517 else
                 "Klingel-Platine neu: 3× Darlington (2× BC547) statt Optokoppler — Stand 16.10.2026",
                 fontsize=13, fontweight="bold", x=0.02, ha="left")
    seite_bestueckung(fig.add_axes((0.0, 0.04, 0.60, 0.88)))
    schaltplan(fig.add_axes((0.60, 0.50, 0.40, 0.42)))
    text(fig.add_axes((0.61, 0.03, 0.38, 0.46)))
    pdf.savefig(fig); fig.savefig(f"{DATEI}-vorschau1.png", dpi=110); plt.close(fig)

    fig = plt.figure(figsize=(11.69, 8.27))
    fig.suptitle("Klingel-Platine neu — Lötseite + Brückenliste", fontsize=13, fontweight="bold", x=0.02, ha="left")
    seite_loet(fig.add_axes((0.0, 0.04, 0.60, 0.88)))
    ax = fig.add_axes((0.61, 0.03, 0.38, 0.88)); ax.axis("off")
    zeilen = ["Brückenliste (Lötseite; Koordinaten wie Bestückungsseite)", ""]
    for nm, fc, pfad in netze():
        zeilen.append(f"{nm}:  " + (f"{SPALTEN[pfad[0][0]-1]}{pfad[0][1]} bis {SPALTEN[pfad[-1][0]-1]}{pfad[-1][1]}"
                      if nm.startswith("GND") else " – ".join(f"{SPALTEN[s-1]}{z}" for s, z in pfad)))
    zeilen += ["", "Bauteile:", f"  {RWERT} liegend, Beine: EG B2/F2, E1 B6/F6, E2 B10/F10"]
    zeilen += (["  BC517 Spalte G — C in Zeile 1/5/9, B in 2/6/10, E in 3/7/11",
                "  (Spalten H–L bleiben frei bis auf die Brücken)"] if BC517 else
               ["  Q1 Spalte G, Q2 Spalte J — C in Zeile 1/5/9,",
                "     B in 2/6/10, E in 3/7/11"])
    zeilen += [
               "Kabel: Ader-Pads A2 / A6 / A10, grau A13,",
               "  zum D1: K1 (D5) / K5 (D6) / K9 (D7), schwarz M13"]
    ax.text(0, 1, "\n".join(zeilen), va="top", fontsize=8, linespacing=1.45)
    pdf.savefig(fig); fig.savefig(f"{DATEI}-vorschau2.png", dpi=110); plt.close(fig)
print("ok")
