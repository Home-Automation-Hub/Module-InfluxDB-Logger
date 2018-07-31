from home_automation_hub import mqtt
from . import storage
mqtt_subscription_tuples = []

def generate_metric_handler(database, measurement):
    def handler(topic, payload):
        print("Hello from handler for "+measurement+","+database)
        print(f"Topic: {topic}, {payload}")
    return handler

def subscribe_to_all():
    global mqtt_subscription_tuples
    # First unsubscribe from everything then resubscribe to everything
    # we have stored
    while mqtt_subscription_tuples:
        subscription_tuple = mqtt_subscription_tuples.pop()
        mqtt.unsubscribe(subscription_tuple)

    metrics = storage.get("metrics")
    for metric in metrics:
        handler = generate_metric_handler(metric.get("database"),
                metric.get("measurement"))
        mqtt_subscription_tuples.append(mqtt.subscribe(metric.get("topic"),
                handler))

def initialise(module_id):
    subscribe_to_all()