#!/usr/bin/env python

import rospy

####################
### DICTIONARIES ###
####################

# BUTTON STATE DICTIONARY
BUTTON_STATES = {"UP": 0, "PRESSED": 1, "DOWN": 2, "RELEASED": 3}

# LOGITECH F710 WIRELESS GAMEPAD
# Dictionaries for Joy Messages
JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES = {"LS_HOR": 0, "LS_VERT": 1, "RS_HOR": 2, "RS_VERT": 3, "DPAD_HOR": 4, "DPAD_VERT": 5}
JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS = {"X": 0, "A": 1, "B": 2, "Y": 3, "LB": 4, "RB": 5, "LT": 6, "RT": 7, "BACK": 8, "START": 9, "LSB": 10, "RSB": 11}

JOY_LOGITECH_F710_WIRELESS_X_INPUT_AXES = {"LS_HOR": 0, "LS_VERT": 1, "LT": 2, "RS_HOR": 3, "RS_VERT": 4, "RT": 5, "DPAD_HOR": 6, "DPAD_VERT": 7}
JOY_LOGITECH_F710_WIRELESS_X_INPUT_BUTTONS = {"A": 0, "B": 1, "X": 2, "Y": 3, "LB": 4, "RB": 5, "BACK": 6, "START": 7, "LOGITECH": 8, "LSB": 9, "RSB": 10}

# Dictionaries for Gamepad Messages
GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES = {"LS_HOR": 0, "LS_VERT": 1, "RS_HOR": 2, "RS_VERT": 3}
GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS = {"X": 0, "A": 1, "B": 2, "Y": 3, "LB": 4, "RB": 5, "LT": 6, "RT": 7, "BACK": 8, "START": 9, "LSB": 10, "RSB": 11, "DPAD_LEFT": 12, "DPAD_RIGHT": 13, "DPAD_UP": 14, "DPAD_DOWN": 15}

GAMEPAD_LOGITECH_F710_WIRELESS_X_INPUT_AXES = {"LS_HOR": 0, "LS_VERT": 1, "LT": 2, "RS_HOR": 3, "RS_VERT": 4, "RT": 5}
GAMEPAD_LOGITECH_F710_WIRELESS_X_INPUT_BUTTONS = {"A": 0, "B": 1, "X": 2, "Y": 3, "LB": 4, "RB": 5, "BACK": 6, "START": 7, "LOGITECH": 8, "LSB": 9, "RSB": 10, "DPAD_LEFT": 11, "DPAD_RIGHT": 12, "DPAD_UP": 13, "DPAD_DOWN": 14}



#################
### FUNCTIONS ###
#################

def ValidGamepadTypes():
    """Returns a list of strings containing valid gamepad types."""

    return ['logitech_f710_wireless']

def ValidGamepadType(gamepad_type):
    """Returns true if the passed gamepad_type, (type str), is valid."""
    return gamepad_type in ValidGamepadTypes()

def GetAxesAndButtonDictionaries(gamepad_type, msg_type, mode = None):
    """Returns the axes and button mapping dictionaries for the specified gamepad, message type and mode.
    
    Keyword Arguments:
        gamepad_type -- (type str) the gamepad type
        msg_type -- (type str) joy or gamepad depending on the mapping standard desired
        mode -- (type str, default None) used to specify the mode of the gamepad

    Returns: axes_dicts, btns_dict    
        axes_dicts -- the mapping dictionary for the axes given the specified arguments
        btns_dicts -- the mapping dictionary for the buttons given the specified arguments
    """

    # Make sure valid gamepad type
    if not ValidGamepadType(gamepad_type):
        raise ValueError('The gamepad type (%s) is not known.'%(gamepad_type))

    # Make sure valid msg_type (joy or gamepad)
    if msg_type.lower() != "joy" and msg_type.lower() != "gamepad":
        raise ValueError('The msg_type argument must be \"joy\" or \"gamepad\". Passed value was %s'%(msg_type))

    # Switch based on gamepad type
    if gamepad_type.lower() == 'logitech_f710_wireless':
        if mode == None or not (mode.lower() == 'directinput' or mode.lower() == 'xinput'):
            raise ValueError('The value of mode argument, \"%s\", is invalid for the %s gamepad'%(str(mode), gamepad_type.replace('_', ' ').title()))

        # joy or gamepad message type
        if msg_type.lower() == 'joy':
            if mode.lower() == 'directinput':
                axes_dict = JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES
                btns_dict = JOY_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS
            elif mode.lower() == 'xinput':
                axes_dict = JOY_LOGITECH_F710_WIRELESS_X_INPUT_AXES
                btns_dict = JOY_LOGITECH_F710_WIRELESS_X_INPUT_BUTTONS
        
        elif msg_type.lower() == 'gamepad':
            if mode.lower() == 'directinput':
                axes_dict = GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_AXES
                btns_dict = GAMEPAD_LOGITECH_F710_WIRELESS_DIRECT_INPUT_BUTTONS
            elif mode.lower() == 'xinput':
                axes_dict = GAMEPAD_LOGITECH_F710_WIRELESS_X_INPUT_AXES
                btns_dict = GAMEPAD_LOGITECH_F710_WIRELESS_X_INPUT_BUTTONS

    # return
    return axes_dict, btns_dict