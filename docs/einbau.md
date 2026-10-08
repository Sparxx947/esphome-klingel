🇬🇧 [English version](einbau.en.md)

# Aufbau, Inbetriebnahme, Einbau und Test

Reihenfolge: **A** Platine aufbauen → **B** Inbetriebnahme am Tisch → **C** Einbau an der Abzweigdose → **D** Abnahmetest
→ **E** Home Assistant. Voraussetzung ist die Aderzuordnung aus [einmessen.md](einmessen.md#1-adern-zuordnen).

---

## A. Platine aufbauen

Material: Minilötplatine 45 × 39 mm, 3 × PC817C, 3 × 1N4007, 3 × 1 kΩ, Anschlussleitungen. Schaltplan:
[`../plaene/klingel_plan.svg`](../plaene/klingel_plan.svg).

1. Bauteile prüfen (Diodentest, siehe [einmessen.md § 4](einmessen.md#4-bauteile-vor-dem-löten-prüfen)).
2. Drei Kanäle nebeneinander anordnen; links die Klingelseite (Etagenadern + Rückleiter), rechts die ESP-Seite
   (D5/D6/D7 + G). *(Anordnung ist ein Vorschlag – die Trennung von Klingel- und ESP-Seite ist der Sinn des Optokopplers.)*
3. Je Kanal:
   - Etagenader → **1 kΩ** → **Pin 1** des PC817
   - **1N4007** zwischen Pin 1 und Pin 2: **Strich (Kathode) an Pin 1**, Anode an Pin 2
   - **Pin 2** → gemeinsame Rückleiter-Schiene
   - **Pin 4** (Kollektor) → Ausgang Dx
   - **Pin 3** (Emitter) → gemeinsame G-Schiene
4. Ausgänge: Erdgeschoss → **D5**, Etage 1 → **D6**, Etage 2 → **D7**, G-Schiene → **G**.
   Keine externen Pull-ups – die Firmware nutzt `INPUT_PULLUP`.
5. **Nicht** D3, D4 oder D8 verwenden (Boot-Pins); D1 bleibt für ein mögliches Relais frei.
6. Nach dem Löten: Durchgang Klingelseite ↔ ESP-Seite messen → muss **unterbrochen** sein.
7. Klemmen/Leitungen beschriften (Etage, Rückleiter).

---

## B. Inbetriebnahme am Tisch

1. Echte Secrets bereitstellen (Vorlage `firmware/secrets.example.yaml`; echte Werte nur lokal bzw. im Builder).
2. **Vor dem ersten Flash:** Filter-Reihenfolge in `firmware/klingel.yaml` klären
   (siehe [fehlersuche.md Nr. 1](fehlersuche.md#1-gong-klingelt-aber-kein-ereignis-in-ha)).
3. D1 mini per USB an den PC, Port freigeben: `setfacl -m u:$USER:rw /dev/ttyUSB0`.
4. Flashen: `esphome run klingel.yaml --no-logs --device /dev/ttyUSB0` → „Successfully compiled“ muss im Log stehen.
   **Kein** `esphome upload` und **kein** Build mit Dummy-Secrets.
5. Gegenprobe: per API mit dem echten Schlüssel verbinden, Zustände lesen.
6. Home Assistant: ESPHome-Integration mit Host und Verschlüsselungsschlüssel hinzufügen; Entitätsnamen prüfen
   (erwartet `event.klingel_erdgeschoss`, `event.klingel_etage_1`, `event.klingel_etage_2`).
7. Router: feste IP für die MAC des D1 mini vergeben (Werkzeug `fb_feste_ip.py`, wie bei den anderen ESPs).
8. ESPHome Builder: Secrets ergänzen, „New device“ → überspringen → YAML einfügen, **nicht** installieren. Ab jetzt OTA.
9. Tischtest je Kanal mit 5 V über 1 kΩ (siehe [einmessen.md § 5](einmessen.md#5-tischtest-vor-dem-einbau-vorschlag)).

---

## C. Einbau an der Abzweigdose

| Ort | Was |
|---|---|
| Abzweigdose oben links über dem linken Verteiler | Abgriff der 3 Etagenadern + Rückleiter (nur Kleinspannung) |
| daneben | Platine + D1 mini (Gehäuse noch offen) |
| linker Verteiler, Reihe 5, Platz 49–52 („SNS016“) | Schuko-Steckdose für das USB-Netzteil |

1. **Sicherung des Klingeltrafos aus** (Trafo: rechter Verteiler, Reihe 3, Platz 25/26).
2. Je Etagenader und am Rückleiter eine zusätzliche Ader anklemmen (in die vorhandene Lüster-/WAGO-Klemme oder eine neue
   WAGO) – die bestehenden Verbindungen zu Gong und Tastern **nicht** auftrennen. *(Art der Klemmung nicht festgelegt.)*
3. Adern zur Platine führen, Etagen laut Messprotokoll an die richtigen Kanäle.
4. Neue Kreppband-Beschriftung anbringen.
5. USB-Netzteil in die Verteiler-Steckdose, D1 mini anschließen.
6. Sicherung des Klingeltrafos wieder ein.
7. Prüfen: Gong klingelt bei allen drei Knöpfen wie vorher (der Abgriff zieht nur ~10 mA zusätzlich).

---

## D. Abnahmetest

| # | Test | Erwartung |
|---|---|---|
| 1 | Knopf Erdgeschoss kurz drücken | Gong klingelt; in HA `event.klingel_erdgeschoss` mit `gedrueckt`; nur dieser Eingang |
| 2 | Knopf Etage 1 | nur `event.klingel_etage_1` |
| 3 | Knopf Etage 2 | nur `event.klingel_etage_2` |
| 4 | langer Druck (3 s) | **ein** Event, kein Flattern im Log |
| 5 | Sturmklingeln (mehrmals binnen 15 s) | eine Push-Meldung je Etage (nach Anlegen des HA-Pakets) |
| 6 | ESP-Neustart (Builder → Restart) | **kein** Event, keine Push-Meldung |
| 7 | WLAN-Signal ablesen | Wert notieren, siehe [einmessen.md § 7](einmessen.md#7-wlan-am-einbauort) |
| 8 | D1 stromlos | Gong klingelt trotzdem normal |

Vertauschte Etagen: entweder die Adern an der Platine tauschen oder die `substitutions` `taster_1..3` anpassen
(dann ändern sich die Entitätsnamen – HA-Paket mitziehen).

---

## E. Home Assistant

1. `ha/klingel.yaml` als Paket anlegen (Entitätsnamen gegen die tatsächlich adoptierten prüfen).
2. Test je Etage: Push geht an die richtigen Empfänger (EG → Bewohner EG; E1/E2 → Bewohner Etage 1/2), Bild der
   Haustürkamera dabei, alle drei Wandpanels wachen auf, zeigen die Übersicht und das Overlay.
3. Start-URL der Panels Etage 1 und Etage 2 prüfen.
4. Alexa: `binary_sensor.klingel_erdgeschoss/_etage_1/_etage_2` in `/config/alexa.yaml` aufnehmen, Gerätesuche,
   je Etage eine Routine mit Ankündigung.
