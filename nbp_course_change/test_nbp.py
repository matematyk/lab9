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
        return {"table":"A","currency":"dolar amerykański","code":"USD","rates":[{"no":"014/A/NBP/2021","effectiveDate":"2021-01-22","mid":3.7255},{"no":"015/A/NBP/2021","effectiveDate":"2021-01-25","mid":3.7402}]}


def test_get_json(monkeypatch):

    # Any arguments may be passed and mock_get() will always return our
    # mocked object, which only has the .json() method.
    def mock_get(*args, **kwargs):
        return MockResponse()

    # apply the monkeypatch for requests.get to mock_get
    monkeypatch.setattr(requests, "get", mock_get)
    currency, days = ['usd','gb'], '2016-04-04'

    # app.get_json, which contains requests.get, uses the monkeypatch
    result = nbp_change.calc_statistics(currency, days)
    assert (result=={'gb': {'change': 1.0039457790900552, 'course': 3.7402, 'full_name': 'dolar amerykański'}, 'usd': {'change': 1.0039457790900552, 'course': 3.7402, 'full_name': 'dolar amerykański'}})