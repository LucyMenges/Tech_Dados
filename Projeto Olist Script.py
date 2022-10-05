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

# %%
products = pd.read_csv('Tabelas\olist_products_dataset.csv')
products.head(10)

# %% [markdown]
# products: Informações sobre os produtos vendidos.

# %%
products.info()

# %%
sellers = pd.read_csv('Tabelas\olist_sellers_dataset.csv')
sellers.head(10)

# %% [markdown]
# sellers: informações sobre os vendedores

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

# %%


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
#     - Criando a coluna com o mês e ano da data de compra do pedido

# %%
orders['Mes_Ano_do_Pedido'] = orders['order_purchase_timestamp'].map(lambda x: 100*x.year +  x.month)
orders.head()

# %%
orders['Mes_Pedido'] = orders['order_purchase_timestamp'].dt.month
orders['Ano_Pedido'] = orders['order_purchase_timestamp'].dt.year

orders.head()

# %%
orders.Mes_Ano_do_Pedido.value_counts().sort_index()

# %%
orders.groupby('Mes_Ano_do_Pedido')

# %%
Qtdade_Pedidos = orders.groupby('Mes_Ano_do_Pedido').order_id.count()
Qtdade_Pedidos

# %%
orders.Mes_Ano_do_Pedido.value_counts().max()

# %%
plt.rcParams['figure.figsize'] = (25,8)
plt.subplot(1,1,1)
sns.distplot(Qtdade_Pedidos)
plt.axis()
plt.show()

# %%
orders.Mes_Ano_do_Pedido.value_counts().sort_index().plot()

# %% [markdown]
# 2b. Qual o mês com os maiores pagamentos (pagamentos/Valores).

# %%
order_payment.head()

# %%
order_payment.info()

# %%
total_vendas_mes = pd.merge(orders , order_payment, how = 'inner', on = 'order_id')
total_vendas_mes.head()

# %%
total_vendas_mes.groupby('Mes_Ano_do_Pedido').payment_value.sum()

# %%
total_vendas_mes.groupby('Mes_Ano_do_Pedido').payment_value.sum().max()

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


