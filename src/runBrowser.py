#!/usr/bin/python3

from app import app 
import os 

app.debug = True
port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
