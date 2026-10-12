#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
**Warning!!!: Beta Firmware**

This firmware is currently in beta testing and has not been confirmed to be stable or reliable. It may contain bugs, unexpected behavior, or other issues. Please use it at your own risk.

By installing or using this firmware, you acknowledge that it is experimental. The developer assumes no responsibility for any damage, data loss, device malfunction, or other issues that may result from its use.

**Use with caution. Not recommended for production or mission-critical devices.**

'''
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CircuitPython macro pad: 4x4 key matrix + rotary encoder + I2C OLED (SSD1306)
# Works as a USB HID keyboard / consumer control (volume) device.
#
# Required libraries in /lib on CIRCUITPY:
#   adafruit_hid
#   adafruit_display_text
#   adafruit_displayio_ssd1306
#   (CircuitPython 9+ also needs adafruit_displayio_ssd1306's dependency
#    i2cdisplaybus, which is built in)

import time
import board
import busio
import displayio
import terminalio
import digitalio
import rotaryio
import usb_hid
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

try:
    from i2cdisplaybus import I2CDisplayBus      # CircuitPython 9+
except ImportError:
    from displayio import I2CDisplay as I2CDisplayBus  # CircuitPython 8

# ============================================================
#  PIN CONFIGURATION  -- change these to match your wiring
# ============================================================

# Key matrix
ROW_PINS = [board.GP2, board.GP3, board.GP4, board.GP5]      # 4 rows
COL_PINS = [board.GP6, board.GP7, board.GP8, board.GP9]      # 4 columns

# Rotary encoder
ENCODER_PIN_A = board.GP10       # encoder A (CLK)
ENCODER_PIN_B = board.GP11       # encoder B (DT)
ENCODER_BUTTON_PIN = board.GP12  # encoder push switch (SW)

# I2C screen
I2C_SDA_PIN = board.GP0          # screen SDA
I2C_SCL_PIN = board.GP1          # screen SCL
SCREEN_I2C_ADDRESS = 0x3C        # most SSD1306 OLEDs use 0x3C (sometimes 0x3D)
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64               # use 32 for 128x32 screens

# ============================================================
#  SETTINGS
# ============================================================
DEBOUNCE_TIME = 0.02   # seconds between key matrix scans
ENCODER_DIVISOR = 4    # encoder steps per detent (use 2 or 1 if it feels wrong)

# ============================================================
#  KEYMAP  -- 4 rows x 4 columns
#  Each entry is (label shown on screen, (keycodes pressed together))
# ============================================================
KEYMAP = [
    [("1", (Keycode.ONE,)),   ("2", (Keycode.TWO,)),   ("3", (Keycode.THREE,)), ("A", (Keycode.A,))],
    [("4", (Keycode.FOUR,)),  ("5", (Keycode.FIVE,)),  ("6", (Keycode.SIX,)),   ("B", (Keycode.B,))],
    [("7", (Keycode.SEVEN,)), ("8", (Keycode.EIGHT,)), ("9", (Keycode.NINE,)),  ("C", (Keycode.C,))],
    [("Copy", (Keycode.CONTROL, Keycode.C)),
     ("0", (Keycode.ZERO,)),
     ("Paste", (Keycode.CONTROL, Keycode.V)),
     ("D", (Keycode.D,))],
]

# Encoder actions (consumer control codes)
ENCODER_CW = ConsumerControlCode.VOLUME_INCREMENT
ENCODER_CCW = ConsumerControlCode.VOLUME_DECREMENT
ENCODER_PRESS = ConsumerControlCode.MUTE

# ============================================================
#  SETUP
# ============================================================
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# --- Screen ---
displayio.release_displays()
i2c = busio.I2C(I2C_SCL_PIN, I2C_SDA_PIN)
display_bus = I2CDisplayBus(i2c, device_address=SCREEN_I2C_ADDRESS)
display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=SCREEN_WIDTH, height=SCREEN_HEIGHT
)

screen = displayio.Group()
display.root_group = screen   # use display.show(screen) on CircuitPython 8

title_label = label.Label(terminalio.FONT, text="MACRO PAD", x=0, y=6)
key_label = label.Label(terminalio.FONT, text="Key: -", x=0, y=24, scale=2)
info_label = label.Label(terminalio.FONT, text="Vol: ready", x=0, y=54)
screen.append(title_label)
screen.append(key_label)
screen.append(info_label)

# --- Key matrix: rows are outputs, columns are inputs with pull-down ---
rows = []
for pin in ROW_PINS:
    r = digitalio.DigitalInOut(pin)
    r.direction = digitalio.Direction.OUTPUT
    r.value = False
    rows.append(r)

cols = []
for pin in COL_PINS:
    c = digitalio.DigitalInOut(pin)
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.DOWN
    cols.append(c)

# --- Rotary encoder ---
encoder = rotaryio.IncrementalEncoder(ENCODER_PIN_A, ENCODER_PIN_B, divisor=ENCODER_DIVISOR)
last_position = encoder.position

# Encoder push button (active low)
enc_button = digitalio.DigitalInOut(ENCODER_BUTTON_PIN)
enc_button.direction = digitalio.Direction.INPUT
enc_button.pull = digitalio.Pull.UP
enc_button_prev = True

# Track key states to detect press / release
key_state = [[False] * len(COL_PINS) for _ in ROW_PINS]


def scan_matrix():
    """Scan the matrix, send key presses/releases, update the screen."""
    for r_idx, row in enumerate(rows):
        row.value = True
        for c_idx, col in enumerate(cols):
            pressed = col.value
            name, keys = KEYMAP[r_idx][c_idx]
            if pressed and not key_state[r_idx][c_idx]:
                key_state[r_idx][c_idx] = True
                kbd.press(*keys)
                key_label.text = name
            elif not pressed and key_state[r_idx][c_idx]:
                key_state[r_idx][c_idx] = False
                kbd.release(*keys)
        row.value = False


# ============================================================
#  MAIN LOOP
# ============================================================
while True:
    scan_matrix()

    # Rotary encoder rotation
    position = encoder.position
    if position != last_position:
        diff = position - last_position
        for _ in range(abs(diff)):
            cc.send(ENCODER_CW if diff > 0 else ENCODER_CCW)
        info_label.text = "Vol " + ("UP" if diff > 0 else "DOWN")
        last_position = position

    # Encoder button
    state = enc_button.value
    if not state and enc_button_prev:   # pressed
        cc.send(ENCODER_PRESS)
        info_label.text = "Vol MUTE"
    enc_button_prev = state

    time.sleep(DEBOUNCE_TIME)
