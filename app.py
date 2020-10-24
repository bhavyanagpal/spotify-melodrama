from flask import Flask
from flask import render_template, redirect
from visual import vis 
from lyrics import initial
app=Flask(__name__)



@app.route('/')
def home():
    print("Hey")
    return render_template("landing.html")

@app.route('/visual')
def visual():
    vis()
    return redirect('/')

@app.route('/lyrics')
def lyr():  
    initial()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True, use_reloader=False)    
