from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Articles
# from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask import jsonify
import  os
import json
import requests
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector.constants import ClientFlag
import requests
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
app = Flask(__name__)


config = {
    'user': 'root',
    'password': 'password',
    'host': '34.135.90.63',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'server-ca.pem',
    'ssl_cert': 'client-cert.pem',
    'ssl_key': 'client-key.pem'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor(buffered=True)  # initialize connection cursor
cursor.execute('CREATE DATABASE IF NOT EXISTS myflaskapp_new')  # create a new 'testdb' database
# cnxn.close() 
#  # close connection because we will be reconnecting to testdb
cursor.execute("USE myflaskapp_new")
config['database'] = 'myflaskapp_new'  # add new database to config dict
cursor.execute("CREATE TABLE IF NOT EXISTS users (id int(11) AUTO_INCREMENT PRIMARY KEY,name varchar(100),email varchar(100), username varchar(30),password varchar(100), register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

cursor.execute('CREATE TABLE IF NOT EXISTS articles (id int(11) AUTO_INCREMENT PRIMARY KEY, title varchar(225), author varchar(100), body TEXT, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
cnxn.commit()
# from datetime import datetime


Articles = Articles()
summary_url_temp="https://api.covid19api.com/summary" #api link
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
@app.route('/')
def index():
    response = requests.get(summary_url_temp)#get the response from the link
    if response.ok:
        resp_data=response.json() #convert the response into json format
        message=resp_data["Message"]
        if (message!=""):
            return(str(message) +"!! Please Refresh the page after few minutes")
        else:
            
            Global=resp_data["Global"]
            new_deaths= Global["NewDeaths"]
            total_deaths=Global["TotalDeaths"]
            new_cases= Global["NewConfirmed"]
            total_cases=Global["TotalConfirmed"]
            new_recovered= Global["NewRecovered"]
            total_recovered=Global["TotalRecovered"]
            updated=resp_data["Date"]

            return render_template("home.html",date=updated, nd_n=new_deaths, td_n=total_deaths,nc_n=new_cases,tc_n=total_cases,nr_n=new_recovered, tr_n=total_recovered)
    else:
        print(response.reason)
    


# About
@app.route('/about')
def about():
    
    # cursor = mysql.connection.cursor()


    # Get articles
    result = cursor.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    # result = cur.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cursor.fetchall()

    if articles != None:
        return render_template('about.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('about.html', msg=msg)
    # Close connection
    # cursor.close()

# Articles
@app.route('/articles')
@is_logged_in
def articles():
    # Create cursor
    # cur = mysql.connection.cursor()

    # Get articles
    result = cursor.execute("SELECT * FROM articles")

    articles = cursor.fetchall()

    if articles != None:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    # cur.close()


#Single Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    # cur = mysql.connection.cursor()

    # Get article
    result = cursor.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cursor.fetchone()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
# Maps
@app.route('/gmaps')
@is_logged_in
def gmap():
     return render_template('gmaps.html')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        # cur = mysql.connection.cursor()

        # Execute query
        cursor.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        # mysql.connection.commit()

        # Close connection
        # cur.close()

        flash('You are now registered and can log in', 'success')
        cnxn.commit()

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        # cur = mysql.connection.cursor()

        # Get user by username
        result = cursor.execute("SELECT * FROM users WHERE username = %s", [username])
        print(result)
        data = cursor.fetchone()
        if data != None:
            # Get stored hash
           
            password = data[4]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['id'] = data[0]

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            # cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    # cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cursor.execute("SELECT * FROM articles WHERE author = %s", [session['username']])

    articles = cursor.fetchall()

    if articles!= None:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    # cur.close()

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        # cur = mysql.connection.cursor()

        # Execute
        cursor.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        cnxn.commit()

        #Close connection
        # cursor.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    # cur = mysql.connection.cursor()

    # Get article by id
    if id != None:
        result = cursor.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cursor.fetchone()
    # cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article[1]
    form.body.data = article[3]

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
 

        print("======================")

        # Create Cursor
        # cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        sql = "UPDATE articles SET title='"+title+"', body='"+body+"' WHERE id='"+id+"'"
        print(sql)
        cursor.execute(sql)
        # Commit to DB
        cnxn.commit()

        #Close connection
        # cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    # cur = mysql.connection.cursor()

    # Execute
    cursor.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    # mysql.connection.commit()
    cnxn.commit()

    #Close connection
    # cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))