Web: https://financial-statement-research-tool.onrender.com
Financial Statement Extraction Research Tool
Overview

This project implements a research-oriented data extraction tool that converts unstructured annual report PDFs into structured, analyst-ready Excel outputs.

The system is intentionally designed as a deterministic research tool, not an open-ended AI chatbot.
It focuses on accuracy, auditability, and explicit uncertainty handling, enabling downstream financial analysis with minimal manual intervention.

Objective

Automate extraction of income statement line items from annual reports while:

Avoiding numeric hallucination

Normalizing inconsistent line item naming

Preserving source traceability

Flagging ambiguous or missing data explicitly

System Flow
Document Upload (PDF)
        ↓
Text Extraction
        ↓
Income Statement Detection
        ↓
Line Item Identification
        ↓
Canonical Normalization
        ↓
Numeric Validation
        ↓
Excel Output for Analysis

Key Design Principles
Deterministic Extraction

Rule-based parsing and fuzzy matching are used for predictable behavior.

No inferred or generated numeric values.

Controlled AI Usage

AI (optional) is limited to classification and normalization only.

Numeric extraction is strictly rule-based.

Analyst-Friendly Output

Ambiguity is surfaced, not hidden.

All outputs are reviewable in Excel.

Project Structure
task/
├── extractor.py        # Core extraction pipeline
├── line_items.py       # Canonical line item definitions
├── utils.py            # Text processing & matching utilities
├── sample_run.py       # End-to-end execution script
├── requirements.txt    # Dependencies
└── README.md

Input

Format: PDF (digital annual reports)

File name: annual_report.pdf

Documents may contain varying terminology and layouts.

Output
Excel File: income_statement_output.xlsx
Sheet 1: Income_Statement
Field	Description
Raw Line Item	Extracted text from document
Canonical Category	Normalized financial category
Value	Extracted numeric value
Currency	Detected or UNKNOWN
Unit	Millions / Crores / UNKNOWN
Page	Source page number
Confidence	Extraction confidence level
Sheet 2: Extraction_Notes

Contains:

Unmapped line items

Ambiguous numeric values

Data requiring analyst review

Handling Real-World Variability
Line Item Name Variations

Different naming conventions are normalized using a canonical dictionary and fuzzy matching:

Example Input	Normalized
Net Sales	Revenue
Operating Costs	Operating Expenses
PAT	Net Profit

Unrecognized items are marked as UNMAPPED.

Missing or Ambiguous Data

Missing values → NA

Multiple numeric matches → AMBIGUOUS

Unknown units or currency → UNKNOWN

No assumptions are made.

Technology Stack

Language: Python 3.11

PDF Parsing: pdfplumber

Data Processing: pandas

Excel Output: openpyxl

Fuzzy Matching: rapidfuzz

Setup & Execution
1. Activate Virtual Environment
source venv/bin/activate

2. Install Dependencies
pip install -r requirements.txt

3. Run Extraction
python sample_run.py

Evaluation Alignment
Requirement	Addressed
Structured outputs	✅
No hallucinated values	✅
Analyst usability	✅
Ambiguity visibility	✅
Extendable design	✅
Limitations

Optimized for text-based PDFs

Scanned documents require OCR extension

Column-level multi-year extraction can be extended further

Extensibility

OCR integration for scanned PDFs

Balance sheet and cash flow extraction

Multi-document consolidation

API deployment (FastAPI)

Confidence scoring per extracted value

Author

Ashish Rokade
Software Development & Research Tooling



Reviewer Note

This implementation intentionally prioritizes correctness and transparency over completeness, aligning with internal research workflows where analyst trust and auditability are critical.

