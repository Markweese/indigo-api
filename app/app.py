import json
import flask
from flask import Response
from segmentation_module import segmentation_module
from logic_editor_module import logic_editor_module
from flask import request, render_template

app = flask.Flask(__name__)
app.config["DEBUG"] = True
segmentation_module = segmentation_module()
logic_editor_module = logic_editor_module()

# The view
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/logic/update', methods=['POST'])
def post_logic():
    try:
        segment_obj = request.get_json()

        try:
            logic_editor_module.update_logic(segment_obj)
        except Exception as e:
            return dict(
                status=500,
                message='Error, please reach out to Mark if you cannot resolve'
            )

        return dict(
            status=200,
            message='Successfully updated logic'
        )
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

    return selection

@app.route('/api/logic/delete', methods=['POST'])
def delete_logic():
    try:
        segment_obj = request.get_json()

        try:
            logic_editor_module.delete_logic(segment_obj)
        except Exception as e:
            return dict(
                status=500,
                message='Error, please reach out to Mark if you cannot resolve'
            )

        return dict(
            status=200,
            message='Successfully updated logic'
        )
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

    return selection

@app.route('/api/events/new', methods=['POST'])
def post_events_csv(name):
    try:
        formatted = request.args.get('formatted')
        selection = segmentation_module.post_events(name, formatted)

        return dict(
            status=200,
            message='Successfully added file'
        )
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

    return selection

@app.route('/api/users/get', methods=['GET'])
def get_user_segments():
    try:
        output = segmentation_module.derive_segments()
        return Response(json.dumps(output), mimetype='application/json')
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

@app.route('/api/user/get/segments/<id>', methods=['GET'])
def get_user_segment(id):
    try:
        output = segmentation_module.derive_user_segment(id)
        return Response(json.dumps(output), mimetype='application/json')
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

@app.route('/api/user/get/events/<id>', methods=['GET'])
def get_user_events(id):
    try:
        output = segmentation_module.get_user_events(id)
        return Response(json.dumps(output), mimetype='application/json')
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

@app.route('/api/segments/get/', methods=['GET'])
def get_all_segments():
    try:
        with open('data/segments.json', 'r') as segments:
            pj = json.loads(segments.read())
            return json.dumps(pj)
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

    return selection

@app.route('/api/usernames/get/', methods=['GET'])
def get_all_usernames():
    try:
        output = segmentation_module.get_usernames()
        return json.dumps(output)
    except Exception as e:
        return dict(
            status=500,
            message='Error, please reach out to Mark if you cannot resolve'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
