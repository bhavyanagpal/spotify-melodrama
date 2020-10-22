from flask import Flask, render_template
from visual import val
from lyrics import lyl

app=Flask(__name__)

@app.route('/')
def home():
    print("Hey")
    return render_template("landing.html")

@app.route('/visual')
def vis():
    return val

@app.route('/lyrics')
def lyr():
    return lyl

if __name__=="__main":
    app.run(debug=True, use_reloader=False)    
