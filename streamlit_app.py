# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session COMMENTED TO PASS FROM SIS TO SNIS
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')
#st.write('The name on your Smoothie will be: ', name_on_order)

st.write(
    """Choose the fruits you want in your cutom Smoothie!"""
)

#option = st.selectbox('How would you like to be contacted?', 
#                      ('Banana', 'Strawberries', 'Peaches'))
#st.write('You selected:', option)

cnx = st.connection("snowflakes") 
session = cnx.session()
#session = get_active_session() COMMENTED TO PASS FROM SIS TO SNIS
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

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
    
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert = st.button('Submit Order')
    
    #st.write(my_insert_stmt)
    #st.stop()
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")