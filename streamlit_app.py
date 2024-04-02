# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col
#import random

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

name_on_order = st.text_input('Name on Smoothie:')
#st.write(
#    """Here the list of the ingredients available!"""
#)

conn = st.experimental_connection("snowpark")
my_dataframe = conn.session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))

#total_ingredient = ""
#number = 0
#ingredients_ordered_df = conn.session.table("SMOOTHIES.PUBLIC.ORDERS").select(col('ingredients')).collect()
#for i in ingredients_ordered_df:
#    total_ingredient = total_ingredient + str(i)

#total_ingredient = total_ingredient.replace("Row(INGREDIENTS=","(")
#total_ingredient = total_ingredient.replace(", ","'),('")
#total_ingredient = total_ingredient.replace("('')","")

#def Convert(string): 
#    li = list(string.split(", ")) 
#    return li

#if total_ingredient[len(total_ingredient)-1] == ',':
#    total_ingredient = total_ingredient[:-1]

#add_ingredients = """ insert into smoothies.public.ing_ordered(ingredients_ordered)
            values """ + total_ingredient + """;"""

#try: 
#    conn.session.sql("truncate table smoothies.public.ing_ordered;").collect()
#    conn.session.sql(add_ingredients).collect()
#except: 
#    st.write('Order data not uploaded')

#convert the snowpark df to a Pandas df so we can use LOC function
#pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients to put in your custom Smoothie!'
    ,my_dataframe
    ,max_selections = 6
)

#created_dataframe = conn.session.sql("select INGREDIENTS_ORDERED as Ingredients, count(INGREDIENTS_ORDERED) as count from ing_ordered group by INGREDIENTS_ORDERED order by count desc;")

#queried_data = created_dataframe.to_pandas()

st.subheader("Cannot decide?")
st.subheader("Look at what our customer love!")
#st.bar_chart(data=queried_data, x="INGREDIENTS", y="COUNT" )

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
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    #if name_on_order == '':
    #    name_on_order = "Online Order "+str(random.randint(1,1000))
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        conn.session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")
        name_on_order = ''
        ingredients_list = ''
        
