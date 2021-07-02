from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import RegistrationForm, LoginForm, TodoForm, TodoEditForm
from sqlalchemy import or_
from app.models import User, Todo
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TodoForm()
    if form.validate_on_submit():
        todo = Todo(text=form.text.data)
        db.session.add(todo)
        db.session.commit()
        flash('Congratulations, you added a new todo!')
        return redirect(url_for('index'))


    return render_template('todos.html', title='Todos', todos = Todo.query.all(), form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/todos/<int:todo_id>', methods=['GET', 'POST'])
def todo(todo_id):
    form = TodoEditForm()
    todo = Todo.query.filter_by(id=todo_id).first()
    if form.validate_on_submit():
        if(form.save.data):
            todo.text=form.text.data
            flash('Congratulations, you edited a todo!')
        else:
            db.session.delete(todo)
            flash('Congratulations, you deleted a todo!')
        db.session.commit()
        return redirect(url_for('index'))
    if todo is not None:
        form.text.data = todo.text
    
    return render_template('todo.html', title='Todo', form=form)