## Exercise 2

# Description
Sample API test.

# Implementation
Written in Python 3.8.3.

Libraries used: 
* requests
* pytest
* pytest-html

# Test details
For this exercise I selected https://exchangeratesapi.io/. This API provides exchange rates, latest and historical.

I'm checking a number of positive scenarios and some error cases. There are also data-driven tests where I check rate value for historic data.

Given endpoint does not require an API key or any other way of authentication.

You may notice there are not much checks of date value in responses. The reason is when requested date is a weekend or holiday the endpoint returns rates for the last business day. For a real test I'd account for this logic: find a source of business days for the given business institution and check such cases as weekends and last and first day of the year. For this exercise I left this out of scope.

The test "test_special_case_will_fail" fails, as it's name implies. It checks a special case, when I request an exchange rate for the currency itself. EUR:EUR and USD:USD are tested. The endpoint acts inconsistently here: for USD:USD if gives 1.0, but for EUR:EUR gives an error code. This could happen because EUR is the default base here.

As this is a 3-rd party website, I do not include any load or failover testing. You can find an example of a performance test where I'm logging responce times for a certain number af currency symbols (1, 2, 4, 8) and increasing date interval (1 day, 1 month, 1 year). In real world I would feed this data to ELK stack and supplement it with server performance data on a dashboard.

# How to run
Run `pytest --html=report.html` in the test directory.

Sample output: [report.html](report.html) (note 1 failing test).