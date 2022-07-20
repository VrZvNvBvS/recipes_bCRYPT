from flask import flash, redirect, render_template, request, session
from flask_app import app,bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/" , methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/register",methods=['POST'])
def registration():
    if not User.validate_registration(request.form):
            return redirect("/")
        
    pw_encryption = bcrypt.generate_password_hash(request.form['password1'])
    data = {
        'first_name':request.form['firstname'],
        'last_name':request.form['lastname'],
        'email':request.form['email'],
        'password':pw_encryption
    }
    response_query = User.create_user(data)
    session['id'] = response_query
    return redirect("/dashboard")

@app.route("/login",methods=['POST'])
def login():
    response_query_user=User.get_user_by_email(request.form)
    
    if not response_query_user:
        flash("Invalid User Login Credentials!!!","login")
        return redirect('/')
    
    if not bcrypt.check_password_hash( response_query_user.password, request.form['password']):
        flash("Invalid User Login Credentials!!!","login")
        return redirect("/")
    session['id'] = response_query_user.id
    return redirect("/dashboard")

@app.route("/dashboard",methods=['GET'])
def dashboard_user():
    if 'id' not in session:
        return redirect('/logout')
    data ={
        'id': session['id']
    }
    response_query=User.get_user_by_id(data)
    recipes=Recipe.get_all()
    return render_template("dashboard.html",user=response_query,recipes=recipes)

@app.route("/logout",methods=['GET'])
def logout():
    session.clear()
    return redirect("/")