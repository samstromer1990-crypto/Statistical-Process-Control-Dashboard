from flask import render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
GRAPH_PATH = os.path.join(BASE_DIR, 'static', 'graph.png')
os.makedirs(os.path.dirname(GRAPH_PATH), exist_ok=True)


def handle():
    if request.method == 'POST':
        try:
            X = [float(i) for i in request.form['x'].replace(' ', '').split(',') if i != '']
        except ValueError:
            return 'Invalid Input'

        Xlabel = request.form.get('xlabel', '')
        Ylabel = request.form.get('ylabel', '')

        if not X:
            return 'No data provided'

        c_mean = sum(X) / len(X)
        UCl = c_mean + 3 * (c_mean ** 0.5)
        LCl = c_mean - 3 * (c_mean ** 0.5)
        CL = c_mean

        if LCl < 0:
            LCl = 0

        plt.clf()
        plt.plot(X, marker='o', label='Defects')
        plt.axhline(CL, color='green', linestyle='--', label='CL')
        plt.axhline(UCl, color='red', linestyle='--', label='UCL')
        plt.axhline(LCl, color='blue', linestyle='--', label='LCL')
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.legend()
        plt.savefig(GRAPH_PATH)

        return render_template('c_chart.html', show_graph=True)

    return render_template('c_chart.html', show_graph=False)
