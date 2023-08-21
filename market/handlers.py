from flask import session

from market.models import Item


def handle_cart():
    products = []
    total_cart = 0
    index = 0
    if 'cart' not in session:
        session['cart'] = []
    for item in session['cart']:
        product = Item.query.filter_by(id=item['id']).first()
        quantity = int(item['quantity'])
        total = quantity * product.price
        total_cart += total
        products.append(
            {'id': product.id, 'name': product.title, 'price': product.price, 'total': total, 'color': product.color,
             'image': product.image, 'quantity': quantity, 'index': index})
        index += 1
    return products, total_cart
