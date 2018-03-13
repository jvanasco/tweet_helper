from __future__ import print_function
from builtins import input  # python2.raw_input = python3.input

# stdlib
import argparse
import json
import os
import pprint
# import sys

# pypi
import twython


# ==============================================================================

# NOTE
#
# docs are available on https://github.com/jvanasco/tweet_helper
#
__VERSION__ = '0.0.2'

# API_KEY and API_SECRET correspond to a twitter Application you create on https://apps.twitter.com
API_KEY = os.getenv('TWEET_HELPER__API_KEY', None)
API_SECRET = os.getenv('TWEET_HELPER__API_SECRET', None)

# USER_TOKEN and USER_SECRET are generated via Authorization to the API Application `python tweet_helper.py -a AUTH`
USER_TOKEN = os.getenv('TWEET_HELPER__USER_TOKEN', None)
USER_SECRET = os.getenv('TWEET_HELPER__USER_SECRET', None)

# ==============================================================================


def go_commandline():
    """
    The commandline interface.
    EXAMPLES:
        python tweet_helper.py -a AUTH
        python tweet_helper.py -a VERIFY
        python tweet_helper.py -a TWEET -m 'i tweeted this off the commandline using tweet_helper!'
    """
    _valid_actions = ('AUTH', 'VERIFY', 'TWEET')
    parser = argparse.ArgumentParser(description='Twitter Commandline Interface')
    parser.add_argument('-a',
                        '--action',
                        type=str,
                        help='What action? %s' % str(_valid_actions)
                        )
    parser.add_argument('-m',
                        '--message',
                        type=str,
                        help='What message? %s'
                        )
    args = parser.parse_args()
    if not args.action or (args.action not in _valid_actions):
        raise ValueError("Missing or invalid `action`")
    if args.action == 'TWEET':
        if not args.message:
            raise ValueError("Missing message for `TWEET`")

    if args.action == 'AUTH':
        # this is not a json wrapped result.
        _go_auth()
    elif args.action == 'VERIFY':
        _print_jsonified_api_result(_go_verify)
    elif args.action == 'TWEET':
        _print_jsonified_api_result(_go_tweet, args.message)
    else:
        raise ValueError("unsupported")


def _print_jsonified_api_result(api_call, *args):
    """
    wrapper for api call, `print()` the value as a json doc
    """
    result = new_JsonResult()
    try:
        api_result = api_call(*args)
        result['status'] = 'success'
        result['api_result'] = api_result
    except Exception as e:
        result['error'] = str(e)
    print(json.dumps(result))
    

def _go_auth():
    """
    Handles Authorizing a Twitter User
    This will generate the access token and secret for the user.

    Usage:
        python tweet_helper.py -a AUTH

    Follow the instructions to visit twitter, authorize the app,
    and paste the PIN into the terminal window.
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
        if _idx == 0:
            continue
        _credentials[_idx] = '       ' + _line
    _credentials = '\n'.join(_credentials)
    print(_credentials)
    print(" - - - - - - - - - - - - - -")
    print("export TWEET_HELPER__USER_TOKEN='%s'" % credentials['oauth_token'])
    print("export TWEET_HELPER__USER_SECRET='%s'" % credentials['oauth_token_secret'])
    print("============================")


def _go_verify():
    """
    Verifies Credentials.
    This will raise an error if anything goes wrong.
    """
    twitterUser = new_TwitterUserClient()
    api_result = twitterUser.verify_credentials()
    return api_result


def _go_tweet(message):
    """
    Tweet a message.
    This will raise an error if anything goes wrong.
    """
    if len(message) > 240:
        raise ValueError("message must be 240 chars or less")
    twitterUser = new_TwitterUserClient()
    api_result = twitterUser.update_status(status=message)
    return api_result


# ==============================================================================


def new_JsonResult():
    return {'status': 'error', }


def new_TwitterUserClient():
    """generates a new Twython client for the user"""
    if not all((API_KEY, API_SECRET, USER_TOKEN, USER_SECRET)):
        raise ValueError("Must set all of: API_KEY, API_SECRET, USER_TOKEN, USER_SECRET")
    twitterUser = twython.Twython(API_KEY, API_SECRET, USER_TOKEN, USER_SECRET)
    return twitterUser


def api_tweet(message):
    """use this from your app to tweet something"""
    twitterUser = new_TwitterUserClient()
    result = twitterUser.update_status(status=message)
    return result


# ==============================================================================


if __name__ == '__main__':
    go_commandline()
