from controller.keyboard import key_press
from controller.mouse import mouse_click, mouse_move
from utils.background import unit_stopped, stop_all
from utils.timeout import set_timeout


actions = {
    'I': { 'onTimeout': False, 'cascadeNumber': 7, 'timeoutDur': 0.3, 'execute': key_press(0x02) },
    'II': { 'onTimeout': False, 'cascadeNumber': 7, 'timeoutDur': 0.3, 'execute': key_press(0x03) },
    'III': { 'onTimeout': False, 'cascadeNumber': 7, 'timeoutDur': 0.3, 'execute': key_press(0x04) },
    'IV': { 'onTimeout': False, 'cascadeNumber': 7, 'timeoutDur': 0.3, 'execute': key_press(0x05) },
    'V': { 'onTimeout': False, 'cascadeNumber': 7, 'timeoutDur': 0.3, 'execute': key_press(0x06) },
    'LC': { 'onTimeout': False, 'cascadeNumber': 5, 'timeoutDur': 0, 'execute': mouse_click('left') },
    'RC': { 'onTimeout': False, 'cascadeNumber': 5, 'timeoutDur': 0, 'execute': mouse_click('right') },
    'R': { 'onTimeout': False, 'cascadeNumber': 20, 'timeoutDur': 1, 'execute': key_press(0x13) },
    'G': { 'onTimeout': False, 'cascadeNumber': 10, 'timeoutDur': 2, 'execute': key_press(0x22) },
    'B': { 'onTimeout': False, 'cascadeNumber': 10, 'timeoutDur': 2, 'execute': key_press(0x30) },
    'GO': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': lambda : unit_stopped(key_press(0x11)) },
    'UP': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': lambda : unit_stopped(mouse_move('UP')) },
    'DOWN': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': lambda : unit_stopped(mouse_move('DOWN')) },
    'LEFT': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': lambda : unit_stopped(mouse_move('LEFT')) },
    'RIGHT': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': lambda : unit_stopped(mouse_move('RIGHT')) },
    'STOP': { 'onTimeout': False, 'cascadeNumber': 1, 'timeoutDur': 0, 'execute': stop_all }
}


actions_buffer = {

}


def is_valid_action(action):
    return action in actions


def handle_action(action):
    if not is_valid_action(action):
        print(action + ' is not valid action!')

        return

    if actions[action]['onTimeout']:
        print(action + ' is on timeout')

        return

    if not action in actions_buffer:
        actions_buffer[action] = 0

    actions_buffer[action] = actions_buffer[action] + 1

    print(actions_buffer)

    if actions_buffer[action] == actions[action]['cascadeNumber']:
        execute_action(action)

        actions[action]['onTimeout'] = True
        set_timeout(clear_timeout, action, actions[action]['timeoutDur'])

        print('Clearing buffer')
        actions_buffer.clear()


def execute_action(action):
    print('executing ' + action)

    action_executor = actions[action]['execute']
    action_executor()

    print(action + ' is executed')


def clear_timeout(action):
    actions[action]['onTimeout'] = False

    print(action + ' is not on timeout anymore')
