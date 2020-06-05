import requests

api_url_base = 'https://cat-fact.herokuapp.com/'

headers = {'Content-Type': 'application/json'}


def test_get_cat_facts():

    cat_facts = '{0}facts'.format(api_url_base)
    response = requests.get(cat_facts, headers)
    assert response.status_code == 200

    data = response.json()
    assert 'cat' in data['all'][0]['text'].lower()

if __name__ == "__main__":
    test_get_cat_facts()