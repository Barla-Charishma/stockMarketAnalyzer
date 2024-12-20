import os
import streamlit as st
import pickle
import time
import langchain
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

# Access the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")




st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url) 
 
process_url_clicked =st.sidebar.button("Process URLs")
file_path="faisss_store_openai_pkl"

main_placeholder = st.empty()  
llm = OpenAI(openai_api_key="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",temperature=0.9, max_tokens=500)  

if process_url_clicked: 
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")  
    data = loader.load()

    
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )

    
    main_placeholder.text("Text Splitter...Started...✅✅✅")  
    docs = text_splitter.split_documents(data)


    
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    pkl = vectorstore_openai.serialize_to_bytes()
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")  
    time.sleep(2)  

    
    with open(file_path, "wb") as f:
        pickle.dump(pkl, f)



query = main_placeholder.text_input("Question: ")

if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pkl = pickle.load(f)
     
            vectorstore = FAISS.deserialize_from_bytes(embeddings=OpenAIEmbeddings(), serialized=pkl, allow_dangerous_deserialization=True)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            st.header("Answer")  
            st.write(result["answer"]) 

           
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:") 
                sources_list = sources.split("\n") 
                for source in sources_list:
                    st.write(source)  
    

