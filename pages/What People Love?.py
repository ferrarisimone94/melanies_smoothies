# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col
#import random

# Write directly to the app
st.title(":heart: What people love?")

conn = st.experimental_connection("snowpark")

total_ingredient = ""
number = 0
ingredients_ordered_df = conn.session.table("SMOOTHIES.PUBLIC.ORDERS").select(col('ingredients')).collect()
for i in ingredients_ordered_df:
    total_ingredient = total_ingredient + str(i)

total_ingredient = total_ingredient.replace("Row(INGREDIENTS=","(")
total_ingredient = total_ingredient.replace(", ","'),('")
total_ingredient = total_ingredient.replace("('')","")

def Convert(string): 
    li = list(string.split(", ")) 
    return li

if total_ingredient[len(total_ingredient)-1] == ',':
    total_ingredient = total_ingredient[:-1]

add_ingredients = """ insert into smoothies.public.ing_ordered(ingredients_ordered)
            values """ + total_ingredient + """;"""

try: 
    conn.session.sql("truncate table smoothies.public.ing_ordered;").collect()
    conn.session.sql(add_ingredients).collect()
except: 
    st.write('Order data not uploaded')

created_dataframe = conn.session.sql("select INGREDIENTS_ORDERED as Ingredients, count(INGREDIENTS_ORDERED) as count from ing_ordered group by INGREDIENTS_ORDERED order by count desc;")

queried_data = created_dataframe.to_pandas()

st.subheader("What our customers love the most")
st.bar_chart(data=queried_data, x="INGREDIENTS", y="COUNT" )
