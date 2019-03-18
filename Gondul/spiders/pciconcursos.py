# -*- coding: utf-8 -*-
import scrapy
import Gondul.items


class PciconcursosSpider(scrapy.Spider):
    name = 'pciconcursos'
    allowed_domains = ['pciconcursos.com.br']
    start_urls = ['http://pciconcursos.com.br/']

    def parse(self, response):
        lista_concursos = response.xpath('//*[@id="capa"]/section')

        for section_concursos in lista_concursos: 
            yield scrapy.Request(
                        url = section_concursos.xpath('h3/a/@href').extract_first(),
                        callback = self.parse_detail
                )
 
 

    def parse_detail(self, response):
        url = response.url
        posted_at = response.xpath('//*[@id="noticia"]/abbr/@title').extract_first()
        title = response.xpath('//*[@id="noticia"]/h1/text()').extract_first()
        yield {
            'url' : url,
            'posted_at' : posted_at,
            'title' : title,
        }
               

    