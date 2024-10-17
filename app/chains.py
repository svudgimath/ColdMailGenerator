from sentiment import analyze_sentiment  # Import the sentiment analysis function
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from sentiment import analyze_sentiment
from sendMail import send_email  # Import the email sending function
load_dotenv()


class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: role, experience, skills and description.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, receiver_email):
        # Generate the portfolio explanation using the LLM
        portfolio_explanation_prompt = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### PORTFOLIO LINKS:
            {link_list}

            ### INSTRUCTION:
            You are an AI assistant. Your job is to explain why the portfolios listed above are relevant to the job description.
            Please generate a brief but clear explanation for each link, aligning the portfolio with the required job skills and description.
            ### EXPLANATION:
            """
        )
        
        chain_explanation = portfolio_explanation_prompt | self.llm
        explanation_res = chain_explanation.invoke({"job_description": str(job), "link_list": links})
        explanation = explanation_res.content

        # Continue with email generation
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}
            
            ### INSTRUCTION:
            You are Sathwik, a business development executive at XYZ. XYZ is a Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of XYZ 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase XYZ's portfolio: {link_list}
            Please include the following explanation as to why these portfolios were chosen:
            {portfolio_explanation}
            Remember you are Sathwik, BDE at XYZ. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            
            """
        )
        
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job), 
            "link_list": links, 
            "portfolio_explanation": explanation
        })
        email = res.content

        # Analyze the sentiment of the generated email
        polarity, subjectivity, tone = analyze_sentiment(email)
        
        # Automatically send the email
        subject = f"Cold Email Regarding {job.get('role')}"
        send_email(receiver_email, subject, email)
        
        return email, tone  # Return the email and its tone
