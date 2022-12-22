import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon="📈",
    layout = 'wide',
)


# image_path = '/Users/daniferreira/Library/CloudStorage/OneDrive-ufpr.br/DS/CDS/1_Fast_track_course/Colab_Notebooks/'
# image = Image.open(image_path + 'food-delivery-2.png')
image = Image.open('food-delivery-2.png')

st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Delivery APP Dashboard')

st.markdown(
    """
The Growth Dashboard was designed to follow the growth metrics related to the **Restaurants**, to the **Delivery people**, and to the **Delivery app**. 
### How to use the Growth Dashboard?
- Company Vision: Indexes of interest of company growth.
    * Management vision: Absolute numbers of orders by traffict and city.
    * Strategic vision: Weekly orders for tatic purposes.  
    * Geographical vision: Orders by location.
- Restaurants Vision: Insights associated with each restaraunt.
- Delivery Vision: Metrics to analyse the deliveries.

#### Ask for Help
    danieli@email.com
""")

