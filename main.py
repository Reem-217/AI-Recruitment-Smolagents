from agent import GeminiRecruitmentAgent
import os

def main():
    resumes_folder = "Resumes" 
    job_desc_path = "Job_Description.txt"
    csv_file = "candidates.csv"

    agent = GeminiRecruitmentAgent()
    for filename in os.listdir(resumes_folder):
        if filename.lower().endswith(".pdf"):  
            cv_path = os.path.join(resumes_folder, filename)
            print(f"\n--- Evaluating {filename} ---")
            result = agent.evaluate_candidate(cv_path, job_desc_path, csv_file)
            print(result)

    print("\n===== All resumes have been evaluated! =====\n")
if __name__ == "__main__":
    main()
