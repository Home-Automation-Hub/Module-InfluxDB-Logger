from home_automation_hub import websocket
from . import storage

ws = None

def get_instance():
    if not ws:
        raise Exception("Websocket not initialised")
    return ws

def initialise(module_id):
    global ws, storage
    ws = websocket.ModuleWebsocket(module_id)    