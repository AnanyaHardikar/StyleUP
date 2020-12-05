import mysql.connector
from datetime import date
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
user=""
filtered_serach=[]
blog_id=1
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
                global user
                user=email
                session['email']=email
                
                print(user)
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
    query1 = "SELECT user_name,content_less,content_more,organisation,date FROM blog NATURAL JOIN customers"
    mycursor.execute(query1)
    d = mycursor.fetchall()
    print(d)
    l=len(d)
    return render_template('blog.html',data=d,l=l)

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
    mycursor.execute("select color, image  from item_color where item_id='%s'"%item_id)
    ONE = mycursor.fetchall()
    print(ONE)
    mycursor.execute("SELECT item_name,brand,cost,image from items  where item_id='%s'" % item_id)
    data2=mycursor.fetchall()
    print(data2)
    mycursor.execute("select size,availability from item_size where item_id='%s'" %item_id)
    data3=mycursor.fetchall()
    print(data3)
    return render_template('product.html',data=ONE,color_len=len(ONE),data2=data2,data3=data3,len=len(data3))

@app.route('/shop/<category>')
def process_shop(category):
    global filtered_serach
    if category=="filter":
        data=filtered_serach
    else:
        query="SELECT category_id,item_id,brand,cost,image FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
        mycursor.execute(query)
        data=mycursor.fetchall()
    return render_template("shop.html", data=data,count=6)

@app.route('/add_to_wishlist/<item_id>', methods=["POST"])
def process_wishlist(item_id):
    if 'email' in session:
        global user
        query="INSERT into wishlist values(%s,%s)"
        value=(user,item_id)
        mycursor.execute(query,value)
        mydb.commit()
        return ("Added Successfully")
    else:
        global url,category
        url='process_shop'
        query="SELECT category_name from styleup.category where category_id in (SELECT category_id from styleup.items where item_id=%s)"%item_id
        mycursor.execute(query)
        category=mycursor.fetchone()[0]
        print(category)
        return ('/login/')

@app.route('/product/<item_id>')
def process_product(item_id):
    print(item_id)
    return render_template('product.html')


@app.route('/remove_fav/<id>',methods=['POST'])
def remove_fav(id):
    query="DELETE FROM wishlist where item_id=%s"%id
    mycursor.execute(query)
    mydb.commit()
    return ("Removed Successfully")

@app.route('/filter/',methods=["POST"])
def filter():
    global filtered_serach
    color=request.form['color']
    category="%"+request.form['category']+"%"
    size=request.form['size']
    query="SELECT item_name,items.item_id,brand,cost,item_color.image FROM styleup.items INNER JOIN  styleup.item_color ON items.item_id=item_color.item_id  where color=%s and category_id in (SELECT category_id from styleup.category where category_name LIKE %s)"
    value=(color,category)
    mycursor.execute(query,value)
    filtered_serach=mycursor.fetchall()
    category="filter"
    return redirect(url_for('process_shop',category=category))

@app.route('/wishlist/')
def wishlist():
    checkvar=True
    if 'email' in session: 
        global user
        query="SELECT category_id,item_id,brand,cost,image FROM styleup.items where item_id IN (SELECT item_id from styleup.wishlist where email_id='%s')"%user
        mycursor.execute(query)
        data=mycursor.fetchall()
        if len(data)==0:
            checkvar=False
        return render_template('wishlist.html' ,data=data,checkvar=checkvar)
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
    checkvar=True
    if 'email' in session: 
        category='men_shirts'
        query="SELECT * FROM styleup.items NATURAL JOIN styleup.category where category_name='%s'"%category
        mycursor.execute(query)
        data=mycursor.fetchall()
        if len(data)==0:
            checkvar=False
        return render_template('cart.html' ,data=data,checkvar=checkvar)
    else:
        global url
        url="cart"
        return render_template('login.html')

@app.route('/profile/')
def profile():
    if 'email' in session: 
        
        query="SELECT user_name,email_id FROM styleup.customers"
        mycursor.execute(query)
        data=mycursor.fetchall()
        return render_template('profile.html' ,data=data)
    else:
        global url
        url="profile"
        return render_template('login.html')

@app.route('/blog_post/',methods=["POST"])
def blog_post_method():
    today = date.today()
    print("Today's date:", today)
    if 'email' in session:
        less=""
        more=""
        content=request.form['content']
        if(len(content)>100):
            less=content[:30]
            more=content[30:len(content)]
        else:
            less=content
        org=request.form['org']
        email=session['email']
        query1 = "INSERT INTO blog(email_id,organisation,date,content_less,content_more)VALUES( %s, %s,%s,%s,%s)"
        val=(email,org,str(today),less,more)
        mycursor.execute(query1, val)
        mydb.commit()


        query = "SELECT user_name,email_id FROM styleup.customers"
        mycursor.execute(query)
        data = mycursor.fetchall()
        return render_template("profile.html", msg="POST SUCCESSFUL",data=data)
if __name__ == "__main__":
    app.run(debug=True)