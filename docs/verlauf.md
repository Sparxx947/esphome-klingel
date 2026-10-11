🇬🇧 [English version](verlauf.en.md)

# Projektverlauf und Entscheidungen

| Datum | Schritt | Ergebnis / Entscheidung |
|---|---|---|
| 04.10.2026 | Ausgangslage | In HA gab es keine Klingel-Entität. Erster Entwurf: **ein** PC814 parallel zum Gong über 1 kΩ 0,5 W an D5, Event „Haustür“; optional Relais „Gong stumm“ an D1 (Öffner, damit der Gong bei ESP-Ausfall weiter klingelt). Kompiliert mit ESPHome 2026.9.1: RAM 38,4 %, Flash 40,2 %. |
| 04.10. abends | Jens: klassische Anlage, **3 Taster**, keine Steckdose am Gong | 3 × PC814 an D5/D6/D7, je ein `event`; Versorgung aus dem Klingeltrafo geplant (Brückengleichrichter + 1000 µF + Step-down auf 5,0 V). Neu kompiliert: RAM 39,0 %, Flash 40,3 %. |
| 04.10. spät | Taster = Erdgeschoss / Etage 1 / Etage 2; Trafo im Verteiler Treppenhaus | `substitutions` gesetzt; HA-Entwurf: 3 Trigger-Templates für Alexa, Automation `parallel`, Sperre 15 s **je Taster** (getestet). Zwei Fehler des ersten Entwurfs behoben (`not_from: unknown`, globale Sperre). Idee „alles am Trafo“ mit Dioden-Abgriff (2+2 antiparallele 1N5408 in Reihe zur Rückleitung, PC817/814 + ~47 Ω parallel) – ungetestet, inzwischen verworfen. |
| 04.10. abends | pausiert | Jens: „merken, machen wir später weiter“. |
| 06.10. | Board-Inventur | Zweiter D1 mini im Bestand → „D1 #2“ für die Klingel, kein neues Board nötig. |
| 06.10. | Fotos Verteiler | Kunststoff-Kleinverteiler in Holznische (kein Metall → normaler D1 mini). Trafo **Hager ST303, 8 VA**, 8 V (2–4) / 12 V (2–8). **Entscheidung: D1 nicht aus dem Trafo versorgen** (8 VA für Gong + ESP-Spitzen ~350 mA zu knapp) → USB-Netzteil an der Verteiler-Steckdose. Daneben Finder 14.01 (Treppenlicht, eigenes Projekt). |
| 06.10. | Abzweigdose | Jens: oben links läuft **jede** Klingelleitung durch eine Abzweigdose → Abgriffpunkt. Fotos: nur Klingeladern, das vermeintliche Papier ist alte Kreppband-Beschriftung. Zuordnung aus Fotos nicht möglich → Messung mit Multimeter. |
| 06.10. | Empfänger | EG → Bewohner EG, Etage 1/2 → Bewohner Etage 1/2; Wandpanels bei jeder Etage. |
| 06.10. ~21:00 | Teile | PC814 bei Amazon.de nicht vor 15.10. lieferbar → **PC817C** + antiparallele Gegendiode (1N4007/1N5819 aus dem Diodensortiment). Vorwiderstand 1 kΩ / 0,25 W. Lochraster: Minilötplatinen 45 × 39 mm. Beides von Jens bestellt. |
| 06.10. | Werkstattbuch | Abschnitt K1 mit Schaltplan PC817 + 1N4007 (Strich an Pin 1). |
| 07.10. | Lieferung | PC817C und Diodensortiment da (von Jens am 08.10. bestätigt). |
| 09.10. | Lieferung | Minilötplatinen da → Teile komplett (PC817C, Dioden, Platinen). Adern-Messung auf Sa 10.10. verschoben. |
| 10.10. (geplant) | Adern messen | **Hat nicht stattgefunden** – Zuordnung der Adern in der Abzweigdose weiter offen. |
| 11.10. | Firmware-Filter | Reihenfolge vor dem Erstflash korrigiert: `delayed_off: 200ms` **zuerst**, dann `delayed_on: 230ms` (200 + 30 ms, weil `delayed_off` auch Störspitzen um 200 ms verlängert). Mit PC817 + Gegendiode ist der Eingang bei 50 Hz nur ~10 ms je 20 ms EIN – `delayed_on` zuerst hätte jeden Druck verworfen. Kopfkommentare auf PC817 + USB-Versorgung aktualisiert. |
| 11.10. | Schaltplan farbig | Druckblatt A4 quer mit Litzenfarben: `plaene/klingel-schaltplan-farbig.pdf`. Klingelseite grau = Gong-Rückleiter, gelb = Erdgeschoss, grün = Etage 1, blau = Etage 2; ESP-Seite gelb → D5, grün → D6, blau → D7, schwarz → G; kein Rot (bleibt für +5 V). |
| 11.10. | Gehäuse | In OpenSCAD konstruiert (`gehaeuse/klingel-gehaeuse.scad`, Teile `box`/`deckel`) und auf die gemessenen Maße angepasst (Lochraster 44,12 × 38,74, D1 34,2 × 25,6, Bauhöhe D1 25 mm, USB-Umspritzung 10,8 × 7,2, Litzen 4 × Ø 1,38). Erste Fassung: Durchbrüche endeten blind, weil `hull()` mit außen liegenden Eckdomen alle Wände auf 6,5 mm verdickte → Schraubsäulen nach innen. Testdruck einer früheren Fassung: Lochraster passt. Druck der aktuellen Fassung noch nicht bestätigt. |
| 11.10. | Platine gelötet | Die Minilötplatine hat **einzelne Lötpunkte ohne Leiterbahnen**. Beim ersten Löten fehlten deshalb die Verbindungen Gegendiode ↔ Pin 1/Pin 2, Widerstand ↔ Pin 1 und Pin 2 ↔ Rückleiter. Nach dem Nachlöten je Kanal (alle 3 gleich): Diodentest + an Pin 1 → Pin 2 = 1,08 V (LED), + an Pin 2 → Pin 1 = 0,60 V (1N4007); Klingelseite ↔ ESP-Seite kein Durchgang. 1 kΩ-Widerstände aus dem Bestand verbaut. |
| 11.10. | Erstflash | Per USB lokal mit echten Secrets (ESPHome 2026.9.1): RAM 39,0 %, Flash 40,3 %. WLAN verbunden, API-Handshake mit echtem Schlüssel ok. Im ESPHome Builder als `klingel.yaml` angelegt; Builder-Secrets, HA-Adoption und feste IP offen. |
| 11.10. | Tischtest | Ein 18650-Shield (Powerbank-Platine) als Quelle lieferte **keine** Erkennung (vermutlich schaltet es bei ~8 mA Last den Ausgang nicht ein, nicht weiter untersucht). Mit einer nackten 18650-Zelle (Minus an grau, Plus 2–3 s an die Farbe) **bestanden**: blau → nur „Etage 2“, gelb → nur „Erdgeschoss“, grün → nur „Etage 1“, je mehrfach, jedes Mal Event `gedrueckt`, kein Übersprechen. |
| 11.10. | Auffälligkeit | Im `esphome logs`-Client kam das Event `gedrueckt` jeweils ~0,13–0,21 s **nach** dem OFF des Binärsensors an, nie beim ON (Beispiel: ON 44,26 s, OFF 49,84 s, Event 50,05 s). Ungeklärt, nach der HA-Adoption prüfen (siehe [Fehlersuche Nr. 16](fehlersuche.md#16-event-erscheint-erst-nach-dem-off)). |

## Verworfene Varianten

| Variante | Grund |
|---|---|
| Versorgung aus dem Klingeltrafo (Gleichrichter, Elko, Step-down) | Hager ST303 hat nur 8 VA; Steckdose im Verteiler vorhanden |
| Abgriff direkt am Trafo über Dioden in der Rückleitung | Abzweigdose bietet alle Etagen an einer Stelle, ohne Eingriff in den Verteiler |
| Hutschienengehäuse im Verteiler | Abgriff nicht mehr im Verteiler |
| D1 mini Pro mit Außenantenne | kein Metallkasten; nur falls RSSI am Einbauort schlecht |
| PC814 | nicht kurzfristig lieferbar |
| Versorgung des Tischtests über 18650-Shield (Powerbank-Platine) | keine Erkennung (Lastabschaltung vermutet) → nackte Zelle oder Labornetzteil |
| Tischtest mit 5 V vom D1 mini (Vorschlag aus `einmessen.md`) | G am D1 ist belegt, die Trennung Klingel-/ESP-Seite bliebe nicht erhalten → separate Batterie |
