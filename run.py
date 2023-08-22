from market import app, db
from market.models import Order, OrderItems, User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Order': Order, 'OrderItem': User}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
