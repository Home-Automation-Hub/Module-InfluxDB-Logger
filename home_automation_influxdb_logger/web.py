from home_automation_hub import web
from flask import render_template, request, jsonify
from . import storage, websockets as ws

def view_index():
    return render_template("influxdb_logger/index.html")

def initialise(module_id):
    web.add_endpoint(module_id, "/", view_index, ["GET"])