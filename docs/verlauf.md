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
| 09.10. (geplant) | | Minilötplatinen; 18:30 Adern in der Abzweigdose messen. |

## Verworfene Varianten

| Variante | Grund |
|---|---|
| Versorgung aus dem Klingeltrafo (Gleichrichter, Elko, Step-down) | Hager ST303 hat nur 8 VA; Steckdose im Verteiler vorhanden |
| Abgriff direkt am Trafo über Dioden in der Rückleitung | Abzweigdose bietet alle Etagen an einer Stelle, ohne Eingriff in den Verteiler |
| Hutschienengehäuse im Verteiler | Abgriff nicht mehr im Verteiler |
| D1 mini Pro mit Außenantenne | kein Metallkasten; nur falls RSSI am Einbauort schlecht |
| PC814 | nicht kurzfristig lieferbar |
