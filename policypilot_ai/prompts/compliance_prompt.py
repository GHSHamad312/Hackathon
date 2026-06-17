from utils.helpers import dedent

COMPLIANCE_SYSTEM_PROMPT = dedent("""
    You are the Corporate Compliance Auditor for PolicyPilot AI.
    Your job is to cross-reference the proposed actions for a given workflow 
    against the actual company policies retrieved from the knowledge base.

    You must output exactly a JSON object with the following schema:
    {
      "compliance_score": int, (0-100, based on how well policies were followed)
      "warnings": [string], (List of policy violations or missing steps found in the actions)
      "missing_requirements": [string] (List of explicit requirements mentioned in the policy that the reasoning agent completely missed)
    }

    Rules:
    1. Be strict. If a policy requires a specific form, approval, or timeline, verify that it is explicitly mentioned in the reasoning actions.
    2. Do NOT invent policies. Only judge based on the provided "Policy Excerpts". If no excerpts exist, give a score of 100 with a warning "No policies found to audit against."
    3. Return ONLY valid JSON.
""")


def build_compliance_user_prompt(
    reasoning_output: dict,
    retrieved_passages: list[dict],
) -> str:
    """Build the prompt for the Compliance Agent."""
    import json
    
    # Format retrieved passages nicely
    if not retrieved_passages:
        policy_text = "No policy documents found."
    else:
        policy_text = "\n\n---\n\n".join(
            f"[Source: {p.get('source', 'unknown')}]\n{p.get('text', '')}"
            for p in retrieved_passages
        )
        
    return dedent(f"""
        ## 1. Proposed Workflow Actions
        {json.dumps(reasoning_output.get("actions", []), indent=2)}
        
        ## 2. Policy Excerpts (Source of Truth)
        {policy_text}
        
        Audit the proposed actions against the policy excerpts. Identify any violations or missing mandatory steps.
    """)
