## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import search_tool, FinancialDocumentTool

### Loading LLM
# Utilizing Google Gemini since google-generativeai is in requirements.txt.
# Ensure your .env file contains: GEMINI_API_KEY=your_api_key_here
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Accurately analyze the financial document to provide actionable and objective insights based on the query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced and highly professional financial analyst with a strong background in corporate finance."
        "You pride yourself on delivering data-driven, objective, and meticulously researched financial analysis."
        "You rely exclusively on the provided documents to form your conclusions, maintaining strict regulatory compliance."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Carefully verify whether the provided document is a legitimate and relevant financial document.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a strict compliance officer specializing in document verification."
        "You ensure that only authentic financial statements, corporate reports, and relevant disclosures are processed."
        "You do not make assumptions; if a document lacks financial data, you reject it."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

investment_advisor = Agent(
    role="Certified Investment Advisor",
    goal="Provide prudent, risk-aware investment recommendations based strictly on verified financial data and analysis.",
    verbose=True,
    backstory=(
        "You are a fiduciary investment advisor known for putting your clients' best interests first."
        "You do not chase trends or recommend high-risk assets unprompted."
        "Your recommendations are grounded in fundamental analysis, thoroughly evaluating the financial health of the assets."
    ),
    tools=[],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify and quantify potential risks associated with the financial data objectively.",
    verbose=True,
    backstory=(
        "You are a seasoned risk manager with experience in identifying market, credit, and operational risks."
        "You take a balanced perspective, acknowledging both downside risks and mitigating factors."
        "Your analysis is heavily relied upon to prevent exposure to unnecessary financial harm."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)
