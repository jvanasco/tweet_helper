import unittest
import tweet_helper
import twython


class TestsTransform(unittest.TestCase):

    def test_environment(self):
        self.assertIsNotNone(tweet_helper.API_KEY)
        self.assertIsNotNone(tweet_helper.API_SECRET)
        self.assertIsNotNone(tweet_helper.USER_TOKEN)
        self.assertIsNotNone(tweet_helper.USER_SECRET)

    def test_generates_user(self):
        twitterUser = tweet_helper.new_TwitterUserClient()
        self.assertIsInstance(twitterUser, twython.api.Twython)
        