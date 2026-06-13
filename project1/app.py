from flask import Flask, render_template
from charts import c_chart, p_chart, np__chart, xbar__chart, r__chart, general_chart

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/c', methods=['GET', 'POST'])
def c():
    return c_chart.handle()

@app.route('/p', methods=['GET', 'POST'])
def p():
    return p_chart.handle()

@app.route('/np', methods=['GET', 'POST'])
def np():
    return np__chart.handle()

@app.route('/xbar', methods=['GET', 'POST'])
def xbar():
    return xbar__chart.handle()

@app.route('/r', methods=['GET', 'POST'])
def r():
    return r__chart.handle()

@app.route('/general', methods=['GET', 'POST'])
def general():
    return general_chart.handle()

if __name__ == '__main__':
    app.run(debug=True)
