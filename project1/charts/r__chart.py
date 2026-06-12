from flask import render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def handle():
    if request.method == 'POST':
        try:
            subgroup_size = request.form.get('subgroupSize', type=int)
            if subgroup_size is None or subgroup_size < 2:
                return render_template('r__chart.html', show_graph=False, error_message='Please provide a valid subgroup size.')

            data = []
            i = 1
            while True:
                row = request.form.getlist(f'x{i}')
                if not row:
                    break

                if len(row) != subgroup_size:
                    return render_template('r__chart.html', show_graph=False, error_message='Each row must contain exactly the subgroup size number of values.')

                if any(v.strip() == '' for v in row):
                    return render_template('r__chart.html', show_graph=False, error_message='Fill in all cells before generating the chart.')

                data.append([float(v) for v in row])
                i += 1
        except ValueError:
            return 'Invalid Input'

        if not data:
            return 'No data provided'

        n = len(data[0])
        for group in data:
            if len(group) != n:
                return 'All rows must have same number of values'

        ranges = [max(group) - min(group) for group in data]
        r_bar = sum(ranges) / len(ranges)

        D3_values = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0.076, 8: 0.136, 9: 0.184, 10: 0.223}
        D4_values = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}

        D3 = D3_values.get(n)
        D4 = D4_values.get(n)
        if D3 is None or D4 is None:
            return 'Unsupported subgroup size'

        CL = r_bar
        UCL = D4 * r_bar
        LCL = D3 * r_bar

        xlabel = request.form.get('xlabel', 'Subgroup')
        ylabel = request.form.get('ylabel', 'Range')

        plt.clf()
        plt.plot(ranges, marker='o', label='Ranges')
        plt.axhline(CL, color='green', linestyle='--', label='CL')
        plt.axhline(UCL, color='red', linestyle='--', label='UCL')
        plt.axhline(LCL, color='blue', linestyle='--', label='LCL')
        plt.legend()
        plt.title('R-Chart')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig('static/graph.png')

        return render_template('r__chart.html', show_graph=True)

    return render_template('r__chart.html', show_graph=False)
