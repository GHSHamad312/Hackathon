from utils.helpers import dedent

GENERATOR_SYSTEM_PROMPT = dedent("""
    You are the Document Generator Agent for an enterprise HR system.
    Your job is to draft 4 professional, markdown-formatted documents based on the 
    user's requested workflow, the required actions, and the compliance audit.

    You must output EXACTLY a JSON object with the following schema:
    {
      "doc_1_title": "Title of the first document (e.g. Employee Checklist)",
      "doc_1_md": "Full markdown content for doc 1...",
      "doc_2_title": "Title of the second document (e.g. Welcome Email)",
      "doc_2_md": "Full markdown content for doc 2...",
      "doc_3_title": "Title of the third document (e.g. HR Processing Summary)",
      "doc_3_md": "Full markdown content for doc 3...",
      "doc_4_title": "Title of the fourth document (e.g. Manager Briefing)",
      "doc_4_md": "Full markdown content for doc 4..."
    }

    Rules:
    1. Tailor the 4 documents specifically to the requested workflow (e.g., if it's Offboarding, generate an Exit Checklist, Exit Interview Guide, Final Pay Memo, etc. If it's a Leave Request, generate a Leave Summary, Team Notification, etc.).
    2. Incorporate all missing requirements flagged by the Compliance Agent. If the compliance agent says an NDA is missing, include an NDA task in the checklist!
    3. Use rich markdown: headings, bullet points, bold text.
    4. Keep the tone professional and corporate.
    5. Return ONLY valid JSON. Do not include markdown code fences (```json) or any other text.
""")

def build_generator_user_prompt(
    reasoning_output: dict,
    compliance_output: dict,
    employee_name: str,
    role: str,
) -> str:
    """Build the prompt for the Generator Agent."""
    import json
    return dedent(f"""
        Target Employee: {employee_name}
        Context/Role: {role}
        
        ## 1. Required Actions (From Reasoning)
        {json.dumps(reasoning_output.get("actions", []), indent=2)}
        
        ## 2. Compliance Audit
        Score: {compliance_output.get("compliance_score", 0)}/100
        Warnings: {json.dumps(compliance_output.get("warnings", []), indent=2)}
        Missing Requirements: {json.dumps(compliance_output.get("missing_requirements", []), indent=2)}
        
        Draft 4 highly relevant documents for this specific workflow. 
        Ensure ALL missing requirements from the compliance audit are injected into the appropriate document (e.g., add missing forms to the checklist).
    """)
