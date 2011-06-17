"""
overseer.management.commands.overseer_twitter_auth
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2011 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from cStringIO import StringIO

import sys
import webbrowser

from django.core.management.base import BaseCommand

from overseer import conf

class Command(BaseCommand):
    def handle(self, **options):
        import urlparse
        import oauth2 as oauth

        consumer_key = conf.TWITTER_CONSUMER_KEY
        consumer_secret = conf.TWITTER_CONSUMER_SECRET

        request_token_url = 'http://twitter.com/oauth/request_token'
        access_token_url = 'http://twitter.com/oauth/access_token'
        authorize_url = 'http://twitter.com/oauth/authorize'

        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        # Step 1: Get a request token. This is a temporary token that is used for 
        # having the user authorize an access token and to sign the request to obtain 
        # said access token.

        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        request_token = dict(urlparse.parse_qsl(content))

        print "Request Token:"
        print "    - oauth_token        = %s" % request_token['oauth_token']
        print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
        print 

        # Step 2: Redirect to the provider. Since this is a CLI script we do not 
        # redirect. In a web application you would redirect the user to the URL
        # below.

        print "We are opening a new browser window to authorize your account"
        print 
        webbrowser.open("%s?oauth_token=%s" % (authorize_url, request_token['oauth_token']))
        print 

        # After the user has granted access to you, the consumer, the provider will
        # redirect you to whatever URL you have told them to redirect to. You can 
        # usually define this in the oauth_callback argument as well.
        oauth_verifier = raw_input('Enter your PIN number once authorized: ')

        # Step 3: Once the consumer has redirected the user back to the oauth_callback
        # URL you can request the access token the user has approved. You use the 
        # request token to sign this request. After this is done you throw away the
        # request token and use the access token returned. You should store this 
        # access token somewhere safe, like a database, for future use.
        token = oauth.Token(request_token['oauth_token'],
            request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        resp, content = client.request(access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))

        print 
        print "Configuration changes:"
        print 
        print "    'TWITTER_ACCESS_TOKEN':  '%s'," % access_token['oauth_token']
        print "    'TWITTER_ACCESS_SECRET': '%s'," % access_token['oauth_token_secret']
        print
        print "Add the above values to your OVERSEER_CONFIG setting" 
        print
