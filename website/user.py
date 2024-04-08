from flask import Flask, request, jsonify
from functools import wraps
from models import User, DailyMenu, Food, MonthlyMenu, Order  
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
    total_amount = 0
    for item in order_items:
        food_id = item.get('food_id')
        quantity = item.get('quantity', 1) # Default to 1 if quantity is not provided
      
    last_order = Order.query.order_by(Order.order_id.desc()).first()
    if last_order:
      token_value = last_order.token + 1
    else:
      token_value = 1


        # Retrieve food details
        food = Food.query.get(food_id)
        if not food:
            return jsonify({'message': 'Food item not found'}), 404

        # Calculate total price for the item
        total_price = food.price * quantity
        total_amount += total_price

        # Update bought count in Food table
        food.bought_count += quantity

        
        order_item = OrderItem(food_id=food_id, quantity=quantity, total_price=total_price)
        db.session.add(order_item)

    # Check if wallet balance is sufficient
    if current_user.wallet < total_amount:
        return jsonify({'message': 'Insufficient balance'}), 400

    # Deduct total amount from wallet balance
    current_user.wallet -= total_amount

    # Add the order to the orders table
    order = Order(user_id=current_user.user_id, token=jwt.encode({'user_id': current_user.user_id}, app.config['SECRET_KEY'], algorithm='HS256'), status='Ordered', total_amount=total_amount, items=order_items)
    db.session.add(order)

    # Commit the changes to the database
    db.session.commit()

    # Return the token and order details
    return jsonify({'order_token': order.token, 'order_details': order_items}), 200


