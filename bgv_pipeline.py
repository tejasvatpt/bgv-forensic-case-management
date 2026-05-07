import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime


DATA_PATH = "data/bgv_employee_dataset.csv"
OUTPUT_DIR = "outputs"
REPORT_DATE = datetime.today().strftime("%d %b %Y")

os.makedirs(OUTPUT_DIR, exist_ok=True)

RISK_COLORS = {
    "Low":      "#22c55e",
    "Medium":   "#f59e0b",
    "High":     "#ef4444",
    "Critical": "#7f1d1d",
}


print("=" * 60)
print("  BGV FORENSIC ANALYSIS PIPELINE")
print(f"  Run date: {REPORT_DATE}")
print("=" * 60)


df = pd.read_csv(DATA_PATH)
print(f"\n[1] Loaded {len(df)} cases from dataset\n")

missing = df.isnull().sum()
if missing.any():
    print("  Heads up — some missing values found:")
    print(missing[missing > 0])
else:
    print("  All fields present, no missing values.")


print("\n[2] Case Status Breakdown")
print("-" * 40)

for status, count in df["case_status"].value_counts().items():
    print(f"  {status:<15} : {count:>3} cases  ({count/len(df)*100:.1f}%)")

print("\n  Compliance outcomes:")
for status, count in df["compliance_status"].value_counts().items():
    print(f"  {status:<28} : {count:>3}  ({count/len(df)*100:.1f}%)")


print("\n[3] Verification Check Results")
print("-" * 40)

edu_fail   = (~df["education_verified"]).mean() * 100
emp_fail   = (~df["employment_verified"]).mean() * 100
criminal   = df["criminal_record_flag"].mean() * 100
addr_fail  = (~df["address_verified"]).mean() * 100
gap_flag   = (df["max_employment_gap_months"] > 6).mean() * 100
bad_ref    = df["reference_check_result"].isin(["Negative", "No Response"]).mean() * 100

checks = {
    "Education mismatch"        : edu_fail,
    "Employment unverified"     : emp_fail,
    "Criminal record flagged"   : criminal,
    "Address unverified"        : addr_fail,
    "Employment gap > 6 months" : gap_flag,
    "Negative/no reference"     : bad_ref,
}

for label, rate in checks.items():
    bar = "█" * int(rate / 5)
    print(f"  {label:<30} {rate:>5.1f}%  {bar}")


print("\n[4] Risk Distribution")
print("-" * 40)

risk_dist = df["risk_level"].value_counts()
for level in ["Low", "Medium", "High", "Critical"]:
    count = risk_dist.get(level, 0)
    print(f"  {level:<10} : {count:>3} candidates  ({count/len(df)*100:.1f}%)")

print(f"\n  Avg risk score : {df['risk_score'].mean():.1f} / 100")
print(f"  Cases needing legal review : {len(df[df['risk_level'].isin(['High','Critical'])])}")


print("\n[5] Building dashboard...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("BGV Forensic Analytics Dashboard", fontsize=16, fontweight="bold", y=1.01)

ax1 = axes[0, 0]
levels = ["Low", "Medium", "High", "Critical"]
counts = [risk_dist.get(l, 0) for l in levels]
bars = ax1.bar(levels, counts, color=[RISK_COLORS[l] for l in levels], edgecolor="white", linewidth=1.5)
ax1.set_title("Risk Level Distribution", fontweight="bold")
ax1.set_ylabel("Number of Cases")
for b, c in zip(bars, counts):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.3, str(c),
             ha="center", va="bottom", fontweight="bold")
ax1.set_ylim(0, max(counts) + 6)
ax1.spines[["top", "right"]].set_visible(False)

ax2 = axes[0, 1]
short_labels = ["Education", "Employment", "Criminal\nFlag", "Address", "Emp Gap\n>6mo", "Negative\nRef"]
rates = list(checks.values())
bar_colors = ["#3b82f6", "#8b5cf6", "#ef4444", "#f59e0b", "#6b7280", "#ec4899"]
bars2 = ax2.barh(short_labels, rates, color=bar_colors, edgecolor="white")
ax2.set_title("Forensic Check Failure Rates (%)", fontweight="bold")
ax2.set_xlabel("Failure Rate (%)")
for b, r in zip(bars2, rates):
    ax2.text(b.get_width() + 0.3, b.get_y() + b.get_height()/2,
             f"{r:.1f}%", va="center", fontsize=9)
ax2.set_xlim(0, max(rates) + 6)
ax2.spines[["top", "right"]].set_visible(False)

ax3 = axes[1, 0]
comp_summary = df["compliance_status"].value_counts()
pie_colors = ["#22c55e", "#f59e0b", "#ef4444", "#7f1d1d"][:len(comp_summary)]
ax3.pie(comp_summary.values, labels=comp_summary.index, autopct="%1.1f%%",
        colors=pie_colors, startangle=90, textprops={"fontsize": 9})
ax3.set_title("Compliance Status Breakdown", fontweight="bold")

ax4 = axes[1, 1]
for level in levels:
    subset = df[df["risk_level"] == level]["risk_score"]
    ax4.hist(subset, bins=10, alpha=0.7, label=level, color=RISK_COLORS[level], edgecolor="white")
ax4.set_title("Risk Score Distribution by Level", fontweight="bold")
ax4.set_xlabel("Risk Score (0–100)")
ax4.set_ylabel("Frequency")
ax4.legend()
ax4.spines[["top", "right"]].set_visible(False)

plt.tight_layout()
chart_path = os.path.join(OUTPUT_DIR, "bgv_dashboard.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"  Saved → {chart_path}")


print("\n[6] Writing compliance report...")

flagged = df[df["risk_level"].isin(["High", "Critical"])].copy()
flagged = flagged.sort_values("risk_score", ascending=False)

lines = [
    "=" * 65,
    "  BGV FORENSIC COMPLIANCE REPORT",
    f"  Generated : {REPORT_DATE}",
    f"  Total Cases Reviewed : {len(df)}",
    "=" * 65,
    "",
    "EXECUTIVE SUMMARY",
    "-" * 65,
    f"  Total cases processed           : {len(df)}",
    f"  Cleared (Low Risk)              : {len(df[df['risk_level']=='Low'])}",
    f"  Under Review (Medium Risk)      : {len(df[df['risk_level']=='Medium'])}",
    f"  Requires Escalation (High)      : {len(df[df['risk_level']=='High'])}",
    f"  Rejected (Critical)             : {len(df[df['risk_level']=='Critical'])}",
    "",
    f"  Education verification failures : {int(edu_fail * len(df) / 100)} cases ({edu_fail:.1f}%)",
    f"  Employment verification failures: {int(emp_fail * len(df) / 100)} cases ({emp_fail:.1f}%)",
    f"  Criminal record flags           : {int(criminal * len(df) / 100)} cases ({criminal:.1f}%)",
    "",
    "FLAGGED CASES — REQUIRES LEGAL & COMPLIANCE REVIEW",
    "-" * 65,
]

for _, row in flagged.iterrows():
    reasons = []
    if not row["education_verified"]:
        reasons.append("Education mismatch")
    if not row["employment_verified"]:
        reasons.append("Employment unverified")
    if row["criminal_record_flag"]:
        reasons.append("Criminal record")
    if row["max_employment_gap_months"] > 6:
        reasons.append(f"Gap {row['max_employment_gap_months']}mo")
    if not row["address_verified"]:
        reasons.append("Address unverified")
    if row["reference_check_result"] in ["Negative", "No Response"]:
        reasons.append(f"Ref: {row['reference_check_result']}")

    lines.append(
        f"  [{row['case_id']}]  {row['candidate_name']:<18}"
        f"  Risk: {row['risk_score']:>3}/100  [{row['risk_level']}]"
        f"  Flags: {', '.join(reasons)}"
    )

lines += [
    "",
    "COMPLIANCE DECLARATION",
    "-" * 65,
    "  This report follows standard BGV procedures and commercial",
    "  hiring compliance guidelines. All flagged cases must be",
    "  reviewed by the Legal & Compliance team before onboarding.",
    "",
    "  Cases marked Critical must not be onboarded without explicit",
    "  written clearance from the Legal department.",
    "=" * 65,
]

report_text = "\n".join(lines)
report_path = os.path.join(OUTPUT_DIR, "bgv_compliance_report.txt")

with open(report_path, "w") as f:
    f.write(report_text)

print(report_text)
print(f"\n  Saved → {report_path}")
print("\nDone.")
