'''from flask import Flask, request, jsonify
from functools import wraps
from models import User, DailyMenu, Food, MonthlyMenu, Order, Admin, OrderItem
import jwt
from auth import token_required
from werkzeug.utils import secure_filename
from . import db

@app.route('/', methods=['GET'])
@token_required


def add_food_items():
if current_user.id == 1:
    form = Order_Food())

    if form.validate_on_submit():
        food_id = form.product_id.data
        item_name = form.product_name.data
        price = form.price.data

        file_name = secure_filename(file.filename)

        file_path = f'./media/{file_name}'

        file.save(file_path)

        new_food_item = MonthlyMenu()
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

@admin.route('/food-items', methods=['GET', 'POST'])
@login_required
def food_items():
    if current_user.id == 1:
        items = MonthlyMenu.query.order_by(MonthlyMenu.date_added).all()
        return render_template('food_items.html', items=items)
    return render_template('404.html')


@admin.route('/update-item/<int:food_id>', methods=['GET', 'POST'])
@login_required
def update_item(food_id):
    if current_user.id == 1:
        form = Order_Food()

        item_to_update = MonthlyMenu.query.get(food_id)


        form.food_id.render_kw = {'placeholder': item_to_update.food_id}
        form.item_name.render_kw = {'placeholder': item_to_update.item_name}
        form.price.render_kw = {'placeholder': item_to_update.price}

        if form.validate_on_submit():
            food_id = form.food_id.data
            item_name = form.item_name.data
            price = form.price.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=food_id).update(dict(item_name=item_name,
                                                                price=price))

                db.session.commit()
                flash(f'{item_name} updated Successfully')
                print('Food Updated')
                return redirect('/food-items')
            except Exception as e:
                print('Product not Updated', e)
                flash('Food Not Updated!!!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')


@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(food_id):
    if current_user.id == 1:
        try:
            item_to_delete = MonthlyMenu.query.get(food_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/food-items')
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/food-items')

    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.id == 1:
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.id == 1:
        form = OrderForm()

        order = Order.query.get(order_id)

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully')
                return redirect('/view-orders')
            except Exception as e:
                print(e)
                flash(f'Order {order_id} not updated')
                return redirect('/view-orders')

        return render_template('order_update.html', form=form)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.id == 1:
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')


@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('404.html')
'''


from flask import Flask, request, jsonify
from functools import wraps
from models import User, Food, MonthlyMenu, Order, OrderItem, db
import jwt
from auth import token_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Token verification decorator
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return func(current_user, *args, **kwargs)

    return decorated

# Add food items endpoint
@app.route('/add-food-items', methods=['POST'])
@token_required
def add_food_items(current_user):
    if current_user.id != 1:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json
    food_id = data.get('product_id')
    item_name = data.get('product_name')
    price = data.get('price')

    new_food_item = MonthlyMenu(food_id=food_id, item_name=item_name, price=price)

    try:
        db.session.add(new_food_item)
        db.session.commit()
        return jsonify({'message': f'{item_name} added successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Failed to add food item'}), 500

# Food items endpoint
@app.route('/food-items', methods=['GET'])
@token_required
def get_food_items(current_user):
    if current_user.id != 1:
        return jsonify({'message': 'Unauthorized access'}), 403

    items = MonthlyMenu.query.order_by(MonthlyMenu.date_added).all()
    food_details = [{'food_id': item.food_id, 'item_name': item.item_name, 'price': item.price} for item in items]

    return jsonify({'food_items': food_details}), 200

# Update food item endpoint
@app.route('/update-item/<int:food_id>', methods=['PUT'])
@token_required
def update_item(current_user, food_id):
    if current_user.id != 1:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json
    item_to_update = MonthlyMenu.query.get(food_id)

    if not item_to_update:
        return jsonify({'message': 'Food item not found'}), 404

    item_to_update.item_name = data.get('product_name', item_to_update.item_name)
    item_to_update.price = data.get('price', item_to_update.price)

    try:
        db.session.commit()
        return jsonify({'message': f'Food item with ID {food_id} updated successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Failed to update food item'}), 500

# Delete food item endpoint
@app.route('/delete-item/<int:food_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, food_id):
    if current_user.id != 1:
        return jsonify({'message': 'Unauthorized access'}), 403

    item_to_delete = MonthlyMenu.query.get(food_id)

    if not item_to_delete:
        return jsonify({'message': 'Food item not found'}), 404

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return jsonify({'message': 'Food item deleted successfully'}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'message': 'Failed to delete food item'}), 500

# Admin page route
@app.route('/admin-page', methods=['GET'])
@token_required
def admin_page(current_user):
    if current_user.id == 1:
        return jsonify({'message': 'Welcome to admin page'}), 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 403

if __name__ == '__main__':
    app.run(debug=True)
