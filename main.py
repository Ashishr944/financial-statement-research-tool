from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import shutil
import os
from fastapi import HTTPException
import traceback

from extractor import extract_income_statement_from_pdf, write_to_excel

app = FastAPI(title="Financial Statement Research Tool")

UPLOAD_DIR = "/tmp/uploads"
OUTPUT_FILE = "income_statement_output.xlsx"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h2>Financial Statement Extraction Tool</h2>
    <form action="/extract" enctype="multipart/form-data" method="post">
      <input type="file" name="file" accept=".pdf" required />
      <br/><br/>
      <button type="submit">Run Extraction</button>
    </form>
    """


@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    try:
        pdf_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        df = extract_income_statement_from_pdf(pdf_path)
        write_to_excel(df, OUTPUT_FILE)

        return FileResponse(
            OUTPUT_FILE,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="income_statement_output.xlsx"
        )

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))