# pipeline_headphone_scrapping
(em construção)

O objetivo desse projeto é fazer uma pesquisa de mercado na categoria de headphones dentro da plataforma Magazineluiza.

O projeto deve avaliar os seguintes pontos:
1) Quais são as marcas mais encontradas até a 10 página de busca?
2) Qual o preço médio por marca?
3) Qual a pontuação de satisfação por marca?

Os resultados devem ser exibidos em um dashboard com informações originadas de um banco de dados.

Para rodar o web scrapping:
``scrapy crawl magazineluiza -o ../data/data_extracted.jsonl``

Para rodar o tratamento:
``python transformacao/tratamento.py``