import csv
from datetime import datetime
from config.config import CSV_FILE

def save_to_csv(candidate, screening):
    header=["Timestamp", "Name", "Email", "Phone",
            "Strengths", "Score", "Result"]
    
    try:
        with open(CSV_FILE, 'x', newline="", encoding="utf-8") as f:
            writer= csv.writer(f)
            writer.writerow(header)
            
    except FileExistsError:
        pass     
    
    strengths = screening.get("strengths", [])
    if isinstance(strengths, list):
        strengths_str = "; ".join(strengths)
    else:
        strengths_str = str(strengths) 

    with open(CSV_FILE,"a", newline="", encoding="utf-8") as f:
        writer= csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            candidate["name"],
            candidate["email"],
            candidate["phone"],
            strengths_str,
            screening["score"],
            screening["result"]
        ])