import base64

from openc3.conversions.conversion import Conversion


class SceneNumberConversion(Conversion):
    """Convert a scene byte into a checksummed Govee ptReal command."""

    def __init__(self):
        super().__init__()
        # The command parameter is presented to users as an unsigned byte,
        # while its raw JSON representation is a Base64 string.
        self.converted_type = "UINT"
        self.converted_bit_size = 8

    def call(self, value, _packet, _buffer):
        text = str(value).strip()
        scene_number = int(text, 16) if text.lower().startswith("0x") else int(text)
        if not 0 <= scene_number <= 255:
            raise ValueError("SCENE_NUMBER must be between 0 and 255")

        payload = b"\x33\x05\x04" + bytes([scene_number]) + (b"\x00" * 15)
        checksum = 0
        for byte in payload:
            checksum ^= byte
        return base64.b64encode(payload + bytes([checksum])).decode("ascii")

