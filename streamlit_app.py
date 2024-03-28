# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')
st.write(
    """Choose the fruits you want in your cutom Smoothie!"""
)

#conn = st.experimental_connection()
conn = st.experimental_connection("snowpark") # Config section defined in [connections.sql] in secrets.toml.
#session = conn.session()
my_dataframe = conn.session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).select(col('SEARCH_ON'))
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)

#if the list is not empty do....
if ingredients_list: 
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=False)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    
    #st.write(my_insert_stmt)
    #st.stop()
    if time_to_insert:
        conn.session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
