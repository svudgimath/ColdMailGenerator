import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator & Sender")
    url_input = st.text_input("Enter a URL:", value="https://job-boards.greenhouse.io/wileyedgerecruitingportal/jobs/4406212006")
    receiver_email = st.text_input("Enter recipient's email address:")
    submit_button = st.button("Submit")

    if submit_button:
        if not receiver_email:
            st.error("Please enter a valid recipient email address.")
        else:
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email, tone = llm.write_mail(job, links, receiver_email)
                    
                    st.code(email, language='markdown')
                    
                    # Display the email tone and sentiment
                    st.write(f"**Detected Tone:** {tone}")
                    if tone == "positive":
                        st.success("The email tone is positive, suitable for outreach.")
                    elif tone == "negative":
                        st.warning("The email tone seems negative, consider adjusting for a more positive or neutral tone.")
                    else:
                        st.info("The email tone is neutral.")
                    
                    st.success(f"Email has been sent to {receiver_email} successfully!")
                    
            except Exception as e:
                st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator & Sender", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)