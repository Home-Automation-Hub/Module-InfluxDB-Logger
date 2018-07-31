from home_automation_hub import web
from flask import render_template, request, jsonify
from . import storage, control

def view_index():
    return render_template("influxdb_logger/index.html")

def view_settings():
    host = storage.get("influxdb_host") or ""
    port = storage.get("influxdb_port") or 8086
    username = storage.get("influxdb_username") or ""
    return render_template("influxdb_logger/settings.html", host=host,
            port=port, username=username)

def view_metrics():
    metrics = storage.get("metrics") or []
    metrics.append({"isTemplate": True})

    return render_template("influxdb_logger/metrics.html", metrics=metrics)

def action_save_settings():
    settings = request.get_json()
    influxdb_host = settings.get("host")
    influxdb_port = settings.get("port")
    influxdb_username = settings.get("username")
    influxdb_password = settings.get("password")
    
    error = None
    if not influxdb_host:
        error = ("You must provide a hostname/IP Address for the InfluxDB "
                "server")
    
    if influxdb_port:
        try:
            influxdb_port = int(influxdb_port)
        except ValueError:
            error = "InfluxDB server port must be a number"
    else:
        error = "You must supply a port for the InfluxDB server"

    if not influxdb_username:
        error = "You must supply a username for the InfluxDB server"

    if not error:
        storage.set("influxdb_host", influxdb_host)
        storage.set("influxdb_port", influxdb_port)
        storage.set("influxdb_username", influxdb_username)
        if influxdb_password:
            storage.set("influxdb_password", influxdb_password)

    success = True
    message = "Settings saved successfully"
    if error:
        success = False
        message = error

    return jsonify(success=success, message=message)

def action_save_metrics():
    metrics = request.get_json()

    metrics_validated = []
    error = None
    for metric in metrics:
        topic = metric.get("topic")
        measurement = metric.get("measurement")
        database = metric.get("database")
        type_name = metric.get("type")

        if not (topic.strip() and measurement.strip() and database.strip()):
            error = "All metrics must have a topic, measurement and database"

        if type_name not in ["string", "integer", "float"]:
            error = f"{type_name} is not a valid type"
        
        metrics_validated.append({
            "topic": topic,
            "measurement": measurement,
            "database": database,
            "type": type_name
        })

    message = error
    if not error:
        storage.set("metrics", metrics_validated)
        message = "Metrics saved successfully"

    control.subscribe_to_all()

    return jsonify(success=(error==None), message=message)
    
def initialise(module_id):
    web.add_endpoint(module_id, "/", view_index, ["GET"])
    web.add_endpoint(module_id, "/settings/", view_settings, ["GET"])
    web.add_endpoint(module_id, "/metrics/", view_metrics, ["GET"])
    web.add_endpoint(module_id, "/action/save_settings/", action_save_settings,
            ["POST"])
    web.add_endpoint(module_id, "/action/save_metrics/", action_save_metrics,
            ["POST"])