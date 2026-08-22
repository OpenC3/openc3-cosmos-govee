# Basic smoke test. This requests status without changing the light.
cmd("GOVEE GET_STATUS")
wait("GOVEE STATUS RECEIVED_COUNT >= 1", 5)
