from smolagents import CodeAgent, OpenAIServerModel
from tools import PdfTool, CandidateInfoTool, CsvSaveTool
import re
from smolagents import OpenAIServerModel
from utils.pdf_utils import extract_text_from_pdf
from utils.csv_utils import save_to_csv
from utils.data_utils import extract_candidate_info
from config.config import CSV_FILE, API_KEY, MODEL_NAME

def parse_json_like(s):
    s = s.strip()
    if s.startswith("```json"):
        s = s[7:]
    if s.endswith("```"):
        s = s[:-3]
    
    try:
        # This is a simplified parser and might not work for all cases.
        strengths_match = re.search(r'"strengths":\s*(\[.*?\])', s, re.DOTALL)
        strengths_str = strengths_match.group(1) if strengths_match else "[]"
        strengths = [item.strip() for item in strengths_str.strip("[]").replace('"', '').split(',') if item.strip()]

        score_match = re.search(r'"score":\s*(\d+)', s)
        score = int(score_match.group(1)) if score_match else 0

        result_match = re.search(r'"result":\s*"(.*?)"', s)
        result = result_match.group(1) if result_match else ""

        return {"strengths": strengths, "score": score, "result": result}
    except Exception as e:
        print(f"Error parsing JSON-like string: {e}")
        return {"strengths": [], "score": 0, "result": "ERROR"}

class GeminiRecruitmentAgent:
    def __init__(self):
        self.model = OpenAIServerModel(
            model_id=MODEL_NAME,
            api_base="https://openrouter.ai/api/v1",
            api_key=API_KEY
        )

    def evaluate_candidate(self, cv_path, job_desc_path, csv_file=CSV_FILE):
        cv_text = extract_text_from_pdf(cv_path)
        candidate_info = extract_candidate_info(cv_text)

        with open(job_desc_path, "r", encoding="utf-8") as f:
            job_description_content = f.read()

        prompt = f"""
        You are a smart AI recruitment assistant.

        Analyze the candidate's CV and the job description carefully.

        CV:
        {cv_text}

        Job Description:
        {job_description_content}

        Extract strengths, score, and result based on the following criteria:
        1. Required skills (technical & soft skills)
        2. Relevant experience (years, projects, roles)
        3. Education or certifications relevant to the job
        4. Achievements or measurable results

        Provide a structured JSON output with the following format:
        {{
            "strengths": ["strength1", "strength2", ...],
            "score": <score from 1 to 10>,
            "result": "PASS" or "FAIL"
        }}

        Return **only the JSON output**.
        """

        model_output = self.model([{"role": "user", "content": prompt}])
        
        # Manual parsing of the JSON-like output
        screening_result = parse_json_like(model_output.content)

        save_to_csv(candidate_info, screening_result)

        return screening_result
