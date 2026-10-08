🇩🇪 [Deutsche Version](fehlersuche.md)

# Troubleshooting

Labels: **verified** = actually occurred in the project notes/other ESP projects or tested in HA;
**derived** = inferred from the circuit or configuration, not yet observed on the doorbell device.

| # | Symptom | Cause | Solution | Origin |
|---|---|---|---|---|
| 1 | Chime rings, but no event in HA | filter order (see below) | `delayed_off` before `delayed_on` | derived |
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

---

## 1. Chime rings, but no event in HA

**Status: suspicion, not checked on the device.**

In `firmware/klingel.yaml` the filters are in this order:

```yaml
filters: &klingelfilter
  - delayed_on: 30ms
  - delayed_off: 200ms
```

ESPHome applies filters **one after another**. `delayed_on` waits 30 ms and **discards** the ON if an OFF arrives
before then. With PC817 + reverse diode, the LED conducts only during the positive half-wave – the input is on for only
about 8–10 ms per 20 ms period. The ON then never survives the 30 ms, and `delayed_off` gets nothing to smooth.

The comment in the YAML ("Nulldurchgänge überbrücken" – bridge zero crossings) stems from the PC814 planning (both
half-waves, only short gaps around the zero crossing); even there, whether the gaps are bridged depends on the fall time
of the phototransistor.

**Check:** set the log to `DEBUG`/`VERBOSE` (or temporarily remove the filter) and press the button: does the raw state
flap at a 10 ms rate?

**Solution (suggestion):**

```yaml
filters: &klingelfilter
  - delayed_off: 200ms    # Halbwellen-Lücken (10 ms) zuerst überbrücken
  - delayed_on: 30ms      # dann kurze Störspitzen verwerfen
```

(Comments: first bridge the half-wave gaps (10 ms); then discard short spikes.)

Alternatively drop `delayed_on` or set it to a few ms. The bench test with DC does **not** reveal the problem – only the
test on the real system does.

---

## Chime gets quieter or stops ringing

Not expected: the three taps draw ~10 mA each, the transformer delivers 8 VA (~1 A at 8 V). If it happens anyway:
disconnect the tap and check whether an existing connection was loosened or a wire was clamped incorrectly when
connecting (e.g. floor wire directly onto the return conductor → chime permanently bridged or short circuit when
pressing).
