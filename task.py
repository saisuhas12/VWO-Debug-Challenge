## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the provided financial document at the path: {file_path} to answer the user's query: {query}.\n\
Please utilize the read tool to extract the document content first. Focus on the core financial performance, margins, and key highlights.",
    expected_output="A concise but thorough financial analysis report addressing the user's specific query.\n\
The report should include key metrics, revenue changes, and notable financial health indicators.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Review the initial financial analysis and the core financial document ({file_path}) to provide sound investment recommendations.\n\
Take into account the user's focus: {query}. Base all recommendations on fundamentals and cite specific data from the report.",
    expected_output="An actionable investment advisory report outlining potential opportunities and whether the asset represents a strong buy, hold, or sell, heavily grounded in the data.",
    agent=investment_advisor,
    tools=[],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Conduct a detailed risk assessment based on the financial document located at {file_path}.\n\
Identify liquidity risks, market uncertainties, debt obligations, or any alarming operational factors mentioned in the text.",
    expected_output="A structured risk assessment detailing low, medium, and high-probability risks, along with suggestions for mitigating those risks if an investment is made.",
    agent=risk_assessor,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Verify the authenticity and relevance of the document located at {file_path}.\n\
Confirm it is a valid financial report (like an earnings release, 10-K, or similar corporate filing) before allowing further analysis.",
    expected_output="A short validation statement confirming the document type and its suitability for financial and investment analysis.",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)