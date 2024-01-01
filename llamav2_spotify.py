import os
import pinecone
import sys
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
import streamlit as st
import getpass

os.environ['REPLICATE_API_TOKEN'] = "r8_EXRCcMkZ0OIbqiyodux14JdxiiNBAIl2uN07o"
pinecone.init(api_key='0633f57d-9b00-4641-b163-e5331a0ab884', environment='gcp-starter')

print("Load document")
loader = CSVLoader(file_path="./data/spotify_review_simplify.csv", encoding="utf8")
documents = loader.load()

print("Split document")
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

print("Embedding Process")
embeddings = HuggingFaceEmbeddings()

index_name = "chatbot-llm"
index = pinecone.Index(index_name)
# Comment below line code if you want to replace the old index
vectordb = Pinecone.from_existing_index(index_name, embeddings)

## Uncomment below code if you want to replace the old index
# vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)

print("Define LLM")
llm = Replicate(
    model="meta/llama-2-7b-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea",
    model_kwargs={"temperature": 0.75, "max_length": 3000}
)

print("Final")
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    vectordb.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True
)

# Streamlit app
st.title("Chatbot with Streamlit")

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)



chat_history = []
query = st.text_input('Prompt:', key="prompt")
if st.button('Submit') or query:
    if query.lower() in ["exit", "quit", "q"]:
        st.write('Exiting')
        sys.exit()

    result = qa_chain({'question': query, 'chat_history': chat_history})
    st.write('Answer: ' + result['answer'])
    chat_history.append((query, result['answer']))