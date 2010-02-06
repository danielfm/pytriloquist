# Whether the server should notify events on the server desktop
USE_PYNOTIFY = True

# Bluetooth channel to use
CHANNEL = 3

# List of whitelisted clients
ALLOWED_DEVICES = (
    # "AA:BB:CC:DD:EE:FF",
)

# Mouse commands
MOUSE_MOVE  = 'xte "mousermove %s %s"' # x, y
MOUSE_CLICK = 'xte "mouseclick %s"'    # mouse button
MOUSE_DRAG  = 'xte "mousedown %s"'     # mouse button
MOUSE_DROP  = 'xte "mouseup %s"'       # mouse button
