# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RtScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tomatoScore = scrapy.Field()
    mainTrailer = scrapy.Field()
    tomatoIcon = scrapy.Field()
    url = scrapy.Field()
    actors = scrapy.Field()
    title = scrapy.Field()
    popcornScore = scrapy.Field()
    synopsisType = scrapy.Field()
    id = scrapy.Field()
    dvdReleaseDate = scrapy.Field()
    posters = scrapy.Field()
    runtime = scrapy.Field()
    mpaaRating = scrapy.Field()
    synopsis = scrapy.Field()
    theaterReleaseDate = scrapy.Field()
    popcornIcon = scrapy.Field()

    pass
