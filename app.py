from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/")
def detectFace():
    return render_template("main.py")

if __name__ == '__main__':
    app.run()
    
    