import requests
import csv
import pytest
import datetime

api_url_base = 'https://api.exchangeratesapi.io/'


def read_test_data(filename):
    test_data = []
    with open(f'test_data/{filename}', newline='') as df:
        reader = csv.reader(df, delimiter=',')
        next(reader)
        for row in reader:
            test_data.append(row)
    return test_data


def get_rates(path, **params):
    rates = f'{api_url_base}{path}'
    response = requests.get(rates, params=params)
    return response


def test_get_last_rate():
    response = get_rates("latest")
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    data = response.json()
    assert data['base'] == 'EUR'
    for rate in data['rates'].values():
        assert isinstance(rate, float)


def test_get_rate_for_symbols():
    symbols = ['CAD', 'USD', 'HUF', 'RUB', 'PLN', 'KRW', 'GBP', 'HKD', 'DKK']
    response = get_rates("latest", symbols=','.join(symbols))
    assert response.status_code == 200
    data = response.json()
    for symbol in symbols:
        assert isinstance(data['rates'][symbol], float)


@pytest.mark.parametrize("date, base, symbol, rate", read_test_data("historic_data.csv"))
def test_get_historic_rates(date, base, symbol, rate):
    response = get_rates(date, base=base, symbols=symbol)
    assert response.status_code == 200
    data = response.json()
    assert str(data['rates'][symbol]) == rate


@pytest.mark.parametrize("path, base, symbol", read_test_data("special_case_data.csv"))
def test_special_case_will_fail(path, base, symbol):
    response = get_rates(path, base=base, symbols=symbol)
    assert response.status_code == 200
    data = response.json()
    assert str(data['rates'][symbol]) == '1.0'


def test_no_such_symbol():
    symbol = 'AAA'
    response = get_rates("latest", symbols=symbol)
    assert response.status_code == 400


def test_date_is_too_old():
    date = '1990-02-02'
    response = get_rates(date)
    assert response.status_code == 400


def test_date_range_in_the_future():
    start_at = '{0:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(1))
    end_at = '{0:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(7))
    response = get_rates("history", start_at=start_at, end_at=end_at)
    assert response.status_code == 200
    assert not response.json()['rates']
