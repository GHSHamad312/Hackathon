from utils.helpers import dedent

ACTION_SYSTEM_PROMPT = dedent("""
    You are the Action Simulator Agent for an enterprise workflow system.
    Your job is to read the auto-generated workflow documents and determine which 
    downstream systems need to be triggered, and what their status is.

    Output a JSON object mapping the action name to its status.
    For example:
    {
      "it_access_revocation": "submitted",
      "exit_interview_scheduled": "ready",
      "manager_notification": "sent"
    }

    Rules:
    1. Keep action keys strictly snake_case.
    2. Statuses should be one of: "created", "ready", "submitted", "sent", "skipped".
    3. Output 4-6 highly relevant simulated actions based strictly on the content of the provided documents.
    4. Return ONLY valid JSON.
""")

def build_action_user_prompt(generated_docs: dict) -> str:
    """Build the prompt for the Action Agent."""
    import json
    
    docs_summary = []
    for i in range(1, 5):
        title = generated_docs.get(f"doc_{i}_title", "")
        content = generated_docs.get(f"doc_{i}_md", "")
        if title and content:
            docs_summary.append(f"### {title}\n{content[:500]}...")  # Just first 500 chars to save context
            
    return dedent(f"""
        Please review the following generated documents and simulate the downstream enterprise actions.
        
        {chr(10).join(docs_summary)}
    """)
