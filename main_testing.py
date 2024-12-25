from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("ECE 10AL Lab Report 4.pdf")
data = loader.load()
print(data)