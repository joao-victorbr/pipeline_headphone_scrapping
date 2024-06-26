# importação de lib:
import pandas as pd
import sqlite3
from datetime import datetime

# Definir caminho do arquivo csv
df = pd.read_json('../data/data_extracted.jsonl',lines=True)

# Configurar pandas para exibir todas as colunas:
pd.options.display.max_columns = None

# Descartas linhas duplicadas:
df = df.drop_duplicates()

# Novas colunas:
df['src'] = 'https://www.magazineluiza.com.br/busca/headphone/?from=submit'
df['data_coleta'] = datetime.now()

# Tratar tipos de colunas e nulos:
df['old_price'] = df['old_price'].fillna(0.0).astype('float')
df['new_price'] = df['new_price'].fillna(0.0).astype('float')
df['product_brand'] = df['product_brand'].astype('string')
df['product_name'] = df['product_name'].astype('string')
df['src'] = df['src'].astype('string')
df['reviews_score'] = df['reviews_score'].fillna(0.0).astype('float')
df['reviews_quantity'] = df['reviews_quantity'].fillna(0).astype('int')

# Uma marca foi coletada como "headphone". Para retirar esse dado incorreto, será feito um filtro:
df = df[df['product_brand']!='headphone']

# Coluna de desconto:
df['discount'] = (((df['old_price'] - df['new_price']) / df['old_price']) * 100).round(1).astype('float')

# Conectar ao banco de dados SQLite:
conn = sqlite3.connect('../data/quotes.db')

# Salvar dataframe no banco SQLite:
df.to_sql('magazineluiza_items', conn, if_exists='replace', index=False)

# Fechar conexão com o banco de dados:
conn.close()
