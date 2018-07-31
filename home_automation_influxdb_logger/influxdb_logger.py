from home_automation_hub import mqtt
from . import storage, web, control

def register(module_id_):
    module_id = module_id_

    storage.initialise(module_id)
    web.initialise(module_id)
    control.initialise(module_id)