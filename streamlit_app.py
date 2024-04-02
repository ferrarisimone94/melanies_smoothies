# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col
import random

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')

conn = st.experimental_connection("snowpark")
my_dataframe = conn.session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#convert the snowpark df to a Pandas df so we can use LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients to put in your custom Smoothie!'
    ,my_dataframe
    ,max_selections = 6
)

st.subheader("Cannot decide? Look at what our customer love in the page on the left!")

#if the list is not empty do....
if ingredients_list: 
 
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ', '
        #st.sidebar.subheader(ingredients_string)
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.sidebar.subheader(search_on + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_df = st.sidebar.dataframe(data=fruityvice_response.json(), use_container_width=False)
                
    st.sidebar.write("Disclaimer: information provided by Fruityvice.com. Not all our ingredents are reported in this website.")
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #if name_on_order == '':
    #    name_on_order = "Online Order "+str(random.randint(1,1000))
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        conn.session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
        name_on_order = ''
        ingredients_list = ''
        
