🇩🇪 [Deutsche Version](einmessen.md)

# Measuring / calibration

A doorbell has no measured values in the strict sense. "Calibrating" here means: finding out **which wire belongs to
which floor**, determining the **chime voltage**, checking the component values against it, testing components and board
**before** installation, and checking filters and Wi-Fi after installation.

Values from the project notes are verified; steps marked *(suggestion)* or *(unverified)* are not in the notes in this
form or have not yet been reproduced on the device.

---

## 0. Check meter range and the device at the other end first

**Lesson from the installation test on 12.10.2026.** For about two hours conclusions were drawn from readings that
rested on two unverified foundations:

1. The multimeter was set to **DC**, while AC voltage was meant to be measured. A reading of **−0.6 V "on V~"** should
   have stood out immediately: an AC display has **no sign**.
2. The whole tap assumed that the **transformer drives the chime**. That each floor has a **battery chime with a
   contact input** only came out with a photo of the chime. The assumption "conventional system" had never been
   measured.

Therefore, before every measurement series now:

| Step | How | Why |
|---|---|---|
| Check the range on a **known reference** | e.g. transformer terminals 2–4 on V~ → must show ~8 V; for DC a battery of known voltage | a reading without a verified range is not a measurement |
| Negative value on "AC" | question the range immediately | AC displays are unsigned – a minus means DC range |
| **Look at the device at the other end** before designing a tap | photo of the chime/load, rating plate, battery compartment, number of wires | the type (transformer chime or battery chime with contact input) decides the whole circuit |
| Hits only right after connecting, several channels at once | count as a **connection transient**, not as a button press | a real press affects exactly one floor |

**For the rebuild with 2N7000** this means (measurement still open):

1. Multimeter on **V⎓** (DC), check the range on a battery of known voltage.
2. In the junction box find the **two wires carrying chime voltage** per floor (floor 1: ~9 V at rest; floor 2
   expected ~4.5 V, *unmeasured*).
3. Black probe on wire A, red on wire B: **+** value → B is plus (signal), A is minus; **−** value → the other way round.
4. Check whether the minus sides of the three floors may be joined (the plan assumes so). Never join two plus wires
   and never plus with minus – that triggers the chime.
5. Note the rest voltage per floor: below ~3.5 V the 2N7000 is not reliable → BC547 intended.

| Floor | Plus wire | Minus wire | Rest voltage V⎓ | when pressed |
|---|---|---|---|---|
| Ground floor | … | … | … V | … V |
| Floor 1 | … | … | ~9 V (measured at the chime terminals) | … V |
| Floor 2 | … | … | … V | … V |

---

## 1. Assigning the wires

> **Superseded (12.10.):** the following procedure assumes that the transformer drives the chime (V~ measurement
> against the 5-way WAGO). That is not the case here – the chimes are battery chimes. Measurement results of 12.10.
> see [verlauf.en.md](verlauf.en.md); for the rebuild, section 0 applies. The text is kept for traceability.

**Date: open.** Fri 09.10. and Sat 10.10. were planned – the measurement has not taken place yet (as of 11.10.).
The colours of the wires to the board are already fixed: grey = chime return conductor, yellow = ground floor,
green = floor 1, blue = floor 2.

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

> **Not applicable (12.10.):** the chimes are not powered by the transformer. Sections 2 and 3 only apply to the PC817 variant.

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

**Measured on 11.10.** after soldering, all 3 channels identical: + on pin 1 → pin 2 = **1.08 V** (LED), + on pin 2 →
pin 1 = **0.60 V** (1N4007); doorbell side ↔ ESP side **no continuity**. If a channel shows "OL", a connection is
probably missing on the single-pad board (see [einbau.en.md A](einbau.en.md#a-building-the-board)).

---

## 5. Bench test before installation

Without the bell transformer, each channel can be tested with DC.

### Method actually used (11.10., passed)

The source is a **separate battery** instead of the 5 V from the D1 mini: G on the D1 is occupied, and this way the
isolation between doorbell side and ESP side is preserved during the test as well.

1. Power the D1 mini via USB, firmware flashed, log open (`esphome logs`).
2. Source: a **bare 18650 cell**. **Minus** to the grey wire (chime return conductor), **plus** for 2–3 s to the wire of
   one floor (yellow / green / blue).
3. Expectation: only `<floor> gedrückt` (pressed) goes **ON**, an event `gedrueckt` appears; after disconnecting,
   **OFF** ~200 ms later.

Result 11.10.: blue → only "Etage 2", yellow → only "Erdgeschoss", green → only "Etage 1", several times each, event
`gedrueckt` every time, **no crosstalk**. Notable: the event arrived in the log only after the OFF – unexplained, see
[fehlersuche.en.md no. 16](fehlersuche.en.md#16-event-appears-only-after-the-off).

> **No 18650 shield (power-bank board) as source:** it gave **no** detection – presumably the shield does not switch its
> output on at ~8 mA load (not investigated further). Use a battery directly or a lab power supply.

### Original suggestion (not used)

From the D1 mini's **5V pin** via the fitted 1 kΩ to **pin 1**, pin-2 rail to **G**; current (5 − 1.2) V / 1 kΩ ≈
3.8 mA. Not used because G is occupied and the isolation of the two sides would have to be broken for it.

This verifies the output side. The **AC behaviour** (50 pulses/s) is only checked by the test on the actual system.

---

## 6. Checking the filters on the real signal

Configuration (since 11.10.): `delayed_off: 200ms`, **then** `delayed_on: 230ms`.

| Situation | Expectation |
|---|---|
| short press (~0.3 s) | exactly **one** event; input reports after ~0.23 s and stays on ~0.2 s longer than pressed |
| long press (3 s) | one event, no ON/OFF flicker in the log |
| two short presses in a row (< 0.2 s pause) | one event (pause is bridged) |
| no press, chime idle | no events (spikes < 30 ms are discarded) |

**Fixed on 11.10. (before the first flash):** ESPHome applies filters **in order**. With PC817 + reverse diode, the
input is only "on" for about 8–10 ms per 20 ms period. The former configuration had `delayed_on: 30ms` as the **first**
filter – it discards an ON as soon as an OFF arrives before the 30 ms have elapsed, and with half-waves that happens
every period. Then **no** press would have got through at all. Now `delayed_off: 200ms` smooths first; `delayed_on` is
set to 230 ms (200 + 30), because `delayed_off` also extends spikes by 200 ms – so spikes < 30 ms remain discarded. The
bench test with DC (step 5) does **not** reveal the order; it has not yet been observed on the real signal. See
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
