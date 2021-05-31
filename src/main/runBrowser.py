#!/usr/bin/python3

import os

from src.main.app import app

app.debug = True
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
