# -----------------------------------
# DASH VISAO ENTREGADORES
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

st.set_page_config(page_title='Delivery Vision',page_icon='🛵', layout='wide')

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
    
    # Arrumando a coluna Weatherconditions
    df['Weatherconditions'] = df['Weatherconditions'].apply(lambda x:x.split('conditions ')[1])
    

    
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
st.header('Delivery Vision')

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

# with st.container():
#     st.title('Overall metrics')

#     col1,col2 = st.columns(2, gap='large')

#     with col1:
#         # st.subheader('Entregador mais velho')
#         maior_idade = df1.loc[:,'Delivery_person_Age'].max()
#         col1.metric('Age of oldest delivery person: ', maior_idade)

#     with col2:
#         # st.subheader('Entregador mais jovem')
#         menor_idade = df1.loc[:,'Delivery_person_Age'].min()
#         col2.metric('Age of youngest delivery person: ', menor_idade)

    # with col3:
    #     # st.subheader('Melhor condição de veículo')
    #     melhor_cond = df1.loc[:,'Vehicle_condition'].max()
    #     col3.metric('Best vehicle condition: ', melhor_cond)
    # with col4:
    #     # st.subheader('Pior condição de veículo')
    #     pior_cond = df1.loc[:,'Vehicle_condition'].min()
    #     col4.metric('Wost vehicle condition: ',pior_cond)

with st.container():  # como se fosse a segunda linha         
    st.markdown("""---""")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader('Mean ratings by traffic')

        avr_ratings_traffic = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').mean().reset_index()
        # st.dataframe(avr_ratings_traffic)
        fig = go.Figure(data=[go.Pie(labels=avr_ratings_traffic['Road_traffic_density'],
                             values=avr_ratings_traffic['Delivery_person_Ratings'])])
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        
    
        st.subheader('Mean ratings by weather conditions')
        avr_ratings_clima = df1.loc[:,['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').mean().reset_index()

        # st.dataframe(avr_ratings_clima)
        fig = go.Figure(data=[go.Pie(labels=avr_ratings_clima['Weatherconditions'],
                             values=avr_ratings_clima['Delivery_person_Ratings'])])
        st.plotly_chart(fig,use_container_width=True)
        
with st.container():
    st.subheader('Mean rating by delivery person')
    avr_ratings = df1.loc[:,['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
    st.dataframe(avr_ratings)

        
with st.container():           
    st.markdown("""---""")    
    st.markdown('### Time taken to deliver')
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Fastest delivery persons')

        df_aux = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City','Time_taken(min)']).reset_index()

        df_aux1 = df_aux.loc[df_aux['City']=='Urban ',:].head(10)
        df_aux2 = df_aux.loc[df_aux['City']=='Semi-Urban ',:].head(10)
        df_aux3 = df_aux.loc[df_aux['City']=='Metropolitian ',:].head(10)
        df_aux = pd.concat([df_aux1,df_aux2,df_aux3]).reset_index()
        st.dataframe(df_aux.loc[:,['Delivery_person_ID','City','Time_taken(min)']])


    with col2:
        st.subheader('Slowest delivery persons')  

        df_aux = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City','Time_taken(min)'],ascending=False).reset_index()

        df_aux1 = df_aux.loc[df_aux['City']=='Urban ',:].head(10)
        df_aux2 = df_aux.loc[df_aux['City']=='Semi-Urban ',:].head(10)
        df_aux3 = df_aux.loc[df_aux['City']=='Metropolitian ',:].head(10)
        df_aux = pd.concat([df_aux1,df_aux2,df_aux3]).reset_index()        
        st.dataframe(df_aux.loc[:,['Delivery_person_ID','City','Time_taken(min)']])
                
st.markdown(
    """
> #### *Insights:*
> - Delivery ratings are similar for traffic and weather conditions.   
> #### *Suggestions for the team:*
> - Investigate the factors most correlated to orders volume and ratings, aiming to increase both.
> - Investigate the factors that affect the time taken for deliveries, aiming to decrease it.
""")

