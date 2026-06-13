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
            d = [float(i) for i in request.form.getlist('d') if i != '']
            n = float(request.form['n'])
        except ValueError:
            return 'Invalid Input'

        if not d:
            return 'Please enter defect values'

        Xlabel = request.form.get('xlabel', 'X-axis')
        Ylabel = request.form.get('ylabel', 'Y-axis')
        p = sum(d) / (len(d) * n)

        CL = p * n
        sigma = (n * p * (1 - p)) ** 0.5
        UCl = CL + 3 * sigma
        LCl = CL - 3 * sigma

        if LCl < 0:
            LCl = 0

        plt.clf()
        plt.title('NP-Chart')
        plt.plot(d, marker='o', label='Defectives')
        plt.axhline(CL, color='green', linestyle='--', label='CL')
        plt.axhline(UCl, color='red', linestyle='--', label='UCL')
        plt.axhline(LCl, color='blue', linestyle='--', label='LCL')
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.legend()
        plt.savefig(GRAPH_PATH)

        return render_template('np__chart.html', show_graph=True)

    return render_template('np__chart.html', show_graph=False)
