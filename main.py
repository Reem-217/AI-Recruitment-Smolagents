from agent import GeminiRecruitmentAgent

def main():
    cv_path = "Reem_CV.pdf"
    job_desc_path = "Job_Description.txt"
    csv_file = "candidates.csv"

    agent = GeminiRecruitmentAgent()
    result = agent.evaluate_candidate(cv_path, job_desc_path)

    print("\n===== Recruitment Result =====\n")
    print(result)
    print("\n==============================\n")

if __name__ == "__main__":
    main()
