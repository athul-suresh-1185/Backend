from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class Order_Food(FlaskForm):
  food_id=IntegerField('Food ID'),validators=[DataRequired()])
  product_name = StringField('Name of Product', validators=[DataRequired()])
  current_price = FloatField('Current Price', validators=[DataRequired()])


  add_product = SubmitField('Add Product')
  update_product = SubmitField('Update')

class OrderForm(FlaskForm):
order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                    ('Out for delivery', 'Out for delivery'),
                                                    ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

update = SubmitField('Update Status')