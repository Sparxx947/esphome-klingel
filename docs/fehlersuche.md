🇬🇧 [English version](fehlersuche.en.md)

# Fehlersuche

Kennzeichnung: **belegt** = in den Projektnotizen/anderen ESP-Projekten tatsächlich aufgetreten bzw. in HA getestet;
**abgeleitet** = aus Schaltung oder Konfiguration geschlossen, am Klingel-Gerät noch nicht beobachtet.

| # | Fehlerbild | Ursache | Lösung | Herkunft |
|---|---|---|---|---|
| 1 | Gong klingelt, aber kein Event in HA | Filter-Reihenfolge (siehe unten) | `delayed_off` vor `delayed_on` | abgeleitet |
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

---

## 1. Gong klingelt, aber kein Ereignis in HA

**Stand: Verdacht, nicht am Gerät geprüft.**

In `firmware/klingel.yaml` stehen die Filter in dieser Reihenfolge:

```yaml
filters: &klingelfilter
  - delayed_on: 30ms
  - delayed_off: 200ms
```

ESPHome wendet Filter **nacheinander** an. `delayed_on` wartet 30 ms und **verwirft** das ON, wenn vorher ein OFF
kommt. Mit PC817 + Gegendiode leitet die LED nur in der positiven Halbwelle – der Eingang ist pro 20-ms-Periode nur
etwa 8–10 ms an. Das ON überlebt die 30 ms dann nie, und `delayed_off` bekommt gar nichts zu glätten.

Der Kommentar in der YAML („Nulldurchgänge überbrücken“) stammt aus der PC814-Planung (beide Halbwellen, nur kurze
Lücken um den Nulldurchgang); auch dort hängt es an der Abfallzeit des Fototransistors, ob die Lücken überbrückt werden.

**Prüfen:** Log auf `DEBUG`/`VERBOSE` (oder den Filter vorübergehend entfernen) und am Knopf drücken: Flattert der
Rohzustand im 10-ms-Takt?

**Lösung (Vorschlag):**

```yaml
filters: &klingelfilter
  - delayed_off: 200ms    # Halbwellen-Lücken (10 ms) zuerst überbrücken
  - delayed_on: 30ms      # dann kurze Störspitzen verwerfen
```

Alternativ `delayed_on` streichen oder auf wenige ms setzen. Der Tischtest mit Gleichspannung deckt das Problem **nicht**
auf – erst der Test an der echten Anlage.

---

## Gong wird leiser oder klingelt nicht mehr

Nicht erwartet: Die drei Abgriffe ziehen je ~10 mA, der Trafo liefert 8 VA (~1 A bei 8 V). Tritt es trotzdem auf:
Abgriff abklemmen und prüfen, ob beim Anklemmen eine bestehende Verbindung gelöst oder eine Ader falsch angeklemmt
wurde (z. B. Etagenader direkt auf den Rückleiter → Gong dauerhaft überbrückt bzw. Kurzschluss beim Drücken).
