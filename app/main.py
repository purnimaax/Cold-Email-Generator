# streamlit run .\app\main.py
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import tempfile
from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm):
    st.title("Cold Mail Generator")
    url_input = st.text_input("Enter a job listing URL:")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    temp_path = None
    if uploaded_file is not None:
        st.success("Resume uploaded successfully!")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

    submit_button = st.button("Generate Cold Email")

    if submit_button:
        if not url_input or not temp_path:
            st.error("Please provide both a job URL and a resume PDF.")
            return

        try:
            # Load and clean job data
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            # Load resume data
            portfolio = Portfolio(temp_path)
            portfolio.load_portfolio()

            jobs = llm.extract_jobs(data)

            for job in jobs:
                skills = job.get("skills", [])
                resume_info = portfolio.text_data  # full resume text
                email = llm.write_mail(job, resume_info)
                with st.container():
                  st.markdown(email, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain)
