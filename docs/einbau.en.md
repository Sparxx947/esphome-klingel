🇩🇪 [Deutsche Version](einbau.md)

# Assembly, commissioning, installation and test

Sequence: **A** build the board → **B** commissioning on the bench → **C** installation at the junction box →
**D** acceptance test → **E** Home Assistant. Prerequisite is the wire assignment from
[einmessen.en.md](einmessen.en.md#1-assigning-the-wires).

---

## A. Building the board

Material: mini solder board 45 × 39 mm, 3 × PC817C, 3 × 1N4007, 3 × 1 kΩ, connecting wires. Schematic:
[`../plaene/klingel_plan.svg`](../plaene/klingel_plan.svg).

1. Check components (diode test, see [einmessen.en.md § 4](einmessen.en.md#4-checking-components-before-soldering)).
2. Arrange three channels side by side; doorbell side on the left (floor wires + return conductor), ESP side on the
   right (D5/D6/D7 + G). *(The layout is a suggestion – separating doorbell side and ESP side is the whole point of
   the optocoupler.)*
3. Per channel:
   - floor wire → **1 kΩ** → **pin 1** of the PC817
   - **1N4007** between pin 1 and pin 2: **stripe (cathode) to pin 1**, anode to pin 2
   - **pin 2** → common return-conductor rail
   - **pin 4** (collector) → output Dx
   - **pin 3** (emitter) → common G rail
4. Outputs: ground floor → **D5**, floor 1 → **D6**, floor 2 → **D7**, G rail → **G**.
   No external pull-ups – the firmware uses `INPUT_PULLUP`.
5. Do **not** use D3, D4 or D8 (boot pins); D1 stays free for a possible relay.
6. After soldering: measure continuity doorbell side ↔ ESP side → must be **open**.
7. Label terminals/wires (floor, return conductor).

---

## B. Commissioning on the bench

1. Provide real secrets (template `firmware/secrets.example.yaml`; real values only locally or in the Builder).
2. **Before the first flash:** settle the filter order in `firmware/klingel.yaml`
   (see [fehlersuche.en.md no. 1](fehlersuche.en.md#1-chime-rings-but-no-event-in-ha)).
3. Connect the D1 mini to the PC via USB, grant port access: `setfacl -m u:$USER:rw /dev/ttyUSB0`.
4. Flash: `esphome run klingel.yaml --no-logs --device /dev/ttyUSB0` → "Successfully compiled" must appear in the log.
   **No** `esphome upload` and **no** build with dummy secrets.
5. Cross-check: connect via the API with the real key, read states.
6. Home Assistant: add the ESPHome integration with host and encryption key; check entity names
   (expected `event.klingel_erdgeschoss`, `event.klingel_etage_1`, `event.klingel_etage_2`).
7. Router: assign a static IP for the D1 mini's MAC (tool `fb_feste_ip.py`, as with the other ESPs).
8. ESPHome Builder: add secrets, "New device" → skip → paste YAML, do **not** install. From now on OTA.
9. Bench test per channel with 5 V via 1 kΩ (see [einmessen.en.md § 5](einmessen.en.md#5-bench-test-before-installation-suggestion)).

---

## C. Installation at the junction box

| Location | What |
|---|---|
| Junction box top left above the left distribution board | tap of the 3 floor wires + return conductor (extra-low voltage only) |
| next to it | board + D1 mini (enclosure still open) |
| left distribution board, row 5, slot 49–52 ("SNS016") | Schuko socket for the USB power supply |

1. **Bell transformer's circuit breaker off** (transformer: right distribution board, row 3, slot 25/26).
2. Clamp an additional wire to each floor wire and to the return conductor (into the existing terminal strip/WAGO or a
   new WAGO) – do **not** break the existing connections to chime and buttons. *(Type of clamping not fixed.)*
3. Route the wires to the board, floors to the correct channels according to the measurement log.
4. Attach new masking-tape labels.
5. Plug the USB power supply into the distribution board socket, connect the D1 mini.
6. Switch the bell transformer's circuit breaker back on.
7. Check: the chime rings for all three buttons as before (the tap draws only ~10 mA extra).

---

## D. Acceptance test

| # | Test | Expectation |
|---|---|---|
| 1 | Press ground-floor button briefly | chime rings; in HA `event.klingel_erdgeschoss` with `gedrueckt` (pressed); only this input |
| 2 | Floor 1 button | only `event.klingel_etage_1` |
| 3 | Floor 2 button | only `event.klingel_etage_2` |
| 4 | long press (3 s) | **one** event, no flapping in the log |
| 5 | Repeated ringing (several times within 15 s) | one push notification per floor (after creating the HA package) |
| 6 | ESP restart (Builder → Restart) | **no** event, no push notification |
| 7 | Read Wi-Fi signal | note the value, see [einmessen.en.md § 7](einmessen.en.md#7-wi-fi-at-the-installation-site) |
| 8 | D1 without power | chime still rings normally |

Swapped floors: either swap the wires on the board or adjust the `substitutions` `taster_1..3`
(the entity names then change – update the HA package accordingly).

---

## E. Home Assistant

1. Create `ha/klingel.yaml` as a package (check entity names against the actually adopted ones).
2. Test per floor: push goes to the right recipients (GF → residents ground floor; F1/F2 → residents floors 1/2),
   front-door camera image included, all three wall panels wake up, show the overview and the overlay.
3. Check the start URL of the panels on floor 1 and floor 2.
4. Alexa: add `binary_sensor.klingel_erdgeschoss/_etage_1/_etage_2` to `/config/alexa.yaml`, discover devices,
   one routine with announcement per floor.
