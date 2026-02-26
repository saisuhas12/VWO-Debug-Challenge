# Financial Document Analyzer - VWO Debug Challenge Submission

## Project Overview
This project is an AI-powered financial document analysis system utilizing the **CrewAI** multi-agent framework alongside Google's **Gemini 2.5 Flash** LLM. The system allows users to upload financial PDF documents (e.g., earnings reports, 10-K filings), which are then processed by a sequence of specialized AI agents:
1. **Verifier:** Ensures the document is a valid financial report.
2. **Financial Analyst:** Extracts and analyzes core metrics (revenue, margins).
3. **Risk Assessor:** Identifies and structured potential market, credit, and operational risks.
4. **Investment Advisor:** Synthesizes the data into an actionable investment recommendation (Buy/Hold/Sell).

This repository represents the completed "Debug Challenge," where deterministic bugs and inefficient prompts have been identified and resolved to make the system fully functional and professional.

---

## 🐛 Bugs Found & Fixes Applied

### 1. Inefficient Prompts (Hallucinations & Joke Configuration)
*   **The Bug:** The roles, goals, and backstories in `agents.py` and `task.py` were highly unprofessional ("Make up investment advice," "Just say yes to everything"). Tasks expected random guesses and explicitly instructed agents to contradict themselves.
*   **The Fix:** I completely rewrote the prompts for all agents and tasks. Agents are now assigned strict, professional personas (Fiduciary Advisor, Compliance Officer). Tasks now heavily enforce strict reasoning tied explicitly to the data extracted from the `{file_path}` context.

### 2. Broken Tool Initialization (`tools.py`)
*   **The Bug:** The `FinancialDocumentTool` attempted to use an undefined `Pdf(path).load()` function. Furthermore, `InvestmentTool` and `RiskTool` were empty husks containing infinite `while` loops and raw syntax errors. None of the classes possessed the required `@tool` decorator.
*   **The Fix:** Implemented `PyMuPDF` (`fitz`) to accurately and performantly extract text from PDF files. Stripped out the broken infinite loops and correctly wrapped the method with the `@tool` decorator so CrewAI could parse it.

### 3. CrewAI Mismatched Agent Assignments (`task.py`)
*   **The Bug:** Every single task (Verification, Risk Assessment, Investment Analysis) was hard-assigned to the generic `financial_analyst` agent, defeating the purpose of a multi-agent framework.
*   **The Fix:** Re-assigned each task to its specialized agent (`verifier`, `risk_assessor`, `investment_advisor`).

### 4. API Logic Flow Failures (`main.py`)
*   **The Bug:** Inside the `run_crew()` initialization, only the `financial_analyst` was registered, leaving 3 agents completely inactive. Additionally, the FastAPI endpoint failed to pass the dynamically generated `file_path` to the crew, meaning agents were always reading a hardcoded dummy location.
*   **The Fix:** Updated the `Crew` initialization to register all 4 agents and tasks in sequential order. Passed both `query` and `file_path` into `financial_crew.kickoff()`. Also fixed a strict `uvicorn` warning by mapping the initialization string to `"main:app"`.

### 5. Dependency & Provider Failures (`agents.py` & `requirements.txt`)
*   **The Bug:** Missing API Key configuration (mapped to `llm=llm` which wasn't instantiated). Also, CrewAI's native Google Provider has version mismatch issues with the `gemini-1.5-flash` string on standard accounts.
*   **The Fix:** Installed `langchain-google-genai`. Replaced the native wrapper with `ChatGoogleGenerativeAI(model="gemini-2.5-flash")` ensuring reliable, fast, and secure API execution. Fixed the typo in the README reading `requirement.txt`.

---

## 🚀 Setup and Usage Instructions

### Prerequisites
Make sure you have **Python 3.10+** installed.

1. **Clone the repository:**
   ```sh
   git clone https://github.com/saisuhas12/VWO-Debug-Challenge
   cd financial-document-analyzer-debug
   ```

2. **Install Required Libraries:**
   ```sh
   pip install -r requirements.txt
   pip install langchain-google-genai pymupdf
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root of the project directory and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Run the Application locally:**
   ```sh
   python main.py
   ```
   *The server will start locally at `http://0.0.0.0:8000`.*

---

## 📖 API Documentation

The application runs using FastAPI. Once the server is running via `python main.py`, the interactive Swagger documentation is automatically hosted at:
### 👉 `http://localhost:8000/docs`

### Primary Endpoint
**`POST /analyze`**
*   **Description:** Uploads a PDF document and runs the sequential multi-agent Crew analysis.
*   **Parameters:**
    *   `file` (File, required): The financial PDF document.
    *   `query` (Form String, optional): A specific question or focus area (e.g., "Analyze the company's EV sales margins"). Defaults to "Analyze this financial document for investment insights".
*   **Response:**
    *   `status` (string)
    *   `query` (string)
    *   `analysis` (string): The formulated markdown response from the Investment Advisor agent.
    *   `file_processed` (string)
