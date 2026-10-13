🇩🇪 [Deutsche Version](README.md)

# Doorbell → Home Assistant (ESPHome, Wemos D1 mini)

The existing, conventional doorbell system in the house gets a "listener": a Wemos D1 mini uses three optocouplers to
detect **on which floor** someone is ringing and reports it as an `event` (device_class `doorbell`) to Home Assistant.
The chime keeps ringing **unchanged** – the ESP only taps extra-low voltage and switches nothing.

> **⚠ Status 13.10.2026: the optocoupler variant (PC817) does not work in this house.** The installation test on 12.10.
> showed: each floor has its **own battery-powered chime with a contact input** (floor 1: 9 V DC at the chime terminals
> at rest). The button only shorts the chime loop, the bell transformer is **not part** of the chime circuit – so no
> current ever flows through the optocoupler LED. A rebuild with **3 × 2N7000 (MOSFET) + 3 × 1 MΩ** is planned
> ([`plaene/klingel-schaltplan-mosfet.pdf`](plaene/klingel-schaltplan-mosfet.pdf)); the transistors arrive on 14.10.
> Before that, **the polarity (plus/minus) of the chime wires must be measured per floor** in the junction box.
> **The firmware is still unchanged** (PC817 state). The description of the PC817 circuit below is kept for
> traceability. Details: [docs/verlauf.en.md](docs/verlauf.en.md), [Rebuild with 2N7000](#rebuild-with-2n7000-planned).

| | |
|---|---|
| Project code (workshop book) | **K1 Türklingel · 3 Etagen mithören** (doorbell · listen in on 3 floors) |
| Board | Wemos D1 mini V3.0.0 (ESP8266), "D1 #2" from stock |
| Detection | 3 × optocoupler **PC817C** + one anti-parallel reverse diode **1N4007** each + 1 kΩ series resistor – **does not work here** (battery chimes), planned: 3 × **2N7000** + 3 × 1 MΩ |
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
- **Look at the chime itself first:** if it has its own battery and only two wires to the button (contact input), the
  transformer does not drive it – then the optocoupler circuit does not fit, use the MOSFET variant instead
  ([Rebuild with 2N7000](#rebuild-with-2n7000-planned)). Exactly that happened here on 12.10.

## Principle

When someone presses a doorbell button downstairs, the AC voltage of the bell transformer (8 or 12 V AC) appears at the
chime of that floor. The LED of a PC817 is connected in parallel to the chime (via 1 kΩ). The optocoupler galvanically
isolates the doorbell from the ESP; its transistor pulls the D1 mini's input (internal pull-up) to GND.

The PC817 has only **one** LED, which tolerates only about 6 V in reverse direction – the transformer delivers up to
~17 V peak. Therefore a **1N4007 is placed anti-parallel** to the LED and absorbs the negative half-wave. As a result
only **50 pulses per second** arrive at the input; the filter `delayed_off: 200ms` turns them into one continuous button
press. It therefore comes **before** `delayed_on: 230ms` – the reverse order would have discarded every press (fixed on
11.10. before the first flash, see [Troubleshooting no. 1](docs/fehlersuche.en.md#1-chime-rings-but-no-event-in-ha)).

> Originally the **PC814** was planned (two anti-parallel LEDs, designed for AC). On Amazon.de it was only available
> from 15.10.–18.11., hence PC817 + reverse diode. Since 11.10. the header comments in `firmware/klingel.yaml` describe
> the PC817/USB state.

---

## Status (as of 13.10.2026)

> **In short:** device flashed, in HA and in the Builder. The installation at the junction box on 12.10. **failed**:
> the chimes are **battery chimes with a contact input**, the PC817 tap never gets current. The board is disconnected
> (grey wire removed), the chimes work normally. **Next step:** measure polarity per floor, then rebuild with 2N7000
> (parts arrive 14.10.) and adapt the firmware. **Firmware not adapted yet.**

| Area | Status | Date |
|---|---|---|
| **Chime type** | **clarified**: each floor has its own battery chime with a contact input. Floor 1: electronic chime with a 9 V block battery, loudspeaker, only 2 wires, **9 V DC** at the terminals at rest (measured). Ground floor: probably also 9 V (*unverified*). Floor 2: different chime with 3 × C cell (LR14) = 4.5 V (*voltage at the wires not measured*). Manufacturer unknown. | 12.10. |
| **PC817 tap** | **does not work here** – the transformer is not in the chime circuit, the LED gets no current. The only hits in the log were connection transients. Board disconnected. | 12.10. |
| **Rebuild with 2N7000** | **planned**, print plan done (`plaene/klingel-schaltplan-mosfet.pdf`), transistor set ordered (delivery 14.10.), 1 MΩ available. The plan rests on an **unmeasured assumption** (separate plus wire per floor, minus sides can be joined). | 12.10. |
| Polarity of the chime wires per floor (DC) | **open** – measurement in the junction box before the rebuild | – |
| Firmware for 2N7000 | **not adapted yet** (`inverted` and filters come from the PC817 variant, see [Rebuild with 2N7000](#rebuild-with-2n7000-planned)) | – |
| Firmware `klingel.yaml` (3 buttons, events, filters) | **done**, filter order corrected (`delayed_off: 200ms` before `delayed_on: 230ms`) | 04.10. / 11.10. |
| First flash | **done** via USB with the real secrets (ESPHome 2026.9.1, RAM 39.0 %, flash 40.3 %); Wi-Fi connected, API handshake with the real key ok | 11.10. |
| Floor names / entities | **done** (`Erdgeschoss` / `Etage 1` / `Etage 2` – ground floor / floor 1 / floor 2) | 04.10. |
| Recipients per floor | **done** (GF → residents ground floor, floor 1/2 → residents floors 1/2) | 06.10. |
| Power concept | **decided**: USB power supply from the distribution board socket instead of the transformer | 06.10. |
| Tap point | **decided**: junction box top left (doorbell wires only, confirmed by Jens) | 06.10. |
| Schematic PC817 + reverse diode | **done** as SVG (`plaene/klingel_plan.svg`) and colour print version with wire colours (`plaene/klingel-schaltplan-farbig.pdf`) | 06.10. / 11.10. |
| PC817C, diode assortment | **delivered** | 07.10. (confirmed by Jens on 08.10.) |
| Mini solder boards 45 × 39 mm | **delivered** | 09.10. |
| 1 kΩ resistors | **available and fitted** | 11.10. |
| Board (3 channels) | **soldered and checked** (diode test per channel, isolation doorbell/ESP side) – single-pad board, missing connections re-soldered | 11.10. |
| Bench test | **passed** with an 18650 cell: all 3 channels, each colour only its floor, no crosstalk | 11.10. |
| Mapping wire ↔ floor in the junction box | **partly**: the 5-way WAGO is transformer pole 4 (all button wires meet there). Which two wires form the chime loop of each floor is still **open** | 12.10. |
| Chime voltage (8 V or 12 V AC) | **not applicable** – the chimes are not powered by the transformer but by their own batteries | 12.10. |
| Static IP | ✔ reserved in the router | 11.10. |
| ESPHome Builder | created as `klingel.yaml`, secrets added, device online ✔ | 11.10. |
| Adoption in HA | ✔ adopted: `event.klingel_erdgeschoss` / `_etage_1` / `_etage_2`, `binary_sensor.klingel_*_gedruckt`, status, Wi-Fi signal, uptime | 11.10. |
| Event `gedrueckt` only after the OFF in the log | ✔ resolved: in HA the event arrives **on press** (test 11.10.: event 49.818 s, binary sensor ON 49.922 s, OFF 53.588 s). The delay was only the log client's output. ([Troubleshooting no. 16](docs/fehlersuche.en.md#16-event-appears-only-after-the-off)) | 11.10. |
| HA package `ha/klingel.yaml` | **draft**, YAML parsed, lockout logic tested in HA, **not yet created in HA** | 04./06.10. |
| Enclosure | **designed** (`gehaeuse/`), printing started on 11.10. (completion not explicitly confirmed in the notes) | 11.10. |
| Side finding 12.10. | **unexplained**: during the installation test an event arrived in HA, but `binary_sensor.klingel_*_gedruckt` never showed "on" | 12.10. |

---

## Bill of materials

| Part | Qty | Designation / type | Source, ASIN, price | Status |
|---|---|---|---|---|
| Microcontroller | 1 | Wemos D1 mini V3.0.0 (ESP8266), "D1 #2" | stock (4 × available) | available |
| Optocoupler | 3 (+ spare) | PC817C, DIP-4, 50 pieces (ALLECIN) | Amazon.de, **B0CBKK6T3D**, €7.99 | delivered 07.10. |
| Reverse diode | 3 | 1N4007 (alternatively 1N5819 – recovery time irrelevant at 50 Hz) from diode assortment (BOJACK) | Amazon.de, **B07YK3XMQQ**, €10.99 (shared with the tank measurement project) | delivered 07.10. |
| Series resistor | 3 | 1 kΩ, 0.25 W is enough (~10 mA, ~0.12 W) | resistor assortment (AZ-Delivery) | available, fitted 11.10. |
| Perfboard | 1 | mini solder board 45 × 39 mm (measured 44.12 × 38.74), 5 pieces – **individual pads without tracks** | Amazon.de, **B073FVX29X**, €5.19 | delivered 09.10., soldered 11.10. |
| Power supply | 1 | USB power supply 5 V (type not fixed) for the Schuko socket in the left distribution board | – | **unresolved** (in stock?) |
| USB cable | 1 | matching the D1 mini, length socket → junction box | – | **unresolved** |
| Wires junction box → board | 4 conductors (3 floor wires + return) | single stranded wires Ø 1.38 mm: grey = chime return, yellow = ground floor, green = floor 1, blue = floor 2; connection in the box (terminal strip/WAGO) | – | colours fixed 11.10.; clamping in the box **not fixed** |
| Connections board → D1 | 4 (D5, D6, D7, G) | yellow → D5, green → D6, blue → D7, black → G (jumper wires from the ELEGOO set M2M/F2M/F2F or soldered directly) | stock | available |
| Enclosure | 1 | box + lid, `gehaeuse/klingel_box.stl` + `gehaeuse/klingel_deckel.stl` (PLA) + 4 self-tapping screws 3 × 12, wall mounting 4 × Spax 4 | own print | designed 11.10., printing not confirmed |
| Tools | – | multimeter (borrowed; own UNI-T UT139C ordered), soldering iron | stock / ordered | available |
| *optional:* relay module | 1 | for "chime mute" on D1 (GPIO5), normally-closed contact | – | idea only, commented out |
| **Rebuild 2N7000:** MOSFET | 3 | 2N7000 (TO-92) from a transistor set with 24 types (ALLECIN; also contains BC547, among others) | Amazon.de, **B0C1V82313**, €9.99 | ordered 12.10., delivery 14.10. (quantity per type not confirmed) |
| **Rebuild 2N7000:** gate resistor | 3 | 1 MΩ | own assortment | available |

**No longer needed** (from the transformer-supply draft of 04.10.): bridge rectifier, electrolytic capacitor 1000 µF/35 V,
step-down module, 1N5408 diodes for the diode tap, DIN-rail enclosure, D1 mini Pro with external antenna (the distribution
boards are plastic in a wooden recess, not a metal cabinet).

---

## Rebuild with 2N7000 (planned)

Print plan: [`plaene/klingel-schaltplan-mosfet.pdf`](plaene/klingel-schaltplan-mosfet.pdf) (A4 landscape, generated by
`plaene/klingel_mosfet_plan.py`, preview `plaene/klingel-schaltplan-mosfet-vorschau.png`; labels in German).

**Why:** at rest every chime puts its battery voltage (floor 1: 9 V DC) on the button loop; the button shorts it. A
MOSFET gate via 1 MΩ puts practically no load on the loop and switches at a few volts already.

| From | Component | To | Note |
|---|---|---|---|
| Plus wire of the floor (signal, 9 V at rest) | 1 MΩ | 2N7000 **gate** | |
| 2N7000 **drain** | – | D5 / D6 / D7 | internal pull-up |
| 2N7000 **source** | – | common ground | all three sources together |
| Minus wires of all floors | – | common ground | only allowed if the minus sides can be joined |
| D1 mini **G** | – | common ground | |

| State | Wire | MOSFET | Input |
|---|---|---|---|
| Rest | 9 V | conducts | **LOW** |
| Button pressed | 0 V | blocks | **HIGH** |

2N7000 pinout (flat side facing you, legs down): **source · gate · drain**. The optocoupler, the 1N4007 and the 1 kΩ
are dropped.

**Assumptions that must be measured before soldering** (all still *unverified*):

- Each floor has its **own plus wire**, and the minus sides of the three chimes may be joined. Never join two plus wires
  and never plus with minus – for the chime that is a button press.
- The wire voltage is enough for the 2N7000: from about 3.5 V. Floor 2 (4.5 V chime) is just above; if it is below,
  a BC547 (included in the set) is intended.

**Firmware:** **not** changed yet. According to the plan the logic changes: rest = LOW, press = HIGH – the PC817
variant's `inverted: true` has to go, and the 50 Hz smoothing (`delayed_off: 200ms` / `delayed_on: 230ms`) is to be
replaced by a simple debounce filter. Exact values are not decided yet.

## Pin assignment and wiring

> This section describes the **PC817 variant** (as of 11.10.), which does not work here. For the rebuild see
> [Rebuild with 2N7000](#rebuild-with-2n7000-planned).

Schematic: [`plaene/klingel_plan.svg`](plaene/klingel_plan.svg) (generated by `plaene/klingel_plan.py`).
Print version with wire colours (A4 landscape): [`plaene/klingel-schaltplan-farbig.pdf`](plaene/klingel-schaltplan-farbig.pdf)
(generated by `plaene/klingel_plan_druck.py`).

### Per floor (3 × identical)

| From | Component | To | Note |
|---|---|---|---|
| Floor wire (determined by measurement) | 1 kΩ | PC817 **pin 1** (anode) | |
| PC817 **pin 2** (cathode) | – | chime return conductor (common) | all three pin 2 on one rail |
| 1N4007 **cathode (stripe)** | – | PC817 pin 1 | anti-parallel to the LED |
| 1N4007 **anode** | – | PC817 pin 2 | |
| PC817 **pin 4** (collector) | – | D1 mini Dx (see below) | internal pull-up, no external resistor |
| PC817 **pin 3** (emitter) | – | D1 mini **G** | all three emitters common |

### Wire colours (as of 11.10.)

| Side | Colour | Meaning |
|---|---|---|
| doorbell side | grey | chime return conductor |
| doorbell side | yellow | ground floor |
| doorbell side | green | floor 1 |
| doorbell side | blue | floor 2 |
| ESP side | yellow | → D5 (ground floor) |
| ESP side | green | → D6 (floor 1) |
| ESP side | blue | → D7 (floor 2) |
| ESP side | black | → G |

Floor = same colour on both sides. **No red** – it is reserved for +5 V.

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

Source: [`gehaeuse/klingel-gehaeuse.scad`](gehaeuse/klingel-gehaeuse.scad) (OpenSCAD, parametric). In OpenSCAD set
`TEIL = "box"` or `"deckel"` (lid), F6, export as STL. Ready-made files:
[`gehaeuse/klingel_box.stl`](gehaeuse/klingel_box.stl) and [`gehaeuse/klingel_deckel.stl`](gehaeuse/klingel_deckel.stl).

**As of 11.10.: designed, printing not yet confirmed.** A test print of an earlier version showed: the perfboard fits.

### Measured dimensions (basis)

| Part | Dimension |
|---|---|
| Perfboard (mini solder board) | 44.12 × 38.74 mm |
| D1 mini | 34.2 × 25.6 mm |
| D1 with pin headers + Dupont plugs pointing up | 25 mm high |
| Micro-USB plug (overmould) | 10.8 × 7.2 mm |
| Wires to the junction box | 4 × Ø 1.38 mm |

### Design

| Point | Implementation |
|---|---|
| Box | outside 102.5 × 44.7 × 37 mm (67.7 mm wide with mounting tabs), wall 2.2 mm, inner height 35 mm |
| Lid | 2 mm with lip and 4 hold-downs (29.7 mm) onto the perfboard corners |
| Perfboard | on the left on 4 corner supports 5.5 × 5.5 mm (the board has large mounting holes in the corners) – **keep the corners free, also of hot glue** |
| D1 mini | on the right on a 6 mm pedestal under the antenna end + 2 supports 4 × 4.5 mm next to the USB socket (middle 9.5 mm free) |
| Wires | on the left through Ø 4.5 mm, cable-tie strain relief on 2 posts |
| USB | on the right through 12.5 × 11.6 mm (covers the socket whether it sits on the top or bottom of the board) |
| Screws | 4 screw columns inside in the corners, lid with 4 self-tapping screws 3 × 12 |
| Wall mounting | 4 tabs for Spax 4 |
| Printing | PLA, 0.2 mm, without supports; lid with the plate facing down (the STL is already oriented that way) |
| Check | via OpenSCAD intersections: openings clear, lid without collision, boards only resting on supports |

### Lessons

| Point | Lesson |
|---|---|
| Wall thickness | In a first version the openings ended **blind**: `hull()` with corner bosses on the outside had thickened all walls to 6.5 mm. The screw columns now sit inside. |
| Collisions | **Check before STL export**: don't place boards on continuous ledges, but on supports **between** the pin headers (pin headers run along the full board length). |

---

## Firmware

File: [`firmware/klingel.yaml`](firmware/klingel.yaml)

| Setting | Value |
|---|---|
| Device name / hostname | `klingel` (→ `klingel.local`) |
| Friendly name | `Klingel` (doorbell) |
| Board | `esp8266` / `d1_mini` |
| IP | **none yet** – assign a static one in the router (as with the other ESPs); still open after the first flash on 11.10. |
| `substitutions` | `taster_1: Erdgeschoss`, `taster_2: Etage 1`, `taster_3: Etage 2` (button 1: ground floor, button 2: floor 1, button 3: floor 2) |
| Filters per input | `delayed_off: 200ms`, **then** `delayed_on: 230ms` (anchor `&klingelfilter`) – order corrected since 11.10., see troubleshooting no. 1 |
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

As of 11.10.: steps 1 and 2 done (first flash locally via USB, API handshake with the real key ok). In the Builder the
device is created as `klingel.yaml` and the secrets are added. HA adoption and the static IP in the router are done
(11.10.).

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

**Short version of the sequence:** check parts ✅ → solder board ✅ → first flash ✅ → bench test ✅ →
HA/Builder/static IP ✅ → installation with PC817 ✗ (12.10., battery chimes) → **measure polarity per floor (V⎓)** →
rebuild with 2N7000 → adapt firmware → ring once per floor → create HA package → Alexa routines.

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
| 1 | ~~Measure the wires in the junction box (V~)~~ – measured on 12.10.; replaced by no. 14 (DC measurement per chime loop) | Jens | ✅ 12.10. |
| 2 | Read the masking-tape labels in the box (cross-check to the measurement) | Jens | with 1 |
| 3 | ~~Chime voltage 8 V or 12 V~~ – not applicable, battery chimes | – | 12.10. |
| 4 | 1 kΩ resistors | – | ✅ available, fitted 11.10. |
| 5 | Mini solder board delivery | – | ✅ delivered 09.10. |
| 6 | **Filter order** in `klingel.yaml` (see troubleshooting no. 1) | – | ✅ corrected 11.10., before the first flash |
| 7 | Update header comments in `klingel.yaml` to PC817 + USB supply | – | ✅ 11.10. |
| 8 | Schematic as PDF (PC817 + reverse diode, with wire colours) | – | ✅ `plaene/klingel-schaltplan-farbig.pdf`, 11.10. |
| 9 | Solder board, bench test, first flash | Jens/Claude | ✅ 11.10. |
| 9a | Assign static IP | – | ✅ 11.10. |
| 9b | ✅ Builder secrets `klingel_api_key` / `klingel_ap_password` added, HA adoption | – | done 11.10. |
| 9c | ✅ Event delay checked: in HA the event arrives on press ([troubleshooting no. 16](docs/fehlersuche.en.md#16-event-appears-only-after-the-off)) | – | done 11.10. |
| 10 | Create HA package, Alexa (`alexa.yaml`, routines), check start URL of panels F1/F2 | Claude/Jens | after adoption |
| 11 | Check Wi-Fi signal at the installation site | – | after installation |
| 12 | Design enclosure | – | ✅ 11.10. (`gehaeuse/`) |
| 12a | Print enclosure | Jens | started 11.10. |
| 12b | Installation at the junction box and acceptance test ([einbau.en.md](docs/einbau.en.md) C/D) | – | failed with PC817 on 12.10.; again after 14–16 |
| 13 | optional: "chime mute" relay | – | later, not commissioned |
| 14 | **Find the two wires carrying chime voltage per floor and measure the polarity** (multimeter on V⎓, check the range on a known point first) | Jens | before the rebuild |
| 15 | Transistor set (2N7000) | – | ordered, delivery **14.10.** |
| 16 | Rebuild: remove PC817/1N4007/1 kΩ, 3 × 2N7000 + 3 × 1 MΩ according to `plaene/klingel-schaltplan-mosfet.pdf` | Jens | from 14.10. |
| 17 | Switch firmware to the new logic (remove `inverted`, debounce filter instead of 50 Hz smoothing), flash via OTA, acceptance test per floor | Claude/Jens | after 16 |
| 18 | Clarify side finding of 12.10.: event arrived in HA, `binary_sensor.klingel_*_gedruckt` never showed "on" | – | after 17 |

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
| `plaene/klingel-schaltplan-farbig.pdf` | print sheet A4 landscape: schematic with wire colours, colour scheme and component colour codes |
| `plaene/klingel_plan_druck.py` | generates the colour PDF; reads `klingel_plan.py` from the working directory (so run it in `plaene/`) |
| `plaene/klingel-schaltplan-mosfet.pdf` | print sheet A4 landscape: rebuild with 3 × 2N7000 + 3 × 1 MΩ, polarity measuring instructions, 2N7000 pinout (12.10., German) |
| `plaene/klingel-schaltplan-mosfet-vorschau.png` | preview of the MOSFET plan |
| `plaene/klingel_mosfet_plan.py` | generates PDF and preview (matplotlib); run it in `plaene/` |
| `plaene/klingel-messblatt-abzweigdose.pdf` | measuring sheet A4 portrait for the wire mapping (11.10., German) – **still based on the assumption "transformer drives the chime" (V~)**, kept for traceability only |
| `plaene/klingel_messblatt.py` | generates the measuring sheet (matplotlib); run it in `plaene/` |
| `gehaeuse/klingel-gehaeuse.scad` | OpenSCAD source of the enclosure (`TEIL = "box"` / `"deckel"` / `"zusammen"` / `"schnitt"` / `"alle"`) |
| `gehaeuse/klingel_box.stl` | box, ready to print |
| `gehaeuse/klingel_deckel.stl` | lid, ready to print (lies with the plate facing down) |
| `.gitignore` | excludes real secrets, `.esphome/`, backup copies |
