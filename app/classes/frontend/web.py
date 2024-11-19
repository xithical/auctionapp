from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    send_from_directory,
    abort
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user
)

from app.classes.controllers.admin import Admin_Controllers
from app.classes.controllers.login import User_Login_Controller
from app.classes.controllers.auction_items import Auction_Items_Controller

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.event_helpers import Event_Helpers

app = Flask('__main__', template_folder='app/classes/frontend/templates')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: str):
    return User_Login_Controller.get_user(user_id)

@app.route('/', methods=['GET'])
def entrypoint():
    return redirect("/login")

@login_manager.unauthorized_handler
def unauthed_request():
    match request.path:
        case '/login':
            return redirect('/login')
        case '/admin/login':
            return redirect('/admin/login')
        
        case _:
            return redirect('/login')

@app.route('/static/assets/<path:path>', methods=['GET'])
def get_static_asset(path):
    return send_from_directory('app/classes/frontend/templates/assets', path)

###################################
#           User Views            #
###################################
@app.route('/login', methods=['GET','POST'])
def user_login():
    match request.method:
        case 'GET':
            org_name = Config_Helpers.get_entity_name()
            return render_template('SignIn.html', org_name=org_name)
        case 'POST':
            email = request.form['email']
            password = request.form['password']
            event_code = request.form['auction_code']
            user = User_Login_Controller.login_user(email, password, event_code)
            if user is not None:
                login_user(user)
                return redirect(f"/events/{Event_Helpers.get_event_id(event_code)}/items")
            else:
                return redirect("/login")
            
@app.route('/events/<int:event_id>/items', methods=['GET'])
@login_required
def auction_items(event_id):
    items = Auction_Items_Controller.get_items(event_id)
    return render_template('Auctions.html', items=items, event_id=event_id)

@app.route('/events/<int:event_id>/items/<int:item_id>', methods=['GET','POST'])
@login_required
def item_details(event_id, item_id):
    match request.method:
        case 'GET':
            item = Auction_Items_Controller.get_item_details(item_id)
            if item["event_id"] == event_id:
                return render_template("AuctionItemInformation.html", item=item, event_id=event_id)
            else:
                return redirect(f"/events/{event_id}/items")
        case 'POST':
            return

###################################
#           Admin Views           #
###################################
@app.route('/admin', methods=['GET'])
def admin_entrypoint():
    return redirect("/admin/login")

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    match request.method:
        case 'GET':
            org_name = Config_Helpers.get_entity_name()
            return render_template("Admin-SignIn.html", org_name=org_name)
        case 'POST':
            email = request.form['email']
            password = request.form['password']
            user = User_Login_Controller.login_admin(email, password)
            if user is not None:
                login_user(user)
                return redirect("/admin/auth-placeholder")
            else:
                return redirect("/admin/login")

@app.route('/admin/events', methods=['GET','POST'])
@login_required
def admin_events():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                events = Admin_Controllers.EventAdmin_Controller.list_events()
                return render_template("Admin-Auctions.html", events=events)
            case 'POST':
                return
    else:
        abort(403)

###################################
#        Auth Placeholders        #
###################################
@app.route('/auth-placeholder', methods=['GET'])
@login_required
def test_page():
    return "Auth worked"

@app.route('/admin/auth-placeholder', methods=['GET'])
@login_required
def test_admin_page():
    if User_Login_Controller.is_admin(current_user.user_id):
        return "Admin auth worked"
    else:
        return redirect("/login")