from smolagents import CodeAgent, OpenAIServerModel
from tools import PdfTool, CandidateInfoTool, CsvSaveTool
from utils.csv_utils import save_to_csv
from utils.data_utils import extract_candidate_info
from config.config import CSV_FILE,API_KEY, MODEL_NAME

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
        
        prompt = f"""
        You are a smart AI recruitment assistant. You have access to these tools:
        - PdfTool(): extracts all text from a PDF file
        - CandidateInfoTool(): extracts candidate name, email, and phone from text
        - CsvSaveTool(): saves candidate info and screening results to a CSV file

        Task:
        Analyze the candidate's CV and the job description carefully by:
        -Read the cv {cv_path}.
        -Extract the name, email, phone number.
        -Read the job description {job_description_content}.
        -Extract strengths , score, and result and focus on matching:

            1. Required skills (technical & soft skills)
            2. Relevant experience (years, projects, roles)
            3. Education or certifications relevant to the job
            4. Achievements or measurable results

        Provide a structured JSON:

        {{
        "strengths": [
            "Explain why each strength proves the candidate is suitable for the job",
            "The candidate MUST be in the same job field"
            "Skill X matches requirement Y",
            "Experience Z in role W is relevant
        ],
        "Score": from 1 to 10 based on how strongly and highly the candidate strengths mathces the job reuirements 
        "result":if score>=6 "PASS"  else "FAIL"
        }}

        Return **only JSON output**.
        -And Finally write the candidate info and screening to the csv file {csv_file}
        """


        result = self.run(prompt)
        return result
