# Exercise 2
Sample API test.

# Implementation
Written in Python3.
Libraries used: 
* requests
* pytest

# Test details
Endpoint tested: https://cat-fact.herokuapp.com/
The app sends daily cat facts. Test checks if 1st received fact contains "cat" word.
No auth required to get cat facts.

# How to run
Run `pytest` in the test directory.
Sample output:

    collected 1 item
    
    test_api.py .                                                                                                    [100%]
    
    ================================================== 1 passed in 3.66s ==================================================
