from openc3.script import *


class Govee:
    """Small Script Runner convenience wrapper for a Govee target."""

    def __init__(self, target="GOVEE"):
        self.target = target

    def refresh(self):
        return cmd(f"{self.target} GET_STATUS")

    def turn_on(self):
        return cmd(f"{self.target} ON")

    def turn_off(self):
        return cmd(f"{self.target} OFF")

    def set_power(self, enabled):
        value = 1 if enabled else 0
        return cmd(f"{self.target} SET_POWER with VALUE {value}")

    def set_brightness(self, percent):
        return cmd(f"{self.target} SET_BRIGHTNESS with BRIGHTNESS {int(percent)}")

    def set_rgb(self, red, green, blue):
        return cmd(
            f"{self.target} SET_RGB with RED {int(red)}, GREEN {int(green)}, BLUE {int(blue)}"
        )

    def set_color_temperature(self, kelvin):
        return cmd(
            f"{self.target} SET_COLOR_TEMPERATURE with KELVIN {int(kelvin)}"
        )

    def set_scene(self, scene):
        """Activate a named scene such as SUNRISE, MOVIE, or CANDLELIGHT."""
        return cmd(f"{self.target} SET_SCENE with SCENE {str(scene).upper()}")

    def set_scene_number(self, scene_number):
        """Activate a raw scene identifier from 0 through 255."""
        return cmd(
            f"{self.target} SET_SCENE_NUMBER with SCENE_NUMBER {scene_number}"
        )
