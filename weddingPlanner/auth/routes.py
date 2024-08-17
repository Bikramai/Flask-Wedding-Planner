import sqlalchemy.exc
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user
from weddingPlanner.auth import auth
from weddingPlanner.extns import db, bcrypt
from weddingPlanner.model import Account


@auth.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')

        account = Account.query.filter_by(email=email).first()

        if account and bcrypt.check_password_hash(account.password, password):
            login_user(account)

            if account.account_type == "VENDOR":
                return redirect(url_for("vendor.choose_vendor"))

            if account.account_type == "USER":
                return redirect(url_for("customer.index"))

        else:
            flash("Incorrect Email or Password", "danger")

    return render_template("auth/login.html")


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        account_type = request.form.get('account_type')

        if password != confirm_password:
            flash("Password must match!", "danger")
            return redirect(url_for("auth.register"))

        new_account = Account(email, bcrypt.generate_password_hash(password), account_type.upper())

        try:
            db.session.add(new_account)
            db.session.commit()
            flash("Account Created Successfully", "success")

            return redirect(url_for("auth.login"))
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            flash("Email Address Already Exists", "danger")
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("An Error Occurred", "danger")

        return redirect(url_for("auth.register"))

    return render_template("auth/register.html")


@auth.route("/logout")
def logout():
    logout_user()
    flash("Logged Out", "warning")
    return redirect(url_for("auth.login"))