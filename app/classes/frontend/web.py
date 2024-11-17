from flask import Flask, render_template, jsonify, request, redirect, send_from_directory

from app.classes.helpers.config_helpers import Config_Helpers

app = Flask('__main__', template_folder='app/classes/frontend/templates')

@app.route('/', methods=['GET'])
def entrypoint():
    return redirect("/login")

@app.route('/static/assets/<path:path>', methods=['GET'])
def get_static_asset(path):
    return send_from_directory('app/classes/frontend/templates/assets', path)

@app.route('/login', methods=['GET','POST'])
def user_login():
    match request.method:
        case 'GET':
            org_name = Config_Helpers.get_entity_name()
            return render_template('SignIn.html', org_name=org_name)
        case 'POST':
            return