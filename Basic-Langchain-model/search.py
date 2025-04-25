## Integrate code with Open AI api
import os
from constants import openai_key
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain #execute prompt template
# from langchain.chains import SimpleSequentialChain #simplesequentialchain provides only last prompt answer

from langchain.chains import SequentialChain # to get al metadata
from langchain.memory import ConversationBufferMemory

import streamlit as st

os.environ["OPENAI_API_KEY"] = openai_key


## streamlit framework init
st.title('Scientist Serarch Results')
input_text = st.text_input("Search scientist name you want..")

#custom prompt templates
first_input_prompt=PromptTemplate(
    input_variables = ['name'],
    template = "Tell me about {name}" )

# Memory

person_memory = ConversationBufferMemory(input_key='name', memory_key='chat_history')
dob_memory = ConversationBufferMemory(input_key='person', memory_key='chat_history')
descr_memory = ConversationBufferMemory(input_key='dob', memory_key='description_history')

## OpenAI llm models
#create llm chain for first prompt template
llm = OpenAI(temperature=0.8)#randomness of output
chain1 = LLMChain (llm=llm,prompt=first_input_prompt,verbose=True,output_key='person',memory=person_memory)


## creating multimple prompt templates

#custom prompt templates
second_input_prompt=PromptTemplate(
    input_variables = ['person'],
    template = "When was {person} born" )


#create llm chain for second prompt template
chain2 = LLMChain (llm=llm,prompt=second_input_prompt,verbose=True,output_key='dob',memory=dob_memory)


#custom prompt templates
third_input_prompt=PromptTemplate(
    input_variables = ['dob'],
    template = "Mention 5 major events happened around {dob} in the world" )

chain3 = LLMChain (llm=llm,prompt=third_input_prompt,verbose=True,output_key='eventsdescription',memory=descr_memory)


mainchain = SequentialChain(chains=[chain1,chain2,chain3],input_variables=['name'],output_variables=['person','dob','eventsdescription'],verbose=True)


if input_text:
    st.write(mainchain({'name':input_text}))

    with st.expander('Scientist name'):
        st.info(person_memory.buffer)
    with st.expander('Scientist dob'):
        st.info(dob_memory.buffer)
    with st.expander('Events'):
        st.info(descr_memory.buffer)

