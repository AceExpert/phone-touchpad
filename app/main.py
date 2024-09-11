#from threading import Thread

import ws, pyautogui, win32api, win32con, socket

server: ws.ServerSocket = ws.ServerSocket()
size: tuple[int, int] = pyautogui.size()

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

#threads: list[Thread] = []
alt: bool = False

@server.event
async def on_ready() -> None:
    print("Listening at", f"ws://{server.address}:{server.port}")
    print(f"Connect to server at http://{server.address}:5000\n")

@server.event
async def on_connect(client, path: str) -> None:
    print("Keyboard client connected")

@server.event
async def on_message(message: ws.Message) -> None:
    global alt
    
    #for thread in threads:
    #    if not thread.is_alive(): threads.remove(thread)

    if key := message.data.get('key', None):
        if isinstance(key, (tuple, list,)):
            pyautogui.press("backspace", key[1])
            pyautogui.write(key[0])
        else:
            pyautogui.press(key)

    elif coords := message.data.get('touch', None):
        #pyautogui.moveRel(coords[0] * size[0] * .2, coords[1] * size[1] * .2, .1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(coords[0] * size[0] * .05), int(coords[1] * size[1] * .05))
    elif message.data.get('tap', None):
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    elif scroll := message.data.get('scroll', None):
        
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], int(scroll[0] * size[1] * 0.05), 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_HWHEEL, win32api.GetCursorPos()[0], win32api.GetCursorPos()[1], int(scroll[1] * size[0] * 0.05), 0)

    elif coords := message.data.get('drag', None):
        if message.data.get('start', None):
        
           win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

        elif message.data.get('end', None):

            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    elif coords := message.data.get('three', None): 
        if not alt:
            pyautogui.keyDown('alt')
            pyautogui.press('tab')
            alt = True
        if abs(coords[0]) > 10:
            pyautogui.press('right' if coords[0] > 0 else 'left')
        if abs(coords[1]) > 10:
            pyautogui.press('down' if coords[1] > 0 else 'up')
        

    elif coords := message.data.get('threeEnd', None): 
        if alt:
            pyautogui.keyUp('alt')
            alt = False

server.listen(socket.gethostbyname(socket.gethostname()), '4000')