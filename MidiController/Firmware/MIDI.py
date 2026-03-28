# MIDI Controller Keyboard - CircuitPython
# Raspberry Pi Pico 2 + MCP23017 key matrix + ST7735 display + rotary encoders

import board
import busio
import digitalio
import time
import displayio
from fourwire import FourWire
from adafruit_st7735r import ST7735R
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.control_change import ControlChange
from adafruit_mcp230xx.mcp23017 import MCP23017
import rotaryio
import usb_midi

# ============ PIN ASSIGNMENTS (from KiCad schematic) ============
# I2C: GPIO0=SDA, GPIO1=SCL (MCP23017)
# SPI Display: GPIO18=SCK, GPIO19=MOSI, GPIO15=CS_LCD, GPIO13=A0/DC, GPIO8=RST
# Encoder 1: GPIO17=1A, GPIO20=1B
# Encoder 2: GPIO21=2A, GPIO22=2B
# I2S DAC: GPIO26=BLCK, GPIO27=LRCLK, GPIO28=DIN (optional - for future audio)

# ============ KEY MATRIX (MCP23017) ============
# Rows: GPA0, GPA1, GPA2, GPA3, GPA4, GPB7 (6 rows)
# Cols: GPB0, GPB1, GPB2, GPB3, GPB4, GPB5, GPB6 (7 cols)
# 6x7 = 42 keys | Rows 0-2: User buttons/encoders | Rows 3-6: Piano keys (low + high octave)

ROWS = 6
COLS = 7
NUM_KEYS = ROWS * COLS

# Base MIDI note (C2 = 36). Keys map to 36-77 (C2 to F5)
BASE_NOTE = 36
VELOCITY = 127

# Octave shift (0 = no shift, 12 = +1 octave, -12 = -1 octave)
octave_shift = 0

# ============ INITIALIZE I2C & MCP23017 ============
i2c = busio.I2C(board.GP0, board.GP1)
mcp = MCP23017(i2c)

# Create row pins (outputs) - GPA0-4, GPB7
row_pins = [
    mcp.get_pin(0),   # GPA0
    mcp.get_pin(1),   # GPA1
    mcp.get_pin(2),   # GPA2
    mcp.get_pin(3),   # GPA3
    mcp.get_pin(4),   # GPA4
    mcp.get_pin(15),  # GPB7
]
# Create column pins (inputs with pull-up) - GPB0-6
col_pins = [
    mcp.get_pin(8),   # GPB0
    mcp.get_pin(9),   # GPB1
    mcp.get_pin(10),  # GPB2
    mcp.get_pin(11),  # GPB3
    mcp.get_pin(12),  # GPB4
    mcp.get_pin(13),  # GPB5
    mcp.get_pin(14),  # GPB6
]

# Configure pins
for pin in row_pins:
    pin.switch_to_output(value=True)  # High = inactive
for pin in col_pins:
    pin.switch_to_input(pull=digitalio.Pull.UP)

# ============ KEY STATE (for debouncing) ============
key_state = [False] * NUM_KEYS

def scan_matrix():
    """Scan key matrix and return list of (key_number, pressed)."""
    events = []
    for row in range(ROWS):
        # Drive current row low
        row_pins[row].value = False
        time.sleep(0.001)  # Settling time
        # Read columns
        for col in range(COLS):
            key_num = row * COLS + col
            pressed = not col_pins[col].value  # Low = pressed (pull-up)
            if pressed != key_state[key_num]:
                key_state[key_num] = pressed
                events.append((key_num, pressed))
        # Drive row high again
        row_pins[row].value = True
    return events

# ============ ROTARY ENCODERS ============
encoder1 = rotaryio.IncrementalEncoder(board.GP17, board.GP20)
encoder2 = rotaryio.IncrementalEncoder(board.GP21, board.GP22)
enc1_pos = encoder1.position
enc2_pos = encoder2.position

# ============ DISPLAY ============
displayio.release_displays()
spi = busio.SPI(board.GP18, MOSI=board.GP19)
display_bus = FourWire(
    spi,
    command=board.GP13,
    chip_select=board.GP15,
    reset=board.GP8,
)
display = ST7735R(display_bus, width=128, height=160, rotation=270)

# Create main group and show
main_group = displayio.Group()
display.show(main_group)

# Simple splash text
text_area = None
try:
    from adafruit_display_text import label
    import terminalio
    text_area = label.Label(terminalio.FONT, text="MIDI Keyboard", color=0x00FF00)
    text_area.x = 10
    text_area.y = 70
    main_group.append(text_area)
except (ImportError, OSError):
    pass

# ============ MIDI ============
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    in_channel=0,
    midi_out=usb_midi.ports[1],
    out_channel=0,
)

# ============ MAIN LOOP ============
last_display_update = 0
pitch_bend_center = 8192  # 14-bit center
current_pitch_bend = pitch_bend_center

while True:
    # Scan keyboard matrix
    for key_num, pressed in scan_matrix():
        # Rows 0-2: control buttons (octave up/down, etc.)
        if key_num < 3 * COLS:  # First 3 rows = user buttons
            if pressed and key_num == 0:  # Octave down
                octave_shift = max(-24, octave_shift - 12)
            elif pressed and key_num == 1:  # Octave up
                octave_shift = min(24, octave_shift + 12)
            # Add more control mappings as needed
        else:
            # Rows 3-5: piano keys (low + high octave) - send MIDI
            midi_note = BASE_NOTE + (key_num - 3 * COLS) + octave_shift
            midi_note = max(0, min(127, midi_note))
            if pressed:
                midi.send(NoteOn(midi_note, VELOCITY))
            else:
                midi.send(NoteOff(midi_note, 0))

    # Encoder 1 = Pitch bend
    pos1 = encoder1.position
    if pos1 != enc1_pos:
        delta = pos1 - enc1_pos
        current_pitch_bend = max(0, min(16383, current_pitch_bend + delta * 400))
        midi.send(PitchBend(current_pitch_bend))
        enc1_pos = pos1

    # Encoder 2 = Modulation wheel (CC 1)
    pos2 = encoder2.position
    if pos2 != enc2_pos:
        delta = pos2 - enc2_pos
        mod_value = max(0, min(127, 64 + delta * 10))
        midi.send(ControlChange(1, mod_value))
        enc2_pos = pos2

    # Return pitch bend to center when encoder not moved (optional)
    # current_pitch_bend = pitch_bend_center  # Uncomment for spring-back

    # Update display periodically
    now = time.monotonic()
    if text_area and (now - last_display_update) > 0.5:
        text_area.text = f"Oct:{octave_shift//12:+d}"
        last_display_update = now

    time.sleep(0.01)  # ~100Hz scan rate

    #test
