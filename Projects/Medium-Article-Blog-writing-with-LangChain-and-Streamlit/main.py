import os 
import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain 
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

#insert your openai - api key here
os.environ['OPENAI_API_KEY'] = ''

#streamlit for UI
st.title('🖥️🤔 Medium Article Blog Assistant')
st.image('./medium.png')
prompt = st.text_input('Plug in your prompt here')

title_template = PromptTemplate(
    input_variables=['topic'], 
    template='write me a medium article blog about {topic}'
)

article_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'], 
    template='write me a medium article blog based on this title TITLE: {title} while leveraging this wikipedia research: {wikipedia_research}'
)

# article_template.format(topic='time series forecast',)

# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
article_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')

# Llms creation
llm = OpenAI(temperature=0.8) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
article_chain = LLMChain(llm=llm, prompt=article_template, verbose=True, output_key='article', memory=article_memory)

wiki = WikipediaAPIWrapper()

# Show the generated article with title on the screen if there's a prompt 
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    article = article_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(article) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Article History'): 
        st.info(article_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
