import pdfplumber
import pandas as pd

from line_items import CANONICAL_LINE_ITEMS
from utils import extract_numbers, fuzzy_match_line_item


def extract_income_statement_from_pdf(pdf_path):
    rows = []
    currency = "UNKNOWN"
    unit = "UNKNOWN"

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text is None:
                continue

            lower_text = text.lower()

            # Detect currency & units
            if "₹" in lower_text or "inr" in lower_text:
                currency = "INR"
            if "million" in lower_text:
                unit = "Millions"
            elif "crore" in lower_text:
                unit = "Crores"

            # Income statement detection
            if "income statement" in lower_text or "statement of profit" in lower_text:
                for line in text.split("\n"):
                    numbers = extract_numbers(line)
                    if not numbers:
                        continue

                    canonical, score = fuzzy_match_line_item(
                        line, CANONICAL_LINE_ITEMS
                    )

                    rows.append({
                        "Raw Line Item": line.strip(),
                        "Canonical Category": canonical if canonical else "UNMAPPED",
                        "Value": numbers[0] if len(numbers) == 1 else "AMBIGUOUS",
                        "Currency": currency,
                        "Unit": unit,
                        "Page": page_number,
                        "Confidence": (
                            "High" if score >= 90 else
                            "Medium" if score >= 80 else
                            "Low"
                        )
                    })

    # ✅ Enforce schema even if rows are empty
    columns = [
        "Raw Line Item",
        "Canonical Category",
        "Value",
        "Currency",
        "Unit",
        "Page",
        "Confidence"
    ]

    return pd.DataFrame(rows, columns=columns)


def write_to_excel(df, output_path):
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Main sheet
        df.to_excel(writer, sheet_name="Income_Statement", index=False)

        # Issues / notes sheet
        if df.empty:
            issues = df
        else:
            issues = df[
                (df["Canonical Category"] == "UNMAPPED") |
                (df["Value"] == "AMBIGUOUS")
            ]

        issues.to_excel(writer, sheet_name="Extraction_Notes", index=False)
