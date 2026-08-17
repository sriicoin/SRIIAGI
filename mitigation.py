# mitigation.py - Defense and mitigation filters for LLM outputs

def apply_output_filter(response: str) -> str:
    """
    Filters out dangerous content or returns a safe fallback message
    if the model accidentally generates malicious content.
    """
    danger_keywords = ["phishing", "ransomware", "malware", "exploit"]
    response_lower = response.lower()
    
    for word in danger_keywords:
        if word in response_lower and len(response) > 100:
            # If malicious content detected, override with a safe response
            return "[Blocked by SRIIAGI Mitigation Filter]: Output contained restricted or harmful material."
            
    return response