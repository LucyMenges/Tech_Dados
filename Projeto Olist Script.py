# %% [markdown]
# # RESIDÊNCIA TECH
# *** PROJETO OLIST ***

# %% [markdown]
# #Sobre o banco de dados: 
# Este conjunto de dados foi generosamente fornecido pela Olist, a maior loja de departamentos dos marketplaces brasileiros. A Olist conecta pequenas empresas de todo o Brasil a canais sem complicações e com um único contrato. Esses comerciantes podem vender seus produtos através da Olist Store e enviá-los diretamente aos clientes usando os parceiros de logística da Olist. Veja mais no site: www.olist.com
# 

# %% [markdown]
# ## Inicialização
# 
# Importando bibliotecas e a carga inicial dos dados para análise

# %%
#Importando a biblioteca Pandas
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# %% [markdown]
# ### Lendo os arquivos de Vendas Olist
# Os arquivos csvs são referentes a vendas reais de e-commerce. 

# %% [markdown]
# * customers = Informações sobre o cliente e sua localização. (99.441 linhas e 5 colunas)
# 
# customer_id, customer_unique_id, customer_zip_code_prefix,	customer_city,	customer_state

# %%
customers = pd.read_csv ('D:\Harve Residencia Tech\Projetos\Projeto Olist\Projeto Olist Script\Tabelas\olist_customers_dataset.csv')
customers.head()

# %%
customers.info() 

# %% [markdown]
# * geolocation = Informações de CEPs brasileiros e suas coordenadas latitude/longitude.

# %%
geolocation = pd.read_csv ('Tabelas\olist_geolocation_dataset.csv')
geolocation.head()

# %%
geolocation.info()

# %% [markdown]
# * order_items: Informações sobre a quantidade de itens do pedido e os preços do produto e do frete individual.

# %%
orders_items = pd.read_csv ('Tabelas\olist_order_items_dataset.csv')
orders_items.head()


# %%
orders_items.info()

# %% [markdown]
# * order_payment: Informações de opções de pagamento de pedidos.

# %%
order_payment = pd.read_csv ('Tabelas\olist_order_payments_dataset.csv')
order_payment.head()

# %%
order_payment.info()

# %% [markdown]
# * order_reviews: Dados de avaliações feitas pelos clientes.

# %%
order_reviews = pd.read_csv('Tabelas\olist_order_reviews_dataset.csv')
order_reviews.head(10)

# %%
order_reviews.info()

# %% [markdown]
# * orders: Dados a respeito do pedido (estampa de tempo da compra, aprovação, entrega para logística, recebimento, previsão de entrega).

# %%
orders = pd.read_csv('Tabelas\olist_orders_dataset.csv')
orders.head(10)

# %%
orders.info()

# %% [markdown]
# products: Informações sobre os produtos vendidos.

# %%
products = pd.read_csv('Tabelas\olist_products_dataset.csv')
products.head(10) 

# %%
products.info()

# %% [markdown]
# sellers: informações sobre os vendedores

# %%
sellers = pd.read_csv('Tabelas\olist_sellers_dataset.csv')
sellers.head(10)

# %%
sellers.info()

# %%
product_category = pd.read_csv('Tabelas\product_category_name_translation.csv')
product_category.head()

# %% [markdown]
# product_category: tradução das categorias dos produtos

# %%
product_category.info()

# %% [markdown]
# # Limpeza do Conjunto

# %% [markdown]
# - Alteração do tipo da coluna orders_items[shipping_limit_date] para DATETIME.

# %%
orders_items['shipping_limit_date'] = pd.to_datetime(orders_items['shipping_limit_date'])
orders_items.info()

# %% [markdown]
# - Alteração do tipo das colunas orders_reviews[review_creation_date] e orders_review[review_answer_timestamp] para DATETIME.

# %%
order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'])
order_reviews.info()

# %% [markdown]
# ### Análise e Limpeza da tabela 'Orders' (Pedidos)

# %%
orders.head(10)

# %% [markdown]
# #### Contando valores não nulos, unique e a frequência do valor mais comum
# - Observações:
#     * Os pedidos têm oito diferentes tipos de status. 
#     * Valores nulos em três colunas

# %%
orders.describe(include=[object])

# %% [markdown]
# - Nenhuma linha vazia nesta tabela

# %%
B = orders.dropna(how='all').shape
B

# %% [markdown]
# - Tipos de Status

# %%
orders.order_status.unique()

# %% [markdown]
# - Quantidade de pedidos por tipo de status

# %%
orders.groupby('order_status').order_id.count().sort_values(ascending = False)

# %% [markdown]
# - Alterando o tipo de algumas colunas para DATETIME

# %%
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

orders.dtypes

# %% [markdown]
# - Quantidade de valores nulos nas colunas da Tabela 'Orders'

# %%

orders.isnull().sum()

# %% [markdown]
# - Tempo de entrega dos pedidos

# %%
# Acrescentando uma coluna com o tempo de entrega dos produtos em dias
orders['tempo_entrega']= round((orders.order_delivered_customer_date - orders.order_approved_at) / np.timedelta64(1,'D'),0)
orders.head()


# %% [markdown]
# * Colocando filtro para retirar os pedidos cancelados, datas vazias das colunas pedido aprovado e entraga ao cliente.

# %%
orders_validas = orders[(orders.order_status != 'canceled') & (orders.order_approved_at.notnull()) & (orders.order_delivered_customer_date.notnull())]
orders_validas

# %%
print(orders.shape)
print(orders_validas.shape)

# %% [markdown]
# - Gráfico com a distribuição dos tempos de entrega dos pedidos.

# %%
plt.rcParams['figure.figsize'] = (25,8)
plt.subplot(1,1,1)
sns.distplot(orders_validas['tempo_entrega'])
plt.show

# %% [markdown]
# * Verificando os outliers.

# %%
print(orders_validas.tempo_entrega.min())
print(orders_validas.tempo_entrega.max())

# %% [markdown]
# * Temos 38 pedidos com tempo de entrega negativo. 

# %%
print(orders_validas[orders_validas.tempo_entrega < 0].shape)

# %%
orders_validas[orders_validas.tempo_entrega < 0].head()

# %% [markdown]
#     * O tempo negativo se deve ao fato de que alguns pedidos foram aprovados após a entrega. 

# %%
orders_validas[orders_validas.tempo_entrega > 150].head()

# %%
orders_validas[orders_validas.tempo_entrega > 60].shape

# %% [markdown]
# - Distribuição do tempo de entrega em grupos para melhor análise.

# %% [markdown]
# 1. Qual é o tempo médio/mediano desde a aprovação do pedido até a sua entrega?

# %%
# TEMPO MÉDIO EM DIAS TABELA ORIGINAL
orders.tempo_entrega.mean()

# %%
# TEMPO MÉDIO EM DIAS, SEM OS VALORES NEGATIVOS
orders_validas[orders_validas.tempo_entrega >= 0].tempo_entrega.mean()

# %%
# TEMPO MEDIANO EM DIAS TABELA ORIGINAL
orders.tempo_entrega.median()

# %%
# TEMPO MEDIANO EM DIAS, SEM OS VALORES NEGATIVOS
orders_validas[orders_validas.tempo_entrega >= 0].tempo_entrega.median()

# %% [markdown]
# 2a. Qual o mês com maior quantidade de vendas (em número de pedido)

# %% [markdown]
#     - Criando um novo dataframe com coluna de mês e ano da data de compra do pedido, além dos pedidos.

# %%
meses_compras = pd.DataFrame()
meses_compras['mes'] = orders['order_purchase_timestamp'].dt.month
meses_compras['ano'] = orders['order_purchase_timestamp'].dt.year
meses_compras['Qtidade_pedidos'] = orders['order_id']
meses_compras = meses_compras.groupby(['ano','mes'])['Qtidade_pedidos'].count().reset_index()

meses_compras['ano_mes'] = meses_compras['ano'].astype(str) + '/' + meses_compras['mes'].astype(str)

meses_compras.head()

# %% [markdown]
#     - Visualização da quantidade de vendas por Mês

# %%
grafico_pedidos = meses_compras.plot(kind='bar', x='ano_mes', y='Qtidade_pedidos', figsize=(25,8))

plt.title('Gráfico de Qtidade de Pedidos', fontsize=18, pad=20)
plt.xlabel('Ano/Mês', size =14)
plt.ylabel('Qtidade de Pedidos', size=14,)
plt.show


# %%
meses_compras.iloc[meses_compras[['Qtidade_pedidos']].idxmax()]

# %% [markdown]
# 2b. Qual o mês com os maiores pagamentos (pagamentos/Valores).

# %%
meses_pagtos = pd.DataFrame()
meses_pagtos['mes'] = orders['order_purchase_timestamp'].dt.month
meses_pagtos['ano'] = orders['order_purchase_timestamp'].dt.year
meses_pagtos['Total_Vendas'] = order_payment['payment_value']

meses_pagtos = meses_pagtos.groupby(['ano','mes'])['Total_Vendas'].sum().reset_index()

meses_pagtos['ano_mes1'] = meses_pagtos['ano'].astype(str) + '/' + meses_pagtos['mes'].astype(str)

meses_pagtos

# %%
grafico_pgtos = meses_pagtos.plot(kind='bar', x='ano_mes1', y='Total_Vendas', figsize=(25,8))

plt.title('Gráfico de Total Vendas', fontsize=18, pad=20)
plt.xlabel('Ano/Mês', size =14)
plt.ylabel('Total_Vendas', size=14)
plt.show

# %%
meses_pagtos.iloc[meses_pagtos[['Total_Vendas']].idxmax()]

# %% [markdown]
# 3. Avalie a satisfação dos clientes: 
# i) notas; ii) estão realizando comentários?
# 
# Notas: de 1 a 5, onde 5 é muito bom e 1 ruim

# %%
order_reviews.head()

# %%
a = order_reviews.groupby('review_score').review_comment_message.count()
a

# %%
Coment_Notas = pd.read_csv ('Tabelas\Tabela_Comentarios_por_Notas.csv')
Coment_Notas

# %% [markdown]
# 4.	Existe algum padrão entre a satisfação do cliente com a entrega antes ou depois do prazo previsto?

# %%
orders['Diferença_Previsão_Realiz_Entrega']= round((orders.order_delivered_customer_date - orders.order_estimated_delivery_date) / np.timedelta64(1,'D'),0)
orders.head()

# %%
m = pd.merge(orders, order_reviews, how= 'inner', on = 'order_id')

m.groupby('review_score').Diferença_Previsão_Realiz_Entrega.count()


# %%
m = pd.merge(tabela_1, tabela_2, how = 'inner', on = 'Nome')

# %% [markdown]
# 5.	Quais as categorias de produtos mais vendidos? E os menos vendidos? Existe relação com os preços dos itens? A quantidade de fotos impacta nas vendas?

# %%
categ_prod_vendas = pd.DataFrame()
categ_prod_vendas['pedidos'] = order_payment['order_id']
categ_prod_vendas['Total_Vendas'] = order_payment['payment_value']
categ_prod_vendas['Produto'] = orders_items['product_id']
categ_prod_vendas['Categorias'] = products['product_category_name']

categ_prod_vendas = categ_prod_vendas.groupby(['Categorias'])['Total_Vendas'].sum().sort_values(ascending=False).reset_index()
#categ_prod_vendas

categ_prod_vendas

# %%
categ_prod_vendas['Total_Vendas'].sum()

# %%
categ_prod_vendas.iloc[categ_prod_vendas[['Total_Vendas']].idxmax()]

# %%
meses_pagtos = pd.DataFrame()
meses_pagtos['mes'] = orders['order_purchase_timestamp'].dt.month
meses_pagtos['ano'] = orders['order_purchase_timestamp'].dt.year
meses_pagtos['Total_Vendas'] = order_payment['payment_value']

meses_pagtos = meses_pagtos.groupby(['ano','mes'])['Total_Vendas'].sum().reset_index()

meses_pagtos['ano_mes1'] = meses_pagtos['ano'].astype(str) + '/' + meses_pagtos['mes'].astype(str)

meses_pagtos

# %%


# %% [markdown]
# 6.	O volume e o peso dos produtos impactam no valor do frete?

# %%


# %% [markdown]
# 7.	Avaliação/Visualização da posição geográfica onde se encontra a maior concentração de clientes e vendedores.

# %%


# %% [markdown]
# 8.	As entregas atrasadas aconteceram entre vendedores/compradores de estados diferentes?

# %%


# %% [markdown]
# 9.	Identificar o padrão dos clientes (localização, método de pagamento, quantidade de parcelas, entrega antes da previsão, notas de satisfação média, tipos de produtos) que fizeram uma recompra no site

# %%



