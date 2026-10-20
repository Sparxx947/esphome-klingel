# Home-Assistant-Anbindung

[English version](home-assistant.en.md)

Stand 20.10.2026 – **in Betrieb**, Abnahme am 20.10. um 17:03.

Drei Bausteine, alle über die HA-Oberfläche angelegt (kein YAML-Paket):

| Datei | In HA | Aufgabe |
|---|---|---|
| [`ha/klingel-automation.yaml`](../ha/klingel-automation.yaml) | Automation „Klingel: Handy benachrichtigen + Kamera aufs Etagen-Panel“ | Push aufs Handy, startet das Skript für das Panel der Etage |
| [`ha/klingel-kamera-skript.yaml`](../ha/klingel-kamera-skript.yaml) | `script.klingel_kamera_auf_panel` | Panel wecken, Livebild zeigen, zurück zur Startseite |
| [`ha/klingel-kamera-dashboard.yaml`](../ha/klingel-kamera-dashboard.yaml) | Dashboard `klingel-kamera` (nicht in der Seitenleiste) | eine `panel`-Ansicht mit dem Livebild der Haustür über die ganze Fläche |

## Ablauf bei einem Druck

1. **Auslöser:** `event.received` auf `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2`, Ereignistyp
   `gedrueckt`. Ein Wiederverbinden des ESP ist kein Ereignis und löst nichts aus.
2. **Push aufs Handy** (HA-Companion-App):
   - Titel „🔔 Es klingelt – Erdgeschoss“ (bzw. Etage 1 / Etage 2), Text mit Uhrzeit.
   - Standbild der Haustürkamera über `/api/camera_proxy/camera.<haustuer>`.
   - `tag: klingel-<etage>` – je Etage eine Meldung; klingelt es dort erneut, wird sie ersetzt statt gestapelt.
   - eigener Android-Kanal `Klingel` (Ton am Handy separat einstellbar), `priority/importance: high`, `ttl: 0`.
   - `clickAction: /klingel-kamera/haustuer` – Antippen öffnet das Livebild.
3. **Wandpanel der Etage** (Fully Kiosk Browser, HA-Integration „Fully Kiosk“), nur das Panel der Etage, auf der
   geklingelt wurde:
   1. Bildschirm an (`switch.*_bildschirm`)
   2. Bewegung auslösen (`button.*_bewegungsaktivitat_auslosen`) – beendet den Bildschirmschoner
   3. `fully_kiosk.load_url` → `/klingel-kamera/haustuer`
   4. 90 s warten
   5. Start-URL laden (`button.*_start_url_laden`) – das Panel kehrt zu seinem normalen Dashboard zurück

   Ist ein Panel offline, wird dieser Teil übersprungen; der Push kommt trotzdem.

Die Automation startet das Skript mit `script.turn_on`, wartet also die 90 s nicht ab. Beide laufen im Modus
`parallel`, damit zwei Etagen kurz nacheinander beide bedient werden.

## Nachbauen

In den drei Dateien stehen Platzhalter in spitzen Klammern:

| Platzhalter | ersetzen durch |
|---|---|
| `notify.mobile_app_<dein_handy>` | eigener Handy-Dienst der Companion-App |
| `camera.<haustuer>` | eigene Haustürkamera (für die Live-Ansicht mit Stream-Unterstützung) |
| `<panel_device_id_eg/e1/e2>` | `device_id` des Fully-Kiosk-Geräts (`fully_kiosk.load_url` verlangt sie; steht in der Adresszeile der Geräteseite) |
| `*.wandpanel_eg_* / _e1_ / _e2_` | Entitäten der Fully-Kiosk-Integration je Panel |
| `<home-assistant-host>` | Adresse, unter der die Panels HA öffnen |

Die Panels brauchen Zugriff auf das Dashboard `klingel-kamera` (nicht „nur Administratoren“), wenn sie mit einem
eigenen, eingeschränkten HA-Benutzer laufen.

## Abnahme 20.10.2026

| Klingel | gedrückt | Panel zeigt `klingel-kamera` | zurück zur Startseite |
|---|---|---|---|
| Erdgeschoss | 17:03:09 | Panel EG | 17:04:42 |
| Etage 1 | 17:03:16 | Panel Etage 1 | 17:04:48 |

Push mit Bild auf dem Handy angekommen. Etage 2: Push geprüft über die Firmware-Abnahme, das Panel dort war zu dem
Zeitpunkt ohne Strom (Kameraanzeige dort noch nicht abgenommen).

## Fallen

- **Fullys Bildschirmfoto zeigt eine Live-Kamerakarte leer** – das Livebild lässt sich so nicht nachweisen. Beleg
  über den Sensor „Aktuelle Seite“ der Fully-Integration (aktualisiert nur etwa alle 30 s) oder per Augenschein.
- **Kameras mit nur einer RTSP-Sitzung** (z. B. manche Tapo-Modelle): go2rtc davorschalten, sonst verdrängen sich
  Panels, Kamera-App und HA gegenseitig.

## Nicht umgesetzt (Ideen aus dem alten Entwurf)

Der Entwurf vom 04.10. liegt unter [`ha/historisch/`](../ha/historisch/klingel-entwurf-20261004.yaml): Alexa-Ansage
je Etage über Trigger-Template-Binärsensoren, Empfänger je Etage, Sturmklingel-Sperre (15 s je Taster). Nichts davon
ist derzeit in HA angelegt.
