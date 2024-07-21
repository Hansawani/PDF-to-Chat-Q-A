# -*- coding: utf-8 -*-
"""Final RAG PDF-to-Q&A Chatbot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NPBdK9X0q5Xovx2MRTmgjt6mNSpNxZWo
"""

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

from torch import cuda, bfloat16
import torch
import transformers
from transformers import AutoTokenizer
from time import time
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

model_id = 'HuggingFaceH4/zephyr-7b-beta'

# Check if CUDA is available and set the device accordingly
if torch.cuda.is_available():
    device = f'cuda:{torch.cuda.current_device()}'
else:
    device = 'cpu'
    print("Warning: No GPU found. Quantization and model loading will be slower.")

# set quantization configuration to load large model with less GPU memory
# this requires the `bitsandbytes` library
bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
)

print(device)

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

model_config = transformers.AutoConfig.from_pretrained(
   model_id,
    trust_remote_code=True,
    max_new_tokens=1024
)
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    config=model_config,
    quantization_config=bnb_config,
    device_map='auto',
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# from torch import cuda, bfloat16
# from transformers import AutoTokenizer
# from time import time
# from langchain.llms import HuggingFacePipeline
# from langchain.vectorstores import Chroma
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain_community.llms import HuggingFaceHub
# from langchain.chains import LLMChain
# from langchain_core.prompts import PromptTemplate
# from langchain.prompts import ChatPromptTemplate
# import os
# from PyPDF2 import PdfReader
# from langchain.chains import RetrievalQA
# from google.colab import files
# import re
# import transformers
# import torch
# 
# model_id = 'HuggingFaceH4/zephyr-7b-beta'
# 
# # Check if CUDA is available and set the device accordingly
# if torch.cuda.is_available():
#     device = f'cuda:{torch.cuda.current_device()}'
# else:
#     device = 'cpu'
#     print("Warning: No GPU found. Quantization and model loading will be slower.")
# 
# # set quantization configuration to load large model with less GPU memory
# # this requires the `bitsandbytes` library
# bnb_config = transformers.BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type='nf4',
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype=bfloat16
# )
# 
# print(device)
# 
# os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
# 
# #model loaded
# model_config = transformers.AutoConfig.from_pretrained(
#    model_id,
#     trust_remote_code=True,
#     max_new_tokens=1024
# )
# model = transformers.AutoModelForCausalLM.from_pretrained(
#     model_id,
#     trust_remote_code=True,
#     config=model_config,
#     quantization_config=bnb_config,
#     device_map='auto',
# )
# 
# #tokenizer initialised
# tokenizer = AutoTokenizer.from_pretrained(model_id)
# 
# st.title("PDF Question Answering with Zephyr-7B")
# 
# #prompr template initialised
# PROMPT_TEMPLATE = """<s>[INST] Using the following piece of information: {context} answer the Question: {question}.
# Just generate the answer without explanation.Only provide the answer.[/INST] </s>"""
# 
# # Upload the PDF file
# uploaded_files = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
# 
# # Read the uploaded PDF file
# if uploaded_files:
#     all_texts = ""
# 
#     for uploaded_file in uploaded_files:
#         # Read each uploaded PDF file
#         reader = PdfReader(uploaded_file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#         all_texts += text
# 
#     # Split text into chunks
#     text_splitter = RecursiveCharacterTextSplitter(
#         separators=['\n'],
#         chunk_size=500,
#         chunk_overlap=150,
#         length_function=len
#     )
#     chunks = text_splitter.split_text(all_texts)
# 
#     # Generate embeddings
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# 
#     # Create vector store
#     vector_store = FAISS.from_texts(chunks, embeddings)
# 
#     # Get user question on main page
#     user_question = st.text_input("Please enter your question: ")
# 
#     if user_question:
# 
#             # Use prompt template
#             prompt = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])
# 
#             #initialise pipeline
#             query_pipeline = transformers.pipeline(
#                 "text-generation",
#                 model=model,
#                 tokenizer=tokenizer,
#                 torch_dtype=torch.float16,
#                 max_length=6000,  # Increase max_length
#                 max_new_tokens=500,  # Control the number of new tokens generated
#                 device_map="auto",
#             )
# 
#             # Initialize the LLM
#             llm = HuggingFacePipeline(pipeline=query_pipeline)
# 
#             # Initialize the QA chain
#             qa=RetrievalQA.from_chain_type(
#                   llm=llm,
#                   chain_type="stuff",
#                   retriever=vector_store.as_retriever(
#                   search_type="similarity",
#                   search_kwargs={"k": 3}
#                   ),
#                   return_source_documents=True,
#                   chain_type_kwargs={"prompt": prompt}
#                 )
# 
#             # Generate the response
#             answer=qa({"query": user_question})
# 
#             # Display the response
#             result=answer["result"]
# 
#             pattern = re.compile(r'<s>\[INST\] Using the following piece of information:.*?\[/INST\] </s>(.*)', re.DOTALL)
#             match = pattern.search(result)
#             if match:
#                 clean_answer = match.group(1).strip()
#             else:
#                 clean_answer = answer.strip()
# 
#             # Display the clean answer
#             st.write(clean_answer)
# 
# else:
#     st.write("Please upload a PDF file to continue.")

