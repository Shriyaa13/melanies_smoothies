import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(" :cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """choose the fruits that you want in custom smoothie
    """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your smoothie will be",name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "choose upto 5 ingredients",
    my_dataframe,max_selections = 5
)
if ingredients_list: 
    ingredients_string =''
    for x in ingredients_list:
        ingredients_string += x + ' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                  values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    #st.write(my_insert_stmt)
    #st.stop
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response(),use_cintainer_width=True)

