🇩🇪 [Deutsche Version](fehlersuche.md)

# Troubleshooting

Labels: **verified** = actually occurred in the project notes/other ESP projects or tested in HA;
**derived** = inferred from the circuit or configuration, not yet observed on the doorbell device.

| # | Symptom | Cause | Solution | Origin |
|---|---|---|---|---|
| 1 | Chime rings, but no event in HA | filter order (see below) | `delayed_off: 200ms` before `delayed_on: 230ms` – **fixed 11.10.** before the first flash | derived, fixed |
| 2 | No event, input always OFF | reverse diode soldered in the same direction as the LED → bypasses the LED (0.7 V < 1.2 V) | turn the diode around: stripe to pin 1 | derived |
| 3 | No event, PC817 broken | reverse diode missing → LED gets up to ~17 V reverse voltage (tolerates ~6 V) | replace PC817, fit the diode | derived |
| 4 | Wrong floor reported | wire assigned incorrectly | swap wires or adjust `substitutions` | derived |
| 5 | Input permanently ON | collector/emitter swapped or short circuit output–G | pin 3 = emitter → G, pin 4 = collector → Dx | derived |
| 6 | Event after ESP restart / Wi-Fi dropout | state change `unavailable` → old timestamp | `not_from: unavailable` (included in the draft) | verified (draft) |
| 7 | Very first press after setup without notification | `not_from: unknown` in the first draft | do **not** exclude `unknown` (fixed 04.10.) | verified |
| 8 | Second floor doesn't notify when rung shortly after the first | global lockout in the first draft | lockout per button, mode `parallel` (fixed 04.10.) | verified |
| 9 | Fallback hotspot doesn't accept the password | test build with dummy secrets flashed | `esphome run` with real secrets, API cross-check | verified (heating ESP 06.10.) |
| 10 | Second flash installs old firmware | `esphome upload` does not recompile | always `esphome run`, watch for "Successfully compiled" | verified |
| 11 | Flash aborts: "No more data to read" | board can't handle 460800 baud | `esptool … --baud 115200` with `firmware.factory.bin` | verified (other board) |
| 12 | `/dev/ttyUSB0` locked after re-plugging | port is recreated, ACL gone | repeat `setfacl -m u:$USER:rw /dev/ttyUSB0` | verified |
| 13 | D1 doesn't boot / hangs at startup | input placed on D3/D4/D8 (boot pins) | use only D5/D6/D7 | derived (pin choice 04.10.) |
| 14 | Events delayed / device often `unavailable` | weak Wi-Fi at the distribution board | check RSSI, change position, if necessary D1 mini Pro with external antenna | derived |
| 15 | Push doesn't reach one person | wrong `notify` service / app logged out | check services in HA; `continue_on_error` ensures the remaining actions keep running | derived |
| 16 | Event `gedrueckt` appears only after the OFF of the binary sensor | only the log client's output (see below) | nothing – in HA the event arrives on press | **resolved** 11.10. |
| 17 | Channel doesn't respond, diode test shows "OL" or wrong values | the mini solder board has **individual pads without tracks** – connection not made (on 11.10. reverse diode ↔ pin 1/pin 2, resistor ↔ pin 1, pin 2 ↔ return conductor were missing) | make all connections on the solder side with wire/solder bridges, diode test per channel (1.08 V / 0.60 V) | verified (11.10.) |
| 18 | Bench test: no detection with an 18650 shield as source | the shield (power-bank board) presumably does not switch its output on at ~8 mA load (not investigated further) | use a bare 18650 cell or a lab power supply | verified (11.10.), cause suspected |
| 19 | Readings make no sense (e.g. negative value "on AC", 0 V at rest / 0.3 V when pressed) | multimeter on the wrong range (DC instead of AC) | check the range on a known reference (transformer 2–4 on V~ = 8 V), see below | **verified** (12.10.) |
| 20 | Chime rings normally, PC817 tap detects nothing – on any transformer pole | the chime is a **battery chime with a contact input**; the transformer is not in the chime circuit, no current ever flows through the LED | look at the chime (battery? only 2 wires?), measure DC at the chime terminals; tap with BC517 + 9.1 MΩ instead of an optocoupler | **verified** (12.10.), rebuilt 20.10. |
| 21 | Single hits right after connecting, often several floors at once | **connection transients**, not a button press | do not count as proof of function; after connecting, check several real presses per floor | **verified** (12.10.) |
| 22 | Event arrives in HA, but `binary_sensor.klingel_*_gedruckt` never shows "on" | unexplained with the PC817 build | no longer seen with BC517: event and binary sensor arrive together | observed (12.10.), **resolved** 20.10. |
| 23 | BC517 build: all channels HIGH at idle (old firmware: "off", new: permanently "pressed"), no event | base gets no current (Kl.1/Kl.2 swapped, jumper wire → R → base missing), emitter not at GND, BC517 rotated – or the pin stays above the LOW threshold | work through `plaene/klingel-messblatt-bc517.pdf` and the continuity check `plaene/klingel-durchgang-bc517.pdf`, see below | **verified** (20.10.), exact cause not recorded |
| 24 | "Klingelbatterie leer" reports | one channel HIGH for more than 30 s: chime battery flat, loose wire or open base path | check the chime battery and measure Kl.1 ↔ grey | derived (sensor since 20.10.) |

---

## 1. Chime rings, but no event in HA

**Status: fixed on 11.10.2026 before the first flash.** The explanation stays here for traceability. The new order has
not yet been observed on the real AC signal (the bench test used DC) – only the acceptance test will show it.

Until 11.10. the filters in `firmware/klingel.yaml` were in this order:

```yaml
filters: &klingelfilter
  - delayed_on: 30ms
  - delayed_off: 200ms
```

ESPHome applies filters **one after another**. `delayed_on` waits 30 ms and **discards** the ON if an OFF arrives
before then. With PC817 + reverse diode, the LED conducts only during the positive half-wave – the input is on for only
about 8–10 ms per 20 ms period. The ON then never survives the 30 ms, and `delayed_off` gets nothing to smooth.

The former comment in the YAML ("Nulldurchgänge überbrücken" – bridge zero crossings) stemmed from the PC814 planning (both
half-waves, only short gaps around the zero crossing); even there, whether the gaps are bridged depends on the fall time
of the phototransistor.

**Check:** set the log to `DEBUG`/`VERBOSE` (or temporarily remove the filter) and press the button: does the raw state
flap at a 10 ms rate?

**Implemented solution (11.10.):**

```yaml
filters: &klingelfilter
  - delayed_off: 200ms    # erst Halbwellen-Lücken (≤ 10–20 ms) zu Dauer-EIN glätten
  - delayed_on: 230ms     # dann alles verwerfen, was vor der Glättung kürzer als ~30 ms war
```

(Comments: first smooth the half-wave gaps (≤ 10–20 ms) into a continuous ON; then discard everything that was shorter
than ~30 ms before smoothing.)

`delayed_on` is **230 ms** instead of 30 ms: `delayed_off` extends every ON by 200 ms – a spike as well. With
200 + 30 ms, spikes below 30 ms are still discarded; a real press is reported after ~0.23 s.

The bench test with DC does **not** reveal the original problem – only the test on the real system does.

---

## 16. Event appears only after the OFF

**Status: resolved (11.10.) – not a fault.** In Home Assistant the event arrives on press:

| Entity | Time (16:35) |
|---|---|
| `event.klingel_erdgeschoss` → `gedrueckt` | 49.818 s |
| `binary_sensor.klingel_erdgeschoss_gedruckt` ON | 49.922 s |
| `binary_sensor.klingel_erdgeschoss_gedruckt` OFF | 53.588 s |

The delay only occurred in the output of the `esphome logs` client. The automation can trigger on the event.

Original observation:

During the bench test on 11.10., the event `gedrueckt` arrived in the `esphome logs` client **~0.13–0.21 s after the OFF**
of the binary sensor each time, never at the ON. Example:

| Line | Time |
|---|---|
| binary sensor ON | 44.26 s |
| binary sensor OFF | 49.84 s |
| event `gedrueckt` | 50.05 s |

What is known:

- The `[S]` lines are formatted by the client (aioesphomeapi) **on receipt**; on the device, `Event::trigger` only logs
  at `VERBOSE`. The timestamps therefore show when the client received the message, not necessarily when the device
  fired it.
- `on_press` is correct: the PressTrigger fires on `state = true`.

Checked after HA adoption using the HA history (table above).

---

## 19. Readings make no sense

**Verified on 12.10.2026.** During the installation test the multimeter was set to **DC** for all first readings
(0.3 V, −0.6 V, −0.634 V), although AC voltage was meant to be measured. Two wrong explanations were derived from that
(reverse diode clamps the sensing circuit; 0.6 V is the chime's sensing voltage). Only the cross-check at a point with
a **known** voltage cleared it up: transformer terminals 2–4 on AC = 8 V.

| Sign | Meaning |
|---|---|
| Minus sign on a supposed AC measurement | the range is DC – AC displays have no sign |
| Readings of a few hundred millivolts on an "8–12 V system" | wrong range or wrong measuring point |
| Voltage **rises** when pressed instead of dropping to ~0 | the measured wire is not the one switched by the button |

Second, more serious lesson: before designing a tap, **look at the device at the other end** (photo, rating plate,
battery?). The assumption "the transformer drives the chime" had never been measured – see no. 20 and
[einmessen.en.md 0](einmessen.en.md#0-check-meter-range-and-the-device-at-the-other-end-first).

---

## 23. BC517 channel does not conduct at idle

**Verified on 20.10.2026** (first connection after the rebuild, all three channels). Test order:

| Step | Measurement (multimeter V⎓, black named first) | Expected | If not |
|---|---|---|---|
| 0 | G → 3V3 at the D1 | +3.2 … +3.4 V | check range/test leads – only then continue |
| 1 | grey → Kl.1 wire of the floor | **plus**, battery voltage (here 3.1 / 9.47 / 5.5 V) | negative: Kl.1/Kl.2 swapped, base gets minus |
| 2 | G → BC517 middle leg (base) | +0.9 … +1.4 V | ≈ 0 V: wire → R → base open; ≈ value of 1: emitter not at GND or BC517 rotated |
| 3 | G → pin D5/D6/D7 at idle | below 0.8 V | 0.8–2.5 V: margin (see below); ≈ 3.3 V: collector jumper missing |
| 4 | continuity G ↔ grey, G ↔ GND rail, G ↔ each emitter | beeps | re-solder the jumper |

**Margin (derived, not measured):** a Darlington has a saturation voltage of ~0.6–0.9 V (the base-emitter voltage of the
second transistor remains). The ESP8266 only reliably reads LOW below ~0.25 × VDD ≈ 0.8 V. If the pin sits just above
that at idle, the D1 reads "HIGH". A fix would be a single NPN instead of a Darlington (needs more base current, i.e. a
smaller base resistor) or an external pull-up with more current.

**Measuring trap 20.10.:** "G against wire" gave −2 / −2 / −4 V although grey and G were verifiably connected and
"grey against wire" showed +3.1 / +9.47 / +5.5 V. The conclusion "G is floating" was wrong; the continuity check
disproved it. Where the negative values came from is unexplained. **Measure voltages against the return (grey), not
against G, and prove connections with a continuity test.**

**Extra ring during the test:** on 20.10. the ground floor rang once more right after the test presses. That was a
real visitor, not crosstalk between floors. Cross-check: in the acceptance test every press triggered exactly one event
on exactly one floor.

---

## Chime gets quieter or stops ringing

Not expected: the three taps draw ~10 mA each, the transformer delivers 8 VA (~1 A at 8 V). If it happens anyway:
disconnect the tap and check whether an existing connection was loosened or a wire was clamped incorrectly when
connecting (e.g. floor wire directly onto the return conductor → chime permanently bridged or short circuit when
pressing).

With the **battery chimes** installed here, additionally: connecting plus and minus of a chime loop (or two plus
wires) triggers the chime or keeps it triggered – exactly what the button does.
