from smolagents import CodeAgent, OpenAIServerModel
from tools import PdfTool, CandidateInfoTool, CsvSaveTool
from utils.csv_utils import save_to_csv
from utils.data_utils import extract_candidate_info
from config.config import CSV_FILE, API_KEY, MODEL_NAME, SKILLS

class GeminiRecruitmentAgent(CodeAgent):
    def __init__(self):
        # my tools
        tools = [
            PdfTool(),
            CandidateInfoTool(),
            CsvSaveTool()
        ]

        model = OpenAIServerModel(
            model_id=MODEL_NAME,
            api_base="https://openrouter.ai/api/v1",
            api_key=API_KEY
        )

        super().__init__(tools=tools, model=model, add_base_tools=True)

    def evaluate_candidate(self, cv_path, job_desc_path, csv_file=CSV_FILE):
        with open(job_desc_path, "r", encoding="utf-8") as f:
            job_description_content = f.read()

        # ديناميكي: يبني الفورمات على حسب SKILLS
        skills_json = ",\n".join([
            f'"{skill}": {{"exists": true/false, "score": 0-5}}'
            for skill in SKILLS
        ])

        prompt = f"""
        You are a smart AI recruitment assistant. You have access to these tools:
        - PdfTool(): extracts all text from a PDF file
        - CandidateInfoTool(): extracts candidate name, email, and phone from text
        - CsvSaveTool(): saves candidate info and screening results to a CSV file

        Task:
        Analyze the candidate's CV and the job description carefully by:
        - Read the CV {cv_path}.
        - Extract the name, email, and phone number.
        - Read the job description {job_description_content}.
        - Check how well the candidate matches the required skills.

        Required skills: {SKILLS}

        Provide a structured JSON in this format ONLY:

        {{
        "skills_scores": {{
            {skills_json}
        }},
        "total_score": sum of all scores,
        "result": "PASS" if total_score >= ({len(SKILLS)*5//2}) else "FAIL"
        }}

        - If a skill does not exist in the CV, set "exists": false and "score": 0.
        - If a skill exists, set "exists": true and assign a score between 1 and 5 based on strength.
        - Do not output reasoning or text outside JSON.
        - Finally, write the candidate info and screening to the CSV file {csv_file}.
        """

        result = self.run(prompt)
        return result
