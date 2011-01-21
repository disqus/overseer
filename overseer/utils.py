import httplib
import oauth2

# example client using httplib with headers
class SimpleTwitterClient(oauth2.Client):

    def __init__(self, server='api.twitter.com', port=httplib.HTTP_PORT, request_token_url='',
                 access_token_url='', authorization_url='', consumer=None, token=None):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))
        self.consumer = consumer
        self.token = token

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return oauth2.Token.from_string(response.read())

    def fetch_access_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        return oauth2.Token.from_string(response.read())

    def authorize_token(self, oauth_request):
        # via url
        # -> typically just some okay response
        self.connection.request(oauth_request.http_method, oauth_request.to_url()) 
        response = self.connection.getresponse()
        return response.read()

    def update_status(self, status):
        # via post body
        # -> some protected resources
        headers = {'Content-Type' :'application/x-www-form-urlencoded'}
        params = {
            'status': status,
        }
        oauth_request = oauth2.Request.from_consumer_and_token(
            consumer=self.consumer, token=self.token, http_method='POST',
            http_url='http://%s/1/statuses/update.json' % self.server, parameters=params)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        
        self.connection.request('POST', '/1/statuses/update.json',
                                body=oauth_request.to_postdata(), headers=headers)
        response = self.connection.getresponse()
        return response, response.read()