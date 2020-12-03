Header header           # timestamp in the header is the time the data is received from the joystick
string mode             # mode 
float32[] axes          # the axes measurements from a joystick
uint8[] button_states   # the current state of the button measurements from a joystick (0 = up, 1 = pressed, 2 = down, 3 = released)