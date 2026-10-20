# Durchgangspruefung Klingel-Platine BC517 (A4 quer, 1 Seite) — 20.10.2026
# Anlass: grau→Farbe +3,1/+9,47/+5,5 V, aber G→Farbe −2/−2/−4 V → G liegt nicht auf grau (Emitter offen).
# Pads laut klingel_darlington_layout.py bc517. Notiz project_ha_klingel.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATEI = "klingel-durchgang-bc517"
fig = plt.figure(figsize=(11.69, 8.27))
fig.text(0.03, 0.955, "Klingel-Platine — Durchgangsprüfung GND (20.10.2026)", fontsize=17, weight="bold")
fig.text(0.03, 0.935, "Multimeter auf Durchgang (Piepser).  USB-Stecker am D1 mini ABZIEHEN, Klingeladern dürfen dranbleiben.\n"
         "Reihenfolge einhalten: die erste Prüfung, die NICHT piept, zeigt die Unterbrechung.", fontsize=10.5, va="top")

def tabelle(y0, kopf, zeilen, breiten, hoehe=0.052):
    x = 0.03
    xs = [x]
    for b in breiten:
        x += b; xs.append(x)
    def zeile(y, werte, fett=False, grau=False):
        for i, w in enumerate(werte):
            if grau:
                fig.patches.append(plt.Rectangle((xs[i], y - hoehe), breiten[i], hoehe, transform=fig.transFigure,
                                                 fc="#e8e8e8", ec="none", zorder=0))
            fig.text(xs[i] + 0.006, y - hoehe / 2, w, fontsize=9.3, va="center", weight="bold" if fett else "normal")
        for xx in xs:
            fig.add_artist(plt.Line2D([xx, xx], [y, y - hoehe], transform=fig.transFigure, color="#444", lw=0.8))
        fig.add_artist(plt.Line2D([xs[0], xs[-1]], [y - hoehe] * 2, transform=fig.transFigure, color="#444", lw=0.8))
    fig.add_artist(plt.Line2D([xs[0], xs[-1]], [y0] * 2, transform=fig.transFigure, color="#444", lw=0.8))
    zeile(y0, kopf, fett=True, grau=True)
    y = y0 - hoehe
    for z in zeilen:
        zeile(y, z)
        y -= hoehe
    return y


fig.text(0.03, 0.865, "0. Anker zuerst: Prüfspitzen aneinanderhalten → muss piepen (sonst falscher Bereich)", fontsize=11.5, weight="bold")
y = tabelle(0.85, ["Nr.", "Fühler 1", "Fühler 2", "Soll", "piept?", "Wenn nicht"], [
    ["a", "G am D1 mini", "graue Ader (Ende an der Platine)", "piept", "☐ ja ☐ nein", "weiter mit b"],
    ["b", "G am D1 mini", "Pad M13", "piept", "☐ ja ☐ nein", "schwarze Litze M13 ↔ G lose / kalt"],
    ["c", "Pad A13 (graue Ader)", "Pad M13", "piept", "☐ ja ☐ nein", "Brücke A13–M13 (Unterseite) fehlt"],
    ["d1", "G am D1 mini", "EG-BC517 unteres Bein E (G3)", "piept", "☐ ja ☐ nein", "Brücke G3–M3 / Schiene M3–M13"],
    ["d2", "G am D1 mini", "E1-BC517 unteres Bein E (G7)", "piept", "☐ ja ☐ nein", "Brücke G7–M7"],
    ["d3", "G am D1 mini", "E2-BC517 unteres Bein E (G11)", "piept", "☐ ja ☐ nein", "Brücke G11–M11"],
], [0.04, 0.17, 0.25, 0.07, 0.11, 0.30])

fig.text(0.03, y - 0.03, "Gegenprobe (darf NICHT piepen)", fontsize=11.5, weight="bold")
y = tabelle(y - 0.045, ["Nr.", "Fühler 1", "Fühler 2", "Soll", "piept?", "Wenn doch"], [
    ["e", "G am D1 mini", "gelbe / grüne / blaue Ader", "still", "☐ ☐ ☐", "Ader auf GND-Schiene → Etage kurzgeschlossen"],
], [0.04, 0.17, 0.25, 0.07, 0.11, 0.30])

fig.text(0.03, y - 0.035,
    "Lage auf der Platine (Draufsicht Bestückungsseite, Spalte A links): graue Ader in A13 · GND-Schiene unten A13–M13 und rechts M3–M13 ·\n"
    "schwarze Litze zum D1 in M13 · BC517 in Spalte G, Emitter unten (Zeile 3 / 7 / 11).  Auf der Lötseite ist Spalte A RECHTS.",
    fontsize=9.5, va="top")
fig.text(0.03, 0.13, "Danach:", fontsize=11.5, weight="bold")
fig.text(0.03, 0.11,
    "Fehlstelle nachlöten → USB wieder einstecken → Claude Bescheid geben.  Erwartung: in HA springen alle drei Kanäle\n"
    "auf „gedrückt“ (alte Firmware, Zeichen dass die BC517 leiten).  Dann neue Firmware und Abnahme je Etage.",
    fontsize=10, va="top")
fig.text(0.03, 0.035, "Offen: Zusätzliches Klingeln im EG — war jemand an der Tür?   ☐ ja   ☐ nein, von allein", fontsize=10)

fig.savefig(f"{DATEI}.pdf")
fig.savefig(f"{DATEI}-vorschau.png", dpi=110)
print("ok")
