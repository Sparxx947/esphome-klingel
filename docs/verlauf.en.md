🇩🇪 [Deutsche Version](verlauf.md)

# Project history and decisions

| Date | Step | Result / decision |
|---|---|---|
| 04.10.2026 | Starting point | There was no doorbell entity in HA. First draft: **one** PC814 parallel to the chime via 1 kΩ 0.5 W on D5, event "Haustür" (front door); optional "chime mute" relay on D1 (normally closed, so the chime keeps ringing if the ESP fails). Compiled with ESPHome 2026.9.1: RAM 38.4 %, flash 40.2 %. |
| 04.10. evening | Jens: conventional system, **3 buttons**, no socket at the chime | 3 × PC814 on D5/D6/D7, one `event` each; power planned from the bell transformer (bridge rectifier + 1000 µF + step-down to 5.0 V). Recompiled: RAM 39.0 %, flash 40.3 %. |
| 04.10. late | Buttons = ground floor / floor 1 / floor 2; transformer in the stairwell distribution board | `substitutions` set; HA draft: 3 trigger templates for Alexa, automation `parallel`, lockout 15 s **per button** (tested). Two bugs of the first draft fixed (`not_from: unknown`, global lockout). Idea "everything at the transformer" with diode tap (2+2 anti-parallel 1N5408 in series with the return line, PC817/814 + ~47 Ω in parallel) – untested, since discarded. |
| 04.10. evening | paused | Jens: "remember it, we'll continue later". |
| 06.10. | Board inventory | Second D1 mini in stock → "D1 #2" for the doorbell, no new board needed. |
| 06.10. | Photos of distribution board | Plastic small distribution boards in a wooden recess (no metal → normal D1 mini). Transformer **Hager ST303, 8 VA**, 8 V (2–4) / 12 V (2–8). **Decision: do not power the D1 from the transformer** (8 VA for chime + ESP peaks ~350 mA too tight) → USB power supply at the distribution board socket. Next to it a Finder 14.01 (stair light, separate project). |
| 06.10. | Junction box | Jens: top left, **every** doorbell line runs through a junction box → tap point. Photos: doorbell wires only, the supposed paper is old masking-tape labelling. Assignment from photos not possible → measurement with multimeter. |
| 06.10. | Recipients | GF → residents ground floor, floor 1/2 → residents floors 1/2; wall panels for every floor. |
| 06.10. ~21:00 | Parts | PC814 not available on Amazon.de before 15.10. → **PC817C** + anti-parallel reverse diode (1N4007/1N5819 from the diode assortment). Series resistor 1 kΩ / 0.25 W. Perfboard: mini solder boards 45 × 39 mm. Both ordered by Jens. |
| 06.10. | Workshop book | Section K1 with schematic PC817 + 1N4007 (stripe to pin 1). |
| 07.10. | Delivery | PC817C and diode assortment arrived (confirmed by Jens on 08.10.). |
| 09.10. | Delivery | Mini solder boards arrived → parts complete (PC817C, diodes, boards). Wire measurement moved to Sat 10.10. |
| 10.10. (planned) | Measure wires | **Did not take place** – assignment of the wires in the junction box still open. |
| 11.10. | Firmware filter | Order corrected before the first flash: `delayed_off: 200ms` **first**, then `delayed_on: 230ms` (200 + 30 ms, because `delayed_off` also extends spikes by 200 ms). With PC817 + reverse diode the input at 50 Hz is ON for only ~10 ms per 20 ms – `delayed_on` first would have discarded every press. Header comments updated to PC817 + USB supply. |
| 11.10. | Colour schematic | Print sheet A4 landscape with wire colours: `plaene/klingel-schaltplan-farbig.pdf`. Doorbell side grey = chime return, yellow = ground floor, green = floor 1, blue = floor 2; ESP side yellow → D5, green → D6, blue → D7, black → G; no red (reserved for +5 V). |
| 11.10. | Enclosure | Designed in OpenSCAD (`gehaeuse/klingel-gehaeuse.scad`, parts `box`/`deckel`) and adapted to the measured dimensions (perfboard 44.12 × 38.74, D1 34.2 × 25.6, D1 height 25 mm, USB overmould 10.8 × 7.2, wires 4 × Ø 1.38). First version: openings ended blind because `hull()` with corner bosses on the outside thickened all walls to 6.5 mm → screw columns moved inside. Test print of an earlier version: perfboard fits. Printing of the current version not yet confirmed. |
| 11.10. | Board soldered | The mini solder board has **individual pads without tracks**. During the first soldering the connections reverse diode ↔ pin 1/pin 2, resistor ↔ pin 1 and pin 2 ↔ return conductor were therefore missing. After re-soldering, per channel (all 3 identical): diode test + on pin 1 → pin 2 = 1.08 V (LED), + on pin 2 → pin 1 = 0.60 V (1N4007); doorbell side ↔ ESP side no continuity. 1 kΩ resistors from stock fitted. |
| 11.10. | First flash | Locally via USB with the real secrets (ESPHome 2026.9.1): RAM 39.0 %, flash 40.3 %. Wi-Fi connected, API handshake with the real key ok. Created in the ESPHome Builder as `klingel.yaml`; Builder secrets, HA adoption and static IP open. |
| 11.10. | Bench test | An 18650 shield (power-bank board) as source gave **no** detection (presumably it does not switch its output on at ~8 mA load; not investigated further). With a bare 18650 cell (minus to grey, plus for 2–3 s to the colour) **passed**: blue → only "Etage 2", yellow → only "Erdgeschoss", green → only "Etage 1", several times each, event `gedrueckt` every time, no crosstalk. |
| 11.10. | Anomaly | In the `esphome logs` client the event `gedrueckt` arrived ~0.13–0.21 s **after** the OFF of the binary sensor each time, never at the ON (example: ON 44.26 s, OFF 49.84 s, event 50.05 s). Unexplained, check after HA adoption (see [troubleshooting no. 16](fehlersuche.en.md#16-event-appears-only-after-the-off)). |
| 11.10. | HA adoption | Builder secrets added, ESPHome integration adopted in HA (entities `event.klingel_erdgeschoss`/`_etage_1`/`_etage_2`, `binary_sensor.klingel_*_gedruckt`), static IP in the router. Event timing checked in HA: event 49.818 s before binary sensor ON 49.922 s (OFF 53.588 s) → the anomaly in the log client is **not a fault**. Enclosure printing. |

## Discarded variants

| Variant | Reason |
|---|---|
| Power from the bell transformer (rectifier, electrolytic capacitor, step-down) | Hager ST303 has only 8 VA; socket available in the distribution board |
| Tap directly at the transformer via diodes in the return line | junction box offers all floors in one place, without intervening in the distribution board |
| DIN-rail enclosure in the distribution board | tap no longer in the distribution board |
| D1 mini Pro with external antenna | no metal cabinet; only if RSSI at the installation site is poor |
| PC814 | not available at short notice |
| Powering the bench test via an 18650 shield (power-bank board) | no detection (load cut-off suspected) → bare cell or lab power supply |
| Bench test with 5 V from the D1 mini (suggestion from `einmessen.md`) | G on the D1 is occupied, isolation doorbell/ESP side would not be preserved → separate battery |
