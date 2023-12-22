import streamlit as st 
from generate_retriever_index import *

# outputs = get_offers('target')
# print_outputs(outputs)

st.title('Offer Retriever/Search Engine')

st.write('Welcome to the Offer Retreiver/Search App!')

st.header('Overview', divider=True)

st.write('We had a dataset of offers on products from various retailers, brands and category of products. \
         We made an Offer Search Engine, where a user can input a natural language query and check if there are any offers \
         relevant to the retailer, brand or type of product mentioned in the query.')

query = st.text_input('query')

# st.write(query)

query_outputs = get_offers(query)

if len(query_outputs) == 0:
    st.write('No Offers :(')
else: 
    query_outputs = query_outputs.reset_index(drop=True)
    query_outputs.index += 1
    st.dataframe(query_outputs)
