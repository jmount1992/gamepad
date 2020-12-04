Header header           # the timestamp in the header is the time the gamepad message was published
string type             # the type of gamepad (e.g. logitech_f710_wireless)
string mode             # mode the gamepad is in (e.g. DirectInput or XInput for the Logitech F710 Wireless Gamepad)
float32[] axes          # the axes measurements from a joystick
uint8[] button_states   # the current state of the button measurements from a joystick (0 = up, 1 = pressed, 2 = down, 3 = released)