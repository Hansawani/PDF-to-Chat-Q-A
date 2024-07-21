PDF-to-Chat-Q-A
This project aims to develop a chatbot that utilises generative AI, specifically the fine-tuned model Zephyr-7B to allow users to upload multiple PDF files and ask questions to the AI model about their domain specific PDFs and get quick answers. This is useful if the data to be read by the user is very large and they require the assistance of an AI model.
The code involves multiple technologies, languages, and techniques for building a PDF-based question-answering application. Here’s a breakdown of each:

Languages:
1. Python

Techniques and Concepts:
1. Natural Language Processing (NLP)
2. Prompt Engineering: Crafting specific prompts for the language model to generate accurate and relevant answers.
3. Quantization: Reducing the precision of the model's weights to decrease memory usage and computation time.
4. Regular Expressions: Used for pattern matching to clean the generated answers.

Technologies and Libraries:
1. Streamlit: Used for building the web interface of the application.
2. PyPDF2: For reading and extracting text from PDF files.
3. LangChain:
   - For chaining different NLP components together.
   - Modules: `HuggingFacePipeline`, `PromptTemplate`, `RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`, `FAISS`, `RetrievalQA`.
4. Transformers:
   - For utilizing pre-trained transformer models.
   - Functions and Classes: `AutoTokenizer`, `pipeline`, `AutoConfig`, `AutoModelForCausalLM`, `BitsAndBytesConfig`.
5. FAISS: For efficient similarity search and clustering of dense vectors.
6. Torch: For tensor computations and deep learning operations.
7. Regular Expressions (re module): For pattern matching and text processing.

In conclusion, this setup integrates multiple modern NLP techniques and libraries to build an interactive question-answering application based on PDF documents.
