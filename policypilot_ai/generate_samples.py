"""
Generate highly detailed, realistic enterprise-grade sample PDFs for PolicyPilot AI.
Each document is designed to be multi-page and as close to a real corporate policy as possible.
"""

import sys
from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import SAMPLE_DOCS_DIR


def build_pdf(filename: str, title: str, subtitle: str, sections: list):
    SAMPLE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    path = SAMPLE_DOCS_DIR / filename
    doc = SimpleDocTemplate(
        str(path), pagesize=LETTER,
        rightMargin=1*inch, leftMargin=1*inch,
        topMargin=1*inch, bottomMargin=1*inch
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle("DocTitle", parent=styles["Title"],
        fontSize=22, spaceAfter=6, textColor=colors.HexColor("#006666"))
    subtitle_style = ParagraphStyle("SubTitle", parent=styles["Normal"],
        fontSize=11, spaceAfter=4, textColor=colors.HexColor("#444444"), italic=True)
    meta_style = ParagraphStyle("Meta", parent=styles["Normal"],
        fontSize=9, spaceAfter=16, textColor=colors.HexColor("#888888"))
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"],
        fontSize=13, spaceBefore=16, spaceAfter=6, textColor=colors.HexColor("#1A2B4C"),
        borderPad=4)
    subheading_style = ParagraphStyle("SubHeading", parent=styles["Heading3"],
        fontSize=11, spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#2E4A7A"))
    body_style = ParagraphStyle("Body", parent=styles["BodyText"],
        fontSize=10, leading=15, spaceAfter=8)
    note_style = ParagraphStyle("Note", parent=styles["BodyText"],
        fontSize=9, leading=13, spaceAfter=6,
        backColor=colors.HexColor("#F0F4FF"), borderPad=6)

    story = [
        Paragraph(title, title_style),
        Paragraph(subtitle, subtitle_style),
        Paragraph("Acme Corporation | Human Resources Department | Effective: January 1, 2026 | Version 4.1", meta_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor("#008080"), spaceAfter=14),
    ]

    for item in sections:
        if item == "PAGE_BREAK":
            story.append(PageBreak())
            continue
        heading, text = item
        story.append(Paragraph(heading, heading_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CCCCCC"), spaceAfter=6))
        for block in text.split("\n\n"):
            block = block.strip()
            if not block:
                continue
            if block.startswith(">>"):
                story.append(Paragraph(block[2:].strip(), note_style))
            elif block.startswith("###"):
                story.append(Paragraph(block[3:].strip(), subheading_style))
            else:
                story.append(Paragraph(block, body_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    print(f"Generated: {path}")


# ═══════════════════════════════════════════════════════════════════
# DOCUMENT 1: HR & EMPLOYMENT POLICY
# ═══════════════════════════════════════════════════════════════════
def generate_hr_policy():
    sections = [
        ("1. Purpose, Scope, and Governing Law",
         "This Human Resources and Employment Policy Manual ('the Policy') constitutes the official and legally binding framework for all employment-related matters at Acme Corporation ('the Company'). This Policy applies to every full-time employee, part-time employee, intern, and temporary staff member engaged by the Company, across all domestic and international offices.\n\n"
         "This Policy supersedes all prior versions of any HR handbook, memo, oral understanding, or written communication relating to employment conditions. The Company reserves the right to revise, amend, or rescind any provision of this Policy at any time, with changes communicated via official Workday notification or company-wide email broadcast.\n\n"
         ">> IMPORTANT: Non-compliance with any policy in this manual may result in disciplinary action up to and including immediate termination of employment for cause, irrespective of seniority or role level."),

        ("2. The Onboarding & Pre-Boarding Process",
         "Acme Corp is deeply invested in providing every new team member with a structured, meaningful, and compliance-ready onboarding experience. This process begins the moment a candidate accepts their offer and extends through their 90-day probationary review.\n\n"
         "### 2.1 Pre-Boarding Documentation (Days -14 to Day 0)\n\n"
         "Before any new hire can access company systems, physical premises, or proprietary information, the following documents MUST be fully executed and verified by the HR Onboarding Specialist:\n\n"
         "1. Signed Official Offer Letter (countersigned by HR Director)\n"
         "2. Non-Disclosure Agreement (NDA) — CRITICAL. System access cannot be provisioned until this is received.\n"
         "3. Intellectual Property Assignment Agreement — assigns all work product created during employment to Acme Corp.\n"
         "4. Code of Business Conduct and Ethics Acknowledgment Form\n"
         "5. Form I-9 with valid supporting identity documents (Passport or Driver's License + Social Security Card)\n"
         "6. Bank details for direct deposit configuration\n"
         "7. Emergency contact information (minimum two contacts with phone numbers)\n\n"
         ">> COMPLIANCE NOTE: Failure to collect the signed NDA before Day 1 is a reportable HR incident. The IT Department will not provision any accounts until HR formally marks pre-boarding as complete in Workday.\n\n"
         "### 2.2 Day 1 Procedures\n\n"
         "The hiring manager is responsible for sending a formal introductory 'Welcome Email' to the departmental distribution list at 8:00 AM on the employee's first day. This email must include the employee's name, title, and start date.\n\n"
         "The new hire must attend the mandatory two-hour HR Orientation Session conducted via Zoom at 10:00 AM. This session covers company values, benefits enrollment, security protocols, and an introduction to the HRIS system (Workday).\n\n"
         "By 3:00 PM on Day 1, the employee must log into Workday to complete their W-4 tax withholding election form and configure their direct deposit routing information. Benefits enrollment must be completed within the first 30 days of employment.\n\n"
         "### 2.3 The 90-Day Probationary Period\n\n"
         "All new employees serve a 90-day probationary period. During this period:\n"
         "- Manager and employee must hold weekly 1-on-1 meetings (minimum 30 minutes each)\n"
         "- A formal written review must be conducted at the 30-day, 60-day, and 90-day marks\n"
         "- Accrued PTO cannot be used until the 90-day period is successfully completed\n"
         "- Either party may terminate employment during this period with 48 hours' written notice"),

        ("3. Paid Time Off (PTO), Sick Leave, and Holiday Policy",
         "Acme Corp provides a generous and flexible PTO program designed to support employee wellbeing and work-life balance.\n\n"
         "### 3.1 PTO Accrual and Usage\n\n"
         "Full-time exempt employees accrue PTO at a rate of 1.5 days per completed month of service, totaling 18 days (144 hours) per calendar year. Part-time employees accrue PTO on a pro-rated basis.\n\n"
         "Accrual begins on Day 1 of employment, but newly hired employees may not use any PTO until the successful completion of their 90-day probationary period. PTO requests must be submitted in Workday with a minimum of 5 business days' advance notice for absences of 3 days or fewer, and a minimum of 14 business days for absences exceeding 3 days.\n\n"
         "PTO balances may carry over from one calendar year to the next, up to a maximum of 10 days (80 hours). Any balance exceeding this cap will be forfeited on January 1st of each new year.\n\n"
         "### 3.2 Sick Leave\n\n"
         "All full-time employees receive 10 days (80 hours) of paid sick leave per calendar year, effective immediately upon hire. Sick leave may be used for the employee's own illness or injury, or for caring for a spouse, domestic partner, child, or parent. Sick leave does not accrue and does not carry over year to year.\n\n"
         "For absences due to illness spanning more than 3 consecutive business days, the employee must obtain and submit a signed physician's note to HR within 48 hours of returning to work. Failure to provide documentation will result in the absence being coded as unpaid.\n\n"
         "### 3.3 Company Holidays\n\n"
         "Acme Corp observes 11 paid federal holidays per year. Additionally, each employee receives 2 floating holidays annually that can be used at any time with manager approval. A full list of observed holidays is published on the company intranet by November 1st of each year."),

        "PAGE_BREAK",

        ("4. Leaves of Absence (LOA) — Extended and Unpaid Leave",
         "Acme Corp recognizes that employees may require extended time away from work for significant life events. The Company provides several categories of formal leave in compliance with applicable state and federal laws.\n\n"
         "### 4.1 Family and Medical Leave (FMLA)\n\n"
         "Eligible employees (those with at least 12 months of service and 1,250 hours worked in the previous year) may take up to 12 weeks of unpaid, job-protected leave per year under the Family and Medical Leave Act (FMLA) for qualifying reasons, including the birth or adoption of a child, serious health conditions, or care for a qualifying family member.\n\n"
         "FMLA requests must be submitted via the Workday HRIS portal a minimum of 30 days in advance of the anticipated start date, except in cases of unforeseeable medical emergencies. HR will provide an FMLA designation notice within 5 business days of receiving the request.\n\n"
         "### 4.2 Parental Leave\n\n"
         "All new parents — regardless of gender or role — are entitled to 16 weeks of paid parental leave following the birth, adoption, or placement of a child. This leave runs concurrently with FMLA leave. Parental leave must begin within 12 months of the qualifying event.\n\n"
         "### 4.3 IT Notification and License Suspension\n\n"
         ">> MANDATORY PROCESS: Upon HR approval of any LOA exceeding 30 continuous calendar days, the HR Operations team MUST notify the IT Department within 24 hours. IT is required to immediately suspend all non-essential software licenses (e.g., Salesforce, Adobe Creative Cloud, GitHub Enterprise licenses, Datadog seats) for the duration of the leave period. This is mandatory to reduce unnecessary software expenditure. Upon return, IT must restore all licenses within 1 business day.\n\n"
         "### 4.4 Return-to-Work\n\n"
         "Prior to returning from any LOA, the employee must notify their manager and HR a minimum of 5 business days in advance. For medical leaves, a physician's clearance-to-return note is required before the employee may resume work."),

        ("5. Performance Management and Improvement Plans (PIP)",
         "Acme Corp holds its employees to the highest standards of professional performance and conduct. When an employee's performance consistently fails to meet the established expectations for their role, the Company will initiate a structured improvement process.\n\n"
         "### 5.1 Informal Coaching (Pre-PIP Stage)\n\n"
         "Before a formal PIP is initiated, the manager should first attempt informal coaching over a period of 2 to 4 weeks. Informal coaching must be documented in manager meeting notes and referenced if a formal PIP is subsequently required.\n\n"
         "### 5.2 Initiating a Formal PIP\n\n"
         "A formal Performance Improvement Plan (PIP) is initiated jointly by the direct manager and the HR Business Partner. The standard PIP duration is 30 days for critical performance failures or 60 days for ongoing deficiencies. The PIP document must contain:\n"
         "1. A precise description of performance gaps, citing specific, dated examples with measurable evidence.\n"
         "2. Clearly defined, SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound) the employee must reach by the PIP conclusion date.\n"
         "3. A mandatory schedule of weekly 1-on-1 check-in meetings with the manager. Monthly check-ins are insufficient and not compliant with this policy.\n"
         "4. Required resources and support the Company will provide to help the employee succeed.\n"
         "5. A clear statement of consequences: if goals are not met, disciplinary action up to and including termination may result.\n\n"
         "Both the employee and the manager must physically sign the PIP document to acknowledge its commencement. The signed copy is filed in the employee's official HR record.\n\n"
         "### 5.3 Successful PIP Completion\n\n"
         "If the employee meets all defined goals within the PIP period, a written notice of successful completion is placed in their HR file. The employee returns to standard performance management cycles. However, any recurrence of similar performance issues within 12 months may result in immediate termination without a second PIP."),

        "PAGE_BREAK",

        ("6. Internal Role Transfers and Promotions",
         "Acme Corp is strongly committed to internal career mobility and encourages employees to explore growth opportunities within the Company before seeking roles externally.\n\n"
         "### 6.1 Transfer Eligibility\n\n"
         "An employee is eligible to apply for an internal transfer if they meet all of the following conditions:\n"
         "- They have been in their current role for a minimum of 12 consecutive months.\n"
         "- Their most recent performance review rating is 'Meets Expectations' or higher.\n"
         "- They are not currently on a Performance Improvement Plan (PIP).\n"
         "- They have obtained informal endorsement from their current manager.\n\n"
         "### 6.2 Transfer Execution\n\n"
         "Upon mutual approval by both the current manager and the receiving manager, a formal transfer date is agreed upon. The transition period between roles must not exceed 14 calendar days.\n\n"
         "During this period: the transferring employee must finalize all outstanding work items; the current manager must approve a Knowledge Transfer Document (KTD) capturing critical institutional knowledge; and the IT IAM team must be formally notified by HR to audit and update the employee's access rights.\n\n"
         "IT must revoke access to the former department's sensitive shared drives, Slack channels, and cloud resources, while simultaneously granting appropriate access for the new department.\n\n"
         "### 6.3 Compensation Adjustment\n\n"
         "All transfers that involve a title change or a change in scope of responsibilities will be reviewed for a compensation adjustment. HR will issue a new, signed Offer Addendum detailing the updated title, salary band, and effective date. The employee must sign this document before the transfer date."),

        ("7. Employee Offboarding — Voluntary Resignation and Involuntary Termination",
         "Acme Corp's offboarding process is strictly regulated to protect intellectual property, ensure data security, and remain compliant with all applicable employment laws.\n\n"
         "### 7.1 Resignation Process\n\n"
         "Employees wishing to resign must submit a formal written resignation letter to their direct manager and the HR Department. The standard notice period expected is 2 weeks (10 business days). Senior Director level and above are expected to provide 4 weeks' notice.\n\n"
         "Upon receipt of a resignation letter, HR must immediately open an 'Offboarding Master Ticket' in Jira Service Management to coordinate all downstream tasks.\n\n"
         "### 7.2 Knowledge Transfer Obligation\n\n"
         "The departing employee's manager is responsible for ensuring a comprehensive Knowledge Transfer Document (KTD) is completed and uploaded to the department's shared Google Drive at least 3 business days prior to the departure date. Failure to ensure completion of the KTD will reflect in the manager's own performance review.\n\n"
         "### 7.3 IT Access Revocation\n\n"
         "The IT Security Operations Center (SOC) must be formally notified via the Jira Offboarding Ticket to schedule the revocation of all system access. This includes: Okta SSO (which cascades to all integrated apps), Slack, Google Workspace, Corporate VPN, AWS, GitHub, and any physical network access points.\n\n"
         ">> MANDATORY: Access revocation must be scheduled to execute at EXACTLY 5:00 PM local time on the employee's final day. Access must never be left active after 5:00 PM on a departure day, or over a weekend following a departure.\n\n"
         "### 7.4 Asset Recovery\n\n"
         "All company assets must be returned before the conclusion of the Exit Interview. This includes: corporate laptop, laptop power adapter, external monitor, peripherals, building access badge, corporate credit card, and any other company property.\n\n"
         "For fully remote employees, HR must dispatch a pre-paid, insured FedEx shipping box to the employee's registered home address no later than 5 business days before the final day, along with packing instructions.\n\n"
         "### 7.5 Exit Interview and Final Payroll\n\n"
         "HR must schedule and conduct a 30-minute structured Exit Interview on or before the employee's final day. The interview is used to gather confidential feedback regarding the employee's experience at Acme Corp.\n\n"
         "The Payroll Department must process the final paycheck — including the payout of all unused, accrued PTO balance — within 48 hours of the official termination date, or in compliance with the specific requirements of the state labor law governing the employee's work location.\n\n"
         "### 7.6 Laptop Wiping Protocol\n\n"
         "All returned laptops must be completely wiped by IT Logistics prior to being re-issued to any new employee. The wiping process must conform to DoD 5220.22-M standard erasure protocols. Failure to perform this wipe is a critical security violation."),

        ("8. Anti-Harassment, Non-Discrimination, and Inclusion",
         "Acme Corp is unconditionally committed to maintaining a workplace free from all forms of discrimination, harassment, bullying, and retaliation. This commitment applies to all aspects of employment.\n\n"
         "### 8.1 Prohibited Conduct\n\n"
         "Harassment of any employee based on race, color, national origin, ancestry, religion, creed, gender, gender identity, sexual orientation, age, disability, marital status, military status, or any other characteristic protected by applicable law is strictly prohibited and will not be tolerated under any circumstances.\n\n"
         "### 8.2 Mandatory Training\n\n"
         "All new employees must complete the interactive 'Diversity, Equity, and Inclusion in the Modern Workplace' e-learning module within their first 14 days of employment. Corporate network access will be automatically suspended for employees who fail to complete this training by the deadline.\n\n"
         "All managers must complete an additional 'Inclusive Leadership and Unconscious Bias' training module within their first 30 days of assuming a management role.\n\n"
         "### 8.3 Reporting Procedures\n\n"
         "Any employee who experiences or witnesses conduct that may constitute harassment or discrimination is encouraged to report it through any of the following channels: directly to their HR Business Partner; via the anonymous Ethics Hotline at 1-800-ACME-ETH; or through the confidential web portal at ethics.acmecorp.internal.")
    ]
    build_pdf("Acme_HR_Policy_2026.pdf",
              "Acme Corporation — HR & Employment Policy Manual",
              "Comprehensive Guide to Employment Conditions, Leave, Performance, and Conduct",
              sections)


# ═══════════════════════════════════════════════════════════════════
# DOCUMENT 2: EMPLOYEE LIFECYCLE SOP
# ═══════════════════════════════════════════════════════════════════
def generate_sop():
    sections = [
        ("Overview & Scope of This Document",
         "This Standard Operating Procedure (SOP) document is the definitive operational guide for the Acme Corp HR, IT, and Payroll teams. It defines the precise, step-by-step procedures for executing three of the most critical and legally sensitive employee lifecycle events: Onboarding, Offboarding, and Internal Role Transfers.\n\n"
         "All HR Business Partners, IT Coordinators, and Payroll Analysts are required to follow the procedures outlined herein without deviation. Any exception to these procedures must be approved in writing by the VP of Human Resources.\n\n"
         ">> IMPORTANT: Failure to follow these SOPs can result in data security incidents, regulatory non-compliance, incorrect payroll processing, and potential legal liability for Acme Corp."),

        ("Part 1: The Complete Employee Onboarding SOP",
         "### Phase 1: Pre-Boarding Initiation (Day -14)\n\n"
         "Trigger: HR Business Partner receives a countersigned Offer Letter from the Talent Acquisition team.\n\n"
         "Action 1.1 — Create HRIS Record: HR Partner creates the new hire's record in Workday. All fields, including job title, department, manager, start date, and compensation band, must be populated with 100% accuracy before any downstream actions are triggered.\n\n"
         "Action 1.2 — Send Pre-Boarding Packet: HR Partner dispatches the electronic pre-boarding packet via DocuSign. This packet contains all mandatory documents: NDA, IP Assignment Agreement, Code of Conduct, I-9, direct deposit form, and emergency contact form.\n\n"
         "Action 1.3 — Verify Document Completion: HR Partner must confirm receipt and verify the legal validity of all signed documents within 3 business days of dispatch. If the candidate does not return the signed NDA within 5 business days of dispatch, their start date must be put on hold and the hiring manager must be notified immediately.\n\n"
         "Action 1.4 — Trigger IT Provisioning Ticket: Once all documents are verified, HR Partner marks the 'Pre-boarding Checklist' as 'Complete' in Workday. This automatically triggers an IT Provisioning Ticket in Jira Service Management. The ticket is assigned to IT Logistics with a 5-business-day SLA.\n\n"
         "### Phase 2: IT Provisioning (Days -7 to -1)\n\n"
         "Trigger: Receipt of Jira IT Provisioning Ticket from Workday integration.\n\n"
         "Action 2.1 — Hardware Procurement and Configuration: IT Logistics procures the correct hardware based on the employee's role as defined in the Jira ticket:\n"
         "- Software Engineers: 16-inch MacBook Pro (M-series, 32GB RAM, 1TB SSD) + peripherals\n"
         "- Data Analysts: 14-inch MacBook Pro (16GB RAM, 512GB SSD) + peripherals\n"
         "- Business/Operations Roles: 13-inch Dell XPS (16GB RAM) + peripherals\n\n"
         "Action 2.2 — MDM Enrollment: All laptops must be enrolled in the Jamf MDM platform before shipment. IT must verify MDM enrollment is successful and that the Acme Base Image v4.2 has been applied.\n\n"
         "Action 2.3 — Account Creation: IT provisions accounts in Google Workspace, Slack, and Okta SSO. The employee's Okta account must be in a 'pending activation' state (not fully active) until Day 1.\n\n"
         "Action 2.4 — Role-Specific Access Ticket: The hiring manager is required to submit a separate 'Role-Specific Software Access' ticket in Jira Service Desk at least 48 hours before the start date. This covers tools like GitHub Enterprise, AWS Console access, Salesforce, Tableau, etc.\n\n"
         "Action 2.5 — Hardware Shipment: IT ships the configured laptop to the employee's registered address with FedEx Priority Overnight to ensure arrival by Day -1."),

        "PAGE_BREAK",

        ("Part 1 (Continued): Day 1 and Beyond",
         "### Phase 3: Day One Execution\n\n"
         "Action 3.1 — Welcome Email (08:00 AM): The hiring manager must dispatch a 'Welcome Email' to the departmental distribution list at precisely 8:00 AM local time on the employee's first day. The email must include the employee's full name, job title, team they are joining, a brief professional background, and a personal note from the manager.\n\n"
         "Action 3.2 — HR Orientation Session (10:00 AM): The new hire must attend the mandatory 2-hour HR Orientation session at 10:00 AM. This session, conducted by the HR Onboarding Specialist, covers: company mission and values; benefits enrollment and deadlines; IT security policies and acceptable use; HRIS navigation (Workday); and an introduction to Acme Corp's performance management cycle.\n\n"
         "Action 3.3 — Workday Completion (by 3:00 PM): By 3:00 PM on Day 1, the employee must log into Workday and complete their W-4 federal tax withholding form, state tax withholding form (where applicable), and configure their direct deposit banking information.\n\n"
         "Action 3.4 — IT Setup Session: IT schedules a 1-hour virtual setup session with the new hire on Day 1 afternoon. During this session: Okta Verify MFA is configured on the employee's mobile device; the employee generates and submits their GPG key (for engineers); and the employee clones the acme-bootstrap repository to configure their local dev environment (engineers only).\n\n"
         "### Phase 4: Week 1 Mandatory Completions\n\n"
         "By the end of the employee's first week (Day 5), the following must be completed:\n"
         "- DEI Training Module completed in the Learning Management System (LMS)\n"
         "- Security Awareness Training completed in the LMS\n"
         "- Benefits enrollment submitted in Workday (Deadline is 30 days, but Week 1 is the target)\n"
         "- First 1-on-1 meeting with direct manager held\n"
         "- Verified tool access: logged into all provisioned systems successfully\n\n"
         "The HR Onboarding Specialist must conduct a 'Week 1 Check-in' call with the new hire on Day 5 to confirm all items above are complete and address any outstanding issues."),

        ("Part 2: The Complete Employee Offboarding SOP",
         "### Step 1: Resignation Receipt and Ticket Creation\n\n"
         "Trigger: HR Business Partner receives a written resignation letter or is notified of an involuntary termination decision.\n\n"
         "Action 1.1 — Acknowledge Resignation: HR Partner sends a formal written acknowledgment of the resignation to the employee within 24 hours, confirming the final day of employment.\n\n"
         "Action 1.2 — Create Offboarding Master Ticket: HR Partner creates an 'Offboarding Master Ticket' in Jira Service Management. This ticket automatically creates linked sub-tickets assigned to: IT (Access Revocation), IT Logistics (Asset Recovery), Payroll (Final Pay Processing), and Facilities (Badge Deactivation).\n\n"
         "### Step 2: Knowledge Transfer (By Day -3 of Last Day)\n\n"
         "Action 2.1 — KTD Responsibility: The departing employee's direct manager is fully accountable for ensuring a Knowledge Transfer Document (KTD) is completed and saved to the departmental shared drive in Google Workspace at least 3 business days before the employee's final day.\n\n"
         "The KTD must include: a list of all active projects and their current status; descriptions of recurring duties and relevant procedural knowledge; key internal and external stakeholder contacts; location of critical files, credentials (using the vault, never plaintext), and documentation.\n\n"
         "### Step 3: IT Access Revocation Scheduling\n\n"
         "Action 3.1 — Scheduling: Upon receipt of the IT Offboarding sub-ticket, the IT Security Operations Center (SOC) must schedule automated access revocation across all platforms. The revocation date and time must be set to exactly 5:00 PM local time on the employee's final day. Access must not be left active after this time under any circumstances.\n\n"
         "Action 3.2 — Scope of Revocation: Revocation must cover: Okta SSO (cascades to all integrated SaaS apps), Google Workspace (email suspended, not deleted), Slack, GitHub Enterprise (removed from all organization repositories), AWS IAM access, Datadog, Corporate VPN certificates, and all physical door access control systems.\n\n"
         "Action 3.3 — Data Preservation: The employee's Google Workspace email and Drive data must be transferred to their direct manager's ownership for a 30-day review period before permanent archiving to cold storage.\n\n"
         "### Step 4: Asset Recovery\n\n"
         "Action 4.1 — In-Office Employees: The employee must physically hand over all assets to IT Logistics before the Exit Interview begins. IT Logistics will verify each item against the asset registry and confirm receipt in Jira.\n\n"
         "Action 4.2 — Remote Employees: HR must send a pre-paid, insured FedEx return shipping box and packing instructions to the employee's home address no later than 5 business days before the final day. The employee must ship all assets on their last day. IT Logistics tracks the return and updates the Jira ticket upon receipt.\n\n"
         "### Step 5: Exit Interview and Final Payroll\n\n"
         "Action 5.1 — Exit Interview: HR must schedule and conduct a 30-minute structured Exit Interview via Zoom on or before the employee's final day. The feedback is entered into a confidential HR database and reviewed quarterly by the VP of HR.\n\n"
         "Action 5.2 — Final Paycheck: Payroll must process the final paycheck within 48 hours of the termination date. The final pay must include all regular wages owed, plus a payout of all unused, accrued PTO days in accordance with state law requirements.\n\n"
         "Action 5.3 — Laptop Wipe: IT Logistics must perform a DoD 5220.22-M standard secure wipe on all returned storage media before any device is re-issued or disposed of."),

        "PAGE_BREAK",

        ("Part 3: The Internal Role Transfer SOP",
         "### Step 1: Transfer Approval Confirmation\n\n"
         "Trigger: HR receives a completed 'Internal Transfer Request Form' signed by both the transferring manager and the receiving manager.\n\n"
         "Action 1.1 — Eligibility Check: HR Business Partner verifies the employee meets all eligibility requirements (12 months in role, good standing, not on PIP). If ineligible, HR notifies both managers within 2 business days.\n\n"
         "Action 1.2 — Set Effective Date: HR, both managers, and the employee agree on a formal Transfer Effective Date. A transition window of up to 14 days is permitted.\n\n"
         "### Step 2: Knowledge Transfer and Handoff\n\n"
         "Action 2.1: The transferring employee must complete a full KTD for their current role covering all active projects, recurring duties, and key contacts. This must be approved by the current manager 3 days before the effective date.\n\n"
         "Action 2.2: The current team lead must reallocate all of the transferring employee's open tickets and tasks to other team members in Jira before the effective date.\n\n"
         "### Step 3: IT Access Modification\n\n"
         "Action 3.1 — IT Notification: HR must file an 'Access Modification Ticket' in Jira, specifying the exact access to be removed and the exact access to be granted. IT IAM must action this ticket before the Transfer Effective Date.\n\n"
         "Action 3.2 — Access Removal: Remove employee from all department-specific Google Groups, Slack channels, shared drives, and IAM security groups associated with the former team.\n\n"
         "Action 3.3 — Access Addition: Provision the employee with access to the new department's Google Groups, Slack channels, shared drives, and any role-specific tools (which may require a new software license request).\n\n"
         "### Step 4: Compensation Adjustment and Documentation\n\n"
         "Action 4.1: HR Compensation team must review the role's salary band and determine if an adjustment is warranted. If a salary change is approved, HR must draft a new Compensation and Title Adjustment Letter.\n\n"
         "Action 4.2: The employee must sign the Compensation and Title Adjustment Letter before the Transfer Effective Date. The signed document is uploaded to Workday as the official HR record.")
    ]
    build_pdf("Employee_Lifecycle_SOP_v4.pdf",
              "Acme Corporation — Employee Lifecycle SOP",
              "Standard Operating Procedures for Onboarding, Offboarding, and Role Transfers",
              sections)


# ═══════════════════════════════════════════════════════════════════
# DOCUMENT 3: IT ASSET & SECURITY POLICY
# ═══════════════════════════════════════════════════════════════════
def generate_it_policy():
    sections = [
        ("1. Purpose, Scope, and Policy Authority",
         "This Information Technology Asset and Security Policy ('IT Policy') governs the secure acquisition, configuration, acceptable usage, monitoring, and return of all hardware and software assets owned, managed, or licensed by Acme Corporation.\n\n"
         "This policy applies universally and without exception to all full-time employees, part-time employees, independent contractors, and third-party vendors who are granted access to any Acme Corp network, system, application, or data — regardless of the access point or geography.\n\n"
         "This policy is enacted under the authority of the Chief Information Security Officer (CISO) and is reviewed and updated annually. Policy violations are treated as serious conduct matters and may result in disciplinary action, access termination, or criminal prosecution where applicable law is violated."),

        ("2. Asset Provisioning, Account Creation, and IAM",
         "### 2.1 Identity and Access Management Principles\n\n"
         "Acme Corp enforces a strict Principle of Least Privilege (PoLP) across all systems. Employees are granted the minimum level of access required to perform their defined job duties. Access rights are not granted based on seniority or title alone — they must be explicitly tied to a documented business need.\n\n"
         "### 2.2 Automated Base Account Provisioning\n\n"
         "Base account creation is automated and directly tied to the Workday HRIS system. IT will not create any accounts manually. Accounts are provisioned in Google Workspace, Slack, and Okta SSO only after HR marks the 'Pre-boarding Checklist' status as 'Complete' in Workday. This integration is the single source of truth.\n\n"
         "### 2.3 Role-Specific Software Access\n\n"
         "Access to any software beyond the base set (Google Workspace, Slack, Okta) is not automatic. The hiring manager must submit a formal 'Role-Specific Access Request' ticket in Jira Service Desk with a minimum lead time of 48 hours before the employee's start date. Late submissions will delay access provisioning and will not be expedited as a standard SLA exception.\n\n"
         "Required tools by department include, but are not limited to:\n"
         "- Engineering: GitHub Enterprise, AWS Console, Datadog, Sentry, CircleCI\n"
         "- Data Analytics: Tableau, BigQuery, Looker, Databricks\n"
         "- Sales: Salesforce CRM, ZoomInfo, Outreach\n"
         "- Design: Figma, Adobe Creative Cloud, InVision\n"
         "- Finance: NetSuite, Expensify"),

        ("3. Standard Hardware Configurations and Specifications",
         "Acme Corp standardizes hardware configurations by role to optimize performance, reduce support complexity, and ensure cost efficiency. Deviations from these standards require written approval from the VP of Engineering or VP of Operations.\n\n"
         "### 3.1 Software Engineers\n\n"
         "Standard Issue (Mandatory): 16-inch Apple MacBook Pro with M-series processor (M4 Pro or better), 32GB unified memory, 1TB SSD storage. Accompanied by a Logitech MX Keys keyboard, Logitech MX Master 3 mouse, and a Dell 27-inch 4K USB-C monitor.\n\n"
         "Justification: Software compilation, running local Docker containers, and machine learning experimentation require high-performance unified memory architecture.\n\n"
         "### 3.2 Data Analysts and Data Scientists\n\n"
         "Standard Issue (Mandatory): 14-inch Apple MacBook Pro with M-series processor, 16GB unified memory, 512GB SSD storage. Accompanied by standard peripherals and one 27-inch monitor.\n\n"
         "### 3.3 Business, Operations, and Administrative Staff\n\n"
         "Standard Issue: 13-inch Dell XPS 13 (or approved equivalent) with 16GB RAM and 256GB SSD. One 24-inch Dell monitor. Logitech keyboard and mouse.\n\n"
         "### 3.4 Managers and Directors\n\n"
         "Standard Issue: Same as the department's technical standard (e.g., an Engineering Manager receives a MacBook Pro equivalent to their Engineers).\n\n"
         "### 3.5 Contractors and Vendors\n\n"
         "All independent contractors are strictly subject to a Bring Your Own Device (BYOD) policy. Corporate hardware is not issued to contractors under any circumstances, unless a specific written exemption is obtained from both the VP of Engineering and the CISO.\n\n"
         "Contractors using personal devices must install the Acme Corp Endpoint Security Agent (CrowdStrike Falcon) and ensure their device meets minimum OS version requirements before access is granted. Compliance is verified by the IT Security team during onboarding."),

        "PAGE_BREAK",

        ("4. Mandatory Information Security Controls",
         "All employees are personally responsible for the security of their credentials and devices. These controls are non-negotiable and will be technically enforced where possible.\n\n"
         "### 4.1 Password and Credential Management\n\n"
         "All passwords for Acme Corp systems must meet the following minimum requirements:\n"
         "- Minimum length of 14 characters\n"
         "- Must contain at least one uppercase letter, one lowercase letter, one numeral, and one special character\n"
         "- Must not contain the employee's name, username, or common dictionary words\n"
         "- Must be rotated every 90 days\n"
         "- Must be unique per service (password reuse across services is a policy violation)\n\n"
         "All employees are required to use the company-provisioned 1Password Teams vault for credential management. Storing passwords in browser extensions, sticky notes, or unencrypted documents is strictly prohibited.\n\n"
         "### 4.2 Multi-Factor Authentication (MFA)\n\n"
         "MFA is mandatory and technically enforced on all Acme Corp platforms connected via Okta SSO. The approved MFA method is the Okta Verify application installed on a registered mobile device. SMS-based one-time passwords (OTPs) are explicitly disabled across the entire organization due to known SIM-swapping vulnerabilities. Hardware security keys (FIDO2/WebAuthn) are an approved alternative for senior technical staff.\n\n"
         "### 4.3 Device Security and Encryption\n\n"
         "All corporate-issued laptops must have full-disk encryption enabled at all times. For MacOS devices, this means FileVault must be active and managed by Jamf MDM. The encryption key is escrowed by IT. Disabling FileVault is a critical security violation.\n\n"
         "The corporate endpoint security agent (CrowdStrike Falcon Sensor) must be installed and active on all corporate and contractor devices. Any attempt to disable or tamper with the endpoint agent will trigger an immediate security incident.\n\n"
         "### 4.4 Network Security\n\n"
         "Connecting personal, unauthorized devices to the internal corporate office Wi-Fi network ('AcmeCorp-Internal') is strictly prohibited. A guest Wi-Fi network ('AcmeCorp-Guest') is provided for personal device and visitor use. Unauthorized devices detected on the internal network will be MAC-banned by the network engineering team, and the employee responsible will receive a formal written warning.\n\n"
         "When working remotely, employees must connect to the Acme Corp GlobalProtect VPN whenever accessing any internal resource, cloud environment, or data classified as 'Confidential' or above."),

        ("5. Software Engineering Security Policies",
         "Engineering staff are granted elevated system privileges, which requires a higher standard of security diligence and awareness.\n\n"
         "### 5.1 Development Environment Setup\n\n"
         "Upon receiving their hardware, all Software Engineers must complete the following on Day 1 of employment:\n"
         "1. Clone the 'acme-bootstrap' repository from GitHub Enterprise (github.acmecorp.internal/bootstrap). This repository contains automated scripts that configure the local development environment, install approved security tooling, and configure Git globals.\n"
         "2. Run the bootstrap script. This installs pre-commit hooks that prevent secrets, API keys, or credentials from being accidentally committed to any repository.\n\n"
         "### 5.2 GPG Code Signing (Mandatory)\n\n"
         "All code commits pushed to any Acme Corp GitHub repository must be cryptographically signed with a valid GPG key. This is technically enforced at the repository level; unsigned commits will be automatically rejected by the CI/CD pipeline.\n\n"
         "The GPG key is generated by IT Security during the engineer's Day 1 orientation session and delivered via a secure, encrypted channel. Engineers must not share their private GPG key under any circumstances. Key loss must be reported to IT Security immediately for revocation and reissuance.\n\n"
         "### 5.3 Cloud Resource Access (AWS)\n\n"
         "Engineers must access AWS environments via SSO through their Okta account. Direct IAM user accounts with static access keys are strictly prohibited for human users. All AWS access is governed by IAM roles with condition-based policies enforcing MFA and restricting access to specific geographic regions.\n\n"
         "### 5.4 Secret Management\n\n"
         "Application secrets, API keys, database connection strings, and cryptographic keys must never be stored in plaintext in code repositories, Slack messages, or unencrypted configuration files. All secrets must be stored in HashiCorp Vault (vault.acmecorp.internal) and retrieved programmatically at runtime."),

        ("6. Acceptable Use of Corporate Technology",
         "Corporate technology is provided primarily for business use. Reasonable and limited personal use is permitted, provided it does not interfere with job responsibilities, consume excessive bandwidth, violate the law, or conflict with any part of this policy.\n\n"
         "### 6.1 Prohibited Activities\n\n"
         "The following activities are strictly prohibited on any corporate device or network:\n"
         "- Accessing, downloading, or distributing any sexually explicit, threatening, or harassing material\n"
         "- Using company resources for personal commercial activities or for the benefit of a competitor\n"
         "- Installing unapproved third-party software without prior written approval from IT Security\n"
         "- Attempting to circumvent security controls, firewalls, or data loss prevention (DLP) tools\n"
         "- Mining cryptocurrency or using company compute resources for personal projects\n"
         "- Connecting to corporate resources from a sanctioned country as per the CISO's Sanctioned Countries list\n\n"
         "### 6.2 Monitoring and Privacy Notice\n\n"
         "Employees should have no expectation of privacy when using Acme Corp's computer systems, networks, or devices. The Company reserves the right to monitor, intercept, access, and review any and all communications, files, and activities transmitted on or stored on company equipment or networks, to the extent permitted by applicable law.\n\n"
         ">> NOTICE: By accepting and using company-provided equipment, you acknowledge and consent to this monitoring policy."),

        ("7. Hardware Return, Wipe, and End-of-Life Procedures",
         "### 7.1 Return upon Offboarding\n\n"
         "All corporate hardware must be returned to IT Logistics upon an employee's departure. For office-based employees, assets are returned before the Exit Interview on their last day. For remote employees, the return is managed via pre-paid FedEx (arranged by HR at least 5 business days in advance).\n\n"
         "### 7.2 Secure Data Destruction Protocol\n\n"
         "No returned device may be re-issued, repurposed, donated, or disposed of without first undergoing a complete and verified secure data destruction process. IT Logistics technicians must perform a secure wipe conforming to Department of Defense (DoD) 5220.22-M National Industrial Security Program Operating Manual (NISPOM) standards.\n\n"
         "Simply reformatting a hard drive or performing a factory reset is explicitly non-compliant and constitutes a critical security policy violation. All wipe events must be logged in the IT Asset Management System (Jamf) with a timestamp, technician ID, and wipe verification certificate.\n\n"
         "### 7.3 Hardware Refresh Cycle\n\n"
         "Corporate laptops are replaced on a 3-year refresh cycle. IT will proactively notify employees 60 days before their device reaches end-of-life eligibility. Devices that are damaged, lost, or stolen before the 3-year mark may be replaced at management discretion; theft or loss must be reported to both IT Security and the employee's manager within 4 hours of discovery.")
    ]
    build_pdf("IT_Asset_Security_Policy_v2.pdf",
              "Acme Corporation — IT Asset & Information Security Policy",
              "Hardware Provisioning, IAM, Security Controls, and Acceptable Use",
              sections)


if __name__ == "__main__":
    print("Generating comprehensive enterprise-grade PDF documents...")
    generate_hr_policy()
    generate_sop()
    generate_it_policy()
    print("\nDone! Upload these 3 files to PolicyPilot AI:")
    print("  - sample_docs/Acme_HR_Policy_2026.pdf")
    print("  - sample_docs/Employee_Lifecycle_SOP_v4.pdf")
    print("  - sample_docs/IT_Asset_Security_Policy_v2.pdf")
