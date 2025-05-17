# KEH
# Modified Gemma M0 Demo

# Adafruit CircuitPython 9.2.7
# Adafruit Gemma M0 with samd21e18

# Built-in libraries:
import time
import board
import digitalio
from touchio import TouchIn
from digitalio import DigitalInOut, Direction, Pull

# Capacitive touch on A2
touch2 = TouchIn(board.A2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Configure APA102 (DotStar) pins
clock = digitalio.DigitalInOut(board.APA102_SCK)
clock.direction = digitalio.Direction.OUTPUT
data = digitalio.DigitalInOut(board.APA102_MOSI)
data.direction = digitalio.Direction.OUTPUT

# DotStar functions:
def send_byte(byte):
    """Send a single byte to the DotStar."""
    for i in range(8):
        clock.value = False
        data.value = (byte >> (7 - i)) & 1
        clock.value = True

def send_pixel(r, g, b, brightness=0.2):
    """Send RGB color to the DotStar with brightness control."""
    for _ in range(4): send_byte(0x00)  # Start frame
    send_byte(0xE0 | int(31 * brightness))  # Global brightness (5 bits)
    send_byte(b)  # Blue
    send_byte(g)  # Green
    send_byte(r)  # Red
    for _ in range(4): send_byte(0xFF)  # End frame

def colorwheel(pos):
    """Generate RGB values for a color wheel position (0-255)."""
    pos = pos % 256  # Ensure pos is 0-255
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)  # Red to green
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)  # Green to blue
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)  # Blue to red

# Main loop
pos = 0
while True:
    # use A2 as capacitive touch to turn on internal LED
    led.value = touch2.value

    r, g, b = colorwheel(pos)
    send_pixel(r, g, b, brightness=0.1)
    pos = (pos + 1) % 256
    time.sleep(0.03)