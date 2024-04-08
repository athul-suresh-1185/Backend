from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, User, Food, MonthlyMenu, DailyMenu, Order
from . import db 
from werkzeug.security import generat_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

