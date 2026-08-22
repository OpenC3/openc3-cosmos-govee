# OpenC3 COSMOS Govee Plugin

Control and monitor a Govee light directly over the local network. The plugin
uses Govee's local UDP JSON protocol and does not require a Govee cloud API key.

## Supported operations

- Poll power, brightness, RGB color, and color temperature telemetry
- Turn the device on or off
- Set brightness (0–100%)
- Set RGB color (0–255 per channel)
- Set white color temperature (2000–9000 K)
- Activate Sunrise, Sunset, Movie, Dating, Romantic, Twinkle, Candlelight,
  Snowflake, Energetic, Breathe, and Crossing scenes
- Try raw scene identifiers from 0–255 to investigate additional device scenes
- Send an advanced, pre-encoded `ptReal` command for model-specific features

Scene and segment support varies by model. `SET_SCENE` provides the standard
scene table used by `govee-local-api`; unsupported devices may ignore it.
Additional model-specific operations can use the advanced `PT_REAL` command.

## Prerequisites

1. The light and the COSMOS interface host must be on the same reachable LAN.
2. Enable **LAN Control** for the device in the Govee Home app. Not every Govee
   model or firmware exposes this setting.
3. Give the light a stable IP address (a DHCP reservation is recommended).
4. Permit outbound UDP/4003 and inbound UDP/4002 on the interface host.

Govee devices accept commands on UDP port 4003 and send responses to UDP port
4002. Device discovery uses multicast UDP/4001, but this plugin intentionally
configures a known device IP so COSMOS can route commands deterministically.

## Build and install

```sh
rake build VERSION=1.0.0
```

Install the resulting `.gem` from **Admin → Plugins** in COSMOS. Configure:

- `govee_target_name`: unique COSMOS target name, default `GOVEE`
- `govee_device_ip`: the light's LAN IP address
- `govee_bind_address`: local interface address, normally `0.0.0.0`
- `govee_poll_interval`: status polling interval in seconds, default `5.0`

Install one plugin instance per device and give each instance a unique target
name. If several instances share UDP/4002, the operating system must support
connected UDP socket reuse; otherwise deploy each interface on a separate host
or assign distinct network namespaces.

When COSMOS runs in Docker, the interface container must have a network path to
the physical LAN and must be able to receive UDP/4002. On Linux, host networking
is the simplest arrangement. Docker Desktop generally requires explicit UDP
port forwarding and may not preserve LAN multicast behavior.

## Examples

```python
cmd("GOVEE ON")
cmd("GOVEE SET_BRIGHTNESS with BRIGHTNESS 60")
cmd("GOVEE SET_RGB with RED 255, GREEN 80, BLUE 0")
cmd("GOVEE SET_COLOR_TEMPERATURE with KELVIN 4000")
cmd("GOVEE SET_SCENE with SCENE MOVIE")
cmd("GOVEE SET_SCENE_NUMBER with SCENE_NUMBER 42")
cmd("GOVEE GET_STATUS")
```

Script Runner also provides a helper:

```python
load_utility("GOVEE/lib/govee.py")
light = Govee()
light.set_rgb(0, 100, 255)
light.set_scene("candlelight")
light.set_scene_number(42)
```

`SET_SCENE_NUMBER` also accepts `0x`-prefixed hexadecimal values. COSMOS
constructs the model-independent scene frame, calculates its XOR checksum, and
Base64-encodes it before transmission. Scene availability is device-specific:
unknown identifiers may be ignored, duplicate an existing scene, or behave
differently across models and firmware versions.

## Protocol notes

The implementation follows the same message formats used by
`govee-local-api`:

- `{"msg":{"cmd":"devStatus","data":{}}}` requests state.
- `turn`, `brightness`, and `colorwc` perform basic control.
- `ptReal` carries checksummed, Base64-encoded scene commands.
- A `devStatus` response reports `onOff`, `brightness`, `color`, and
  `colorTemInKelvin` under `msg.data`.

Commands are JSON-accessor packets, so COSMOS validates parameter ranges and
serializes the final datagram. The UDP interface binds its source and receive
port to 4002, matching the behavior expected by Govee devices.

## License

MIT. See [LICENSE.md](LICENSE.md).
