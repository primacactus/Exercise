import requests
import csv
import datetime
from test_api import read_test_data
from test_api import api_url_base


def test_get_rate_times():
    """Response times are measured for increasing number of currencies and increasing date intervals."""
    rates = f'{api_url_base}history'
    perf_data = []
    for d in read_test_data("workload.csv"):
        time_before = datetime.datetime.now()
        params = {'symbols': d[0], 'start_at': d[1], 'end_at': d[2]}
        requests.get(rates, params)
        time_after = datetime.datetime.now()
        perf_data.append([d[0], d[1], d[2], time_before, time_after])
    suffix = '{0:%Y-%m-%d %H.%M.%S}'.format(datetime.datetime.now())
    fieldnames = ['symbols', 'start_at', 'end_at', 'time_before', 'time_after']
    with open(f'perf_data/perf_data {suffix}.csv', 'w', newline='') as df:
        writer = csv.writer(df, delimiter=',')
        writer.writerow(fieldnames)
        writer.writerows(perf_data)
