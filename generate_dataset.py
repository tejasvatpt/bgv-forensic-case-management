import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta


random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

companies = [
    "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra",
    "Accenture", "Cognizant", "IBM India", "Deloitte", "KPMG",
    "EY India", "PwC India", "Capgemini", "Mphasis", "Hexaware"
]
universities = [
    "IIT Delhi", "IIT Bombay", "Delhi University", "Anna University",
    "VIT Vellore", "Manipal University", "Amity University",
    "BITS Pilani", "NIT Trichy", "Pune University"
]
degrees = [
    "B.Tech Computer Science", "B.Tech IT", "BCA", "MCA", "B.Sc IT",
    "MBA", "B.Com", "B.Tech Electronics", "M.Tech CS", "BBA"
]
roles = [
    "Software Engineer", "Data Analyst", "HR Executive", "Finance Analyst",
    "Operations Manager", "Business Analyst", "QA Engineer", "Project Manager"
]
cities = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai", "Pune", "Kolkata", "Noida"]


def rand_date(start_year=2015, end_year=2022):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

def gap_months(prev_end, next_start):
    return max(0, (next_start - prev_end).days // 30)


rows = []

for i in range(1, 101):
    case_id   = f"BGV-2024-{i:03d}"
    grad_year = random.randint(2012, 2022)

    edu_verified = random.choices([True, False], weights=[85, 15])[0]
    edu_result   = (
        random.choice(degrees)
        if edu_verified
        else random.choice(["Degree Not Found", "University Mismatch", "Year Mismatch"])
    )

    num_jobs     = random.randint(1, 3)
    emp_verified = random.choices([True, False], weights=[80, 20])[0]

    job_start = rand_date(grad_year, grad_year + 1)
    max_gap   = 0
    for _ in range(num_jobs - 1):
        job_end    = job_start + timedelta(days=random.randint(180, 900))
        next_start = job_end   + timedelta(days=random.randint(0, 300))
        max_gap    = max(max_gap, gap_months(job_end, next_start))
        job_start  = next_start

    criminal_flag = random.choices([False, True], weights=[90, 10])[0]
    ref_result    = random.choices(
        ["Positive", "Neutral", "Negative", "No Response"],
        weights=[60, 20, 10, 10]
    )[0]
    addr_verified = random.choices([True, False], weights=[88, 12])[0]

    flags = 0
    if not edu_verified:                          flags += 2
    if not emp_verified:                          flags += 2
    if max_gap > 6:                               flags += 1
    if criminal_flag:                             flags += 3
    if ref_result in ["Negative", "No Response"]: flags += 1
    if not addr_verified:                         flags += 1

    if flags == 0:
        risk_score  = random.randint(5, 20)
        risk_level  = "Low"
        compliance  = "Cleared"
        case_status = "Closed"
    elif flags <= 2:
        risk_score  = random.randint(21, 50)
        risk_level  = "Medium"
        compliance  = "Under Review"
        case_status = "Under Review"
    elif flags <= 4:
        risk_score  = random.randint(51, 75)
        risk_level  = "High"
        compliance  = "Requires Escalation"
        case_status = "Flagged"
    else:
        risk_score  = random.randint(76, 100)
        risk_level  = "Critical"
        compliance  = "Rejected"
        case_status = "Flagged"

    rows.append({
        "case_id":                       case_id,
        "candidate_name":                f"Candidate_{i:03d}",
        "age":                           random.randint(22, 40),
        "city":                          random.choice(cities),
        "applied_role":                  random.choice(roles),
        "declared_degree":               random.choice(degrees),
        "declared_university":           random.choice(universities),
        "graduation_year":               grad_year,
        "education_verified":            edu_verified,
        "education_verification_result": edu_result,
        "declared_experience_years":     random.randint(1, 8),
        "previous_companies":            ", ".join(random.sample(companies, num_jobs)),
        "employment_verified":           emp_verified,
        "max_employment_gap_months":     max_gap,
        "criminal_record_flag":          criminal_flag,
        "reference_check_result":        ref_result,
        "address_verified":              addr_verified,
        "total_flags":                   flags,
        "risk_score":                    risk_score,
        "risk_level":                    risk_level,
        "compliance_status":             compliance,
        "case_status":                   case_status,
        "case_opened_date":              (datetime.today() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d"),
    })


df = pd.DataFrame(rows)
df.to_csv("data/bgv_employee_dataset.csv", index=False)

print(f"Done — {len(df)} records saved to data/bgv_employee_dataset.csv")
print(df["risk_level"].value_counts().to_string())
