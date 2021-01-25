# import requests for the purposes of monkeypatching
import requests

# our app.py that includes the get_json() function
# this is the previous code block example
import nbp_change

# custom class to be the mock return value
# will override the requests.Response returned from requests.get
class MockResponse:

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"table":"C","currency":"dolar amerykański","code":"USD","rates":[{"no":"064/C/NBP/2016","effectiveDate":"2016-04-04","bid":3.6929,"ask":3.7675}]}


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)
    currency, days = 'usd', '2016-04-04'

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = nbp_change.calc_statistics(currency, days)
    assert result["mock_key"] == "mock_response"