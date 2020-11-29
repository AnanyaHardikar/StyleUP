import mysql.connector
import json
from flask import Flask, render_template,request,session,redirect,url_for
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="root123",
  database="styleup"
)
mycursor=mydb.cursor()
app=Flask(__name__)
app.secret_key="secret key"

@app.route('/')
def index():
   return render_template('home.html')
@app.route('/home/')
def home():
    return render_template('home.html')
@app.route('/blog/')
def blog():

    return render_template('blog.html',)
@app.route('/men/')
def men():
    return render_template('men.html')
@app.route('/product/')
def product():
    mycursor.execute("select color, image from item_color where item_id=1001;")
    ONE = mycursor.fetchall()
    return render_template('product.html',data=ONE)
if __name__ == "__main__":
    app.run(debug=True)