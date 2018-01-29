# -*- coding: utf-8 -*-
from scrapy import Item, Field


class User(Item):
    ID = Field()                # user id
    name = Field()              # user name
    screen_name = Field()       # user screen name
    avatar = Field()            # avatar url
    location = Field()          # city, country
    nbr_tweets = Field()        # nbr of tweets
    nbr_following = Field()     # nbr of following
    nbr_followers = Field()     # nbr of followers
    nbr_likes = Field()         # nbr of likes
