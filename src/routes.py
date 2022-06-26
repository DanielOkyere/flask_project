from calendar import c
from nis import cat

import flask_sqlalchemy
from src import app, db
from flask import render_template, redirect, url_for, flash, request
from src.models import Item, User
from src.forms import RegisterForm, Loginform, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("hello.html")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        purchased = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congrats! You just purchsed {p_item_object.name} for {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you dont have enough funds to purchse {p_item_object.name}", category='danger')
        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Item.query.filter_by(owner = None)
        owned_items = Item.query.filter_by(owner= current_user.id)
    return render_template("market.html", items=items, purchase_form = purchase_form, owned_items = owned_items)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                                email=form.email.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f" Account created Success, You are logged in as: {user_to_create.username}", category='succes')

        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f"Error creating user : {err_msg}", category='danger')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = Loginform()
    if form.validate_on_submit():
        attempte_user = User.query.filter_by(username=form.username.data).first()
        if attempte_user and attempte_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempte_user)
            flash(f"Success, You are logged in as: {attempte_user.username}", category='succes')
            return redirect(url_for('market_page'))
        else:
            flash(f"Username and password are not a match! Please try again", category='error')


    return render_template('login.html', form = form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f"You have successfully logged out", category='info')
    return redirect(url_for('home_page'))
