# Exercise 1
## Task
Assume you are part of an engineering team that is building a loyalty app for a large retailer.
You are in a meeting in which the following stories are being discussed by the Product Owner
and the Engineering Team:

**Story 1:** As a customer, I want to enroll in the loyalty program.

**Story 2:** As a program participant, I want to check my balance of reward points.

**Story 3:** As a program participant, I want to redeem some of my points for a reward.

Please complete the following:

1. Describe how you might participate in this meeting to ensure that the development work for
these stories can be demonstrated to the product owner. What are your areas of concern?

2. How would you address them? Provide your answers as a PDF.

## Solution
Answering this question I would like to focus on two points: doing the right things and visibility.

When I participate in user story discussion I guide myself with the following consideration: user story should add value for the client and the result of our work has to be tangible.

First I would listen if the Engineering Team and the Product Owner share a common understanding of what should be done. If anything is unclear, I’d ask questions.

Who our users are? Why are they using features under consideration? Are they expected to be existing loyal customers or newcomers attracted by the program?

What are the functional and non-functional expectations? I would ensure we know what details to add to these stories and I have an idea how to test it.

How many users are expected? What is their location? Any time periods when extremely high usage is expected?

Are there any time limits for the loyalty program? Do points expire?

Are there any special cases? Any error cases to handle? For example,

__*Story 1:*__

_Given a customer enrolled into a program_

_When a customer enrolls to a program_

_Then they are told double enrollment is not possible._

__*Story 3:*__

_Given a customer has 5 reward points_

_When a customer tries to redeem 100 points_

_Then they should be allowed to redeem 5 points only. Remark: the actual requirement could be different, this is to give an idea of the case._

Do we miss any requirements or stories? I’d check and ask if there are stories about reward points accumulation.
After I ensure we are going to do the right things, I'd see if we are going to show our work result in the right way. Imagine the case when the backend is developed first and there's no UI yet to show new features on. And our PO is not inclined to dive into API call details or log entries.

In this case we should agree with PO what is the expected outcome of each story which could be demonstrated with acceptable level of technical detail. For example, we can demonstrate automated tests passing. Some workflow diagrams will help, too.

Actual project situation could be different, but the idea stays the same - our work has to be valuable and visible.

# Exercise 2
## Description
Sample API test.

## Implementation
Written in Python 3.8.3.

Libraries used: 
* requests
* pytest
* pytest-html

## Test details
For this exercise I selected https://exchangeratesapi.io/. This API provides currency exchange rates, latest and historical.

I'm checking a number of positive scenarios and some error cases in [test_api.py](test_api.py). There are also data-driven tests where I check rate value for historic data.

Given endpoint does not require an API key or any other way of authentication.

You may notice there are not much checks for date value in responses. The reason is when requested date is a weekend or a holiday the endpoint returns rates for the last business day. For a real test I'd account for this logic: find a source of business days for the given business institution and check such cases as weekends and last and first day of the year. For this exercise I left holiday check out of scope.

The test `test_special_case_will_fail` fails, as it's name implies. It checks a special case, when I request an exchange rate for the currency itself. EUR:EUR and USD:USD are tested. The endpoint acts inconsistently: for USD:USD if gives 1.0, but for EUR:EUR gives an error code. This could happen because EUR is the default base here.

As this is a 3-rd party service, I do not include any load or failover testing for it. You can find an example of a performance test in [test_api_times.py](test_api_times.py) where I'm logging responce times for a certain number of currency symbols (1, 2, 4, 8) and increasing date interval (1 day, 1 month, 1 year). In real world I would feed this data (and probably use Python logging) to ELK stack and supplement it with server performance data on a dashboard.

## How to run
Run `pytest --html=report.html` in the test directory.

Sample output: [report.html](https://htmlpreview.github.io/?https://github.com/primacactus/Exercise/blob/develop/report.html) (note 1 failing test).
