🇬🇧 [English version](einmessen.en.md)

# Einmessen / Kalibrieren

Eine Klingel hat keine Messwerte im engeren Sinn. „Einmessen“ heißt hier: herausfinden, **welche Ader zu welcher Etage**
gehört, die **Gong-Spannung** bestimmen, die Bauteilwerte dagegen nachrechnen, Bauteile und Platine **vor** dem Einbau
prüfen und nach dem Einbau Filter und WLAN kontrollieren.

Werte aus den Projektnotizen sind belegt; mit *(Vorschlag)* oder *(ungeprüft)* markierte Schritte stehen so nicht in den
Notizen bzw. wurden noch nicht am Gerät nachvollzogen.

---

## 1. Adern zuordnen

**Termin: Fr 09.10.2026 18:30.**

Ausgangslage (Fotos 06.10.): In der Abzweigdose oben links über dem linken Verteiler laufen mehrere Fernmeldeleitungen
zusammen (Adern rot, schwarz, gelb, weiß, blau, lila, grün, grau, schwarz-weiß und schwarz-orange geringelt). Unten
kommen Einzeladern rot/weiß/blau heraus – vermutlich zum Trafo im Verteiler. Verbunden ist mit Lüsterklemmen sowie einer
WAGO 2273-203 (3-fach) und einer **WAGO 2273-205 (5-fach)**, die vermutlich den gemeinsamen Leiter vom Trafo trägt.
Die alten Kreppband-Beschriftungen sind kaum lesbar. Aus den Fotos war die Zuordnung **nicht** möglich.

### Vorgehen

1. Abdeckung der Dose öffnen. Werden Klemmen gelöst: **vorher Sicherung des Klingeltrafos aus.** Zum Messen selbst
   muss die Anlage natürlich unter Spannung stehen (Kleinspannung 8/12 V AC).
2. Multimeter auf **V~** (Wechselspannung, Bereich 20 V oder Auto).
3. Eine Messspitze fest an die **5er-WAGO** (gemeinsamer Leiter).
4. Zweite Person drückt unten **einen** Klingelknopf und hält ihn; mit der anderen Spitze nacheinander die
   Lüsterklemmen-Schrauben abtasten.
5. Die Ader, die **nur bei diesem Knopf 8–12 V** zeigt, ist die Etagenader dieser Etage.
6. Für die anderen beiden Knöpfe wiederholen.
7. Den **Gong-Rückleiter** (Gegenpol für Pin 2 der Optokoppler) bestimmen – laut Plan „per Messung bestimmen“.
   *(Ungeprüft, wie genau er sich in dieser Dose zeigt: Ist die 5er-WAGO selbst der Rückleiter, ist sie der
   gemeinsame Anschlusspunkt aller drei Pin 2.)*
8. Ergebnis notieren und **auf neues Kreppband schreiben**:

| Etage | Aderfarbe / Klemme | gemessene Spannung | Eingang |
|---|---|---|---|
| Erdgeschoss | … | … V~ | D5 |
| Etage 1 | … | … V~ | D6 |
| Etage 2 | … | … V~ | D7 |
| Rückleiter | … | – | Pin 2 aller PC817 |

Gegenprobe: Kreppband-Beschriftung lesen, falls möglich.

---

## 2. Gong-Spannung bestimmen

Der Hager ST303 liefert **8 V zwischen Klemme 2–4** und **12 V zwischen 2–8**. Welche der Gong nutzt, ist offen.
Die Messung aus Schritt 1 zeigt es direkt (~8 V oder ~12 V effektiv; leerlaufend kann sie etwas höher liegen).

---

## 3. Bauteilwerte nachrechnen

### Spitzenspannung

Û = U_eff × √2

| Trafo-Abgriff | U_eff | Û |
|---|---|---|
| 8 V (2–4) | 8 V | ≈ 11,3 V |
| 12 V (2–8) | 12 V | ≈ 17 V |

Die LED des PC817 verträgt in Sperrrichtung nur ~6 V → **Gegendiode 1N4007 antiparallel ist Pflicht**.

### LED-Strom und Leistung am Vorwiderstand (1 kΩ)

Formel aus dem Werkstattbuch (U_F der LED ≈ 1,2 V):

I ≈ (U − 1,2 V) / 1 kΩ  P ≈ (U − 1,2 V)² / 1 kΩ

| Gong-Spannung | I (Effektivwert-Rechnung) | I in der Spitze (Û) | P am Widerstand |
|---|---|---|---|
| 8 V | ≈ 6,8 mA | ≈ 10 mA | ≈ 0,05 W |
| 12 V | ≈ 11 mA | ≈ 16 mA | ≈ 0,12 W |

Die Rechnung mit dem Effektivwert ist konservativ: Durch die Gegendiode leitet die LED nur in einer Halbwelle, die
tatsächliche Verlustleistung ist etwa halb so groß. **1 kΩ / 0,25 W reicht** in beiden Fällen. Der Optokoppler verträgt
laut Notizen 50 mA (dort für den PC814 genannt; beim PC817 laut gängigem Datenblatt ebenfalls 50 mA – *nicht gegen das
konkrete Datenblatt geprüft*).

### Belastung des Klingeltrafos

8 VA ⇒ max. ~1 A bei 8 V bzw. ~0,67 A bei 12 V. Die drei Optokoppler-Zweige ziehen nur je ~10 mA, und nur solange
geklingelt wird – unkritisch. Der D1 mini (~80 mA, Sendespitzen ~350 mA bei 5 V) wird **bewusst nicht** aus dem Trafo
versorgt.

---

## 4. Bauteile vor dem Löten prüfen

| Prüfung | Wie | Erwartung |
|---|---|---|
| 1N4007 Polung | Multimeter Diodentest | Durchlass ~0,6–0,7 V von Anode nach Kathode (Strich), Gegenrichtung „OL“ |
| PC817 LED | Diodentest zwischen Pin 1 (+) und Pin 2 | ~1,0–1,2 V Durchlass, umgekehrt „OL“ |
| PC817 Pin 1 finden | Punkt/Kerbe auf dem Gehäuse | Pin 1 = Anode, Pin 2 = Kathode, Pin 3 = Emitter, Pin 4 = Kollektor |
| Widerstand | Ohm-Messung | ~1 kΩ (Farbringe braun-schwarz-rot) |
| Gegendiode richtig herum | nach dem Löten Diodentest über Pin 1/Pin 2 | in **einer** Richtung ~0,65 V (1N4007, von Pin 2 nach Pin 1), in der anderen ~1,1 V (LED). Zeigen beide Richtungen ~0,65 V oder eine „OL“, ist etwas falsch |

*(Die Tabelle ist ein Vorschlag aus dem Schaltplan abgeleitet; Werte sind typische Datenblattwerte.)*

---

## 5. Tischtest vor dem Einbau *(Vorschlag)*

Ohne Klingeltrafo lässt sich jeder Kanal mit Gleichspannung testen:

1. D1 mini per USB versorgen, Firmware geflasht, Log offen (ESPHome Builder → Logs oder `esphome logs`).
2. Vom **5V-Pin** des D1 mini über den bestückten 1 kΩ an **Pin 1**, Pin-2-Schiene an **G** (nur für den Test –
   im Betrieb bleibt die Klingelseite getrennt!).
3. Erwartung: `<Etage> gedrückt` geht auf **ON**, ein Event `gedrueckt` erscheint; nach Trennen nach ~200 ms **OFF**.
4. Strom dabei: (5 − 1,2) V / 1 kΩ ≈ 3,8 mA – reicht für den PC817 bei internem Pull-up.

Damit ist die Ausgangsseite geprüft. Das **Wechselspannungsverhalten** (50 Pulse/s) prüft erst der Test an der Anlage.

---

## 6. Filter am echten Signal kontrollieren

Konfiguration: `delayed_on: 30ms`, dann `delayed_off: 200ms`.

| Situation | Erwartung |
|---|---|
| kurzer Druck (~0,3 s) | genau **ein** Event, Eingang ~0,2 s länger an als gedrückt |
| langer Druck (3 s) | ein Event, kein Flackern ON/OFF im Log |
| zweimal kurz hintereinander (< 0,2 s Pause) | ein Event (Pause wird überbrückt) |
| kein Druck, Gong ruhig | keine Events (Störspitzen < 30 ms werden verworfen) |

**Wichtig – ungeprüfter Verdacht:** ESPHome wendet die Filter **der Reihe nach** an. Mit PC817 + Gegendiode ist der
Eingang pro 20-ms-Periode nur rund 8–10 ms „an“. `delayed_on: 30ms` als **erster** Filter verwirft ein ON, sobald vor
Ablauf der 30 ms ein OFF kommt – das passiert bei Halbwellen jede Periode. Dann käme **gar kein** Druck durch.
Abhilfe: Reihenfolge tauschen (`delayed_off: 200ms` zuerst, dann `delayed_on: 30ms`), oder `delayed_on` auf ≤ 5 ms
senken. Beim Tischtest mit Gleichspannung (Schritt 5) fällt das **nicht** auf. Siehe
[fehlersuche.md](fehlersuche.md#1-gong-klingelt-aber-kein-ereignis-in-ha).

---

## 7. WLAN am Einbauort

Die Verteiler sind Kunststoff in einer Holznische (kein Metallkasten), ein normaler D1 mini sollte reichen – laut
Notiz trotzdem **nach dem Einbau prüfen**: Entität `WLAN-Signal` (alle 120 s).

| RSSI | Bewertung *(allgemeiner Richtwert, nicht aus den Notizen)* |
|---|---|
| besser als −70 dBm | gut |
| −70 … −80 dBm | brauchbar, Events können sich verzögern |
| schlechter als −80 dBm | Abhilfe: Lage ändern; notfalls D1 mini Pro mit Außenantenne |

---

## 8. Sperrzeit in Home Assistant

Die Automation meldet je Taster höchstens alle **15 s**. Getestet (04.10., Template in HA):

| Vorher → nachher | Abstand | Ergebnis |
|---|---|---|
| `unknown` → Zeitstempel | erster Druck überhaupt | meldet |
| Zeitstempel → Zeitstempel | 8 s | meldet **nicht** |
| Zeitstempel → Zeitstempel | 20 s | meldet |

Die Sperre ist **je Etage** getrennt – zwei Etagen kurz nacheinander melden beide.
