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

      
# ******************
# Barra lateral
# ******************       
st.header('Visão Restaurantes')

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
tab1, tab2, tab3 = st.tabs(['Visão Gerencial','_','_'])

with tab1:
    with st.container():
            st.title('Overall metrics')

            col1,col2,col3 = st.columns(3)

            with col1:
        
                deliv_unique = len(df1.loc[:,'Delivery_person_ID'].unique())
                col1.metric('Número de entregadores',deliv_unique)
            with col2:

                col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

                df1['Distance'] = df1.loc[:,col].apply(lambda x: haversine(
                    (x['Restaurant_latitude'], x['Restaurant_longitude']),
                    (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)

                avg_distance = np.round(df1['Distance'].mean(),decimals=2)
                col2.metric('Distância média entre restaurante e entrega',avg_distance)
                
            with col3:               
            
                df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
                df_aux.columns = ['avg_time', 'std_time' ]
                df_aux = df_aux.reset_index()
                df_aux = np.round(df_aux.loc[df_aux['Festival']=='Yes','avg_time'],2)
                col3.metric(' Tempo de entrega médio em Festivais',df_aux)

    with st.container()   :         
            col1,col2,col3 = st.columns(3)
    
            with col1:
                
                df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
                df_aux.columns = ['avg_time', 'std_time' ]
                df_aux = df_aux.reset_index()
                df_aux = np.round(df_aux.loc[df_aux['Festival']=='Yes','std_time'],2)
                col1.metric(' STD c/ Festivais',df_aux)
                
            with col2:
                
                df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
                df_aux.columns = ['avg_time', 'std_time' ]
                df_aux = df_aux.reset_index()
                df_aux = np.round(df_aux.loc[df_aux['Festival']=='No','avg_time'],2)
                col2.metric(' Tempo de entrega médio em não Festivais',df_aux)
                          
                
            with col3:
                df_aux = df1.loc[:, ['City', 'Festival','Time_taken(min)' ] ].groupby( 'Festival' ).agg( {'Time_taken(min)': ['mean','std']})
                df_aux.columns = ['avg_time', 'std_time' ]
                df_aux = df_aux.reset_index()
                df_aux = np.round(df_aux.loc[df_aux['Festival']=='No','std_time'],2)
                col3.metric(' STD s/ Festivais',df_aux)
                          

    with st.container():
        
        st.title('titulo')
        col1,col2 = st.columns(2)
        
        with col1:
            df_aux = df1.loc[:, ['City', 'Time_taken(min)' ] ].groupby( 'City' ).agg( {'Time_taken(min)': ['mean','std']})
            df_aux.columns = ['avg_time', 'std_time' ]
            df_aux = df_aux.reset_index()

            # fazendo grafico novo - meiga nao explicou!!!
            fig = go.Figure()
            fig.add_trace(go.Bar(name ='Control',x=df_aux['City'],y=df_aux['avg_time'],error_y = dict( type='data', array=df_aux['std_time'])))
            fig.update_layout(barmode= 'group')
            st.plotly_chart(fig, use_container_width=True) 
        
        with col2:
            df_aux=df1.loc[:,['City','Time_taken(min)','Type_of_order']].groupby(['City','Type_of_order']).agg({'Time_taken(min)':['mean', 'std']})
            st.dataframe(df_aux)

        
    with st.container():
            st.title('titulo')
            col1,col2 = st.columns(2)

            with col1:
                # st.markdown('##### ...')

                # fazendo grafico novo - meiga nao explicou!!!
                # dentro dos 27.35 km, pega % em cada tipo de cidade

                col = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']

                df1['Distance'] = df1.loc[:,col].apply(lambda x: haversine(
                (x['Restaurant_latitude'], x['Restaurant_longitude']),
                (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis=1)

                avg_distance = df1.loc[:,['City','Distance']].groupby('City').mean().reset_index()

                fig = go.Figure(data =[ go.Pie (labels=avg_distance['City'],values=avg_distance['Distance'],pull=[0,0.05,0])])
                # pull é pra puxar aquela parte da fixa q fica meio separada
                st.plotly_chart(fig, use_container_width=True)


            with col2:
                # st.markdown('##### ...')

                cols =['City', 'Time_taken(min)' , 'Road_traffic_density'] 
                df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density']).agg( {'Time_taken(min)': ['mean','std']})
                df_aux.columns = ['avg_time', 'std_time' ]
                df_aux = df_aux.reset_index()

                # fazendo grafico novo - meiga nao explicou!!!
                # graf sunburts -> legal p/ variaveis categoricas de mais de 1 dimensao > achei bem confuso
                fig = px.sunburst(df_aux,path=['City','Road_traffic_density'],values='avg_time',color='std_time',color_continuous_scale='RdBu',color_continuous_midpoint=np.average(df_aux['std_time']))
                st.plotly_chart(fig, use_container_width=True)   
            
            













