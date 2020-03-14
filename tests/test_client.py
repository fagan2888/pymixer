import json
import time
from urllib import parse

from pymixer import Client

import pytest
import mock


class FakeResponse(mock.Mock):

    def json(self):
        return json.loads(self.content)


@pytest.fixture
def client():
    client = Client('x-client_id-x', 'x-client_secret-x', 'https://httpbin.org/get', 'test')
    assert '<test: x-client_id-x>' in repr(client)
    return client


def test_authorize_url(client):
    authorize_url = client.authorize_url
    parsed_url = parse.urlparse(authorize_url)
    params = parse.parse_qs(parsed_url.query)
    assert params['client_id'][0] == client.client_id
    assert params['response_type'][0] == 'code'
    assert params['redirect_uri'][0] == client.redirect_uri


def test_authorization_grant(client):
    with mock.patch('pymixer.client.OAuth2Session.send') as mock_send:
        def fake_response(self, *args, **kwargs):
            data = {
                'access_token': 'x-access_token-x',
                'refresh_token': 'x-refresh_token-x',
                'token_type': 'Bearer',
                'expires_in': 2
            }
            return FakeResponse(content=json.dumps(data), status_code=200, request=self)
        mock_send.side_effect = fake_response
        client.get_access_data('ab1234cd')
        assert '<x-access_token-x' in repr(client.token)
        assert client.token.access_token == 'x-access_token-x'
        assert client.token.refresh_token == 'x-refresh_token-x'
        assert client.token.is_valid() is True
        time.sleep(1)
        assert client.token.is_valid() is False
        session = client.session
        assert session.access_token == client.token.access_token
        assert session.service == client.service
