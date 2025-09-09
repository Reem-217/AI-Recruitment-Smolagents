import re

def extract_candidate_info(cv_text):
    email = re.search(r"[\w\.-]+@[\w\.-]+", cv_text)
    phone = re.search(r"\+?\d[\d\s\-\(\)]{7,}", cv_text)
    
    # extract name from the first line in the cv
    lines=[l.strip() for l in cv_text.split("\n") if l.strip()]
    name=lines[0] if lines else "Unknown"
    
    
    return {
        "name":name,
        "email":email.group(0) if email else "Not Found",
        "phone":phone.group(0) if phone else "Not Found"
        
    }    