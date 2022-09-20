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
# Importando a biblioteca Pandas
import pandas as pd


# %% [markdown]
# ##Lendo os arquivos de Vendas Olist
# Os arquivos csvs são referentes a vendas reais de e-commerce.

# %%
customers = pd.read_csv('olist_customers_dataset.csv')
customers.head()

# %%
customers.info()

# %% [markdown]
# customers = Informações sobre o cliente e sua localização.
# customer_id,	customer_unique_id,	customer_zip_code_prefix,	customer_city,	customer_state

# %%
geolocation = pd.read_csv('olist_geolocation_dataset.csv')
geolocation.head()

# %% [markdown]
# geolocation = Informações de CEPs brasileiros e suas coordenadas latitude/longitude.

# %%
geolocation.info()

# %%
orders_items = pd.read_csv('olist_order_items_dataset.csv')
orders_items.head()


# %% [markdown]
# order_items: Informações sobre a quantidade de itens do pedido e os preços do produto e do frete individual.

# %%
orders_items.info()

# %%
order_payment = pd.read_csv('olist_order_payments_dataset.csv')
order_payment.head()

# %% [markdown]
# ●	order_payment: Informações de opções de pagamento de pedidos.

# %%
order_payment.info()

# %%
order_reviews = pd.read_csv('olist_order_reviews_dataset.csv')
order_reviews.head(20)

# %% [markdown]
# order_reviews: Dados de avaliações feitas pelos clientes.

# %%
order_reviews.info()

# %%
orders = pd.read_csv('olist_orders_dataset.csv')
orders.head(10)

# %% [markdown]
#

# %% [markdown]
# orders: Dados a respeito do pedido (estampa de tempo da compra, aprovação, entrega para logística, recebimento, previsão de entrega).

# %%
orders.info()

# %%
products = pd.read_csv('olist_products_dataset.csv')
products.head(10)

# %% [markdown]
# products: Informações sobre os produtos vendidos.

# %%
products.info()

# %%
sellers = pd.read_csv('olist_sellers_dataset.csv')
sellers.head(10)

# %% [markdown]
# sellers: informações sobre os vendedores

# %%
sellers.info()

# %%
product_category = pd.read_csv('product_category_name_translation.csv')
product_category.head()

# %% [markdown]
# product_category: tradução das categorias dos produtos

# %%
product_category.info()

# %% [markdown]
# # Limpeza do Conjunto

# %% [markdown]
# ## Análise e Limpeza da tabela 'Orders' (Pedidos)

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
# - Quantidade de linhas por tipo de status

# %%
orders.order_status.drop_duplicates()

# %% [markdown]
# - Alterando o tipo de algumas colunas para DATETIME

# %%
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(
    orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(
    orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(
    orders['order_estimated_delivery_date'])

orders.dtypes

# %%

orders.dtypes

# %% [markdown]
# - Quantidade de valores nulos nas colunas da Tabela 'Orders'

# %%

orders.isnull().sum()