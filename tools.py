from smolagents import Tool
from utils.pdf_utils import extract_text_from_pdf
from utils.data_utils import extract_candidate_info
from utils.csv_utils import save_to_csv


class PdfTool(Tool):
    name = "pdf_tool"
    description = "Extract text from a PDF file path"
    inputs = {"pdf_path": {"type": "string", "description": "Path to PDF file"}}
    output_type = "string"

    def forward(self, pdf_path: str) -> str:
        return extract_text_from_pdf(pdf_path)

class CandidateInfoTool(Tool):
    name = "candidate_info_tool"
    description = "Extract candidate info (name, email, phone) from CV text"
    inputs = {"cv_text": {"type": "string", "description": "Full CV text"}}
    output_type = "object"

    def forward(self, cv_text: str) -> dict:
        return extract_candidate_info(cv_text)

class CsvSaveTool(Tool):
    name = "csv_save_tool"
    description = "Save candidate info and screening results into CSV"
    inputs = {
        "candidate": {"type": "object", "description": "Candidate info dict"},
        "screening": {"type": "object", "description": "Screening results dict"}
    }
    output_type = "string"

    def forward(self, candidate: dict, screening: dict) -> str:
        save_to_csv(candidate, screening)
        return "Saved successfully"
