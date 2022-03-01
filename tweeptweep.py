# You will need to PIP INSTALL tweepy for this to work and also create a twitter API. Run this on your own machine, not in this Repl.
# Tweepy APi v2.0 - https://docs.tweepy.org/en/stable/client.html#

from pickle import TRUE
import tweepy
import time

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

#Get information about Twitter API user
user__fields = ['created_at', 'location', 'public_metrics']
user = client.get_me(user_fields=user__fields)
user_id = user.data.id
print(user.data.created_at)  # prints your name.
print(user.data.location)
print(user.data.public_metrics["followers_count"])

#Variables
search = "zerotomastery"
numberOfTweets = 10
twitter_username = "TwitterDev"
specified_username = "Insert Specified username"

twitter_user_data = client.get_user(username=twitter_username, user_auth=TRUE)
twitter_user_id = twitter_user_data.data['id']

#To handle RateLimitError due to Pagination
def limit_handle(cursor):
    while True:
        try:
            for i in cursor:
                yield i
        except tweepy.TooManyRequests:
            time.sleep(10)

# Get a list of a twitter user's follower and follow a specified username
for follower in limit_handle(tweepy.Paginator(client.get_users_followers, twitter_user_id, user_auth=TRUE, max_results=30)):
    for data in follower.data:
        if data['username'] == specified_username:
            client.follow_user(data['id'], user_auth=TRUE)
            break
    break

#Previous way to handle Pagination
# def get_ffs(id):
#   while True:
#     try:
#       for response in tweepy.Paginator(client.get_users_followers, id, user_auth=TRUE, max_results=100):
#           print(response.meta)
#     except tweepy.TooManyRequests as err:
#           print("rate limit exceeded")
#           print (err)
#           time.sleep(1000)
# get_ffs(2244994945)

# Be a narcisist and love your own tweets. or retweet anything with a keyword!
for tweets in client.search_recent_tweets(search, max_results=numberOfTweets, user_auth=TRUE):
	for i, tweet in enumerate(tweets):
		try:

			#To like the the search results
			client.like(tweet['id'])

			#To retweet the first two searches
			if i < 2:
				print('retweeted the tweet')
				client.retweet(tweet['id'])
		except tweepy.TweepyException as e:
			print(e.reason)
		except TypeError:
			break
	break