import os

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    send_from_directory,
    abort,
    session
)
from flask_login import (
    LoginManager,
    login_required,
    login_user,
    current_user
)
from werkzeug.utils import secure_filename

from app.classes.controllers.admin import Admin_Controllers
from app.classes.controllers.login import User_Login_Controller, User_Registration_Controller
from app.classes.controllers.auction_items import Auction_Items_Controller
from app.classes.controllers.checkout import Checkout_Controller
from app.classes.controllers.merchandise import Merchandise_Item_Controller

from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers
from app.classes.helpers.auth_helpers import Auth_Helpers
from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.event_helpers import Event_Helpers
from app.classes.helpers.payments_helpers import Payments_Helpers

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))

login_manager = LoginManager()
login_manager.init_app(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates/assets'), path)

@app.route('/uploads/<filename>')
def get_uploads(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

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
                return redirect(f"/login/{event_code}")
            else:
                return redirect("/login")
            
@app.route('/register', methods=['GET','POST'])
def user_register():
    match request.method:
        case 'GET':
            org_name = Config_Helpers.get_entity_name()
            return render_template('SignUp.html', org_name=org_name)
        case 'POST':
            new_user = User_Registration_Controller.register_user(
                user_firstname=request.form["user_firstname"],
                user_lastname=request.form["user_lastname"],
                user_email=request.form["user_email"],
                user_phone=request.form["user_phone"],
                user_password=request.form["user_password"],
                event_code=request.form["event_code"]
            )
            if new_user is not False:
                user = User_Login_Controller.get_user(new_user)
                login_user(user)
                return redirect(f"/login/{request.form['event_code']}")
            else:
                return redirect("/register")
            
@app.route('/login/<string:event_code>', methods=['GET'])
@login_required
def event_login(event_code):
    session["event_id"] = Event_Helpers.get_event_id(event_code)
    return redirect("/event/items")

@app.route('/card_setup', methods=['GET'])
@login_required
def card_setup():
    customer_id = Payments_Helpers.verify_customer(current_user.user_id)
    return redirect(Payments_Helpers.create_checkout_session(
        customer_id=customer_id,
        success_url=f"{request.base_url}/card_add?session_id={{CHECKOUT_SESSION_ID}}"
    )["url"])

@app.route('/card_setup/card_add', methods=['GET'])
@login_required
def card_add():
    user_id = current_user.user_id
    event_id = session["event_id"]
    checkout_session = request.args.get('session_id')
    if not Payments_Helpers.verify_checkout_session(checkout_session):
        return redirect("/card_setup")
    Checkout_Controller.create_cart(user_id, event_id, checkout_session)
    return redirect("/event/items")
            
@app.route('/event/items', methods=['GET'])
@login_required
def auction_items():
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "cart":
            return redirect("/card_setup")
    event_id = session["event_id"]
    items = Auction_Items_Controller.get_items(event_id)
    return render_template('Auctions.html', items=items)

@app.route('/event/items/<int:item_id>', methods=['GET','POST'])
@login_required
def item_details(item_id):
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "item_id":
            return redirect("/event/items")
        elif validate_session == "cart":
            return redirect("/card_setup")
    item = Auction_Items_Controller.get_item_details(item_id)
    match request.method:
        case 'GET':
            return render_template("AuctionItemInformation.html", item=item, event_id=session["event_id"])
        case 'POST':
            item = Auction_Items_Controller.get_item_details(item_id)
            bid = Auction_Items_Controller.place_bid(
                item_id=item_id,
                bid_amount=request.form["bid_amount"],
                user_id=current_user.user_id
            )
            if bid is not None:
                return redirect("/event/items")
            else:
                return redirect(f"/event/items/{item_id}")

@app.route('/cart', methods=['GET'])
@login_required
def user_cart():
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "cart":
            return redirect("/card_setup")
    event_id = session["event_id"]
    cart = Checkout_Controller.get_cart(current_user.user_id, event_id)
    auction_items = cart["auction_items"]["items"]
    merch_items = cart["merch_items"]["items"]
    auction_total = cart["auction_items"]["price_total"]
    merch_total = cart["merch_items"]["price_total"]
    total = auction_total + merch_total
    return render_template("Cart.html",
        auction_items=auction_items,
        merch_items=merch_items,
        auction_total=auction_total,
        merch_total=merch_total,
        total=total
    )

@app.route('/cart/remove', methods=['POST'])
@login_required
def cart_remove():
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "cart":
            return redirect("/card_setup")
    event_id = session["event_id"]
    entry_id = request.args.get("entry_id")
    cart_id = Checkout_Controller.get_cart(current_user.user_id, event_id)["cart_id"]
    Checkout_Controller.remove_merchcart_entry(cart_id, entry_id)
    return redirect("/cart")

@app.route('/merch', methods=['GET'])
@login_required
def merch_items():
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "cart":
            return redirect("/card_setup")
    event_id = session["event_id"]
    merch_items = Merchandise_Item_Controller.list_items()
    return render_template("Merchandise.html", merch_items=merch_items)

@app.route('/merch/<int:item_id>', methods=['GET','POST'])
@login_required
def merch_item_details(item_id):
    validate_session = Auth_Helpers.validate_session(
        current_user,
        session
    )
    if validate_session is not True:
        if validate_session == "event_id":
            return redirect("/login")
        elif validate_session == "cart":
            return redirect("/card_setup")
    event_id = session["event_id"]
    match request.method:
        case 'GET':
            item = Merchandise_Item_Controller.get_merch_item_details(item_id)
            return render_template("MerchandiseItemInfo.html", item=item)
        case 'POST':
            Merchandise_Item_Controller.add_item_to_cart(
                item_id = item_id,
                user_id = current_user.user_id,
                event_id = event_id
            )
            return redirect("/merch")

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
                return redirect("/admin/events")
            else:
                return redirect("/admin/login")

@app.route('/admin/events', methods=['GET','POST','PUT','DELETE'])
@login_required
def admin_events():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                events = Admin_Controllers.EventAdmin_Controller.list_events()
                return render_template("Admin-Auctions.html", events=events)
            case 'POST':
                if request.form['StartTime'] < request.form['EndTime']:
                    Admin_Controllers.EventAdmin_Controller.create_event(
                        event_name = request.form['EventName'],
                        start_time = request.form['StartTime'],
                        end_time = request.form['EndTime']
                    )
                return redirect("/admin/events")
            case 'PUT':
                data = request.get_json()
                Admin_Controllers.EventAdmin_Controller.update_event(
                    event_id = data["event_id"],
                    event_name = data["event_name"],
                    start_time = data["start_time"],
                    end_time = data["end_time"]
                )
                return redirect("/admin/events")
            case 'DELETE':
                Admin_Controllers.EventAdmin_Controller.delete_event(
                    request.get_json()["event_id"]
                )
                return redirect("/admin/events")
    else:
        abort(403)

@app.route('/admin/events/<int:event_id>/items', methods=['GET','DELETE'])
@login_required
def admin_auction_items(event_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                items = Admin_Controllers.EventAdmin_Controller.list_auction_items(event_id)
                return render_template("Admin-Auctions-Items.html", event_id=event_id, items=items)
            case 'DELETE':
                Admin_Controllers.EventAdmin_Controller.delete_auction_item(
                    request.get_json()["item_id"]
                )
                return redirect(f"/admin/events/{event_id}/items")
    else:
        abort(403)

@app.route('/admin/events/<int:event_id>/items/new', methods=['GET','POST'])
@login_required
def admin_new_auction_item(event_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                item = {
                    "item_title": "Item Title",
                    "donor_id": None,
                    "item_description": "Item Description",
                    "item_value": "Item Value"
                }
                donors = Admin_Controllers.DonorAdmin_Controller.list_donors()
                donor_list = []
                for donor in donors:
                    donor_out = {
                        "donor_id": donor["donor_id"],
                        "donor_name": Auction_Items_Helpers.get_donor_name(donor["donor_id"])
                    }
                    donor_list.append(donor_out)
                return render_template("Admin-Auctions-Items-Modify.html", event_id=event_id, item=item, donors=donor_list)
            case 'POST':
                file = request.files['file']
                item_image = "/static/assets/img/placeholder1.png"
                if not file.filename == "":
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        item_image = f"/uploads/{filename}"
                Admin_Controllers.EventAdmin_Controller.create_auction_item(
                    item_title=request.form["item_title"],
                    item_description=request.form["item_description"],
                    item_price=float(request.form["item_price"]),
                    item_image=item_image,
                    donor_id=int(request.form["donor_id"]),
                    event_id=event_id
                )
                return redirect(f"/admin/events/{event_id}/items")
    else:
        abort(403)

@app.route('/admin/events/<int:event_id>/items/<int:item_id>', methods=['GET','POST'])
@login_required
def admin_edit_auction_item(event_id, item_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                item = Admin_Controllers.EventAdmin_Controller.get_auction_item(item_id)
                donors = Admin_Controllers.DonorAdmin_Controller.list_donors()
                donor_list = []
                for donor in donors:
                    donor_out = {
                        "donor_id": donor["donor_id"],
                        "donor_name": Auction_Items_Helpers.get_donor_name(donor["donor_id"])
                    }
                    donor_list.append(donor_out)
                return render_template("Admin-Auctions-Items-Modify.html", event_id=event_id, item=item, donors=donor_list)
            case 'POST':
                file = request.files['file']
                item_image = Admin_Controllers.EventAdmin_Controller.get_auction_item(item_id).item_image
                if not file.filename == "":
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        item_image = f"/uploads/{filename}"
                Admin_Controllers.EventAdmin_Controller.update_auction_item(
                    item_id=item_id,
                    item_title=request.form["item_title"],
                    item_description=request.form["item_description"],
                    item_price=float(request.form["item_price"]),
                    item_image=item_image,
                    donor_id=int(request.form["donor_id"]),
                    event_id=event_id,
                    is_active=True
                )
                return redirect(f"/admin/events/{event_id}/items")
    else:
        abort(403)

@app.route('/admin/events/<int:event_id>/items/<int:item_id>/bids', methods=['GET','DELETE'])
@login_required
def admin_item_bids(event_id, item_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                bids = Admin_Controllers.EventAdmin_Controller.get_item_bids(item_id)
                return render_template("Admin-Item-Bids.html", event_id=event_id, bids=bids)
            case 'DELETE':
                data = request.get_json()
                Admin_Controllers.EventAdmin_Controller.delete_bid(data["item_id"])
                return redirect(f"/admin/events/{event_id}/items/{item_id}/bids")
    else:
        abort(403)

@app.route('/admin/merch', methods=['GET','DELETE'])
@login_required
def admin_merch_items():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                items = Admin_Controllers.MerchAdmin_Controller.list_merch_items()
                return render_template("Admin-Auctions-Merchandise.html", items=items)
            case 'DELETE':
                Admin_Controllers.MerchAdmin_Controller.delete_merch_item(
                    int(request.get_json()["item_id"])
                )
                return redirect("/admin/merch")
    else:
        abort(403)

@app.route('/admin/merch/new', methods=['GET','POST'])
@login_required
def admin_merch_new():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                item = {
                    "merch_title": "Item Title",
                    "merch_description": "Item description",
                    "merch_price": 0
                }
                return render_template("Admin-Auctions-Merchandise-Modify.html", item=item)
            case 'POST':
                file = request.files['file']
                item_image = "/static/assets/img/placeholder1.png"
                if not file.filename == "":
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        item_image = f"/uploads/{filename}"
                Admin_Controllers.MerchAdmin_Controller.create_merch_item(
                    merch_title=request.form["item_title"],
                    merch_description=request.form["item_description"],
                    merch_price=float(request.form["item_price"]),
                    merch_image = item_image
                )
                return redirect("/admin/merch")
    else:
        abort(403)

@app.route('/admin/merch/<int:merch_id>', methods=['GET','POST'])
@login_required
def admin_merch_edit(merch_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                item = Admin_Controllers.MerchAdmin_Controller.get_merch_item(merch_id)
                return render_template("Admin-Auctions-Merchandise-Modify.html", item=item)
            case 'POST':
                file = request.files['file']
                item_image = Admin_Controllers.MerchAdmin_Controller.get_merch_item(merch_id).merch_image
                if not file.filename == "":
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        item_image = f"/uploads/{filename}"
                Admin_Controllers.MerchAdmin_Controller.modify_merch_item(
                    merch_id=merch_id,
                    merch_title=request.form["item_title"],
                    merch_description=request.form["item_description"],
                    merch_price=float(request.form["item_price"]),
                    merch_image=item_image
                )
                return redirect("/admin/merch")
    else:
        abort(403)

@app.route('/admin/donors', methods=['GET','POST','PUT','DELETE'])
@login_required
def admin_donors():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                donors = Admin_Controllers.DonorAdmin_Controller.list_donors()
                return render_template("Admin-Donors.html", donors=donors)
            case 'POST':
                if request.form["UserCompany"] == "":
                    donor_company = None
                else:
                    donor_company = request.form["UserCompany"]
                Admin_Controllers.DonorAdmin_Controller.create_donor(
                    donor_firstname = request.form["UserFirst"],
                    donor_lastname = request.form["UserLast"],
                    donor_email = request.form["UserEmail"],
                    donor_phone = request.form["UserPhone"],
                    company_name = donor_company
                )
                return redirect("/admin/donors")
            case 'PUT':
                data = request.get_json()
                match data["UserCompany"]:
                    case None:
                        donor_company = None
                    case "":
                        donor_company = None
                    
                    case _:
                        donor_company = data["UserCompany"]
                Admin_Controllers.DonorAdmin_Controller.update_donor(
                    donor_id = data["donor_id"],
                    donor_firstname = data["UserFirst"],
                    donor_lastname = data["UserLast"],
                    donor_email = data["UserEmail"],
                    donor_phone = data["UserPhone"],
                    company_name = donor_company
                )
                return redirect("/admin/donors")
            case 'DELETE':
                data = request.get_json()
                Admin_Controllers.DonorAdmin_Controller.delete_donor(
                    donor_id = data["donor_id"]
                )
                return redirect("/admin/donors")

    else:
        abort(403)

@app.route('/admin/donors/<int:donor_id>/items', methods=['GET'])
@login_required
def admin_donors_items(donor_id):
    if User_Login_Controller.is_admin(current_user.user_id):
        items = Admin_Controllers.DonorAdmin_Controller.list_donor_items(donor_id)
        return render_template("Admin-Donor-Information.html", items=items)
    else:
        abort(403)

@app.route('/admin/config', methods=['GET','POST'])
@login_required
def admin_config():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                config = Admin_Controllers.Config_Controller.get_config()
                return render_template("Admin-Settings.html", config=config)
            case 'POST':
                file = request.files['entity_logo']
                logo_image = Config_Helpers.get_entity_logo()
                if not file.filename == "":
                    if allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        logo_image = f"/uploads/{filename}"
                Admin_Controllers.Config_Controller.update_config(
                    min_bid_percent = request.form["min_bid_percent"],
                    min_bid_amount = round(float(request.form["min_bid_amount"])),
                    entity_name = request.form["entity_name"],
                    entity_logo = logo_image,
                    primary_color = request.form["primary_color"],
                    secondary_color = request.form["secondary_color"],
                    tax_id = request.form["tax_id"],
                    stripe_api_key = request.form["stripe_api_key"]
                )
                return redirect("/admin/config")
    else:
        abort(403)

@app.route('/admin/config/regen-secrets', methods=['GET'])
@login_required
def admin_regen_secrets():
    if User_Login_Controller.is_admin(current_user.user_id):
        Admin_Controllers.Config_Controller.regen_secret()
        return redirect("/admin/login")
    else:
        abort(403)

@app.route('/admin/users', methods=['GET','POST','PUT','DELETE'])
@login_required
def admin_users():
    if User_Login_Controller.is_admin(current_user.user_id):
        match request.method:
            case 'GET':
                users = Admin_Controllers.UserAdmin_Controller.list_users()
                return render_template("Admin-UserInfo.html", users=users)
            case 'POST':
                data = request.get_json()
                Admin_Controllers.UserAdmin_Controller.create_user(
                    user_firstname = data["user_firstname"],
                    user_lastname = data["user_lastname"],
                    user_email = data["user_email"],
                    user_phone = data["user_phone"],
                    user_password = data["user_password"],
                    type_id = data["type_id"]
                )
                return redirect("/admin/users")
            case 'PUT':
                data = request.get_json()
                Admin_Controllers.UserAdmin_Controller.update_user(
                    user_id = data["user_id"],
                    user_firstname = data["user_firstname"],
                    user_lastname = data["user_lastname"],
                    user_email = data["user_email"],
                    user_phone = data["user_phone"],
                    user_password = data["user_password"],
                    type_id = data["type_id"]
                )
                return redirect("/admin/users")
            case 'DELETE':
                data = request.get_json()
                Admin_Controllers.UserAdmin_Controller.delete_user(
                    user_id = data["user_id"]
                )
                return redirect("/admin/users")
    else:
        abort(403)

@app.route('/admin/users/get_roles', methods=['GET'])
@login_required
def admin_get_roles():
    if User_Login_Controller.is_admin(current_user.user_id):
        return jsonify({"roles": Admin_Controllers.UserAdmin_Controller.list_roles()})
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