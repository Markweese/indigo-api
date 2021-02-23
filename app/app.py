import json
import flask
from segmentation_module import segmentation_module
from flask import request, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
segmentation_module = segmentation_module()

# The view
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/logic/update', methods=['POST'])
def post_logic(code):
    try:
        formatted = request.args.get('formatted')
        selection = segmentation_module.post_logic(code, formatted)

        return dict({
            status: 200,
            message: 'Successfully updated logic'
        })
    except Exception as e:
        return dict({
            status: 500,
            message: 'Error, please reach out to Mark if you cannot resolve'
        })

    return selection

@app.route('/api/events/new', methods=['POST'])
def post_events_csv(name):
    try:
        formatted = request.args.get('formatted')
        selection = segmentation_module.post_events(name, formatted)

        return dict({
            status: 200,
            message: 'Successfully added file'
        })
    except Exception as e:
        return dict({
            status: 500,
            message: 'Error, please reach out to Mark if you cannot resolve'
        })

    return selection

@app.route('/api/users/get', methods=['GET'])
def get_user_segments(name):
    try:
        formatted = request.args.get('formatted')
        output = segmentation_module.get_segments(name, formatted)
        return output
    except Exception as e:
        return dict({
            status: 500,
            message: 'Error, please reach out to Mark if you cannot resolve'
        })

    return selection

@app.route('/api/user/get/:id', methods=['GET'])
def get_user_segment(id):
    try:
        output = segmentation_module.get_segment(name, formatted)
        return output
    except Exception as e:
        return dict({
            status: 500,
            message: 'Error, please reach out to Mark if you cannot resolve'
        })

    return selection


@app.route('/api/segments/get/', methods=['GET'])
def get_all_segments():
    try:
        with open('data/segments.json', 'r') as segments:
            pj = json.loads(segments.read())
            return json.dumps(pj)
    except Exception as e:
        return dict({
            status: 500,
            message: 'Error, please reach out to Mark if you cannot resolve'
        })

    return selection

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
