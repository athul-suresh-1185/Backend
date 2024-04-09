from flask import Flask, request, jsonify
from functools import wraps
from models import User, DailyMenu, Food, MonthlyMenu, Order, OrderItem  
import jwt
from auth import token_required

@app.route('/', methods=['GET'])
@token_required
def home(current_user):

    wallet_details = {
        'balance': current_user.wallet
    }

    food_details = []
    for daily_menu in daily_menu_items:
        food = Food.query.get(daily_menu.food_id)
        food_dict = {
            'food_id': daily_menu.food_id,
            'item_name': food.item_name,
            'bought_count': food.bought_count,
            'price': food.price
        }
        food_details.append(food_dict)

    
    data = {
        'wallet_details': wallet_details,
        'daily_menu': food_details
    }

    
    return jsonify(data)


def place_order(current_user):
    # Get data from the request
    order_data = request.json
    order_items = order_data.get('items', [])

    # Calculate total amount based on order items
    total_amount = sum(item['total_price'] for item in order_items)

    # Increment the order token value
    last_order = Order.query.order_by(Order.order_id.desc()).first()
    token_value = 1 if last_order is None else last_order.token + 1

    # Check if wallet balance is sufficient
    if current_user.wallet < total_amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Deduct total amount from wallet balance
    current_user.wallet -= total_amount

    # Create OrderItem instances and add them to the list of order items
    order_items_instances = []
    for item in order_items:
        food_id = item.get('food_id')
        quantity = item.get('quantity', 1)  # Default to 1 if quantity is not provided

        # Retrieve food details
        food = Food.query.get(food_id)
        if not food:
            return jsonify({'message': 'Food item not found'}), 404

        # Update bought count in Food table
        food.bought_count += quantity

        # Create an OrderItem and add it to the list of order items
        order_item = OrderItem(food_id=food_id, quantity=quantity, total_price=item['total_price'])
        order_items_instances.append(order_item)

    # Create the order
    order = Order(user_id=current_user.user_id, token=token_value, status='Delivered', total_amount=total_amount, items=order_items_instances)
    db.session.add(order)

    try:
        # Commit the changes to the database
        db.session.commit()
        # Return the token and order details with status "Delivered"
        return jsonify({'order_token': order.token, 'order_details': order_items, 'status': 'Delivered'}), 200
    except:
        # Rollback changes if an error occurs
        db.session.rollback()
        return jsonify({'message': 'Failed to place order. Please try again later.'}), 500



def get_recent_order_history(current_user):
    try:
        # Query recent 5 order history for the current user
        recent_orders = Order.query.filter_by(user_id=current_user.user_id).order_by(Order.order_date.desc()).limit(5).all()

        # Serialize order data into JSON format
        order_history = []
        for order in recent_orders:
            # Get ordered items for the current order
            ordered_items = OrderItem.query.filter_by(order_id=order.order_id).all()
            items_list = []
            for item in ordered_items:
                item_data = {
                    'food_id': item.food_id,
                    'item_name': item.food.item_name,
                    'quantity': item.quantity
                }
                items_list.append(item_data)

            # Serialize order data including ordered items
            order_data = {
                'order_id': order.order_id,
                'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),  # Convert datetime to string
                'total_amount': order.total_amount,
                'status': order.status,
                'items': items_list
            }
            order_history.append(order_data)

        return jsonify({'order_history': order_history}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to fetch order history. Please try again later.', 'error': str(e)}), 500
