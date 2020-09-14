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

@app.route('/api/state/<code>', methods=['GET'])
def get_state(code):
    formatted = request.args.get('formatted')
    selection = crop_module.get_state(code, formatted)

    return selection

@app.route('/api/crop/<name>', methods=['GET'])
def get_crop(name):
    formatted = request.args.get('formatted')
    selection = crop_module.get_crop(name, formatted)

    return selection

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
