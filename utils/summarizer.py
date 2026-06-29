import google.generativeai as genai
from dotenv import load_dotenv
import re
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    API_KEY = "AIzaSyBxo0ms2JwNdfDJm-GRitUU8Y89DRDEzYA"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def clean_response(text: str) -> str:
    """Strip markdown fences and whitespace from model output."""
    text = text.strip()
    # Remove ```html ... ``` or ``` ... ```
    text = re.sub(r'^```[a-zA-Z]*\n?', '', text)
    text = re.sub(r'\n?```$', '', text)
    text = text.strip()
    return text


def summarize_with_gemini(text: str) -> str:
    if len(text.strip()) < 40:
        return '<p class="text-gray-400 text-sm text-center py-8">Not enough content to summarize.</p>'

    prompt = """You are a senior editor at The Economist. Summarize the article below as a structured HTML briefing.

Return ONLY this HTML, nothing else, no markdown, no code fences:

<div class="sn-bottom-line">
<span class="sn-label">Bottom Line</span>
<p>WRITE ONE SENTENCE: what happened, who is involved, why it matters now.</p>
</div>
<div class="sn-facts">
<span class="sn-label">Key Facts</span>
<ul>
<li>FACT ONE with specific name or number</li>
<li>FACT TWO with specific name or number</li>
<li>FACT THREE with specific name or number</li>
<li>FACT FOUR with specific name or number</li>
</ul>
</div>
<div class="sn-context">
<span class="sn-label">Context</span>
<p>WRITE 2-3 SENTENCES about background and broader significance.</p>
</div>
<div class="sn-watch">
<span class="sn-label">What to Watch</span>
<p>WRITE ONE SENTENCE about the next key development to monitor.</p>
</div>

Rules:
- Replace ALL CAPS placeholders with real content from the article
- Never invent facts not in the article
- Each fact bullet starts with a verb
- Tone: precise, neutral, authoritative
- Output ONLY the 4 divs above, nothing before or after

ARTICLE:
""" + text[:5000]

    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.2, "max_output_tokens": 900}
        )
        raw = clean_response(response.text)

        # Validate output contains our expected divs
        if 'sn-bottom-line' not in raw and 'sn-facts' not in raw:
            # Model returned unexpected format — wrap whatever it returned
            return f'<div class="sn-context"><span class="sn-label">Summary</span><p>{raw}</p></div>'

        return raw

    except Exception as e:
        return f'<div class="sn-watch"><span class="sn-label">Error</span><p>{str(e)}</p></div>'


def research_topic(topic: str) -> str:
    prompt = f"""You are a senior correspondent at a world-class news organization.
The user searched for "{topic}" but no articles were found.

Write a professional, informative briefing (4–6 sentences). Cover:
- What this topic is
- Why it matters
- Its current global relevance

Rules: plain prose only, no headers, no bullets, no markdown.
End with exactly: "Note: This is an AI-generated briefing based on general knowledge, not a live news article."

Topic: {topic}"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.4, "max_output_tokens": 500}
        )
        return response.text.strip()
    except Exception as e:
        return f"Error generating briefing: {str(e)}"
