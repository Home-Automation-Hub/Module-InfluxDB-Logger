from home_automation_hub import storage

instance = None

def get_instance():
    if not instance:
        raise Exception("Storage instance not initialised")
    return instance

def set_default_values():
    pass

def set(key, value):
    return instance.set(key, value)

def get(key):
    return instance.get(key)

def initialise(module_id):
    global instance
    instance = storage.ModuleStorage(module_id)
    set_default_values()
