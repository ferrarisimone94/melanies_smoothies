# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")

#name_on_order = st.text_input('Name on Smoothie:')
#st.write('The name on your Smoothie will be: ', name_on_order)

st.write(
    """Orders that need to be filled:"""
)

session = get_active_session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()

if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')

    if submitted:

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['order_uid'] == edited_dataset['order_uid'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
            st.success("Order(s) Updated!")
        except:
            st.write('Something went wrong.')
else:
    st.success('There are no pending orders right now! ;(')

#option = st.selectbox('How would you like to be contacted?', 
#                      ('Banana', 'Strawberries', 'Peaches'))
#st.write('You selected:', option)

#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#ingredients_list = st.multiselect(
#    'Choose up to 5 ingredients:'
#    ,my_dataframe
#)

#if the list is not empty do....
#if ingredients_list: 
#    #st.write(ingredients_list)
#    #st.text(ingredients_list)
#    
#    ingredients_string = ''
#    
#    for fruit_chosen in ingredients_list:
#        ingredients_string += fruit_chosen + ' '
#    
#    #st.write(ingredients_string)

#    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

#    time_to_insert = st.button('Submit Order')
    
#    #st.write(my_insert_stmt)
#    #st.stop()
#    if time_to_insert:
#        session.sql(my_insert_stmt).collect()
#        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")