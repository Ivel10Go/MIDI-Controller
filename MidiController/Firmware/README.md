# MIDI Controller Keyboard Firmware

CircuitPython firmware for the Hack Club MIDI Controller - a 42-key keyboard with rotary encoders and display.

## Features

- **42-key matrix** (6×7) via MCP23017 I/O expander
  - Rows 0–2: User buttons (octave up/down on keys 0 and 1)
  - Rows 3–5: Piano keys (21 notes, C2–A3 range, shiftable)
- **Rotary encoder 1**: Pitch bend
- **Rotary encoder 2**: Modulation wheel (CC#1)
- **ST7735 display**: Shows octave shift
- **USB MIDI**: Plug in and use as a class-compliant MIDI controller

## Hardware

- Raspberry Pi Pico 2 (RP2040)
- MCP23017 I2C I/O expander for key matrix
- ST7735R 128×160 TFT display
- 2× rotary encoders (Alps EC11E)
- PCM5100 I2S DAC (for future audio)

## Setup

1. **Flash CircuitPython** on the Pico 2 from [circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico2/).

2. **Install libraries** (with board connected):
   ```bash
   circup install adafruit_midi adafruit_mcp230xx adafruit_st7735r adafruit_display_text
   ```

3. **Copy `MIDI.py`** to the board as `code.py` (or `MIDI.py` and rename in `boot.py`).

4. **Connect via USB** – the device appears as a USB MIDI keyboard.

## Pin Assignments

| Function   | Pins                          |
|-----------|--------------------------------|
| I2C       | GP0 (SDA), GP1 (SCL)          |
| Display   | GP8 (RST), GP13 (DC), GP15 (CS), GP18 (SCK), GP19 (MOSI) |
| Encoder 1 | GP17 (A), GP20 (B)            |
| Encoder 2 | GP21 (A), GP22 (B)            |

## Configuration

- `BASE_NOTE`: Base MIDI note (default 36 = C2)
- `VELOCITY`: Note-on velocity (default 127)
- Octave range: ±2 octaves via keys 0 and 1

## Troubleshooting

- **Display not working**: If RST is tied to 3.3V on your board, set `reset=None` in the FourWire call.
- **Wrong keys**: Row/column order may differ; adjust `row_pins` and `col_pins` to match your schematic.
- **No MIDI output**: Ensure the host recognizes the device as a USB MIDI interface.
