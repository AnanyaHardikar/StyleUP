import mysql.connector
import json
from flask import Flask, render_template,request,session,redirect,url_for,Response
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  passwd="root123",
  database="styleup"
)
mycursor=mydb.cursor()
app=Flask(__name__)
app.secret_key="secret key"


url=""
category=""
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/submit', methods=['POST'])
def signUp_submit():
    s_uname = request.form['s_uname']
    s_email = request.form['s_email']
    s_password = request.form['s_psw']
    if s_uname and s_email and s_password and request.method == 'POST':
        query = "SELECT * FROM customers WHERE email_id='%s'" % s_email
        query1 = "INSERT INTO customers VALUES(%s, %s, %s)"
        val = (s_email,s_uname,s_password)
        mycursor.execute(query)
        d = mycursor.fetchall()
        d = str(d).strip("[](),''")
        print(d)
        if (d == ''):
            mycursor.execute(query1, val)
            print(s_email)
            mydb.commit()
            return render_template("login.html", data="SUCCESSFUL")

        else:
            return render_template("login.html", data="email already exist")


    return render_template('home.html')
@app.route('/check', methods=['POST'])
def check():
    psw = request.form['psw']
    email = request.form['email']
    if psw and email and request.method == 'POST':
        query1= "SELECT * FROM customers WHERE email_id='%s'" %email
        val=(email,psw)
        mycursor.execute(query1)
        d = mycursor.fetchall()
        if(str(d).strip("[](),'")==''):
            return render_template("login.html", data1="Invalid Email")
        else:
            if(d[0][0]==email and d[0][2]==psw):
                session['email']=email
                if 'email' in session:
                    global url,category
                    if category=="":
                        return redirect(url_for(url))
                    else:
                        return redirect(url_for(url,category=category))
                else:
                    return render_template('login.html')
            else:
                return render_template("login.html", data1="Please check the    password")


@app.route('/logout/')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/blog/')
def blog():
    return render_template('blog.html',)

@app.route('/men/')
def men():
    return render_template('men.html')

@app.route('/women/')
def women():
    return render_template('women.html')

@app.route('/kids/')
def kids():
    return render_template('kids.html')

@app.route('/product/<item_id>')
def product(item_id):
    mycursor.execute("select color, image from item_color where item_id=%s"%item_id)
    ONE = mycursor.fetchall()
    return render_template('product.html',data=ONE)

@app.route('/shop/<category>')
def process_shop(category):
    query="SELECT * FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template("shop.html", data=data,count=6)

@app.route('/add_to_wishlist/<item_id>', methods=["POST"])
def process_wishlist(item_id):
    if 'email' in session:
        print ("Hello ",item_id)
        return ("Added Successfully")
    else:
        global url,category
        url='process_shop'
        category='menshirts'
        return ('/login/')

@app.route('/product/<item_id>')
def process_product(item_id):
    print(item_id)
    return render_template('product.html')


@app.route('/remove_fav/<id>',methods=['POST'])
def remove_fav(id):
    print(id)
    return ("Removed Successfully")

@app.route('/filter/',methods=["POST"])
def filter():
    color=request.form['color']
    category=request.form['category']
    print(color,category)
    return render_template('blog.html')

@app.route('/wishlist/')
def wishlist():
    if 'email' in session: 
        category='menshirts'
        query="SELECT * FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
        mycursor.execute(query)
        data=mycursor.fetchall()
        return render_template('wishlist.html' ,data=data)
    else:
        global url
        url="wishlist"
        return render_template('login.html')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"]="no-cache,no-store,must-revalidate"
    return response

@app.route('/cart/')
def cart():
    if 'email' in session: 
        category='menshirts'
        query="SELECT * FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
        mycursor.execute(query)
        data=mycursor.fetchall()
        return render_template('cart.html' ,data=data)
    else:
        global url
        url="cart"
        return render_template('login.html')

@app.route('/profile/')
def profile():
    if 'email' in session: 
        
        query="SELECT name,email_id FROM styleup.customers"
        mycursor.execute(query)
        data=mycursor.fetchall()
        return render_template('profile.html' ,data=data)
    else:
        global url
        url="profile"
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)