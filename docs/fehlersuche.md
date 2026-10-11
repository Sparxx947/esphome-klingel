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
| 16 | Event `gedrueckt` erscheint erst nach dem OFF des Binärsensors | **ungeklärt** (siehe unten) | nach der HA-Adoption prüfen; Ausweg: Automation auf den Binärsensor EIN statt auf das Event | belegt (Log 11.10.), **offen** |
| 17 | Kanal reagiert nicht, Diodentest zeigt „OL“ oder falsche Werte | Minilötplatine hat **einzelne Lötpunkte ohne Leiterbahnen** – Verbindung nicht hergestellt (11.10. fehlten Gegendiode ↔ Pin 1/Pin 2, Widerstand ↔ Pin 1, Pin 2 ↔ Rückleiter) | alle Verbindungen auf der Lötseite mit Draht/Zinnbrücke herstellen, je Kanal Diodentest (1,08 V / 0,60 V) | belegt (11.10.) |
| 18 | Tischtest: keine Erkennung mit 18650-Shield als Quelle | Shield (Powerbank-Platine) schaltet bei ~8 mA Last den Ausgang vermutlich nicht ein (nicht weiter untersucht) | nackte 18650-Zelle oder Labornetzteil nehmen | belegt (11.10.), Ursache vermutet |

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

**Stand: offen, nicht geklärt.**

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

**Prüfen:** nach der HA-Adoption, wann `event.klingel_*` in HA tatsächlich seinen Zeitstempel bekommt.

**Ausweg, falls es sich bestätigt:** die Automation auf den Binärsensor **EIN** auslösen statt auf das Event.

---

## Gong wird leiser oder klingelt nicht mehr

Nicht erwartet: Die drei Abgriffe ziehen je ~10 mA, der Trafo liefert 8 VA (~1 A bei 8 V). Tritt es trotzdem auf:
Abgriff abklemmen und prüfen, ob beim Anklemmen eine bestehende Verbindung gelöst oder eine Ader falsch angeklemmt
wurde (z. B. Etagenader direkt auf den Rückleiter → Gong dauerhaft überbrückt bzw. Kurzschluss beim Drücken).
