## Integrate code with Open AI api
import os
from constants import openai_key
from langchain.llms import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = openai_key


## streamlit framework init
st.title('Langchain Demo with OpenAI API')
input_text = st.text_input("Search what you want")


## OpenAI llm models
llm = OpenAI(temperature=0.8)#randomness of output


if input_text:
    st.write(llm(input_text))