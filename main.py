#!/usr/bin/env python3

from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/', methods=['GET', 'POST'])
@app.route('/all', methods=['GET', 'POST'])
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.jinja2')

    name = request.form['name']
    Task(name=name).save() # don't forget to save!

    # use redirect here I will get the exception below
    # jinja2.exceptions.TemplateNotFound: /all/
    return redirect(url_for('all_tasks'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    # for key in request.session.keys():
    #     del request.session[key]

    if request.method == 'GET':
        return render_template('login.jinja2')
    else:

        input_name = request.form['name']
        input_password = request.form['password']

        user = None
        msg = ""
        success = False

        try:
            user = User.get(User.name == input_name)

            if pbkdf2_sha256.verify(input_password, user.password) == False:
                msg = "Incorrect password for user {}".format(user.name)
                return render_template('login.jinja2', user=user, msg=msg)

            msg = "login successful"
            session['current_user'] = str(user.name)
            success = True

        except Exception as e:
            msg = e
            # msg = "user does not exist"
            pass

        if success == True:
            return redirect(url_for('all_tasks'))

        # if user is not None:
        #     return render_template(url_for('all_tasks'))
        # session['current_user'] = user.name

        # if User.Does
        # Task(name=name).save() # don't forget to save!
        # return render_template(url_for('all_tasks'))
        return render_template('login.jinja2', user=user, msg=msg)


@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    # If the visitor is not logged in as a user:
        # Then redirect them to the login page

    """
    If the request method is POST
    # Then retrieve the username from the session and find the associated user
    # Retrieve the task_id from the form submission and use it to find the
    associated task # Update the task to indicate that it has been completed
    at datetime.now() by the current user # Retrieve a list of all incomplete
    tasks # Render the incomplete.jinja2 template, injecting in the list of
    all incomplete tasks
    """
    msg = ""
    username = ""
    if session.get('current_user') == None:
        username = 'no current_user'
        msg = username
    else:
        username = session.get('current_user')
        msg = "User: " + username

    if request.method == 'POST':
        task_id = request.form['task_id']
        msg += "task_id = " + task_id

        # user = User.select().where(User.name == username)
        user2 = User.select().where(User.name == username).get()

        # AttributeError: 'User' object has no attribute '_hash'
        # assert user == user2, "Are these equal?"

        Task.update(performed=datetime.now()).where(Task.id == task_id).execute()
        Task.update(performed_by=user2).where(Task.id == task_id).execute()

        # user = User.get(User.name == input_name)
        # Task.update(performed=datetime.now(), performed_by=user)\
        #     .where(Task.id = request.form['task_id'])\
        #     .execute()

    return render_template('incomplete.jinja2', debug=msg, tasks=Task.select().where(Task.performed.is_null()))


@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST' and request.form['debug_action'] == 'mark_all_as_incomplete':
        Task.update(performed=None).execute()
        Task.update(performed_by=None).execute()
        return redirect(url_for('all_tasks'))

    # username = "no current user"
    # if 'username' not in session:
    #     username = "no current user"
    # else:
        # username = str(session.get('current_user'))
    username = session['current_user']

    return render_template('debug.jinja2', user=username)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
