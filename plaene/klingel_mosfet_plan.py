# Druckblatt Klingel-Umbau auf 2N7000 (A4 quer, 1 Seite) — 12.10.2026
# Anlass: Gongs sind elektronische 9-V-Batteriegongs mit Kontakteingang (Ruhe 9 V DC, Taster schliesst kurz),
# Optokoppler-Abgriff bekam nie Strom. Siehe docs/verlauf.md (12.10.).
# ANNAHME (noch ungemessen): je Etage ist eine Ader Plus (Signal, 9 V in Ruhe), die andere Minus; Minus-Seiten duerfen zusammen.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib.lines import Line2D

FARBE = {"Erdgeschoss": ("#d4a800", "gelb", "D5"), "Etage 1": ("#1a9850", "grün", "D6"), "Etage 2": ("#2166ac", "blau", "D7")}
GRAU = "#8c8c8c"

fig = plt.figure(figsize=(11.69, 8.27))
ax = fig.add_axes((0.02, 0.07, 0.68, 0.82)); ax.set_xlim(0, 200); ax.set_ylim(0, 130); ax.axis("off")
def L(*pts, **kw):
    kw.setdefault("color", "black"); kw.setdefault("lw", 1.6)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], solid_capstyle="round", **kw)
def T(x, y, s, **kw): ax.text(x, y, s, **kw)
def masse(x, y, farbe="black"):
    L((x, y), (x, y - 3), color=farbe, lw=2.4)
    for i, w in enumerate((4, 2.6, 1.2)):
        L((x - w, y - 3 - i * 1.3), (x + w, y - 3 - i * 1.3), color="black", lw=1.6)

for i, (name, (fc, farbe, pin)) in enumerate(FARBE.items()):
    y = 108 - i * 38
    T(2, y + 7, name, fontsize=10, fontweight="bold", color=fc)
    # Plus-Ader (Signal) → 1 MΩ → Gate
    L((4, y), (40, y), color=fc, lw=3.2)
    T(5, y + 1.8, f"{farbe}: + Ader (9 V)", fontsize=7.5)
    ax.add_patch(Rectangle((40, y - 2.2), 16, 4.4, fill=False, lw=1.6))
    T(48, y + 3.6, "1 MΩ", fontsize=8.5, ha="center")
    L((56, y), (72, y))
    T(66, y + 1.2, "G", fontsize=8, color="#555")
    # N-MOSFET 2N7000 (vereinfachtes Symbol)
    L((72, y - 5), (72, y + 5), lw=2)                                     # Gate-Platte
    for a, b in ((y + 3.5, y + 6.5), (y - 1.5, y + 1.5), (y - 6.5, y - 3.5)):
        L((75, a), (75, b), lw=2.4)                                      # Kanal (3 Segmente)
    L((75, y + 5), (82, y + 5), (82, y + 12))                           # Drain
    L((75, y - 5), (82, y - 5), (82, y - 12))                           # Source
    L((82, y), (82, y - 5))                                              # Body an Source
    ax.add_patch(FancyArrow(82, y, -5.6, 0, width=0.05, head_width=2.2, head_length=2.2, color="black", length_includes_head=True))
    T(85, y + 9, "D", fontsize=8, color="#555"); T(85, y - 10, "S", fontsize=8, color="#555")
    T(68, y - 10.5, "2N7000", fontsize=8.5, fontweight="bold", ha="center")
    masse(82, y - 12)
    # Drain → D1-Pin
    L((82, y + 12), (150, y + 12), lw=2.4)
    T(120, y + 13.4, f"→ {pin}", fontsize=8.5, ha="center")
    # Minus-Ader der Etage
    L((4, y - 8), (26, y - 8), color=GRAU, lw=3.2)
    T(5, y - 6.2, "− Ader (Gong-Minus) → grau", fontsize=7.5)
    masse(26, y - 8, GRAU)

# D1 mini
ax.add_patch(Rectangle((150, 12), 34, 112, fill=False, lw=2))
T(167, 116, "Wemos\nD1 mini", fontsize=10, fontweight="bold", ha="center", va="top")
for i, (name, (fc, farbe, pin)) in enumerate(FARBE.items()):
    T(152, 108 - i * 38 + 12 - 1.2, pin, fontsize=9, fontweight="bold")
T(167, 52, "interner Pull-up\n(Firmware)", fontsize=8, ha="center", style="italic")
T(167, 30, "USB-Netzteil\n(Verteiler)", fontsize=8, ha="center", style="italic")
L((150, 18), (140, 18), lw=2.4); T(152, 16.8, "G", fontsize=9, fontweight="bold"); masse(140, 18)
T(100, 2, "Massezeichen = gemeinsame Masse: alle Source-Beinchen + alle Minus-Adern (grau) + D1 „G“ (schwarz)", fontsize=8.5, ha="center")

fig.text(0.03, 0.955, "Türklingel → Home Assistant: Umbau auf 2N7000 (Batteriegong mit Kontakteingang)", fontsize=15, fontweight="bold")
fig.text(0.03, 0.932, "3 × 2N7000 + 3 × 1 MΩ, Wemos D1 mini · Stand 12.10.2026 · Optokoppler, 1N4007 und 1 kΩ entfallen · Trafo ist NICHT beteiligt", fontsize=9)

# rechte Spalte
x0 = 0.71; y = 0.885
def H(s):
    global y; fig.text(x0, y, s, fontsize=11, fontweight="bold"); y -= 0.032
def Z(s, **kw):
    global y; fig.text(x0, y, s, fontsize=8.6, **kw); y -= 0.026

H("① VOR dem Löten messen (DC)")
Z("Je Etage die 2 Adern mit 9 V finden.")
Z("Schwarz an Ader A, rot an Ader B:")
Z("  +9 V → B ist Plus (Signal), A ist Minus")
Z("  −9 V → umgekehrt")
Z("Plan gilt nur, wenn je Etage eine eigene", color="#b2182b")
Z("Plus-Ader und Minus gemeinsam/verbindbar.", color="#b2182b")
Z("Sonst: Werte an Claude, Plan anpassen.", color="#b2182b"); y -= 0.012

H("② Pinbelegung 2N7000")
# kleines Bild: flache Seite zum Betrachter
bx, by = x0 + 0.02, y - 0.075
fig.add_artist(Rectangle((bx, by + 0.03), 0.09, 0.045, transform=fig.transFigure, fill=False, lw=1.5))
fig.text(bx + 0.045, by + 0.052, "2N7000\n(flache Seite)", fontsize=7.5, ha="center", va="center")
for k, s in enumerate(("S", "G", "D")):
    xx = bx + 0.015 + k * 0.03
    fig.add_artist(Line2D([xx, xx], [by + 0.03, by + 0.002], transform=fig.transFigure, color="black", lw=1.5))
    fig.text(xx, by - 0.016, s, fontsize=10, fontweight="bold", ha="center")
fig.text(bx + 0.11, by + 0.045, "links → rechts:\nSource · Gate · Drain", fontsize=8.3, va="center")
y = by - 0.045
Z("Gegenprobe Diodentest: rot an S, schwarz an D")
Z("  → 0,5–0,8 V (Body-Diode), umgekehrt: OL"); y -= 0.012

H("③ Bauteile")
Z("1 MΩ: braun – schwarz – grün (– gold)")
Z("   oder braun – schwarz – schwarz – gelb – braun")
Z("Raus: 3× PC817, 3× 1N4007, 3× 1 kΩ"); y -= 0.012

H("④ Funktion")
Z("Ruhe: Ader 9 V → MOSFET leitet → Dx = LOW")
Z("Taste: Ader 0 V → MOSFET sperrt → Dx = HIGH")
Z("Gong-Last: ≈ 0 (Gate zieht keinen Strom)")

fig.text(0.03, 0.035, "Nie zwei Plus-Adern verbinden und nie Plus mit Minus — das ist für den Gong ein Tastendruck · Minus-Adern dürfen zusammen", fontsize=8.3)
fig.text(0.03, 0.015, "Keine Pins D3/D4/D8 · nach dem Löten Durchgang prüfen: Drain ↔ Gate und Drain ↔ Source dürfen nicht piepen", fontsize=8.3)
fig.savefig("klingel-schaltplan-mosfet.pdf")
fig.savefig("klingel-schaltplan-mosfet-vorschau.png", dpi=80)
