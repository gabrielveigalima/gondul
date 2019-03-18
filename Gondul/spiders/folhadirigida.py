# -*- coding: utf-8 -*-
import scrapy
import os
import time
from scrapy_splash import SplashRequest
import numpy as np


class FolhadirigidaSpider(scrapy.Spider):
    name = 'folhadirigida'

    start_urls = ['https://folhadirigida.com.br/noticias?page=1']

    def parse(self, response):
        num_page = response.xpath('/html/body/section/div[3]/main/ul/li[12]/a/text()').extract_first()

        for number_this_page in np.arange(1,int(num_page)+1):
            yield scrapy.Request(
                url = 'https://folhadirigida.com.br/noticias?page='+str(number_this_page),
                callback = self.parse_page_home
            )


    def parse_page_home(self, response):
        #news = response.xpath('/html/body/section/div[3]/main/section//article')
        news = response.xpath('/html/body/section/div[3]/main/section//article/meta[4]')
        for new in news:
            url = new.xpath('@content').extract_first()
            yield scrapy.Request(
                url = url,
                callback = self.parse_page_new
            )
            time.sleep(1)
    def parse_page_new(self, response):
        url = response.url
        title1 = response.xpath('//*[@id="noticia"]/abbr/@title').extract_first()
        title = response.xpath('//title/text()').extract_first()
        posted_at = response.xpath('/html/body/section/div[2]/main/section[1]/article/div[1]/time[1]/@datetime').extract_first()

        self.log('================= ok ================')
        self.log(url)
        self.log(title[:-17])
        self.log(posted_at)


        yield {
            'url' : url,
            'posted_at' : posted_at,
            'title' : title[:-17],
        }
