# import pandas as pd
# import chromadb
# import uuid


# class Portfolio:
#     def __init__(self, file_path="app/resource/my_portfolio.csv"):
#         self.file_path = file_path
#         self.data = pd.read_csv(file_path)
#         self.chroma_client = chromadb.PersistentClient('vectorstore')
#         self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

#     def load_portfolio(self):
#         if not self.collection.count():
#             for _, row in self.data.iterrows():
#                 self.collection.add(documents=row["Techstack"],
#                                     metadatas={"links": row["Links"]},
#                                     ids=[str(uuid.uuid4())])

#     def query_links(self, skills):
#         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])



import fitz  # PyMuPDF
import uuid
import chromadb
import os

class Portfolio:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text_data = self.extract_text_from_pdf()
        self.chroma_client = chromadb.PersistentClient("vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def extract_text_from_pdf(self):
        doc = fitz.open(self.file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text.strip()

    def load_portfolio(self):
        if not self.collection.count():
            self.collection.add(
                documents=[self.text_data],
                metadatas={"source": os.path.basename(self.file_path)},
                ids=[str(uuid.uuid4())]
            )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
