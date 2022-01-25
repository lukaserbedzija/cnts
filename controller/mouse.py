import pyautogui

pyautogui.FAILSAFE = False

def mouse_click(button):
  return lambda: pyautogui.click(button=button)

def mouse_move(position):
  moveByPositions = {
    'UP': (0, -7),
    'DOWN': (0, 7),
    'LEFT': (-7, 0),
    'RIGHT': (7, 0)
  }

  x, y = moveByPositions[position]
  
  return lambda: pyautogui.move(x, y)
