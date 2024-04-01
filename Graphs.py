# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

conn = st.experimental_connection("snowpark")
#my_dataframe = conn.session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#convert the snowpark df to a Pandas df so we can use LOC function
#pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)

#ingredients_list = st.multiselect(
#    'Choose up to 5 ingredients:'
#    ,my_dataframe
#    ,max_selections = 6
#)

#if the list is not empty do....
#if ingredients_list: 
    
#    ingredients_string = ''
    
#    for fruit_chosen in ingredients_list:
#        ingredients_string += fruit_chosen + ' '
#        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#        st.subheader(search_on + ' Nutrition Information')
#        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
#        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=False)

#    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

#    time_to_insert = st.button('Submit Order')
    
#    if time_to_insert:
#        conn.session.sql(my_insert_stmt).collect()
#        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
#        name_on_order = ''

hifives_val = st.slider(
    "Number of high-fives in Q3",
    min_value=0,
    max_value=90,
    value=60,
    help="Use this to enter the number of high-fives you gave in Q3",
)

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = conn.session.create_dataframe(
    [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
    schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Number of high-fives")
st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

st.subheader("Underlying data")
st.dataframe(queried_data, use_container_width=True)

