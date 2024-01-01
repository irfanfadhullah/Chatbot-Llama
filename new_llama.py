import os
import pinecone
import sys
import streamlit as st
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
import time

with st.sidebar:
    st.title('🦙💬 Llama 2 Chatbot Authentication')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
        pinecone_api = st.secrets['PINECONE_API_TOKEN']
        environment_name = st.secrets['ENVIRONMENT_NAME']
        mode = 'existing'
    else:
        mode = 'new'
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
        pinecone_api = st.text_input('Enter Pinecone API token:', type='password')
        environment_name = st.text_input('Enter Pinecone Environment Name:', type='password')
        st.write('Please wait until indexing process done.')

os.environ['REPLICATE_API_TOKEN'] = replicate_api
pinecone.init(api_key=pinecone_api, environment=environment_name)

def load_and_split_documents():
    print("Load document")
    loader = CSVLoader(file_path="./data/spotify_review_simplify.csv", encoding="utf8")
    documents = loader.load()

    print("Split document")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    return texts

def create_or_load_index(embeddings, texts, mode="existing"):
    index_name = "chatbot-llm"
    index = pinecone.Index(index_name)

    if mode =='existing':
        vectordb = Pinecone.from_existing_index(index_name, embeddings)
    elif mode == "new":
        vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)
    return vectordb

def initialize_llm():
    print("Define LLM")
    llm = Replicate(
        model="meta/llama-2-7b-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea",
        model_kwargs={"temperature": 0.75, "max_length": 3000}
    )
    return llm

def initialize_qa_chain(llm, vectordb):
    print("Final")
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        vectordb.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )
    return qa_chain

texts = load_and_split_documents()
embeddings = HuggingFaceEmbeddings()
vectordb = create_or_load_index(embeddings, texts, mode = mode)
llm = initialize_llm()
qa_chain = initialize_qa_chain(llm, vectordb)

st.title("🎼Chatbot about Spotify🎼")
chat_history = []
query = st.text_input('Prompt:', key="prompt")

if st.button('Submit') or query:
    if query.lower() in ["exit", "quit", "q"]:
        st.write('Exiting')
        sys.exit()
    try:
        result = qa_chain({'question': query, 'chat_history': chat_history})
        st.write('Answer: ' + result['answer'])
        chat_history.append((query, result['answer']))
    except Exception as e:
        try:
            result = qa_chain({'question': query, 'chat_history': chat_history})
            st.write('Answer: ' + result['answer'])
            chat_history.append((query, result['answer']))
        except Exception as e:
            st.write('Please Submit Again')
