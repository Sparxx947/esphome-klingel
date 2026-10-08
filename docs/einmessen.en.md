🇩🇪 [Deutsche Version](einmessen.md)

# Measuring / calibration

A doorbell has no measured values in the strict sense. "Calibrating" here means: finding out **which wire belongs to
which floor**, determining the **chime voltage**, checking the component values against it, testing components and board
**before** installation, and checking filters and Wi-Fi after installation.

Values from the project notes are verified; steps marked *(suggestion)* or *(unverified)* are not in the notes in this
form or have not yet been reproduced on the device.

---

## 1. Assigning the wires

**Date: Fri 09.10.2026 18:30.**

Starting point (photos 06.10.): In the junction box top left above the left distribution board, several telecom cables
meet (wires red, black, yellow, white, blue, purple, green, grey, black-white and black-orange ringed). At the bottom,
single wires red/white/blue come out – presumably to the transformer in the distribution board. Connections are made
with terminal strips as well as a WAGO 2273-203 (3-way) and a **WAGO 2273-205 (5-way)**, which presumably carries the
common conductor from the transformer. The old masking-tape labels are barely legible. The assignment could **not** be
determined from the photos.

### Procedure

1. Open the box cover. If terminals are loosened: **switch off the bell transformer's circuit breaker first.** For the
   measurement itself the system must of course be live (extra-low voltage 8/12 V AC).
2. Multimeter to **V~** (AC voltage, range 20 V or auto).
3. One probe firmly on the **5-way WAGO** (common conductor).
4. A second person presses and holds **one** doorbell button downstairs; probe the terminal-strip screws one after
   another with the other probe.
5. The wire that shows **8–12 V only with this button** is the floor wire of that floor.
6. Repeat for the other two buttons.
7. Determine the **chime return conductor** (counterpart for pin 2 of the optocouplers) – according to the plan
   "determine by measurement".
   *(Unverified how exactly it shows up in this box: if the 5-way WAGO itself is the return conductor, it is the
   common connection point of all three pin 2.)*
8. Note the result and **write it on new masking tape**:

| Floor | Wire colour / terminal | measured voltage | Input |
|---|---|---|---|
| Ground floor | … | … V~ | D5 |
| Floor 1 | … | … V~ | D6 |
| Floor 2 | … | … V~ | D7 |
| Return conductor | … | – | pin 2 of all PC817 |

Cross-check: read the masking-tape labels, if possible.

---

## 2. Determining the chime voltage

The Hager ST303 delivers **8 V between terminals 2–4** and **12 V between 2–8**. Which one the chime uses is open.
The measurement from step 1 shows it directly (~8 V or ~12 V RMS; at no load it can be somewhat higher).

---

## 3. Recalculating component values

### Peak voltage

Û = U_rms × √2

| Transformer tap | U_rms | Û |
|---|---|---|
| 8 V (2–4) | 8 V | ≈ 11.3 V |
| 12 V (2–8) | 12 V | ≈ 17 V |

The PC817's LED tolerates only ~6 V in reverse direction → **the anti-parallel 1N4007 reverse diode is mandatory**.

### LED current and power in the series resistor (1 kΩ)

Formula from the workshop book (U_F of the LED ≈ 1.2 V):

I ≈ (U − 1.2 V) / 1 kΩ  P ≈ (U − 1.2 V)² / 1 kΩ

| Chime voltage | I (RMS calculation) | I at peak (Û) | P in the resistor |
|---|---|---|---|
| 8 V | ≈ 6.8 mA | ≈ 10 mA | ≈ 0.05 W |
| 12 V | ≈ 11 mA | ≈ 16 mA | ≈ 0.12 W |

The calculation with the RMS value is conservative: because of the reverse diode the LED conducts in only one
half-wave, so the actual power dissipation is about half. **1 kΩ / 0.25 W is sufficient** in both cases. According to
the notes, the optocoupler tolerates 50 mA (stated there for the PC814; for the PC817 also 50 mA according to the usual
datasheet – *not checked against the specific datasheet*).

### Load on the bell transformer

8 VA ⇒ max. ~1 A at 8 V or ~0.67 A at 12 V. The three optocoupler branches draw only ~10 mA each, and only while the
bell is ringing – uncritical. The D1 mini (~80 mA, transmit peaks ~350 mA at 5 V) is **deliberately not** powered from
the transformer.

---

## 4. Checking components before soldering

| Check | How | Expectation |
|---|---|---|
| 1N4007 polarity | multimeter diode test | forward ~0.6–0.7 V from anode to cathode (stripe), reverse "OL" |
| PC817 LED | diode test between pin 1 (+) and pin 2 | ~1.0–1.2 V forward, reverse "OL" |
| Finding PC817 pin 1 | dot/notch on the package | pin 1 = anode, pin 2 = cathode, pin 3 = emitter, pin 4 = collector |
| Resistor | ohm measurement | ~1 kΩ (colour bands brown-black-red) |
| Reverse diode the right way round | after soldering, diode test across pin 1/pin 2 | in **one** direction ~0.65 V (1N4007, from pin 2 to pin 1), in the other ~1.1 V (LED). If both directions show ~0.65 V or one shows "OL", something is wrong |

*(The table is a suggestion derived from the schematic; values are typical datasheet values.)*

---

## 5. Bench test before installation *(suggestion)*

Without the bell transformer, each channel can be tested with DC:

1. Power the D1 mini via USB, firmware flashed, log open (ESPHome Builder → Logs or `esphome logs`).
2. From the D1 mini's **5V pin** via the fitted 1 kΩ to **pin 1**, pin-2 rail to **G** (for the test only –
   in operation the doorbell side stays isolated!).
3. Expectation: `<floor> gedrückt` (pressed) goes **ON**, an event `gedrueckt` appears; after disconnecting, **OFF**
   after ~200 ms.
4. Current: (5 − 1.2) V / 1 kΩ ≈ 3.8 mA – enough for the PC817 with internal pull-up.

This verifies the output side. The **AC behaviour** (50 pulses/s) is only checked by the test on the actual system.

---

## 6. Checking the filters on the real signal

Configuration: `delayed_on: 30ms`, then `delayed_off: 200ms`.

| Situation | Expectation |
|---|---|
| short press (~0.3 s) | exactly **one** event, input on ~0.2 s longer than pressed |
| long press (3 s) | one event, no ON/OFF flicker in the log |
| two short presses in a row (< 0.2 s pause) | one event (pause is bridged) |
| no press, chime idle | no events (spikes < 30 ms are discarded) |

**Important – unverified suspicion:** ESPHome applies filters **in order**. With PC817 + reverse diode, the input is
only "on" for about 8–10 ms per 20 ms period. `delayed_on: 30ms` as the **first** filter discards an ON as soon as an
OFF arrives before the 30 ms have elapsed – with half-waves that happens every period. Then **no** press would get
through at all. Remedy: swap the order (`delayed_off: 200ms` first, then `delayed_on: 30ms`), or reduce `delayed_on` to
≤ 5 ms. The bench test with DC (step 5) does **not** reveal this. See
[fehlersuche.en.md](fehlersuche.en.md#1-chime-rings-but-no-event-in-ha).

---

## 7. Wi-Fi at the installation site

The distribution boards are plastic in a wooden recess (no metal cabinet), a normal D1 mini should suffice – according
to the notes, **check after installation** anyway: entity `WLAN-Signal` (Wi-Fi signal, every 120 s).

| RSSI | Rating *(general guideline, not from the notes)* |
|---|---|
| better than −70 dBm | good |
| −70 … −80 dBm | usable, events may be delayed |
| worse than −80 dBm | remedy: change position; if necessary D1 mini Pro with external antenna |

---

## 8. Lockout time in Home Assistant

The automation notifies at most every **15 s** per button. Tested (04.10., template in HA):

| Before → after | Interval | Result |
|---|---|---|
| `unknown` → timestamp | very first press | notifies |
| timestamp → timestamp | 8 s | does **not** notify |
| timestamp → timestamp | 20 s | notifies |

The lockout is separate **per floor** – two floors in quick succession both notify.
