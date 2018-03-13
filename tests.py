# stdlib
import json
import os
import subprocess
import unittest

# pypi
import twython

# our lib
import tweet_helper


# ==============================================================================


class TestsSetup(unittest.TestCase):

    def test_environment(self):
        "make sure we have all the environment vars set"
        self.assertIsNotNone(tweet_helper.API_KEY)
        self.assertIsNotNone(tweet_helper.API_SECRET)
        self.assertIsNotNone(tweet_helper.USER_TOKEN)
        self.assertIsNotNone(tweet_helper.USER_SECRET)


class TestsPythonApi(unittest.TestCase):
    """testing a tweet is not supported, because it will go live to twitter
    """

    def test_generates_user(self):
        "generate a user"
        twitterUser = tweet_helper.new_TwitterUserClient()
        self.assertIsInstance(twitterUser, twython.api.Twython)

    def test_good_user(self):
        "generate a GOOD user"
        twitterUser = tweet_helper.new_TwitterUserClient()
        api_result = twitterUser.verify_credentials()

    def test_bad_user(self):
        "generate a BAD user"
        try:
            og_USER_SECRET = tweet_helper.USER_SECRET
            tweet_helper.USER_SECRET = 'xxxx'
            twitterUser = tweet_helper.new_TwitterUserClient()
            self.assertRaises(twython.TwythonAuthError, twitterUser.verify_credentials)
        except:
            raise
        finally:
            tweet_helper.USER_SECRET = og_USER_SECRET


class TestsCommandlineApi(unittest.TestCase):
    """testing a tweet is not supported, because it will go live to twitter
    """

    def test_auth(self):
        """not sure how to test this, since it is interactive"""
        raise unittest.SkipTest("not tested")

    def test_invalid_user(self):
        "validate a BAD user"
        try:
            og_USER_SECRET = tweet_helper.USER_SECRET
            os.environ["TWEET_HELPER__USER_SECRET"] = 'xxxx'
            result = subprocess.check_output(["python", "tweet_helper.py", "-a", "VERIFY"]).strip()
            result_parsed = json.loads(result)
            self.assertEqual(result_parsed['status'], 'error')
        except:
            raise
        finally:
            os.environ["TWEET_HELPER__USER_SECRET"] = og_USER_SECRET

    def test_valid_user(self):
        "validate a GOOD user"
        result = subprocess.check_output(["python", "tweet_helper.py", "-a", "VERIFY"]).strip()
        result_parsed = json.loads(result)
        self.assertEqual(result_parsed['status'], 'success')
