from flask import Flask

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<h1>Chào mừng đến với krm-sharing</h1>"

if __name__ == "__main__":
    app.run()