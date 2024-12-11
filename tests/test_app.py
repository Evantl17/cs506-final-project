import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    # Replace the old assertion with this one (or another suitable check)
    assert b"Portfolio Optimizer" in response.data

def test_get_tickers_endpoint(client):
    response = client.get('/get-tickers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "Expected JSON list of tickers"

def test_submit_invalid_ticker(client):
    # Test submitting an invalid ticker and see if the error message shows up
    data = {
        'tickers': ['FAKE_TICKER'],  # invalid ticker
        'prices': ['100']
    }
    response = client.post('/submit', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"The following tickers are invalid" in response.data
