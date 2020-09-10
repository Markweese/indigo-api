import json
import flask
from flask import request
from crop_module import crop_module

app = flask.Flask(__name__)
app.config["DEBUG"] = True
crop_module = crop_module()

# API Documentation
@app.route('/api/county/<fips>', methods=['GET'])
def get_county(fips):
    selection = crop_module.get_county(fips)
    return selection

@app.route('/api/state/<code>', methods=['GET'])
def get_state(code):
    selection = crop_module.get_state(code)
    return selection

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
