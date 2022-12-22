![Banner](3.png)

## Food delivery: a dashboard to evaluate the Company Growth

### 1. Project overview
 
*What is the goal?* 
Provide real time analysis of food delivery data and KPIs of company growth. The developed Dashboard allows to evaluate growth metrics related to the **delivery people**, **restaurants**, and **delivery app**.
 
*Tools and skills:* 
 - ETL: extracting, transforming and loading data
 - Data visualization (plotly express, folium, matplotlib)
 - Deploy (streamlit)

*Why is this subjetc important?* 

  1. Delivery platforms connect Restaurants, Delivery persons, and Clients. They make money through various revenue streams, according to [Ahuja et al., 2021](https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/ordering-in-the-rapid-evolution-of-food-delivery):
  - Restaurant commission fees
  - Customer delivery fees
  - In-app advertising

2. Therefore, stakeholders need to know a few key aspects related to:

**Delivery people**

- Who are the best delivery people (fastest and with highest score)?
    - The manager can offer rewards for faster deliveries

**Restaurants**

- What is the average distance between the restaurant and the delivery location?
    - The restaurant may limit the type of order to closer locations (to avoid food arriving cold and a consequent a bad review, for example)

**Delivery app**

- Is the volume of orders higher during heavy traffic conditions?
    - The team may offer lower prices during the conditions of lowest orders
    
  
### 2. Solution strategy 

- Import data: [Food Delivery Dataset in India](https://www.kaggle.com/datasets/gauravmalik26/food-delivery-dataset).
- Data wrangling to assure quality and useful data:
    - Dealing with missing values
    - Converting datatypes (string, dates, and numerical)
    - Cleaning empty spaces and other unwanted caracteres from numerical values
- Data exploration and visualization to analyze business hypothesis. 
- Dashboard for real-time analysis.

### 3. Highlights of the results

- Overall, daily orders have a consistent temporal behavior.
- The larger part of orders happen during low traffic density, with the opposite during high traffic conditions.
- Most orders are in Metropolitan and Urban cities with traffic density under low and jam conditions.
- Delivery ratings are similar for traffic and weather conditions.
- Deliveries during Festivals take longer.
- Deliveries in semi-urban cities take longer. 
- The time taken to delivery in urban and metropolitan cities are similar.
- Suggestions for the team:
    - Sales: investigate the gap during February.
    - Marketing: prepare promotions during high traffic conditions to increase sales (but  extend the delivery time prediction, to avoid bad reviews).

### 3. Further steps
- Evaluate correlations to understand how the components are related.
    - for example:
        - Does rainy conditions affect orders?
        - Investigate the factors most correlated to orders volume and ratings, aiming to increase both.
        - Investigate the factors that affect the time taken for deliveries, aiming to decrease it.
- Develop machine learning models to predict the expected daily or weekly orders.


***Take a look at the responsive, interactive and multi-purpose app:***

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mfdanieli-curry-company-home-70myun.streamlit.app/)
