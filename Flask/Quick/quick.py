from flask import Flask, request, render_template


app = Flask(__name__, template_folder="./")

@app.route('/')
def index():
    return render_template('select.html')


if __name__ == '__main__':
    app.run(debug=1, host='localhost', port=5050)
