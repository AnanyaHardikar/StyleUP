from flask import Flask,render_template

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
if __name__ == "__main__":
    app.run(debug=True)