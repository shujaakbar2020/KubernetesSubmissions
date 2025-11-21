from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # You can pass variables to the template as keyword arguments
    return render_template('index.html')

if __name__ == "__main__":
    print("Server started in port 5000")   # printed on startup
    app.run(host="0.0.0.0", port=5000)
