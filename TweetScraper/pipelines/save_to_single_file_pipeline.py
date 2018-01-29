# -*- coding: utf-8 -*-
import json

from scrapy.conf import settings
import logging
import os

from TweetScraper.items.tweet import Tweet
from TweetScraper.items.user import User
from TweetScraper.utils import mkdirs, save_to_file

logger = logging.getLogger(__name__)


class SaveToSingleFilePipeline(object):
    """ pipeline that save all data to a single file on disk """

    def __init__(self):
        self.tweets_file = None
        self.users_file = None

        self.saveTweetPath = settings['SAVE_TWEET_PATH']
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveTweetPath)  # ensure the path exists
        mkdirs(self.saveUserPath)

    def open_spider(self, spider):
        self.tweets_file = open(os.path.join(self.saveTweetPath, "tweets.ji"), "w")
        self.users_file = open(os.path.join(self.saveUserPath, "users.ji"), "w")

    def close_spider(self, spider):
        self.tweets_file.close()
        self.users_file.close()

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            self.tweets_file.write(json.dumps(item.__dict__))
            logger.debug("Add tweet:%s" % item['url'])

        elif isinstance(item, User):
            self.users_file.write(json.dumps(item.__dict__))
            logger.debug("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))
