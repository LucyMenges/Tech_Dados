# %% [markdown]
# -*- coding: utf-8 -*-
# @author: Residencia Tech Analista Dados - Luciana Lanzoni Menges (10/2022)

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
# Os arquivos .csv são referentes a vendas reais de e-commerce. 

# %% [markdown]
# * customers = Informações sobre o cliente e sua localização. (99.441 linhas e 5 colunas)

# %%
customers = pd.read_csv ('D:\Harve Residencia Tech\Projetos\Projeto Olist\Projeto Olist Script\Tabelas\olist_customers_dataset.csv')
customers.head()

# %%
customers.info() 

# %% [markdown]
# * geolocation = Informações de CEPs brasileiros e suas coordenadas latitude/longitude. (1.000.163 linhas, 5 colunas)

# %%
geolocation = pd.read_csv ('Tabelas\olist_geolocation_dataset.csv')
geolocation.head()

# %%
geolocation.info()

# %% [markdown]
# * order_items: Informações sobre a quantidade de itens do pedido e os preços do produto e do frete individual. (112.650 linhas, 7 colunas)

# %%
orders_items = pd.read_csv ('Tabelas\olist_order_items_dataset.csv')
orders_items.head()


# %%
orders_items.info()

# %% [markdown]
# * order_payment: Informações de opções de pagamento de pedidos. (103.886 linhas, 5 colunas)

# %%
order_payment = pd.read_csv ('Tabelas\olist_order_payments_dataset.csv')
order_payment.head()

# %%
order_payment.info()

# %% [markdown]
# * order_reviews: Dados de avaliações feitas pelos clientes. (99.224 linhas, 7 colunas)

# %%
order_reviews = pd.read_csv('Tabelas\olist_order_reviews_dataset.csv')
order_reviews.head(10)

# %%
order_reviews.info()

# %% [markdown]
# * orders: Dados a respeito do pedido (estampa de tempo da compra, aprovação, entrega para logística, recebimento, previsão de entrega). (99.441 linhas, 8 colunas)

# %%
orders = pd.read_csv('Tabelas\olist_orders_dataset.csv')
orders.head(10)

# %%
orders.info()

# %% [markdown]
# * products: Informações sobre os produtos vendidos. (32.951 linhas, 9 colunas)

# %%
products = pd.read_csv('Tabelas\olist_products_dataset.csv')
products.head(10) 

# %%
products.info()

# %% [markdown]
# * sellers: informações sobre os vendedores. (3.095 linhas, 4 colunas)

# %%
sellers = pd.read_csv('Tabelas\olist_sellers_dataset.csv')
sellers.head(10)

# %%
sellers.info()

# %% [markdown]
# * product_category: tradução das categorias dos produtos. (71 linhas, 2 colunas)

# %%
product_category = pd.read_csv('Tabelas\product_category_name_translation.csv')
product_category.head()

# %%
product_category.info()

# %% [markdown]
# ## Limpeza do Conjunto

# %% [markdown]
# ### Alteração do tipo de coluna

# %% [markdown]
# - DataFrame: orders_items. Alteração do tipo da coluna orders_items[shipping_limit_date] para DATETIME.

# %%
orders_items['shipping_limit_date'] = pd.to_datetime(orders_items['shipping_limit_date'])
orders_items.info()

# %% [markdown]
# - DataFrame: orders_reviews. Alteração do tipo das colunas orders_reviews[review_creation_date] e orders_review[review_answer_timestamp] para DATETIME.

# %%
order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'])
order_reviews.info()

# %% [markdown]
# - DataFrame: orders. Alterando o tipo de cinco colunas para DATETIME

# %%
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

orders.dtypes

# %% [markdown]
# ### Análise e Limpeza da tabela 'Orders' (Pedidos)

# %%
orders.head(10)

# %% [markdown]
# #### Contando valores nulos, unique e a frequência do valor mais comum
# - Observações:
#      * Valores nulos em três colunas: order_approved_at, order_delivered_carrier_date e order_delivered_customer_date
#     * Os pedidos têm oito diferentes tipos de status. 

# %%
orders.describe(include=[object])

# %%
orders.describe(datetime_is_numeric=True)

# %% [markdown]
# - Quantidade de valores nulos nas colunas da Tabela 'Orders'

# %%
orders.isnull().sum()

# %% [markdown]
#         * Estes valores nulos em três colunas indica que o dataset é uma fotografia de um determinado momento. Ou seja não de um período com os processos todos fechados.

# %% [markdown]
# - Tipos de Status

# %%
orders.order_status.unique()

# %% [markdown]
# - Quantidade de pedidos por tipo de status

# %%
orders.groupby('order_status').order_id.count().sort_values(ascending = False).reset_index()

# %% [markdown]
# ## Backlog´s demandados pelo Product Owner

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
orders_validas.head()

# %%
print(orders.shape)
print(orders_validas.shape)

# %%
orders_validas.info()

# %% [markdown]
# - Gráfico com a distribuição dos tempos de entrega dos pedidos.

# %%

plt.rcParams["figure.figsize"]= (20,6)
plt.subplot(1,1,1)
sns.distplot(orders_validas['tempo_entrega']) #, kde = False
plt.xlim(left= -7,right=209)
plt.savefig('GraficoTempoEntrega.png', dpi= 600, bbox_inches = 'tight')
plt.show()

# %% [markdown]
#         * 92,8% dos pedidos são entregues até o 25o.dia após a aprovação do pedido.

# %%
ped_tempo_entrega = orders_validas.groupby('tempo_entrega')['order_id'].count().reset_index()
total_pedidos = ped_tempo_entrega['order_id'].sum()

ped_tempo_entrega['%_do_total_ped']= round((ped_tempo_entrega['order_id']/ total_pedidos *100),3)

ped_tempo_entrega.head(15)

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
orders_validas[orders_validas.tempo_entrega >= 40].shape

# %% [markdown]
#     * 1753 ou 1,82% do total de pedidos são entregues após 40 dias.

# %% [markdown]
# #### 1. Qual é o tempo médio/mediano desde a aprovação do pedido até a sua entrega?

# %%
# TEMPO MÉDIO EM DIAS TABELA ORIGINAL
orders.tempo_entrega.mean()

# %%
# TEMPO MÉDIO EM DIAS, SEM OS VALORES NEGATIVOS E SEM CANCELADOS
orders_validas[orders_validas.tempo_entrega >= 0].tempo_entrega.mean()

# %%
# TEMPO MEDIANO EM DIAS TABELA ORIGINAL
orders.tempo_entrega.median()

# %%
# TEMPO MEDIANO EM DIAS, SEM OS VALORES NEGATIVOS E SEM CANCELADOS
orders_validas[orders_validas.tempo_entrega >= 0].tempo_entrega.median()

# %% [markdown]
# #### 2a. Qual o mês com maior quantidade de vendas (em número de pedido)

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
# #### 2b. Qual o mês com os maiores pagamentos (pagamentos/Valores).

# %%
meses_pagtos = pd.DataFrame()
meses_pagtos['mes'] = orders['order_purchase_timestamp'].dt.month
meses_pagtos['ano'] = orders['order_purchase_timestamp'].dt.year
meses_pagtos['Total_Vendas'] = order_payment['payment_value']

meses_pagtos = meses_pagtos.groupby(['ano','mes'])['Total_Vendas'].sum().reset_index()

meses_pagtos['ano_mes1'] = meses_pagtos['ano'].astype(str) + '/' + meses_pagtos['mes'].astype(str)

meses_pagtos

# %%
from matplotlib.ticker import FuncFormatter

# %%
def mil (x,pos):
    return f'R$ {x * 1e-3:.0f}k'

# %%
formatter = FuncFormatter(mil)

# %%
grafico_pgtos = meses_pagtos.plot(kind='bar', x='ano_mes1', y='Total_Vendas', figsize=(25,8))
grafico_pgtos.yaxis.set_major_formatter(formatter)
plt.title('Gráfico de Total Vendas', fontsize=18, pad=20)
plt.xlabel('Ano/Mês', size =14)
plt.ylabel('Total_Vendas', size=14)
plt.show

# %%
meses_pagtos.iloc[meses_pagtos[['Total_Vendas']].idxmax()]

# %% [markdown]
# #### 3. Avalie a satisfação dos clientes: a) notas; b) estão realizando comentários?

# %% [markdown]
# * Notas: de 1 a 5, onde 5 é muito bom e 1 ruim

# %%
order_reviews.head()

# %%
total_notas = order_reviews.groupby('review_score').review_comment_message.count().reset_index()
total_notas

# %%
Coment_Notas = pd.read_csv ('Tabelas\Tabela_Comentarios_por_Notas.csv')
Coment_Notas

# %% [markdown]
# #### 4.	Existe algum padrão entre a satisfação do cliente com a entrega antes ou depois do prazo previsto?

# %% [markdown]
# * Criando uma coluna nova com a diferença entre a data recebida pelo cliente e a previsão de entrega.
# * Além da classificação desta diferença em cinco categorias

# %%
orders['Dif_Prev_Realiz_Entrega']= round((orders.order_delivered_customer_date - orders.order_estimated_delivery_date) / np.timedelta64(1,'D'),0)

resultado = []
for value in orders['Dif_Prev_Realiz_Entrega']:
    if (value < 0):
        resultado.append ("Antes")
    elif (value == 0):
        resultado.append ("Pontual")
    elif value < 30:
       resultado.append ("Após até 30 dias")
    elif value >= 31:
        resultado.append("Após acima 31 dias")
    else: 
        resultado.append("Sem entrega")
orders['Realiz_entrega']= resultado

orders.head()

# %% [markdown]
# * Fazendo o cruzamento entre os Datasets orders e orders_review

# %%
m_orders_o_reviews = pd.merge(orders, order_reviews, how= 'inner', on = 'order_id')
m_orders_o_reviews.head()

# %%
m_orders_o_reviews.groupby('review_score').Realiz_entrega.count().reset_index()

# %%
notas_entrega = m_orders_o_reviews.groupby(['review_score', 'Realiz_entrega']).Dif_Prev_Realiz_Entrega.count().reset_index()
notas_entrega

# %% [markdown]
# #### 5.	a) Quais as categorias de produtos mais vendidos? 
# ####   b) E os menos vendidos? 
# ####   c) Existe relação com os preços dos itens?     
# ####   d) A quantidade de fotos impacta nas vendas?

# %% [markdown]
# * Fazendo o cruzamento entre os Datasets de orders_items, products e order_payment, após isso a seleção apenas das colunas necessárias.

# %%
m_prod = pd.merge(orders_items, products, how= 'left', on= 'product_id')
m_prod_paym = pd.merge(m_prod, order_payment, how='inner', on= 'order_id')
m_prod_paym ['id_pedido_item'] = (m_prod_paym['order_id']).astype(str) + (m_prod_paym['order_item_id']).astype(str)
m_prod_paym = m_prod_paym.drop_duplicates('id_pedido_item')
m_prod_paym

# %% [markdown]
# * Criado novo DataFrame com as colunas necessárias para continuar as análises

# %%
categ_prod_vendas = pd.DataFrame()
categ_prod_vendas['pedidos'] = m_prod_paym['order_id']
categ_prod_vendas['pedidos_item'] = m_prod_paym['order_item_id']
categ_prod_vendas['id_pedido_item'] = m_prod_paym['id_pedido_item']
categ_prod_vendas['Total_Vendas_PAYM'] = m_prod_paym['payment_value']
categ_prod_vendas['Total_Vendas_Calcul'] = m_prod_paym['price']+ m_prod_paym['freight_value']
categ_prod_vendas['Produto'] = m_prod_paym['product_id']
categ_prod_vendas['Preço'] = m_prod_paym['price']
categ_prod_vendas['Categorias'] = m_prod_paym['product_category_name']
categ_prod_vendas['Frete'] = m_prod_paym['freight_value']
categ_prod_vendas['Qtdade_fotos'] = m_prod_paym['product_photos_qty']

categ_prod_vendas

# %%
print( m_prod_paym.payment_value.sum())
print ('Total_Vendas_PAYM: '+ categ_prod_vendas.Total_Vendas_PAYM.sum().astype(str))
print ('Total_Vendas_Calcul: ' + categ_prod_vendas.Total_Vendas_Calcul.sum().astype(str))
print ('Diferença: ' + (categ_prod_vendas.Total_Vendas_PAYM.sum() - categ_prod_vendas.Total_Vendas_Calcul.sum()).astype(str))

# %% [markdown]
# * Foi escolhido a categoria 'pc_gamer', por ter poucos pedidos, para conferência de valores e entender a dinâmica dos resultados.

# %%
categ_prod_vendas.loc[categ_prod_vendas.Categorias == 'pc_gamer']

# %%
categ_prod_vendas[categ_prod_vendas.Categorias == 'pc_gamer'].Total_Vendas_PAYM.sum()

# %%
categ_prod_vendas[categ_prod_vendas.Categorias == 'pc_gamer'].Total_Vendas_Calcul.sum()

# %%
categ_prod_vendas.loc[categ_prod_vendas.pedidos == '285c2e15bebd4ac83635ccc563dc71f4']

# %%
categ_prod_vendas_total = categ_prod_vendas.groupby(['Categorias'])['Total_Vendas_Calcul'].sum().sort_values(ascending=False).reset_index()
categ_prod_vendas_total

# %% [markdown]
# 5.	a) Quais as categorias de produtos mais vendidos? 

# %%
categ_prod_vendas_total.nlargest(5, 'Total_Vendas_Calcul')

# %% [markdown]
# 5.	b) E os menos vendidos? 

# %%
categ_prod_vendas_total.nsmallest(5, 'Total_Vendas_Calcul', keep='last')

# %%
categ_prod_vendas[categ_prod_vendas.Categorias == 'flores']

# %% [markdown]
# 5.  c) Existe relação com os preços dos itens? 

# %%
categ_prod_vendas_media = categ_prod_vendas.groupby(['Categorias']).agg({'Total_Vendas_Calcul': 'sum', 'Preço': 'mean', 'Qtdade_fotos': 'mean'}).sort_values('Total_Vendas_Calcul',ascending=False).reset_index()
categ_prod_vendas_media = round(categ_prod_vendas_media, 1)
categ_prod_vendas_media.nlargest(5, 'Total_Vendas_Calcul')



# %%
#Média de Preço dos produtos 
print('Média de Preço geral dos produtos: ')
print(round(categ_prod_vendas.Preço.mean(),2))
print('Maior média de preço: ')
print(round(categ_prod_vendas_media.Preço.max(),2))

# %%
# Categoria com o maior preço e sua média de fotos.
categ_prod_vendas_media.iloc[categ_prod_vendas_media[['Preço']].idxmax()]

# %% [markdown]
# A média de preço por categoria não ficou muito mais alta do que a média de preço dos produtos em geral. A partir da terceira até a quinta posição, das categorias mais vendidas, temos a média de preço mais baixa do que a geral. Indicando que os clientes não buscam apenas produtos de baixo valor. 

# %% [markdown]
# 5. d) A quantidade de fotos impacta nas vendas?

# %% [markdown]
# * Classificação das categorias pelo número de fotos (média)

# %%
categ_prod_vendas_media.nlargest(5, 'Qtdade_fotos')

# %% [markdown]
# A quantidade de fotos não impacta diretamente nas vendas, nesta avaliação incial, as categorias com uma média maior de quantidade de fotos não tiveram vendas tão significativas como as top 5. E por sua vez as cinco categorias com maior volume de vendas tem uma média de aproximadamente duas fotos. A foto é sim essencial para o cliente conhecer o produto, mas na minha opinião a quantidade de fotos não resulta em um aumento direto nas vendas. O que não significa que o produto sem foto vende também, normalmente os clientes rejeitam os produtos sem foto nenhuma, por esse motivo a plataforma exige uma foto do produto.

# %% [markdown]
#     * Todos os produtos vendidos possuíam ao menos uma foto.

# %%
categ_prod_vendas[categ_prod_vendas.Qtdade_fotos == 0]

# %% [markdown]
# #### 6.	O volume e o peso dos produtos impactam no valor do frete?

# %% [markdown]
# * Criação das colunas 'Volume_Prod_m3', 'Peso_Prod_kg', 'Peso_Cubado_kg' para a análise

# %%
categ_prod_vendas ['Volume_Prod_m3'] = (m_prod_paym['product_length_cm'] * m_prod_paym['product_height_cm'] * m_prod_paym['product_width_cm']) * 0.000001
categ_prod_vendas ['Peso_Prod_kg'] = m_prod_paym['product_weight_g']/1000
categ_prod_vendas ['Peso_Cubado_kg'] = categ_prod_vendas ['Volume_Prod_m3']*300
categ_prod_vendas

# %% [markdown]
# * Calculando os valores médios do Frete, Volume_Prod_m3 e Peso_Prod_kg para compara com o total de vendas das 5 categorias mais vendidas.

# %%
categ_prod_frete = categ_prod_vendas.groupby('Categorias').agg({'Total_Vendas_Calcul': 'sum', 'Preço' : 'mean','Frete': 'mean',  'Peso_Prod_kg': 'mean', 'Peso_Cubado_kg': 'mean', 'Volume_Prod_m3': 'mean'}).sort_values('Total_Vendas_Calcul',ascending=False).reset_index()
categ_prod_frete = round(categ_prod_frete, 2)
categ_prod_frete ['%_Frete_sobre_Preço'] = round(((categ_prod_frete['Frete']/ categ_prod_frete['Preço'])*100),2)
categ_prod_frete

# %% [markdown]
# - As empresas de transporte calculam o frete verificando o peso e o volume do produto com a embalagem, ou pelo peso cubado. 
# Porque alguns produtos podem ser pequenos nas dimensões, mas pesados ou podem ser grandes, com volume maior, mas leves. Nestes casos é usado o peso cubado.
# Basicamente é comparado o peso com o peso cubado, e prevalece o maior para o cálculo do frete.
# Analisando as médias dos volumes e pesos por cada categoria, vemos que os volumes são baixos, assim como os pesos. 
# Entretanto os pesos cubados já se alteram um pouco mais, mas mantêm a faixa de preço de frete médio. 
# Lembrando que aqui se tratam de valores médios e poderia ser feita uma análise mais aprofundada dentro de cada categoria.
# Podemos analisar também o impacto do frete sobre o preço do produto. 
# 

# %% [markdown]
# #### 7.	Avaliação/Visualização da posição geográfica onde se encontra a maior concentração de clientes e vendedores.

# %% [markdown]
# ##### Preparação

# %% [markdown]
# * Fazendo o cruzamento dos datasets necessários para responder esta demanda.

# %%
orders_resumo = pd.DataFrame()
orders_resumo = orders[['order_id', 'customer_id', 'tempo_entrega', 'Realiz_entrega']]
orders_resumo

# %%
m_orders_cus = pd.merge(orders_resumo, customers, how= 'inner', on= 'customer_id')
m_orders_cus

# %%
m_orders_cus['customer_id'].nunique()

# %%
orders_items_resumo = pd.DataFrame()
orders_items_resumo = orders_items[['order_id', 'seller_id']]
orders_items_resumo

# %%
m_ord_cus_o_item = pd.merge(m_orders_cus, orders_items_resumo, how= 'left', on= 'order_id')
m_ord_cus_o_item

# %%
m_ord_cus_o_item['seller_id'].nunique()

# %%
m_ord_cus_o_item['customer_id'].nunique()

# %%
m_ord_cus_o_it_sell = pd.merge(m_ord_cus_o_item, sellers, how= 'left', on= 'seller_id' )
m_ord_cus_o_it_sell

# %%
m_ord_cus_o_it_sell['seller_id'].nunique()

# %%
m_ord_cus_o_it_sell['customer_id'].nunique()

# %%
cust_sell = m_ord_cus_o_it_sell.groupby('customer_state').agg({'seller_id': pd.Series.nunique, 'customer_id' : pd.Series.nunique}).reset_index()
cust_sell

# %%
cust_sell.sum()

# %%
sell = m_ord_cus_o_it_sell.groupby('seller_state')['seller_id'].nunique().reset_index()
sell

# %%
sell.sum()

# %%
cus = m_ord_cus_o_it_sell.groupby('customer_state')['customer_id'].nunique().reset_index()
cus

# %%
cus.sum()

# %% [markdown]
# 7.	Avaliação/Visualização da posição geográfica onde se encontra a maior concentração de clientes e vendedores.

# %%
m_cust_sell = pd.merge(cus, sell, how= 'left', left_on='customer_state', right_on='seller_state')
m_cust_sell = m_cust_sell.drop(columns=['seller_state'])
m_cust_sell = m_cust_sell.sort_values(by='customer_id', ascending= False )
m_cust_sell

# %%
m_cust_sell.sum()

# %%
tab_estados = pd.read_csv('D:\Harve Residencia Tech\Projetos\Projeto Olist\Projeto Olist Script\Tabelas\Tabela_estados.csv', sep= ';')
tab_estados

# %%
m_est_cus_sell = pd.merge(m_cust_sell, tab_estados, how= 'inner', left_on='customer_state', right_on= 'Sigla' )
m_est_cus_sell

# %%
file_name = 'D:\Harve Residencia Tech\Projetos\Projeto Olist\Projeto Olist Script\Tabelas\Customer_Seller_estados.csv'
m_est_cus_sell.to_csv(file_name)
print('ok')

# %% [markdown]
# #### 8.	As entregas atrasadas aconteceram entre vendedores/compradores de estados diferentes?

# %%
m_ord_cus_o_it_sell

# %%
entregas_cus_sell = pd.DataFrame()
entregas_cus_sell = m_ord_cus_o_it_sell [['order_id', 'customer_id', 'customer_state', 'seller_id', 'seller_state' ,'tempo_entrega', 'Realiz_entrega']]
entregas_cus_sell.head()

# %%
mesmo_estado = []
for i, valor in enumerate(entregas_cus_sell['customer_state']):
    if( valor == entregas_cus_sell['seller_state'][i]):
        mesmo_estado.append(0)
    else:
        mesmo_estado.append(1)
entregas_cus_sell['Entregas_mesmo_estado'] = mesmo_estado
entregas_cus_sell

# %%


# %% [markdown]
# 9.	Identificar o padrão dos clientes (localização, método de pagamento, quantidade de parcelas, entrega antes da previsão, notas de satisfação média, tipos de produtos) que fizeram uma recompra no site

# %%



