# -----------------------------------
# DASH VISAO ENTREGADORES
# -----------------------------------

# ******************
# Importando bibliotecas
import pandas as pd
import plotly.express as px
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
# FASE 1: PERGUNTAS VISÃO ENTREGADORES:
       
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
st.header('Visão Entregadores')

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
        
        col1,col2,col3,col4 = st.columns(4, gap='large')
        
        with col1:
            # st.subheader('Entregador mais velho')
            maior_idade = df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior idade = ', maior_idade)
            
        with col2:
            # st.subheader('Entregador mais jovem')
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor idade = ', menor_idade)
            
        with col3:
            # st.subheader('Melhor condição de veículo')
            melhor_cond = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor cond = ', melhor_cond)
        with col4:
            # st.subheader('Pior condição de veículo')
            pior_cond = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior condição = ',pior_cond)

    with st.container():  # como se fosse a segunda linha         
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1,col2 = st.columns(2)
        
        with col1:
            st.subheader('Avaliação média por entregador')
            avr_ratings = df1.loc[:,['Delivery_person_ID', 'Delivery_person_Ratings']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(avr_ratings)
            
        with col2:
            st.subheader('Avaliação média por traffic')
            
            avr_ratings_traffic = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').mean().reset_index()
            st.dataframe(avr_ratings_traffic)
            
            st.subheader('Avaliação média por clima')
            avr_ratings_clima = df1.loc[:,['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').mean().reset_index()

            st.dataframe(avr_ratings_clima)
            
    with st.container():           
        st.markdown("""---""")    
        st.title('Velocidade de entrega')
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Top entregadores mais rápidos')
            
            df_aux = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City','Time_taken(min)']).reset_index()

            df_aux1 = df_aux.loc[df_aux['City']=='Urban ',:].head(10)
            df_aux2 = df_aux.loc[df_aux['City']=='Semi-Urban ',:].head(10)
            df_aux3 = df_aux.loc[df_aux['City']=='Metropolitian ',:].head(10)
            df_aux = pd.concat([df_aux1,df_aux2,df_aux3]).reset_index()
            st.dataframe(df_aux)
            
            
        with col2:
            st.subheader('Top entregadores mais lentos')  
        
            df_aux = df1.loc[:,['Delivery_person_ID','City','Time_taken(min)']].groupby(['City','Delivery_person_ID']).min().sort_values(['City','Time_taken(min)'],ascending=False).reset_index()

            df_aux1 = df_aux.loc[df_aux['City']=='Urban ',:].head(10)
            df_aux2 = df_aux.loc[df_aux['City']=='Semi-Urban ',:].head(10)
            df_aux3 = df_aux.loc[df_aux['City']=='Metropolitian ',:].head(10)
            df_aux = pd.concat([df_aux1,df_aux2,df_aux3]).reset_index()        
            st.dataframe(df_aux)
        
        
