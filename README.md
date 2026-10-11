🇬🇧 [English version](README.en.md)

# Türklingel → Home Assistant (ESPHome, Wemos D1 mini)

Die vorhandene, klassische Klingelanlage im Haus bekommt einen „Mithörer“: Ein Wemos D1 mini erkennt über
drei Optokoppler, an **welcher Etage** jemand klingelt, und meldet das als `event` (device_class `doorbell`) an
Home Assistant. Der Gong klingelt **unverändert weiter** – der ESP greift nur Kleinspannung ab und schaltet nichts.

| | |
|---|---|
| Projektkürzel (Werkstattbuch) | **K1 Türklingel · 3 Etagen mithören** |
| Board | Wemos D1 mini V3.0.0 (ESP8266), „D1 #2“ aus dem Bestand |
| Erkennung | 3 × Optokoppler **PC817C** + je eine antiparallele Gegendiode **1N4007** + 1 kΩ Vorwiderstand |
| Abgriff | Abzweigdose oben links über dem linken Kleinverteiler im Treppenhaus (dort laufen **alle** Klingeladern zusammen, nur Kleinspannung) |
| Klingeltrafo | Hager ST303, 8 VA, PRI 230 V (Klemmen 1/7), SEC 8 V (2–4) / 12 V (2–8), rechter Verteiler, Reihe 3, Platz 25/26 |
| Stromversorgung D1 | USB-Netzteil an einer Schuko-Steckdose im linken Verteiler („SNS016“, Reihe 5, Platz 49–52) – **nicht** aus dem Klingeltrafo |
| Eingänge | Erdgeschoss → D5 (GPIO14) · Etage 1 → D6 (GPIO12) · Etage 2 → D7 (GPIO13) |
| HA-Reaktion | Push mit Kamerabild an die Bewohner der Etage, alle drei Wandpanels zeigen das Livebild der Haustür, Alexa-Ansage je Etage |

## Nachbauen

Hinweise für den Nachbau in einem anderen Haus:

- **Secrets:** `firmware/secrets.example.yaml` nach `secrets.yaml` kopieren (bzw. im ESPHome Builder anlegen) und
  WLAN-Name, WLAN-Passwort, API-Schlüssel und Hotspot-Passwort durch eigene Werte ersetzen.
- **HA-Paket:** In `ha/klingel.yaml` die Benachrichtigungsdienste `notify.mobile_app_handy_*` durch die eigenen
  Handy-Dienste ersetzen, ebenso die Entitäts-IDs der Kamera (`camera.haustuer_standardauflosung`) und der Wandpanels
  (`switch.wandpanel_*`, `button.wandpanel_*`, `notify.wandpanel_*`).
- **Klingeltrafo zuerst messen:** Die Gong-Spannung (hier 8 oder 12 V AC) vor dem Löten mit dem Multimeter bestimmen
  und Vorwiderstand und Gegendiode danach prüfen (siehe [docs/einmessen.md](docs/einmessen.md)).

## Prinzip

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

## Status (Stand 11.10.2026)

| Bereich | Stand | Datum |
|---|---|---|
| Firmware `klingel.yaml` (3 Taster, Events, Filter) | **fertig**, Filter-Reihenfolge korrigiert (`delayed_off: 200ms` vor `delayed_on: 230ms`) | 04.10. / 11.10. |
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
| Zuordnung Ader ↔ Etage in der Abzweigdose | **offen** – Messung am 10.10. hat nicht stattgefunden | – |
| Gong-Spannung (8 V oder 12 V) | **offen** | – |
| Feste IP | ✔ im Router fest vergeben | 11.10. |
| ESPHome Builder | als `klingel.yaml` angelegt, Secrets eingetragen, Gerät online ✔ | 11.10. |
| Adoption in HA | ✔ eingebunden: `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2`, `binary_sensor.klingel_*_gedruckt`, Status, WLAN-Signal, Laufzeit | 11.10. |
| Event `gedrueckt` erst nach dem OFF im Log | ✔ geklärt: In HA kommt das Event **beim Drücken** an (Test 11.10.: Event 49,818 s, Binärsensor EIN 49,922 s, AUS 53,588 s). Die Verzögerung war nur die Ausgabe des Log-Clients. ([Fehlersuche Nr. 16](docs/fehlersuche.md#16-event-erscheint-erst-nach-dem-off)) | 11.10. |
| HA-Paket `ha/klingel.yaml` | **Entwurf**, YAML geparst, Sperrlogik in HA getestet, **noch nicht in HA angelegt** | 04./06.10. |
| Gehäuse | **konstruiert** (`gehaeuse/`), gedruckt noch nicht bestätigt | 11.10. |

---

## Stückliste

| Teil | Menge | Bezeichnung / Typ | Bezugsquelle, ASIN, Preis | Status |
|---|---|---|---|---|
| Mikrocontroller | 1 | Wemos D1 mini V3.0.0 (ESP8266), „D1 #2“ | Bestand (4 × vorhanden) | vorhanden |
| Optokoppler | 3 (+ Reserve) | PC817C, DIP-4, 50 Stück (ALLECIN) | Amazon.de, **B0CBKK6T3D**, 7,99 € | geliefert 07.10. |
| Gegendiode | 3 | 1N4007 (alternativ 1N5819 – Erholzeit bei 50 Hz egal) aus Diodensortiment (BOJACK) | Amazon.de, **B07YK3XMQQ**, 10,99 € (gemeinsam mit Projekt Tankmessung) | geliefert 07.10. |
| Vorwiderstand | 3 | 1 kΩ, 0,25 W reicht (~10 mA, ~0,12 W) | Widerstandssortiment (AZ-Delivery) | vorhanden, verbaut 11.10. |
| Lochraster | 1 | Minilötplatine 45 × 39 mm (gemessen 44,12 × 38,74), 5 Stück – **einzelne Lötpunkte ohne Leiterbahnen** | Amazon.de, **B073FVX29X**, 5,19 € | geliefert 09.10., gelötet 11.10. |
| Netzteil | 1 | USB-Netzteil 5 V (Typ nicht festgelegt) für die Schuko-Steckdose im linken Verteiler | – | **ungeklärt** (Bestand?) |
| USB-Kabel | 1 | passend zum D1 mini, Länge Steckdose → Abzweigdose | – | **ungeklärt** |
| Leitungen Abzweigdose → Platine | 4 Adern (3 Etagenadern + Rückleiter) | Einzellitzen Ø 1,38 mm: grau = Gong-Rückleiter, gelb = Erdgeschoss, grün = Etage 1, blau = Etage 2; Verbindung in der Dose (Lüster/WAGO) | – | Farben festgelegt 11.10.; Klemmung in der Dose **nicht festgelegt** |
| Verbindungen Platine → D1 | 4 (D5, D6, D7, G) | gelb → D5, grün → D6, blau → D7, schwarz → G (Jumperkabel aus dem ELEGOO-Set M2M/F2M/F2F oder direkt gelötet) | Bestand | vorhanden |
| Gehäuse | 1 | Box + Deckel, `gehaeuse/klingel_box.stl` + `gehaeuse/klingel_deckel.stl` (PLA) + 4 Blechschrauben 3 × 12, Wandmontage 4 × Spax 4 | Eigendruck | konstruiert 11.10., Druck nicht bestätigt |
| Werkzeug | – | Multimeter (geliehen; eigenes UNI-T UT139C bestellt), Lötkolben | Bestand / bestellt | vorhanden |
| *optional:* Relaismodul | 1 | für „Gong stumm“ an D1 (GPIO5), Öffner-Kontakt | – | nur Idee, auskommentiert |

**Nicht mehr nötig** (aus dem Trafo-Versorgungsentwurf vom 04.10.): Brückengleichrichter, Elko 1000 µF/35 V, Step-down-Modul,
1N5408-Dioden für den Dioden-Abgriff, Hutschienengehäuse, D1 mini Pro mit Außenantenne (Verteiler sind Kunststoff in einer
Holznische, kein Metallkasten).

---

## Pinbelegung und Verdrahtung

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
| D5 | GPIO14 | Erdgeschoss, `INPUT_PULLUP`, invertiert | `event.klingel_erdgeschoss` |
| D6 | GPIO12 | Etage 1, `INPUT_PULLUP`, invertiert | `event.klingel_etage_1` |
| D7 | GPIO13 | Etage 2, `INPUT_PULLUP`, invertiert | `event.klingel_etage_2` |
| G | – | gemeinsamer Emitter der 3 PC817 | |
| USB | – | Versorgung über USB-Netzteil | |
| D1 (GPIO5) | – | reserviert für optionales „Gong stumm“-Relais | |
| D3 / D4 / D8 | – | **nicht verwenden** (Boot-Pins) | |

Welche Ader in der Abzweigdose welche Etage ist, ist **noch nicht bekannt** → [docs/einmessen.md](docs/einmessen.md#1-adern-zuordnen).

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
| IP | **noch keine** – im Router fest vergeben (wie bei den anderen ESPs); nach dem Erstflash vom 11.10. noch offen |
| `substitutions` | `taster_1: Erdgeschoss`, `taster_2: Etage 1`, `taster_3: Etage 2` |
| Filter je Eingang | `delayed_off: 200ms`, **dann** `delayed_on: 230ms` (Anker `&klingelfilter`) – Reihenfolge seit 11.10. korrigiert, siehe Fehlersuche Nr. 1 |
| Logger | `INFO` |
| API | verschlüsselt (`!secret klingel_api_key`) |
| OTA | `platform: esphome` |
| Fallback-Hotspot | SSID `Klingel-Fallback`, Passwort `!secret klingel_ap_password`, mit Captive Portal |

### Entitäten in Home Assistant (nach Adoption – Namen dann prüfen)

| Entität (erwartet) | Typ | Bedeutung |
|---|---|---|
| `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2` | event, doorbell | Event-Typ `gedrueckt`; Zustand = Zeitstempel des letzten Drucks |
| `binary_sensor.klingel_erdgeschoss_gedruckt` usw. | binary_sensor | Rohzustand des Eingangs (gefiltert) |
| `binary_sensor.klingel_status` | status | ESP online |
| `sensor.klingel_wlan_signal` | Signal (dBm), alle 120 s | |
| `sensor.klingel_laufzeit` | Uptime, alle 600 s | |

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

**Kurzfassung der Reihenfolge:** Teile prüfen ✅ → Platine löten ✅ → Erstflash ✅ → Tischtest ✅ → Adern messen →
HA/Builder/feste IP → Gehäuse drucken → Einbau an der Abzweigdose → je Etage einmal klingeln → HA-Paket anlegen →
Alexa-Routinen.

**Sicherheit:** Vor dem Öffnen von Klemmen die Sicherung des Klingeltrafos ausschalten. In der Abzweigdose liegen laut
Sichtprüfung (Jens, 06.10.) nur Klingeladern. Die 230-V-Seite des Trafos gehört dem Elektriker.

---

## Home-Assistant-Anbindung

Datei: [`ha/klingel.yaml`](ha/klingel.yaml) – **Entwurf als HA-Paket, noch nicht in HA angelegt.**

| Baustein | Funktion |
|---|---|
| 3 Trigger-Template-`binary_sensor` „Klingel Erdgeschoss / Etage 1 / Etage 2“ (device_class `motion`, `auto_off: 60`) | Signal für je eine eigene **Alexa-Routine** pro Etage (Muster wie die 3D-Druck-Meldung) |
| Automation `klingel_haustuer_meldung` | Push mit Bild der Haustürkamera (`camera.haustuer_standardauflosung`, Reolink E1 Pro) und Etage im Titel |
| Empfänger | Erdgeschoss → Bewohner EG; Etage 1 / Etage 2 → Bewohner Etage 1/2 |
| Wandpanels | bei **jeder** Etage alle drei: Bildschirm an, Start-URL laden (Übersicht mit Livebild), Overlay-Text |
| Sturmklingel-Sperre | **15 s je Taster** (Abstand zum vorigen Zeitstempel desselben Events); in HA getestet: erster Druck (`unknown` → Zeit) meldet, 8 s danach nicht, 20 s danach wieder |
| Neustart-Schutz | `not_from: unavailable` – Wiederverbinden des ESP ist kein Druck; `unknown` wird bewusst **nicht** ausgeschlossen, sonst ginge der allererste Druck verloren |
| Modus | `parallel`, `max: 6` (zwei Etagen kurz nacheinander melden beide) |

Nach dem Anlegen in `/config/alexa.yaml` unter `filter.include_entities` die drei `binary_sensor.klingel_*` aufnehmen
(je `entity_config` mit Name und `display_categories: MOTION_SENSOR`), dann in der Alexa-App Geräte suchen und je Etage
eine Routine „Wenn Klingel <Etage> Bewegung erkennt → Ankündigung“ anlegen.

Weitere Nutzer der Events: Die geplante Automation „Klingel abends“ im Projekt Treppenlicht (L1) schaltet bei einem
Klingel-Ereignis das Treppenlicht ein, wenn es dunkel ist.

Vor dem Einbau prüfen: Start-URL der Panels Etage 1/2 (EZpad im EG startet nachweislich auf `/uebersicht`).

---

## Offene Punkte / nächste Schritte / Termine

| # | Punkt | Wer | Termin |
|---|---|---|---|
| 1 | Adern in der Abzweigdose messen und Etagen zuordnen (Multimeter V~) | Jens | **offen** (am 10.10. nicht erfolgt) |
| 2 | Kreppband-Beschriftung in der Dose lesen (Gegenprobe zur Messung) | Jens | mit 1 |
| 3 | Gong-Spannung feststellen: 8 V (Klemmen 2–4) oder 12 V (2–8) | Jens | mit 1 |
| 4 | 1 kΩ-Widerstände | – | ✅ vorhanden, verbaut 11.10. |
| 5 | Minilötplatinen-Lieferung | – | ✅ geliefert 09.10. |
| 6 | **Filter-Reihenfolge** in `klingel.yaml` (siehe Fehlersuche Nr. 1) | – | ✅ korrigiert 11.10., vor dem Erstflash |
| 7 | Kopfkommentare in `klingel.yaml` auf PC817 + USB-Versorgung aktualisieren | – | ✅ 11.10. |
| 8 | Schaltplan als PDF (PC817 + Gegendiode, mit Litzenfarben) | – | ✅ `plaene/klingel-schaltplan-farbig.pdf`, 11.10. |
| 9 | Platine löten, Tischtest, Erstflash | Jens/Claude | ✅ 11.10. |
| 9a | Feste IP vergeben | – | **offen** |
| 9b | ✅ Builder-Secrets `klingel_api_key` / `klingel_ap_password` ergänzt, HA-Adoption | – | erledigt 11.10. |
| 9c | ✅ Event-Verzögerung geprüft: in HA kommt das Event beim Drücken ([Fehlersuche Nr. 16](docs/fehlersuche.md#16-event-erscheint-erst-nach-dem-off)) | – | erledigt 11.10. |
| 10 | HA-Paket anlegen, Alexa (`alexa.yaml`, Routinen), Start-URL Panels E1/E2 prüfen | Claude/Jens | nach Adoption |
| 11 | WLAN-Signal am Einbauort prüfen | – | nach Einbau |
| 12 | Gehäuse konstruieren | – | ✅ 11.10. (`gehaeuse/`) |
| 12a | Gehäuse drucken | – | **offen** |
| 12b | Einbau an der Abzweigdose und Abnahmetest ([einbau.md](docs/einbau.md) C/D) | – | nach 1–3 und 12a |
| 13 | optional: Relais „Gong stumm“ | – | später, nicht beauftragt |

---

## Dateien im Repo

| Pfad | Inhalt |
|---|---|
| `README.md` | diese Übersicht |
| `docs/einmessen.md` | Einmessen / Kalibrieren |
| `docs/einbau.md` | Aufbau, Inbetriebnahme, Einbau, Test |
| `docs/fehlersuche.md` | Fehlerbilder |
| `docs/verlauf.md` | Projektverlauf und verworfene Varianten |
| `firmware/klingel.yaml` | ESPHome-Konfiguration (D1 mini, 3 Eingänge, 3 Events) |
| `firmware/secrets.example.yaml` | Vorlage für die Secrets (ohne echte Werte) |
| `ha/klingel.yaml` | HA-Paket-Entwurf (Trigger-Templates für Alexa, Push-/Panel-Automation) |
| `plaene/klingel_plan.svg` | Schaltplan je Etage: 1 kΩ, PC817, 1N4007, Ausgänge D5/D6/D7 |
| `plaene/klingel_plan.py` | erzeugt den Schaltplan (matplotlib); schreibt nach `doku/klingel_plan.svg` relativ zum Arbeitsverzeichnis – Pfad bei Bedarf anpassen |
| `plaene/klingel-schaltplan-farbig.pdf` | Druckblatt A4 quer: Schaltplan mit Litzenfarben, Farbschema und Kennfarben der Bauteile |
| `plaene/klingel_plan_druck.py` | erzeugt das farbige PDF; liest `klingel_plan.py` aus dem Arbeitsverzeichnis (also in `plaene/` ausführen) |
| `gehaeuse/klingel-gehaeuse.scad` | OpenSCAD-Quelle des Gehäuses (`TEIL = "box"` / `"deckel"` / `"zusammen"` / `"schnitt"` / `"alle"`) |
| `gehaeuse/klingel_box.stl` | Box, druckfertig |
| `gehaeuse/klingel_deckel.stl` | Deckel, druckfertig (liegt mit der Platte nach unten) |
| `.gitignore` | schließt echte Secrets, `.esphome/`, Sicherungskopien aus |
