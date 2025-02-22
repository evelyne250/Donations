# from flask import render_template
from . import auth
from flask import render_template,redirect,url_for
from ..models import User, Donation, Subscription
from .. import db
from flask import render_template,redirect,url_for, flash,request
from flask_login import login_user
from ..models import User
from .forms import LoginForm,RegistrationForm,DonationForm
from flask_login import login_user,logout_user,login_required
from ..email import mail_message


@auth.route('/login',methods=['GET','POST'])
def login():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    flash('Invalid username or Password')
    title = "Donation login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
    

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        # mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html',registration_form = form)

@auth.route('/subscription', methods=["GET", "POST"])
def subscription():
   subform = DonationForm()
   if subform.validate_on_submit():
       subscribers = Subscription(name=subform.name.data, email=subform.email.data)
       db.session.add(subscribers)
       db.session.commit()
       mail_message("Welcome to Donation...",
                    "email/welcome_user", subscribers.email, subscribers=subscribers)
       return redirect(url_for('main.index'))
       title = "New Subscription"
   return render_template('auth/subscribe.html', subscription_form=subform)