## Importing libraries and files
import os
import fitz  # PyMuPDF for reading PDFs
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool
from crewai.tools import tool

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool():
    @tool("Read Financial Document Data Tool")
    def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path
        
        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file textual content.
        """
        try:
            doc = fitz.open(path)
            full_report = ""
            for page in doc:
                content = page.get_text()
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF {path}: {str(e)}"

## Creating Investment Analysis Tool
class InvestmentTool:
    @tool("Analyze Investment Tool")
    def analyze_investment_tool(financial_document_data: str) -> str:
        """Tool to analyze investment from financial document data.
        
        Args:
            financial_document_data (str): The content of the financial document
            
        Returns:
            str: Analysis regarding the investment
        """
        # A simple pass-through or basic preprocessing if needed
        # We can let the agent LLM do the actual thinking, this tool just structures the task
        return "Investment analysis structure initialized. Please review the financial data directly to form an opinion."

## Creating Risk Assessment Tool
class RiskTool:
    @tool("Create Risk Assessment Tool")
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """Tool to create a risk assessment based on document data.
        
        Args:
            financial_document_data (str): The content of the financial document
            
        Returns:
            str: Assessment regarding the risk
        """
        return "Risk assessment structure initialized. Please review the financial data to identify real risk factors."