🇬🇧 [English version](README.en.md)

# Türklingel → Home Assistant (ESPHome, Wemos D1 mini)

Die vorhandene, klassische Klingelanlage im Haus bekommt einen „Mithörer“: Ein Wemos D1 mini erkennt über
drei Darlington-Transistoren (**BC517**), an **welcher Etage** jemand klingelt, und meldet das als `event` (device_class `doorbell`) an
Home Assistant. Der Gong klingelt **unverändert weiter** – der ESP greift nur Kleinspannung ab und schaltet nichts.

> **✅ Stand 20.10.2026: läuft.** Jede Etage hat einen **eigenen batteriebetriebenen Gong mit Kontakteingang**; der
> Taster schließt nur die Gong-Schleife kurz (Optokoppler-Abgriff deshalb ungeeignet, siehe [Verlauf](docs/verlauf.md)).
> Seit dem 20.10. hängt je Etage ein **BC517 mit 9,1 MΩ Basiswiderstand** an der Schleife: In Ruhe liegt die
> Batteriespannung an, der BC517 leitet, der Eingang ist **LOW**; beim Drücken bricht die Spannung zusammen → **HIGH**.
> Abnahme am 20.10.: alle drei Etagen je genau **ein** Event, kein Übersprechen. Plan:
> [`plaene/klingel-platine-bc517.pdf`](plaene/klingel-platine-bc517.pdf), Einzelheiten:
> [Schaltung BC517](#schaltung-bc517-seit-20102026). Die PC817-Abschnitte weiter unten sind **historisch**.

| | |
|---|---|
| Projektkürzel (Werkstattbuch) | **K1 Türklingel · 3 Etagen mithören** |
| Board | Wemos D1 mini V3.0.0 (ESP8266), „D1 #2“ aus dem Bestand |
| Erkennung | 3 × **BC517** (Darlington, TO-92) + 3 × **9,1 MΩ** an den Gong-Schleifen (seit 20.10.2026). Historisch: PC817C + 1N4007 + 1 kΩ (funktioniert bei Batteriegongs nicht), 2N7000 (fürs Erdgeschoss mit ~3 V zu knapp) |
| Abgriff | Abzweigdose oben links über dem linken Kleinverteiler im Treppenhaus (dort laufen **alle** Klingeladern zusammen, nur Kleinspannung) |
| Klingeltrafo | Hager ST303, 8 VA, PRI 230 V (Klemmen 1/7), SEC 8 V (2–4) / 12 V (2–8), rechter Verteiler, Reihe 3, Platz 25/26 |
| Stromversorgung D1 | USB-Netzteil an einer Schuko-Steckdose im linken Verteiler („SNS016“, Reihe 5, Platz 49–52) – **nicht** aus dem Klingeltrafo |
| Eingänge | Erdgeschoss → D5 (GPIO14) · Etage 1 → D6 (GPIO12) · Etage 2 → D7 (GPIO13) |
| HA-Reaktion | Push mit Kamerabild an die Bewohner der Etage, alle drei Wandpanels zeigen das Livebild der Haustür, Alexa-Ansage je Etage |

## Nachbauen

Hinweise für den Nachbau in einem anderen Haus:

- **Secrets:** `firmware/secrets.example.yaml` nach `secrets.yaml` kopieren (bzw. im ESPHome Builder anlegen) und
  WLAN-Name, WLAN-Passwort, API-Schlüssel und Hotspot-Passwort durch eigene Werte ersetzen.
- **Home Assistant:** In `ha/klingel-*.yaml` die Platzhalter in spitzen Klammern ersetzen (Handy-Dienst, Kamera,
  Fully-Kiosk-Geräte und -Entitäten, HA-Adresse) – Tabelle in [docs/home-assistant.md](docs/home-assistant.md#nachbauen).
- **Zuerst den Gong ansehen:** Hat er eine eigene Batterie und nur zwei Drähte zum Taster (Kontakteingang), passt
  die BC517-Schaltung dieses Repos. Wird der Gong dagegen vom Klingeltrafo getrieben (Wechselspannung am Gong beim
  Drücken), passt die historische Optokoppler-Variante (PC817 + Gegendiode).
- **Polarität je Etage messen** (Multimeter auf V⎓, vorher an einem bekannten Punkt prüfen): Die Ader an der Basis
  (hier „Kl.1“) muss **Plus** gegen den gemeinsamen Rückleiter (grau) sein. Siehe
  [`plaene/klingel-messblatt-bc517.pdf`](plaene/klingel-messblatt-bc517.pdf).

## Prinzip (BC517, seit 20.10.2026)

Jeder Gong legt in Ruhe seine Batteriespannung auf die Taster-Schleife (hier: Erdgeschoss ~3,1 V, Etage 1 ~9,5 V,
Etage 2 ~5,5 V, gemessen 20.10.). Der Taster schließt die Schleife kurz, der Gong erkennt das und läutet. Über
**9,1 MΩ** fließt aus der Schleife ein Basisstrom von nur etwa 0,2–1 µA in einen **BC517** (Darlington, Verstärkung
≥ 30 000) – genug, um den Eingang des D1 mini gegen den internen Pull-up auf LOW zu ziehen, und so wenig, dass der
Gong ihn nicht als Tastendruck wertet. Beim Drücken fällt die Schleifenspannung auf ~0 V, der BC517 sperrt, der
Eingang geht auf **HIGH** → Event `gedrueckt`.

Der Emitter aller drei BC517 und der gemeinsame Rückleiter (grau = alle Kl.2) liegen an **G** des D1 mini.

## Prinzip (PC817, historisch – funktioniert hier nicht)

Drückt jemand unten einen Klingelknopf, liegt am Gong dieser Etage die Wechselspannung des Klingeltrafos (8 oder 12 V AC)
an. Parallel zum Gong hängt die LED eines PC817 (über 1 kΩ). Der Optokoppler trennt die Klingel galvanisch vom ESP;
sein Transistor zieht den Eingang des D1 mini (interner Pull-up) gegen GND.

Der PC817 hat nur **eine** LED, die in Sperrrichtung nur etwa 6 V verträgt – der Trafo liefert in der Spitze bis ~17 V.
Deshalb liegt eine **1N4007 antiparallel** zur LED und fängt die negative Halbwelle ab. Dadurch kommen am Eingang nur
**50 Pulse pro Sekunde** an; der Filter `delayed_off: 200ms` macht daraus einen durchgehenden Tastendruck. Er steht
deshalb **vor** `delayed_on: 230ms` – die umgekehrte Reihenfolge hätte jeden Druck verworfen (behoben am 11.10. vor dem
Erstflash, siehe [Fehlersuche Nr. 1](docs/fehlersuche.md#1-gong-klingelt-aber-kein-ereignis-in-ha)).

> Ursprünglich war der **PC814** geplant (zwei antiparallele LEDs, für Wechselspannung gebaut). Er war bei Amazon.de
> erst ab 15.10.–18.11. lieferbar, daher PC817 + Gegendiode. Die Kopfkommentare in `firmware/klingel.yaml` beschreiben
> seit dem 11.10. den PC817-/USB-Stand.

---

## Status (Stand 20.10.2026)

> **Kurz:** In Betrieb. Platine mit 3 × BC517 + 9,1 MΩ an der Abzweigdose angeschlossen, Firmware per OTA aus dem
> ESPHome Builder umgestellt (nicht invertiert, 30/100 ms Entprellung, Sensor „Klingelbatterie leer“). Abnahme am
> 20.10.: je Etage ein Druck → genau ein Event (gedrückt 0,31 / 0,37 / 0,34 s), keine andere Etage ausgelöst.
> HA-Anbindung seit 20.10. 17:03 abgenommen: Push mit Kamerabild aufs Handy, Livebild 90 s auf dem Wandpanel der
> Etage ([docs/home-assistant.md](docs/home-assistant.md)).

| Bereich | Stand | Datum |
|---|---|---|
| **Abnahme BC517** | ✔ **bestanden**: Erdgeschoss, Etage 1, Etage 2 nacheinander gedrückt → je genau ein Event, Binärsensor 0,31–0,37 s EIN, kein Übersprechen, „Klingelbatterie leer“ AUS | 20.10. |
| **Firmware BC517** | ✔ per OTA (ESPHome Builder): `inverted: false`, `delayed_on: 30ms` / `delayed_off: 100ms`, Template-Sensor „Klingelbatterie leer“ (ein Kanal > 30 s gedrückt) | 20.10. |
| **Platine BC517** | ✔ gelötet nach [`plaene/klingel-platine-bc517.pdf`](plaene/klingel-platine-bc517.pdf); beim ersten Anschluss leitete kein Kanal (Ursache beim Nachprüfen behoben, nicht im Einzelnen festgehalten), danach alle drei ✔ | 20.10. |
| Polarität der Gong-Adern je Etage (DC) | ✔ gemessen: Kl.1 gegen grau Erdgeschoss **+3,1 V**, Etage 1 **+9,47 V**, Etage 2 **+5,5 V** | 20.10. |
| Gong-Belegung | ✔ je Etage Klemme 1 = Gong-Ader (Plus), Klemme 2 = Rückkanal; Erdgeschoss 2 × AA (~3 V) → 2N7000 zu knapp → **BC517** | 14.10. |
| **Gong-Typ** | **geklärt**: je Etage ein eigener Batteriegong mit Kontakteingang. Etage 1: elektronischer Gong mit 9-V-Block, Lautsprecher, nur 2 Drähte, **9 V DC** an den Klemmen in Ruhe (gemessen). Erdgeschoss: vermutlich ebenfalls 9 V (*ungeprüft*). Etage 2: anderer Gong mit 3 × Babyzelle (C/LR14) = 4,5 V (*Spannung an den Adern ungemessen*). Hersteller unbekannt. | 12.10. |
| **PC817-Abgriff** | **funktioniert hier nicht** – Trafo ist nicht im Gong-Kreis, die LED bekommt keinen Strom. Einzige Treffer im Log waren Anklemmstöße. Platine abgeklemmt. | 12.10. |
| Umbau auf 2N7000 | **verworfen** (14.10.): Erdgeschoss hat nur ~3 V Schleifenspannung, zu knapp für die Gate-Schwelle. Ersetzt durch BC517 | 12.10. / 14.10. |
| Firmware `klingel.yaml` PC817-Stand (historisch) | Filter `delayed_off: 200ms` vor `delayed_on: 230ms` für 50-Hz-Halbwellen – seit 20.10. ersetzt | 04.10. / 11.10. |
| Erstflash | **erledigt** per USB mit echten Secrets (ESPHome 2026.9.1, RAM 39,0 %, Flash 40,3 %); WLAN verbunden, API-Handshake mit echtem Schlüssel ok | 11.10. |
| Etagen-Namen / Entitäten | **fertig** (Erdgeschoss / Etage 1 / Etage 2) | 04.10. |
| Empfänger je Etage | **fertig** (EG → Bewohner EG, Etage 1/2 → Bewohner Etage 1/2) | 06.10. |
| Versorgungskonzept | **entschieden**: USB-Netzteil aus der Verteiler-Steckdose statt Trafo | 06.10. |
| Abgriffpunkt | **entschieden**: Abzweigdose oben links (nur Klingeladern, von Jens bestätigt) | 06.10. |
| Schaltplan PC817 + Gegendiode | **fertig** als SVG (`plaene/klingel_plan.svg`) und farbiger Druckplan mit Litzenfarben (`plaene/klingel-schaltplan-farbig.pdf`) | 06.10. / 11.10. |
| PC817C, Diodensortiment | **geliefert** | 07.10. (von Jens am 08.10. bestätigt) |
| Minilötplatinen 45 × 39 mm | **geliefert** | 09.10. |
| 1 kΩ-Widerstände | **vorhanden und verbaut** | 11.10. |
| Platine (3 Kanäle) | **gelötet und geprüft** (Diodentest je Kanal, Trennung Klingel-/ESP-Seite) – Einzelpad-Platine, fehlende Verbindungen nachgelötet | 11.10. |
| Tischtest | **bestanden** mit 18650-Zelle: alle 3 Kanäle, jede Farbe nur ihre Etage, kein Übersprechen | 11.10. |
| Zuordnung Ader ↔ Etage in der Abzweigdose | **teilweise**: Die 5er-WAGO ist Trafo-Pol 4 (dort laufen alle Taster-Leitungen zusammen). Welche zwei Adern je Etage die Gong-Schleife bilden, ist noch **offen** | 12.10. |
| Gong-Spannung (8 V oder 12 V AC) | **entfällt** – die Gongs hängen nicht am Trafo, sondern an eigenen Batterien | 12.10. |
| Feste IP | ✔ im Router fest vergeben | 11.10. |
| ESPHome Builder | als `klingel.yaml` angelegt, Secrets eingetragen, Gerät online ✔ | 11.10. |
| Adoption in HA | ✔ eingebunden: `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2`, `binary_sensor.klingel_*_gedruckt`, Status, WLAN-Signal, Laufzeit | 11.10. |
| Event `gedrueckt` erst nach dem OFF im Log | ✔ geklärt: In HA kommt das Event **beim Drücken** an (Test 11.10.: Event 49,818 s, Binärsensor EIN 49,922 s, AUS 53,588 s). Die Verzögerung war nur die Ausgabe des Log-Clients. ([Fehlersuche Nr. 16](docs/fehlersuche.md#16-event-erscheint-erst-nach-dem-off)) | 11.10. |
| HA-Anbindung | ✔ **in Betrieb**: Push mit Kamerabild je Etage, Livebild 90 s auf dem Panel der Etage; abgenommen EG + Etage 1 (Panel Etage 2 war ohne Strom). Alter Entwurf `ha/historisch/` nie angelegt | 20.10. |
| Gehäuse | **konstruiert** (`gehaeuse/`), Druck am 11.10. gestartet (Abschluss in den Notizen nicht ausdrücklich bestätigt) | 11.10. |
| Nebenbefund 12.10. | ✔ **erledigt**: Mit BC517 kommen Event und Binärsensor „on“ zusammen an (Event ~0,1 s vor dem Binärsensor) | 12.10. / 20.10. |
| Einmaliges Nachläuten Erdgeschoss | **ungeklärt**: beim ersten Test am 20.10. läutete der Erdgeschoss-Gong einmal zusätzlich; bei der Abnahme nicht wieder beobachtet | 20.10. |

---

## Stückliste

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| Mikrocontroller | 1 | Wemos D1 mini V3.0.0 (ESP8266), „D1 #2“ | Bestand (4 × vorhanden) | vorhanden |
| *historisch:* Optokoppler | 3 (+ Reserve) | PC817C, DIP-4, 50 Stück (ALLECIN) | Amazon.de, **B0CBKK6T3D**, 7,99 € | geliefert 07.10. |
| *historisch:* Gegendiode | 3 | 1N4007 (alternativ 1N5819 – Erholzeit bei 50 Hz egal) aus Diodensortiment (BOJACK) | Amazon.de, **B07YK3XMQQ**, 10,99 € (gemeinsam mit Projekt Tankmessung) | geliefert 07.10. |
| *historisch:* Vorwiderstand | 3 | 1 kΩ, 0,25 W reicht (~10 mA, ~0,12 W) | Widerstandssortiment (AZ-Delivery) | vorhanden, verbaut 11.10. |
| Lochraster | 1 | Minilötplatine 45 × 39 mm (gemessen 44,12 × 38,74), 5 Stück – **einzelne Lötpunkte ohne Leiterbahnen** | Amazon.de, **B073FVX29X**, 5,19 € | geliefert 09.10., gelötet 11.10. |
| Netzteil | 1 | USB-Netzteil 5 V (Typ nicht festgelegt) für die Schuko-Steckdose im linken Verteiler | – | **ungeklärt** (Bestand?) |
| USB-Kabel | 1 | passend zum D1 mini, Länge Steckdose → Abzweigdose | – | **ungeklärt** |
| Leitungen Abzweigdose → Platine | 4 Adern (3 Etagenadern + Rückleiter) | Einzellitzen Ø 1,38 mm: grau = Gong-Rückleiter, gelb = Erdgeschoss, grün = Etage 1, blau = Etage 2; Verbindung in der Dose (Lüster/WAGO) | – | Farben festgelegt 11.10.; Klemmung in der Dose **nicht festgelegt** |
| Verbindungen Platine → D1 | 4 (D5, D6, D7, G) | gelb → D5, grün → D6, blau → D7, schwarz → G (Jumperkabel aus dem ELEGOO-Set M2M/F2M/F2F oder direkt gelötet) | Bestand | vorhanden |
| Gehäuse | 1 | Box + Deckel, `gehaeuse/klingel_box.stl` + `gehaeuse/klingel_deckel.stl` (PLA) + 4 Blechschrauben 3 × 12, Wandmontage 4 × Spax 4 | Eigendruck | konstruiert 11.10., Druck nicht bestätigt |
| Werkzeug | – | Multimeter (geliehen; eigenes UNI-T UT139C bestellt), Lötkolben | Bestand / bestellt | vorhanden |
| *optional:* Relaismodul | 1 | für „Gong stumm“ an D1 (GPIO5), Öffner-Kontakt | – | nur Idee, auskommentiert |
| **BC517:** Darlington-Transistor | 3 (10 bestellt) | BC517 (TO-92, CDIL) | reichelt | geliefert 20.10., verbaut |
| **BC517:** Basiswiderstand | 3 (5 bestellt) | 9,1 MΩ, 1/4 W (10 MΩ war ausverkauft; 1 MΩ geht laut Rechnung auch) | reichelt | geliefert 20.10., verbaut |
| *historisch:* 2N7000 | – | aus einem Transistor-Set mit 24 Typen (ALLECIN; enthält auch BC547 → Darlington-Ersatz aus 2 × BC547) | Amazon.de, **B0C1V82313**, 9,99 € | nicht verbaut |

**Nicht mehr nötig** (aus dem Trafo-Versorgungsentwurf vom 04.10.): Brückengleichrichter, Elko 1000 µF/35 V, Step-down-Modul,
1N5408-Dioden für den Dioden-Abgriff, Hutschienengehäuse, D1 mini Pro mit Außenantenne (Verteiler sind Kunststoff in einer
Holznische, kein Metallkasten).

---

## Schaltung BC517 (seit 20.10.2026)

Druckplan: [`plaene/klingel-platine-bc517.pdf`](plaene/klingel-platine-bc517.pdf) (2 Seiten A4 quer: Bestückungsseite mit
Schaltplan je Etage und Prüfschritten, Lötseite gespiegelt mit Brückenliste; Vorschau
`plaene/klingel-platine-bc517-vorschau1.png` / `-vorschau2.png`). Erzeugt von `plaene/klingel_darlington_layout.py bc517`;
ohne Argument entsteht die Ersatzvariante mit je **2 × BC547 als Darlington** + 1 MΩ
([`plaene/klingel-platine-darlington.pdf`](plaene/klingel-platine-darlington.pdf)).

| Von | Bauteil | Nach | Hinweis |
|---|---|---|---|
| Kl.1 der Etage (Plus der Gong-Batterie) | 9,1 MΩ | BC517 **Basis** | gelb = Erdgeschoss, grün = Etage 1, blau = Etage 2 |
| BC517 **Kollektor** | – | D5 / D6 / D7 | interner Pull-up |
| BC517 **Emitter** | – | GND-Schiene → D1 mini **G** | alle drei Emitter gemeinsam |
| Kl.2 aller Etagen (grau) | – | GND-Schiene | gemeinsamer Rückleiter |

| Zustand | Schleife | BC517 | Eingang | HA |
|---|---|---|---|---|
| Ruhe | Batteriespannung (3–9,5 V) | leitet | **LOW** | aus |
| Taste gedrückt | ~0 V | sperrt | **HIGH** | gedrückt + Event |
| Dauer-HIGH > 30 s | keine Spannung (Batterie leer, Ader lose) | sperrt | HIGH | „Klingelbatterie leer“ |

Pinbelegung BC517 (Datenblatt CDIL, flache Seite zum Betrachter, Beine unten): **C · B · E**. Im Layout steht er gedreht
(C oben, E unten, flache Seite nach links).

**Prüfblätter:** [`plaene/klingel-messblatt-bc517.pdf`](plaene/klingel-messblatt-bc517.pdf) (Spannungen je Etage:
Kontrollmessung 3V3↔G, Kl.1↔grau, Basis, Pin in Ruhe/gedrückt) und
[`plaene/klingel-durchgang-bc517.pdf`](plaene/klingel-durchgang-bc517.pdf) (Durchgang G ↔ grau ↔ GND-Schiene ↔ Emitter).

**Grenzwert (abgeleitet, nicht gemessen):** Ein Darlington zieht den Kollektor nicht ganz auf 0 V, es bleiben
~0,6–0,9 V. Der ESP8266 erkennt LOW sicher erst unter ~0,8 V. Liegt der Pin in Ruhe in diesem Bereich, kann der D1
„HIGH“ lesen – siehe [Fehlersuche Nr. 23](docs/fehlersuche.md#23-bc517-kanal-leitet-in-ruhe-nicht).

> **Historisch – 2N7000 (12.–14.10.):** Geplant war je Etage ein 2N7000 mit 1 MΩ am Gate
> ([`plaene/klingel-schaltplan-mosfet.pdf`](plaene/klingel-schaltplan-mosfet.pdf)). Verworfen, weil die
> Erdgeschoss-Schleife nur ~3 V hat und die Gate-Schwelle des 2N7000 dafür zu knapp ist.

## Pinbelegung und Verdrahtung

> Die Litzenfarben und die D1-Belegung gelten unverändert. Die Tabelle „Je Etage“ beschreibt die **historische
> PC817-Variante** – für die aktuelle Schaltung gilt [Schaltung BC517](#schaltung-bc517-seit-20102026).

Schaltplan: [`plaene/klingel_plan.svg`](plaene/klingel_plan.svg) (erzeugt von `plaene/klingel_plan.py`).
Druckfassung mit Litzenfarben (A4 quer): [`plaene/klingel-schaltplan-farbig.pdf`](plaene/klingel-schaltplan-farbig.pdf)
(erzeugt von `plaene/klingel_plan_druck.py`).

### Je Etage (3 × identisch)

| Von | Bauteil | Nach | Hinweis |
|---|---|---|---|
| Etagenader (per Messung bestimmt) | 1 kΩ | PC817 **Pin 1** (Anode) | |
| PC817 **Pin 2** (Kathode) | – | Gong-Rückleiter (gemeinsam) | alle drei Pin 2 auf eine Schiene |
| 1N4007 **Kathode (Strich)** | – | PC817 Pin 1 | antiparallel zur LED |
| 1N4007 **Anode** | – | PC817 Pin 2 | |
| PC817 **Pin 4** (Kollektor) | – | D1 mini Dx (siehe unten) | interner Pull-up, kein externer Widerstand |
| PC817 **Pin 3** (Emitter) | – | D1 mini **G** | alle drei Emitter gemeinsam |

### Litzenfarben (Stand 11.10.)

| Seite | Farbe | Bedeutung |
|---|---|---|
| Klingelseite | grau | Gong-Rückleiter |
| Klingelseite | gelb | Erdgeschoss |
| Klingelseite | grün | Etage 1 |
| Klingelseite | blau | Etage 2 |
| ESP-Seite | gelb | → D5 (Erdgeschoss) |
| ESP-Seite | grün | → D6 (Etage 1) |
| ESP-Seite | blau | → D7 (Etage 2) |
| ESP-Seite | schwarz | → G |

Etage = gleiche Farbe auf beiden Seiten. **Kein Rot** – das bleibt für +5 V.

### D1 mini

| Pin D1 | GPIO | Funktion | Entität (Erwartung) |
|---|---|---|---|
| D5 | GPIO14 | Erdgeschoss, `INPUT_PULLUP`, nicht invertiert (seit 20.10.) | `event.klingel_erdgeschoss` |
| D6 | GPIO12 | Etage 1, `INPUT_PULLUP`, nicht invertiert (seit 20.10.) | `event.klingel_etage_1` |
| D7 | GPIO13 | Etage 2, `INPUT_PULLUP`, nicht invertiert (seit 20.10.) | `event.klingel_etage_2` |
| G | – | gemeinsamer Emitter der 3 BC517 + grauer Rückleiter | |
| USB | – | Versorgung über USB-Netzteil | |
| D1 (GPIO5) | – | reserviert für optionales „Gong stumm“-Relais | |
| D3 / D4 / D8 | – | **nicht verwenden** (Boot-Pins) | |

Zuordnung und Polarität der Adern sind seit dem 14./20.10. gemessen (siehe Status).

---

## Gehäuse

Quelle: [`gehaeuse/klingel-gehaeuse.scad`](gehaeuse/klingel-gehaeuse.scad) (OpenSCAD, parametrisch). In OpenSCAD
`TEIL = "box"` bzw. `"deckel"` setzen, F6, als STL exportieren. Fertige Dateien:
[`gehaeuse/klingel_box.stl`](gehaeuse/klingel_box.stl) und [`gehaeuse/klingel_deckel.stl`](gehaeuse/klingel_deckel.stl).

**Stand 11.10.: konstruiert, gedruckt noch nicht bestätigt.** Ein Testdruck einer früheren Fassung zeigte: das
Lochraster passt.

### Gemessene Maße (Grundlage)

| Teil | Maß |
|---|---|
| Lochraster (Minilötplatine) | 44,12 × 38,74 mm |
| D1 mini | 34,2 × 25,6 mm |
| D1 mit Stiftleisten + Dupont-Steckern nach oben | 25 mm hoch |
| Micro-USB-Stecker (Umspritzung) | 10,8 × 7,2 mm |
| Litzen zur Abzweigdose | 4 × Ø 1,38 mm |

### Aufbau

| Punkt | Ausführung |
|---|---|
| Box | außen 102,5 × 44,7 × 37 mm (mit Laschen 67,7 mm breit), Wand 2,2 mm, Innenhöhe 35 mm |
| Deckel | 2 mm mit Lippe und 4 Niederhaltern (29,7 mm) auf die Lochraster-Ecken |
| Lochraster | links auf 4 Eckstützen 5,5 × 5,5 mm (die Platine hat große Befestigungslöcher in den Ecken) – **Ecken frei lassen, auch von Heißkleber** |
| D1 mini | rechts auf einem 6-mm-Sockel unter dem Antennen-Ende + 2 Stützen 4 × 4,5 mm neben der USB-Buchse (Mitte 9,5 mm frei) |
| Litzen | links durch Ø 4,5 mm, Kabelbinder-Zugentlastung an 2 Pfosten |
| USB | rechts durch 12,5 × 11,6 mm (deckt die Buchse, ob sie oben oder unten auf der Platine sitzt) |
| Verschraubung | 4 Schraubsäulen innen in den Ecken, Deckel mit 4 Blechschrauben 3 × 12 |
| Wandmontage | 4 Laschen für Spax 4 |
| Druck | PLA, 0,2 mm, ohne Stützen; Deckel mit der Platte nach unten (die STL liegt schon so) |
| Prüfung | per OpenSCAD-Schnittmengen: Durchbrüche frei, Deckel ohne Kollision, Platinen nur auflagernd |

### Lehren

| Punkt | Lehre |
|---|---|
| Wandstärke | In einer ersten Fassung endeten die Durchbrüche **blind**: `hull()` mit außen liegenden Eckdomen hatte alle Wände auf 6,5 mm verdickt. Jetzt sitzen die Schraubsäulen innen. |
| Kollisionen | **Vor dem STL-Export prüfen**: Platinen nicht auf durchgehende Auflagen legen, sondern auf Stützen **zwischen** den Stiftleisten (Stiftleisten laufen über die ganze Platinenlänge). |

---

## Firmware

Datei: [`firmware/klingel.yaml`](firmware/klingel.yaml)

| Einstellung | Wert |
|---|---|
| Gerätename / Hostname | `klingel` (→ `klingel.local`) |
| Friendly Name | `Klingel` |
| Board | `esp8266` / `d1_mini` |
| IP | im Router fest vergeben (11.10.) |
| `substitutions` | `taster_1: Erdgeschoss`, `taster_2: Etage 1`, `taster_3: Etage 2` |
| Eingänge | `INPUT_PULLUP`, `inverted: false` (Ruhe LOW, Druck HIGH) |
| Filter je Eingang | `delayed_on: 30ms`, `delayed_off: 100ms` (Anker `&klingelfilter`) – Gleichspannung, nur Prellen/Störspitzen verwerfen (bis 19.10.: 200/230 ms für 50-Hz-Halbwellen, siehe Fehlersuche Nr. 1) |
| Logger | `INFO` |
| API | verschlüsselt (`!secret klingel_api_key`) |
| OTA | `platform: esphome` |
| Fallback-Hotspot | SSID `Klingel-Fallback`, Passwort `!secret klingel_ap_password`, mit Captive Portal |

### Entitäten in Home Assistant

| Entität (erwartet) | Typ | Bedeutung |
|---|---|---|
| `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2` | event, doorbell | Event-Typ `gedrueckt`; Zustand = Zeitstempel des letzten Drucks |
| `binary_sensor.klingel_erdgeschoss_gedruckt` usw. | binary_sensor | Rohzustand des Eingangs (gefiltert) |
| `binary_sensor.klingel_status` | status | ESP online |
| `sensor.klingel_wlan_signal` | Signal (dBm), alle 120 s | |
| `sensor.klingel_laufzeit` | Uptime, alle 600 s | |
| `binary_sensor.*_klingelbatterie_leer` | problem | EIN, wenn ein Kanal länger als 30 s „gedrückt“ zeigt: Gong-Batterie leer oder Ader lose (seit 20.10.) |

### Secrets

`firmware/secrets.example.yaml` ist nur die Vorlage (Schlüssel `wifi_ssid`, `wifi_password`, `klingel_api_key`,
`klingel_ap_password`). **Echte Werte stehen nur im ESPHome Builder** bzw. lokal in einer nicht eingecheckten Datei
(`.gitignore` schließt `secrets.yaml` und `secrets.*.yaml` aus). API-Schlüssel erzeugen: `openssl rand -base64 32`.

### Flashen

1. **Erstflash per USB** mit den **echten** Secrets:
   `esphome run klingel.yaml --no-logs --device /dev/ttyUSB0` – auf „Successfully compiled“ achten.
   Unter Linux vorher den Port freigeben: `setfacl -m u:$USER:rw /dev/ttyUSB0` (nach jedem Umstecken neu).
2. Gegenprobe per API mit dem echten Schlüssel (Zustände lesen).
3. In HA die ESPHome-Integration mit Host und Verschlüsselungsschlüssel hinzufügen; im Router feste IP setzen.
4. Im **ESPHome Builder**: Secrets ergänzen, „New device“ → überspringen → YAML einfügen, **nicht** installieren.
   Ab dann Updates **per OTA** aus dem Builder.

Stand 20.10.: Updates laufen per OTA aus dem ESPHome Builder (zuletzt die BC517-Firmware am 20.10.).

Stand 11.10.: Schritt 1 und 2 erledigt (Erstflash lokal per USB, API-Handshake mit echtem Schlüssel ok). Im Builder ist
das Gerät als `klingel.yaml` angelegt und die Secrets eingetragen. HA-Adoption und feste IP im Router sind erledigt
(11.10.).

> **Falle:** Nie einen Prüf-Build mit Dummy-Secrets flashen (am 06.10. beim Heizungs-ESP passiert: Hotspot-Passwort
> und API-Schlüssel falsch). `esphome upload` übersetzt **nicht** neu und spielt blind den letzten Build auf – für echte
> Firmware immer `esphome run`.

---

## Anleitungen

| Dokument | Inhalt |
|---|---|
| [docs/einmessen.md](docs/einmessen.md) | Adern zuordnen, Gong-Spannung, Strom-/Leistungsrechnung, Bauteile prüfen, Tischtest, Filter, WLAN |
| [docs/einbau.md](docs/einbau.md) | Aufbau der Platine, Inbetriebnahme, Einbau an der Abzweigdose, Abnahmetest |
| [docs/fehlersuche.md](docs/fehlersuche.md) | bekannte und absehbare Fehlerbilder mit Ursache und Lösung |
| [docs/verlauf.md](docs/verlauf.md) | Entscheidungen und verworfene Varianten (PC814, Trafo-Versorgung, Dioden-Abgriff) |

**Kurzfassung der Reihenfolge:** Teile prüfen ✅ → Platine löten ✅ → Erstflash ✅ → Tischtest ✅ →
HA/Builder/feste IP ✅ → Einbau mit PC817 ✗ (12.10., Batteriegongs) → Polarität je Etage messen ✅ → Umbau auf
BC517 ✅ → Firmware umstellen ✅ → je Etage einmal klingeln ✅ (20.10.) → **HA-Paket anlegen** → Alexa-Routinen.

**Sicherheit:** Vor dem Öffnen von Klemmen die Sicherung des Klingeltrafos ausschalten. In der Abzweigdose liegen laut
Sichtprüfung (Jens, 06.10.) nur Klingeladern. Die 230-V-Seite des Trafos gehört dem Elektriker.

---

## Home-Assistant-Anbindung

**In Betrieb seit 20.10.2026** – Einzelheiten, Nachbau und Abnahme in [docs/home-assistant.md](docs/home-assistant.md).

| Baustein | Funktion |
|---|---|
| Automation [`ha/klingel-automation.yaml`](ha/klingel-automation.yaml) | `event.received` je Etage → Push aufs Handy mit Standbild der Haustürkamera, Etage im Titel, je Etage eine Meldung (`tag`), eigener Kanal „Klingel“, Antippen öffnet das Livebild |
| Skript [`ha/klingel-kamera-skript.yaml`](ha/klingel-kamera-skript.yaml) | Wandpanel der Etage (Fully Kiosk): Bildschirm an → Bewegung auslösen → `load_url` Kamera-Dashboard → 90 s → Start-URL |
| Dashboard [`ha/klingel-kamera-dashboard.yaml`](ha/klingel-kamera-dashboard.yaml) | `klingel-kamera`: Livebild der Haustür über die ganze Fläche |

Nicht umgesetzt (Ideen aus dem alten Entwurf in [`ha/historisch/`](ha/historisch/klingel-entwurf-20261004.yaml)):
Alexa-Ansage je Etage, Empfänger je Etage, Sturmklingel-Sperre.

---

## Offene Punkte / nächste Schritte / Termine

| # | Punkt | Wer | Termin |
|---|---|---|---|
| 1 | ~~Adern in der Abzweigdose messen (V~)~~ – am 12.10. gemessen; ersetzt durch Nr. 14 (DC-Messung je Gong-Schleife) | Jens | ✅ 12.10. |
| 2 | Kreppband-Beschriftung in der Dose lesen (Gegenprobe zur Messung) | Jens | mit 1 |
| 3 | ~~Gong-Spannung 8 V oder 12 V~~ – entfällt, Batteriegongs | – | 12.10. |
| 4 | 1 kΩ-Widerstände | – | ✅ vorhanden, verbaut 11.10. |
| 5 | Minilötplatinen-Lieferung | – | ✅ geliefert 09.10. |
| 6 | **Filter-Reihenfolge** in `klingel.yaml` (siehe Fehlersuche Nr. 1) | – | ✅ korrigiert 11.10., vor dem Erstflash |
| 7 | Kopfkommentare in `klingel.yaml` auf PC817 + USB-Versorgung aktualisieren | – | ✅ 11.10. |
| 8 | Schaltplan als PDF (PC817 + Gegendiode, mit Litzenfarben) | – | ✅ `plaene/klingel-schaltplan-farbig.pdf`, 11.10. |
| 9 | Platine löten, Tischtest, Erstflash | Jens/Claude | ✅ 11.10. |
| 9a | Feste IP vergeben | – | ✅ 11.10. |
| 9b | ✅ Builder-Secrets `klingel_api_key` / `klingel_ap_password` ergänzt, HA-Adoption | – | erledigt 11.10. |
| 9c | ✅ Event-Verzögerung geprüft: in HA kommt das Event beim Drücken ([Fehlersuche Nr. 16](docs/fehlersuche.md#16-event-erscheint-erst-nach-dem-off)) | – | erledigt 11.10. |
| 10 | HA-Paket anlegen, Alexa (`alexa.yaml`, Routinen), Start-URL Panels E1/E2 prüfen | Claude/Jens | nach Adoption |
| 11 | WLAN-Signal am Einbauort prüfen | – | nach Einbau |
| 12 | Gehäuse konstruieren | – | ✅ 11.10. (`gehaeuse/`) |
| 12a | Gehäuse drucken | Jens | am 11.10. gestartet |
| 12b | Einbau an der Abzweigdose und Abnahmetest ([einbau.md](docs/einbau.md) C/D) | – | 12.10. mit PC817 gescheitert; neu nach 14–16 |
| 13 | optional: Relais „Gong stumm“ | – | später, nicht beauftragt |
| 14 | ✅ Je Etage Gong-Adern und Polarität gemessen (Kl.1 = Plus) | Jens | 14.10. / 20.10. |
| 15 | ✅ Teile: BC517 + 9,1 MΩ (reichelt) | – | geliefert 20.10. |
| 16 | ✅ Umbau: PC817/1N4007/1 kΩ raus, 3 × BC517 + 3 × 9,1 MΩ nach `plaene/klingel-platine-bc517.pdf` | Jens | 20.10. |
| 17 | ✅ Firmware umgestellt (OTA), Abnahmetest je Etage bestanden | Claude/Jens | 20.10. |
| 18 | ✅ Nebenbefund 12.10.: mit BC517 kommen Event und Binärsensor zusammen an | – | 20.10. |
| 19 | Einmaliges Nachläuten des Erdgeschoss-Gongs beim ersten Test (20.10.) beobachten | Jens | laufend |

---

## Dateien im Repo

| Pfad | Inhalt |
|---|---|
| `README.md` | diese Übersicht |
| `docs/einmessen.md` | Einmessen / Kalibrieren |
| `docs/einbau.md` | Aufbau, Inbetriebnahme, Einbau, Test |
| `docs/fehlersuche.md` | Fehlerbilder |
| `docs/verlauf.md` | Projektverlauf und verworfene Varianten |
| `firmware/klingel.yaml` | ESPHome-Konfiguration (D1 mini, 3 Eingänge, 3 Events, Batterie-leer-Sensor) – BC517-Stand |
| `firmware/secrets.example.yaml` | Vorlage für die Secrets (ohne echte Werte) |
| `ha/klingel-automation.yaml` | Automation: Push aufs Handy + Kamera aufs Etagen-Panel (in Betrieb seit 20.10.) |
| `ha/klingel-kamera-skript.yaml` | Skript: Wandpanel wecken, Livebild 90 s, zurück zur Startseite |
| `ha/klingel-kamera-dashboard.yaml` | Dashboard `klingel-kamera` (Livebild über die ganze Fläche) |
| `ha/historisch/klingel-entwurf-20261004.yaml` | **historisch**: nie angelegter Paket-Entwurf (Alexa, Sturmklingel-Sperre) |
| `docs/home-assistant.md` | HA-Anbindung: Ablauf, Nachbau, Abnahme, Fallen |
| `plaene/klingel-platine-bc517.pdf` | **aktueller Plan**: Platine mit 3 × BC517 + 9,1 MΩ, 2 Seiten (Bestückung + Schaltplan + Prüfschritte, Lötseite + Brückenliste), Stand 20.10. |
| `plaene/klingel-platine-bc517-vorschau1.png` / `-vorschau2.png` | Vorschau der beiden Seiten |
| `plaene/klingel-platine-darlington.pdf` | Ersatzvariante mit je 2 × BC547 als Darlington + 1 MΩ (16.10., nicht verbaut) |
| `plaene/klingel_darlington_layout.py` | erzeugt beide Platinenpläne (`python3 klingel_darlington_layout.py bc517` bzw. ohne Argument); in `plaene/` ausführen |
| `plaene/klingel-messblatt-bc517.pdf` / `klingel_messblatt_bc517.py` | Messblatt Spannungen je Etage nach dem Umbau (20.10.) |
| `plaene/klingel-durchgang-bc517.pdf` / `klingel_durchgang_bc517.py` | Durchgangsprüfung der GND-Verbindungen (20.10.) |
| `plaene/klingel_plan.svg` | *historisch:* Schaltplan je Etage: 1 kΩ, PC817, 1N4007, Ausgänge D5/D6/D7 |
| `plaene/klingel_plan.py` | erzeugt den Schaltplan (matplotlib); schreibt nach `doku/klingel_plan.svg` relativ zum Arbeitsverzeichnis – Pfad bei Bedarf anpassen |
| `plaene/klingel-schaltplan-farbig.pdf` | *historisch:* Druckblatt A4 quer: Schaltplan mit Litzenfarben, Farbschema und Kennfarben der Bauteile |
| `plaene/klingel_plan_druck.py` | erzeugt das farbige PDF; liest `klingel_plan.py` aus dem Arbeitsverzeichnis (also in `plaene/` ausführen) |
| `plaene/klingel-schaltplan-mosfet.pdf` | *historisch, verworfen:* Druckblatt A4 quer: Umbau auf 3 × 2N7000 + 3 × 1 MΩ, Messanleitung Polarität, Pinbelegung 2N7000 (12.10.) |
| `plaene/klingel-schaltplan-mosfet-vorschau.png` | Vorschau des MOSFET-Plans |
| `plaene/klingel_mosfet_plan.py` | erzeugt PDF und Vorschau (matplotlib); in `plaene/` ausführen |
| `plaene/klingel-messblatt-abzweigdose.pdf` | Messblatt A4 hoch für die Aderzuordnung (11.10.) – **beruht noch auf der Annahme „Trafo treibt Gong“ (V~)**, nur noch zur Nachvollziehbarkeit |
| `plaene/klingel_messblatt.py` | erzeugt das Messblatt (matplotlib); in `plaene/` ausführen |
| `gehaeuse/klingel-gehaeuse.scad` | OpenSCAD-Quelle des Gehäuses (`TEIL = "box"` / `"deckel"` / `"zusammen"` / `"schnitt"` / `"alle"`) |
| `gehaeuse/klingel_box.stl` | Box, druckfertig |
| `gehaeuse/klingel_deckel.stl` | Deckel, druckfertig (liegt mit der Platte nach unten) |
| `.gitignore` | schließt echte Secrets, `.esphome/`, Sicherungskopien aus |
