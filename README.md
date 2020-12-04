# Gamepad
A ROS package that extends the Joy package. This package adds additional information in the published topic including controller type, current controller mode and button event state. 

This package subscribes to the joy node. Hence, you will still need to run the joy node. This package simply adds additional information to the published joy message data. The additional information is contained within a new message of type gamepad.

*Note: As of version 0.1.0 only the Logitech F710 Wireless Gamepad has been implemented. I do not have access to other controllers. However, I am happy to extend the capabilities, please reach out via a [Github feature request/bug tracker](https://github.com/jmount1992/gamepad/issues).*

## Extended Gamepad Topic
The gamepad message type extends the joy message type by including the following information:

    std_msgs/Header header  # the timestamp in the header is the time the gamepad message was published
        uint32 seq
        time stamp
        string frame_id
    string type             # the type of gamepad (e.g. logitech_f710_wireless)
    string mode             # mode the gamepad is in (e.g. DirectInput or XInput for the Logitech F710 Wireless Gamepad)
    float32[] axes          # the axes measurements from a joystick
    uint8[] button_states   # the current state of the button measurements from a joystick (0 = up, 1 = pressed, 2 = down, 3 = released)

Those familiar with the joy message will notice the inclusion of the gamepad type, the current mode of the gamepad as well as a difference in the button component (from raw data to button state data). 

## Button State
The button state component is one of the more drastic differences between the joy and gamepad message types. The gamepad node/message utilises the data from the joy message and determines the current state of each button. There are four button states:

- Up, value of 0, indicating the button is currently untouched (i.e. joy message data is currently and was previously 0)
- Pressed, value of 1, indicating the button has gone from being untouched to pressed (i.e. joy message data is currently 1 and was previously 0, rising edge)
- Down, value of 2, indicating the button is currently being held down (i.e. joy message data is currently and was previously 1)
- Released, value of 3, indicating the button has gone from being held down to untouched (i.e. joy message data is currently 0 and was previously 1, falling edge)

This allows nodes to subscribe to this data and not have to implement/re-implement button state logic. Additionally, items that are in the joy message axes vector that are discrete (e.g. the DPAD values in the Logitech F710 Wireless Gamepad) are moved to the button states component within the gamepad message. The code snippet below shows how one could use the gamepad message to determine if the X-button has just been pressed:

    from gamepad.gamepad import * # provides access to GetAxesAndButtonDictionaries function and BUTTON_STATES dictionary
    
    def GamepadCallback(gamepad_msg):
        # get the axes and button mapping dictionaries for the gamepad type, in the gamepad standard, for current gamepad mode
        axes_dict, btns_dict = GetAxesAndButtonDictionaries(gamepad_msg.type, 'gamepad', gamepad_msg.mode)

        # check to see if X button has been pressed
        if gamepad_msg.button_states[btns_dict["X]] == BUTTON_STATES["PRESSED"]:
            do blah

## Axis/Button Mapping Dictionaries
Dictionaries mapping appropriate axis/button names to the index of that axes/button within the axes/button vectors are also provided to improve code readability and help prevent errors. These are provided for both the joy and gamepad message standards. These can be accessed by including the following Python code:

    from gamepad.gamepad import *

Mappings dictionaries are provided for each gamepad type for both the joy and gamepad message standards. The standards are not the same as discrete axes within the joy message, such as the Logitech F710 Wireless Gamepad DPAD, are moved to the button component. The mapping dictionaries for the Logitech F710 Wireless Gamepad are, for example:

    # The joy standard mapping dictionaries for the Logitech F710 Wireless Gamepad, in DirectInput mode
    JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES        
    JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS

    # The gamepad standard mapping dictionaries for the Logitech F710 Wireless Gamepad, in DirectInput mode
    GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES        
    GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS

So you do not need to remember the names of the mapping dictionaries there is a `GetAxesAndButtonDictionaries(gamepad_type, msg_type, mode = None)` function. This will return the axes and button mapping dictionaries for the provided gamepad type, message type/standard (joy or gamepad) and the gamepad mode (only required if the gamepad has multiple modes). ROS nodes subscribing to the gamepad message type can simply pass in the gamepad_type and mode from the gamepad message data to get the required dictionaries. An example of how this could be used in a robot teleoperation application is below:

    from gamepad.gamepad import * # provides access to GetAxesAndButtonDictionaries function

    def Gamepad_Callback(gamepad_msg):
        # get the axes and button mapping dictionaries for the gamepad type, in the gamepad standard, for current gamepad mode
        axes_dict, btns_dict = GetAxesAndButtonDictionaries(gamepad_msg.type, 'gamepad', gamepad_msg.mode)

        # Use the mapping dictionaries to get the vertical component of the left joystick 
        # The horizontal component of the right joystick. 
        # These are used to determine the forward and rotational velocity components
        forward_vel = gamepad_msg[axes_dict['LS_VERT']] * MAX_FORWARD_VELOCITY
        rotational_vel = gamepad_msg[axes_dict['RS_HOR']] * MAX_ROTATIONAL_VELOCITY

### Axis/Button Names
The mapping dictionaries axis and button names/keys for the implemented gamepads:

**Logitech F710 Wireless Gamepad (DirectInput Mode) - Joy Standard**
| **Index**   | 0       | 1       | 2       | 3       | 4        | 5         | 6   | 7   | 8    | 9     | 10  | 11  |
| :---------: | :-----: | :-----: | :-----: | :-----: | :------: | :-------: | :-: | :-: | :--: | :---: | :-: | :-: |
| **Axes**    | LS_HOR  | LS_VERT | RS_HOR  | RS_VERT | DPAD_HOR | DPAD_VERT |
| **Buttons** | X       | A       | B       | Y       | LB       | RB        | LT  | RT  | BACK | START | LSB | RSB |

<br/>

**Logitech F710 Wireless Gamepad (XInput Mode) - Joy Standard**
| **Index**   | 0       | 1       | 2   | 3       | 4       | 5   | 6        | 7         | 8        | 9   | 10  |
| :---------: | :-----: | :-----: | :-: | :-----: | :-----: | :-: | :------: | :-------: | :------: | :-: | :-: |
| **Axes**    | LS_HOR  | LS_VERT | LT  | RS_HOR  | RS_VERT | RT  | DPAD_HOR | DPAD_VERT |
| **Buttons** | A       | B       | X   | Y       | LB      | RB  | BACK     | START     | LOGITECH | LSB | RSB |

<br/>

**Logitech F710 Wireless Gamepad (DirectInput Mode) - Gamepad Standard**
| **Index**   | 0       | 1       | 2       | 3       | 4   | 5   | 6   | 7   | 8    | 9     | 10  | 11  | 12        | 13         | 14      | 15        |
| :---------: | :-----: | :-----: | :-----: | :-----: | :-: | :-: | :-: | :-: | :--: | :---: | :-: | :-: | :-------: | :--------: | :-----: | :-------: |
| **Axes**    | LS_HOR  | LS_VERT | RS_HOR  | RS_VERT |
| **Buttons** | X       | A       | B       | Y       | LB  | RB  | LT  | RT  | BACK | START | LSB | RSB | DPAD_LEFT | DPAD_RIGHT | DPAD_UP | DPAD_DOWN |

<br/>

**Logitech F710 Wireless Gamepad (XInput Mode) - Gamepad Standard**
| **Index**   | 0       | 1       | 2   | 3       | 4       | 5   | 6    | 7     | 8        | 9   | 10  | 11        | 12         | 13      | 14        |
| :---------: | :-----: | :-----: | :-: | :-----: | :-----: | :-: | :--: | :---: | :------: | :-: | :-: | :-------: | :--------: | :-----: | :-------: |
| **Axes**    | LS_HOR  | LS_VERT | LT  | RS_HOR  | RS_VERT | RT  |
| **Buttons** | A       | B       | X   | Y       | LB      | RB  | BACK | START | LOGITECH | LSB | RSB | DPAD_LEFT | DPAD_RIGHT | DPAD_UP | DPAD_DOWN |
