import json
import flask
from crop_module import crop_module
from flask import request, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
crop_module = crop_module()

# The view
@app.route("/")
def index():
    return render_template("index.html")

# The API
@app.route('/api/county/<fips>', methods=['GET'])
def get_county(fips):
    selection = crop_module.get_county(fips)
    return selection

@app.route('/api/state/<code>', methods=['GET'])
def get_state(code):
    selection = crop_module.get_state(code)
    return selection

@app.route('/api/crop/<name>', methods=['GET'])
def get_crop_overview(name):
    selection = crop_module.get_crop(name)
    return selection

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
