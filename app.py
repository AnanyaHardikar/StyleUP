from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="",
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
    return render_template('blog.html')

@app.route('/men/')
def men():
    return render_template('men.html')

@app.route('/shop/<category>')
def process_shop(category):
    query="SELECT * FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template("shop.html", data=data,count=6)

@app.route('/product/<item_id>')
def process_product(item_id):
    print(item_id)
    return render_template('product.html')

if __name__ == "__main__":
    app.run(debug=True)