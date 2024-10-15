from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain_openai import OpenAI,ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from decouple import config
key  = config('OPENAI_API_KEY')
from typing_extensions import Concatenate
# read text from pdf

def extract_data_from_text(raw_text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        # chunk_size = 1800,
        # chunk_overlap  = 200,
        # length_function = len,
    )
    texts = text_splitter.split_text(raw_text)
    embeddings = OpenAIEmbeddings(openai_api_key=key)
    document_search = FAISS.from_texts(texts, embeddings)
    query = "share the json"
    docs = document_search.similarity_search(query)
    relevant_info = "\n".join([doc.page_content for doc in docs])
    llm = ChatOpenAI(openai_api_key=key)
    messages = [
        SystemMessage(
            content="You are Jarvis, a helpful AI assistant. Answer the user's question based on the information provided."
        ),
        HumanMessage(
            content=f"Question: {query}\n\nUse this data to respond: {relevant_info}"
        )
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg.content

def extract_data_from_pdf(file_path):
    raw_text = ''
    pdfreader = PdfReader(file_path)
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content
    result = extract_data_from_text(raw_text)
    print(result)
    return result

    