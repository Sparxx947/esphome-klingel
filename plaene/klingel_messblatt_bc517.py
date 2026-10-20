# Messblatt Klingel nach BC517-Umbau (A4 quer, 1 Seite) — 20.10.2026
# Anlass: nach dem Umbau zeigt HA in Ruhe alle 3 Kanaele "aus" (Pin HIGH) und kein Event bei 9 Druecken.
# Ziel: Polaritaet Kl.1/Kl.2, GND-Verbindung, Basis- und Pinspannung je Etage. Notiz project_ha_klingel.
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATEI = "klingel-messblatt-bc517"
fig = plt.figure(figsize=(11.69, 8.27))
fig.text(0.03, 0.955, "Klingel nach BC517-Umbau — Messblatt (20.10.2026)", fontsize=17, weight="bold")
fig.text(0.03, 0.935, "Multimeter auf DC V (20-V-Bereich).  Schwarze Spitze = erste Spalte, rote = zweite.\n"
         "Alles in RUHE messen, außer Zeile 5.  Vorzeichen immer mitschreiben!", fontsize=10.5, va="top")

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

fig.text(0.03, 0.865, "0. Anker zuerst (prüft Messbereich + Spitzen)", fontsize=11.5, weight="bold")
y = tabelle(0.85, ["Schwarz an", "Rot an", "Erwartet", "Gemessen"],
            [["G (D1 mini)", "3V3 (D1 mini)", "+3,2 … +3,4 V", ""]],
            [0.17, 0.17, 0.2, 0.2])

fig.text(0.03, y - 0.025, "Je Etage", fontsize=11.5, weight="bold")
B = [0.035, 0.12, 0.18, 0.27, 0.11, 0.11, 0.11]
y = tabelle(y - 0.04, ["Nr.", "Schwarz an", "Rot an", "Erwartet", "EG (gelb, D5)", "E1 (grün, D6)", "E2 (blau, D7)"], [
    ["1", "grau (Kl.2)", "Kl.1-Ader der Etage", "PLUS: EG ≈ 2,7 · E1 ≈ 9,5 · E2 ? V", "", "", ""],
    ["2", "G (D1 mini)", "BC517 Mittelbein (B)", "+0,9 … +1,4 V", "", "", ""],
    ["3", "G (D1 mini)", "Pin D5 / D6 / D7", "unter 0,8 V (= LOW)", "", "", ""],
    ["4", "G (D1 mini)", "grau (Kl.2)", "0 V (nur einmal nötig)", "", "—", "—"],
    ["5", "G (D1 mini)", "Pin, Taster GEDRÜCKT", "≈ +3,3 V (Helfer drückt)", "", "", ""],
], B)

fig.text(0.03, y - 0.03, "Was die Werte bedeuten", fontsize=11.5, weight="bold")
fig.text(0.03, y - 0.045,
    "Zeile 0 ≠ 3,3 V  → Bereich falsch (AC? mV?) oder Spitzen nicht richtig drin — erst das klären.\n"
    "Zeile 1 negativ  → Kl.1 und Kl.2 vertauscht: Basis bekommt Minus, BC517 leitet nie (geht dabei nicht kaputt).\n"
    "Zeile 1 = 0 V    → Ader nicht an der Platine oder Batterie leer.\n"
    "Zeile 2 ≈ 0 V bei richtiger Zeile 1 → Widerstand/Brücke Ader→R→B fehlt oder kalte Lötstelle.\n"
    "Zeile 2 ≈ Wert von Zeile 1 → Emitter hängt nicht an GND, oder BC517 gedreht (flache Seite muss nach LINKS).\n"
    "Zeile 3 zwischen 0,8 und 2,5 V → BC517 leitet nur halb: Grenzbereich des D1-Eingangs (unbestätigt).\n"
    "Zeile 3 ≈ 3,3 V bei guter Zeile 2 → Collector-Brücke zum Pin fehlt.\n"
    "Zeile 4 nicht 0 V → graue Leitung nicht mit G / GND-Schiene (M3–M13, A13–M13) verbunden.",
    fontsize=9.3, va="top", family="monospace")

fig.text(0.03, 0.105, "Zum zusätzlichen Klingeln im EG:", fontsize=11.5, weight="bold")
fig.text(0.03, 0.085, "War jemand an der Haustür?   ☐ ja   ☐ nein, Gong kam von allein   ☐ weiß nicht"
         "        Nach welchem Taster?  ☐ EG  ☐ E1  ☐ E2       Uhrzeit ca.: ________",
         fontsize=10, va="top")
fig.text(0.03, 0.035, "Fällt dir beim Messen etwas auf (Gong klingelt, Dauerklingeln): sofort graue Leitung abklemmen.",
         fontsize=9.5, style="italic")

fig.savefig(f"{DATEI}.pdf")
fig.savefig(f"{DATEI}-vorschau.png", dpi=110)
print("ok")
