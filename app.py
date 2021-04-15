# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 06:54:30 2019

@author: AHIABA
"""

import os
from flask import Flask, jsonify, request

from .lib.lib import generate_conditions

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Welcome"


@app.route("/simulate", methods=["POST"])
def simulate():
    file = os.getenv("GEOTIFF_FILE")
    input_data = request.get_json()
    simulation = generate_conditions(
        file, input_data.get("waveAngle"), input_data.get("wavePeriod")
    )
    return jsonify({"image": "{}static/{}".format(request.host_url, simulation)})
