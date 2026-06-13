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
            TYPE = request.form['TYPE']
            if TYPE == 'pie chart':
                X = [i.strip() for i in request.form['X'].replace(' ', '').split(',') if i != '']
                Y = [float(i) for i in request.form['Y'].replace(' ', '').split(',') if i != '']
            else:
                X = [float(i) for i in request.form['X'].replace(' ', '').split(',') if i != '']
                Y = [float(i) for i in request.form['Y'].replace(' ', '').split(',') if i != '']
        except ValueError:
            return 'Invalid input!'

        Xlabel = request.form.get('xlabel', '')
        Ylabel = request.form.get('ylabel', '')

        try:
            plt.clf()
            plt.xlabel(Xlabel)
            plt.ylabel(Ylabel)
            plt.grid()

            if TYPE == 'line graph':
                plt.plot(X, Y)
            elif TYPE == 'bar graph':
                plt.bar(X, Y)
            elif TYPE == 'horizontal bar graph':
                plt.barh(X, Y)
            elif TYPE == 'scatter graph':
                plt.scatter(X, Y)
            elif TYPE == 'pie chart':
                plt.pie(Y, labels=X)
            elif TYPE == 'histogram':
                plt.hist(Y)
            elif TYPE == 'area plot':
                plt.fill_between(X, Y)
            elif TYPE == 'step plot':
                plt.step(X, Y)
            else:
                return 'Unsupported graph type'

            plt.savefig(GRAPH_PATH)
            return render_template('gernal_chart.html', show_graph=True)
        except ValueError:
            return 'enter the correct value and of same length'

    return render_template('gernal_chart.html', show_graph=False)
