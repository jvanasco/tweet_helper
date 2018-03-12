This is designed to quickly tweet things.

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

	cp credentials.bash_template credentials.bash

SETUP APPLICATION CREDENTIALS
==============================

To create application credentials, visit https://apps.twitter.com and create a new app.

Copy/Paste the following into your `credentials.bash`` file

* "API KEY" or "APP KEY" goes into `TWEET_HELPER__API_KEY`
* "API SECRET" or "APP SECRET" goes into `TWEET_HELPER__API_SECRET`


SETUP USER CREDENTIALS
==============================

You can create a user token when you create an application IF the owner will be tweeting.

In the sqlalchemy example, it probably makes sense for Mike Bayer to own the application and SqlAlchemy user to tweet, so we will generate user credentials:

	python tweet_helper.py -a AUTH

This will prompt you to visit a url, with text like this:

	In a web-browser, visit the following url to authorize this application:

		https://api.twitter.com/oauth/authenticate?oauth_token=***************

	What is the PIN code? 
	
While logged in to twitter as the correct user, visit the URL and authorize the application.

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

Copy/Paste the two `export`	 lines into our "credentials" file to overwrite the default null values

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
	
The value of `api_result` will be the api result of twitter's validation, which is twitter profile data for the authenticating user.



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

The value of `api_result` will be the twitter api response for UPDATE STATUS which is a dict representing the newly formed tweet.



TWEET SOMETHING FROM AN APP
==================================

If you'd like to tweet from an app...

	from tweet_helper import api_tweet

	api_tweet(message="Tweet me!")

If you want more control...

	from tweet_helper import new_TwitterUserClient

	twitterUser = new_TwitterUserClient()
	twitterUser.update_status(status="Tweet me!")

