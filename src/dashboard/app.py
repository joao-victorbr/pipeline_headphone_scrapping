import streamlit as st
import pandas as pd
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('/home/joao-vicbr/pipeline_headphone_scrapping/data/quotes.db')

# Carregar dados da tabela do banco em um dataframe pandas
df = pd.read_sql_query('SELECT * FROM magazineluiza_items', conn)

# Fechar conexão com o banco de dados
conn.close()

renamming = {
    'product_brand':'Marca',
    'product_name':'Nome do produto',
    'reviews_score':'Pontuação de reviews',
    'reviews_quantity':'Número de reviews',
    'old_price':'Preço antigo (R$)',
    'new_price':'Preço atual (R$)',
    'discount':'Desconto (%)',
}
df_renamed = df.rename(columns=renamming)

# Título da aplicação
st.title('Pesquisa de mercado - Headphones no Magazineluiza')
st.subheader('KPIs principais da pesquisa',divider='rainbow')

# # Exibir df inicial em tela
# st.write(df)

col1, col2, col3 = st.columns(3)

# KPI 1: Número total de registros
total_items = df_renamed.shape[0]
col1.metric(label = '**Número total de registros**', value = total_items)

# KPI 2: Número de marcas:
brands_quantity = df_renamed['Marca'].nunique()
col2.metric(label = '**Quantidade de marcas**', value = brands_quantity)

# KPI 3: Preço médio:
average_price = df_renamed['Preço atual (R$)'].mean().round(2)
col3.metric(label = '**Preço médio atual de headphones (R$)**', value = average_price)

# Gráficos e tabelas:
# Marcas mais encontradas
st.subheader('Marcas mais encontradas',divider='rainbow')
col1,col2 = st.columns([4, 2])
df_renamed['Anúncios'] = df_renamed.groupby('Marca')['Marca'].transform('count')
top_10_pages_brands = df_renamed['Marca'].value_counts(ascending=False)
col1.bar_chart(top_10_pages_brands.head(15),x_label='Marca', y_label='Quantidade de anúncios')
col2.write(top_10_pages_brands)

# Preço médio por marca
st.subheader('Preço médio por marca',divider='rainbow')
st.markdown('''Preço médio das 10 marcas com mais anúncios encontrados''')
col1,col2 = st.columns([4, 2])
df_avg_price = df_renamed.groupby('Marca')['Preço atual (R$)'].mean().sort_values(ascending=False).round(2)
df_quantity_items = df_renamed['Marca'].value_counts().sort_values(ascending=False)
avg_price_by_brand = pd.merge(df_avg_price, df_quantity_items, on='Marca', how='left').sort_values(by='count',ascending=False).rename(columns={'count':'Anúncios','Preço atual (R$)':'Preço médio (R$)'})
col1.bar_chart(avg_price_by_brand.drop(columns=['Anúncios']).head(10),x_label='Marca', y_label='Preço médio (R$)')
col2.write(avg_price_by_brand)

# Satifação por marca
st.subheader('Satifação por marca',divider='rainbow')
st.markdown('''Pontuação de reviews das 10 marcas com mais anúncios encontrados''')
col1,col2 = st.columns([4, 2])
df_non_zero_reviews = df_renamed[df_renamed['Pontuação de reviews']>0]
df_avg_score = df_non_zero_reviews.groupby('Marca')['Pontuação de reviews'].mean().sort_values(ascending=False).round(2)
satisfaction_by_brand = pd.merge(df_avg_score, df_quantity_items, on='Marca', how='left').sort_values(by='count',ascending=False).head(10).rename(columns={'count':'Anúncios'})
col1.bar_chart(satisfaction_by_brand.drop(columns=['Anúncios']), horizontal=True,x_label='Pontuação média por review', y_label='Marca')
col2.write(satisfaction_by_brand)

# Produtos com maiores descontos
st.subheader('Produtos com maiores descontos',divider='rainbow')
st.markdown('''Produtos com maiores descontos''')
# col1,col2 = st.columns([4, 2])
df_without_discounts = df_renamed[df_renamed['Desconto (%)']>0.0]
discount_by_brand = df_without_discounts.sort_values('Desconto (%)',ascending=False).drop_duplicates(subset=['Nome do produto']) # para remover anúncios repetidos para cores diferentes do mesmo headphone
# col1.bar_chart(discount_by_brand.head(10),x='Marca', y='Desconto (%)', horizontal=True)
# col2.write(discount_by_brand[['Marca','Nome do produto','Desconto (%)','Preço antigo (R$)','Preço atual (R$)','url_product']])
st.data_editor(
    discount_by_brand[['Marca','Nome do produto','Desconto (%)','Preço antigo (R$)','Preço atual (R$)','url_product']],
    column_config={
        "url_product": st.column_config.LinkColumn(
            "Link do produto", display_text="Link"
        ),
    },
    hide_index=True,
)
# col2.data_editor


