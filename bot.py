# -*- coding: utf-8 -*-

# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import tweepy
import random

from secrets import *
from time import gmtime, strftime


# ====== Individual bot configuration ==========================
bot_username = 'honestly'
logfile_name = bot_username + ".log"

# ==============================================================

def create_tweet():
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    """Create the text of the tweet you want to send."""
    # Replace this with your code!

    searchResults = api.search(q="honestly -rt -@",lang="en")

    for result in list(searchResults):
        cleantext = result.text.lower()
        if result.in_reply_to_status_id != None:
            searchResults.remove(result)

        elif "honestly" not in cleantext.split(' ')[0]:
            if "honestly" not in cleantext.split(' ')[1]:
                searchResults.remove(result)

        elif "@" in cleantext or \
        "http" in cleantext or \
        "https" in cleantext or \
        "#"    in cleantext or \
        "nigg"    in cleantext or \
        "hitler"    in cleantext:
            searchResults.remove(result)

        elif "@" in cleantext.split(' ')[0]:
            searchResults.remove(result)

    for result in list(searchResults):
        cleantext = result.text.lower()
        #print result

        if "honestly" not in result.text.split(' ')[0].lower():
            if "honestly" not in result.text.split(' ')[1].lower():
                print "~~~"
                print "nope"
                print "~~~"

        if "@" in cleantext or \
        "http" in cleantext or \
        "#" in cleantext or \
        "https" in cleantext:
            print "~~~"
            print "nooo"
            print "~~~"
            searchResults.remove(result)

        else:
            print "~~~"
            print result.text.encode('utf-8')
            print "~~~"

    result = random.choice(searchResults)
    api.create_favorite(result.id_str)
    tweet_text = result.text
    tweet_user = result.user.screen_name
    tweet_text.replace("&amp;","&")
    return tweet_text, tweet_user


def tweet(tweet_text, tweet_user):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    result = "empty result"

    # Send the tweet and log success or failure
    try:
        result = api.update_status(tweet_text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + tweet_text.encode('utf-8')) 
      
    tweet_id = result.id_str 
    tweet_text = "(this honestly brought to you by @" + tweet_user + ")"

    try:
        result = api.update_status(tweet_text, tweet_id)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + tweet_text.encode('utf-8')) 
     

def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    tweet_text, tweet_user = create_tweet()  
    tweet(tweet_text, tweet_user)
