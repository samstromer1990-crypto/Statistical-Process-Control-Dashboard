from flask import render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def handle():
    if request.method == 'POST':
        try:
            d = [float(i) for i in request.form.getlist('d') if i != '']
            n = [float(i) for i in request.form.getlist('n') if i != '']
        except ValueError:
            return 'Invalid Input'

        if len(d) != len(n):
            return 'Length of d and n must be the same'

        Xlabel = request.form.get('xlabel', 'X-axis')
        Ylabel = request.form.get('ylabel', 'Y-axis')
        total_p = sum(d) / sum(n)
        p_bar = [d[i] / n[i] for i in range(len(d))]

        CL = (total_p * (1 - total_p) / sum(n)) ** 0.5
        UCl = total_p + 3 * CL
        LCl = total_p - 3 * CL

        if LCl < 0:
            LCl = 0

        plt.clf()
        plt.plot(p_bar, marker='o', label='Proportion')
        plt.axhline(total_p, color='green', linestyle='--', label='CL')
        plt.axhline(UCl, color='red', linestyle='--', label='UCL')
        plt.axhline(LCl, color='blue', linestyle='--', label='LCL')
        plt.xlabel(Xlabel)
        plt.ylabel(Ylabel)
        plt.legend()
        plt.savefig('static/graph.png')

        return render_template('p__chart.html', show_graph=True)

    return render_template('p__chart.html', show_graph=False)
