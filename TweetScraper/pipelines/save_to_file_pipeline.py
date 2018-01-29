# -*- coding: utf-8 -*-
from scrapy.conf import settings
import logging
import os

from TweetScraper.items.tweet import Tweet
from TweetScraper.items.user import User
from TweetScraper.utils import mkdirs, save_to_file

logger = logging.getLogger(__name__)


class SaveToFilePipeline(object):
    """ pipeline that save data to disk """

    def __init__(self):
        self.saveTweetPath = settings['SAVE_TWEET_PATH']
        self.saveUserPath = settings['SAVE_USER_PATH']
        mkdirs(self.saveTweetPath)  # ensure the path exists
        mkdirs(self.saveUserPath)

    def process_item(self, item, spider):
        if isinstance(item, Tweet):
            save_path = os.path.join(self.saveTweetPath, item['ID'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update tweet:%s"%dbItem['url'])
            else:
                save_to_file(item, save_path)
                logger.debug("Add tweet:%s" % item['url'])

        elif isinstance(item, User):
            save_path = os.path.join(self.saveUserPath, item['ID'])
            if os.path.isfile(save_path):
                pass  # simply skip existing items
                # or you can rewrite the file, if you don't want to skip:
                # self.save_to_file(item,savePath)
                # logger.info("Update user:%s"%dbItem['screen_name'])
            else:
                save_to_file(item, save_path)
                logger.debug("Add user:%s" % item['screen_name'])

        else:
            logger.info("Item type is not recognized! type = %s" % type(item))
