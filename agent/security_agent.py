import json
import os
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

def analyze_security_input(user_input):
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""You are an expert cybersecurity analyst. Analyze this security input and respond ONLY with a valid JSON object, no extra text:

{{
  "severity": "CRITICAL or HIGH or MEDIUM or LOW",
  "category": "threat category here",
  "summary": "one sentence description",
  "affected_assets": ["asset1", "asset2"],
  "indicators_of_compromise": ["ioc1", "ioc2"],
  "recommended_actions": ["action1", "action2", "action3"],
  "compliance_impact": "ISO 27001/NIST impact",
  "confidence_score": "HIGH or MEDIUM or LOW",
  "analyst_notes": "additional context"
}}

Security input to analyze:
{user_input}"""

    data = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
    
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

def main():
    print("\n🔐 AI Security Triage Agent (Powered by Gemini)")
    print("="*50)
    print("Paste your security input and press Enter twice:\n")
    
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    user_input = "\n".join(lines)
    print("\n⏳ Analyzing with Gemini AI...\n")
    
    result = analyze_security_input(user_input)
    
    print("="*50)
    print(f"SEVERITY:    {result['severity']}")
    print(f"CATEGORY:    {result['category']}")
    print(f"SUMMARY:     {result['summary']}")
    print(f"CONFIDENCE:  {result['confidence_score']}")
    print("\nRECOMMENDED ACTIONS:")
    for i, action in enumerate(result['recommended_actions'], 1):
        print(f"  {i}. {action}")
    print(f"\nCOMPLIANCE:  {result['compliance_impact']}")
    print(f"NOTES:       {result['analyst_notes']}")
    print("="*50)

if __name__ == "__main__":
    main()