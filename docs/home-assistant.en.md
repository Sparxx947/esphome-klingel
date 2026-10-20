# Home Assistant integration

[Deutsche Version](home-assistant.md)

As of 20.10.2026 – **in operation**, acceptance test on 20.10. at 17:03.

Three building blocks, all created through the HA UI (no YAML package):

| File | In HA | Purpose |
|---|---|---|
| [`ha/klingel-automation.yaml`](../ha/klingel-automation.yaml) | automation "Klingel: Handy benachrichtigen + Kamera aufs Etagen-Panel" | push to the phone, starts the script for that floor's panel |
| [`ha/klingel-kamera-skript.yaml`](../ha/klingel-kamera-skript.yaml) | `script.klingel_kamera_auf_panel` | wake the panel, show the live image, return to the start page |
| [`ha/klingel-kamera-dashboard.yaml`](../ha/klingel-kamera-dashboard.yaml) | dashboard `klingel-kamera` (not in the sidebar) | one `panel` view with the front-door live image filling the screen |

## What happens on a press

1. **Trigger:** `event.received` on `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2`, event type `gedrueckt`.
   The ESP reconnecting is not an event and triggers nothing.
2. **Push to the phone** (HA companion app):
   - title "🔔 Es klingelt – Erdgeschoss" (or Etage 1 / Etage 2), message with the time.
   - still image from the front-door camera via `/api/camera_proxy/camera.<haustuer>`.
   - `tag: klingel-<floor>` – one notification per floor; ringing again replaces it instead of stacking.
   - dedicated Android channel `Klingel` (own sound on the phone), `priority/importance: high`, `ttl: 0`.
   - `clickAction: /klingel-kamera/haustuer` – tapping opens the live image.
3. **Wall panel of that floor** (Fully Kiosk Browser, HA integration "Fully Kiosk"), only the panel of the floor
   where someone rang:
   1. screen on (`switch.*_bildschirm`)
   2. trigger motion (`button.*_bewegungsaktivitat_auslosen`) – ends the screensaver
   3. `fully_kiosk.load_url` → `/klingel-kamera/haustuer`
   4. wait 90 s
   5. load start URL (`button.*_start_url_laden`) – the panel returns to its normal dashboard

   If a panel is offline this part is skipped; the push still goes out.

The automation starts the script with `script.turn_on`, so it does not wait for the 90 s. Both run in `parallel`
mode so two floors in quick succession are both served.

## Rebuilding

The three files contain placeholders in angle brackets:

| Placeholder | replace with |
|---|---|
| `notify.mobile_app_<dein_handy>` | your own companion-app notify service |
| `camera.<haustuer>` | your front-door camera (with stream support for the live view) |
| `<panel_device_id_eg/e1/e2>` | `device_id` of the Fully Kiosk device (`fully_kiosk.load_url` requires it; shown in the address bar of the device page) |
| `*.wandpanel_eg_* / _e1_ / _e2_` | Fully Kiosk integration entities per panel |
| `<home-assistant-host>` | address the panels use to open HA |

If the panels run with their own restricted HA user, they need access to the `klingel-kamera` dashboard (not
"admin only").

## Acceptance 20.10.2026

| Doorbell | pressed | panel shows `klingel-kamera` | back to start page |
|---|---|---|---|
| Ground floor | 17:03:09 | panel ground floor | 17:04:42 |
| Floor 1 | 17:03:16 | panel floor 1 | 17:04:48 |

Push with image arrived on the phone. Floor 2: event verified in the firmware acceptance test; that panel had no
power at the time (camera display there not yet verified).

## Pitfalls

- **Fully's screenshot shows a live camera card empty** – the live image cannot be proven that way. Use the
  integration's "current page" sensor (updates only about every 30 s) or look at the panel.
- **Cameras with a single RTSP session** (e.g. some Tapo models): put go2rtc in front, otherwise panels, the camera
  app and HA push each other out.

## Not implemented (ideas from the old draft)

The draft of 04.10. lives in [`ha/historisch/`](../ha/historisch/klingel-entwurf-20261004.yaml): Alexa announcement per
floor via trigger-template binary sensors, recipients per floor, repeated-ringing lockout (15 s per button). None of
this is currently set up in HA.
