import requests
import csv
import pytest
import datetime

api_url_base = 'https://api.exchangeratesapi.io/'


def read_test_data(filename):
    """A function that reads request parameters, such as currency symbols, base and dates, from csv file."""
    test_data = []
    with open(f'test_data/{filename}', newline='') as df:
        reader = csv.reader(df, delimiter=',')
        next(reader)
        for row in reader:
            test_data.append(row)
    return test_data


def get_rates(path, **params):
    """Helper function to make a request and return its response."""
    rates = f'{api_url_base}{path}'
    response = requests.get(rates, params=params)
    return response


def check_request_success(response):
    """Helper function to check if request is successful and properly formatted"""
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"


def test_get_last_rate():
    """Test gets last available rate for EUR, checks response code and data format."""
    response = get_rates("latest")
    check_request_success(response)
    data = response.json()
    assert data['base'] == 'EUR'
    for rate in data['rates'].values():
        assert isinstance(rate, float)


def test_get_rate_for_symbols():
    """Test checks if a number returned for each currency symbol in request."""
    symbols = ['CAD', 'USD', 'HUF', 'RUB', 'PLN', 'KRW', 'GBP', 'HKD', 'DKK']
    response = get_rates("latest", symbols=','.join(symbols))
    check_request_success(response)
    data = response.json()
    for symbol in symbols:
        assert isinstance(data['rates'][symbol], float)


@pytest.mark.parametrize("date, base, symbol, rate", read_test_data("historic_data.csv"))
def test_get_historic_rates(date, base, symbol, rate):
    """Test checks if historic rates are returned correctly compared to stored data."""
    response = get_rates(date, base=base, symbols=symbol)
    check_request_success(response)
    data = response.json()
    assert str(data['rates'][symbol]) == rate


@pytest.mark.parametrize("path, base, symbol", read_test_data("special_case_data.csv"))
def test_special_case_will_fail(path, base, symbol):
    """Test checks if exchange rate is 1.0 when currency symbol and base are the same."""
    response = get_rates(path, base=base, symbols=symbol)
    check_request_success(response)
    data = response.json()
    assert str(data['rates'][symbol]) == '1.0'


def test_no_such_symbol():
    """Tests checks if error returned when there is no such currency symbol."""
    symbol = 'AAA'
    response = get_rates("latest", symbols=symbol)
    assert response.status_code == 400


def test_date_is_too_old():
    """Tests checks if error returned when request made for date earlier than 1999-01-04."""
    date = '1990-02-02'
    response = get_rates(date)
    assert response.status_code == 400


def test_date_range_in_the_future():
    """Tests checks if no rates returned for future dates."""
    start_at = '{0:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(1))
    end_at = '{0:%Y-%m-%d}'.format(datetime.datetime.now() + datetime.timedelta(7))
    response = get_rates("history", start_at=start_at, end_at=end_at)
    check_request_success(response)
    assert not response.json()['rates']
