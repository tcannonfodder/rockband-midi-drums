import signal
from xbox360controller import Xbox360Controller

import pdb

controller = Xbox360Controller(0, axis_threshold=0.2, raw_mode=False)

def is_active_button(button):
    return button.is_pressed


def current_button_combo():
    active_buttons = [x for x in controller.buttons if is_active_button(x)]
    # active_buttons = filter(is_active_button, controller.buttons)
    print("Buttons: {0}".format(active_buttons))
    # for button in :
    #     if button.is_pressed
    #         print("Button {0} is active")


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

        pdb.set_trace()
        signal.pause()
except KeyboardInterrupt:
    pass