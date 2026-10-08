🇩🇪 [Deutsche Version](README.md)

# Doorbell → Home Assistant (ESPHome, Wemos D1 mini)

The existing, conventional doorbell system in the house gets a "listener": a Wemos D1 mini uses three optocouplers to
detect **on which floor** someone is ringing and reports it as an `event` (device_class `doorbell`) to Home Assistant.
The chime keeps ringing **unchanged** – the ESP only taps extra-low voltage and switches nothing.

| | |
|---|---|
| Project code (workshop book) | **K1 Türklingel · 3 Etagen mithören** (doorbell · listen in on 3 floors) |
| Board | Wemos D1 mini V3.0.0 (ESP8266), "D1 #2" from stock |
| Detection | 3 × optocoupler **PC817C** + one anti-parallel reverse diode **1N4007** each + 1 kΩ series resistor |
| Tap point | Junction box top left above the left small distribution board in the stairwell (**all** doorbell wires meet there, extra-low voltage only) |
| Bell transformer | Hager ST303, 8 VA, PRI 230 V (terminals 1/7), SEC 8 V (2–4) / 12 V (2–8), right distribution board, row 3, slot 25/26 |
| D1 power supply | USB power supply in a Schuko socket in the left distribution board ("SNS016", row 5, slot 49–52) – **not** from the bell transformer |
| Inputs | Ground floor → D5 (GPIO14) · Floor 1 → D6 (GPIO12) · Floor 2 → D7 (GPIO13) |
| HA reaction | Push notification with camera snapshot to the residents of that floor, all three wall panels show the live image of the front door, Alexa announcement per floor |

## Rebuilding

Notes for rebuilding this in another house:

- **Secrets:** copy `firmware/secrets.example.yaml` to `secrets.yaml` (or create it in the ESPHome Builder) and
  replace Wi-Fi name, Wi-Fi password, API key and hotspot password with your own values.
- **HA package:** in `ha/klingel.yaml`, replace the notify services `notify.mobile_app_handy_*` with your own phone
  services, as well as the entity IDs of the camera (`camera.haustuer_standardauflosung`) and of the wall panels
  (`switch.wandpanel_*`, `button.wandpanel_*`, `notify.wandpanel_*`).
- **Measure the bell transformer first:** determine the chime voltage (here 8 or 12 V AC) with a multimeter before
  soldering, and check the series resistor and reverse diode against it (see [docs/einmessen.en.md](docs/einmessen.en.md)).

## Principle

When someone presses a doorbell button downstairs, the AC voltage of the bell transformer (8 or 12 V AC) appears at the
chime of that floor. The LED of a PC817 is connected in parallel to the chime (via 1 kΩ). The optocoupler galvanically
isolates the doorbell from the ESP; its transistor pulls the D1 mini's input (internal pull-up) to GND.

The PC817 has only **one** LED, which tolerates only about 6 V in reverse direction – the transformer delivers up to
~17 V peak. Therefore a **1N4007 is placed anti-parallel** to the LED and absorbs the negative half-wave. As a result
only **50 pulses per second** arrive at the input; the filter `delayed_off: 200ms` turns them into one continuous button
press. (But see the important note on **filter order** under [Troubleshooting](docs/fehlersuche.en.md#1-chime-rings-but-no-event-in-ha).)

> Originally the **PC814** was planned (two anti-parallel LEDs, designed for AC). On Amazon.de it was only available
> from 15.10.–18.11., hence PC817 + reverse diode. The comments at the top of `firmware/klingel.yaml` still describe
> the PC814/transformer state of 04.10. – the **code itself** fits both variants.

---

## Status (as of 08.10.2026)

| Area | Status | Date |
|---|---|---|
| Firmware `klingel.yaml` (3 buttons, events, filters) | **done**, compiled with ESPHome 2026.9.1 (RAM 39.0 %, flash 40.3 %) | 04.10. |
| Floor names / entities | **done** (`Erdgeschoss` / `Etage 1` / `Etage 2` – ground floor / floor 1 / floor 2) | 04.10. |
| Recipients per floor | **done** (GF → residents ground floor, floor 1/2 → residents floors 1/2) | 06.10. |
| Power concept | **decided**: USB power supply from the distribution board socket instead of the transformer | 06.10. |
| Tap point | **decided**: junction box top left (doorbell wires only, confirmed by Jens) | 06.10. |
| Schematic PC817 + reverse diode | **done** as SVG (`plaene/klingel_plan.svg`), PDF still missing | 06.10. |
| PC817C, diode assortment | **delivered** | 07.10. (confirmed by Jens on 08.10.) |
| Mini solder boards 45 × 39 mm | **ordered**, delivery announced | Fri 09.10. |
| 1 kΩ resistors | **open** – unclear whether included in the existing assortment | – |
| Mapping wire ↔ floor in the junction box | **open** – measurement planned | Fri 09.10. 18:30 |
| Chime voltage (8 V or 12 V) | **open** | – |
| Solder board, first flash, adoption in HA/Builder, static IP | **open** | – |
| HA package `ha/klingel.yaml` | **draft**, YAML parsed, lockout logic tested in HA, **not yet created in HA** | 04./06.10. |
| Enclosure | **open** – not yet designed | – |

---

## Bill of materials

| Part | Qty | Designation / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| Microcontroller | 1 | Wemos D1 mini V3.0.0 (ESP8266), "D1 #2" | stock (4 × available) | available |
| Optocoupler | 3 (+ spare) | PC817C, DIP-4, 50 pieces (ALLECIN) | Amazon.de, **B0CBKK6T3D**, €7.99 | delivered 07.10. |
| Reverse diode | 3 | 1N4007 (alternatively 1N5819 – recovery time irrelevant at 50 Hz) from diode assortment (BOJACK) | Amazon.de, **B07YK3XMQQ**, €10.99 (shared with the tank measurement project) | delivered 07.10. |
| Series resistor | 3 | 1 kΩ, 0.25 W is enough (~10 mA, ~0.12 W) | resistor assortment (AZ-Delivery) – **Jens checks whether 1 kΩ is included**; only 220 Ω and 10 kΩ are confirmed there | **open** |
| Perfboard | 1 | mini solder board 45 × 39 mm, 5 pieces | Amazon.de, **B073FVX29X**, €5.19 | ordered, delivery Fri 09.10. |
| Power supply | 1 | USB power supply 5 V (type not fixed) for the Schuko socket in the left distribution board | – | **unresolved** (in stock?) |
| USB cable | 1 | matching the D1 mini, length socket → junction box | – | **unresolved** |
| Wires junction box → board | 4 conductors (3 floor wires + return) | thin stranded wire / bell wire; connection in the box (terminal strip/WAGO) | – | **not fixed** |
| Connections board → D1 | 4 (D5, D6, D7, G) | jumper wires (ELEGOO set M2M/F2M/F2F) or soldered directly | stock | available |
| Enclosure | 1 | not yet designed (PETG/PLA from stock) | – | open |
| Tools | – | multimeter (borrowed; own UNI-T UT139C ordered), soldering iron | stock / ordered | available |
| *optional:* relay module | 1 | for "chime mute" on D1 (GPIO5), normally-closed contact | – | idea only, commented out |

**No longer needed** (from the transformer-supply draft of 04.10.): bridge rectifier, electrolytic capacitor 1000 µF/35 V,
step-down module, 1N5408 diodes for the diode tap, DIN-rail enclosure, D1 mini Pro with external antenna (the distribution
boards are plastic in a wooden recess, not a metal cabinet).

---

## Pin assignment and wiring

Schematic: [`plaene/klingel_plan.svg`](plaene/klingel_plan.svg) (generated by `plaene/klingel_plan.py`).
A PDF version is **not yet** in the repo (see [Open items](#open-items--next-steps--dates)).

### Per floor (3 × identical)

| From | Component | To | Note |
|---|---|---|---|
| Floor wire (determined by measurement) | 1 kΩ | PC817 **pin 1** (anode) | |
| PC817 **pin 2** (cathode) | – | chime return conductor (common) | all three pin 2 on one rail |
| 1N4007 **cathode (stripe)** | – | PC817 pin 1 | anti-parallel to the LED |
| 1N4007 **anode** | – | PC817 pin 2 | |
| PC817 **pin 4** (collector) | – | D1 mini Dx (see below) | internal pull-up, no external resistor |
| PC817 **pin 3** (emitter) | – | D1 mini **G** | all three emitters common |

### D1 mini

| D1 pin | GPIO | Function | Entity (expected) |
|---|---|---|---|
| D5 | GPIO14 | Ground floor, `INPUT_PULLUP`, inverted | `event.klingel_erdgeschoss` |
| D6 | GPIO12 | Floor 1, `INPUT_PULLUP`, inverted | `event.klingel_etage_1` |
| D7 | GPIO13 | Floor 2, `INPUT_PULLUP`, inverted | `event.klingel_etage_2` |
| G | – | common emitter of the 3 PC817 | |
| USB | – | power via USB power supply | |
| D1 (GPIO5) | – | reserved for optional "chime mute" relay | |
| D3 / D4 / D8 | – | **do not use** (boot pins) | |

Which wire in the junction box belongs to which floor is **not yet known** → [docs/einmessen.en.md](docs/einmessen.en.md#1-assigning-the-wires).

---

## Enclosure

**There is no enclosure for the doorbell yet** (no `gehaeuse/` folder, no SCAD/STL). The earlier plan of a DIN-rail
enclosure in the distribution board is obsolete now that the tap is at the junction box. What should apply when
designing it – taken over from the other ESP projects:

| Point | Requirement / lesson |
|---|---|
| Design | OpenSCAD, parametric (dimensions as variables at the top, part selected via `TEIL = "…"`) |
| Material | PLA is sufficient (indoors, no heat source); PETG is in stock |
| Printing | 0.2 mm layer, without supports (like the other enclosures) |
| Collisions | **Check before STL export**: don't place boards on continuous ledges, but on supports **between** the pin headers (pin headers run along the full board length); magnet pockets must not go through the floor. |
| Assembly | D1 mini + mini solder board 45 × 39 mm, route cables for doorbell wires and USB out separately |

Dimensions of the D1 mini and the finished perfboard are not fixed yet – measure only after soldering.

---

## Firmware

File: [`firmware/klingel.yaml`](firmware/klingel.yaml)

| Setting | Value |
|---|---|
| Device name / hostname | `klingel` (→ `klingel.local`) |
| Friendly name | `Klingel` (doorbell) |
| Board | `esp8266` / `d1_mini` |
| IP | **none yet** – assign a static one in the router after the first flash (as with the other ESPs) |
| `substitutions` | `taster_1: Erdgeschoss`, `taster_2: Etage 1`, `taster_3: Etage 2` (button 1: ground floor, button 2: floor 1, button 3: floor 2) |
| Filters per input | `delayed_on: 30ms`, `delayed_off: 200ms` (anchor `&klingelfilter`) – **check order**, see troubleshooting |
| Logger | `INFO` |
| API | encrypted (`!secret klingel_api_key`) |
| OTA | `platform: esphome` |
| Fallback hotspot | SSID `Klingel-Fallback`, password `!secret klingel_ap_password`, with captive portal |

### Entities in Home Assistant (after adoption – check names then)

| Entity (expected) | Type | Meaning |
|---|---|---|
| `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2` | event, doorbell | event type `gedrueckt` (pressed); state = timestamp of the last press |
| `binary_sensor.klingel_erdgeschoss_gedruckt` etc. | binary_sensor | raw state of the input (filtered) |
| `binary_sensor.klingel_status` | status | ESP online |
| `sensor.klingel_wlan_signal` | signal (dBm), every 120 s | |
| `sensor.klingel_laufzeit` | uptime, every 600 s | |

### Secrets

`firmware/secrets.example.yaml` is only the template (keys `wifi_ssid`, `wifi_password`, `klingel_api_key`,
`klingel_ap_password`). **Real values exist only in the ESPHome Builder** or locally in a file that is not checked in
(`.gitignore` excludes `secrets.yaml` and `secrets.*.yaml`). Generate an API key: `openssl rand -base64 32`.

### Flashing

1. **First flash via USB** with the **real** secrets:
   `esphome run klingel.yaml --no-logs --device /dev/ttyUSB0` – watch for "Successfully compiled".
   On Linux, grant access to the port first: `setfacl -m u:$USER:rw /dev/ttyUSB0` (again after every re-plug).
2. Cross-check via the API with the real key (read states).
3. In HA, add the ESPHome integration with host and encryption key; set a static IP in the router.
4. In the **ESPHome Builder**: add the secrets, "New device" → skip → paste YAML, do **not** install.
   From then on, updates **via OTA** from the Builder.

> **Pitfall:** Never flash a test build with dummy secrets (happened on 06.10. with the heating ESP: hotspot password
> and API key wrong). `esphome upload` does **not** recompile and blindly uploads the last build – for real firmware
> always use `esphome run`.

---

## Guides

| Document | Contents |
|---|---|
| [docs/einmessen.en.md](docs/einmessen.en.md) | Assigning wires, chime voltage, current/power calculation, checking components, bench test, filters, Wi-Fi |
| [docs/einbau.en.md](docs/einbau.en.md) | Building the board, commissioning, installation at the junction box, acceptance test |
| [docs/fehlersuche.en.md](docs/fehlersuche.en.md) | known and foreseeable failure patterns with cause and solution |
| [docs/verlauf.en.md](docs/verlauf.en.md) | decisions and discarded variants (PC814, transformer supply, diode tap) |

**Short version of the sequence:** check parts → measure wires (Fri 09.10.) → solder board → bench test → first flash →
HA/Builder/static IP → installation at the junction box → ring once per floor → create HA package → Alexa routines.

**Safety:** Before opening any terminals, switch off the circuit breaker of the bell transformer. According to a visual
inspection (Jens, 06.10.) the junction box contains only doorbell wires. The 230 V side of the transformer is the
electrician's job.

---

## Home Assistant integration

File: [`ha/klingel.yaml`](ha/klingel.yaml) – **draft as an HA package, not yet created in HA.**

| Building block | Function |
|---|---|
| 3 trigger-template `binary_sensor` "Klingel Erdgeschoss / Etage 1 / Etage 2" (doorbell ground floor / floor 1 / floor 2; device_class `motion`, `auto_off: 60`) | signal for a separate **Alexa routine** per floor (same pattern as the 3D-print notification) |
| Automation `klingel_haustuer_meldung` | push with image from the front-door camera (`camera.haustuer_standardauflosung`, Reolink E1 Pro) and the floor in the title |
| Recipients | Ground floor → residents ground floor; floor 1 / floor 2 → residents floors 1/2 |
| Wall panels | for **every** floor all three: screen on, load start URL (overview with live image), overlay text |
| Repeated-ringing lockout | **15 s per button** (interval to the previous timestamp of the same event); tested in HA: first press (`unknown` → time) notifies, 8 s later not, 20 s later again |
| Restart protection | `not_from: unavailable` – ESP reconnecting is not a press; `unknown` is deliberately **not** excluded, otherwise the very first press would be lost |
| Mode | `parallel`, `max: 6` (two floors in quick succession both notify) |

After creating it, add the three `binary_sensor.klingel_*` to `/config/alexa.yaml` under `filter.include_entities`
(each with `entity_config` containing a name and `display_categories: MOTION_SENSOR`), then discover devices in the Alexa
app and create one routine per floor "When Klingel <floor> detects motion → announcement".

Other consumers of the events: the planned automation "Klingel abends" (doorbell in the evening) in the stair-light
project (L1) turns on the stair light on a doorbell event when it is dark.

Check before installation: start URL of the panels on floors 1/2 (the EZpad on the ground floor demonstrably starts on
`/uebersicht`).

---

## Open items / next steps / dates

| # | Item | Who | Date |
|---|---|---|---|
| 1 | Measure the wires in the junction box and assign floors (multimeter V~) | Jens | **Fri 09.10.2026 18:30** |
| 2 | Read the masking-tape labels in the box (cross-check to the measurement) | Jens | with 1 |
| 3 | Determine chime voltage: 8 V (terminals 2–4) or 12 V (2–8) | Jens | with 1 |
| 4 | 1 kΩ in the resistor assortment? Otherwise buy | Jens | before soldering |
| 5 | Mini solder board delivery | – | Fri 09.10. |
| 6 | Check/change **filter order** in `klingel.yaml` (see troubleshooting no. 1) – untested | Claude/Jens | before the first flash |
| 7 | Update header comments in `klingel.yaml` to PC817 + USB supply (documentation, not a functional bug) | – | at the next firmware update |
| 8 | Generate/print the schematic as PDF (PC817 + reverse diode) | Claude | after wire assignment |
| 9 | Solder board, bench test, first flash, HA, static IP, Builder | Jens/Claude | after 1–5 |
| 10 | Create HA package, Alexa (`alexa.yaml`, routines), check start URL of panels F1/F2 | Claude/Jens | after adoption |
| 11 | Check Wi-Fi signal at the installation site | – | after installation |
| 12 | Design and print enclosure | Claude | after soldering (dimensions) |
| 13 | optional: "chime mute" relay | – | later, not commissioned |

---

## Files in the repo

| Path | Contents |
|---|---|
| `README.md` / `README.en.md` | this overview (German / English) |
| `docs/einmessen.md` | measuring / calibration |
| `docs/einbau.md` | assembly, commissioning, installation, test |
| `docs/fehlersuche.md` | failure patterns (troubleshooting) |
| `docs/verlauf.md` | project history and discarded variants |
| `docs/*.en.md` | English versions of the docs |
| `firmware/klingel.yaml` | ESPHome configuration (D1 mini, 3 inputs, 3 events) |
| `firmware/secrets.example.yaml` | template for the secrets (without real values) |
| `ha/klingel.yaml` | HA package draft (trigger templates for Alexa, push/panel automation) |
| `plaene/klingel_plan.svg` | schematic per floor: 1 kΩ, PC817, 1N4007, outputs D5/D6/D7 |
| `plaene/klingel_plan.py` | generates the schematic (matplotlib); writes to `doku/klingel_plan.svg` relative to the working directory – adjust path if needed |
| `.gitignore` | excludes real secrets, `.esphome/`, backup copies |
