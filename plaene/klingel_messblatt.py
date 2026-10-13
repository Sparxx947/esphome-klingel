# Messblatt Abzweigdose (A4 hoch) fuer die Aderzuordnung der Klingel — 11.10.2026
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig = plt.figure(figsize=(8.27, 11.69)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 210); ax.set_ylim(0, 297); ax.axis("off")
T = lambda x, y, s, **k: ax.text(x, y, s, **{"fontsize": 9.5, "va": "top", **k})
T(14, 285, "Klingel: Messblatt Abzweigdose", fontsize=17, fontweight="bold")
T(14, 277, "Datum: ____________    Abzweigdose oben links über dem linken Verteiler · nur Kleinspannung (8/12 V~)", fontsize=8.5)
y = 268
T(14, y, "Vorbereitung", fontsize=11.5, fontweight="bold"); y -= 6
for s in ["Zweite Person an den Klingelknöpfen (Handy/Rufen). Multimeter auf V~, Bereich 20 V oder Auto.",
          "Deckel öffnen. Klemmen lösen nur mit Trafo-Sicherung AUS (rechter Verteiler, Reihe 3, Platz 25/26).",
          "Zum Messen muss die Sicherung EIN sein. Nichts abklemmen, nur Schrauben/WAGO-Prüföffnungen antasten.",
          "Jede Klemme mit Kreppband nummerieren (1, 2, 3 …) und die Nummern unten eintragen."]:
    T(18, y, "• " + s, fontsize=9); y -= 5.2
y -= 3; T(14, y, "Messen", fontsize=11.5, fontweight="bold"); y -= 6
for s in ["1.  Schwarze Messspitze fest an die 5er-WAGO (Bezugspunkt, bleibt die ganze Zeit dort).",
          "2.  Rote Spitze nacheinander an jede nummerierte Klemme. Je Klemme vier Werte eintragen:",
          "      ohne Drücken  ·  Knopf EG gedrückt  ·  Knopf Etage 1 gedrückt  ·  Knopf Etage 2 gedrückt",
          "3.  Gong: Klingelt er bei jedem Knopf? Ein Gong für alle oder je Etage einer? (unten ankreuzen)",
          "4.  Foto von der offenen Dose mit den Kreppband-Nummern machen."]:
    T(18, y, s, fontsize=9); y -= 5.2
y -= 4; top = y
cols = [14, 26, 74, 98, 122, 146, 170, 196]
heads = ["Nr.", "Aderfarbe(n) / Klemmtyp", "ohne\nDrücken", "EG\ngedrückt", "Etage 1\ngedrückt", "Etage 2\ngedrückt", "Bemerkung"]
rh = 9.2; n = 12
for i, h in enumerate(heads):
    ax.add_patch(Rectangle((cols[i], top - 11), cols[i + 1] - cols[i], 11, facecolor="#e8e8e8", edgecolor="black", lw=0.8))
    T(cols[i] + 1.5, top - 1.5, h, fontsize=8.3, fontweight="bold")
for r in range(n):
    yy = top - 11 - (r + 1) * rh
    for i in range(len(heads)):
        ax.add_patch(Rectangle((cols[i], yy), cols[i + 1] - cols[i], rh, fill=False, edgecolor="black", lw=0.6))
    for i in (2, 3, 4, 5):
        ax.text(cols[i + 1] - 1.5, yy + 1.5, "V~", fontsize=7.5, ha="right", color="#666")
y = top - 11 - n * rh - 6
T(14, y, "Gong:  ☐ ein Gong für alle Etagen   ☐ je Etage ein eigener Gong     Klingelt bei: ☐ EG  ☐ Etage 1  ☐ Etage 2", fontsize=9); y -= 6.5
T(14, y, "Gong-Spannung (optional, an den 2 Gong-Klemmen beim Drücken): ________ V~   (8 oder 12 V?)", fontsize=9); y -= 8
T(14, y, "Woran man es erkennt (wertet Claude aus)", fontsize=10.5, fontweight="bold"); y -= 5.5
for s in ["Etagenader = Klemme, deren Wert sich NUR bei EINEM Knopf ändert (~0 → 8–12 V oder umgekehrt).",
          "Ob 0→12 oder 12→0 zeigt nur, an welchem Trafo-Pol die WAGO hängt – beides ist in Ordnung.",
          "Klemmen, die sich bei keinem Knopf ändern, sind Zuleitung/Rückleiter – bitte auch eintragen."]:
    T(18, y, "• " + s, fontsize=8.6); y -= 4.8
y -= 2
ax.add_patch(Rectangle((12, y - 15), 186, 15, fill=False, edgecolor="#b00", lw=1.2))
T(15, y - 2, "Sicherheit", fontsize=9.5, fontweight="bold", color="#b00")
T(15, y - 7, "In der Dose liegt nur Klingel-Kleinspannung. Sieht eine Ader nach 230 V aus (dicke Mantelleitung,", fontsize=8.3)
T(15, y - 11, "braun/blau/grün-gelb) oder zeigt das Multimeter über 30 V: sofort aufhören, nichts weiter anfassen.", fontsize=8.3)
fig.savefig("klingel-messblatt-abzweigdose.pdf")
