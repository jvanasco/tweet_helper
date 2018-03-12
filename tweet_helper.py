from __future__ import print_function
from builtins import input  # python2.raw_input = python3.input


import argparse
import twython
import os
import sys
import pprint


__VERSION__ = '0.0.1'


API_KEY = os.getenv('TWEET_HELPER__API_KEY')
API_SECRET = os.getenv('TWEET_HELPER__API_SECRET')
USER_TOKEN = os.getenv('TWEET_HELPER__USER_TOKEN')
USER_SECRET = os.getenv('TWEET_HELPER__USER_SECRET')

# ==============================================================================



def go_commandline():
    """
    EXAMPLES:
        python __init__.py -a AUTH
    """
    _valid_actions = ('AUTH', 'VERIFY', 'TWEET')
    parser = argparse.ArgumentParser(description='Twitter Commandline Interface')
    parser.add_argument('-a',
                        '--action',
                        type = str,
                        help = 'What action? %s' % str(_valid_actions)
                        )
    parser.add_argument('-m',
                        '--message',
                        type = str,
                        help = 'What message? %s'
                        )
    args = parser.parse_args()
    if not args.action or (args.action not in _valid_actions):
        raise ValueError("Missing or invalid `action`")
    if args.action == 'TWEET':
        if not args.message:
            raise ValueError("Missing message for `TWEET`")
    
    if args.action == 'AUTH':
        _go_auth()
    elif args.action == 'VERIFY':
        _go_verify()
    elif args.action == 'TWEET':
        _go_tweet(args.message)
    else:
        raise ValueError("unsupported")
    

def _go_auth():
    """
    Handles Authorizing a Twitter User
    """
    twitterApp = twython.Twython(API_KEY, API_SECRET)
    auth = twitterApp.get_authentication_tokens()
    
    # auth will have the following data:
    # {'auth_url': 'https://api.twitter.com/oauth/authenticate?oauth_token=OAUTH_TOKEN}',
    #  'oauth_callback_confirmed': u'true',
    #  'oauth_token': u'OAUTH_TOKEN',
    #  'oauth_token_secret': u'OAUTH_SECRET'}    

    print("")
    print("In a web-browser, visit the following url to authorize this application:")
    print("")
    print("\t%s" % auth['auth_url'])
    print("")
    oauth_verifier = input("What is the PIN code? ")
    oauth_verifier = oauth_verifier.strip()
    twitterUser = twython.Twython(API_KEY, API_SECRET, auth['oauth_token'], auth['oauth_token_secret'])
    credentials = twitterUser.get_authorized_tokens(oauth_verifier)
    
    print("============================")
    print("AUTH SUCCESS")
    print("============================")
    print(" - Human Formatted Report -")
    print("\tscreen_name: %s" % credentials['screen_name'])
    print("\tuser_id: %s" % credentials['user_id'])
    print("\tAccess Token: %s" % credentials['oauth_token'])
    print("\tAccess Token Secret: %s" % credentials['oauth_token_secret'])
    print(" - Machine Readable Formats Below -")
    print(" - - - - - - - - - - - - - -")
    _credentials = ("auth = %s" % pprint.pformat(credentials)).split('\n')
    for _idx, _line in enumerate(_credentials):
        if _idx == 0: continue
        _credentials[_idx] = '       ' + _line
    _credentials = '\n'.join(_credentials)
    print(_credentials)
    print(" - - - - - - - - - - - - - -")
    print("export TWEET_HELPER__USER_TOKEN='%s'" % credentials['oauth_token'])
    print("export TWEET_HELPER__USER_SECRET='%s'" % credentials['oauth_token_secret'])
    print("============================")


def _go_verify():
    """
    Verifies Credentials
    """
    twitterUser = new_TwitterUserClient()
    result = twitterUser.verify_credentials()
    print("============================")
    print("AUTH VALID")
    print("============================")
    pprint.pprint(result)
    print("============================")


def _go_tweet(message):
    """
    Tweet a message
    """
    if len(message) > 240:
        raise ValueError("message must be 240 chars or less")
    twitterUser = new_TwitterUserClient()
    result = twitterUser.update_status(status=message)
    print("============================")
    print("TWEETED")
    print("============================")
    pprint.pprint(result)
    print("============================")


def new_TwitterUserClient():
    """generates a new Twython client for the user"""
    twitterUser = twython.Twython(API_KEY, API_SECRET, USER_TOKEN, USER_SECRET)
    return twitterUser


def api_tweet(message):
    """use this from your app to tweet something"""
    twitterUser = new_TwitterUserClient()
    result = twitterUser.update_status(status=message)
    return result


if __name__ == '__main__':
    go_commandline()
