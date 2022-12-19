import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon="🎲",
    layout = 'wide',
)


# image_path = '/Users/daniferreira/Library/CloudStorage/OneDrive-ufpr.br/DS/CDS/1_Fast_track_course/Colab_Notebooks/'
# image = Image.open(image_path + 'food-delivery-2.png')
image = Image.open('food-delivery-2.png')

st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Cury Company Dashboard')

st.markdown(
    """
Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
### Como utilizar esse Growth Dashboard?
- Visão Empresa:
- Visão Gerencial: Métricas gerais de comportamento.
- Visão Tática: Indicadores senanais de crescimento.
- Visão Geográfica: Insights de geolocalização.
- Visão Entregador:
- Acompanhamento dos indicadores semanais de crescimento
- Visão Restaurante:
- Indicadores senanais de crescimento dos restaurantes
## Ask for Help
Time de Data Science no Discord
    -danieli
""")