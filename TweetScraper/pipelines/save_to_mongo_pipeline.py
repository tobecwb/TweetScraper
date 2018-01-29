# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.conf import settings
import logging
import pymongo

from TweetScraper.items.tweet import Tweet
from TweetScraper.items.user import User

logger = logging.getLogger(__name__)


class SaveToMongoPipeline(object):
    """ pipeline that save data to mongodb """

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        self.updateItem = settings['MONGODB_UPDATE']

        db = connection[settings['MONGODB_DB']]
        self.tweetCollection = db[settings['MONGODB_TWEET_COLLECTION']]
        self.userCollection = db[settings['MONGODB_USER_COLLECTION']]

        self.tweetCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)
        self.tweetCollection.ensure_index([('usernameTweet', pymongo.ASCENDING)])
        self.tweetCollection.ensure_index([('datetime', pymongo.ASCENDING)])
        self.tweetCollection.ensure_index([('user_id', pymongo.ASCENDING)])
        self.userCollection.ensure_index([('ID', pymongo.ASCENDING)], unique=True, dropDups=True)

    # convert field types (from string to int and datetime)
    def convert_fields(self, item):
        mongo_entity = dict(item)

        # convert string datetime to true datetime
        mongo_entity['datetime'] = datetime.strptime(mongo_entity['datetime'], "%Y-%m-%d %H:%M:%S")
        mongo_entity['ID'] = int(mongo_entity['ID'])  # convert id to a number
        mongo_entity['user_id'] = int(mongo_entity['user_id'])  # convert user_id to a number

        return mongo_entity

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            db_item = self.tweetCollection.find_one({'ID': item['ID']})
            if db_item:
                if self.updateItem:
                    mongo_entity = self.convert_fields(item)
                    db_item.update(mongo_entity)
                    self.tweetCollection.save(db_item)
                    logger.info("Update tweet: %s" % db_item['url'])

            else:
                mongo_entity = self.convert_fields(item)
                self.tweetCollection.insert_one(mongo_entity)
                logger.debug("Add tweet: %s" % item['url'])

        elif isinstance(item, User):
            db_item = self.userCollection.find_one({'ID': item['ID']})
            if db_item:
                if self.updateItem:
                    db_item.update(dict(item))
                    self.userCollection.save(db_item)
                    logger.info("Update user: %s" % db_item['screen_name'])
            else:
                self.userCollection.insert_one(dict(item))
                logger.debug("Add user: %s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))
