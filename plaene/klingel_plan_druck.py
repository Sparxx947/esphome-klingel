# Druckblatt Klingel-Schaltplan mit Farbschema (A4 quer, 1 Seite) — 11.10.2026
# Basis: klingel_plan.py (unveraendert); Leitungen hier nach Aderfarbe eingefaerbt.
import re, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
FARBE = {"Erdgeschoss": "#d4a800", "Etage 1": "#1a9850", "Etage 2": "#2166ac"}
RUECK = "#8c8c8c"
src = open("klingel_plan.py").read()
src = src.replace('fig=plt.figure(figsize=(8.27,5.4)); ax=fig.add_axes([0,0,1,1]);', 'ax=fig.add_axes([0.03,0.10,0.70,0.80]);')
src = re.sub(r'fig\.savefig.*', '', src)
R = [
 ('line((12,yB),(118,yB),lw=1.8)', 'line((12,yB),(118,yB),lw=3,color=RUECK)'),
 ('    T(2,y+2.5,name,fontsize=9,fontweight="bold")', '    FC=FARBE[name]; T(2,y+2.5,name,fontsize=9,fontweight="bold",color=FC)'),
 ('line((24,y),(32,y))', 'line((24,y),(32,y),lw=3,color=FC)'),
 ('line((44,y),(58,y))', 'line((44,y),(58,y),lw=3,color=FC)'),
 ('line((52,y-11),(48,y-11),(48,y-15))', 'line((52,y-11),(48,y-11),(48,y-15),lw=3,color=RUECK)'),
 ('line((48,y-15),(48,yB) if i==2 else (48,y-15))', 'line((48,y-15),(48,yB) if i==2 else (48,y-15),lw=3,color=RUECK)'),
 ('line((98,y+1),(152,y+1))', 'line((98,y+1),(152,y+1),lw=3,color=FC)'),
 ('line((98,y-11),(132,y-11),(132,yB+8))', 'line((98,y-11),(132,y-11),(132,yB+8),lw=2.6)'),
 ('line((48,112-15),(48,yB))', 'line((48,112-15),(48,yB),lw=3,color=RUECK)'),
 ('line((132,yB+8),(172,yB+8),(172,30),lw=1.4)', 'line((132,yB+8),(172,yB+8),(172,30),lw=2.6)'),
]
for a, b in R:
    assert src.count(a) == 1, a; src = src.replace(a, b)
fig = plt.figure(figsize=(11.69, 8.27))
exec(src, {"plt": plt, "fig": fig, "matplotlib": matplotlib, "FARBE": FARBE, "RUECK": RUECK})
fig.text(0.03, 0.955, "Türklingel → Home Assistant: Schaltplan mit Aderfarben", fontsize=15, fontweight="bold")
fig.text(0.03, 0.932, "3 × PC817C + 1N4007 + 1 kΩ, Wemos D1 mini · Stand 11.10.2026 · nur Kleinspannung (Hager ST303, 8/12 V~)", fontsize=9)

# Legende rechts: eigene Verdrahtung
x0 = 0.75; y = 0.88
fig.text(x0, y, "Farbschema eigene Litzen", fontsize=11, fontweight="bold"); y -= 0.035
fig.text(x0, y, "(Etage = gleiche Farbe auf beiden Seiten)", fontsize=8, style="italic"); y -= 0.04
for name, farbe, pin in (("Erdgeschoss", "gelb", "D5"), ("Etage 1", "grün", "D6"), ("Etage 2", "blau", "D7")):
    fig.add_artist(Rectangle((x0, y - 0.004), 0.035, 0.014, transform=fig.transFigure, color=FARBE[name]))
    fig.text(x0 + 0.045, y, f"{farbe}: {name}  →  {pin}", fontsize=9.5); y -= 0.035
fig.add_artist(Rectangle((x0, y - 0.004), 0.035, 0.014, transform=fig.transFigure, color=RUECK))
fig.text(x0 + 0.045, y, "grau: Gong-Rückleiter", fontsize=9.5); y -= 0.035
fig.add_artist(Rectangle((x0, y - 0.004), 0.035, 0.014, transform=fig.transFigure, color="black"))
fig.text(x0 + 0.045, y, "schwarz: G (Masse D1)", fontsize=9.5); y -= 0.035
fig.text(x0, y, "Kein Rot verwenden (bleibt für +5 V).", fontsize=8.5); y -= 0.06

fig.text(x0, y, "Kennfarben der Bauteile", fontsize=11, fontweight="bold"); y -= 0.035
for t in ("1 kΩ: braun – schwarz – rot (– gold)",
          "1N4007: grauer/silberner Ring = Kathode",
          "       → Ring an PC817 Pin 1",
          "PC817: Punkt/Kerbe = Pin 1 (Anode)"):
    fig.text(x0, y, t, fontsize=9); y -= 0.03

fig.text(0.03, 0.03, "Trafo-Sicherung aus beim Anklemmen · nach dem Löten Durchgang Klingelseite ↔ ESP-Seite prüfen: muss unterbrochen sein · keine Pull-ups, nicht D3/D4/D8",
         fontsize=8.5)
fig.savefig("klingel-schaltplan-farbig.pdf")
