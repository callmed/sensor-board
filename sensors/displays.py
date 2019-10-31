# import threading
import logging


RASPBERRYPI = False
logger = logging.getLogger("sensorboard")


try:
    # Non-existent modules on non-raspberry pi systems
    # Display
    import Adafruit_SSD1306
    # Image functions
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    RASPBERRYPI = True
except ImportError:
    RASPBERRYPI = False
    logger.warning("Module not found")


class Display:
    logo = None

    def __init__(i2c_address):
        pass

    def _clear(self):
        """ Clear display, what acutally means empty. """
        pass

    def show_logo(self):
        pass

# Links:
# Modules required?!: smbus, i2c-tools python-pil
# https://indibit.de/raspberry-pi-oled-display-128x64-mit-python-ansteuern-i2c/#Adresse_ermitteln
