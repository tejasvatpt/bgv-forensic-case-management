<<<<<<< HEAD
# bgv-forensic-case-management
Simulates a Background Verification (BGV) workflow used in forensic consulting. Runs 100 employee records through 6 verification checks, assigns weighted risk scores, and generates a compliance report flagging high-risk cases for legal review.
=======
# BGV Forensic Case Management & Risk Analytics

A Python-based pipeline that simulates a Background Verification (BGV) workflow — the kind used in forensic consulting and HR compliance teams. It generates a synthetic employee dataset, runs each record through a multi-step verification process, scores risk, and produces a compliance report with flagged cases.

---

## Why I built this

BGV and forensic data work is something I wanted to get hands-on with. Most publicly available datasets don't reflect the structure of real investigative pipelines, so I built one from scratch — synthetic data, realistic flag logic, and a compliance output that mirrors what you'd actually hand to a legal team.

---

## What it does

- Generates 100 synthetic employee records with fields like education history, employment gaps, criminal flags, and reference check outcomes
- Runs each record through 6 verification checks and assigns a weighted risk score
- Classifies cases as Low / Medium / High / Critical
- Builds a 4-panel analytics dashboard
- Outputs a structured compliance report listing all flagged cases with specific flag reasons

---

## Project structure

```
bgv-forensic-case-management/
│
├── data/
│   └── bgv_employee_dataset.csv
│
├── outputs/
│   ├── bgv_dashboard.png
│   └── bgv_compliance_report.txt
│
├── generate_dataset.py
├── bgv_pipeline.py
└── README.md
```

---

## Setup

```bash
pip install pandas numpy matplotlib
```

```bash
python generate_dataset.py   # creates the dataset
python bgv_pipeline.py       # runs the full analysis
```

---

## Verification checks covered

| Check | Weight |
|---|---|
| Education mismatch | 2 flags |
| Employment unverified | 2 flags |
| Criminal record | 3 flags |
| Employment gap > 6 months | 1 flag |
| Address unverified | 1 flag |
| Negative / no reference | 1 flag |

Cases with 0 flags → Cleared. 1–2 → Under Review. 3–4 → Escalation. 5+ → Rejected.

---

## Sample output

```
[3] Verification Check Results
  Education mismatch              21.0%  ████
  Employment unverified           20.0%  ████
  Criminal record flagged         10.0%  ██
  Address unverified              12.0%  ██
  Employment gap > 6 months       26.0%  █████
  Negative/no reference           18.0%  ███
```

---

## Tools used

Python, Pandas, NumPy, Matplotlib

---

## Note

All data in this project is fully synthetic — generated programmatically with no real personal information.
>>>>>>> 40fefa8 (Initial commit - added README)
