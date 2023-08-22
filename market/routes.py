from flask import render_template, redirect, url_for, flash, session
from flask_admin import AdminIndexView, expose, Admin
from flask_admin.contrib.sqla import ModelView
from market.handlers import handle_cart
from market import app, db, login_manager
from market.models import Item, User, Order, OrderItems
from market.forms import RegisterForm, LogInForm, AddToCart, CheckoutForm
from flask_login import login_user, logout_user, login_required
from market import celery
from jsonrpc.backend.flask import api

app.register_blueprint(api.as_blueprint())
app.add_url_rule('/api', 'api', api.as_view(), methods=['POST'])


@api.dispatcher.add_method
def get_order_status(order_num):
    order = Order.query.filter_by(id=order_num).first()
    return order.status


@app.route('/', methods=['POST', 'GET'])
def catalog_page():
    items = Item.query.order_by(Item.price).all()
    add_to_cart_form = AddToCart()
    return render_template('catalog.html', data=items, cart_form=add_to_cart_form)


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []
    form = AddToCart()
    if form.validate_on_submit():
        session['cart'].append({'id': form.id.data, 'quantity': form.quantity.data})
        session.modified = True

    else:
        print(form.errors)
    return redirect(url_for('catalog_page'))


@app.route('/cart', methods=['GET', "POST"])
@login_required
def cart_page():
    checkout_form = CheckoutForm()
    products, total_cart = handle_cart()
    if checkout_form.validate_on_submit():
        total_quantity = sum([p['quantity'] for p in products])

        order = Order()
        checkout_form.populate_obj(order)
        order.status = 'PENDING'
        order.total_quantity = total_quantity

        for product in products:
            order_item = OrderItems(product_id=product['id'], quantity=product['quantity'])
            order.items.append(order_item)

        db.session.add(order)
        db.session.commit()
        return redirect(url_for('succeed_order'))

    else:
        for err_msg in checkout_form.errors.values():
            flash(f"Error with creating user: {err_msg}", category='danger')

    return render_template('cart.html', items=products, total_cart=total_cart, checkout_form=checkout_form)


@app.route('/succeed-order')
@login_required
def succeed_order():
    return render_template('order_success.html')


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index)]
    session.modified = True
    return redirect(url_for('cart_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors != {}:  # if no errors
        for err_msg in form.errors.values():
            flash(f"Error with creating user: {err_msg}", category='danger')
    return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LogInForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are signed in as: {attempted_user.username}', category='success')
            return redirect(url_for('catalog_page'))
        else:
            flash(f'Username and password are not match! Please try again.', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('catalog_page'))


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        orders = Order.query.all()
        all_items = Item.query.all()
        return self.render('admin/index.html', orders=orders, items=all_items)


admin = Admin(app, index_view=MyHomeView(name='Dashboard'), template_mode='bootstrap3')


@celery.task
def create_order_status_history(order_id, status):
    with open('order_status_history', 'a') as file:
        file.write(f'Order: {order_id} changed status to {status}')


class OrderViewAdmin(ModelView):
    form_choices = {
        'status': [
            ('COMPLETED', 'COMPLETED'),
            ('PROCESSING', 'PROCESSING'),
            ('CANCELED', 'CANCELED'),
        ]
    }

    def on_model_change(self, form, model, is_created):
        if form.data['status']:
            create_order_status_history.delay(model.id, model.status)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Item, db.session))
admin.add_view(OrderViewAdmin(Order, db.session))
