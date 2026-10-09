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
| 10.10. (planned) | | Measure the wires in the junction box and assign floors. |

## Discarded variants

| Variant | Reason |
|---|---|
| Power from the bell transformer (rectifier, electrolytic capacitor, step-down) | Hager ST303 has only 8 VA; socket available in the distribution board |
| Tap directly at the transformer via diodes in the return line | junction box offers all floors in one place, without intervening in the distribution board |
| DIN-rail enclosure in the distribution board | tap no longer in the distribution board |
| D1 mini Pro with external antenna | no metal cabinet; only if RSSI at the installation site is poor |
| PC814 | not available at short notice |
