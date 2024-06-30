import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('/home/joao-vicbr/pipeline_headphone_scrapping/data/quotes.db')

# Carregar dados da tabela do banco em um dataframe pandas
df = pd.read_sql_query('SELECT * FROM magazineluiza_items', conn)

# Fechar conexão com o banco de dados
conn.close()

# Título da aplicação
st.title('Pesquisa de mercado - Headphones no Magazineluiza')
st.subheader('KPIs principais da pesquisa')

# # Exibir df inicial em tela
# st.write(df)

col1, col2, col3 = st.columns(3)

# KPI 1: Número total de registros
total_items = df.shape[0]
col1.metric(label = 'Número total de registros', value = total_items)

# KPI 2: Número de marcas:
brands_quantity = df['product_brand'].nunique()
col2.metric(label = 'Quantidade de marcas', value = brands_quantity)

# KPI 3: Preço médio:
average_price = df['new_price'].mean().round(2)
col3.metric(label = 'Preço médio atual (R$)', value = average_price)

# Marcas mais encontradas até a 10ª página
st.subheader('Marcas mais encontradas até a 10ª página')
col1,col2 = st.columns([4, 2])
top_10_pages_brands = df['product_brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col1.write(top_10_pages_brands)

# Preço médio por marca
st.subheader('Preço médio por marca até a 10ª página')
col1,col2 = st.columns([4, 2])
average_price_by_brand = df.groupby('product_brand')['new_price'].mean().sort_values(ascending=False).round(2)
col1.bar_chart(average_price_by_brand)
col1.write(average_price_by_brand)

# Satifação por marca
st.subheader('Satifação por marca')
col1,col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['reviews_score']>0]
satisfaction_by_brand = df_non_zero_reviews.groupby('product_brand')['reviews_score'].mean().sort_values(ascending=False).round(2)
col1.bar_chart(satisfaction_by_brand)
col1.write(satisfaction_by_brand)


