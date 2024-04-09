from flask import Flask, request, jsonify
from functools import wraps
from models import User, DailyMenu, Food, MonthlyMenu, Order, OrderItem  
import jwt
from auth import token_required

@app.route('/', methods=['GET'])
@token_required

def show_monthly_menu(current_user):

food_details = []
for monthly_menu in monthly_menu_items:
    food = Food.query.get(monthly_menu.food_id)
    food_dict = {
        'food_id': monthly_menu.food_id,
        'item_name': food.item_name,
        'bought_count': food.bought_count,
        'price': food.price
    }
    food_details.append(food_dict)


data = {
    'monthly_menu': food_details
}


return jsonify(data)

def show_daily_menu(current_user):

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
    'daily_menu': food_details
}


return jsonify(data)

def delete_daily_menu(food_id):
if current_user.id == 1:
    try:
        item_to_delete = DailyMenu.query.get(food_id)
        db.session.delete(item_to_delete)
        db.session.commit()
        flash('One Item deleted')
        return redirect('/food-items')
    except Exception as e:
        print('Item not deleted', e)
        flash('Item not deleted!!')
    return redirect('/food-items')

return render_template('404.html')

def add_food_items():
food_details = []
for monthly_menu in monthly_menu_items:
    food = Food.query.get(monthly_menu.food_id)
        food_id = monthly_menu.food_id,
        item_name = food.item_name,
        bought_count = food.bought_count,
        price = food.price

        file_name = secure_filename(file.filename)

        file_path = f'./media/{file_name}'

        file.save(file_path)

        new_food_item = DailyMenu()
        new_food_item.food_id = food_id
        new_food_item.item_name = item_name
        new_food_item.price = price


        try:
            db.session.add(new_food_item)
            db.session.commit()
            flash(f'{item_name} added Successfully')
            print('Food Added')
            return render_template('add_food_items.html', form=form)
        except Exception as e:
            print(e)
            flash('Food Not Added!!')

    return render_template('add_food_items.html', form=form)

return render_template('404.html')







