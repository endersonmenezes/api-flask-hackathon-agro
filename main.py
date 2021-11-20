from flask import Flask
import os

app = Flask('app')

@app.route('/')
def hello_world():
  return 'Hello, World!'

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)
