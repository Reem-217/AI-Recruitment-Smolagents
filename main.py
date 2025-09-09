from agent import GeminiRecruitmentAgent
from config.config import CV_PATH, JOB_DESC_PATH

def main():
    agent = GeminiRecruitmentAgent()
    result = agent.evaluate_candidate(CV_PATH, JOB_DESC_PATH)

    print("\n===== Recruitment Result \n")
    print(result)
    print("\n==============================\n")

if __name__ == "__main__":
    main()
