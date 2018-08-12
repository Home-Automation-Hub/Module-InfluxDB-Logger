from home_automation_hub import mqtt
from . import storage
from influxdb import InfluxDBClient
import datetime
mqtt_subscription_tuples = []

type_conversion_methods = {
    "string": lambda x: x.decode("UTF-8"),
    "integer": lambda x: int(float(x)), # Can't directly convert bytes to int
    "float": float,
}

def generate_metric_handler(database, measurement, type_name):
    def handler(topic, payload):
        try:
            payload_converted = type_conversion_methods[type_name](payload)
        except ValueError:
            # TODO: Log this somewhere to be presented in the UI
            print(f"Could not convert {payload} to type {type_name}")
            return
        
        send_to_influxdb(database, measurement, payload_converted, topic)
    return handler


def send_to_influxdb(database, measurement, value, topic):
    host = storage.get("influxdb_host")
    port = storage.get("influxdb_port")
    username = storage.get("influxdb_username")
    password = storage.get("influxdb_password")
    
    client = InfluxDBClient(host, port, username, password, database)
    
    request_body = [
        {
            "measurement": measurement,
            "tags": {
                "mqtt_topic": topic,
            },
            "time": datetime.datetime.utcnow().isoformat(),
            "fields": {
                "value": value,
            },
        }
    ]
    client.write_points(request_body)


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
                metric.get("measurement"), metric.get("type"))
        mqtt_subscription_tuples.append(mqtt.subscribe(metric.get("topic"),
                handler))

def initialise(module_id):
    subscribe_to_all()