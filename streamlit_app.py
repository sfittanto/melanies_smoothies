# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")


name_on_order = st.text_input('Name on Smoothie')
st.write('The name for your Smoothie will be:', name_on_order)

fruit_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"))
)

fruit_options = [
    row["FRUIT_NAME"]
    for row in fruit_dataframe.collect()
]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list and name_on_order:
    ingredients_string = " ".join(ingredients_list)

    submit_order = st.button("Submit Order")

    if submit_order:
        my_insert_stmt = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
                (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
        """

        session.sql(
            my_insert_stmt,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success("Your Smoothie is ordered!", icon="✅")
