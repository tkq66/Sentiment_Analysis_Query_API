"""A module defining Analysis business logic.

Author: Teekayu Klongtruajrok
"""
import re
from common import twitter_api
from urllib.parse import quote_plus
from textblob import TextBlob


class AnalysisLogic:
    """Analysis business logic to perform various tasks."""

    def __init__(self):
        """Initialize search query parameters."""
        # Query parameters
        self.query_count = 100
        self.tweet_mode = 'extended'
        self.filter_query = ' AND '.join([
            '-filter:retweets',
            '-filter:replies',
            '-filter:links',
            '-filter:media'
        ])

    def group_text_by_sentiment(self, data_list):
        """Group text data according to different sentiment categories.

        Args:
            data_list: A list of dict of local text data. Formatting as follows:
                [
                    {
                        'id': <tweet id>,
                        'text': <tweet text>,
                        'user_handle': <twitter user id>,
                        'user_name': <twitter user name>,
                        'user_img_url': <user profile image url>
                        'timestamp': <tweeted date>,
                        'polarity': <tweet sentiment>
                    }
                    ...
                ]

        Returns:
            A dict of list of local text data, grouped by sentiment categories.
            Formatting as follows:
                {
                    '1': [
                        {
                            'id': <tweet id>,
                            'text': <tweet text>,
                            'user_handle': <twitter user id>,
                            'user_name': <twitter user name>,
                            'user_img_url': <user profile image url>
                            'timestamp': <tweeted date>,
                            'polarity': <tweet sentiment>
                        }
                        ...
                    ],
                    '0': ...
                    '-1': ...
                }

        """
        text_grouping = {}
        for data in data_list:
            sentiment_category = self.__categorize_sentiment_polarity(data['polarity'])
            text_grouping[sentiment_category] = text_grouping.get(sentiment_category, []) + [data]
        return text_grouping

    def construct_data_source(self, query_phrase):
        """Build a local data object for the queried text data.

        Args:
            query_phrase: A string of phrase to search Tweets with.

        Returns:
            A list of dict of locally processable data. Formatting as follows:
                [
                    {
                        'id': <tweet id>,
                        'text': <tweet text>,
                        'user_handle': <twitter user id>,
                        'user_name': <twitter user name>,
                        'user_img_url': <user profile image url>
                        'timestamp': <tweeted date>,
                        'polarity': <tweet sentiment>
                    }
                    ...
                ]

        """
        return [self.__map_tweets_to_local(result)
                for result
                in self.__fetch_tweets(query_phrase)]

    def __categorize_sentiment_polarity(self, polarity):
        """Round the text polarity to either '1', '0', or '-1'.

        Args:
            polarity: A float indicating text polarity.

        Returns:
            An int indicating 3 different sentiment categories:
                1 - positive sentiment, if polarity is greater than 0
                0 - neutral sentiment, if polarity is equal to 0
                -1 - negative sentiment, if polarity is lesser than 0

        """
        return 1 if polarity > 0 else -1 if polarity < 0 else 0

    def __fetch_tweets(self, query_phrase):
        """Get twitter search results.

        Args:
            query_phrase: A string of phrase to search Tweets with.

        Returns:
            A list of twitter.Status objects for all the tweet search results.

        """
        return twitter_api.GetSearch(raw_query=self.__construct_twitter_search_query(query_phrase))

    def __construct_twitter_search_query(self, query_phrase):
        """Build a Twitter search query.

        Query is based on the search phrase, search count, tweet mode to fetch,
        and elements to filter in or out.

        Args:
            query_phrase: A string of phrase to search Tweets with.

        Returns:
            A string of url encoded query string that satisfies the Twitter
            search syntax.

        """
        return quote_plus('q={}'
                          '{}'
                          '&count={}'
                          '&tweet_mode={}'.format(query_phrase,
                                                  self.filter_query,
                                                  self.query_count,
                                                  self.tweet_mode),
                          safe="&=")

    def __map_tweets_to_local(self, tweet_status):
        """Map twitter.Status object to relevant dict and calculate sentiment polarity.

        Args:
            tweet_status: A twitter.Status object storing tweet data.

        Returns:
            A dict of minimal tweet info. Formatting as follows:
                {
                    'id': <tweet id>,
                    'text': <tweet text>,
                    'user_handle': <twitter user id>,
                    'user_name': <twitter user name>,
                    'user_img_url': <user profile image url>,
                    'timestamp': <tweeted date>,
                    'polarity': <tweet sentiment>
                }

        """
        tweet_text = tweet_status.full_text
        tweet_polarity = TextBlob(tweet_text).sentiment.polarity
        return {
            'id': tweet_status.id_str,
            'text': tweet_text,
            'user_handle': tweet_status.user.screen_name,
            'user_name': tweet_status.user.name,
            'user_img_url': tweet_status.user.profile_image_url,
            'timestamp': tweet_status.created_at,
            'polarity': tweet_polarity
        }

    def __clean_tweet(self, tweet):
        """Clean tweet text by removing links, special characters.

        Args:
            tweet: A string of raw tweet data.

        Returns:
            A string of cleaned-up tweet.

        """
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
