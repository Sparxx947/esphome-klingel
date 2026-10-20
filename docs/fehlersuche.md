🇬🇧 [English version](fehlersuche.en.md)

# Fehlersuche

Kennzeichnung: **belegt** = in den Projektnotizen/anderen ESP-Projekten tatsächlich aufgetreten bzw. in HA getestet;
**abgeleitet** = aus Schaltung oder Konfiguration geschlossen, am Klingel-Gerät noch nicht beobachtet.

| # | Fehlerbild | Ursache | Lösung | Herkunft |
|---|---|---|---|---|
| 1 | Gong klingelt, aber kein Event in HA | Filter-Reihenfolge (siehe unten) | `delayed_off: 200ms` vor `delayed_on: 230ms` – **behoben 11.10.** vor dem Erstflash | abgeleitet, behoben |
| 2 | Kein Event, Eingang bleibt immer AUS | Gegendiode gleichsinnig zur LED gelötet → überbrückt die LED (0,7 V < 1,2 V) | Diode drehen: Strich an Pin 1 | abgeleitet |
| 3 | Kein Event, PC817 kaputt | Gegendiode fehlt → LED bekommt bis ~17 V Sperrspannung (verträgt ~6 V) | PC817 tauschen, Diode einsetzen | abgeleitet |
| 4 | Falsche Etage gemeldet | Ader falsch zugeordnet | Adern tauschen oder `substitutions` anpassen | abgeleitet |
| 5 | Eingang dauerhaft EIN | Kollektor/Emitter vertauscht oder Kurzschluss Ausgang–G | Pin 3 = Emitter → G, Pin 4 = Kollektor → Dx | abgeleitet |
| 6 | Event nach ESP-Neustart / WLAN-Abbruch | Zustandswechsel `unavailable` → alter Zeitstempel | `not_from: unavailable` (im Entwurf enthalten) | belegt (Entwurf) |
| 7 | Allererster Druck nach Einrichtung ohne Meldung | `not_from: unknown` im ersten Entwurf | `unknown` **nicht** ausschließen (behoben 04.10.) | belegt |
| 8 | Zweite Etage meldet nicht, wenn kurz nach der ersten geklingelt | globale Sperre im ersten Entwurf | Sperre je Taster, Modus `parallel` (behoben 04.10.) | belegt |
| 9 | Fallback-Hotspot nimmt das Passwort nicht | Prüf-Build mit Dummy-Secrets geflasht | mit echten Secrets `esphome run`, API-Gegenprobe | belegt (Heizungs-ESP 06.10.) |
| 10 | Zweiter Flash spielt alte Firmware | `esphome upload` übersetzt nicht neu | immer `esphome run`, auf „Successfully compiled“ achten | belegt |
| 11 | Flash bricht ab: „No more data to read“ | Board verträgt 460800 Baud nicht | `esptool … --baud 115200` mit `firmware.factory.bin` | belegt (anderes Board) |
| 12 | `/dev/ttyUSB0` nach Umstecken gesperrt | Port wird neu angelegt, ACL weg | `setfacl -m u:$USER:rw /dev/ttyUSB0` wiederholen | belegt |
| 13 | D1 bootet nicht / hängt beim Start | Eingang auf D3/D4/D8 (Boot-Pins) gelegt | nur D5/D6/D7 verwenden | abgeleitet (Pinwahl 04.10.) |
| 14 | Events verspätet / Gerät oft `unavailable` | schwaches WLAN am Verteiler | RSSI prüfen, Lage ändern, notfalls D1 mini Pro mit Außenantenne | abgeleitet |
| 15 | Push kommt bei einer Person nicht an | falscher `notify`-Dienst / App abgemeldet | Dienste in HA prüfen; `continue_on_error` sorgt dafür, dass die übrigen Aktionen weiterlaufen | abgeleitet |
| 16 | Event `gedrueckt` erscheint erst nach dem OFF des Binärsensors | nur Ausgabe des Log-Clients (siehe unten) | nichts – in HA kommt das Event beim Drücken | **geklärt** 11.10. |
| 17 | Kanal reagiert nicht, Diodentest zeigt „OL“ oder falsche Werte | Minilötplatine hat **einzelne Lötpunkte ohne Leiterbahnen** – Verbindung nicht hergestellt (11.10. fehlten Gegendiode ↔ Pin 1/Pin 2, Widerstand ↔ Pin 1, Pin 2 ↔ Rückleiter) | alle Verbindungen auf der Lötseite mit Draht/Zinnbrücke herstellen, je Kanal Diodentest (1,08 V / 0,60 V) | belegt (11.10.) |
| 18 | Tischtest: keine Erkennung mit 18650-Shield als Quelle | Shield (Powerbank-Platine) schaltet bei ~8 mA Last den Ausgang vermutlich nicht ein (nicht weiter untersucht) | nackte 18650-Zelle oder Labornetzteil nehmen | belegt (11.10.), Ursache vermutet |
| 19 | Messwerte ergeben keinen Sinn (z. B. negativer Wert „auf AC“, Ruhe 0 V / Druck 0,3 V) | Multimeter auf dem falschen Bereich (DC statt AC) | Bereich am bekannten Anker prüfen (Trafo 2–4 auf V~ = 8 V), siehe unten | **belegt** (12.10.) |
| 20 | Gong läutet normal, PC817-Abgriff erkennt nichts – an keinem Trafo-Pol | Gong ist ein **Batteriegong mit Kontakteingang**; der Trafo ist nicht im Gong-Kreis, durch die LED fließt nie Strom | Gong ansehen (Batterie? nur 2 Drähte?), DC an den Gong-Klemmen messen; Abgriff mit BC517 + 9,1 MΩ statt Optokoppler | **belegt** (12.10.), umgebaut 20.10. |
| 21 | Einzelne Treffer direkt nach dem Anklemmen, oft mehrere Etagen gleichzeitig | **Anklemmstöße**, kein Tastendruck | nicht als Funktionsnachweis werten; nach dem Anklemmen erst mehrere echte Drücke je Etage prüfen | **belegt** (12.10.) |
| 22 | Event kommt in HA an, `binary_sensor.klingel_*_gedruckt` zeigt dabei nie „on“ | beim PC817-Aufbau ungeklärt | mit BC517 nicht mehr aufgetreten: Event und Binärsensor kommen zusammen an | beobachtet (12.10.), **erledigt** 20.10. |
| 23 | BC517-Aufbau: alle Kanäle in Ruhe HIGH (alte Firmware: „aus“, neue: Dauer-„gedrückt“), kein Event | Basis bekommt keinen Strom (Polarität Kl.1/Kl.2 vertauscht, Brücke Ader → R → Basis fehlt), Emitter nicht an GND, BC517 gedreht – oder der Pin bleibt über der LOW-Schwelle | Messblatt `plaene/klingel-messblatt-bc517.pdf` und Durchgangsprüfung `plaene/klingel-durchgang-bc517.pdf` abarbeiten, siehe unten | **belegt** (20.10.), Ursache im Einzelnen nicht festgehalten |
| 24 | „Klingelbatterie leer“ meldet | ein Kanal länger als 30 s HIGH: Gong-Batterie leer, Ader lose oder Basisstrecke unterbrochen | Gong-Batterie und Spannung Kl.1 ↔ grau messen | abgeleitet (Sensor seit 20.10.) |

---

## 1. Gong klingelt, aber kein Ereignis in HA

**Stand: behoben am 11.10.2026 vor dem Erstflash.** Die Erklärung bleibt hier zur Nachvollziehbarkeit stehen. Am echten
Wechselspannungssignal ist die neue Reihenfolge noch nicht beobachtet (der Tischtest lief mit Gleichspannung) – das
zeigt erst der Abnahmetest.

Bis zum 11.10. standen die Filter in `firmware/klingel.yaml` in dieser Reihenfolge:

```yaml
filters: &klingelfilter
  - delayed_on: 30ms
  - delayed_off: 200ms
```

ESPHome wendet Filter **nacheinander** an. `delayed_on` wartet 30 ms und **verwirft** das ON, wenn vorher ein OFF
kommt. Mit PC817 + Gegendiode leitet die LED nur in der positiven Halbwelle – der Eingang ist pro 20-ms-Periode nur
etwa 8–10 ms an. Das ON überlebt die 30 ms dann nie, und `delayed_off` bekommt gar nichts zu glätten.

Der damalige Kommentar in der YAML („Nulldurchgänge überbrücken“) stammte aus der PC814-Planung (beide Halbwellen, nur kurze
Lücken um den Nulldurchgang); auch dort hängt es an der Abfallzeit des Fototransistors, ob die Lücken überbrückt werden.

**Prüfen:** Log auf `DEBUG`/`VERBOSE` (oder den Filter vorübergehend entfernen) und am Knopf drücken: Flattert der
Rohzustand im 10-ms-Takt?

**Umgesetzte Lösung (11.10.):**

```yaml
filters: &klingelfilter
  - delayed_off: 200ms    # erst Halbwellen-Lücken (≤ 10–20 ms) zu Dauer-EIN glätten
  - delayed_on: 230ms     # dann alles verwerfen, was vor der Glättung kürzer als ~30 ms war
```

`delayed_on` ist **230 ms** statt 30 ms: `delayed_off` verlängert jedes EIN um 200 ms – auch eine Störspitze. Mit
200 + 30 ms bleiben Spitzen unter 30 ms weiterhin verworfen; ein echter Druck meldet sich nach ~0,23 s.

Der Tischtest mit Gleichspannung deckt das ursprüngliche Problem **nicht** auf – erst der Test an der echten Anlage.

---

## 16. Event erscheint erst nach dem OFF

**Stand: geklärt (11.10.) – kein Fehler.** In Home Assistant kommt das Event beim Drücken an:

| Entität | Zeit (16:35) |
|---|---|
| `event.klingel_erdgeschoss` → `gedrueckt` | 49,818 s |
| `binary_sensor.klingel_erdgeschoss_gedruckt` EIN | 49,922 s |
| `binary_sensor.klingel_erdgeschoss_gedruckt` AUS | 53,588 s |

Die Verzögerung entstand nur in der Ausgabe des `esphome logs`-Clients. Die Automation kann auf das Event auslösen.

Ursprüngliche Beobachtung:

Beim Tischtest am 11.10. kam im `esphome logs`-Client das Event `gedrueckt` jeweils **~0,13–0,21 s nach dem OFF** des
Binärsensors an, nie beim ON. Beispiel:

| Zeile | Zeit |
|---|---|
| Binärsensor ON | 44,26 s |
| Binärsensor OFF | 49,84 s |
| Event `gedrueckt` | 50,05 s |

Was bekannt ist:

- Die `[S]`-Zeilen formatiert der Client (aioesphomeapi) **beim Empfang**; geräteseitig loggt `Event::trigger` nur auf
  `VERBOSE`. Die Zeitstempel zeigen also, wann der Client die Meldung bekam, nicht zwingend, wann das Gerät sie auslöste.
- `on_press` ist korrekt: der PressTrigger feuert bei `state = true`.

Geprüft wurde nach der HA-Adoption anhand der HA-Historie (Tabelle oben).

---

## 19. Messwerte ergeben keinen Sinn

**Belegt am 12.10.2026.** Beim Einbautest stand das Multimeter bei allen ersten Werten (0,3 V, −0,6 V, −0,634 V) auf
**DC**, obwohl Wechselspannung gemessen werden sollte. Daraus wurden zwei falsche Erklärungen abgeleitet (Gegendiode
klemmt den Abfragekreis; 0,6 V sei die Abfragespannung des Gongs). Aufgeklärt hat es erst der Gegencheck an einem
Punkt mit **bekannter** Spannung: Trafo Klemme 2–4 auf AC = 8 V.

| Anzeichen | Bedeutung |
|---|---|
| Minuszeichen bei vermeintlicher AC-Messung | Bereich ist DC – AC-Anzeigen haben kein Vorzeichen |
| Werte im Bereich weniger hundert Millivolt an einer „8–12-V-Anlage“ | Bereich oder Messpunkt falsch |
| Spannung **steigt** beim Drücken, statt auf ~0 zu fallen | gemessene Ader ist nicht die vom Taster geschaltete |

Zweite, schwerere Lehre: Vor dem Entwurf eines Abgriffs **das Gerät am anderen Ende ansehen** (Foto, Typenschild,
Batterie?). Die Annahme „der Trafo treibt den Gong“ war nie gemessen – siehe Nr. 20 und
[einmessen.md 0](einmessen.md#0-messbereich-und-gerät-am-anderen-ende-zuerst-prüfen).

---

## 23. BC517-Kanal leitet in Ruhe nicht

**Belegt am 20.10.2026** (erster Anschluss nach dem Umbau, alle drei Kanäle). Prüfreihenfolge:

| Schritt | Messung (Multimeter V⎓, schwarz zuerst genannt) | Soll | Wenn nicht |
|---|---|---|---|
| 0 | G → 3V3 am D1 | +3,2 … +3,4 V | Messbereich/Messleitungen prüfen – erst danach weiter |
| 1 | grau → Kl.1-Ader der Etage | **Plus**, Batteriespannung (hier 3,1 / 9,47 / 5,5 V) | negativ: Kl.1/Kl.2 vertauscht, Basis bekommt Minus |
| 2 | G → BC517 Mittelbein (Basis) | +0,9 … +1,4 V | ≈ 0 V: Ader → R → Basis offen; ≈ Wert aus 1: Emitter nicht an GND oder BC517 gedreht |
| 3 | G → Pin D5/D6/D7 in Ruhe | unter 0,8 V | 0,8–2,5 V: Grenzbereich (siehe unten); ≈ 3,3 V: Kollektor-Brücke fehlt |
| 4 | Durchgang G ↔ grau, G ↔ GND-Schiene, G ↔ jeder Emitter | piept | Brücke nachlöten |

**Grenzbereich (abgeleitet, nicht gemessen):** Ein Darlington hat eine Sättigungsspannung von ~0,6–0,9 V (die
Basis-Emitter-Spannung des zweiten Transistors bleibt stehen). Der ESP8266 erkennt LOW sicher erst unter ~0,25 × VDD
≈ 0,8 V. Liegt der Pin in Ruhe knapp darüber, liest der D1 „HIGH“. Abhilfe wäre ein einzelner NPN statt Darlington
(mehr Basisstrom nötig, also kleinerer Basiswiderstand) oder ein externer Pull-up mit größerem Strom.

**Messfalle 20.10.:** „G gegen Ader“ ergab −2 / −2 / −4 V, obwohl grau und G nachweislich verbunden waren und
„grau gegen Ader“ +3,1 / +9,47 / +5,5 V zeigte. Der Schluss „G schwebt“ war falsch; die Durchgangsprüfung hat ihn
widerlegt. Woher die Minuswerte kamen, ist ungeklärt. **Spannungen gegen den Rückleiter (grau) messen, nicht gegen G,
und Verbindungen per Durchgang belegen.**

---

## Gong wird leiser oder klingelt nicht mehr

Nicht erwartet: Die drei Abgriffe ziehen je ~10 mA, der Trafo liefert 8 VA (~1 A bei 8 V). Tritt es trotzdem auf:
Abgriff abklemmen und prüfen, ob beim Anklemmen eine bestehende Verbindung gelöst oder eine Ader falsch angeklemmt
wurde (z. B. Etagenader direkt auf den Rückleiter → Gong dauerhaft überbrückt bzw. Kurzschluss beim Drücken).

Bei den hier verbauten **Batteriegongs** gilt zusätzlich: Wer Plus und Minus einer Gong-Schleife verbindet (oder zwei
Plus-Adern), löst den Gong aus bzw. hält ihn ausgelöst – genau das, was der Taster tut.
