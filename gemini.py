import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-2.0-flash-exp")

VALID = {"present", "absent_permitted", "coming_late", "absent_no_reason"}

_PROMPT = """You are an attendance classifier for an office in Uzbekistan.
A worker sent this message in response to "are you at work today?":
"{text}"

Classify into exactly one of these:
- present → at work / already there / confirmed attendance
- absent_permitted → has permission, gave a reason, sick, vacation, official business
- coming_late → on the way, will be late, coming soon
- absent_no_reason → said no without reason, unclear, or off-topic

Reply with ONLY one word: present, absent_permitted, coming_late, or absent_no_reason"""

def classify_response(text: str) -> str:
    try:
        r = _model.generate_content(_PROMPT.format(text=text))
        result = r.text.strip().lower().split()[0]
        return result if result in VALID else "absent_no_reason"
    except Exception:
        return "absent_no_reason"
