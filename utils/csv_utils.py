import csv
from datetime import datetime
from config.config import CSV_FILE

skills = ["RAG", "Automation", "NLP", "Web Scraping"]

def save_to_csv(candidate, screening):
    # بناء الهيدر: لكل skill عمودين (exists + score)
    header = ["Timestamp", "Name", "Email", "Phone"]
    for skill in skills:
        header.append(skill)          # البوليان
        header.append(f"{skill} Score")  # السكور
    header.extend(["Total Score", "Result"])

    try:
        with open(CSV_FILE, 'x', newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
    except FileExistsError:
        pass

    # كتابة البيانات
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        candidate["name"],
        candidate["email"],
        candidate["phone"]
    ]

    # نضيف كل skill (exists + score)
    for skill in skills:
        skill_data = screening["skills_scores"].get(skill, {"exists": False, "score": 0})
        row.append(skill_data["exists"])
        row.append(skill_data["score"])

    row.extend([screening["total_score"], screening["result"]])

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)
