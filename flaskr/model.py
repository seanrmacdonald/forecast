from numpy.random import choice
import numpy as np
import random
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
from .data_reference import StatsTester

class MonteCarlo():
    def __init__(self, runs, config):
        self.results = []
        self.initial_value = float(config.get('initial_value'))
        self.rate = float(config.get('rate'))
        self.years = int(config.get('years'))
        self.run_count = runs

    def calculate_growth(self, initial_value, rate, years):
        initial_value = float(initial_value)
        rate = float(rate)
        years = float(years)
        value = initial_value * (1 + rate) ** years
        return round(value)

    def get_rate(self, base_rate):
        mean_rate = 0.08548
        st_dev = 0.19294
        rate = random.choices(
            population=[mean_rate - 2*st_dev, mean_rate - st_dev, mean_rate, mean_rate + st_dev, mean_rate + 2*st_dev],
            weights=[0.025, 0.225, 0.5, 0.225, 0.025],
            k=1
        )
        return rate[0]

    def run_simulation(self):
        runs = []
        for _ in range(self.run_count):
            runs.append(self.make_run(self.initial_value))

        return self.get_summary(runs)

    def make_run(self, initial_value):
        run = [initial_value]
        for _ in range(self.years):
            rate = self.get_rate(self.rate)
            initial_value = self.calculate_growth(initial_value, rate, 1)
            run.append(initial_value)

        return run

    def get_summary(self, runs):
        totals = [run[-1] for run in runs]
        results = np.array(totals)
        p10 = np.percentile(results, 10)
        p50 = np.percentile(results, 50)
        p90 = np.percentile(results, 90)
        p10_run_total = totals[(np.abs(totals - p10)).argmin()]
        p50_run_total = totals[(np.abs(totals - p50)).argmin()]
        p90_run_total = totals[(np.abs(totals - p90)).argmin()]
        min_run = [run for run in runs if run[-1] == min(totals)][0]
        max_run = [run for run in runs if run[-1] == max(totals)][0]
        p10_run = [run for run in runs if run[-1] == p10_run_total][0]
        p50_run = [run for run in runs if run[-1] == p50_run_total][0]
        p90_run = [run for run in runs if run[-1] == p90_run_total][0]
        
        summary = {
            'p10': p10, 
            'p50': p50, 
            'p90': p90,
            'min_run': min_run,
            'max_run': max_run,
            'p10_run': p10_run,
            'p50_run': p50_run,
            'p90_run': p90_run
        }
        plot_url = self.get_summary_graph(summary)
        summary['plot_url'] = plot_url
        return summary
    
    def get_summary_graph(self, summary):
        img = BytesIO()
        current_year = datetime.now().year
        x = list(range(current_year,  current_year + self.years + 1))
        # y1 = summary['min_run']
        y2 = summary['p10_run']
        y3 = summary['p50_run']
        y4 = summary['p90_run']
        # y5 = summary['max_run']

        # plt.plot(x, y1, label ='min')
        plt.plot(x, y2, '-.', label =summary['p10'])
        plt.plot(x, y3, label =summary['p50'])
        plt.plot(x, y4, '-.', label =summary['p90'])
        # plt.plot(x, y5, label ='max')

        plt.ylabel("Value")
        plt.legend()
        plt.savefig(img, format='png')
        plt.close()
        
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        return plot_url