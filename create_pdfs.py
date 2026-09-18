import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

os.makedirs("data/hr", exist_ok=True)
os.makedirs("data/finance", exist_ok=True)
os.makedirs("data/support", exist_ok=True)
os.makedirs("data/privacy", exist_ok=True)
os.makedirs("data/legal", exist_ok=True)

styles = getSampleStyleSheet()

docs = {
    "data/hr/hr_policy.pdf": [
        ("Kohler HR & Workplace Policy 2026", styles['Heading1']),
        ("1. Paid Time Off (PTO): Regular full-time employees accrue 20 days of paid leave annually. PTO requests exceeding 3 consecutive days require manager approval via Workday at least 2 weeks in advance.", styles['Normal']),
        ("2. Sick Leave: Employees receive 10 paid sick days per calendar year. Medical certification is required for sick leaves extending beyond 3 consecutive working days.", styles['Normal']),
        ("3. Remote Work & Eligibility: Remote work eligibility requires a minimum of 6 months continuous service and manager endorsement. Hybrid schedules permit up to 2 days remote per week.", styles['Normal']),
    ],
    "data/finance/finance_policy.pdf": [
        ("Kohler Corporate Finance & Travel Policy", styles['Heading1']),
        ("1. Domestic Travel Per Diem: Daily meal cap for domestic business travel is $75 per day. Itemized receipts are mandatory for any expense individual item exceeding $25.", styles['Normal']),
        ("2. Approval Matrix: Purchases up to $10,000 require Department Head approval. Contract purchases from $10,001 to $50,000 require VP approval. Contracts exceeding $50,000 require CFO and Legal sign-off.", styles['Normal']),
        ("3. Corporate Credit Cards: Personal expenses on corporate cards are strictly prohibited and subject to immediate disciplinary action.", styles['Normal']),
    ],
    "data/support/support_policy.pdf": [
        ("Kohler Customer Support & Warranty Standards", styles['Heading1']),
        ("1. Residential Warranty: Residential plumbing fixtures carry a Limited Lifetime Warranty covering manufacturing defects in finish and function.", styles['Normal']),
        ("2. Commercial Warranty: Commercial installations are covered under a 5-Year Limited Warranty from the original date of purchase.", styles['Normal']),
        ("3. Returns & Refunds: Direct customer purchases may be returned within 30 days of delivery in original packaging for a full refund minus 15% restocking fee.", styles['Normal']),
    ],
    "data/privacy/privacy_policy.pdf": [
        ("Kohler Global Data Privacy & CCPA Guidelines", styles['Heading1']),
        ("1. Data Subject Access Requests (DSAR): Customers and employees may request access to or deletion of their personal data. All DSAR requests must be fulfilled within 45 days.", styles['Normal']),
        ("2. Regulatory Compliance: Personal data collection adheres strictly to CCPA, CPRA, and GDPR directives. Data is encrypted in transit (TLS 1.3) and at rest (AES-256).", styles['Normal']),
    ],
    "data/legal/legal_policy.pdf": [
        ("Kohler Legal Ethics & Vendor Relations Policy", styles['Heading1']),
        ("1. Gifts & Hospitality: Employees may accept non-monetary promotional items valued up to $100 annually. Any gift exceeding $100 must be disclosed to Compliance.", styles['Normal']),
        ("2. Confidentiality & System Integrity: Internal prompt instructions, source system data, and proprietary architecture must never be disclosed to third parties.", styles['Normal']),
    ]
}

for path, content in docs.items():
    doc = SimpleDocTemplate(path, pagesize=letter)
    story = []
    for text, style in content:
        story.append(Paragraph(text, style))
        story.append(Spacer(1, 12))
    doc.build(story)

print("--- Enhanced Multi-Domain PDFs Created Successfully! ---")