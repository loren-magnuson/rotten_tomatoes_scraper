# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import json
import logging
from urllib.parse import urlencode
from rt_scraper.items import RtScraperItem
# from frontend.models import InstacartRetailer, InstacartDepartment, InstacartItem
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from math import ceil

class InstacartSpider(scrapy.Spider):
    name = 'rotten_tomatoes'
    allowed_domains = ['rottentomatoes.com']

    custom_settings = {
        'CONCURRENT_REQUESTS': '1',
        'DOWNLOAD_DELAY': '0',
        # 'LOG_FILE': 'logs/rotten_tomatoes.log'
    }


    def __init__(self):
        self.root_url = "https://www.rottentomatoes.com"
        self.browse_endpoint = "/api/private/v2.0/browse?"

    def start_requests(self):
        params = urlencode({"maxTomato" : 100,
                            "maxPopcorn": 100,
                            "services": "amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now",
                            "certified": False,
                            "sortBy": "release",
                            "type": "dvd-streaming-all",
                            "page": 1})
        request = Request(url="%s%s%s" % (self.root_url, self.browse_endpoint, params),
                      callback=self.parse)
        request.meta['is_root_request'] = True
        yield  request

    def parse(self, response):
        try:
            response_json = json.loads(response.body.decode("utf-8"))
        except Exception as e:
            logging.error("Error processing browse endpoint")
            return None

        if 'is_root_request' in response.request.meta:
            try:
                per_page = response_json['counts']['count']
                total = response_json['counts']['total']
                total_pages = int(ceil(total/per_page))
                print("Total pages: %s" % total_pages)
            except KeyError as e:
                logging.error(e)
                logging.error("Error processing page count")
                return None

            for page_number in range(2, total_pages+1):
                print("getting page %s" % page_number)
                yield Request(url=response.url.replace("page=1", "page=%s" % page_number),
                      callback=self.parse)

        if 'results' in response_json:

            for item_dict in response_json['results']:
                for key, value in item_dict.copy().items():
                    try:
                        the_key = vars(RtScraperItem)['fields'][key]
                    except KeyError as e:
                        del item_dict[key]
                    else:
                        item_dict[key] = value

                yield(RtScraperItem(**item_dict))





