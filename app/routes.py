from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import SignUpForm
from sqlalchemy import or_
from app.models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template('users.html', title='Users', users = User.query.all())


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_user.html', title='Sign Up', form=form)