# -----------------------------------
# DASH VISAO RESTAURANTES
# -----------------------------------

# ******************
# Importando bibliotecas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
import folium
import streamlit as st
import folium      
from haversine import haversine
from PIL import Image
from streamlit_folium import folium_static

st.set_page_config(page_title='Restaurants Vision',page_icon='🍕', layout='wide')

# ******************
# LIMPEZA DOS DADOS
# ******************

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
     
# ******************
# Barra lateral Streamlit
# ******************       
st.header('Restaurants Vision')

image = Image.open('food-delivery-2.png')

st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Select a date interval')

date_slider = st.sidebar.slider(
    'Until when?',
    value = pd.datetime(2022,4,13),
    min_value = pd.datetime(2022,2,11),
    max_value = pd.datetime(2022,4,6),
    format = 'DD-MM-YYYY')

# st.header(date_slider)

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Select Traffic Conditions',
    ['Low','Medium','High','Jam'],
    default = ['Low','Medium','High','Jam'])
    
st.sidebar.markdown("""---""")

st.sidebar.markdown('### Powered by @mfdanieli')

#### usando o filtro de data que o usuario definiu
linhas_selecionadas = df1['Order_Date']<date_slider
df1 = df1.loc[linhas_selecionadas,:]

#### usando o filtro de tráfego que o usuario definiu
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

# ****************** ****************** ******************
# Layout do streamlit + métricas de negócio
# ****************** ****************** ******************  

with st.container():
    st.markdown("""---""")
    st.markdown('### Overall metrics')

    col1,col2,col3,col4 = st.columns(4,gap='medium')

    with col1:

        deliv_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
        col1.metric('Number of delivery persons',deliv_unique)
    
    with col2:

        col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

        df1['Distance'] = df1.loc[:,col].apply(lambda x: haversine(
            (x['Restaurant_latitude'], x['Restaurant_longitude']),
            (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)

        avg_distance = np.round(df1['Distance'].mean(),decimals=2)
        col2.metric('Distance to delivery location',avg_distance, delta= 'average km', delta_color="off")

    with col3:               
        df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time', 'std_time' ]
        df_aux = df_aux.reset_index()
        df_aux = np.round(df_aux.loc[df_aux['Festival']=='Yes','avg_time'],2)
        col3.metric('Time to deliver during Festivais',df_aux, delta='average min', delta_color="off")

    with col4:
        df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time', 'std_time' ]
        df_aux = df_aux.reset_index()
        df_aux = np.round(df_aux.loc[df_aux['Festival']=='No','avg_time'],2)
        col4.metric('Time to deliver in regular day',df_aux, delta='average min', delta_color="off")
        

with st.container():

    # col1,col2 = st.columns(2)

    # with col1:
        st.markdown('### Time to deliver by city')
        df_aux = df1.loc[:, ['City', 'Time_taken(min)' ] ].groupby( 'City' ).agg( {'Time_taken(min)': ['mean','std']})
        df_aux.columns = ['avg_time', 'std_time' ]
        df_aux = df_aux.reset_index()

        # graf barras 
        fig = go.Figure()
        fig.add_trace(go.Bar(name ='Control',x=df_aux['City'],y=df_aux['avg_time'],error_y = dict( type='data', array=df_aux['std_time'])))
        fig.update_layout(barmode= 'group')
        st.plotly_chart(fig, use_container_width=True) 
        st.markdown('*P. S. Blue bar is the average, and the black line represents the standard deviation*')

            
#     # aqui agrupei tempo de entrega por tipo de ordem, mas nao deu nada interessante
#     with col2:
#         df_aux=df1.loc[:,['City','Time_taken(min)','Type_of_order']].groupby('Type_of_order').agg({'Time_taken(min)':['mean', 'std']})
#         df_aux.columns = ['avg_time', 'std_time' ]
#         df_aux = df_aux.reset_index()
        
#         # graf barras 
#         fig = go.Figure()
#         fig.add_trace(go.Bar(name ='Control',x=df_aux['Type_of_order'],y=df_aux['avg_time'],error_y = dict( type='data', array=df_aux['std_time'])))
#         fig.update_layout(barmode= 'group')
#         st.plotly_chart(fig, use_container_width=True) 
        

# with st.container():
        
#         col1,col2 = st.columns(2)

#         with col1:
#             st.markdown('### Average delivery distance by city')

#             # fazendo grafico novo 
#             # dentro dos 27.35 km, pega % em cada tipo de cidade

#             col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

#             df1['Distance'] = df1.loc[:,col].apply(lambda x: haversine(
#             (x['Restaurant_latitude'], x['Restaurant_longitude']),
#             (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)

#             avg_distance = df1.loc[:,['City','Distance']].groupby('City').mean().reset_index()
            
#             fig = go.Figure(data =[ go.Pie (labels=avg_distance['City'],values=avg_distance['Distance'],pull=[0,0.05,0])])
#             # pull é pra puxar aquela parte da fixa q fica meio separada
#             st.plotly_chart(fig, use_container_width=True)


#         with col2:
#             st.markdown('##### ...')

#             cols =['City', 'Time_taken(min)' , 'Road_traffic_density'] 
#             df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density']).agg( {'Time_taken(min)': ['mean','std']})
#             df_aux.columns = ['avg_time', 'std_time' ]
#             df_aux = df_aux.reset_index()

#             # graf sunburts -> legal p/ variaveis categoricas de mais de 1 dimensao 
#             fig = px.sunburst(df_aux,path=['City','Road_traffic_density'],values='avg_time',color='std_time',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(df_aux['std_time']))
#             st.plotly_chart(fig, use_container_width=True)   
            
with st.container():
        st.markdown(
    """
> ### *Insights:*
> - Deliveries during Festivals take longer.
> - Deliveries in semi-urban cities take longer.
> - The time taken to delivery in urban and metropolitan cities are similar.
""")            













