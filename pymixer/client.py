import time
import webbrowser

from rauth import OAuth2Service, OAuth2Session

MIXER_BASE_URL = 'https://mixer.com/api/v1/'
MIXER_AUTHORIZE_URL = 'https://mixer.com/oauth/authorize'
MIXER_TOKEN_URL = 'https://mixer.com/api/v1/oauth/token'


class TokenJar(object):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return '{self.access_token}:{self.expires_at}'.format(self=self)

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def is_valid(self):
        return (self.expires_at - time.time()) > 1


class Client(object):

    def __init__(self, client_id, client_secret, redirect_uri, name=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.name = name if name else 'Mixer'
        self.token = None
        self.service = OAuth2Service(
            client_id=client_id, client_secret=client_secret, name=self.name,
            authorize_url=MIXER_AUTHORIZE_URL, access_token_url=MIXER_TOKEN_URL,
            base_url=MIXER_BASE_URL)

    def __str__(self):
        return '{self.name}: {self.client_id}'.format(self=self)

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    @property
    def authorize_url(self):
        return self.service.get_authorize_url(
            response_type='code', redirect_uri=self.redirect_uri)

    def get_access_data(self, code):
        code = code if code else self.code
        params = {
            'code': code, 'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        response = self.service.get_raw_access_token(data=params)
        data = response.json()
        if response.status_code == 200 and data.get('access_token'):
            data['expires_at'] = time.time() + data['expires_in']
            self.token = TokenJar(**data)
        return data

    @property
    def session(self):
        token = None
        if self.token and self.token.access_token:
            token = self.token.access_token
        return OAuth2Session(
            self.client_id, self.client_secret, token, service=self.service)

    def cli(self):
        # get authorization code
        webbrowser.open(self.authorize_url)
        code = input('Paste code: ')
        # get access token
        return self.get_access_data(code)
