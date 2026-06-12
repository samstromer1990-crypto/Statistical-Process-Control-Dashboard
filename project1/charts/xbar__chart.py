from flask import render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def handle():
    if request.method == 'POST':
        try:
            data = []
            i = 1

            while True:
                row = request.form.getlist(f'x{i}')
                if not row:
                    break

                row = [float(v) for v in row if v != '']
                if row:
                    data.append(row)
                i += 1
        except ValueError:
            return 'Invalid Input'

        if not data:
            return 'No data provided'

        n = len(data[0])
        for group in data:
            if len(group) != n:
                return 'All rows must have same number of values'

        means = [sum(group) / len(group) for group in data]
        ranges = [max(group) - min(group) for group in data]
        overall_mean = sum(means) / len(means)
        r_bar = sum(ranges) / len(ranges)

        A2_values = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308}
        A2 = A2_values.get(n)
        if A2 is None:
            return 'Unsupported subgroup size'

        CL = overall_mean
        UCl = overall_mean + A2 * r_bar
        LCl = overall_mean - A2 * r_bar

        if LCl < 0:
            LCl = 0

        xlabel = request.form.get('xlabel', 'Subgroup')
        ylabel = request.form.get('ylabel', 'Value')

        plt.clf()
        plt.plot(means, marker='o', label='Sample Means')
        plt.axhline(CL, color='green', linestyle='--', label='CL')
        plt.axhline(UCl, color='red', linestyle='--', label='UCL')
        plt.axhline(LCl, color='blue', linestyle='--', label='LCL')
        plt.legend()
        plt.title('X-bar Chart')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('static/graph.png')

        return render_template('xbar__chart.html', show_graph=True)

    return render_template('xbar__chart.html', show_graph=False)
