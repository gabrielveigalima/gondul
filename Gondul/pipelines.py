# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# ATENÇÃO NA VARIALVEL sources, SE FOR IGUAL A:
# 0 A FONTE É O PCICONCURSOS;
# 1 A FONTE É O FOLHA DIRIGIDA;

import os
import simplejson
from sqlalchemy import create_engine
import sqlalchemy

class DeolhoPipeline(object):
    def process_item(self, item, spider):
        spider.log('------- CAPTURADO --------')

        #Buscando a fonte cadastrada na tabela sources
        sources = None
        domain = item['url'].split('noticias')[:-1]
        if 'https://www.pciconcursos.com.br/' == domain[0]:
            domain_complete = domain[0]+"noticias/"
            sources = 0
            spider.log('------- PCICONCURSOS --------')

        elif 'https://folhadirigida.com.br/' == domain[0]:
            domain_complete = domain[0] + "noticias/concurso/"
            sources = 1
            spider.log('------- FOLHADIRIGIDA --------')

        query = '''
			     SELECT id
			     FROM sources 
			     WHERE domain = '{}'
			    '''.format(domain_complete)


        result_query = self.timescale_engine.execute(query)
        result = next(result_query)



		#Verificando se a notícia já foi cadastrada
        if sources == 0:
            url_clean = item['url'].split('/')[len(item['url'].split('/'))-1]
        elif sources == 1:
            url_clean = item['url'].split('/')[5]+'/'+item['url'].split('/')[6]

        query_news = '''
			     SELECT COUNT(*)
			     FROM news
			     WHERE url = '{}' AND source_id = '{}'
			    '''.format(url_clean,result[0])


        result_query_news = self.timescale_engine.execute(query_news)
        result_news = next(result_query_news)

        if result_news[0] < 1:
            spider.log('=================== Não cadastrada =====================')

        	#Cadastrando notícias
            query_news_insert = '''
			     INSERT INTO news
			     (
			     	created_at,updated_at,url,title,posted_at,source_id,relevance
			     )
			     VALUES
			     (
			     	NOW(),NULL,'{}','{}','{}',{},0
			     )
			    '''.format(url_clean,item['title'],item['posted_at'],result[0])
            try:
                result_query_news_insert = self.timescale_engine.execute(query_news_insert)
                return result_query_news_insert
            except StopIteration as ex:
                return ex
        


    def open_spider(self, spider):
    	# Conectando ao Timescale
        with open("../Credentials/timescale.json") as fh:
            red_creds = simplejson.loads(fh.read())
    
        connection_string = "postgresql+psycopg2://{user}:{passw}@{host}/{db}".format(user=red_creds['user'],
                                                               passw=red_creds['pass'],
                                                               host=red_creds['host'],
                                                               db=red_creds['db'])
        timescale_db_alias = "{user}@{db}".format(user=red_creds['user'],db=red_creds['db'])

        self.timescale_engine = create_engine(connection_string)


    def close_spider(self, spider):
        #timescale_engine.close()   
        pass 	

