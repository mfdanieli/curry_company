# Importando bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import folium
import streamlit as st
import folium    

from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Visão Empresa',page_icon='📈', layout='wide')

# LIMPEZA

def clean_code(df):
    """" Funcao para limpeza de dados
         Tipos de limpeza:
         1. Remocao Nan
         2. Mudanca tipo dados
         3. Remocao de espaços de variavies de texto
         4. Formatação da coluna de datas
         5.Limpeza da coluna de tempo (remoção do texto misturado com variável numérica)
         
         Input: dataframe
         Output: dataframe
    
    """
    # Pegando somente dados diferentes de NaN
    df = df.loc[(df['Delivery_person_Age'] != 'NaN '),:]
    df = df.loc[(df['Road_traffic_density'] != 'NaN '),:]
    df = df.loc[(df['City'] != 'NaN '),:]
    df = df.loc[(df['Festival'] != 'NaN '),:]
    df = df.loc[(df['multiple_deliveries'] != 'NaN '),:]

    # Removendo espaco em branco de strings
    df.loc[:, 'ID'] = df.loc[:, 'ID'].str.strip()
    df.loc[:, 'Delivery_person_ID'] = df.loc[:,'Delivery_person_ID'].str.strip()
    df.loc[:, 'Festival'] = df.loc[:,'Festival'].str.strip()
    df.loc[:,'Road_traffic_density'] = df.loc[:,'Road_traffic_density'].str.strip()
    df.loc[:,'Type_of_order'] = df.loc[:,'Type_of_order'].str.strip()
    df.loc[:,'Type_of_vehicle'] = df.loc[:,'Type_of_vehicle'].str.strip()

    # Convertendo de texto/categoria/string para numeros inteiros
    df['Delivery_person_Age'] = df['Delivery_person_Age'].astype( int )
    df['multiple_deliveries'] = df['multiple_deliveries'].astype( int )

    # onvertendo de texto/categoria/strings para numeros decimais
    df['Delivery_person_Ratings'] = df['Delivery_person_Ratings'].astype( float )

    # Convertendo de texto para data
    df['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

    # Arrumando a coluna time_taken(min) 
    df['Time_taken(min)'] = df['Time_taken(min)'].apply(lambda x:x.split('(min)')[1])
    df['Time_taken(min)'] = pd.to_numeric(df['Time_taken(min)'])

    
    return df

# ---------------------- Inicio da logica do código

# ----------------------
# EXTRAÇÃO: Leitura dados brutos
# ----------------------

df_raw = pd.read_csv('train.csv')
df = df_raw.copy()  # Fazendo uma cópia do DataFrame Lido raw

# ----------------------
# TRANFORMAÇÃO
# ----------------------

df = clean_code(df)

# ----------------------
# CARGA
# ----------------------

df1 = df.copy()  # Fazendo uma cópia do DataFrame limpo

# ----------------------
# FASE 1: PERGUNTAS VISÃO EMPRESA:
       
# 1. Quantidade de pedidos por dia.
 
df_aux = df1.groupby('Order_Date').count().reset_index() 
px.bar(df_aux, x = 'Order_Date',y = 'ID')
      
       
# 2. Quantidade de pedidos por semana.
df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U')  # determina semana do ano correspondente
df_aux = df1.groupby('week_of_year').count().reset_index()
px.line(df_aux,x='week_of_year',y='ID')
              
# 3. Distribuição dos pedidos por tipo de tráfego.
       
df_aux = df1.groupby('Road_traffic_density').count().reset_index()
df_aux['entrega_perc'] = df_aux['ID']/df_aux['ID'].sum()  # calcula %
px.pie(df_aux,values='entrega_perc',names='Road_traffic_density')       
            
       
# 4. Comparação do volume de pedidos por cidade e tipo de tráfego.
       
# 5. A localização central de cada cidade por tipo de tráfego.

       
# ******************
# Barra lateral
# ******************       
st.header('Visão Empresa')

image = Image.open('food-delivery-2.png')

st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime(2022,4,13),
    min_value = pd.datetime(2022,2,11),
    max_value = pd.datetime(2022,4,6),
    format = 'DD-MM-YYYY')

# st.header(date_slider)

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High','Jam'])
    
st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by Dani')


#### usando o filtro de data que o usuario definiu
linhas_selecionadas = df1['Order_Date']<date_slider
df1 = df1.loc[linhas_selecionadas,:]

#### usando o filtro de tráfego que o usuario definiu
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

# ******************
# Layout do streamlit
# ******************    

# ciar abas
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','Visão Tática','Visão Geográfica'])

# with uso p/ selecionar o que quero dentro de cada aba 
with tab1: 
    with st.container(): # coloca tudo num primeiro blocao
            
        # colocando em funcao 
        def order_metric(df1):
            # Order metric
            # 1. Quantidade de pedidos por dia.
            df_aux = df1.groupby('Order_Date').count().reset_index() 
            fig = px.bar(df_aux, x = 'Order_Date',y = 'ID')
            return fig
        
        st.header('Daily orders')
        fig = order_metric(df1)
        st.plotly_chart(fig,use_container_width=True)
    
    with st.container():
        # criando colunas em um segundo blocao
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('# Orders by traffic')
            df_aux = df1.groupby('Road_traffic_density').count().reset_index()    
            # p/ pegar as %
            df_aux['entrega_perc'] = df_aux['ID']/df_aux['ID'].sum()
            fig = px.pie(df_aux,values='entrega_perc',names='Road_traffic_density')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown('# Orders by city and by traffic')
            df_aux = df1.loc[:,['ID', 'City', 'Road_traffic_density']].groupby(['City','Road_traffic_density']).count().reset_index()
            fig = px.scatter(df_aux,x='City', y='Road_traffic_density',size = 'ID', color = 'City')
            st.plotly_chart(fig,use_container_width=True)

    
with tab2:
    with st.container():
        col1,col2 = st.columns(2)
        with col1:       
            st.markdown('# Weekly orders')
            df1['week_of_year'] = df1['Order_Date'].dt.strftime('%U') # strftime: string format time
            df_aux = df1.groupby('week_of_year').count().reset_index()
            fig=px.line(df_aux,x='week_of_year',y='ID')
            st.plotly_chart(fig,use_container_width=True)
        with col2: 
            st.markdown('# Weekly orders by entregador ')
            df_aux1 = df1[['ID','week_of_year']].groupby(['week_of_year']).count().reset_index()
            # dataframe qtiadde entregue por entregador na semana
            df_aux2 = df1.loc[:,['week_of_year','Delivery_person_ID']].groupby('week_of_year').nunique().reset_index()
            # juntando 1 e 2
            df_aux = pd.merge(df_aux1,df_aux2,how='inner')
            # % de vendas por semana por entregador 
            df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID'] 
            fig = px.line(df_aux, x ='week_of_year' , y='order_by_delivery')
            st.plotly_chart(fig,use_container_width=True)
            # ex: o que observo -> na semana 6, todo entregador q trabalhou fez 3 entregas




with tab3:
    st.markdown('# Central city location by traffic') # !!!
    df_aux = df1.loc[:,['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
      folium.Marker([location_info['Delivery_location_latitude'],
                 location_info['Delivery_location_longitude']]).add_to(map)
    folium_static(map,width=1024,height=600)


