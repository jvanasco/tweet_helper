IMPORTANT NOTE
==============

This package is longer actively maintained as of 2022.

Please, do not use this package for new projects.

This package was originally designed to enable announcements on Twitter from the automatic SqlAlchemy.org build/release process.

In 2022, Twitter was purchased by a private individual. Over the next few months, the new owner gutted the labor force and product features, removed essentially all of the Trust & Safety policies, and even went to rebranding the company and shifting focus.  This led to many people dropping the platform - especially amongst the core target audience of this package's purpose.  There are now much better avenues to make announcements for software releases.

Due to the decline of potential utility for this project, and highly problematic decisions by the Twitter ownership, the maintainer of this project has no plans to support the Twitter ecosystem in any manner.

About
==========

This package is designed to quickly tweet things.

It was specifically designed to enable Mike Bayer to automate release announcements
via Tweets as part of his build/release process for SQLAlchemy.  Mike needed that
functionality, and I needed to read his (very important) tweets.

The package is a single file and wraps the Twython library.  It expects Twitter
credentials stuffed into the os environment in a certain way.

The package can be imported into a Python process for tweeting, but was designed
to enable tweeting off a terminal prompt so any release process can invoke it.

    python tweet_helper.py -a TWEET -m 'i tweeted this off the commandline using tweet_helper!'

There are full-fledged commandline Twitter clients. This is not one of them.
This project's goal is to simplify tweeting from the commandline.

This package is available on PyPi as `tweet_helper`.

Oh and yes there are tests.


RELEASE INFO / STRATEGY
==================================

`v0.0.1` is the first release.

No breaking changes should be introduced until the next minor release `v0.1.0`.

It would probably be best to pin dependencies to `tweet_helper<0.1.0`


INSTALLATION
==================================

Install via pip, or another package manager if you want...

Python 2.7

    pip install tweet_helper

Python 3

    pip3 install tweet_helper


OR just download the file and invoke it as you wish. That might be easier in some
situations. HOWEVER...

Installing the package via pip/etc will install a console script entrypoint into
your (virtualenv's) /bin named `tweet_helper`

So instead of doing...

	python tweet_helper.py -a VERIFY

you can invoke it as

	tweet_helper -a VERIFY

Isn't that handy?
	
SETUP
======================================

Twitter requires two sets of credentials:

* APPLICATION
* USER

We're going to store these in the following environment variables:

* `TWEET_HELPER__API_KEY`
* `TWEET_HELPER__API_SECRET`
* `TWEET_HELPER__USER_TOKEN`
* `TWEET_HELPER__USER_SECRET`

We're also going to store them in a bash file, so we can just 'source' them into the environment:

To start:

	python tweet_helper.py -a NEW_CREDENTIALS

That will generate some output for you to fill out, and save in a file `credentials.bash`

This strategy lets our applications use the credentials, and we don't have to leave them on a filesystem or pass them along as command args which can be read.


!! IMPORTANT !!
---------------

The `credentials.bash` file contains very sensitive information.

It should NEVER be checked into source control or left lying around in plaintext.

This information can be used to compromise your Twitter Account and your
Twitter Application.

If you store this data, it should be strongly encrypted - not plaintext. 

I like using `GPG` and the `blackbox` wrapper (https://github.com/StackExchange/blackbox),
which can automate decryption.

If you're using `ansible`, use a Vault (https://docs.ansible.com/ansible/2.4/vault.html)

There are many widely available tools for encryption of passcodes and tokens.  

DON'T BE STUPID, ENCRYPT.

Also be sure to `ignore` the plaintext version of this file and only allow the
encrypted version into your source control.


SETUP APPLICATION CREDENTIALS
==============================

To create application credentials, visit https://apps.twitter.com and create a new app.

Copy/Paste the following into your `credentials.bash` file

* "API KEY" or "APP KEY" goes into `TWEET_HELPER__API_KEY`
* "API SECRET" or "APP SECRET" goes into `TWEET_HELPER__API_SECRET`


SETUP USER CREDENTIALS
==============================

You can create a user token when you create an application IF the owner will be
 tweeting.

In the SQLAlchemy example, it probably makes sense for Mike Bayer to own the
application and SQLAlchemy user to tweet, so we will generate user credentials:

    python tweet_helper.py -a AUTH

This will prompt you to visit a url, with text like this:

    In a web-browser, visit the following url to authorize this application:

        https://api.twitter.com/oauth/authenticate?oauth_token=***************

    What is the PIN code? 
    
While logged in to Twitter as the correct user, visit the URL and authorize the application.

You will be presented with a PIN code. Copy/Paste that into the terminal window.

You will now have this data:

    ============================
    AUTH SUCCESS
    ============================
    - Human Formatted Report -
        screen_name: 2xlp
        user_id: 14275299
        Access Token: ****************
        Access Token Secret: ************
    - Machine Readable Formats Below -
     - - - - - - - - - - - - - -
    auth = {u'oauth_token': u'************',
            u'oauth_token_secret': u'************',
            u'screen_name': u'2xlp',
            u'user_id': u'14275299',
            u'x_auth_expires': u'0'}
     - - - - - - - - - - - - - -
    export TWEET_HELPER__USER_TOKEN='*****'
    export TWEET_HELPER__USER_SECRET='*****'
    ============================

Copy/Paste the two `export`  lines into our "credentials" file to overwrite the
default null values

You are done!


SETUP TESTING
==============================

Two steps

1. populate the environment
2. Validate your credentials

Which look like:

    source credentials.bash
    python tweet_helper.py -a VERIFY

If the credentials don't work, you'll see the following:

    {'status': 'error', 'error': 'Twitter API returned a 400 (Bad Request), Bad Authentication data.'}

Notice how that's JSON? Yep, you can parse it.

If the credentials work, the payload will be:

    {'status': 'success', 'api_result': {}, }
    
The value of `api_result` will be the API result of Twitter's validation,
which is Twitter profile data for the authenticating user.



TWEET SOMETHING ON THE COMMANDLINE
==================================

You can now tweet something off the commandline

    source credentials.bash
    python tweet_helper.py -a TWEET -m "test yes it is a test http://example.com 'punctuation' \"other punctuation\""

On failure, an error is raised by Twython:

    {'status': 'error', 'error': 'Twitter API returned a 400 (Bad Request), Bad Authentication data.'}

Notice how that's JSON? Yep, you can parse it.

On success, we'll see:

    {'status': 'success', 'api_result': {}, }

The value of `api_result` will be the Twitter API response for UPDATE STATUS
which is a dict representing the newly formed tweet.



TWEET SOMETHING FROM AN APP
=================================

If you'd like to tweet from an app...

    from tweet_helper import api_tweet

    api_tweet(message="Tweet me!")

If you want more control...

    from tweet_helper import new_TwitterUserClient

    twitterUser = new_TwitterUserClient()
    twitterUser.update_status(status="Tweet me!")


TODO
================================

[] Tests for the authentication flow.
