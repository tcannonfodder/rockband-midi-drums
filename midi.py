import signal
from xbox360controller import Xbox360Controller
from midi import MidiConnector
import json

# read file
with open('settings.json', 'r') as myfile:
    data=myfile.read()

# parse file
settings = json.loads(data)

controller = Xbox360Controller(0, axis_threshold=0.2, raw_mode=False)
midi_connection = MidiConnector('/dev/serial0')


def is_active_button(button):
    return button.is_pressed


def is_button_combo(button_combo, active_buttons):
    return set(button_combo["combo"]) == set(active_buttons)

def current_button_combo():
    active_buttons = [x.name for x in controller.buttons if is_active_button(x)]

    if controller.hat.x == 1:
        active_buttons.append("dpad_right")

    if controller.hat.x == -1:
        active_buttons.append("dpad_left")

    if controller.hat.y == 1:
        active_buttons.append("dpad_up")

    if controller.hat.y == -1:
        active_buttons.append("dpad_down")

    # active_buttons = filter(is_active_button, controller.buttons)
    print("Buttons: {0}".format(active_buttons))


    active_button_combos = [x for x in settings["button_combos"] if is_button_combo(x, active_buttons)]

    print("COMBOs: {0}".format(active_button_combos))
    # for button in :
    #     if button.is_pressed
    #         print("Button {0} is active")

    for button_combo in active_button_combos:
        message = NoteOn(button_combo["note_number"], button_combo["velocity"])
        print(midi_connection.write(message))


def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))
    current_button_combo()


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

try:
    with controller:
        for button in controller.buttons:
            button.when_pressed = on_button_pressed
            button.when_released = on_button_released

        controller.info()
        # Left and right axis move event
        controller.hat.when_moved = on_axis_moved
        controller.axis_l.when_moved = on_axis_moved
        controller.axis_r.when_moved = on_axis_moved

        signal.pause()
except KeyboardInterrupt:
    pass