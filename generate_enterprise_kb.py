import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib import colors

domains = ["hr", "finance", "support", "privacy", "legal"]
for d in domains:
    os.makedirs(f"data/{d}", exist_ok=True)

def create_pdf(filename, title, department, code, content_sections):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor("#002B49"), spaceAfter=6)
    meta_style = ParagraphStyle('DocMeta', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor("#555555"), spaceAfter=12)
    h1_style = ParagraphStyle('SectionH1', parent=styles['Heading2'], fontSize=12, leading=15, textColor=colors.HexColor("#002B49"), spaceBefore=12, spaceAfter=6)
    body_style = ParagraphStyle('BodyTextCustom', parent=styles['BodyText'], fontSize=10, leading=14, textColor=colors.HexColor("#222222"), spaceAfter=8)

    story = [
        Paragraph("<b>KOHLER CO. ENTERPRISE COMPLIANCE & POLICY DOCUMENTATION</b>", meta_style),
        Paragraph(title, title_style),
        Paragraph(f"<b>Department:</b> {department} | <b>Doc Ref:</b> {code} | <b>Effective:</b> 2026-01-01", meta_style),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#002B49"), spaceAfter=12)
    ]
    
    for sec_title, sec_text in content_sections:
        story.append(Paragraph(sec_title, h1_style))
        story.append(Paragraph(sec_text, body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)
    print(f"Generated PDF: {filename}")

create_pdf("data/hr/Kohler_HR_Policy_2026.pdf", "HR Policy & Benefits Guide", "Human Resources", "KOH-HR-2026", [
    ("1. Leave Entitlements", "Full-time employees accrue 20 business days of paid annual leave per calendar year. Sick leave accrues at 1 day per working month."),
    ("2. Remote Work Policy", "Eligible employees are permitted up to 2 remote workdays per week subject to manager sign-off.")
])

create_pdf("data/finance/Kohler_Finance_Guidelines_2026.pdf", "Travel & Procurement Guidelines", "Finance", "KOH-FIN-2026", [
    ("1. Travel Expenses", "Daily meal allowance during domestic travel is capped strictly at $75 USD per day. Flights under 6 hours must be Economy Class."),
    ("2. Expense Approvals", "Expense reports must be filed within 14 calendar days post-trip with itemized receipts for items over $25 USD.")
])

create_pdf("data/support/Kohler_Customer_Support_Manual.pdf", "Product Warranty & Returns", "Customer Support", "KOH-SUP-2026", [
    ("1. Warranty Coverage", "Kohler plumbing fixtures and touchless faucets carry a Limited Lifetime Warranty for original residential owners."),
    ("2. Return Window", "Standard returns for direct purchases must be initiated within 30 days of delivery in original packaging.")
])

create_pdf("data/privacy/Kohler_Data_Privacy_Policy.pdf", "Data Protection Policy", "Privacy & Compliance", "KOH-PRIV-2026", [
    ("1. Privacy Standards", "Kohler processes personal information strictly in compliance with GDPR and CCPA guidelines. Personal data is never sold to third parties."),
    ("2. Access Requests", "Data Subject Access Requests (DSAR) must be serviced by the Privacy Office within 30 calendar days.")
])

create_pdf("data/legal/Kohler_Legal_Code_of_Conduct.pdf", "Legal Code of Conduct", "Legal", "KOH-LEG-2026", [
    ("1. Non-Disclosure & IP", "Employees are bound by NDAs regarding non-public technological innovations and proprietary designs."),
    ("2. Gifts Policy", "Gifts from vendors or third parties exceeding $100 USD in value require explicit compliance office authorization.")
])

print("\n--- All 5 Domain PDFs successfully created! ---")