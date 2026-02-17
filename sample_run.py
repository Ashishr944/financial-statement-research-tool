from extractor import extract_income_statement_from_pdf, write_to_excel

PDF_PATH = "annual_report.pdf"
OUTPUT_PATH = "income_statement_output.xlsx"

df = extract_income_statement_from_pdf(PDF_PATH)
write_to_excel(df, OUTPUT_PATH)

print("✅ Extraction complete")
print(df.head())
